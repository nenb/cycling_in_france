import pytest
import numpy as np
import geopandas as gpd
import xarray as xr
import dask
from cycling_in_france.helper_func import create_windmax_dict


def test_windmax_dict():
    """Set specific cities in each French region as location of max wind speed.
    Test to confirm that these maximum speeds are returned in dict object."""

    # Setup regions
    regs_fr = gpd.read_file("../../data/raw/gadm36_FRA.gpkg", layer=1)
    regnames = regs_fr.NAME_1.drop(4)
    region_borders = regs_fr.geometry.values

    # Import data
    ds_u = xr.open_dataset(
        "../../data/raw/cycling_in_france/10m_u_component_of_wind_1981_1985.nc"
    )
    u10 = ds_u["u10"][0]
    lon = ds_u.longitude.values
    lat = ds_u.latitude.values

    # Normalise all valid wind speeds to 1m/s
    u10.values = u10.values / u10.values

    # Set specific max values for cities in each French region
    # Rennes - Bretagne
    u10[39, 46] = 2
    # Rouen - Normandie
    u10[27, 71] = 4
    # Lille - Hauts-de-France
    u10[17, 90] = 6
    # Strasbourg - Grand Est
    u10[36, 134] = 8
    # Paris - Île-de-France
    u10[35, 82] = 10
    # Nantes - Pays de la Loire
    u10[49, 47] = 12
    # Orleans - Centre-Val de Loire
    u10[45, 75] = 14
    # Dijon - Bourgogne-Franche-Comté
    u10[48, 110] = 16
    # Bordeaux - Nouvelle-Aquitaine
    u10[75, 57] = 18
    # Toulouse - Occitanie
    u10[86, 73] = 20
    # Lyon - Auvergne-Rhône-Alpes
    u10[65, 105] = 22
    # Avignon - Provence-Alpes-Côte d'Azur
    # WARNING - Don't use coastal cities, border too coarse!
    u10[84, 105] = 24

    windmax_dict = create_windmax_dict(u10, u10, regnames, region_borders, lon, lat)
    windmax_dict = dask.compute(windmax_dict)[0]

    metre_to_mile = 3600.0 / 1609.3

    errors = []
    if "%.3f" % (windmax_dict["Bretagne"].values) != "%.3f" % (
        np.sqrt(2 * 2 ** 2) * metre_to_mile
    ):
        errors.append("Bretagne Error")
    if "%.3f" % (windmax_dict["Normandie"].values) != "%.3f" % (
        np.sqrt(2 * 4 ** 2) * metre_to_mile
    ):
        errors.append("Normandie Error")
    if "%.3f" % (windmax_dict["Hauts-de-France"].values) != "%.3f" % (
        np.sqrt(2 * 6 ** 2) * metre_to_mile
    ):
        errors.append("Hauts-de-France Error")
    if "%.3f" % (windmax_dict["Grand Est"].values) != "%.3f" % (
        np.sqrt(2 * 8 ** 2) * metre_to_mile
    ):
        errors.append("Grand Est Error")
    if "%.3f" % (windmax_dict["Île-de-France"].values) != "%.3f" % (
        np.sqrt(2 * 10 ** 2) * metre_to_mile
    ):
        errors.append("Île-de-France Error")
    if "%.3f" % (windmax_dict["Pays de la Loire"].values) != "%.3f" % (
        np.sqrt(2 * 12 ** 2) * metre_to_mile
    ):
        errors.append("Pays de la Loire Error")
    if "%.3f" % (windmax_dict["Centre-Val de Loire"].values) != "%.3f" % (
        np.sqrt(2 * 14 ** 2) * metre_to_mile
    ):
        errors.append("Centre-Val de Loire Error")
    if "%.3f" % (windmax_dict["Bourgogne-Franche-Comté"].values) != "%.3f" % (
        np.sqrt(2 * 16 ** 2) * metre_to_mile
    ):
        errors.append("Bourgogne-Franche-Comté Error")
    if "%.3f" % (windmax_dict["Nouvelle-Aquitaine"].values) != "%.3f" % (
        np.sqrt(2 * 18 ** 2) * metre_to_mile
    ):
        errors.append("Nouvelle-Aquitaine Error")
    if "%.3f" % (windmax_dict["Occitanie"].values) != "%.3f" % (
        np.sqrt(2 * 20 ** 2) * metre_to_mile
    ):
        errors.append("Occitanie Error")
    if "%.3f" % (windmax_dict["Auvergne-Rhône-Alpes"].values) != "%.3f" % (
        np.sqrt(2 * 22 ** 2) * metre_to_mile
    ):
        errors.append("Auvergne-Rhône-Alpes Error")
    if "%.3f" % (windmax_dict["Provence-Alpes-Côte d'Azur"].values) != "%.3f" % (
        np.sqrt(2 * 24 ** 2) * metre_to_mile
    ):
        errors.append("Provence-Alpes-Côte d'Azur Error")

    assert errors == []
