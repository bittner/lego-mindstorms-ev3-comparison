#!/usr/bin/env python3
#
#    LEGO Mindstorms Editions Pieces Comparison
#    Copyright (C) 2015-2016  Peter Bittner <django@bittner.it>
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
A simple python program to find out which pieces you need to buy when
you have bought LEGO Mindstorms EV3 Home Edition (31313) and the Education
Expansion Set (45560).  So you can make all robots that can be made with
the Education Core Set (45544) + Education Expansion Set.
"""
import os.path
import sys
from argparse import ArgumentParser

SET_EV3HOME = '31313'
SET_EDUCORE = '45544'
SET_EDUEXPA = '45560'


def main():
    parser = ArgumentParser(description="Help with calculating and ordering required LEGO Mindstorms EV3 spare parts.")
    commands = parser.add_subparsers(metavar='command', dest='command')
    commands.required = True

    cmd = commands.add_parser(
        'parse', help="Parse 3 inventory data files and combine them into a single data list."
                      " You can redirect the output into a text file on the command line.")
    cmd.add_argument('datafiles', nargs=3, help="3 inventory data files for the 3 LEGO sets")

    cmd = commands.add_parser(
        'missing', help="Calculate the LEGO pieces missing in the combination of the Edu"
                        " Expansion set + Home or Edu Core, that only the other (omitted)"
                        " set would have.")
    cmd.add_argument('omitted_set', choices=[SET_EV3HOME, SET_EDUCORE],
                     help="The LEGO set you did *not* buy, which you need the bricks from."
                          " 31313 = Mindstorms EV3, 45544 = Edu Core, 45560 = Edu Expansion.")
    datafile_default = os.path.join('raw-data', 'Lego Mindstorms EV3 combined list.csv')
    cmd.add_argument('--datafile', '-f', default=datafile_default,
                     help="The combined list data file. Default: {}".format(datafile_default))

    cmd = commands.add_parser(
        'order', help="Add the LEGO parts you need to the shopping bag on LEGO's customer service platform.")
    cmd.add_argument('--shop', '-s', default='en-us',
                     choices=['nl-be', 'fr-be', 'cs-cz', 'da-dk', 'de-de', 'es-es', 'fr-fr',
                              'it-it', 'es-ar', 'hu-hu', 'nl-nl', 'nb-no', 'pl-pl', 'fi-fi',
                              'sv-se', 'en-gb', 'en-us', 'ru-ru', 'ko-kr', 'zh-cn', 'ja-jp'],
                     help="<language-country> identifier of the LEGO shop (language and geographic region)"
                          " you want to use for ordering. Default: en-us")
    cmd.add_argument('--browser', '-b', default='firefox', choices=['chrome', 'firefox'],
                     help="Web browser that will be used to open the LEGO shop. Default: firefox")
    cmd.add_argument('--username', '-u', help="User name for your LEGO ID account")
    cmd.add_argument('--password', '-p', help="Password for your LEGO ID account")
    cmd.add_argument('--lego-set', '-l', default=SET_EDUCORE, choices=[SET_EV3HOME, SET_EDUCORE, SET_EDUEXPA],
                     help="The LEGO set you did *not* buy, which you need the bricks from."
                          " 31313 = Mindstorms EV3, 45544 = Edu Core, 45560 = Edu Expansion."
                          " Default: 45544 (Edu Core)")
    cmd.add_argument('order_list',
                     help="A list of LEGO part_number:quantity you want to buy, separated by comma signs."
                          " Example: 370526:4,370726:2,4107085:4,4107767:2")

    # avoid intimidating the user ("error: ... required") with no arguments
    if len(sys.argv) == 1:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    kwargs = vars(args).copy()
    kwargs.pop('command', None)

    function = globals()[args.command]
    function(**kwargs)


def parse(datafiles):
    """
    Parse LEGO inventory files and combine them into a single list.
    """
    part_list = {}
    part_names = {}
    part_designids = {}
    part_imageurls = {}
    NO_PARTS = [0 for a in range(len(datafiles))]

    for file_count, name in enumerate(datafiles):
        print('Reading file: %s' % name, file=sys.stderr)
        with open(name) as f:
            data_lines = f.readlines()[1:]
            for line in data_lines:
                line = line.strip()
                try:
                    (set_no, part_no, quantity, color, category, design_id,
                     part_name, image_url, set_count) = line.split('\t')

                    part_no, quantity = int(part_no), int(quantity)

                    if part_no not in part_list.keys():
                        part_list[part_no] = NO_PARTS.copy()
                        part_names[part_no] = part_name
                        part_designids[part_no] = design_id
                        part_imageurls[part_no] = image_url

                    part_list[part_no][file_count] = quantity
                except ValueError as err:
                    print('Ignoring error: %s (%s)' % (err, line),
                          file=sys.stderr)

    part_numbers = list(part_list.keys())
    part_numbers.sort()

    print('Part no.\tLego ID\t%s\tPart name\tImage' % '\t'.join(datafiles))
    for part_no in part_numbers:
        part_data = {
            'partno': part_no,
            'legoid': part_designids[part_no],
            'counts': '\t'.join([str(a) for a in part_list[part_no]]),
            'name': part_names[part_no],
            'image': part_imageurls[part_no],
        }
        print('%(partno)s\t'
              '%(legoid)s\t'
              '%(counts)s\t'
              '%(name)s\t'
              '%(image)s' % part_data)


def missing(omitted_set, datafile):
    """
    Generate a list of LEGO parts missing in the remaining two LEGO sets.
    """
    order_list = []

    with open(datafile) as f:
        data_lines = f.readlines()[1:]
        for line in data_lines:
            (partno, legoid, count_home, count_core, count_expa, name, image) = line.split('\t')
            difference = \
                int(count_home) - int(count_core) if omitted_set == SET_EV3HOME else (
                    int(count_core) - int(count_home) if omitted_set == SET_EDUCORE else (
                        None  # undefined (will cause an error)
                    )
                )
            if difference > 0:
                order_list += ['{pn}:{qty}'.format(pn=partno, qty=difference)]

    print(','.join(order_list))


def order(shop=None, browser=None, lego_set=None, order_list=None, username=None, password=None):
    """
    Fill in LEGO parts to be ordered in LEGO's customer service shop.
    """
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver import Chrome, Firefox
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.select import Select
    from selenium.webdriver.support.wait import WebDriverWait
    from time import sleep

    order_list = order_list.split(',')

    shop_url = 'https://wwwsecure.us.lego.com/{shop}/service/replacementparts/order'.format(shop=shop)
    browser = Chrome() if browser == 'chrome' else Firefox()
    browser.get(shop_url)

    print("Sometimes they ask you to fill in a survey.")
    try:
        survey_layer = browser.find_element_by_id('ipeL104230')
        survey_layer.send_keys(Keys.ESCAPE)
    except NoSuchElementException:
        print("We're lucky, no survey on the LEGO shop today!")

    print("They want to know how old we are.")
    age_field = browser.find_element_by_name('rpAgeAndCountryAgeField')
    age_field.send_keys('55')
    age_field.send_keys(Keys.RETURN)

    if username and password:
        print("Let's log in with LEGO ID {user}.".format(user=username))
        login_link = browser.find_element_by_css_selector('.legoid .links > a')
        login_link.click()

        browser.switch_to.frame('legoid-iframe')

        user_input = browser.find_element_by_id('fieldUsername')
        user_input.click()
        user_input.send_keys(username)
        passwd_input = browser.find_element_by_id('fieldPassword')
        passwd_input.click()
        passwd_input.send_keys(password)
        login_button = browser.find_element_by_id('buttonSubmitLogin')
        login_button.click()

        browser.switch_to.default_content()

    sleep(4)  # seconds
    wait = WebDriverWait(browser, 5)

    print("We need to tell them which set we want to buy parts from: {lego_set}".format(lego_set=lego_set))
    setno_field = wait.until(EC.element_to_be_clickable(
        (By.CSS_SELECTOR, '.product-search input[ng-model=productNumber]')))
    setno_field.send_keys(lego_set)
    setno_field.send_keys(Keys.RETURN)

    print("Let's scroll the page down a bit, so we can see things better.")
    browser.execute_script("window.scroll(0, 750);")

    print("That's gonna be crazy: {count} elements to order! Let's rock.".format(count=len(order_list)))
    element_field = wait.until(EC.element_to_be_clickable(
        (By.ID, 'element-filter')))
    print()

    for brick in order_list:
        part_no, quantity = brick.split(':')
        print("- {qty}x #{pn} ".format(qty=quantity, pn=part_no), end='')

        element_field.clear()
        element_field.send_keys(part_no)
        element_field.send_keys(Keys.RETURN)
        sleep(.3)  # seconds

        try:
            add_button = browser.find_element_by_css_selector('.element-details + button')
            add_button.click()
            sleep(.2)  # seconds
        except NoSuchElementException:
            print("OOOPS! No LEGO part with that number found in set #{set}. :-(".format(set=lego_set))
            continue

        try:
            warn_msg = browser.find_element_by_css_selector('.alert-warning .sold-out-info')
            if warn_msg.is_displayed():
                print("NOTE: item out of stock. ", end='')
                add_anyway = browser.find_element_by_css_selector('.alert-warning + .clearfix button')
                add_anyway.click()
        except NoSuchElementException:
            pass

        amount_select = browser.find_elements_by_css_selector('.bag-item select')[-1]
        amount_select.send_keys(quantity)
        amount_select.send_keys(Keys.TAB)

        selected = Select(amount_select).first_selected_option
        if quantity != selected.text:
            print("WARNING: Could not select desired quantity. {} != {}".format(quantity, selected.text))
        else:
            print()

    browser.execute_script("window.scroll(0, 0);")
    print()
    print("We're done. You can finalize your order now. Thanks for watching!")


if __name__ == "__main__":
    main()
