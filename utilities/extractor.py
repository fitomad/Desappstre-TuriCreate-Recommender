#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import http.client
from datetime import datetime
import argparse
import sqlite3
import csv

themoviedb_server = str("api.themoviedb.org")

results = list()

def fetch_shows():
    """
    Recuperamos los distintos identificador de shows 
    seleccionados por los usuarios
    """
    con = sqlite3.connect('harvester.db')
    cursorObj = con.cursor()
 
    cursorObj.execute('select distinct show_id from lists order by show_id desc')

    rows = cursorObj.fetchall()
    shows = list(map(lambda show: show[0], rows))

    return shows



def request_show(show_id):
    """
    Request an URL
    """
    url = "/3/tv/{0}?api_key=ae18023495231d6c234fd8f8ba1e2eb0&language=en-US".format(show_id)
    conn = http.client.HTTPSConnection(themoviedb_server)
    headers = { "Cache-Control" : "no-cache" }
    conn.request("GET", url, None, headers)
    r1 = conn.getresponse()

    if r1.status == 200:
        data1 = r1.read()
        show_json = json.loads(data1)
        # JSON document
        process_result(show_json)

    conn.close()


def process_result(show_json):
    """
    Process JSON and recover results
    """

    global results

    information = {
        "showId" : show_json["id"],
        "name" : show_json["name"],
        "year" : transform_date(show_json["first_air_date"]),
        "genres" : transform_genres(show_json["genres"]),
        "networks" : transform_neworks(show_json["networks"])
    }

    results.append(information)

def transform_date(date_string):
    """

    """
    show_date = datetime.strptime(date_string, '%Y-%m-%d')
    return show_date.year

def transform_genres(genres):
    """

    """
    return list(map(lambda genre: genre["name"], genres))

def transform_neworks(networks):
    """

    """
    return list(map(lambda network: network["name"], networks))

#
# Workflow.
#

shows = fetch_shows()

for show in shows:
    request_show(show)

csv_file = "shows.csv"
csv_columns = ['showId', 'name', 'year', 'genres', 'networks']

try:
    with open(csv_file, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        
        for result in results:
            writer.writerow(result)
except IOError as io:
    print("I/O error")
    print(io)
