"""
Common Utilities for working with the dataservice.
"""
import sys

import requests

from kf_ds_tools.common.constants import banned_items


def test_url_connection(url):
    """Test that it's possible to connect to the dataservice url

    :param url: url of the dataservice
    :type url: str
    :return: response from the url
    :rtype: requests.Response
    """
    resp = requests.get(
        (url + "status"), headers={"Content-Type": "application/json"}
    )
    if resp.status_code != 200:
        print(("conection FAILED to " + url))
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
        sys.exit(0)
    if test_url_connection(target).status_code != 200:
        sys.exit(0)


def clean_response_body(body):
    """Remove unneeded links from api response body

    :param body: response body from dataservice api query
    :type body: dict
    :return: response body with unused items removed
    :rtype: dict
    """
    return {k: body[k] for k in body if k not in banned_items}
