#!/usr/bin/env python3
"""
#
#    LEGO Mindstorms Editions Pieces Comparison
#    Copyright (C) 2015-2018  Peter Bittner <django@bittner.it>
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
"""

import os.path
import sys
import textwrap

from time import sleep
from selenium import webdriver

from selenium.common.exceptions import (
    NoSuchElementException, TimeoutException, WebDriverException
)
from selenium.webdriver import Chrome, Firefox, ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class UpdatedPartMapping:
    """
    Manage list of updated partno
    """

    def __init__(self, datafile=None):
        """
        Load list of new element IDs
        """

        self.map = {}

        try:
            if not os.path.isfile(datafile):
                print("{} is not a file".format(datafile))
                return
        except KeyError:
            print("Datafile for New Element ID not set")
            return

        with open(datafile) as file_handler:
            data_lines = file_handler.readlines()[1:]
            for line in data_lines:
                line = line.strip()
                eid_origin, eid_chain, eid_comment = line.split(';')
                # list:  convert each new element id of eid_chain as number
                self.map[int(eid_origin)] = {
                    'list': list(map(int, eid_chain.split(","))),
                    'comment': eid_comment
                }

    def partno_exists(self, original_part_no):
        """
        Detect if a part has new ID

        return boolean
        """
        original_part_no = int(original_part_no)
        if original_part_no in self.map.keys():
            return True
        return False

    def get_part_list(self, original_part_no):
        """
        Get list of updated ID(s) for wanted part ID

        return hash
        """

        new_part_no_list = []

        original_part_no = int(original_part_no)

        if self.partno_exists(original_part_no):
            new_part_no_list = self.map[original_part_no]['list']

        return new_part_no_list

    def get_part_comment(self, original_part_no):
        """
        Get comment about a part ID

        return string
        """

        original_part_no = int(original_part_no)

        if self.partno_exists(original_part_no):
            return self.map[original_part_no]['comment']

        return "<no comment set>"


class MindstormsElectricPart:
    """
    Manage inventory about Mindstorms electric parts
    """

    def __init__(self, datafile):
        """
        Load list of electric part ID
        """

        self.map = {}

        try:
            if not os.path.isfile(datafile):
                print("{} is not a file".format(datafile))
                return
        except KeyError:
            print("Datafile for Electric Parts not set")
            return

        with open(datafile) as file_handler:
            data_lines = file_handler.readlines()[1:]
            for line in data_lines:
                partno, dummy_legoid, legoshop_set = line.split('\t')
                self.map[int(partno)] = int(legoshop_set)

    def partno_exists(self, part_no):
        """
        Detect if part is in EV3 Electric parts array

        return boolean
        """
        part_no = int(part_no)

        if part_no in self.map.keys():
            return True
        return False

    def get_partno_standalone_link(self, part_no):
        """
        Print link to standalone Set
        """

        part_no = int(part_no)

        if self.partno_exists(part_no):
            lego_shop_set = self.map[part_no]
            print("#{part_no}: standalone set URL "
                  "https://shop.lego.com/en-US/search/{legoshop_set}"
                  .format(part_no=part_no,
                          legoshop_set=lego_shop_set))


