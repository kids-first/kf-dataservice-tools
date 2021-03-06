"""
Common Utilities for working with the dataservice.
"""
import sys

import requests

from kf_ds_tools.common.constants import banned_items
from kf_ds_tools.common.logging import get_logger

logger = get_logger(__name__, testing_mode=False, log_format="detailed")


def test_url_connection(url, exit_on_non200=False):
    """Test that it's possible to connect to the dataservice url

    :param url: url of the dataservice
    :type url: str
    :param exit_on_non200: exit script on a status code that isn't 200
    :type exit_on_non200: bool
    :return: response from the url
    :rtype: requests.Response
    """
    resp = requests.get(
        (url + "status"), headers={"Content-Type": "application/json"}
    )
    if resp.status_code != 200:
        if exit_on_non200:
            logger.error(("Connection FAILED to " + url))
            sys.exit(0)
        else:
            logger.debug(("Connection FAILED to " + url))
    return resp


def check_status(source, target):
    """check that both source and target can be connected to

    :param source: url of source dataservice
    :type source: str
    :param target: url of target dataservice
    :type target: str
    """
    # check that both source and target can be connected to
    if test_url_connection(source).status_code != 200:
        logger.error("Connection failed to " + source)
        sys.exit(0)
    if test_url_connection(target).status_code != 200:
        logger.error("Connection failed to " + target)
        sys.exit(0)


def clean_response_body(body):
    """Remove unneeded links from api response body

    :param body: response body from dataservice api query
    :type body: dict
    :return: response body with unused items removed
    :rtype: dict
    """
    logger.debug(f"cleaning body of {body['kf_id']}")
    return {k: body[k] for k in body if k not in banned_items}


def dry_run_handler(dry_run=True):
    logger.info("testing dry run value")
    if dry_run:
        logger.info("Dry Run detected")
    else:
        logger.warning("Dry Run is off")
    return dry_run
