#-*- coding: utf-8 -*-
import xlrd


def read_xls(filename, sheet_name, picked=[]):
    print picked
    data = xlrd.open_workbook(filename)
    table = data.sheet_by_name(sheet_name)
    headers = table.row_values(0)
    rsltDict = {}

    for i in range(table.ncols):
        col = table.col_values(i)
        h = headers[i]

        if str(h) in picked:
            col.pop(0)
            print 'contain ', h
            rsltDict[h] = col

    return rsltDict



if __name__ == "__main__":



    fn = 'resource_table.xlsx'

    light_table0 = read_xls(fn, 'light', ['N', 'product_id', 'degree', 'light_id', 'def_power', 'def_cct'])

    '''lg_name	description	lights	default_light'''
    lg_table0 = read_xls(fn, 'light_group', ['lg_name', 'description', 'lights', 'default_light'])
    '''scene_id	scene_name	tour_order	light_groups	map	icon'''
    scene_table0 = read_xls(fn, 'scene', ['scene_id', 'scene_name', 'tour_order', 'light_groups', 'map', 'icon'])
    '''space_id	space_version	space_name	space_desc	space_map_ver	space_icon_ver	space_address'''
    space_table0 = read_xls(fn, 'space', ['space_id', 'space_version', 'space_name',
                                   'space_desc', 'space_map_ver', 'space_icon_ver', 'space_address'])

    print light_table0
    print lg_table0
    print scene_table0
    print space_table0

