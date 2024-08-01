"""
TODO in here:
- Update archive_noaa_rtsw_data so it only updates files, doesn't read in all every time.
- Write NOAA RTSW data minute+hourly data into year files.
"""

import os
import sys
from datetime import datetime, timedelta
import h5py
import json
import logging
from matplotlib.dates import num2date, date2num
import matplotlib.pyplot as plt
import numpy as np
import urllib
import urllib.error
import requests

#logger = logging.getLogger(__name__)

# -------------------------------------------------------------------
#    DOWNLOAD
# -------------------------------------------------------------------

def download_noaa_rtsw_data(save_path, datestrf="%Y-%m-%dT%Hh"):
    """Downloads NOAA real-time solar wind data (plasma and mag).

    Parameters
    ==========
    save_path : str
        String of directory to save files to.

    Returns
    =======
    (get_plas, get_mag) : (bool, bool)
        Both True if both files were successfully downloaded.

    Example
    =======
    >>> pla_success, mag_success = download_noaa_rtsw_data("data")
    """

    plasma = 'http://services.swpc.noaa.gov/products/solar-wind/plasma-7-day.json'
    mag = 'http://services.swpc.noaa.gov/products/solar-wind/mag-7-day.json'
    dst = 'http://services.swpc.noaa.gov/products/kyoto-dst.json'

    datestr = str(datetime.utcnow().strftime(datestrf))
    logging.info('downloading NOAA real time solar wind plasma and mag for {}'.format(datestr))

    get_plas, get_mag, get_dst = True, True, False

    try:
        urllib.request.urlretrieve(plasma, os.path.join(save_path, 'plasma-7-day_'+datestr+'.json'))
    except urllib.error.URLError as e:
        logging.error(' '+plasma+' '+e.reason)
        get_plas = False

    try:
        urllib.request.urlretrieve(mag, os.path.join(save_path, 'mag-7-day_'+datestr+'.json'))
    except urllib.error.URLError as e:
        logging.error(' '+mag+' '+e.reason)
        get_mag = False

    try:
        urllib.request.urlretrieve(dst, os.path.join(save_path, 'dst-7-day_'+datestr+'.json'))
    except urllib.error.URLError as e:
        logging.error(' '+dst+' '+e.reason)
        get_dst = False

    return get_plas, get_mag


