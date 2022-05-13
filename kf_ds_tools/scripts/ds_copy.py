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
    required=False,
    help="""csv file with a column named 'kf_id' that holds the kf_ids of
     interest""",
)
@click.option(
    "-k",
    "--kf_id",
    type=str,
    required=False,
    multiple=True,
    help="KF_ID of item to copy. Multiple KF_IDs can be supplied.",
)
@click.pass_context
def copy_kfids(ctx, file, kf_id):
    """Copy the kf_ids from the ids in the given file from
    the source dataservice to the target dataservice
    """
    breakpoint()
    if file:
        kf_ids_file = pd.read_csv(file)["kf_id"].to_list()
    else:
        kf_ids_file = [None]
    kf_id_list = {i for i in list(kf_id) + kf_ids_file if i}
    copy_kf_ids(ctx.obj["source"], ctx.obj["target"], kf_id_list)


@copy.command("descendants")
@click.argument("kf_id", type=str)
@click.option(
    "-c",
    "--copy_sc",
    is_flag=True,
    help="if sequencing experiments are not in the target, copy them",
)
@click.pass_context
def copy_descendants(ctx, kf_id, copy_sc):
    """Copy all descendants of a kf_id. This is a way to copy everything under
    a study.
    """
    if copy_sc:
        sequencing_center_handler(ctx.obj["source"], ctx.obj["target"])
    copy_all_descendants(ctx.obj["source"], ctx.obj["target"], kf_id)


@copy.command("sequencing_centers")
@click.pass_context
def copy_sequencing_center(ctx):
    sequencing_center_handler(ctx.obj["source"], ctx.obj["target"])


if __name__ == "__main__":
    copy()  # pylint: disable=no-value-for-parameter