class LegoShopBase:
    """
    Simple acces to Lego website: manage cookie acceptance + authentication
    """

    def __init__(self, browser_name=None, shop=None):
        self.browser_name = browser_name
        self.lego_shop = shop

        # Lego's credentials
        self.username = ""
        self.password = ""

        # future objects for selenium
        self.browser = None
        self.wait = None

        self.shop_url = ""

    def set_credentials(self, username, password):
        """
        Set username/password for Lego shop Login
        """
        self.username = username
        self.password = password

    def _init_browser(self, browser, url_path=""):
        """
        Open browser with LEGO shop URL (index page if path not set)
        """
        self.shop_url = "https://www.lego.com/%s" % url_path

        self._load_driver(browser)

        # Selenium can't find some elements otherwise
        self.browser.maximize_window()

        self.browser.get(self.shop_url)

        # will wait to 5 sec for and ExpectedCondition success,
        # otherwise exception TimeoutException
        self.wait = WebDriverWait(self.browser, 5)

        self.browser_info()

    def _load_driver(self, browser):
        """
        Loads the browser driver binary handling loading errors
        """
        installers = {
            'chrome': {
                'linux': 'sudo apt-get install chromium-chromedriver',
                'linux2': 'sudo apt-get install chromium-chromedriver',
                'darwin': 'brew install chromedriver',
                # for Windows add 'win32' and 'cygwin'
            },
            'firefox': {
                'linux': 'sudo apt-get install firefox-geckodriver',
                'linux2': 'sudo apt-get install firefox-geckodriver',
                'darwin': 'brew install geckodriver',
                # for Windows add 'win32' and 'cygwin'
            },
        }
        try:
            install_instructions = textwrap.dedent("""\
                If you have not installed your Web browser driver yet try:
                %s""" % installers[browser][sys.platform])
        except KeyError:
            install_instructions = textwrap.dedent("""\
                See the README for details:
                https://github.com/bittner/lego-mindstorms-ev3-comparison#requirements
                """).strip()

        if browser == 'chrome':
            # With selenium version above this one, chrome is closed
            # at the end without the "quit()" method!
            # Here is a fix to detach Chrome from python.
            opts = ChromeOptions()
            if webdriver.__version__ > '2.48.0':
                print("* Apply experimental detach option for Chrome")
                opts.add_experimental_option("detach", True)

        try:
            if browser == 'chrome':
                self.browser = Chrome(chrome_options=opts)
            else:
                self.browser = Firefox()
        except WebDriverException as err:
            message = textwrap.dedent("""\
                There was a problem when loading the driver for your Web browser:
                %(exception)s

                %(installer)s""") % dict(
                    exception=err.msg,
                    installer=install_instructions,
                )
            raise SystemExit(message)

    def browser_info(self):
        """
        Print information about browser instance
        """
        print("* Using Selenium version: {}", format(webdriver.__version__))
        print("* Browser capabilities")
        print(self.browser.capabilities)
        print("* Browser wanted URL: {url}".format(url=self.shop_url))
        print("* Browser current URL: {url}".format(url=self.browser.current_url))

    def _process_age_gate(self):
        """
        Continue Passed Age Gate
        """
        print("* Continue Passed Age Gate")
        try:
            self.wait \
                .until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test = 'age-gate-grown-up-cta']")))\
                .click()
        except NoSuchElementException:
            print("!!! Something's wrong with the age gate button")

    def _process_choose_country(self):
        """
        Choose Country
        """
        print("* Choose Country")
        try:
            self.wait \
                .until(EC.visibility_of_element_located((By.XPATH, "//select[@data-cy='choose-country-select']")))

            sleep(.3)

            self.wait \
                .until(EC.element_to_be_clickable((By.XPATH, "//button[@data-cy = 'choose-country-button']")))\
                .click()
        except NoSuchElementException:
            print("!!! Something's wrong with the age gate button")

    def _process_cookies_accept(self):
        """
        Accept Lego's cookies
        """
        print("* Accept Lego's website cookies")
        try:
            self.wait \
                .until(EC.element_to_be_clickable((By.XPATH, "//button[@data-test = 'cookie-necessary-button']"))) \
                .click()
        except NoSuchElementException:
            print("!!! Something's wrong with the cookies button")

    def _process_survey(self):
        """
        Validate Lego's survey form
        """

        print("* Sometimes they ask you to fill in a survey.")
        try:
            # FIXME: survey's layer escape key no longer work
            survey_layer = self.browser.find_element_by_id('ipeL104230')
            survey_layer.send_keys(Keys.ESCAPE)

            # we should click on the "no" button to close the survey window
            # no_survey_button = self.browser.find_element_by_xpath(
            #     "//area[contains(@onclick,'ipe.clWin')]")
            # no_survey_button.click()

        except NoSuchElementException:
            print("We're lucky, no survey on the LEGO shop today!")

    def _process_login(self):
        """
        Manage LEGO Shop login form

        return boolean
        """

        # login stuff #
        if self.username and self.password:

            print("* Let's log in with LEGO ID {user}.".format(user=self.username))
            login_link = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[@data-test = 'util-bar-account-dropdown']")))
            login_link.click()

            login_link = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[@data-test = 'legoid-login-button']")))
            login_link.click()

            self.wait.until(EC.invisibility_of_element_located(
                (By.XPATH, "//div[@id='loginform']")))

            user_input = self.wait.until(EC.element_to_be_clickable(
                (By.ID, 'username')))
            user_input.click()
            user_input.send_keys(self.username)

            passwd_input = self.wait.until(EC.element_to_be_clickable(
                (By.ID, 'password')))
            passwd_input.click()
            passwd_input.send_keys(self.password)

            login_button = self.browser.find_element_by_id('loginBtn')
            login_button.click()

            self.browser.switch_to.default_content()

            # ensure the user/password are good
            try:
                account_link = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[@data-test = 'util-bar-account-dropdown']")))
                account_link.click()

                self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//div[text()='Logout']")))

                self.browser.get(self.lego_shop + "/service/replacementparts/sale?chosenFlow=3")

                print("login success!")
                return True
            except TimeoutException:
                print("login failed!")
                # close the browser and stop here
                # self.browser.quit()
                return False
        else:
            print("!!! credentials are not defined")
            return True


