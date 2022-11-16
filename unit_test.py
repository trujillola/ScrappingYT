import unittest

import pytest
import requests
from bs4 import BeautifulSoup

import scrapper as sc

# Tests de la classe Scrapper :

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
        print(desc)
        print("ABONNE TOI, par piti\u00e9 : https://www.youtube.com/user/ZeratoRSC2/?sub_confirmation=1Retrouvez-moi en live sur : https://www.twitch.tv/zeratorVOD du live : htt...")
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



#test ligne de commande

#Test des conditions