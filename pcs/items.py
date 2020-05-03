# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Rider(scrapy.Item):
    slug = scrapy.Field()
    name = scrapy.Field()
    dob = scrapy.Field()

class Race(scrapy.Item):
    slug = scrapy.Field()
    season = scrapy.Field() 
    name = scrapy.Field()
    stage = scrapy.Field()
    stage_type = scrapy.Field()
    date = scrapy.Field()
    distance = scrapy.Field()
    difficulty = scrapy.Field()

class Result(scrapy.Item):
    rider = scrapy.Field()
    race = scrapy.Field()
    team = scrapy.Field()
    stage_rank = scrapy.Field()
    stage_time = scrapy.Field()
    gc_rank = scrapy.Field()
    gc_time = scrapy.Field()
    pc_rank = scrapy.Field()
    pc_points = scrapy.Field()
    kom_rank = scrapy.Field()
    kom_points = scrapy.Field()