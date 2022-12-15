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


# Our lists of targeted players
CHAMPS = ['magnus-carlsen', 'viswanathan-anand', 'vladimir-kramnik', 'garry-kasparov', 'anatoly-karpov', 'bobby-fischer',
          'boris-spassky', 'tigran-petrosian', 'mikhail-tal', 'vasily-smyslov', 'mikhail-botvinnik', 'max-euwe',
          'alexander-alekhine', 'jose-raul-capablanca', 'emanuel-lasker', 'wilhelm-steinitz']

MASTERS = ['magnus-carlsen', 'ding-liren', 'ian-nepomniachtchi', 'alireza-firouzja', 'hikaru-nakamura', 'fabiano-caruana',
       'anish-giri', 'wesley-so', 'viswanathan-anand', 'sergey-karjakin', 'teimour-radjabov', 'alexander-grischuk',
       'leinier-dominguez-perez', 'shakhriyar-mamedyarov', 'richard-rapport', 'maxime-vachier-lagrave']


# Don't double-count carlsen and anand
players = list(set(MASTERS + CHAMPS))


# Per player, get their primary player page
for player_name in players:
    driver.get(f"https://www.chess.com/games/{player_name}")
    page = 1

    # Use Selenium to iterate over pages until there is no next one
    completed = False
    while not completed:
        try:
            # Per page, try: clicking the select all button, clicking the download button, clicking the next page button
            for class_ in [GM_CLASS, DL_CLASS, NP_CLASS]:

                element = driver.find_element(By.CLASS_NAME, class_)

                driver.execute_script(f'window.scrollTo({element.location["x"]},{element.location["y"]});')
                
                # When the next page button is grayed out, leave this player.
                if class_ == NP_CLASS and 'ui_pagination-item-disabled' in element.get_attribute("class"):
                    completed = True
                    break
                
                # Skip downloading from pages we've already downloaded, in case of errors in this or previous iterations.
                if class_ in [GM_CLASS, DL_CLASS] and os.path.exists(f'{game_dir}/{player_name}/page-{page}.pgn'):
                    continue
                
                actions.move_to_element(element).click(element).perform()

                # Account for a variety of download speeds
                if class_ == DL_CLASS:
                    time.sleep(2)
                    if not os.path.isdir(f'{game_dir}/{player_name}'):
                        os.makedirs(f'{game_dir}/{player_name}')
                    # Move the downloaded file from the downloads folder to the project directory.
                    shutil.move(f'{os.path.expanduser("~")}/Downloads/{file_name}', f'{game_dir}/{player_name}/page-{page}.pgn')

                # Wait for the next page to load
                if class_ == NP_CLASS:
                    page += 1
                    time.sleep(1)
        except FileNotFoundError:
            print(f"{player_name}: {page}")
        except NoSuchElementException as e:
            print(f"{player_name}: {page}")
