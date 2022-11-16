import json
import re
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

    def find_title(self, soup):
        return soup.find("meta", property="og:title")["content"]

    def find_author(self, soup):
        return soup.find("meta", property="og:video:tag")["content"]

    def find_description(self, soup):
        return soup.find("meta", property="og:description")["content"]

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



if __name__ == "__main__" :
    print('Lancement')

    # Read input file
    f = open('./input.json')
    data = json.load(f)
    f.close()

    # Start scrapping
    scrapper = Scrapper(data["videos_id"])
    videos = scrapper.scrap()

    # Create a dictionnary from array  
    dict_videos = dict(zip(data["videos_id"],list(map(lambda x : x.__dict__, videos))))

    # Save data in json file
    # json_object = json.dumps(dict_videos) 
    # print(json_object)

    with open("output.json", "w") as outfile:
        json.dump(dict_videos, outfile, indent = 4)

