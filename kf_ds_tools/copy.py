"""
Copies contents of prd dataservice to local dataservice for a particular study
"""


from kf_utils.dataservice.descendants import find_descendants_by_kfids
from kf_utils.dataservice.meta import get_endpoint

import requests

from kf_ds_tools.common.logging import get_logger
from kf_ds_tools.common.utils import clean_response_body
from kf_ds_tools.etl.extract import get_kf_ids
from kf_ds_tools.etl.load import load_kf_id

logger = get_logger(__name__, testing_mode=False, log_format="detailed")


def sequencing_center_handler(source, target):
    """Check to make sure that all sequencing centers in source are in target.
    If a sequencing center is not in the target, loads all the source
    sequencing centers into target.

    :param source: url of source dataservice
    :type source: str
    :param target: url of target dataservice
    :type target: str
    """
    logger.info("checking to make sure all sequencing centers are present")
    src_centers = requests.get(
        (source + "sequencing-centers?limit=100"),
        headers={"Content-Type": "application/json"},
    ).json()
    target_centers = requests.get(
        (target + "sequencing-centers?limit=100"),
        headers={"Content-Type": "application/json"},
    ).json()
    if src_centers["total"] == 0:
        logger.warning("No sequencing centers discovered in source.")
        src_centers = None
    else:
        src_centers = [clean_response_body(c) for c in src_centers["results"]]
    if target_centers["total"] == 0:
        logger.info("No sequencing centers discovered in target.")
        target_centers = None
    else:
        target_centers = [
            clean_response_body(c) for c in target_centers["results"]
        ]
    if src_centers:
        if not target_centers:
            logger.info("will load all sequencing centers from source")
            load_these = src_centers
        else:
            load_these = []
            for s_center in src_centers:
                if s_center.get("kf_id") not in [
                    t.get("kf_id") for t in target_centers
                ]:
                    load_these.append(s_center)
                    logger.info(f"will load: {s_center.get('kf_id')}")
        if len(load_these) > 0:
            for center in load_these:
                load_kf_id(target, center)


def copy_kf_ids(source, target, kf_id_list):
    """Copy a list of things from a source dataservice to a target dataservice

    param source: url of source dataservice
    :type source: str
    :param target: url of target dataservice
    :type target: str
    :param kf_id_list: kf_ids of things to copy
    :type kf_id_list: list
    """
    logger.info("querying source for kf_ids")
    kf_id_info = get_kf_ids(source, kf_id_list)
    logger.info("loading into target")
    for entity in kf_id_info:
        load_kf_id(target, entity)


def copy_all_descendants(source, target, kf_id):
    """copy a kf_id and all of its desendants

    :param source: url of source dataservice
    :type source: str
    :param target: url of target dataservice
    :type target: str
    :param kf_id: kf_id to copy
    :type kf_id: str
    """
    # Copy the kf_id
    logger.info(f"Querying source for {kf_id}")
    kf_id_info = requests.get(
        (source + get_endpoint(kf_id) + "/" + kf_id),
        headers={"Content-Type": "application/json"},
    )
    body = kf_id_info.json()["results"]
    load_kf_id(target, body)

    # Fetch the data from the source dataservice
    logger.info(f"Querying source for descendants of {kf_id}")
    descendants = find_descendants_by_kfids(
        source,
        get_endpoint(kf_id),
        [kf_id],
        ignore_gfs_with_hidden_external_contribs=False,
        kfids_only=False,
    )
    # Put the things in the target dataservice
    for service in descendants.keys():
        if service != get_endpoint(kf_id):
            logger.info(
                f"Loading {service}: {len(descendants[service])} items found"
            )
            for e in descendants[service].items():
                body = e[1]
                load_kf_id(target, body)
        else:
            logger.debug(f"Current endpoint is {service}")
            continue
