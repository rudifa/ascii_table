#!/usr/local/bin/python
#
#  ascii_table_unittest.py v.0.1.2
#  Tests for ascii_table.py
#
#  Created by Rudolf Farkas on 28.02.2020
#  Copyright © 2020 Rudolf Farkas. All rights reserved.
#

import unittest
from ascii_table import AsciiTable

class AsciiTable_unittest(unittest.TestCase):

    def setUp(self):
        self.tsv_delim = '\t'
        self.tsv_3_lines = ["state	s.e	event	action	next state",
                ".idle  0 cells selected	0.0	hit a free cell	select cell	.booking1",
                "	0.1	hit a cell in a current user's booking	select cell	.cancelling"]
        self.tsv_3_lines_uneven_len = ["state	s.e	event	action	next state",
                ".idle  0 cells selected	0.0	hit a free cell	select cell	.booking1	UNKNOWN FLYING OBJECT",
                "	0.1	hit a cell in a current user's booking	select cell	.cancelling"]
        self.maxDiff = None # <- enables to display long string differences

    def test_splitme(self):
        input = "deselect the selected"
        self.assertEqual(len(input), 21)
        limit = 25
        self.assertEqual(AsciiTable.splitme(input, limit),  ('deselect the selected', ''))
        limit = 21
        self.assertEqual(AsciiTable.splitme(input, limit),  ('deselect the selected', ''))
        limit = 20
        self.assertEqual(AsciiTable.splitme(input, limit),  ('deselect the', ' selected'))
        limit = 15
        self.assertEqual(AsciiTable.splitme(input, limit),  ('deselect the', ' selected'))
        limit = 12
        self.assertEqual(AsciiTable.splitme(input, limit),  ('deselect', ' the selected'))
        limit = 11
        self.assertEqual(AsciiTable.splitme(input, limit),  ('deselect', ' the selected'))
        limit = 9
        self.assertEqual(AsciiTable.splitme(input, limit),  ('deselect', ' the selected'))
        limit = 8
        self.assertEqual(AsciiTable.splitme(input, limit),  ('deselect', ' the selected'))
        limit = 7
        self.assertEqual(AsciiTable.splitme(input, limit),  ('deselec', 't the selected'))
        limit = 1
        self.assertEqual(AsciiTable.splitme(input, limit),  ('d', 'eselect the selected'))
        limit = 0
        self.assertEqual(AsciiTable.splitme(input, limit),  ('d', 'eselect the selected'))
        limit = -7
        self.assertEqual(AsciiTable.splitme(input, limit),  ('d', 'eselect the selected'))

        input = ""
        self.assertEqual(len(input), 0)
        limit = 5
        self.assertEqual(AsciiTable.splitme(input, limit),  ('', ''))
        limit = 0
        self.assertEqual(AsciiTable.splitme(input, limit),  ('', ''))
        limit = -5
        self.assertEqual(AsciiTable.splitme(input, limit),  ('', ''))

    def test_len_of(self):
        input = ['']
        self.assertEqual(AsciiTable.len_of(input), 0)
        input = ['', '0.1', 'select cell', '.cancelling']
        self.assertEqual(AsciiTable.len_of(input), 25)

    def test_fields_from(self):
        delim = '\t'
        input = "	0.1	hit a cell in a current user's booking	select cell	.cancelling"
        self.assertEqual(AsciiTable.fields_from(input, delim), ['', '0.1', "hit a cell in a current user's booking", 'select cell', '.cancelling'])
        input = ""
        self.assertEqual(AsciiTable.fields_from(input, delim), [''])
        input = "\t"
        self.assertEqual(AsciiTable.fields_from(input, delim), ['', ''])

    def test_max_fieldwidths_from(self):
        delim = '\t'
        table_width = 80
        self.assertEqual(AsciiTable.max_fieldwidths_from(self.tsv_3_lines, self.tsv_delim), [23, 3, 38, 11, 11])
        self.assertEqual(AsciiTable.max_fieldwidths_from(self.tsv_3_lines_uneven_len, self.tsv_delim), [23, 3, 38, 11, 11, 21])

    def test_table_width_for(self):
        fieldwidths = [23, 3, 38, 11, 11]
        output = AsciiTable.table_width_for(fieldwidths)
        self.assertLessEqual(output, 120)
        self.assertEqual(output, 102)
        fieldwidths = [10, 3, 10, 10, 10]
        output = AsciiTable.table_width_for(fieldwidths)
        self.assertLessEqual(output, 60)
        self.assertEqual(output, 59)

    def test_fit(self):
        max_fieldwidths = [23, 3, 38, 11, 11]
        table_width = 120
        self.assertEqual(AsciiTable.fit(max_fieldwidths, table_width), [23, 3, 38, 11, 11])
        table_width = 60
        self.assertEqual(AsciiTable.fit(max_fieldwidths, table_width), [10, 3, 10, 10, 10])
        max_fieldwidths = [23, 3, 38, 11, 11, 21]
        self.assertEqual(AsciiTable.fit(max_fieldwidths, table_width), [7, 3, 7, 7, 7, 7])

    def test_linebreak_from(self):
        maxwidths = [10, 3, 10, 10, 10]
        self.assertEqual(AsciiTable.linebreak_from(maxwidths), '+------------+-----+------------+------------+------------+')
        maxwidths = [7, 3, 7, 7, 7, 7]
        self.assertEqual(AsciiTable.linebreak_from(maxwidths), '+---------+-----+---------+---------+---------+---------+')

    def test_string_from(self):
        maxwidths = [10, 3, 10, 10, 10]
        fields = AsciiTable.fields_from(self.tsv_3_lines[2], self.tsv_delim)
        output = AsciiTable.string_from(maxwidths, fields)
        self.assertEqual(output, "|            | 0.1 | hit a cell | select cel | .cancellin |")

    def test_limited_lines(self):
        maxwidths = [10, 3, 10, 10, 10]
        fields = AsciiTable.fields_from(self.tsv_3_lines[2], self.tsv_delim)
        expected = ['|            | 0.1 | hit a      | select     | .cancellin |',
                    '|            |     | cell in a  | cell       | g          |',
                    '|            |     | current    |            |            |',
                    "|            |     | user's     |            |            |",
                    '|            |     | booking    |            |            |']
        output = AsciiTable.limited_lines(maxwidths, fields)
        self.assertEqual(output, expected)

    def test_table_limited(self):
        table_width = 50
        input = ['']
        self.assertEqual(AsciiTable.table_limited(input, self.tsv_delim, table_width), '+--+')
        table_width = 80
        #self.maxDiff = None #<- uncomment to see long string differences
        expected = """\
+---------------------+-----+---------------------+-------------+-------------+
| state               | s.e | event               | action      | next state  |
+---------------------+-----+---------------------+-------------+-------------+
| .idle  0 cells      | 0.0 | hit a free cell     | select cell | .booking1   |
| selected            |     |                     |             |             |
+---------------------+-----+---------------------+-------------+-------------+
|                     | 0.1 | hit a cell in a     | select cell | .cancelling |
|                     |     | current user's      |             |             |
|                     |     | booking             |             |             |
+---------------------+-----+---------------------+-------------+-------------+"""
        self.assertEqual(AsciiTable.table_limited(self.tsv_3_lines, self.tsv_delim, table_width), expected)
        #print("\n"+table_limited(input, delim, table_width))

        # verify that uneven number of fields in lines is supported graciosly
        table_width = 80
        expected = """\
+--------------+-----+--------------+-------------+-------------+--------------+
| state        | s.e | event        | action      | next state  |              |
+--------------+-----+--------------+-------------+-------------+--------------+
| .idle  0     | 0.0 | hit a free   | select cell | .booking1   | UNKNOWN      |
| cells        |     | cell         |             |             | FLYING       |
| selected     |     |              |             |             | OBJECT       |
+--------------+-----+--------------+-------------+-------------+--------------+
|              | 0.1 | hit a cell   | select cell | .cancelling |              |
|              |     | in a         |             |             |              |
|              |     | current      |             |             |              |
|              |     | user's       |             |             |              |
|              |     | booking      |             |             |              |
+--------------+-----+--------------+-------------+-------------+--------------+"""
        output = AsciiTable.table_limited(self.tsv_3_lines_uneven_len, self.tsv_delim, table_width)
        self.assertEqual(output, expected)


if __name__ == "__main__":
    unittest.main()
