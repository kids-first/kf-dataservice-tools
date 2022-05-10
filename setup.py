from os import path

from setuptools import find_packages, setup

# requirements from requirements.txt
root_dir = path.dirname(path.abspath(__file__))
with open(path.join(root_dir, "requirements.txt"), "r") as f:
    requirements = f.read().splitlines()

# long description from README
with open(path.join(root_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="kf-dataservice-tools",
    use_scm_version={
        "local_scheme": "dirty-tag",
        "version_scheme": "post-release",
    },
    setup_requires=["setuptools_scm"],
    description="Kids First Dataservice Tools",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kids-first/kf-dataservice-tools/",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "kf_dscopy = kf_ds_tools.scripts.ds_copy:copy",
        ],
    },
    python_requires=">=3.6, <4",
    install_requires=requirements,
)
