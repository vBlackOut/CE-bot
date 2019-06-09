# Dependency for wait element
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException
import re
import time

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNYELLOW = '\033[1;33m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Utils():

    def __init__(self, navigateur):
        self.navigateur = navigateur

    def cleanhtmls(self, raw_html):
        raw_html = raw_html.replace('<br>', ' ')
        raw_html = re.sub('<[^<]+?>', '', raw_html)
        raw_html = re.sub('&nbsp;', ' ', raw_html)
        raw_html = re.sub('&amp;', '&', raw_html)
        raw_html = raw_html.replace('\t', ' ')
        raw_html = raw_html.replace('\n', ' ')
        return raw_html

    '''
    Cet fonction définie la navigation dans la navbar en haut du site
    @search_navbar (str) definie le premier menu du navbar
    @search_element (str) definie le sous menu du navbar
    @getmetric (bool) retour ou pas les métriques de la page.

    retour un dictionnaire des éléments rechercher. (avec ou sans métrique)
    '''
    def search_element_click(self, name, search_element, getmetric=False):
        data = {
            "elements": {
              "{}".format(name): {
                  "search_by": By.XPATH,
                  "element": search_element,
                  "action": "click"
               }
            }
        }

        element = self.retry(define=data,
                            objects="json_search",
                            message="Click on element [{0}{1}{3}{4}] \
[{0}{2}{3}{4}]".format(bcolors.OKGREEN,
                                                   name,
                                                   search_element,
                                                   bcolors.ENDC,
                                                   bcolors.OKBLUE),
                            message_fail="Timeout check element recheck...",)
        if getmetric is True:
            print(navbar["perform_backendfull"])
            print(navbar["perform_frontendfull"])

        return element


    '''
    Cet fonction définie la navigation dans la navbar en haut du site
    @search_navbar (str) definie le premier menu du navbar
    @search_element (str) definie le sous menu du navbar
    @getmetric (bool) retour ou pas les métriques de la page.

    retour un dictionnaire des éléments rechercher. (avec ou sans métrique)
    '''

    def search_element(self, name, search_element, getmetric=False):
        data = {
            "elements": {
              "{}".format(name): {
                  "search_by": By.XPATH,
                  "element": search_element,
                  "action": None
               }
            }
        }

        element = self.retry(define=data,
                            objects="json_search",
                            message="Click on element [{0}{1}{3}{4}] \
                            [{0}{2}{3}{4}]".format(bcolors.OKGREEN,
                                                   name,
                                                   search_element,
                                                   bcolors.ENDC,
                                                   bcolors.OKBLUE),
                            message_fail="Timeout check element recheck...",)
        if getmetric is True:
            print(navbar["perform_backendfull"])
            print(navbar["perform_frontendfull"])

        return element

    def search_all_elements(self, name, search_all_elements, getmetric=False):
        data = {
            "all_elements": {
              "{}".format(name): {
                  "search_by": By.XPATH,
                  "element": search_all_elements,
               }
            }
        }

        element = self.retry(define=data,
                            objects="json_search",
                            message="Click on element [{0}{1}{3}{4}] \
                            [{0}{2}{3}{4}]".format(bcolors.OKGREEN,
                                                   name,
                                                   search_all_elements,
                                                   bcolors.ENDC,
                                                   bcolors.OKBLUE),
                            message_fail="Timeout check element recheck...",)
        if getmetric is True:
            print(navbar["perform_backendfull"])
            print(navbar["perform_frontendfull"])

        return element



    def search_innerhtml_click(self, name, search_element, getmetric=False):
        data = {
            "elements": {
              "{}".format(name): {
                  "search_by": "innerHTML",
                  "element": search_element,
                  "action": "click"
              }
            }
        }

        elment = self.retry(define=data,
                            objects="json_search",
                            message="Click on element [{0}{1}{3}{4}] \
[{0}{2}{3}{4}]".format(bcolors.OKGREEN,
                                                   name,
                                                   search_element,
                                                   bcolors.ENDC,
                                                   bcolors.OKBLUE),
                            message_fail="Timeout check element recheck...",)
        if getmetric is True:
            print(navbar["perform_backendfull"])
            print(navbar["perform_frontendfull"])
        return element


    def set_text_input(self, name, value, search_element, getmetric=False):
        data = {
            "inputs": {
                "{}".format(name): {
                  "search_by": By.XPATH,
                  "element": search_element,
                  "enter_value": value
                }
            }
        }

        element = self.retry(define=data,
                            objects="json_search",
                            message="set value [{0}{1}{3}{4}] \
[{0}{2}{3}{4}]".format(bcolors.OKGREEN,
                                                   name,
                                                   search_element,
                                                   bcolors.ENDC,
                                                   bcolors.OKBLUE),
                            message_fail="Timeout check element recheck...",)
        if getmetric is True:
            print(navbar["perform_backendfull"])
            print(navbar["perform_frontendfull"])

        return element


    def analysepad(self, name, search_element):

        data = {
            "all_elements": {
                "{}".format(name): {
                  "search_by": By.XPATH,
                  "element": search_element,
                }
            }
        }

        element = self.retry(define=data,
                            objects="json_search",
                            message="analyse pad [{0}{1}{3}{4}] \
[{0}{2}{3}{4}]".format(bcolors.OKGREEN,
                                                   name,
                                                   search_element,
                                                   bcolors.ENDC,
                                                   bcolors.OKBLUE),
                            message_fail="Timeout check element recheck...",)

        return element



    '''
    Cet fonction est utiliser partout pour rechercher un element ou
    faire une action sur la page.
    @kwargs

          - message, (str) definie le message du chargement de l'element.
          - color, (str) definie la couleur dans la class.
            bcolors, pour le message.
          - objects, (str) definie le type de recherche par defaut json_search
            dans le type de recherche json_search nous avons
            4 types de recherches différentes.
          - define, contient les données sous forme de dictionnaire.

             - inputs, définie les input dans un champs de formulaire
               - search_by, définie la methode de recherche, définie par By.
               - enter_value, (str) définie le message
                              qui sera rentré automatiquement
               - element, (str) donnée le chemin d'accés DOM vers l'élément.

             - button, définie les buttons
               - search_by, définie la methode de recherche, définie par By.
               - action, (str) définie ce que dois faire cet élément.
                 - click, cliqué sur l'element.
               - element, (str) donnée le chemin d'accés DOM vers l'élément.

             - all_elements
               - search_by, définie la methode de recherche, définie par By.
               - element, (str) donnée le chemin d'accés DOM vers l'élément.
               - navbar, (str) définie l'element à rechercher
                         dans le module navbar.
                  - action, (str) définie ce que dois faire cet élément.
                    - click, cliqué sur l'element.

             - elements
               - search_by, (method/str) définie la methode de recherche,
                            définie par By. ou par innerHTML pour rechercher
                            directement un element dans l'attribue HTML
                            ( element deviendra l'element html à rechercher )
               - element, (str) donnée le chemin d'accés DOM vers l'élément.
               - action, (str) définie ce que dois faire cet élément.
                 - click, cliqué sur l'element.

    retour un dictionnaire des éléments rechercher. (metrique inclus)
    '''
    def retry(self, **kwargs):

        navigationStart = self.navigateur.execute_script("return window.performance.timing.navigationStart")
        responseStart = self.navigateur.execute_script("return window.performance.timing.responseStart")

        try:
            kwargs["timeout"]
        except KeyError as e:
            if "'timeout'" == str(e):
                kwargs["timeout"] = 10

        try:
            kwargs["timeout_fail"]
        except KeyError as e:
            if "'timeout_fail'" == str(e):
                kwargs["timeout_fail"] = 10

        try:
            kwargs["retry"]
        except KeyError as e:
            if str(e) == "'retry'":
                kwargs["retry"] = 3

        try:
            kwargs["message"]
        except KeyError as e:
            if str(e) == "'message'":
                kwargs["message"] = ""

        try:
            kwargs["color"]
        except KeyError as e:
            if str(e) == "'color'":
                kwargs["color"] = bcolors.OKBLUE

        if kwargs["objects"] == "json_search":
            print(bcolors.OKBLUE + kwargs["message"] + bcolors.ENDC)
            element_dict = {}
            for key, value in kwargs["define"].items():
                if key == "inputs":
                    for key, value in value.items():
                        if value["search_by"]:
                            method = value["search_by"]

                        if value["enter_value"]:
                            insert_value = value["enter_value"]

                        if value["element"]:
                            element = value["element"]

                        inputs = WebDriverWait(self.navigateur, kwargs["timeout"]).until(EC.presence_of_element_located((method, element)))
                        element_dict[key] = inputs
                        inputs.send_keys(insert_value)

                if key == "button":
                    for key, value in value.items():
                        if value["search_by"]:
                            method = value["search_by"]

                        if value["element"]:
                            element = value["element"]

                        button = WebDriverWait(self.navigateur, kwargs["timeout"]).until(EC.presence_of_element_located((method, element)))
                        element_dict[key] = button
                        if value["action"] == "click":
                            button.click()

                if key == "elements":
                    for key, value in value.items():
                        if value["search_by"]:
                            method = value["search_by"]
                            if value["search_by"] == "innerHTML":
                                method = By.XPATH
                                element = "//*[text()[contains(., '{}')]]".format(value["element"])

                        if value["element"] and value["search_by"] is not "innerHTML":
                            element = value["element"]
                        try:
                            button = WebDriverWait(self.navigateur, kwargs["timeout"]).until(EC.presence_of_element_located((method, element)))
                        except TimeoutException:
                            for i in range(0, kwargs["retry"]):
                                print("Error retry... {}".format(i))
                                try:
                                    button = WebDriverWait(self.navigateur, kwargs["timeout"]).until(EC.presence_of_element_located((method, element)))
                                    if button:
                                        break
                                except TimeoutException:
                                    pass
                            try:
                                if button:
                                    pass
                            except UnboundLocalError:
                                return "Error element not found"

                        element_dict[key] = button
                        if value["action"] == "click":
                            actions = ActionChains(self.navigateur)
                            actions.move_to_element(button).perform()
                            button.click()

                if key == "all_elements":
                    for key, value in value.items():
                        if value["search_by"]:
                            method = value["search_by"]
                            if value["search_by"] == "innerHTML":
                                method = By.XPATH
                                element = "//*[text()[contains(., '{}')]]".format(value["element"])

                        if value["element"] and value["search_by"] is not "innerHTML":
                            element = value["element"]

                        elements = WebDriverWait(self.navigateur, kwargs["timeout"]).until(EC.presence_of_all_elements_located((method, element)))
                        try:
                            if value["navbar"]:
                                for navbar_name in elements:
                                    if value["navbar"] in navbar_name.get_attribute("innerHTML"):
                                        element_dict[key] = navbar_name
                                        if value["action"] == "click":
                                            actions = ActionChains(self.navigateur)
                                            actions.move_to_element(navbar_name).perform()
                                            navbar_name.click()
                        except KeyError:
                            for i, elem in enumerate(elements):
                                element_dict["{}-{}".format(key, i)] = elem

            domComplete = self.navigateur.execute_script("return window.performance.timing.domComplete")

            backendPerformance = responseStart - navigationStart
            frontendPerformance = domComplete - responseStart
            element_dict["perform_backendfull"] = "backend {} ms".format(backendPerformance)
            element_dict["perform_frontendfull"] = "frontend {} ms".format(frontendPerformance)
            element_dict["perform_backend"] = "{}".format(backendPerformance)
            element_dict["perform_frontend"] = "{}".format(frontendPerformance)
            return element_dict
