import os
import sys

sys.path.append('.')
sys.path.append('../')
import unittest

import pytest
import requests
from bs4 import BeautifulSoup

import scrapper as sc

# Test command line
class TestMain(unittest.TestCase) :

    #Test constructor
    def test_init(self):
        argv = ['scrapper.py', '--output', 'outputtest.json', '--input', 'inputtest.json']
        self.assertEqual(sc.main(argv), 1)

# Test File manager :

class TestFileManager(unittest.TestCase) :

    #Test constructor
    def test_init(self):
        input_file = "inputtest.json"
        output_file = "outputtest.json"
        manager = sc.FilesManager(input_file, output_file)
        self.assertEqual(manager.input_file, input_file)
        self.assertEqual(manager.output_file, output_file)

    # Test read
    def test_read(self):
        input_file = "inputtest.json"
        output_file = "outputtest.json"
        data = sc.FilesManager("inputtest.json", output_file).read()
        self.assertEqual(data,{'videos_id' : ['fmsoym8I-3o', 'JhWZWXvN_yo']})            

    # Test save
    def test_save(self):
        data = {'videos_id' : ['fmsoym8I-3o', 'JhWZWXvN_yo']}
        videos = [sc.Video(id='fmsoym8I-3o', title='Pierre Niney : L’interview face cachée par HugoDécrypte', author='HugoDécrypte', likes=0, description="🍿 L'acteur Pierre Niney est dans L’interview face cachée ! Ces prochains mois, le format revient plus fort avec des artistes, sportifs, etc.🔔 Abonnez-vous ...", links=[], comments=[]), sc.Video(id='JhWZWXvN_yo', title='ELISE LUCET EST SUB CHEZ MOI ?! (Débrief Cash Investigation)', author='ZeratoR', likes=0, description='ABONNE TOI, par pitié : https://www.youtube.com/user/ZeratoRSC2/?sub_confirmation=1Retrouvez-moi en live sur : https://www.twitch.tv/zeratorVOD du live : htt...', links=['https://www.youtube.com', 'https://www.twitch.tv'], comments=[])]
        input_file = "inputtest.json"
        output_file = "outputtest.json"
        sc.FilesManager(input_file, output_file).save(data,videos)
        self.assertTrue(os.path.exists(output_file) and os.path.getsize(output_file)!=0)            


# Tests Scrapper :

class TestScrapper(unittest.TestCase) : 

    #Test constructor
    def test_init(self):
        data = { "videos_id" : [ "fmsoym8I-3o", "JhWZWXvN_yo" ] }
        scrapper = sc.Scrapper(data["videos_id"])
        self.assertEqual(scrapper.list_id_vid, data["videos_id"])

    # Test Find title
    def test_find_title(self):
        data = { "videos_id" : [ "fmsoym8I-3o"] }
        req = requests.get("https://www.youtube.com/watch?v=fmsoym8I-3o")
        soup = BeautifulSoup(req.content, 'html.parser')
        title = sc.Scrapper(data["videos_id"]).find_title(soup)
        self.assertEqual(title, "Pierre Niney : L\u2019interview face cach\u00e9e par HugoD\u00e9crypte" )

    def test_find_title_null(self):
        data = { "videos_id" : [ "000000"] }
        req = requests.get("https://www.youtube.com/watch?v=000000")
        soup = BeautifulSoup(req.content, 'html.parser')
        title = sc.Scrapper(data["videos_id"]).find_title(soup)
        self.assertEqual(title,"")

    # Test Find author
    def test_find_author(self):
        data = { "videos_id" : [ "fmsoym8I-3o"] }
        req = requests.get("https://www.youtube.com/watch?v=fmsoym8I-3o")
        soup = BeautifulSoup(req.content, 'html.parser')
        author = sc.Scrapper(data["videos_id"]).find_author(soup)
        self.assertEqual(author, "HugoD\u00e9crypte")

    def test_find_author_null(self):
        data = { "videos_id" : [ "000000"] }
        req = requests.get("https://www.youtube.com/watch?v=000000")
        soup = BeautifulSoup(req.content, 'html.parser')
        author = sc.Scrapper(data["videos_id"]).find_author(soup)
        self.assertEqual(author, "")
    
    # Test Find description 
    def test_find_description(self):
        data = { "videos_id" : [ "JhWZWXvN_yo"] }
        req = requests.get("https://www.youtube.com/watch?v=JhWZWXvN_yo")
        soup = BeautifulSoup(req.content, 'html.parser')
        desc = sc.Scrapper(data["videos_id"]).find_description(soup)
        self.assertEqual(desc,"ABONNE TOI, par piti\u00e9 : https://www.youtube.com/user/ZeratoRSC2/?sub_confirmation=1Retrouvez-moi en live sur : https://www.twitch.tv/zeratorVOD du live : htt...")

    def test_find_description_null(self):
        data = { "videos_id" : [ "000000"] }
        req = requests.get("https://www.youtube.com/watch?v=000000")
        soup = BeautifulSoup(req.content, 'html.parser')
        desc = sc.Scrapper(data["videos_id"]).find_description(soup)
        self.assertEqual(desc, "")

    # Test find_links
    def test_find_links(self):
        data = { "videos_id" : [ "JhWZWXvN_yo"] }
        description =  "ABONNE TOI, par piti\u00e9 : https://www.youtube.com/user/ZeratoRSC2/?sub_confirmation=1Retrouvez-moi en live sur : https://www.twitch.tv/zeratorVOD du live : htt..."
        links = sc.Scrapper(data["videos_id"]).find_links(description)
        self.assertEqual(links,["https://www.youtube.com","https://www.twitch.tv"])

    def test_find_links_null(self):
        data = { "videos_id" : [ "000000"] }
        description =  ""
        links = sc.Scrapper(data["videos_id"]).find_links(description)
        self.assertEqual(links, [])

    # Test Scrap
    def test_find_scrap(self):
        data = { "videos_id" : ["fmsoym8I-3o","JhWZWXvN_yo","vcORt-798EU","dV360CxA2BQ","000000"]}
        result = sc.Scrapper(data["videos_id"]).scrap()
        self.assertEqual(len(result), len(data["videos_id"]))




# Test conditions

