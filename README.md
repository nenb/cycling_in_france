<img align="right" width="273" height="240" src="https://upload.wikimedia.org/wikipedia/commons/4/4e/Michauxjun.jpg">

# Cycling in France
[![License:MIT](https://img.shields.io/badge/License-MIT-lightgray.svg?style=flt-square)](https://opensource.org/licenses/MIT)

*Cycling in France* is a Python project analysing surface wind speeds over France using [ERA5 Land](https://www.ecmwf.int/en/era5-land) data. To reproduce the analysis, see details below.

## Quickstart
To start a new project, run:

``` bash
git clone http://github.com/nenb/cycling_in_france
```

Most of the data for this project has been taken from the [ERA5 Land](https://www.ecmwf.int/en/era5-land) product. This data is also available from [Dropbox](https://www.dropbox.com/sh/jcgzoiyiguo723w/AABDsZvDPfLLz7tx7mMSgXh8a?dl=0). The data represents about 40 years of hourly 10m wind speeds inside a bounding box that includes Metropolitan France. Please allow time for retrieval to your local machine as there is more than 20GB of data.

Once the ERA5 Land data is available locally, a soft link to the data should be set: 

```bash
export DATA_DIR=/local_parent_directory_of_data/
```
For further details, have a look at `/scripts/data_retrieve.sh`. 

(**Note**: You might need to play around with this if you are having trouble reading the data in the Jupyter notebook later.)

The analysis also uses [GADM](https://gadm.org/) geospatial data. For retrieval, run the `data_retrieve` shell script from **inside** the `scripts/` subdirectory:

```bash
./data_retrieve.sh
```

Now return to the project root directory and create and activate the conda environment:

```bash
conda env create -f environment.yml
conda activate cycling_in_france
```

Finally, install the Python package:

```bash
python setup.py develop
```

That's it for the setup. You can now go ahead and repeat my analysis:

```bash
cd notebooks
jupyter-lab
```

--------

<p><small>Project based on the <a target="_blank" href="https://github.com/jbusecke/cookiecutter-science-project">cookiecutter science project template</a>.</small></p>
