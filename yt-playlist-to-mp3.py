from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EXP_CON
from selenium.common.exceptions import TimeoutException
from webdriver_manager.firefox import GeckoDriverManager
import pytube as pt
import os

links = []

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
url = input("Enter the link of the playlist: ")
print("The process has started, DO NOT close!\n")
driver.get(url)

try:
    elements_ = WebDriverWait(driver, 15).until(
        EXP_CON.presence_of_element_located(
            (By.XPATH, '//*[@id="playlist-items"]')))
    print("Page is now ready to be scraped! Fetching Links...")
except TimeoutException:
    print("Page Loading Timeout...")

playlist_items = driver.find_elements(By.XPATH, '//*[@id="playlist-items"]')

for item in playlist_items:
    sub_ele = item.find_element(By.ID, 'wc-endpoint')
    video_link = sub_ele.get_attribute("href")
    video_link_cleaned = video_link[0:video_link.index("&")]
    links.append(video_link_cleaned)

print("Fetching Complete! Total videos: {0}\n".format(len(links)))

print("Downloading videos with MP4 Extension...\n")

output_folder = os.getcwd() + "\\output"

for link in links:
    yt_ref = pt.YouTube(link)
    yt_audio = yt_ref.streams.get_audio_only()
    if not (yt_audio.exists_at_path("{0}\\output\\{1}".format(
            os.getcwd(), yt_audio.default_filename))):
        dl_audio = yt_audio.download(
            output_path=("{0}\\output".format(os.getcwd())))
        print("[{0}/{1}] ({2})\t {3} has been downloaded!".format(
            len(os.listdir(output_folder)), len(links),
            "{0:.0%}".format(len(os.listdir(output_folder)) / len(links)),
            yt_audio.title))
    else:
        print("{0} already exists! Skipping...".format(yt_audio.title))

print("All videos were downloaded! Converting to MP3...")

for count, file in enumerate(os.listdir(output_folder)):
    base_name, ext = os.path.splitext(file)
    mod_name = base_name + '.mp3'
    abs_old = "{0}\\{1}".format(output_folder, file)
    abs_new = "{0}\\{1}".format(output_folder, mod_name)
    os.rename(abs_old, abs_new)

print("Conversion successful! The playlist has been downloaded!")