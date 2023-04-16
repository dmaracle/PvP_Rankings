from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv

# URLs to swap in/out (In order)
url_list = [
        'US/2/', 'US/3/', 'US/5/',
        'EU/2/', 'EU/3/', 'EU/5/',
        'OCE/2/', 'OCE/3/', 'OCE/5/'
    ]

# Headers for when CSV File is saved
csv_header_list = [
    'Rank', 'Rating', 'Name', 'Class', 'Server', 'Win_Loss', 'Win_Perc'
    ]

# player list to be filled with data
player_list = []

# Creating function to find highest page number
def find_max_page_number(soup):
    number_soup = soup.find_all("div", class_="leaderboards__pagination col-12")
    for div in number_soup:
        div_string = div.find('strong').text
        max_num = int(div_string[5:7])
    return max_num

def save_csv(csv_file_name):
    with open(f"{csv_file_name}.csv","w",newline='', encoding='utf-8') as my_csv:
        csvWriter = csv.writer(my_csv,delimiter=',')
        csvWriter.writerow(csv_header_list)
        csvWriter.writerows(player_list)

# Giving driver proper path so it will run
driver = webdriver.Chrome(r"C:\Users\Dmara\OneDrive\Documents\Web_Scrape\chromedriver.exe")  

# Run Main Loop of Program
for num_loop in range(len(url_list)):
    
    # Loading the driver with a url - changes based on loop 
    driver.get(f"https://ironforge.pro/pvp/leaderboards/archive/season-5/{url_list[num_loop]}")
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # Pulling the html from the soup
    for y in range(find_max_page_number(soup)-1):
        small_soup = BeautifulSoup(driver.page_source, "html.parser")
        player_ranks = small_soup.find_all("td", class_="leaderboards__table_ranking")
        player_ratings = small_soup.find_all("td", class_="leaderboards__table_rating")
        player_names = small_soup.find_all("td", class_="leaderboards__table_name")
        player_classes = small_soup.find_all("td", class_="leaderboards__table_class")
        player_servers = small_soup.find_all("td", class_="leaderboards__table_server")
        player_win_loss_ratios = small_soup.find_all("td", class_="leaderboards__table_wl")
        player_win_percentages = small_soup.find_all("td", class_="leaderboards__table_wr")

        # Append pulled data to list
        for z in range(len(player_ranks)):
            player_rank = player_ranks[z].text
            player_rating = player_ratings[z].text
            player_name = player_names[z].text
            player_class = player_classes[z].text
            player_server = player_servers[z].text
            player_win_loss_ratio = player_win_loss_ratios[z].text
            player_win_percentage = player_win_percentages[z].text
            player = [
                player_rank, player_rating, player_name, player_class, 
                player_server, player_win_loss_ratio, player_win_percentage
                ]
            player_list.append(player)

        # Click to the next page after the data is gathered and stored
        driver.find_element_by_xpath('//button[normalize-space()=">"]').click()

    # Name the CSV File to be saved
    csv_file_name = url_list[num_loop].replace("/", "_")
    save_csv(csv_file_name)
    
    # Write code here to clear the list to prepare for next bracket
    player_list.clear()
    
# Close the driver and end the program
driver.quit()  