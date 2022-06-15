<!-- <p align="center">
  <img src="docs/kids_first_logo.svg" alt="Kids First repository logo" width="660px" />
</p>
<p align="center">
  <a href="https://github.com/kids-first/kf-template-repo/blob/master/LICENSE"><img src="https://img.shields.io/github/license/kids-first/kf-template-repo.svg?style=for-the-badge"></a>
</p> -->

# Kids First Dataservice Tools

CLI tools for bulk interaction with the dataservice. Built with (Kids First
Pyton Utilities)[https://github.com/kids-first/kf-utils-python]

## Installation

Using pip

```sh
pip install git+https://github.com/kids-first/kf-dataservice-tools.git@latest-release
```

# Tools included so far

## Copy specific kf_ids from one dataservice to another

Copy a list of kf_ids. The list of kf_ids should be in a file, minimally with a
column named `kf_id`.

```sh
kf_dscopy -s prd -t localhost kfids -k BS_12345678 -k PT_ABCDEFGH 
```

## Copy a list of kf_ids from one dataservice to another

Copy a list of kf_ids. The list of kf_ids should be in a file, minimally with a
column named `kf_id`.

```sh
kf_dscopy -s prd -t localhost file -f "path/to/file.csv"
```

## Copy an entire study

Copy an entire study (study + all of its descendants)

```sh
kf_dscopy -s prd -t localhost study SD_ME0WME0W
```

Copy an entire study and copy all sequencing centers

```sh
kf_dscopy -s prd -t localhost study SD_ME0WME0W --copy_sc
```

## Copy sequencing centers

Check if all the sequencing centers in the source are in
target. Copy all the sequencing centers not in target into
target.

```sh
kf_dscopy -s prd -t localhost sequencing_centers
```
