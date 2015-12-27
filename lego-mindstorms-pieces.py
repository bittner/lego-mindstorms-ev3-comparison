#!/usr/bin/env python3
"""
A simple python program to find out which pieces you need to buy when
you have bought Lego Mindstorms EV3 Home Edition (31313) and the Education
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
        for line in f.readlines():
            line = line.strip()
            try:
                count, part_no = line.split('\t')
                count, part_no = int(count), int(part_no)

                if part_no not in part_list.keys():
                    part_list[part_no] = NO_PARTS.copy()

                part_list[part_no][file_count] = count
            except ValueError as err:
                print('Ignoring error: %s (%s)' % (err, line),
                      file=sys.stderr)

part_numbers = list(part_list.keys())
part_numbers.sort()

print('Part no.\t%s' % '\t'.join(files))
for part_no in part_numbers:
    part_counts = '\t'.join([str(a) for a in part_list[part_no]])
    print('%s\t%s' % (part_no, part_counts))
