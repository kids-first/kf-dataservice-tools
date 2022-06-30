"""
Copies contents of prd dataservice to local dataservice for a particular study
"""
from kf_utils.dataservice.delete import delete_entities, delete_kfids

import click
import pandas as pd

from kf_ds_tools.common.constants import KF_API_URLS
from kf_ds_tools.common.utils import dry_run_handler, test_url_connection

api_url_help_text = (
    "Either http url to dataservice or \n"
    + f"{[i for i in KF_API_URLS.keys()]}"
)


@click.group()
@click.option(
    "-h",
    "--host",
    type=str,
    required=True,
    help="Host dataservice to run deletes in. " + api_url_help_text,
)
@click.option(
    "--dry_run/--safety_off",
    default=True,
    help="Whether to delete if resource is not at localhost",
)
@click.pass_context
def delete(ctx, host, dry_run):
    ctx.ensure_object(dict)
    ctx.obj["host"] = KF_API_URLS.get(host.lower()) or host
    ctx.obj["dry_run"] = dry_run_handler(dry_run)
    test_url_connection(ctx.obj["host"], exit_on_non200=True)
    pass


@delete.command("kfids")
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
    help="KF_ID of item to delete. Multiple KF_IDs can be supplied.",
)
@click.pass_context
def delete_kfids(ctx, file, kf_id):
    """delete the supplied kf_ids"""
    breakpoint()
    if file:
        kf_ids_file = pd.read_csv(file)["kf_id"].to_list()
    else:
        kf_ids_file = [None]
    kf_id_list = {i for i in list(kf_id) + kf_ids_file if i}
    delete_kfids(
        host=ctx.obj["host"],
        kfids=kf_id_list,
        safety_check=not ctx.obj["dry_run"],
    )


@delete.command("study")
@click.option(
    "-s",
    "--study_id",
    type=str,
    required=True,
    multiple=True,
    help="KF_ID of item to delete. Multiple KF_IDs can be supplied.",
)
@click.pass_context
def delete_study(ctx, study_id):
    """Delete a study and all its descendants"""
    delete_entities(
        host=ctx.obj["host"],
        study_ids=study_id,
        safety_check=not ctx.obj["dry_run"],
    )


@delete.command("everything")
@click.confirmation_option(prompt="Are you sure you want to delete everything?")
@click.pass_context
def delete_everything(ctx):
    """delete all studies and their descendants in a dataservice. This can only
    be used against localhost"""
    delete_entities(
        host=ctx.obj["host"],
        study_ids=None,
    )


if __name__ == "__main__":
    delete()  # pylint: disable=no-value-for-parameter
