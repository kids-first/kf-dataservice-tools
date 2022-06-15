"""
Copies contents of prd dataservice to local dataservice for a particular study
"""
import click
import pandas as pd
import requests

from kf_ds_tools.common.constants import KF_API_URLS
from kf_ds_tools.common.utils import check_status
from kf_ds_tools.copy import (
    copy_all_descendants,
    copy_kf_ids,
    sequencing_center_handler,
)

api_url_help_text = (
    "Either http url to dataservice or \n"
    + f"{[i for i in KF_API_URLS.keys()]}"
)


@click.group()
@click.option(
    "-s",
    "--source",
    type=str,
    required=True,
    help="Source dataservice to copy FROM. " + api_url_help_text,
)
@click.option(
    "-t",
    "--target",
    type=str,
    required=True,
    help="Target dataservice to copy TO. " + api_url_help_text,
)
@click.pass_context
def copy(ctx, source, target):
    ctx.ensure_object(dict)
    ctx.obj["source"] = KF_API_URLS.get(source.lower()) or source
    ctx.obj["target"] = KF_API_URLS.get(target.lower()) or target
    pass


@copy.command("kfids")
@click.option(
    "-k",
    "--kfid",
    type=str,
    required=True,
    multiple=True,
    help="kf_id to copy.",
)
@click.option(
    "-c",
    "--copy_sc",
    is_flag=True,
    help="if sequencing centers are not in the target, copy them",
)
@click.option(
    "-d",
    "--copy_descendants",
    is_flag=True,
    help="copy the descendants of the given kfids",
)
@click.pass_context
def copy_kfids(ctx, kfid, copy_sc, copy_descendants):
    """Copy the kf_ids from the ids in the given file from
    the source dataservice to the target dataservice
    """
    check_status(ctx.obj["source"], ctx.obj["target"])
    if copy_sc:
        sequencing_center_handler(ctx.obj["source"], ctx.obj["target"])
    if copy_descendants:
        for kf_id in kfid:
            copy_all_descendants(ctx.obj["source"], ctx.obj["target"], kf_id)
    else:
        copy_kf_ids(ctx.obj["source"], ctx.obj["target"], kfid)


@copy.command("file")
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    help="""csv file with a column named 'kf_id' that holds the kf_ids of 
    interest""",
)
@click.pass_context
def copy_file(ctx, file):
    """Copy the kf_ids from the ids in the given file from
    the source dataservice to the target dataservice
    """
    check_status(ctx.obj["source"], ctx.obj["target"])
    kf_id_list = pd.read_csv(file)["kf_id"].to_list()
    copy_kf_ids(ctx.obj["source"], ctx.obj["target"], kf_id_list)


@copy.command("study")
@click.argument("study_id", type=str)
@click.option(
    "-c",
    "--copy_sc",
    is_flag=True,
    help="if sequencing experiments are not in the target, copy them",
)
@click.pass_context
def copy_study(ctx, study_id, copy_sc):
    if copy_sc:
        sequencing_center_handler(ctx.obj["source"], ctx.obj["target"])
    copy_all_descendants(ctx.obj["source"], ctx.obj["target"], study_id)


@copy.command("sequencing_centers")
@click.pass_context
def copy_study(ctx):
    sequencing_center_handler(ctx.obj["source"], ctx.obj["target"])


if __name__ == "__main__":
    copy()