class ReplacementPart(LegoShopBase):
    """
    Add a list of LEGO parts and their quantity to the 'Shopping Bag' of LEGO's
    customer service platform.  A browser window will be opened, you'll be able
    to watch the browser do what you would normally do by hand, and execution
    will stop after all pieces have been added, so you can review and finalize
    your order.  (This is just to help you save time on entering 60+ pieces
    manually.  Nothing is ordered on your behalf!)
    """

    def __init__(self, browser_name=None, shop=None):
        super().__init__(browser_name, shop)

        self.datafiles = {}

        # future objects to manage elements
        self.updated_parts = None
        self.electric_parts = None

        # inventory of added electric parts in order process
        self.electric_part_list = []

        self.partno_status = {
            'found': 1,
            'not_found': 2,
            'electric': 3,
        }

        #  set statistics counters to zero
        self.part_stats_counter = {
            'total_elements': 0,
            'found': 0,
            'duplicate_part': 0,
            'not_in_set': 0,
            'out_of_stock': 0,
            'electric_part': 0
        }

    def _process_survey_age_country(self):
        try:
            print("* They want to know how old we are.")
            age_field = self.wait.until(EC.element_to_be_clickable(
                (By.NAME, 'rpAgeAndCountryAgeField')))
            age_field.send_keys('55')
            age_field.send_keys(Keys.RETURN)

            # wait for age_field's DOM element to be removed
            self.wait.until(EC.staleness_of(age_field))
        except TimeoutException:
            print("!!! Something's wrong with the survey")

    def __process_select_lego_set(self, lego_set):
        """
        Manage Lego's Set choice
        """

        print("* We need to tell them which set we want to buy parts from: {lego_set}".format(
            lego_set=lego_set))
        setno_field = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@data-cy = 'enter-set-number-search']"))
        )

        setno_field.send_keys(lego_set)
        setno_field.send_keys(Keys.RETURN)

        self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[@data-cy = 'set-number-details-information']"))
        )

    def __process_partno(self, original_part_no):
        """
        Ensure a part is found, or test with newer ID
        """

        return_code = self.partno_status['not_found']

        original_part_no = int(original_part_no)
        new_part_no_list = self.updated_parts.get_part_list(original_part_no)
        # merge original part number with his alternatives
        partno_list = list([original_part_no] + new_part_no_list)

        part_no = None

        for idx, part_no in enumerate(partno_list):

            # idx 0 has the original part_no
            if idx > 0:
                print("\t>> Trying to replace with #{pn} ".format(pn=part_no), end='')

            element_field = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//input[@data-cy = 'search-set-number']")))
            element_field.clear()
            element_field.send_keys(part_no)
            element_field.send_keys(Keys.RETURN)
            sleep(.3)  # seconds

            try:
                # tip: count results to ensure the wanted part_no return nothing or one
                results_count = len(
                    self.browser.find_elements(By.XPATH, "//button[@data-cy = 'brick-item-direct-add-to-bag']"))

                if results_count == 0:

                    if self.electric_parts.partno_exists(part_no):
                        return_code = self.partno_status['electric']
                        break

                    if idx == 0 and len(partno_list) > 1:
                        # we're on the original part, and we've a list of new Element ID
                        print("Not Found, but has a chain of other Element ID:")
                        # a comment about the mapping
                        comment = self.updated_parts.get_part_comment(original_part_no)
                        print("\tcomment: {}".format(comment))
                    else:
                        print("Not Found!")

                elif results_count == 1:
                    return_code = self.partno_status['found']
                    break

                else:
                    print("Too many results with that part_no, bad number!")

            except NoSuchElementException:
                print("!!! Selenium error: CSS element not found")

        return part_no, return_code

    def __process_statistics(self):
        """
        Print statistics about ordered parts
        """

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

        print()
        print("We're done. You can finalize your order now. Thanks for watching!")
        print()
        if self.part_stats_counter['out_of_stock'] > 0:
            print("!! Take care about out of stock elements")
        if self.part_stats_counter['not_in_set'] > 0:
            print("!! Take care about not in set elements")

        if self.part_stats_counter['electric_part'] > 0:
            print()
            print("Electric parts you can add to your bag once you've added your order:")

            for item in self.electric_part_list:
                self.electric_parts.get_partno_standalone_link(item)

    def set_new_element_id_datafile(self, datafile):
        """
        Set path to datafile for New Element ID mapping
        """
        self.datafiles['newelementid'] = datafile

    def set_electric_part_datafile(self, datafile):
        """
        Set path to datafile for Electric part ID mapping
        """
        self.datafiles['electricparts'] = datafile

    def process(self, lego_set, order_list):
        """
        Main process to order LEGO's set parts
        """

        self.updated_parts = UpdatedPartMapping(self.datafiles['newelementid'])
        self.electric_parts = MindstormsElectricPart(self.datafiles['electricparts'])

        # simulate click to the third button ('Buy Bricks')
        self._init_browser(self.browser_name,
                           self.lego_shop + "/service/replacementparts/sale?chosenFlow=3")
        self._process_survey()
        self._process_age_gate()
        self._process_cookies_accept()
        self._process_choose_country()

        # The site now fails these login attempts as they are too fast.
        # if not self._process_login():
        #     return

        self.__process_select_lego_set(lego_set)

        print("Let's scroll the page down a bit, so we can see things better.")
        self.browser.execute_script("window.scroll(0, 750);")

        order_list = order_list.split(',')

        self.part_stats_counter['total_elements'] = len(order_list)

        print("That's gonna be crazy: {count} elements to order! Let's rock.".format(
            count=self.part_stats_counter['total_elements']))
        print()

        self.__process_order_list(lego_set, order_list)
        self.browser.execute_script("window.scroll(0, 0);")
        self.__process_statistics()

    def __process_order_list(self, lego_set, order_list=None):
        """
        Add set's parts to the bag

        - Detect duplicated ID, out-of-stock, not-in-set
        - Manage quantity
        - Manage separate order link for Mindstorms Electric parts
        """
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

                add_button = self.wait \
                    .until(EC.element_to_be_clickable((By.XPATH, "//button[@data-cy = 'brick-item-direct-add-to-bag']")))

                if add_button.is_enabled():
                    add_button.click()
                    sleep(.2)  # seconds
                    self.part_stats_counter['found'] += 1
                else:
                    self.part_stats_counter['out_of_stock'] += 1
                    print("\t!! NOTE: item out of stock.")
                    continue

                # set the value for item's quantity drop-down menu
                self.browser.execute_script("window.scroll(0, 0);")
                amount_select = self.wait \
                    .until(EC.visibility_of_element_located((By.XPATH, "//select[@data-cy = 'bag-item-quantity-select']")))
                Select(amount_select).select_by_visible_text(quantity)

                # ensure the value is correct
                selected = Select(amount_select).first_selected_option

                if quantity != selected.text:
                    print("\t!! WARNING: Could not select desired quantity. {} != {}".format(
                        quantity, selected.text))

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
