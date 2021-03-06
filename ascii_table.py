#!/usr/local/bin/python
#
#  ascii_table.py v.0.1.2
#  Converts a .tsv or .csv file to an ascii table
#
#  Created by Rudolf Farkas on 28.02.2020
#  Copyright © 2020 Rudolf Farkas. All rights reserved.
#

import sys
import os
from itertools import zip_longest
from argparse import ArgumentParser

class AsciiTable(object):

    def __init__(self, text_lines = [''], delimiter = ','):
        """Given a list of `text_lines` and a `delimiter` character
        initialize the instance and prepare for generation of the ascii table representation.
        """
        self.text_lines = text_lines
        self.delimiter = delimiter

    @staticmethod
    def len_of(strings):
        """Given a list `strings`, returns the total length of listed strings.
        """
        return len(''.join(strings))

    @staticmethod
    def splitme(text, limit):
        """Splits text into prefix and suffix
        such that len(prefix) <= limit
        and prefix ends with a whole word if possible,
        while suffix contains the remainder of text, if any.
        Returns a tuple (prefix, suffix).
        """
        limit = max(limit, 1)
        if len(text) <= limit:
            return text, ''
        prefix = text[:limit]
        lsx = prefix.rfind(' ')
        if lsx >= 0:
            return text[:lsx], text[lsx:]
        else:
            return text[:limit], text[limit:]

    @staticmethod
    def fields_from(textline, delim):
        """ Strips textline of outer spaces, splits it on the delim character
        into a list of fields, each stripped of its outer spaces.
        Returns the list of fields.
        """
        return [field.strip() for field in textline.strip(' ').split(delim)]

    @staticmethod
    def max_fieldwidths_from(lines, delim):
        """Given a list of lines and a delim that splits each line into fields
        finds max width for each column.
        Returns the list of column widths.
        """
        maxwidths = []
        for line in lines:
            widths = [len(field) for field in AsciiTable.fields_from(line, delim)]
            maxwidths = [max(m, w) for m, w in zip_longest(maxwidths, widths, fillvalue = 0)]
        return maxwidths

    @staticmethod
    def table_width_for(maxwidths):
        """Given `maxwidths` returns the corresponding table width.
        """
        return sum(maxwidths) + 3 * (len(maxwidths) - 1) + 2*2

    @staticmethod
    def fit(maxwidths, max_table_width):
        """Given `maxwidths` and a `max_table_width`, reduce `maxwidths` values (largest first)
        so that the resulting `table_width` is not above `max_table_width`.
        Return the reduced `maxwidths`.
        """
        while(True):
            table_width = AsciiTable.table_width_for(maxwidths)
            if sum(maxwidths)== 0:
                return maxwidths
            elif table_width <= max_table_width:
                return maxwidths
            else:
                limit = int(max(maxwidths) - (table_width - max_table_width) / len(maxwidths))
                maxwidths = [limit if width > limit else width for width in maxwidths]

    @staticmethod
    def string_from(fieldwidths, linefields):
        """Given `fieldwidths` and `linefields`
        compose a string each field is truncated or padded if needed to the corresponding fieldwidth
        then fields are joined by column separators and surrounded by column ends.
        Moreover, in the case of uneven numbner of fields in lines, pad shorter line fields with '' fields.
        Returns the composed string.
        """
        out = []
        for idx, field in enumerate(linefields):
            fieldwidth = fieldwidths[idx]
            out.append(field[:fieldwidth] + ' ' * (fieldwidth - len(field)))
        for idx in range(len(linefields), len(fieldwidths)):
            out.append(' ' * fieldwidths[idx])
        return '| ' + ' | '.join(out) + ' |'

    @staticmethod
    def linebreak_from(fieldwidths):
        """Given `fieldwidths` compose a `linebreak` string
        compatible with `fieldwidths`.
        Returns the `linebreak` string.
        """
        out = []
        for width in fieldwidths:
            out.append('-' * (width + 2))
        return '+' + '+'.join(out) + '+'

    @staticmethod
    def limited_lines(fieldwidths, fields):
        """Given `fieldwidths` and `fields` of a line
        fold `fields` into several `row_lines` if necessary
        such that each field remains within the corresponding `fieldwidths` value.
        Returns the list of row_lines.
        """
        row_lines = []
        while(AsciiTable.len_of(fields) > 0):
            field_prefixes = [AsciiTable.splitme(field, limit)[0] for field, limit in zip(fields, fieldwidths)]
            row_lines.append(AsciiTable.string_from(fieldwidths, field_prefixes))
            fields = [AsciiTable.splitme(field, limit)[1].lstrip() for field, limit in zip(fields, fieldwidths)]
        return row_lines

    @staticmethod
    def table_limited(lines, delim, table_width):
        """Given `lines`, `delim` and `table_width` composes and returns a multiline table string.
        """
        max_fieldwidths = AsciiTable.max_fieldwidths_from(lines, delim)
        new_maxwidths = AsciiTable.fit(max_fieldwidths, table_width)
        linebreak = AsciiTable.linebreak_from(new_maxwidths)
        textlines = [linebreak]
        for line in lines:
             fields = AsciiTable.fields_from(line, delim)
             if AsciiTable.len_of(fields) == 0:
                 continue # skip a blank line
             limited = AsciiTable.limited_lines(new_maxwidths, fields)
             textlines += limited
             textlines.append(linebreak)
        return "\n".join(textlines)
    pass

def lines_from(filehandle):
    """Given a `filehandle` to an open text file
    returns a list of text lines from the file.
    """
    filehandle.seek(0,0)
    lines = []
    for line in filehandle:
        lines.append(line)
    return lines

def string_table_limited(filehandle, delim, table_width):
    """Given `filehandle`, `delim` and `table_width` get text lines from the file,
    composes a multiline table string and returns it.
    """
    lines = lines_from(filehandle)
    return AsciiTable.table_limited(lines, delim, table_width)

def run(args):
    with open(args.filepath,'r') as fh:
        table_limited2 = string_table_limited(fh, delim, args.w)
        print(table_limited2)

if __name__ == "__main__":
    parser = ArgumentParser(description='Converts a .tsv or .csv file to an ascii table.\nPrints the result to stdout.')
    parser.add_argument("filepath", type=str, default=None, help='path to a text file containing a tsv or a csv representation of table data.')
    parser.add_argument("-d", default=',', help='delimiter (determined automatically for .tsv and .csv files)')
    parser.add_argument("-w", default=150, type=int, help='desired table width (characters)')
    args = parser.parse_args()

    # print("args.filepath=", args.filepath)
    # print("args.d=", args.d)
    # print("args.w=", args.w)

    if args.filepath is not None:
        fileroot, ext = os.path.splitext(args.filepath)
        if ext == ".csv":
            delim = ","
        elif ext == ".tsv":
            delim = "\t"
        run(args)
