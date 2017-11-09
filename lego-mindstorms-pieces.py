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

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))


def main():
    parser = ArgumentParser(description="Help with calculating and ordering required"
                                        " LEGO Mindstorms EV3 spare parts.")
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
    datafile_default = os.path.join(SCRIPT_PATH,
                                    'raw-data', 'Lego Mindstorms EV3 combined list.csv')
    cmd.add_argument('--datafile', '-f', default=datafile_default,
                     help="The combined list data file. Default: {}".format(datafile_default))

    cmd = commands.add_parser('order', help="Add the LEGO parts you need to the shopping bag"
                                            " on LEGO's customer service platform.")
    cmd.add_argument('--shop', '-s', default='en-us',
                     choices=['nl-be', 'fr-be', 'cs-cz', 'da-dk', 'de-de', 'es-es', 'fr-fr',
                              'it-it', 'es-ar', 'hu-hu', 'nl-nl', 'nb-no', 'pl-pl', 'fi-fi',
                              'sv-se', 'en-gb', 'en-us', 'ru-ru', 'ko-kr', 'zh-cn', 'ja-jp'],
                     help="<language-country> identifier of the LEGO shop (language and"
                          " geographic region) you want to use for ordering. Default: en-us")
    cmd.add_argument('--browser', '-b', default='firefox', choices=['chrome', 'firefox'],
                     help="Web browser that will be used to open the LEGO shop. Default: firefox")
    cmd.add_argument('--username', '-u', help="User name for your LEGO ID account")
    cmd.add_argument('--password', '-p', help="Password for your LEGO ID account")
    cmd.add_argument('--lego-set', '-l', default=SET_EDUCORE,
                     choices=[SET_EV3HOME, SET_EDUCORE, SET_EDUEXPA],
                     help="The LEGO set you did *not* buy, which you need the bricks from."
                          " 31313 = Mindstorms EV3, 45544 = Edu Core, 45560 = Edu Expansion."
                          " Default: 45544 (Edu Core)")
    cmd.add_argument('order_list',
                     help="A list of LEGO part_number:quantity you want to buy, separated by"
                          " comma signs. Example: 370526:4,370726:2,4107085:4,4107767:2")

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
    import legoshop

    order = legoshop.ReplacementPart(browser, shop)
    order.set_new_element_id_datafile(
        os.path.join(SCRIPT_PATH, 'raw-data', 'elementid-refresh.csv'))
    order.set_electric_part_datafile(os.path.join(SCRIPT_PATH, 'raw-data', 'Electric-parts.csv'))
    order.set_credentials(username, password)
    order.process(lego_set, order_list)


if __name__ == "__main__":
    main()
