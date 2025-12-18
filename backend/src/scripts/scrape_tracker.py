from bs4 import BeautifulSoup
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.action_chains import ActionChains
from collections import defaultdict
import csv
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.color import Color
from selenium.webdriver.common.keys import Keys


def meta_leaderboard():
    """
    Scrape Marvel Rivals leaderboard data from rivalsmeta.com and return a list of player names and UIDs.
    """
    url = "https://rivalsmeta.com"
    driver = uc.Chrome(headless=False)
    driver.get(url)
    rows = []

    time.sleep(15)
    leaderboard = driver.find_element("css selector", "a[href='/leaderboard']")
    action = ActionChains(driver)
    action.move_to_element(leaderboard)
    leaderboard.click()
    time.sleep(1.5)
    players = driver.find_elements("css selector", "a[class='profile']")
    print(f"Found {len(players)} players")
    for player in players:
        
        url = player.get_attribute("href")
        print(url)
        rivals_uid = url.split("/")[-1]
        print(rivals_uid)
        print ("Player:", player.text)
        #js.append(rivals_uid)
        rows.append({"Name": player.text, "Rivals_uid": rivals_uid})
    
 
    fieldnames = ["Name", "Rivals_uid"]

    with open('../data/S5_leaderboard_meta.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
    time.sleep(2)
    driver.quit()
    driver = None
    return rows


def tracker_leaderboard():
    """
    Scrape Marvel Rivals leaderboard data from tracker.gg and save it to a CSV file.
    """
    url = "https://tracker.gg/marvel-rivals"
    driver = uc.Chrome(headless=False)
    try:
        driver.get(url)

        time.sleep(5)
    
        leaderboard = driver.find_element("css selector", "span[class='name name--expandable']")
        action = ActionChains(driver)
        action.move_to_element(leaderboard)
        leaderboard.click()
        time.sleep(5)
    
        HEX_COLOUR = Color.from_string('#FFFFFF')

        js = []         
    
        for i in range(5):
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a.flex.items-center.gap-4.no-underline"))
            )

            players = driver.find_elements(By.XPATH, f"(//a[@class='flex items-center gap-4 no-underline'])")
            j = 0
            for player in players:
                j += 1
                if j > 99:
                    break
                login_button_colour = Color.from_string(player.value_of_css_property('color'))
                if login_button_colour != HEX_COLOUR:
                    continue
                player_name = player.text
                dict_entry = {"Name": player_name}
                js.append(dict_entry)
            WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, f"(//a[@title='Go to page {i + 2}'])"))
            )

            next_page = driver.find_element(By.XPATH, f"(//a[@title='Go to page {i + 2}'])")

            action.move_to_element(next_page)
            next_page.click()

        merged = defaultdict(dict)

        for entry in js:
            name = entry["Name"]
            merged[name].update(entry)

        merged_list = list(merged.values())

        # Collect all unique keys across all entries
        fieldnames = set()
        for entry in merged_list:
            fieldnames.update(entry.keys())
        fieldnames = list(fieldnames)

        with open('../data/s5_leaderboard.csv', 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(merged_list)

        time.sleep(2)
    finally:
        driver.quit()
    return "Successfully scraped data and saved to S5_leaderboard_wr.csv"


def rivals():
    """
    Scrape Marvel Rivals hero data from the official website and save it to a CSV file.
    """
    
    url = "https://www.marvelrivals.com/heroes_data/index.html"
    driver = uc.Chrome(headless=False)
    driver.get(url)

    time.sleep(.5)
    comp = driver.find_element("css selector", "div[class='djms-btn-item']")
    action = ActionChains(driver)
    action.move_to_element(comp)
    comp.click()
    time.sleep(.5)
    comp.click()
    print(comp.text)
    time.sleep(2)

    ranks = ['Bronze','Silver','Gold','Platinum','Diamond','Grandmaster', 'Celestial+']
    js = [] 
    iter=0
    while iter in range(len(ranks)):
        select = driver.find_element("css selector","div[class='dan-h']")
        action.move_to_element(select)
        select.click()
        time.sleep(1)
        fix = driver.find_elements("css selector","div[class='dan-btn-item']")[iter]
        action.move_to_element(fix)
        fix.click()

        #select.select_by_visible_text(option.text) # To select by visible text
        html = driver.page_source
        soup = BeautifulSoup(html, features="html.parser")
        ps = soup.find_all('p')

        j = 0
        for (i, tag) in enumerate(ps):
            if (j % 3 == 1 and i + 3 < len(ps)):
                js.append({
                    "Name": tag.text.strip(),
                    f"{ranks[iter]} PR": ps[i + 1].text,
                    f"{ranks[iter]} WR": ps[i + 2].text
                })

            if (tag.text == 'RANK' or j > 0):
                j+=1
        
        iter+=1

    merged = defaultdict(dict)

    for entry in js:
        name = entry["Name"]
        merged[name].update(entry)

    # Convert to list of dicts
    merged_list = list(merged.values())

    with open('../data/Official_Hero_WR.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=merged_list[0].keys())
        writer.writeheader()
        writer.writerows(merged_list)

    time.sleep(2)
    driver.quit()
    return "Successfully scraped data and saved to output.csv"

def tracker_player(player_tag):
    """
    Scrapes the tracker.gg site for data on the player profile matching the username player_tag
    
    Args:
        player_tag: The username of the player to be looked up

    Returns:
        The player data structured as a dict
    """

    url = "https://tracker.gg/marvel-rivals"
    
    driver = uc.Chrome(headless=False)
    #soup = BeautifulSoup(html_content, 'html.parser')
    driver.get(url)

    time.sleep(.5)
    search_box = driver.find_element("css selector", "input[aria-label='Enter In-Game Name or UID']")
    time.sleep(.5)
    search_box.send_keys(player_tag)
    time.sleep(.5)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)
    spans = driver.find_elements("tag name", "span")[:200]
    time.sleep(3)
    js = []         
    
    for (i, span) in enumerate(spans):
        #print(f"{i}: {span.text}")
        if span.text == 'WR' and i + 1 < len(spans) and i - 1 >= 0 :
            js.append(f"{spans[i - 1].text} :  {spans[i + 2].text}")
          
    matches = driver.find_elements("class name", "v3-tabs__item")[1]
    action = ActionChains(driver)
    action.move_to_element(matches)
    matches.click()
    time.sleep(.5)
    html = driver.page_source
    soup = BeautifulSoup(html, features="html.parser")
    ps = soup.find_all('span')[:500]

    j = 0
    for (i, tag) in enumerate(ps):
            print(tag.text)
            if (j % 3 == 1 and i + 10 < len(ps)):
                js.append({
                    "Name": tag.text.strip(),
                    f"PR": ps[i + 1].text,
                    f"WR": ps[i + 2].text
                })

            if (tag.text == 'RANK' or j > 0):
                j+=1
    time.sleep(1)
    
    driver.quit()
    return js

def meta_player(player_tag):
    """
    Scrapes the rivalsmeta site for data on the player profile matching the username player_tag
    
    Args:
        player_tag: The username of the player to be looked up

    Returns:
        The player data structured as a list
    """

    url = "https://rivalsmeta.com"
    driver = uc.Chrome(headless=False)
    driver.get(url)

    time.sleep(.5)
    search_box = driver.find_elements("tag name", "input")[1]
    action = ActionChains(driver)
    action.move_to_element(search_box)
    search_box.click()
    time.sleep(.5)
    search_box.send_keys(player_tag)
    time.sleep(1.5)
    player = driver.find_element("css selector", "a[class='player']")
    action = ActionChains(driver)
    action.move_to_element(player)
    player.click()
    time.sleep(2)
    spans = driver.find_elements("tag name", "div")[:400]
    time.sleep(1)
    js = []         
    
    j = 0
    for (i, span) in enumerate(spans):
        #print(f"{i}: {span.text}")
        #span.text == 'WR' and 
        if i + 3 < len(spans) and i - 1 >= 0 and j % 3 == 0:
            js.append(f"{i} : {{ {span.text}, {spans[i - 1].text},  {spans[i + 2].text} }}")
        j += 1
    #texts = [span.text for span in spans]
    time.sleep(2)
    driver.quit()
    return js


if __name__ == "__main__":
    rivals()