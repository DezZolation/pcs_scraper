# -*- coding: utf-8 -*-
import scrapy, re, datetime, sqlite3
from ..items import Rider, Race, Result

class RacespiderSpider(scrapy.Spider):
    name = 'racespider'
    allowed_domains = ['www.procyclingstats.com']
    start_urls = [
        # World Tour
        'https://www.procyclingstats.com/race/tour-de-france',
        'https://www.procyclingstats.com/race/giro-d-italia',
        'https://www.procyclingstats.com/race/vuelta-a-espana',

        'https://www.procyclingstats.com/race/paris-nice',
        'https://www.procyclingstats.com/race/tirreno-adriatico',
        'https://www.procyclingstats.com/race/volta-a-catalunya',
        'https://www.procyclingstats.com/race/tour-de-romandie',
        'https://www.procyclingstats.com/race/tour-de-suisse',
        'https://www.procyclingstats.com/race/binckbank-tour',

        'https://www.procyclingstats.com/race/tour-down-under',
        'https://www.procyclingstats.com/race/great-ocean-race',
        'https://www.procyclingstats.com/race/uae-tour',
        'https://www.procyclingstats.com/race/omloop-het-nieuwsblad',
        'https://www.procyclingstats.com/race/strade-bianche',
        'https://www.procyclingstats.com/race/milano-sanremo',
        'https://www.procyclingstats.com/race/driedaagse-vd-panne',
        'https://www.procyclingstats.com/race/e3-harelbeke',
        'https://www.procyclingstats.com/race/gent-wevelgem',
        'https://www.procyclingstats.com/race/dwars-door-vlaanderen',
        'https://www.procyclingstats.com/race/ronde-van-vlaanderen',
        'https://www.procyclingstats.com/race/itzulia-basque-country',
        'https://www.procyclingstats.com/race/paris-roubaix',
        'https://www.procyclingstats.com/race/amstel-gold-race',
        'https://www.procyclingstats.com/race/la-fleche-wallone',
        'https://www.procyclingstats.com/race/liege-bastogne-liege',
        'https://www.procyclingstats.com/race/Eschborn-Frankfurt',
        'https://www.procyclingstats.com/race/tour-of-california',
        'https://www.procyclingstats.com/race/dauphine',
        'https://www.procyclingstats.com/race/san-sebastian',
        'https://www.procyclingstats.com/race/tour-de-pologne',
        'https://www.procyclingstats.com/race/ride-london-classic',
        'https://www.procyclingstats.com/race/cyclassics-hamburg',
        'https://www.procyclingstats.com/race/bretagne-classic',
        'https://www.procyclingstats.com/race/gp-quebec',
        'https://www.procyclingstats.com/race/gp-montreal',
        'https://www.procyclingstats.com/race/il-lombardia',
        'https://www.procyclingstats.com/race/tour-of-guangxi',

        # World Championships
        'https://www.procyclingstats.com/race/world-championship',
        'https://www.procyclingstats.com/race/world-championship-itt',

        # Pro tour
        'https://www.procyclingstats.com/race/vuelta-ciclista-a-la-provincia-de-san-juan',
        'https://www.procyclingstats.com/race/vuelta-a-la-comunidad-valenciana',
        'https://www.procyclingstats.com/race/tour-cycliste-international-la-provence',
        'https://www.procyclingstats.com/race/volta-ao-algarve',
        'https://www.procyclingstats.com/race/ruta-del-sol',
        'https://www.procyclingstats.com/race/tour-of-turkey',
        'https://www.procyclingstats.com/race/tour-of-the-alps',
        'https://www.procyclingstats.com/race/tour-de-yorkshire',
        'https://www.procyclingstats.com/race/4-jours-de-dunkerque',
        'https://www.procyclingstats.com/race/ster-elektro-tour',
        'https://www.procyclingstats.com/race/boucles-de-la-mayenne',
        'https://www.procyclingstats.com/race/tour-of-belgium',
        'https://www.procyclingstats.com/race/tour-of-slovenia',
        'https://www.procyclingstats.com/race/tour-of-austria',
        'https://www.procyclingstats.com/race/tour-de-wallonie',
        'https://www.procyclingstats.com/race/vuelta-a-burgos',
        'https://www.procyclingstats.com/race/arctic-race-of-norway',
        'https://www.procyclingstats.com/race/tour-of-denmark',
        'https://www.procyclingstats.com/race/deutschland-tour',
        'https://www.procyclingstats.com/race/tour-of-britain',
        'https://www.procyclingstats.com/race/tour-de-luxembourg',

        'https://www.procyclingstats.com/race/clasica-de-almeria',
        'https://www.procyclingstats.com/race/trofeo-laigueglia',
        'https://www.procyclingstats.com/race/les-boucles-du-dus-ardeche',
        'https://www.procyclingstats.com/race/kuurne-brussel-kuurne',
        'https://www.procyclingstats.com/race/la-drome-classic',
        'https://www.procyclingstats.com/race/gp-industria-artigianato',
        'https://www.procyclingstats.com/race/nokere-koers',
        'https://www.procyclingstats.com/race/gp-de-denain',
        'https://www.procyclingstats.com/race/bredene-koksijde-classic',
        'https://www.procyclingstats.com/race/gp-miguel-indurain',
        'https://www.procyclingstats.com/race/scheldeprijs',
        'https://www.procyclingstats.com/race/brabantse-pijl',
        'https://www.procyclingstats.com/race/tro-bro-leon',
        'https://www.procyclingstats.com/race/gp-de-plumelec',
        'https://www.procyclingstats.com/race/dwars-door-het-hageland',
        'https://www.procyclingstats.com/race/brussels-cycling-classic',
        'https://www.procyclingstats.com/race/gp-citta-di-peccioli',
        'https://www.procyclingstats.com/race/circuit-franco-belge',
        'https://www.procyclingstats.com/race/gp-de-fourmies',
        'https://www.procyclingstats.com/race/gp-de-wallonie',
        'https://www.procyclingstats.com/race/gp-impanis-van-petegem',
        'https://www.procyclingstats.com/race/coppa-bernocchi',
        'https://www.procyclingstats.com/race/giro-dell-emilia',
        'https://www.procyclingstats.com/race/munsterland-giro',
        'https://www.procyclingstats.com/race/tre-valli-varesine',
        'https://www.procyclingstats.com/race/milano-torino',
        'https://www.procyclingstats.com/race/gran-piemonte',
        'https://www.procyclingstats.com/race/paris-tours',

        # Olympic Games
        'https://www.procyclingstats.com/race/olympic-games',
        'https://www.procyclingstats.com/race/olympic-games-itt'
    ]
    until_year = 2019

    def __init__(self):
        self.connection = sqlite3.connect("pcs.db")
        self.cursor = self.connection.cursor()

    def parse(self, response):
        editions = response.xpath("//div[@class='ESNav editions']//option")
        for edition in editions:
            if int(edition.xpath("text()").get()) >= self.until_year:
                slug = edition.xpath("@value").get()
                if not self.is_edition_known(slug.replace("//results", "").replace("/results", "").replace("race/", "")):
                    yield response.follow("https://www.procyclingstats.com/"+slug, callback = self.parse_edition)

    def parse_edition(self, response):
        stages = response.xpath("//div[@class='ESNav stages']//option")
        if len(stages) > 0:
            for stage in stages:
                if "stage" in stage.xpath("./text()").get():
                    slug = stage.xpath("./@value").get().replace("race/", "").replace("//", "/").replace("/results", "")
                    if not self.is_race_known(slug):
                        yield response.follow("https://www.procyclingstats.com/race/"+slug, callback = self.parse_race)
        else:
            slug = response.request.url.replace("https://www.procyclingstats.com/race/", '').strip().replace("//", "/").replace("/results", "")
            if not self.is_race_known(slug):
                yield response.follow("https://www.procyclingstats.com/race/"+slug, callback = self.parse_race)        
    
    def parse_race(self, response):
        race = Race() 
        restabs = response.xpath("//ul[@class='restabs ']//a")
        isOneDayRace = len(restabs) == 0

        race_slug = response.request.url.replace("https://www.procyclingstats.com/race/", '').strip()               
        race['slug'] = race_slug
        race['season'] = int(response.xpath("//span[@class='year']/text()").get())
        race['name'] = response.xpath("//div[@class='entry race']/h1/text()").get().split(" (")[0]

        stage_info = response.xpath("//div[@class='entry race']/h2/span[@class='blue']/text()").get()
        if not isOneDayRace:      
            stage_info_digits = [int(s) for s in stage_info.split() if s.isdigit()]
            race['stage'] = stage_info_digits[0]
        else:
            race['stage'] = None

        if "ITT" in stage_info or "ITT" in race['name']:
            race['stage_type'] = "ITT"
        elif "TTT" in stage_info or "TTT" in race['name']:
            race['stage_type'] = "TTT"
        else:
            race['stage_type'] = "REGULAR"

        fuzzy_date = re.sub(r"(?<=[0-9])(st|nd|rd|th)", "", response.xpath("//div[@class='res-right']/text()").get())
        race['date'] = datetime.datetime.strptime(fuzzy_date, " %d %B %Y").strftime("%Y-%m-%d")

        race_course = response.xpath("//span[@class='red distance']/text()").get()
        if race_course:
            race['distance'] = float(race_course.strip("(").strip("k)"))
        else:
            race['distance'] = None

        difficulty = response.xpath("//div[@class='res-right']/a/text()").get()
        if not "*" in difficulty:
            race['difficulty'] = int(difficulty)
        else:
            race['difficulty'] = None

        all_riders = {}
        gc_time = None

        if isOneDayRace:
            if race['stage_type'] == "TTT":
                all_riders = getTTTResults(response.xpath("//div[@class='resultCont ']/div[@class='tttRidersCont']"), race_slug)
            else:
                all_riders = getStageResults(response.xpath("(//table[@class='basic results'])[1]/tbody/tr"), race_slug)
        else:
            gc_data_id = restabs.xpath("./span[@class='st4']/parent::a/@data-id").get()
            pc_data_id = restabs.xpath("./span[@class='st5']/parent::a/@data-id").get()
            kom_data_id = restabs.xpath("./span[@class='st7']/parent::a/@data-id").get()
            stage_data_id = restabs.xpath("(//ul[@class='restabs ']//a)[1]/@data-id").get()            
            
            
            stage_data = response.xpath("//div[@data-id='"+stage_data_id+"']//tbody/tr")
            if race['stage_type'] == "TTT":
                all_riders = getTTTResults(response.xpath("//div[@data-id='"+stage_data_id+"']/div[@class='tttRidersCont']"), race_slug)
            else:
                all_riders = getStageResults(stage_data, race_slug)

            if gc_data_id != None:
                gc_data = response.xpath("//div[@data-id='"+gc_data_id+"']//tbody/tr")
                for gc_row in gc_data:
                    rider = gc_row.xpath(".//a[1]/@href").get().replace("rider/", '')
                    rank = gc_row.xpath("./td[1]/text()").get()
                    time = timeStrToSeconds(gc_row.xpath(".//span[@class='timeff']/text()").get())

                    if rank and rank.isdigit():
                        all_riders[rider]['gc_rank'] = int(rank)

                    if isinstance(time, int):
                        if not gc_time:
                            gc_time = time
                            all_riders[rider]['gc_time'] = time
                        else:
                            all_riders[rider]['gc_time'] = time + gc_time  
            
            if pc_data_id != None:
                pc_data = response.xpath("//div[@data-id='"+pc_data_id+"']//tbody/tr")
                pc_points_col = getPointIndex(len(pc_data[0].xpath("./td")))
                for pc_row in pc_data:
                    rider = pc_row.xpath(".//a[1]/@href").get().replace("rider/", '')
                    rank = pc_row.xpath("./td[1]/text()").get()
                    points = pc_row.xpath("./td["+pc_points_col+"]/text()").get()

                    if rank and rank.isdigit():
                        all_riders[rider]['pc_rank'] = int(rank)

                    if points and points.isdigit():
                        all_riders[rider]['pc_points'] = int(points)

            if kom_data_id != None:
                kom_data = response.xpath("//div[@data-id='"+kom_data_id+"']//tbody/tr")
                kom_point_col = getPointIndex(len(kom_data[0].xpath("./td")))
                for kom_row in kom_data:
                    rider = kom_row.xpath(".//a[1]/@href").get().replace("rider/", '')
                    rank = kom_row.xpath("./td[1]/text()").get()
                    points = kom_row.xpath("./td["+kom_point_col+"]/text()").get()

                    if rank and rank.isdigit():
                        all_riders[rider]['kom_rank'] = int(rank)

                    if points and points.isdigit():
                        all_riders[rider]['kom_points'] = int(points)
        
        for result in all_riders.values():
            if not self.is_rider_known(result['rider']):
                yield response.follow("https://www.procyclingstats.com/rider/"+result['rider'], callback = self.parse_rider)
            yield result
        yield race

    def parse_rider(self, response):
        rider = Rider()        
        rider['slug'] = response.request.url.replace("https://www.procyclingstats.com/rider/", '').strip()
        rider['name'] = response.xpath("//div[@class='entry']/h1/text()").get()
        description = response.xpath("//meta[@name='description']/@content").get()
        rider['dob'] = description[description.find("(")+1:description.find(")")].replace("born ", '')
        yield rider

    def is_rider_known(self, slug):
        self.cursor.execute("""SELECT * FROM riders WHERE slug=?""", (slug,))
        result = self.cursor.fetchone()
        if result:
            return True
        else:
            return False

    def is_race_known(self, slug):
        self.cursor.execute("""SELECT * FROM results WHERE race=?""", (slug,))
        result = self.cursor.fetchone()
        if result:
            return True
        else:
            return False

    def is_edition_known(self, slug):
        self.cursor.execute("""SELECT * FROM results WHERE race LIKE ?""", (slug+'%',))
        result = self.cursor.fetchone()
        if result:
            return True
        else:
            return False

