"""
Copies contents of prd dataservice to local dataservice for a particular study
"""
import click
import pandas as pd

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
    check_status(ctx.obj["source"], ctx.obj["target"])
    pass


@copy.command("kfids")
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True, dir_okay=False),
    required=True,
    help="""csv file with a column named 'kf_id' that holds the kf_ids of
     interest""",
)
@click.pass_context
def copy_kfids(ctx, file):
    """Copy the kf_ids from the ids in the given file from
    the source dataservice to the target dataservice
    """
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
def copy_sequencing_center(ctx):
    sequencing_center_handler(ctx.obj["source"], ctx.obj["target"])


if __name__ == "__main__":
    copy()  # pylint: disable=no-value-for-parameter
