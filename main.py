import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import pydub
import urllib
import speech_recognition

data_path = "PATH TO MAIN.PY"

# startet Chromedriver und ruft die Website auf
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.get("https://www.google.com/recaptcha/api2/demo")

# reCAPTCHA Frame wird gesucht und ausgewählt
frames = browser.find_elements(By.TAG_NAME, "iframe")
browser.switch_to.frame(frames[0])

# zufällige Zeit zwischen 2 & 4 Sekunden warten um menschliches Verhalten zu imitieren
time.sleep(random.randint(2, 4))
browser.find_element(By.CLASS_NAME, "recaptcha-checkbox-border").click()
browser.switch_to.default_content()

# Audiobutton auswählen und zur Audiobasierten Überprüfung wechseln
frames = browser.find_element(By.XPATH, "/html/body/div[2]/div[4]").find_elements(By.TAG_NAME, "iframe")
browser.switch_to.frame(frames[0])
time.sleep(random.randint(2, 4))
browser.find_element(By.ID, "recaptcha-audio-button").click()
browser.switch_to.default_content()

# Abspielbutton auswählen und Audio abspielen
frames = browser.find_elements(By.TAG_NAME, "iframe")
browser.switch_to.frame(frames[-1])
time.sleep(random.randint(2, 4))
(browser.find_element(By.XPATH, "/html/body/div/div/div[3]/div/button")).click()
time.sleep(random.randint(2, 4))

# Audiodatei herunterladen und von mp3 in wav umwandeln
src = browser.find_element(By.ID, "audio-source").get_attribute("src")
urllib.request.urlretrieve(src, data_path + "/audio.mp3")
sound = pydub.AudioSegment.from_mp3(
    data_path + "/audio.mp3"
).export(data_path + "/audio.wav", format="wav")

# Google Audio checker scannen lassen
recognizer = speech_recognition.Recognizer()
google_audio = speech_recognition.AudioFile(
    data_path + "/audio.wav"
)
with google_audio as source:
    audio = recognizer.record(source)
    text = recognizer.recognize_google(audio, language='de-DE')
    print("<Erkannter Text>: {}".format(text))

# Ermittelten Text in das Eingabefeld schreiben und bestätigen
inputfield = browser.find_element(By.ID, "audio-response")
inputfield.send_keys(text.lower())
inputfield.send_keys(Keys.ENTER)
time.sleep(15)
