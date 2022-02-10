import os
import re
import sys
import requests
from bs4 import BeautifulSoup

def download_midis(url):
    url = url + "/" if url[-1] != "/" else url
    
    try:
        req = requests.get(url)
    except:
        print(f"ERRO ao carregar o endereço {url}")
        return
    
    if req.status_code != 200:
        print(f"ERRO na requisição do endereço {url}")
        return
    
    console_name = [x for x in url.split("/") if len(x)][-1].upper()
    
    soup = BeautifulSoup(req.text, "html.parser")
    cells = soup.find_all("td")
    
    game_name = ""
    for c in cells:
        if "class" in c.attrs and c["class"][0] == "header":
            header_link = c.find("a")
            game_name = header_link["name"]
            continue
        
        td_link = c.find("a")
        if td_link is None:
            continue
        else:
            if ".mid" in td_link["href"].lower():
                music_name = re.sub(r"\W+", "", td_link.text.strip())
                filename = f"[{console_name}][{game_name}]_{music_name}.mid"
                filename = filename.replace("\"", "")
                download_url = url + td_link["href"]
                
                try:
                    raw = requests.get(download_url, allow_redirects=True)
                except:
                    print(f"ERRO ao requisitar MIDI {download_url}")
                    continue
                
                if raw.status_code != 200:
                    print(f"ERRO ao baixar MIDI {download_url}")
                    continue
                
                midi_file = open(filename, "wb")
                midi_file.write(raw.content)
                midi_file.close()
                
                print(f"Donwload OK:\t{filename}")
    

def main_script():
    if len(sys.argv) != 2:
        print("ERRO! Número errado de argumentos!")
        print("USO:  python vgmusic.py <url>")
        sys.exit()
    
    download_midis(sys.argv[1])


if __name__ == "__main__":
    main_script()