def timeStrToSeconds(strTime):
    if strTime.count(':') == 0:
        return None
    if strTime.count(':') == 1:
        strTime = "0:" + strTime
    return sum([a*b for a,b in zip([3600,60,1], map(int,strTime.split(':')))])

def prepareResult(race, rider, team):
    result = Result()
    result['race'] = race
    result['rider'] = rider
    result['team'] = team
    result['stage_rank'] = None
    result['stage_time'] = None
    result['gc_rank'] = None
    result['gc_time'] = None
    result['pc_rank'] = None
    result['pc_points'] = None
    result['kom_rank'] = None
    result['kom_points'] = None

    return result

def getStageResults(rows, race):
    all_riders = {}
    winning_time = None
    for row in rows:
        rider = row.xpath("(.//a)[1]/@href").get().replace("rider/", '')
        team = row.xpath("(.//a)[2]/@href").get()

        all_riders[rider] = prepareResult(race, rider, team)

        rank = row.xpath("./td[1]/text()").get()            
        time = timeStrToSeconds(row.xpath(".//span[@class='timeff']/text()").get())

        if rank and rank.isdigit():
            all_riders[rider]['stage_rank'] = int(rank)

        if isinstance(time, int):
            if not winning_time:
                winning_time = time
                all_riders[rider]['stage_time'] = time
            else:
                all_riders[rider]['stage_time'] = time + winning_time

    return all_riders

