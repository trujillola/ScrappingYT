# Title : Python script for YouTube scrapping
# Author name : Laura Trujillo
# Mail : trujillola@cy-tech.fr
# Version : 1.0.0
# Date : 16/11/2022

import json
import os
import re
import sys
from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup

@dataclass
class Video:

    id: str
    title: str
    author: str
    likes: int
    description: str
    links: list
    comments: list   

    def __init__(self, id, title, author, likes, description,links,comments) -> None:
        self.id = id
        self.title = title
        self.author = author
        self.likes = int(likes)
        self.description = description
        self.links = links
        self.comments = comments

@dataclass
class Scrapper :

    list_id_vid : list

    def __init__(self,list_id_vid) -> None:
        self.list_id_vid = list_id_vid

    def _get_list_id_vid(self):
        return self._list_id_vid

    def _set_list_id_vid(self, val):
        self._list_id_vid = val

    def find_title(self, soup):
        try :
            res = soup.find("meta", property="og:title")["content"]
        except :
            res = ""
        return res

    def find_author(self, soup):
        try :
            res = soup.find("meta", property="og:video:tag")["content"]
        except : 
            res = ""
        return res

    def find_description(self, soup):
        try : 
            res = soup.find("meta", property="og:description")["content"]
        except :
            res = ""
        return res

    def find_links(self, description):
        return re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', description)

    # def find_comments(self, soup):
    #     
    #     return 1

    def find_likes(self, soup):
        list_script_tags = soup.findAll("script")
        # print(list_script_tags)
        return "0"

    def scrap(self):
        print('Scrapping...')
        videos = list()
        for id in self.list_id_vid:
            url = "https://www.youtube.com/watch?v="+id
           
            req = requests.get(url)
            soup = BeautifulSoup(req.content, 'html.parser')

            title = self.find_title(soup)
            author = self.find_author(soup)
            likes = self.find_likes(soup)
            description = self.find_description(soup)
            links = self.find_links(description)
            comments = []

            videos.append(Video(id,title,author,int(likes),description, links, comments))
       
        return videos
    list_id_vid = property(
        fget = _get_list_id_vid,
        fset = _set_list_id_vid
    )


@dataclass
class FilesManager :

    input_file : str
    output_file : str

    def __init__(self, input_file, output_file) -> None:
            self.input_file = input_file
            self.output_file = output_file

    def read(self) :
        print("Reading file.")
        with open(self.input_file,"r") as f :
            data = json.load(f)
        return data

    def save(self,data,videos) :
        print('Saving data.') 
        dict_videos = dict(zip(data,list(map(lambda x : x.__dict__, videos))))

        with open(self.output_file, "w") as outfile:
            json.dump(dict_videos, outfile, indent = 4)



def main(argv) : 
    if len(argv) == 5 :
        if argv[1] == "--input" and argv[3] == "--output" :
            input_file = argv[2]
            output_file = argv[4]
        elif argv[1] == "--output" and argv[3] == "--input" :
            input_file = argv[4]
            output_file = argv[2]
        else : 
            exit("WRONG ARGUMENTS")

        if os.path.isfile(os.path.abspath(os.getcwd())+'/'+ str(input_file)) :    
            print('Launching.')
            print(input_file)
            fileManager = FilesManager(input_file, output_file)
            
            # Start scrapping
            scrapper = Scrapper(fileManager.read()["videos_id"])
            videos = scrapper.scrap()

            # Create a dictionnary from array 
            fileManager.save(scrapper.list_id_vid,videos)

            print('Job done.')
        else : 
            exit("INPUT FILE DOESN'T EXIST")
    else :
        exit("WRONG NUMBER OF PARAMETERS")
    return 1

if __name__ == "__main__" :
    main(sys.argv)
   
