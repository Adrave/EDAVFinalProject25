# import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
import time
import shutil
import os


driver = webdriver.Firefox()
actions = ActionChains(driver)
game_dir = 'chess-games'
file_name = 'master_games.pgn'

GM_CLASS = 'master-games-check-all'
DL_CLASS = 'master-games-download-icon'
NP_CLASS = 'pagination-next'

if not os.path.isdir(game_dir):
    os.makedirs(game_dir)

# Correct control loop, something clearly isn't functioning for the actual looping part
champs = ['magnus-carlsen', 'viswanathan-anand', 'vladimir-kramnik', 'garry-kasparov', 'anatoly-karpov', 'bobby-fischer',
          'boris-spassky', 'tigran-petrosian', 'mikhail-tal', 'vasily-smyslov', 'mikhail-botvinnik', 'max-euwe',
          'alexander-alekhine', 'jose-raul-capablanca', 'emanuel-lasker', 'wilhelm-steinitz']

gms = ['magnus-carlsen', 'ding-liren', 'ian-nepomniachtchi', 'alireza-firouzja', 'hikaru-nakamura', 'fabiano-caruana',
       'anish-giri', 'wesley-so', 'viswanathan-anand', 'sergey-karjakin', 'teimour-radjabov', 'alexander-grischuk',
       'leinier-dominguez-perez', 'shakhriyar-mamedyarov', 'richard-rapport', 'maxime-vachier-lagrave']

players = list(set(gms + champs))

for player_name in players:
    driver.get(f"https://www.chess.com/games/{player_name}")
    page = 1
    completed = False
    while not completed:
        try:
            for class_ in [GM_CLASS, DL_CLASS, NP_CLASS]:

                element = driver.find_element(By.CLASS_NAME, class_)

                driver.execute_script(f'window.scrollTo({element.location["x"]},{element.location["y"]});')
                
                if class_ == NP_CLASS and 'ui_pagination-item-disabled' in element.get_attribute("class"):
                    completed = True
                    break

                if class_ in [GM_CLASS, DL_CLASS] and os.path.exists(f'{game_dir}/{player_name}/page-{page}.pgn'):
                    continue
                
                actions.move_to_element(element).click(element).perform()
                if class_ == DL_CLASS:
                    time.sleep(2)
                    if not os.path.isdir(f'{game_dir}/{player_name}'):
                        os.makedirs(f'{game_dir}/{player_name}')
                    shutil.move(f'{os.path.expanduser("~")}/Downloads/{file_name}', f'{game_dir}/{player_name}/page-{page}.pgn')
                if class_ == NP_CLASS:
                    page += 1
                    time.sleep(1)
        except FileNotFoundError:
            print(f"{player_name}: {page}")
        except NoSuchElementException as e:
            print(f"{player_name}: {page}")
