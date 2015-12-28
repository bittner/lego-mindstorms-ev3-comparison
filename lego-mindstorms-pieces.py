#!/usr/bin/env python3
#
#    LEGO Mindstorms Editions Pieces Comparison
#    Copyright (C) 2015  Peter Bittner <django@bittner.it>
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

files = sys.argv[1:]
part_list = {}
NO_PARTS = [0 for a in range(len(files))]

for file_count, name in enumerate(files):
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

                part_list[part_no][file_count] = quantity
            except ValueError as err:
                print('Ignoring error: %s (%s)' % (err, line),
                      file=sys.stderr)

part_numbers = list(part_list.keys())
part_numbers.sort()

print('Part no.\t%s\tPart name' % '\t'.join(files))
for part_no in part_numbers:
    part_counts = '\t'.join([str(a) for a in part_list[part_no]])
    print('%s\t%s' % (part_no, part_counts))
