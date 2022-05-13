<!-- <p align="center">
  <img src="docs/kids_first_logo.svg" alt="Kids First repository logo" width="660px" />
</p>
<p align="center">
  <a href="https://github.com/kids-first/kf-template-repo/blob/master/LICENSE"><img src="https://img.shields.io/github/license/kids-first/kf-template-repo.svg?style=for-the-badge"></a>
</p> -->

# Kids First Dataservice Tools

Command-line tools for bulk interaction with the dataservice. Built with (Kids
First Pyton Utilities)[https://github.com/kids-first/kf-utils-python]

## Installation

Using pip

```sh
pip install git+https://github.com/kids-first/kf-dataservice-tools.git@latest-release
```

# Tools included so far

## Copy a list of kf_ids from one dataservice to another

Copy a list of kf_ids. The list of kf_ids should be in a file, minimally with a
column named `kf_id`.

```sh
kf_dscopy -s prd -t localhost kf_ids -f "path/to/file.csv"
```

Copy a single kf_id

```sh
kf_dscopy -s prd -t localhost kfids -k PT_GRMPYCAT
```

Copy multiple kf_ids

```sh
kf_dscopy -s prd -t localhost kfids -k PT_GRMPYCAT -k BS_FRRRBA11
```

Copy kf_ids that are in a file manifest and some specific kf_id(s):

```sh
kf_dscopy -s prd -t localhost kfids -f "path/to/file.csv" -k PT_GRMPYCAT -k BS_FRRRBA11
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
