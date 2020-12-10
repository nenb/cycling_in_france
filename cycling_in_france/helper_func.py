import regionmask
import numpy as np
import dask


def create_windmax_dict(u, v, names, borders, longitude, latitude):
    """Produce a dictionary of masked maximum wind speeds in units of mph."""

    if u.units != "m s**-1":
        raise ValueError("U field does not have units m/s")
    if v.units != "m s**-1":
        raise ValueError("V field does not have units m/s")
    metre_to_mile = 3600.0 / 1609.3
    speed = np.sqrt(u ** 2 + v ** 2) * metre_to_mile

    windmax_dict = {}
    for i, regname in enumerate(names):
        # Modify index in case any entries have been dropped e.g. Corsica
        idx = names.index[i]
        # Create object from 'borders' for masking gridded data
        regmask = regionmask.Regions(name=regname, outlines=list(borders[idx]))
        # Apply mask to dataset coordinates
        mask_zeros = regmask.mask(longitude, latitude)
        # Replace zeros with ones for matrix multiplication
        mask_ones = mask_zeros.where(np.isnan(mask_zeros.values), 1)
        # Use Dask dataframes for lazy execution
        mask_ones = dask.array.from_array(mask_ones)
        speed_mask = speed * mask_ones
        # Compute maximum over lat-lon grid
        windmax_dict[regname] = speed_mask.max(dim=["longitude", "latitude"])
    return windmax_dict
