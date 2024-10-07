#!/usr/bin/python3
import urllib3
from bs4 import BeautifulSoup
import re
import argparse
from rich.live import Live
from rich.table import Table
from rich import box

def menu():
    parser = argparse.ArgumentParser(description='Search custom guitar flash custom song')
    parser.add_argument("-s", "--search", help='Band name or song title',required=True)
    parser.add_argument("-l", "--limit", help='Limit search output',required=False,default=0,type=int)
    
    return parser.parse_args()

def req_list(page):
    result = http.request("GET",base_url+str(page))
    return BeautifulSoup(result.data,'html.parser')

args = menu()

# Creating a PoolManager instance for sending requests.
http = urllib3.PoolManager()

base_url = "https://www.guitarflash.com/custom/lista.asp?pag="

first_page = req_list(0)
total_page = int(re.search(r'divididas em(.*?)páginas!',first_page.body.text).group(1))

match_songs = []

table = Table(box=box.SQUARE)
table.add_column("Link")
table.add_column("Songs")
table.add_column("Difficulty")

with Live(table,refresh_per_second=1,vertical_overflow="visible"):
    for page in range(0,total_page):
        result_page = req_list(page)
        for songs in result_page.find_all('a')[1:]:
            if args.search.upper() in songs.text.upper():
                if songs.get('href') not in match_songs:
                    table.add_row(songs.get('href'), songs.text ,songs.find_next("td").text)
                    match_songs.append(songs.get('href'))
                    if args.limit:
                        if table.row_count > args.limit:
                            exit(0)