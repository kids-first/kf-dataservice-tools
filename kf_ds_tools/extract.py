from kf_utils.dataservice.scrape import yield_entities_from_kfids


def get_kf_ids(source, kf_id_list):
    """Query the dataservice for a list of kf_ids

    :param source: url of source dataservice
    :type source: str
    :param kf_id_list: list of kf_ids to query
    :type kf_id_list: list
    :return: list of information about the requested IDs from the dataservice
    :rtype: list
    """
    kf_id_info = []
    for e in yield_entities_from_kfids(source, kf_id_list, show_progress=True):
        kf_id_info.append(e)
    return kf_id_info
