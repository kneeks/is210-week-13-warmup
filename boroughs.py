#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""open and read a CSV file found on the local filesystem."""


import csv
import json


GRADES = {
    'A': float(1.0),
    'B': float(0.90),
    'C': float(0.80),
    'D': float(0.70),
    'F': float(0.60)
}


def get_score_summary(filename):
    """Parses through data from a csv file.

    Args:
        filename(str): the csv file

    Returns:
        dict: amount of resteraunts and avg score of total amount of rest.

    Examples:
        >>> get_score_summary('inspection_results.csv')
        {'BRONX': (156, 0.9762820512820514),
         'BROOKLYN': (417, 0.9745803357314141),
         'STATEN ISLAND': (46, 0.9804347826086955),
         'MANHATTAN': (748, 0.9771390374331531),
         'QUEENS': (414, 0.9719806763285017)}
    """
    csv_open = open(filename, 'r')
    csv_parse = csv.reader(csv_open)
    key_g = []
    value = []
    for index in csv_parse:
        camis = index[0]
        boro = index[1]
        grade = index[10]
        if grade != '' and grade != 'P' and grade != 'GRADE':
            grade_score = GRADES[grade]
            key_g.append(camis)
            value.append((boro, grade_score))
    insp_dict = dict(zip(key_g, value))
    csv_open.close()

    man_cnt = 0
    que_cnt = 0
    brook_cnt = 0
    bx_cnt = 0
    si_cnt = 0
    man_num = 0
    que_num = 0
    brook_num = 0
    bx_num = 0
    si_num = 0
    for value in insp_dict.itervalues():
        if value[0] == 'MANHATTAN':
            man_cnt += 1
            man_num += value[1]
        elif value[0] == 'QUEENS':
            que_cnt += 1
            que_num += value[1]
        elif value[0] == 'BROOKLYN':
            brook_cnt += 1
            brook_num += value[1]
        elif value[0] == 'BRONX':
            bx_cnt += 1
            bx_num += value[1]
        elif value[0] == 'STATEN ISLAND':
            si_cnt += 1
            si_num += value[1]
    dict_ret = {}
    dict_ret['MANHATTAN'] = man_cnt, man_num / man_cnt,
    dict_ret['QUEENS'] = que_cnt, que_num / que_cnt,
    dict_ret['BROOKLYN'] = brook_cnt, brook_num / brook_cnt,
    dict_ret['BRONX'] = bx_cnt, bx_num / bx_cnt,
    dict_ret['STATEN ISLAND'] = si_cnt, si_num / si_cnt
    return dict_ret


def get_market_density(filename):
    """
    Takes green markets in the city and reducing the data to only markets
    per borough.

    Args:
        filename(str): json file that is being opened

    Returns:
        dict: set that has green markets of each borough

    Example:
        >>> get_market_density('green_markets.json')
        {u'BRONX': 32, u'BROOKLYN': 48, u'STATEN ISLAND': 2, u'MANHATTAN': 39,
         u'QUEENS': 16}
    """
    json_open = open(filename, 'r')
    data = json.load(json_open)
    red_data = data['data']
    dict_ret = {}
    for value in red_data:
        boro = value[8].strip().upper()
        if boro not in dict_ret:
            boro_cnt = 1
            dict_ret[boro] = boro_cnt
        else:
            boro_cnt += 1
            dict_ret[boro] = boro_cnt
    json_open.close()
    return dict_ret


def correlate_data(csv_open, json_open, output='output.txt'):
    """Combines these two pieces of data and their borough keys and write
    the results to a file.

    Args:
        csv_open(str): csv file that it will pull from
        json_open(str): json file that it will pull from
        output(str): filename of the file that is writ, defaults to output.txt

    Returns:
`       dict: borough names are the keys and inspect score and mrkt percent.
        are the values of the keys

    Examples:
        >>> correlate_data('inspection_results.csv', 'green_markets.json')
        {'BRONX': (0.9762820512820514, 0.20512820512820512),
        'BROOKLYN': (0.9745803357314141, 0.11510791366906475),
        'STATEN ISLAND': (0.9804347826086955, 0.043478260869565216),
        'MANHATTAN': (0.9771390374331531, 0.05213903743315508),
        'QUEENS': (0.9719806763285017, 0.03864734299516908)}
    """
    inspection_score = get_score_summary(csv_open)
    market_ret = get_market_density(json_open)
    correlate = {}
    for key1 in inspection_score:
        for key2 in market_ret:
            if key1 == key2:
                correlate[key1] = (inspection_score[key1][1],
                                   (market_ret[key2] /
                                    float(inspection_score[key1][0])))
    fhandler = open(output, 'w')
    json.dump(correlate, fhandler)
    fhandler.close()
