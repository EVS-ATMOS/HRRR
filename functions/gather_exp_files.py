#! /usr/bin/env python



def gather_exp_files(date,radar_dir,sounding_dir,ceilometer_dir):


    [[dates_radar,dates_sounding,dates_ceil],[filename_rad,filename_sound,filename_ceil]] = org_exp_files(radar_dir,sounding_dir,ceilometer_dir)

    index_radar = dates_radar.index(date)
    index_sounding = dates_sounding.index(date)
    index_ceilometer = dates_ceil.index(date)

    return [filename_rad[index_radar],filename_sound[index_sound],filename_ceil[index_ceilometer]]    