def getTTTResults(tttDivs, race):
    all_riders = {}
    winning_time = None
    for teamDiv in tttDivs:
        team = teamDiv.xpath("./div[@class='resTTTb']//a/@href").get()
        rank = teamDiv.xpath("(./div[@class='resTTTb']/span)[1]/text()").get().replace(" ", "")
        time = timeStrToSeconds(teamDiv.xpath("(./div[@class='resTTTb']/span)[3]/text()").get())
        for rider_row in teamDiv.xpath("./div[@class='res_line resTTTr']"):
            rider = rider_row.xpath(".//a/@href").get().replace("rider/", '')
            additional_time_string = rider_row.xpath(".//span[@class='blue']/text()").get()
            if additional_time_string:
                additional_time = timeStrToSeconds(additional_time_string.replace("+", ""))

            all_riders[rider] = prepareResult(race, rider, team)

            if rank and rank.isdigit():
                all_riders[rider]['stage_rank'] = int(rank)

            all_riders[rider]['stage_time'] = time
            if additional_time_string and isinstance(additional_time, int) and isinstance(time, int):
                all_riders[rider]['stage_time'] = all_riders[rider]['stage_time'] + additional_time 

    return all_riders

def getPointIndex(numCols):
    if numCols == 11:
        return "9"
    else:
        return str(numCols - 1)