def archive_noaa_rtsw_data(json_path, archive_path, limit_by_ndays=100):
    """Archives the NOAA real-time solar wind data files in hdf5 format.

    Parameters
    ==========
    json_path : str
        String of directory containing plasma data files.
    archive_path : str
        String of directory to save plasma data file.

    Returns
    =======
    True if completed.

    Example
    =======
    >>> archive_noaa_rtsw_data("rtswdata", "archive")
    """

    logging.info('Archive NOAA real time solar wind data as h5 file')

    items = os.listdir(json_path)
    pla_list, mag_list, dst_list = [], [], []
    for name in items:
       if name.startswith("mag") and name.endswith(".json"):
            mag_list.append(name)
       if name.startswith("pla") and name.endswith(".json"):
            pla_list.append(name)
       if name.startswith("dst") and name.endswith(".json"):
            dst_list.append(name)

    pla_keys = ['time_tag', 'density', 'speed', 'temperature']
    mag_keys = ['time_tag', 'bx_gsm', 'by_gsm', 'bz_gsm', 'bt']
    dst_keys = ['time_tag', 'dst']
    rtsw_pla = np.zeros((500000000, len(pla_keys)))
    rtsw_mag = np.zeros((500000000, len(mag_keys)))
    rtsw_dst = np.zeros((500000000, len(dst_keys)))

 
    # READ FILES
    # ----------

    
    # Go through plasma files:
    kp = 0
    for json_file in pla_list:
        try:
            pla_data = read_noaa_rtsw_json(os.path.join(json_path, json_file))
            for ip, pkey in enumerate(pla_keys):
                rtsw_pla[kp:kp+np.size(pla_data),ip] = pla_data[pkey]
            kp = kp + np.size(pla_data)
            #print(json_file)
        except:
            logging.error("JSON load failed for file test {}".format(json_file))
    rtsw_pla_cut = rtsw_pla[0:kp]
    rtsw_pla_cut = rtsw_pla_cut[rtsw_pla_cut[:,0].argsort()] # sort by time
    dum, ind = np.unique(rtsw_pla_cut[:,0], return_index=True)
    rtsw_pla_fin = rtsw_pla_cut[ind] # remove multiples of timesteps

  

    # Go through magnetic files:
    km = 0
    for json_file in mag_list:
        try:
            mag_data = read_noaa_rtsw_json(os.path.join(json_path, json_file))
            for ip, pkey in enumerate(mag_keys):
                rtsw_mag[km:km+np.size(mag_data),ip] = mag_data[pkey]
            km = km + np.size(mag_data)
        except:
            logging.error("JSON load failed for file {}".format(json_file))
    rtsw_mag_cut = rtsw_mag[0:km]
    rtsw_mag_cut = rtsw_mag_cut[rtsw_mag_cut[:,0].argsort()] # sort by time
    dum, ind = np.unique(rtsw_mag_cut[:,0], return_index=True)
    rtsw_mag_fin = rtsw_mag_cut[ind] # remove multiples of timesteps

    # Go through Dst files:
    kd = 0
    for json_file in dst_list:
        try:
            dst_data = read_noaa_rtsw_json(os.path.join(json_path, json_file),
                                           timef="%Y-%m-%d %H:%M:%S")
            for ip, pkey in enumerate(dst_keys):
                rtsw_dst[kd:kd+np.size(dst_data),ip] = dst_data[pkey]
            kd = kd + np.size(dst_data)
        except:
            logging.error("JSON load failed for file {}".format(json_file))
    rtsw_dst_cut = rtsw_dst[0:kd]
    rtsw_dst_cut = rtsw_dst_cut[rtsw_dst_cut[:,0].argsort()] # sort by time
    dum, ind = np.unique(rtsw_dst_cut[:,0], return_index=True)
    rtsw_dst_fin = rtsw_dst_cut[ind] # remove multiples of timesteps

    # Interpolate onto minute and hour timesteps (since both files are mismatched/missing timesteps):
    first_timestamp_min = num2date(np.max((rtsw_pla_fin[0,0], rtsw_mag_fin[0,0])))
    first_timestamp_min = first_timestamp_min - timedelta(seconds=first_timestamp_min.second)
    first_timestamp_hour = num2date(np.max((rtsw_pla_fin[0,0], rtsw_mag_fin[0,0], rtsw_dst_fin[0,0])))
    first_timestamp_hour = first_timestamp_hour - timedelta(seconds=first_timestamp_hour.second)
    last_timestamp_min = num2date(np.min((rtsw_pla_fin[-1,0], rtsw_mag_fin[-1,0])))
    last_timestamp_min = last_timestamp_min - timedelta(seconds=last_timestamp_min.second)
    last_timestamp_hour = num2date(np.min((rtsw_pla_fin[-1,0], rtsw_mag_fin[-1,0], rtsw_dst_fin[-1,0])))
    last_timestamp_hour = last_timestamp_hour - timedelta(seconds=last_timestamp_hour.second)
    n_min = int((last_timestamp_min-first_timestamp_min).total_seconds() / 60)
    n_hour = int(np.round(int((last_timestamp_hour-first_timestamp_hour).total_seconds() / 60) / 60, 0))

    min_steps = np.array([date2num(first_timestamp_min+timedelta(minutes=n)) for n in range(n_min)])
    hour_steps = np.array([date2num(first_timestamp_hour+timedelta(hours=n)) for n in range(n_hour)])

    # DEFINE HEADER
    # -------------
    metadata = {
        "Description": "Real time solar wind magnetic field and plasma data from NOAA",
        "TimeRange": "{} - {}".format(first_timestamp_min.strftime("%Y-%m-%dT%H:%M"), last_timestamp_min.strftime("%Y-%m-%d %H:%M")),
        "SourceURL": "https://services.swpc.noaa.gov/products/solar-wind/",
        "CompiledBy": "Helio4Cast code, https://github.com/helioforecast/helio4cast",
        "Authors": "C. Moestl (twitter @chrisoutofspace) and R. L. Bailey (GitHub bairaelyn)",
        "FileCreationDate": datetime.utcnow().strftime("%Y-%m-%dT%H:%M")+' UTC',
        "Units": "B-field: nT, Density: cm^-3, Temperature: K, Speed: km s^-1",
        "Notes": "None in data have been replaced with np.NaNs.",
    }

    # WRITE DATA: LAST 100 DAYS
    # -------------------------
    past_100days = datetime.utcnow() - timedelta(days=limit_by_ndays)

    if not os.path.exists(archive_path):
        os.mkdir(archive_path)

    # Write to file (minute timesteps):
    min_steps_100 = min_steps[min_steps > date2num(past_100days)]
    hour_steps_100 = hour_steps[hour_steps > date2num(past_100days)]
    hdf5_file = os.path.join(archive_path, 'rtsw_min_last100days.h5')
    hf = h5py.File(hdf5_file, mode='w')

    hf.create_dataset('time', data=min_steps_100)
    for key in pla_keys[1:]:
        data_interp = np.interp(min_steps_100, rtsw_pla_fin[:,0], rtsw_pla_fin[:,pla_keys.index(key)])
        hf.create_dataset(key, data=data_interp)
    for key in mag_keys[1:]:
        data_interp = np.interp(min_steps_100, rtsw_mag_fin[:,0], rtsw_mag_fin[:,mag_keys.index(key)])
        hf.create_dataset(key, data=data_interp)
    metadata['SamplingRate'] = 1./24./60.
    for k, v in metadata.items():
        hf.attrs[k] = v
    hf.close()

    # Write to file (hour timesteps):
    metadata["TimeRange"] = "{} - {}".format(first_timestamp_hour.strftime("%Y-%m-%dT%H:%M"), last_timestamp_hour.strftime("%Y-%m-%d %H:%M"))
    hdf5_file = os.path.join(archive_path, 'rtsw_hour_last100days.h5')
    hf = h5py.File(hdf5_file, mode='w')

    hf.create_dataset('time', data=hour_steps_100)
    for key in pla_keys[1:]:
        data_interp = np.interp(hour_steps_100, rtsw_pla_fin[:,0], rtsw_pla_fin[:,pla_keys.index(key)])
        hf.create_dataset(key, data=data_interp)
    for key in mag_keys[1:]:
        data_interp = np.interp(hour_steps_100, rtsw_mag_fin[:,0], rtsw_mag_fin[:,mag_keys.index(key)])
        hf.create_dataset(key, data=data_interp)
    for key in dst_keys[1:]:
        data_interp = np.interp(hour_steps_100, rtsw_dst_fin[:,0], rtsw_dst_fin[:,dst_keys.index(key)])
        hf.create_dataset(key, data=data_interp)
    metadata['SamplingRate'] = 1./24.
    for k, v in metadata.items():
        hf.attrs[k] = v
    hf.close()

    logging.info('Archiving of NOAA data done')

    return True


def read_noaa_rtsw_json(json_file, timef="%Y-%m-%d %H:%M:%S.%f"):
    """Reads NOAA real-time solar wind data JSON files (already downloaded).

    Parameters
    ==========
    json_file : str
        String of direct path to plasma data file.

    Returns
    =======
    rtsw_data : np.array
        Numpy array with JSON keys accessible as keys or under rtsw_data.dtype.names.

    Example
    =======
    >>> json_file = 'data/plasma-7-day_2020_Mar_28_17_00.json'
    >>> pla_data = read_noaa_rtsw_json(json_file)
    """

    # Read JSON file:
    with open(json_file, 'r') as jdata:
        dp = json.loads(jdata.read())
        dpn = [[np.nan if x == None else x for x in d] for d in dp]     # Replace None w NaN
        dtype=[(x, 'float') for x in dp[0]]
        datesp = [datetime.strptime(x[0], timef)  for x in dpn[1:]]
        #convert datetime to matplotlib times
        mdatesp = date2num(datesp)
        dp_ = [tuple([d]+[float(y) for y in x[1:]]) for d, x in zip(mdatesp, dpn[1:])]
        rtsw_data = np.array(dp_, dtype=dtype)

    return rtsw_data



