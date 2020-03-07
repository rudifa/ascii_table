# ascii_table

    ascii_table % ascii_table.py
    usage: ascii_table.py [-h] [-d D] [-w W] filepath
    ascii_table.py: error: the following arguments are required: filepath

    ascii_table % ascii_table.py -h
    usage: ascii_table.py [-h] [-d D] [-w W] filepath

    Converts a .tsv or .csv file to an ascii table. Prints the result to stdout.

    positional arguments:
      filepath    path to a text file containing a tsv or a csv representation of
                  table data.

    optional arguments:
      -h, --help  show this help message and exit
      -d D        delimiter (determined automatically for .tsv and .csv files)
      -w W        desired table width (characters)
