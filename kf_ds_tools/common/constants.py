"""
Common constants used for interacting with the dataservice.
"""

banned_items = (
    "_links",
    "created_at",
    "modified_at",
    "sequencing_experiment_genomic_files",
    "read_group_genomic_files",
)

KF_API_URLS = {
    "prd": "https://kf-api-dataservice.kidsfirstdrc.org/",
    "qa": "https://kf-api-dataservice-qa.kidsfirstdrc.org/",
    "localhost": "http://localhost:5000/",
}
