#!/usr/bin/python3
# -*- coding: utf-8  -*-

# dependency for Selenium
from selenium import webdriver

# Dependency for wait element
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from utils import Utils, bcolors
from datetime import datetime

# Dependancy for other element
from PIL import Image
from detect_images import *
import concurrent.futures
import matplotlib.pyplot as plt
from collections import Counter
import numpy as np
from database.db import Bank
from peewee import *
import re

import yaml
import platform
import time
import locale

# Read YML file
with open("config.yml", 'r') as stream:
    Configuration = yaml.safe_load(stream)

class Banking():
    '''
    Initalisation account on caisse d'epargne and define the broswer
    option for navigate on the page.
    '''
    def __init__(self, username, password, hidden_position):
        self.username = username
        self.password = password
        self.pad_name = "padsecret"
        self.hidden_position = hidden_position
        self.url_checking = "https://www.net751.caisse-epargne.fr/Portail.aspx"
        self.compte_courant = 0.00
        self.compte_epargne = 0.00
        self.compte_courant_format = ""
        self.compte_epargne_format = ""
        self.category = {}

        ''' New Row in bank '''
        # try connect database registry one row
        NewBank = Bank()
        NewBank.description = "test"
        NewBank.date = ""
        NewBank.price = 0
        try:
            NewBank.save()
        except DatabaseError:
            print("Error database is corrupted please verify passphrase " \
                  "or delete database in database/bank.db")
            exit()


        ''' DELETE BANKING '''
        #query = Bank.delete().where(Bank.id >= 0)
        #query.execute()

        ''' SELECT BANKING '''
        BankQuery = Bank.select()

        for BankQ in BankQuery:
            print(BankQ.id, BankQ.description, BankQ.date)

        locale.setlocale(locale.LC_ALL, "fr_FR.UTF-8")

        ___author___ = "vBlackOut"
        ___version___ = "0.0.1 (Beta)"

        print('''{0}
 _______________________________________________
⎢*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*⎢
|{2}  |     |   __|  | __  |     |_   _|   {1}|
|{1}  |   --|   __|  | __ -|  |  | | |     {2}|
|{2}  |_____|_____|  |_____|_____| |_|     {1}|
⎢-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-*-⎢
 ⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺
{3}
Author: {4}{5}{6}
Version: {7}{8}{9}
Platform: {10}{11} ({12}){13}\n'''.format(bcolors.OKBLUE,
                                     ".*. ",
                                     " .*.",
                                     bcolors.ENDC,
                                     bcolors.WARNING,
                                     ___author___,
                                     bcolors.ENDC,
                                     bcolors.WARNING,
                                     ___version___,
                                     bcolors.ENDC,
                                     bcolors.WARNING,
                                     platform.system(),
                                     platform.machine(),
                                     bcolors.ENDC))

    '''
    it's used for define broswer selenium and Profile option
    '''
    def navigateur(self):
        print("{} {} {}".format(bcolors.OKGREEN,
                                "Connection à CE (Caisse D'epargne)",
                                bcolors.ENDC))

        url = "https://www.caisse-epargne.fr/"

        options = Options()
        #options.add_argument("--headless")
        navigateur = webdriver.Firefox(options=options)
        navigateur.set_window_size(1200, 800)
        navigateur.get(url)
        return navigateur

    def login(self):
        self.navigateur = self.navigateur()
        self.ut = Utils(self.navigateur)

        self.ut.search_element_click("popup-click",
                                     "//a[@class='bouton-croix close_warning']")
        time.sleep(0.5)

        self.ut.search_element_click("main-login-button",
                                     "//p[@class='account-link']/a")
        time.sleep(0.5)

        self.ut.set_text_input("ID-login", self.username,
                               "//input[@id='idClient']")

        self.ut.search_element_click("button-valider",
                                     "//button[@class='cta']")

        list_padbutton = self.ut.analysepad(self.pad_name,
                                           "//button[@class='code-btns_button']")
        # print(list_padbutton)
        number_element = len(list_padbutton)-4
        # print(number_element)

        self.navigateur.save_screenshot('images/screenshot.png')
        dictelement = {}
        for i in range(0, number_element):
            # print(list_padbutton["{}-{}".format(self.pad_name, i)].get_attribute("id"))
            location = list_padbutton["{}-{}".format(self.pad_name, i)].location
            size = list_padbutton["{}-{}".format(self.pad_name, i)].size

            im = Image.open('images/screenshot.png')
            left = location['x']
            top = location['y']
            right = location['x'] + size['width']
            bottom = location['y'] + size['height']
            im = im.crop((left, top, right, bottom)) # defines crop points
            # saves new cropped image
            im.save('images/Downloads/cel_'+str(i)+'.png')
            dictelement[i] = list_padbutton["{}-{}".format(self.pad_name, i)]

        listes = [(x, y) for x in range(0, 15) for y in range(-1, 10)]

        dictpad = {}

        time.sleep(1)

        with concurrent.futures.ThreadPoolExecutor(max_workers=13) as executor:
            for i, a in listes:
                lineexec = executor.submit(calcule_image,
                                           'cel_'+str(i)+'.png', a,
                                           number_detect_firefox)

                if lineexec.result() == 1.0:
                    #print(lineexec.result())
                    #print([a, i])
                    dictpad[a] = [i, dictelement[i]]

        time.sleep(2)
        size_pad = len(dictpad)
        print("Success load pad {} buttons".format(size_pad))

        password = self.password
        for number in list(str(password)):
            #print(dictpad[int(number)][0])
            dictpad[int(number)][1].click()
            if self.hidden_position:
                print("{}click on pad number{} *{}".format(bcolors.OKBLUE,
                                                           bcolors.OKGREEN,
                                                           bcolors.ENDC))
            else:
                print("{}click on pad number{} {}{}".format(
                                                     bcolors.OKBLUE,
                                                     bcolors.OKGREEN,
                                                     dictpad[int(number)][0],
                                                     bcolors.ENDC))

        self.ut.search_element_click("click-login-button",
                                     "//button[@class='cta confirm']")
        time.sleep(3)
        if self.navigateur.current_url == self.url_checking:
            print("Success login")

    def getMoneyWithDepot(self, depot, methode, output):

        table_compte = self.ut.search_all_elements("compte",
                                                   "//table[@class='accompte']")
        if methode == "compte courant":
            print(table_compte["compte-0"].text)


        if methode == "mon epargne":
            print(table_compte["compte-1"]
                 .text.replace("Mon épargne disponible", ""))

        if methode == "all":
          liste = re.findall('[-+]?([0-9]*\,[0-9]+|[0-9]+)',
                             table_compte["compte-0"].text)
          liste.pop(0)

          self.compte_courant = float("".join(liste).replace(",", "."))
          self.compte_courant_format = locale.format_string("%0.2f",
                                                            self.compte_courant,
                                                            True)
          if output:
              print("\nVotre compte courant\n{} €"
                    .format(self.compte_courant_format))

          liste = re.findall('[-+]?([0-9]*\,[0-9]+|[0-9]+)',
                             table_compte["compte-1"].text)

          liste.pop(0)
          self.compte_epargne = float("".join(liste).replace(",", "."))
          self.compte_epargne_format = locale.format_string("%0.2f",
                                                            self.compte_epargne,
                                                            True)
          if output:
              print("\nVotre compte epargne\n{} €"
                    .format(self.compte_epargne_format))

          return { "compte_courant":self.compte_courant_format,
                   "compte_epargne":self.compte_epargne_format }

        return None

    def GetHistory(self, methode):

        table_compte = self.ut.search_all_elements("compte",
                                                   "//table[@class='accompte']")
        if methode == "compte courant":
            table_compte["compte-0"].click()

        if methode == "mon epargne":
            table_compte["compte-1"].click()


        #print(history_compte)
        history_log = []
        forloop = True
        while forloop == True:

            history_compte = self.ut.search_all_elements("compte",
                                                    "//tr[@class='rowClick']")
            for history in history_compte:
                if "compte" in history:
                    history_log.append(history_compte[history].text)

            SCROLL_PAUSE_TIME = 0.5

            # Get scroll height
            last_height = self.navigateur.execute_script("return document." \
                                                         "body.scrollHeight")

            while True:
                # Scroll down to bottom
                self.navigateur.execute_script("window.scrollTo(0, 614);")

                # Wait to load page
                time.sleep(SCROLL_PAUSE_TIME)

                # Calculate new scroll height and compare with last scroll height
                new_height = self.navigateur.execute_script("return 614;")
                if new_height == last_height:
                    break
                last_height = new_height

            time.sleep(2)
            page_suivant = self.ut.search_element_click("click_page_suivant",
                                                        "//a[@class='next']")
            if page_suivant == "Error element not found":
                break

            time.sleep(1)

            regex = r'\d+/\d+/\d+|(?<=).+(?=[+-])|[+-]' \
                     ' \d+(?:\,\d+)|[+-] \d+ \d+(?:\,\d+)?'

            for i, history in enumerate(history_log):
                date_montant, description, debit = re.findall(regex, history)
                debit = float(debit.replace(' ','').replace(",", "."))

                self.categoryDescription(date_montant, description, debit, i)

        return self.category


    def categoryDescription(self, date_montant, description, debit, loop):
        group0 = "{}/{}".format(date_montant.split("/")[1],
                                date_montant.split("/")[2])

        group1 = "{}".format(description.split(' ')[1])

        if "Fact" in description:
            group2 = "{} {}".format(description.split(' ')[2],
                                    description.split(' ')[3])
            try:
                if "Fact" in description.split(' ')[4]:
                    group3 = "{} {}_{}".format(description.split(' ')[4],
                                              description.split(' ')[5], loop)
                else:
                    group3 = "{} {}".format(description.split(' ')[4], loop)

            except:
                group3 = None

        else:
            try:
                group2 = "{} {}".format(description.split(' ')[2],
                                        description.split(' ')[3],
                                        description.split(' ')[4])
            except:
                group2 = "{} {}".format(description.split(' ')[2],
                                        description.split(' ')[3])
            group3 = None

        if group0 not in self.category:
            self.category[group0] = {}

        if group1 not in self.category[group0]:
            self.category[group0][group1] = {}

        if group2 not in self.category[group0][group1]:
            self.category[group0][group1][group2] = {}

        if group3 not in self.category[group0][group1][group2] and group3 is not None:
            self.category[group0][group1][group2][group3] = {}

        if group3 is not None:
            self.category[group0][group1][group2][group3] = {'price': debit}
        else:
            self.category[group0][group1][group2] = {'price': debit}

    def getAllGroup(self, date):
        list_group = []
        for keygroup, group in self.category.items():
            if date == keygroup:
                for subkeygroup, subgroup in group.items():
                    for subsubkeygroup, subsubgroup in subgroup.items():
                        list_group.append(subsubkeygroup)
        return list_group

    def calculeallwithgroup(self, search_group, date, transaction="-"):
        totalprice = 0.00

        for keygroup, group in self.category.items():
            if date == keygroup:
                for subkeygroup, subgroup in group.items():
                    for subsubkeygroup, subsubgroup in subgroup.items():
                        if search_group == subsubkeygroup:
                            try:
                                for keyfact, fact in subsubgroup.items():
                                    if transaction == "-":
                                        if fact["price"] < 0.00:
                                            totalprice += fact["price"]
                                    if transaction == "+":
                                        if fact["price"] > 0.00:
                                            totalprice += fact["price"]

                            except:
                                if transaction == "-":
                                    if subsubgroup["price"] < 0.00:
                                        totalprice += subsubgroup["price"]
                                if transaction == "+":
                                    if subsubgroup["price"] > 0.00:
                                        totalprice += subsubgroup["price"]
        return totalprice

    def fixOverLappingText(self, text):

        # if undetected overlaps reduce sigFigures to 1
        sigFigures = 2
        positions = [(round(item.get_position()[1],
                            sigFigures), item) for item in text]

        overLapping = Counter((item[0] for item in positions))
        overLapping = [key for key, value in overLapping.items() if value >= 2]

        for key in overLapping:
            textObjects = [text for position, text in positions if position == key]

            if textObjects:

                # If bigger font size scale will need increasing
                scale = 0.05

                spacings = np.linspace(0,scale*len(textObjects),len(textObjects))

                for shift, textObject in zip(spacings,textObjects):
                    textObject.set_y(key + shift)

    def showGraph(self):

        '''labels = self.getAllGroup("05/2019")'''

        '''sizes = []'''
        '''explode = []'''

        '''for label in labels:
            sizes.append(abs(Drivers.calculeallwithgroup(label, "05/2019")))
            explode.append(1)'''

        # Pie chart, where the slices will be ordered and plotted counter-clockwise:
        #labels = 'Frogs', 'Hogs', 'Dogs', 'Logs'
        #sizes = [15.5, 30.5, 45.5, 10.5]
        #explode = (0, 0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

        '''fig1, ax1 = plt.subplots()
        text = ax1.pie(sizes, explode=explode, labels=labels, autopct='%d',
                       shadow=True, startangle=100)[1]
        ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        self.fixOverLappingText(text)'''

        labels = self.getAllGroup("05/2019")
        Gender=['+','-']

        pos = np.arange(len(labels))
        bar_width = 0.35

        sizes_neg = []
        for label in labels:
            sizes_neg.append(abs(int(Drivers
                                     .calculeallwithgroup(label,
                                                          Configuration["date_search"],
                                                          transaction="-"))))

        sizes_plus = []
        for label in labels:
            sizes_plus.append(abs(int(Drivers
                                     .calculeallwithgroup(label,
                                                         Configuration["date_search"],
                                                         transaction="+"))))

        bar1 = plt.bar(pos,sizes_plus,
                      bar_width,
                      color='blue',
                      edgecolor='black')

        bar2 = plt.bar(pos+bar_width,
                       sizes_neg,bar_width,
                       color='red',
                       edgecolor='black')

        for bar in bar1:
            yval = bar.get_height()
            plt.text(bar.get_x(), yval + .005, yval)

        for bar in bar2:
            yval = bar.get_height()
            plt.text(bar.get_x(), yval + .005, yval)

        plt.xticks(pos, labels, rotation='vertical')
        plt.xlabel('City', fontsize=10, )
        plt.ylabel('Happiness_Index', fontsize=10)
        plt.title('Group Barchart - Happiness index across cities By Gender',
                  fontsize=18)
        plt.legend(Gender, loc=2)
        plt.show()

if __name__ == '__main__':
    startTime = datetime.now()
    Drivers = Banking(username=Configuration["username"],
                      password=Configuration["password"],
                      hidden_position=Configuration['hidden_position'])
    Drivers.login()
    Drivers.getMoneyWithDepot("", methode="all", output=False)
    Drivers.GetHistory(methode="compte courant")
    print(Drivers.calculeallwithgroup("Paypal Fact", Configuration["date_search"]))
    Drivers.showGraph()

    print("\nTotal Time: {}".format(datetime.now() - startTime))
