#!/usr/bin/env python3
#
#    LEGO Mindstorms Editions Pieces Comparison
#    Copyright (C) 2015-2017  Peter Bittner <django@bittner.it>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os.path

from selenium import webdriver

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from selenium.webdriver import Chrome, Firefox, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep


class ReplacementPart:
    """
    Add a list of LEGO parts and their quantity to the 'Shopping Bag' of LEGO's
    customer service platform.  A browser window will be opened, you'll be able
    to watch the browser do what you would normally do by hand, and execution
    will stop after all pieces have been added, so you can review and finalize
    your order.  (This is just to help you save time on entering 60+ pieces
    manually.  Nothing is ordered on your behalf!)
    """

    def __init__(self, browser_name=None, shop=None):

        self.browser_name = browser_name
        self.lego_shop = shop
        self.username = ""
        self.password = ""

        self.datafiles = {}

        self.partno_status = {
            'found': 1,
            'not_found': 2,
            'electric': 3,
        }

    def __reset_stats_counters(self):
        """
        set statistics counters to zero
        """

        self.part_stats_counter = {
              'total_elements': 0,
              'found': 0,
              'duplicate_part': 0,
              'not_in_set': 0,
              'out_of_stock': 0,
              'electric_part': 0
             }

    def __load_new_element_ids(self):
        """
        load list of new element IDs
        """

        self.newelementid_map = {}

        try:
            datafile = self.datafiles['newelementid']
            if not os.path.isfile(datafile):
                print("{} is not a file".format(datafile))
                return
        except KeyError:
            print("Datafile for New Element ID not set")
            return

        with open(datafile) as f:
            data_lines = f.readlines()[1:]
            for line in data_lines:
                line = line.strip()
                eid_origin, eid_chain, eid_comment = line.split(';')
                # list:  convert each new element id of eid_chain as number
                self.newelementid_map[int(eid_origin)] = {
                    'list': list(map(int, eid_chain.split(","))),
                    'comment': eid_comment
                }

    def __load_electric_parts(self):
        """
        load list of electric part ID
        """

        self.electricpart_map = {}
        try:
            datafile = self.datafiles['electricparts']
            if not os.path.isfile(datafile):
                print("{} is not a file".format(datafile))
                return
        except KeyError:
            print("Datafile for Electric Parts not set")
            return

        with open(datafile) as f:
            data_lines = f.readlines()[1:]
            for line in data_lines:
                partno, legoid, legoshop_set = line.split('\t')
                self.electricpart_map[int(partno)] = int(legoshop_set)

    def __is_electric_part(self, wanted_part_no, print_set_link=False):
        """
        Detect if part is in EV3 Electric parts array, print link to standalone Set if wanted

        return boolean
        """

        wanted_part_no = int(wanted_part_no)

        exit_code = False

        if wanted_part_no in self.electricpart_map.keys():
            exit_code = True

            if print_set_link:
                lego_shop_set = self.electricpart_map[wanted_part_no]
                print("#{partno}: standalone set URL "
                      "https://shop.lego.com/en-US/search/{legoshop_set}"
                      .format(partno=wanted_part_no,
                              legoshop_set=lego_shop_set))

        return exit_code

    def __init_browser(self, browser, shop):
        """
        open browser with LEGO shop URL
        """

        shop_url = "https://wwwsecure.us.lego.com/{shop}/service/replacementparts/sale".format(
                    shop=shop)
        # The querystring will fix the age survey.
        # simulate click to the third button ('Buy Bricks')
        shop_url += "?chosenFlow=3"

        print("Using Selenium version: ", webdriver.__version__)
        print("Browser wanted URL: {url}".format(url=shop_url))

        # detect browser choice #
        if browser == 'chrome':
            opts = ChromeOptions()
            # With selenium version above this one, chrome is closed
            # at the end without the "quit()" method!
            # Here is a fix to detach Chrome from python.
            if webdriver.__version__ > '2.48.0':
                print("Apply experimental detach option for Chrome")
                opts.add_experimental_option("detach", True)

            self.browser = Chrome(chrome_options=opts)
        else:
            self.browser = Firefox()

        print("Browser capabilities")
        print(self.browser.capabilities)

        # Selenium can't find some elements otherwise
        self.browser.maximize_window()

        self.browser.get(shop_url)
        print("Browser current URL: {url}".format(url=self.browser.current_url))

        # will wait to 5 sec for and ExpectedCondition success,
        # otherwise exception TimeoutException
        self.wait = WebDriverWait(self.browser, 5)

    def __process_survey(self):
        """
        validate Lego's survey form
        """

        print("Sometimes they ask you to fill in a survey.")

        try:
            survey_layer = self.browser.find_element_by_id('ipeL104230')
            survey_layer.send_keys(Keys.ESCAPE)
        except NoSuchElementException:
            print("We're lucky, no survey on the LEGO shop today!")

        try:
            print("They want to know how old we are.")
            age_field = self.wait.until(EC.element_to_be_clickable(
                (By.NAME, 'rpAgeAndCountryAgeField')))
            age_field.send_keys('55')
            age_field.send_keys(Keys.RETURN)

            # wait for age_field's DOM element to be removed
            self.wait.until(EC.staleness_of(age_field))
        except TimeoutException:
            print("Something's wrong with the survey")

    def __process_login(self):
        """
        Manage LEGO Shop login form

        return boolean
        """

        # login stuff #
        if self.username and self.password:

            print("Let's log in with LEGO ID {user}.".format(user=self.username))
            login_link = self.wait.until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, ".legoid .links > a[data-uitest='login-link']")))
            login_link.click()

            self.browser.switch_to.frame('legoid-iframe')

            user_input = self.wait.until(EC.element_to_be_clickable(
                (By.ID, 'fieldUsername')))
            user_input.click()
            user_input.send_keys(self.username)

            passwd_input = self.wait.until(EC.element_to_be_clickable(
                (By.ID, 'fieldPassword')))
            passwd_input.click()
            passwd_input.send_keys(self.password)

            login_button = self.browser.find_element_by_id('buttonSubmitLogin')
            login_button.click()

            self.browser.switch_to.default_content()

            # ensure the user/password are good
            try:
                self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR,
                        ".legoid .links > a[data-uitest='logout-link']")
                ))

                print("login success!")
                return True
            except TimeoutException:
                print("login failed!")
                # close the browser and stop here
                self.browser.quit()
                return False
        else:
            print("credentials are not defined")
            return True

    def __process_select_lego_set(self, lego_set):
        """
        Manage Lego's Set choice
        """

        print("We need to tell them which set we want to buy parts from: {lego_set}".format(
            lego_set=lego_set))
        setno_field = self.wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '.product-search input[ng-model=productNumber]'))
        )

        setno_field.send_keys(lego_set)
        setno_field.send_keys(Keys.RETURN)
        sleep(.3)  # seconds

    def __process_partno(self, original_part_no):
        """
        Ensure a part is found, or test with newer ID
        """

        return_code = self.partno_status['not_found']

        new_part_no_list = []
        original_part_no = int(original_part_no)
        if original_part_no in self.newelementid_map.keys():
            new_part_no_list = self.newelementid_map[original_part_no]['list']

        partno_list = list([original_part_no] + new_part_no_list)

        for idx, part_no in enumerate(partno_list):

            # idx 0 has the original part_no
            if idx > 0:
                print("\t>> Trying to replace with #{pn} ".format(pn=part_no), end='')

            element_field = self.wait.until(
                              EC.element_to_be_clickable((By.ID, 'element-filter')))
            element_field.clear()
            element_field.send_keys(part_no)
            element_field.send_keys(Keys.RETURN)
            sleep(.3)  # seconds

            try:
                # tip: count results to ensure the wanted part_no return nothing or one
                results_count = len(
                    self.browser.find_elements_by_css_selector('.element-details + button'))

                if results_count == 0:

                    if self.__is_electric_part(part_no):
                        return_code = self.partno_status['electric']
                        break

                    if idx == 0 and len(partno_list) > 1:
                        # we're on the original part, and we've a list of new Element ID
                        print("Not Found, but has a chain of other Element ID:")
                        # a comment about the mapping
                        comment = self.newelementid_map[original_part_no]['comment']
                        print("\tcomment: {}".format(comment))
                    else:
                        print("Not Found!")

                elif results_count == 1:
                    return_code = self.partno_status['found']
                    break

                else:
                    print("Too many results with that part_no, bad number!")

            except NoSuchElementException:
                print("Selenium error: CSS element not found")

        return part_no, return_code

    def __process_statistics(self):
        """
        Print statistics about ordered parts
        """

        print()
        print("We're done. You can finalize your order now. Thanks for watching!")
        print()
        print("Statistics:")
        print("- {s} Wanted elements".format(s=self.part_stats_counter['total_elements']))
        print("- {s} Elements found".format(s=self.part_stats_counter['found']))
        print("- {s} Elements ignored (duplicated)"
              .format(s=self.part_stats_counter['duplicate_part']))
        print("- {s} Elements not in set".format(s=self.part_stats_counter['not_in_set']))
        print("- {s} Elements out of stock".format(s=self.part_stats_counter['out_of_stock']))
        print("- {s} Elements of type 'Electric part'"
              .format(s=self.part_stats_counter['electric_part']))

        if self.part_stats_counter['out_of_stock'] > 0:
            print("\n!! Take care about out of stock elements")
        if self.part_stats_counter['not_in_set'] > 0:
            print("\n!! Take care about not in set elements")

        if self.part_stats_counter['electric_part'] > 0:
            print()
            print("Electric parts you can add to your bag once you've added your order:")

            for item in self.electric_part_list:
                self.__is_electric_part(item, True)

    def set_credentials(self, username, password):
        """
        set username/password for Lego shop Login
        """
        self.username = username
        self.password = password

    def set_new_element_id_datafile(self, datafile):
        """
        set path to datafile for New Element ID mapping
        """
        self.datafiles['newelementid'] = datafile

    def set_electric_part_datafile(self, datafile):
        """
        set path to datafile for Electric part ID mapping
        """
        self.datafiles['electricparts'] = datafile

    def process(self, lego_set, order_list):
        """
        Main process to order LEGO's set parts
        """

        self.__load_new_element_ids()
        self.__load_electric_parts()

        self.__init_browser(self.browser_name, self.lego_shop)
        self.__process_survey()

        if not self.__process_login():
            return

        self.__process_select_lego_set(lego_set)

        print("Let's scroll the page down a bit, so we can see things better.")
        self.browser.execute_script("window.scroll(0, 750);")

        self.electric_part_list = []

        order_list = order_list.split(',')

        self.__reset_stats_counters()
        self.part_stats_counter['total_elements'] = len(order_list)

        print("That's gonna be crazy: {count} elements to order! Let's rock.".format(
            count=self.part_stats_counter['total_elements']))
        print()

        added_part = {}
        counter = 0

        for brick in order_list:
            part_no, quantity = brick.split(':')
            part_no = int(part_no)
            original_part_no = part_no

            counter += 1

            print("- [{counter}/{total_elements}] {qty}x #{pn} ".format(
                qty=quantity,
                pn=part_no,
                counter=counter,
                total_elements=self.part_stats_counter['total_elements']), end='')

            # never add the same part twice,
            # otherwise the quantity will be set to the previous part
            if part_no in added_part.keys():
                self.part_stats_counter['duplicate_part'] += 1
                print("IGNORE: Already added!".format(pn=part_no))
                if part_no != added_part[part_no]:
                    print("\t- #{}'s updated Element ID ".format(added_part[part_no]))
                continue

            elif part_no in self.electric_part_list:
                # an electric part is managed out of added part
                self.part_stats_counter['duplicate_part'] += 1
                print("IGNORE: Electric part already mentioned")
                continue

            # part_no may be overrided if new ID found
            part_no, partno_result = self.__process_partno(original_part_no)

            if partno_result == self.partno_status['found']:
                print("Found!")
                added_part[part_no] = original_part_no

                add_button = self.browser.find_element_by_css_selector('.element-details + button')

                if add_button.is_enabled():
                    add_button.click()
                    sleep(.2)  # seconds
                    self.part_stats_counter['found'] += 1
                else:
                    self.part_stats_counter['out_of_stock'] += 1
                    print("\t!! NOTE: item out of stock.")

            elif partno_result == self.partno_status['electric']:
                print("Not Found, but electric part:")
                print("\t!! The LEGO Group provides electric part out of set #{set}, "
                      .format(set=lego_set), end='')
                print("see note at the end.")

                self.electric_part_list.append(part_no)
                self.part_stats_counter['electric_part'] += 1
            else:
                print("\t!! OOOPS! No LEGO part with that number found in set #{set}. :-(".format(
                      set=lego_set))
                self.part_stats_counter['not_in_set'] += 1
                continue

            # set the value for item's quantity drop-down menu
            amount_select = self.browser.find_elements_by_css_selector('.bag-item select')[-1]
            Select(amount_select).select_by_visible_text(quantity)

            # ensure the value is correct
            selected = Select(amount_select).first_selected_option

            if quantity != selected.text:
                print("\t!! WARNING: Could not select desired quantity. {} != {}".format(
                    quantity, selected.text))

        self.browser.execute_script("window.scroll(0, 0);")

        self.__process_statistics()
