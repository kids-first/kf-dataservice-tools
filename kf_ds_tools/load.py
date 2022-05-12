from kf_utils.dataservice.meta import get_endpoint

import requests

from kf_ds_tools.common.logging import get_logger
from kf_ds_tools.common.utils import clean_response_body

logger = get_logger(__name__, testing_mode=False, log_format="detailed")


def load_kf_id(target, body):
    """Load the given information into the target dataservice

    :param target: url of target dataservice
    :type target: str
    :param body: json -style payload to load into the target dataservice
    :type body: dict
    """
    kf_id = body["kf_id"]
    logger.debug(f"begining load stage for {kf_id}")
    endpoint = get_endpoint(kf_id)
    logger.debug(f"endpoint: {endpoint}")
    clean_body = clean_response_body(body)
    if endpoint == "participants":
        _, _, clean_body["study_id"] = body["_links"]["study"].rpartition("/")
    elif endpoint == "family-relationships":
        _, _, clean_body["participant1_id"] = body["_links"][
            "participant1"
        ].rpartition("/")
        _, _, clean_body["participant2_id"] = body["_links"][
            "participant2"
        ].rpartition("/")
    elif endpoint in (
        "outcomes",
        "diagnoses",
        "biospecimens",
        "phenotypes",
    ):
        _, _, clean_body["participant_id"] = body["_links"][
            "participant"
        ].rpartition("/")
        if endpoint == "biospecimens":
            _, _, clean_body["sequencing_center_id"] = body["_links"][
                "sequencing_center"
            ].rpartition("/")
    elif endpoint == "sequencing-experiments":
        _, _, clean_body["sequencing_center_id"] = body["_links"][
            "sequencing_center"
        ].rpartition("/")
    elif endpoint == "biospecimen-diagnoses":
        _, _, clean_body["biospecimen_id"] = body["_links"][
            "biospecimen"
        ].rpartition("/")
        _, _, clean_body["diagnosis_id"] = body["_links"][
            "diagnosis"
        ].rpartition("/")
    elif endpoint in (
        "sequencing-experiment-genomic-files",
        "biospecimen-genomic-files",
        "read-group-genomic-files",
    ):
        _, _, clean_body["genomic_file_id"] = body["_links"][
            "genomic_file"
        ].rpartition("/")
        if endpoint == "sequencing-experiment-genomic-files":
            _, _, clean_body["sequencing_experiment_id"] = body["_links"][
                "sequencing_experiment"
            ].rpartition("/")
        elif endpoint == "biospecimen-genomic-files":
            _, _, clean_body["biospecimen_id"] = body["_links"][
                "biospecimen"
            ].rpartition("/")
        elif endpoint == "read-group-genomic-files":
            _, _, clean_body["read_group_id"] = body["_links"][
                "read_group"
            ].rpartition("/")
    logger.debug("cleaning of body complete")
    logger.info("loading " + kf_id + " into " + target + endpoint + "/")
    resp = requests.post(
        target + endpoint + "/",
        headers={"Content-Type": "application/json"},
        json=clean_body,
    )
    if resp.status_code == 201:
        logger.info(resp.json()["_status"]["message"])
    elif resp.status_code != 201:
        logger.warning(kf_id + " - " + resp.json()["_status"]["message"])
