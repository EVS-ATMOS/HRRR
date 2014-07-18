# -*- coding: utf-8 -*-


'''
This function calls the org_dis_files function (which organizes the files by date) and returns the first file by date. 

author: gmckercher
'''

def gather_disdrometer_files(date,dis_dir):

    [[dates_dis],[filename_dis]] = org_dis_files(dis_dir)

    index_dis = dates_dis.index(date)

    return [filename_dis[index_dis]]