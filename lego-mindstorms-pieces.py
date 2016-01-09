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
import sys
from argparse import ArgumentParser


def main():
    parser = ArgumentParser(description="Help with calculating and ordering required LEGO Mindstorms EV3 spare parts.")
    commands = parser.add_subparsers(metavar='command', dest='command')
    commands.required = True
    cmd = commands.add_parser(
            'parse', help="Parse 3 inventory data files and combine them into a single data list."
                          " You can redirect the output into a text file on the command line.")
    cmd.add_argument('datafiles', nargs=3, help="3 inventory data files for the 3 LEGO sets")
    cmd = commands.add_parser(
            'order', help="Add the LEGO parts you need to the shopping bag on LEGO's customer service platform.")
    cmd.add_argument('--lego-shop', dest='shop', default='en-us',
                     help="<language-country> identifier of the LEGO shop (language and geographic region)"
                          " you want to use for ordering. Default: en-us")

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
                    set_no, part_no, quantity, color, category, design_id, \
                    part_name, image_url, set_count = line.split('\t')

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


def order():
    """
    Fill in LEGO parts to be ordered in LEGO's customer service shop.
    """
    pass


if __name__ == "__main__":
    main()
