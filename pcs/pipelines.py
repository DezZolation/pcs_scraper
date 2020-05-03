# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import sqlite3
from pcs.items import Rider, Race, Result

class PcsPipeline:
    def __init__(self):
        self.connection = sqlite3.connect("pcs.db")
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS riders(
            slug TEXT PRIMARY KEY, 
            name TEXT, 
            dob TEXT
        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS races(
            slug TEXT PRIMARY KEY, 
            season INTEGER, 
            name TEXT, 
            stage INTEGER, 
            stage_type TEXT, 
            date TEXT,
            distance REAL,
            difficulty INTEGER
        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS results(
            rider TEXT, 
            race TEXT, 
            team TEXT,
            stage_rank INTEGER,
            stage_time INTEGER,
            gc_rank INTEGER,
            gc_time INTEGER,
            pc_rank INTEGER,
            pc_points INTEGER,
            kom_rank INTEGER,
            kom_points INTEGER
        )""")

    def process_item(self, item, spider):
        if isinstance(item, Rider):
            self.cursor.execute("""SELECT * FROM riders WHERE slug=?""", (item['slug'],))
            result = self.cursor.fetchone()
            if result:
                pass
                #print("Rider already in database: %s" % item)
            else:
                self.cursor.execute("""INSERT INTO riders VALUES (?,?,?)""", (
                    item['slug'], 
                    item['name'], 
                    item['dob']
                    )
                )
                self.connection.commit()
                #print("Rider stored : " % item)
        elif isinstance(item, Race):
            self.cursor.execute("""SELECT * FROM races WHERE slug=?""", (item['slug'],))
            result = self.cursor.fetchone()
            if result:
                pass
                #print("Race already in database: %s" % item)
            else:
                self.cursor.execute("""INSERT INTO races VALUES (?,?,?,?,?,?,?,?)""", (
                    item['slug'], 
                    item['season'], 
                    item['name'],
                    item['stage'],
                    item['stage_type'],
                    item['date'],
                    item['distance'],
                    item['difficulty']
                    ),
                )
                self.connection.commit()
                #print("Race stored : " % item)
        elif isinstance(item, Result):
            self.cursor.execute("""SELECT * FROM results WHERE rider=? AND race=?""", (item['rider'],item['race']))
            result = self.cursor.fetchone()
            if result:
                pass
                #print("Result already in database: %s" % item)
            else:
                self.cursor.execute("""INSERT INTO results VALUES (?,?,?,?,?,?,?,?,?,?,?)""", (
                    item['rider'], 
                    item['race'], 
                    item['team'],
                    item['stage_rank'],
                    item['stage_time'],
                    item['gc_rank'],
                    item['gc_time'],
                    item['pc_rank'],
                    item['pc_points'],
                    item['kom_rank'],
                    item['kom_points']
                    )
                )
                self.connection.commit()
                #print("Result stored : " % item)
        return item
