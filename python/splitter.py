#!/usr/bin/env python3
"""
Splits a file into multiple chunks.

**Changelog**

* 20/08/2015 - Pablo - First script version.
"""
import argparse
import glob
import logging.config
import os
import re
import shutil
import sys
import time

DEFAULT_COMMENTS = ['#']

def main(argv = None):
    # Retrieve arguments
    if argv is None:
        argv = sys.argv

    # Parse arguments
    parser = argparse.ArgumentParser(description = "Splits a file in the specified number of chunks")
    parser.add_argument('-f', '--files', type = str, nargs = '+',
                        required = True, dest = 'files',
                        help = "Files to split")
    parser.add_argument('-n', '--chunks', type = int, required = True,
                        help = "Number of chunks to split the file into")
    parser.add_argument('--commentChars', type = str, nargs = '*',
                        default = DEFAULT_COMMENTS, dest = 'comment_chars',
                        help = "Chars that represents comment line")
    parser.add_argument('--splitEmpty', action = 'store_true', default = False,
                        dest = 'split_empty',
                        help = "Char that represents comment line")
    parser.add_argument('-v', '--verbose', action = 'count', default = 0,
                        help = "Display verbose output")
    args = parser.parse_args()

    # Configure logging
    log_level = max(logging.WARNING - 10 * args.verbose, logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(logging.Formatter(fmt = '%(message)s'))

    logger = logging.getLogger('splitter')
    logger.setLevel(log_level)
    logger.addHandler(console_handler)

    # Expand file list
    file_list = []
    for file_expr in args.files:
        file_list.extend(glob.glob(file_expr))
    if not file_list:
        logger.error('No existent files specified')
        exit(1)
    logger.debug('Files to split - %s', file_list)

    # Split files
    for file in file_list:
        split_file(file, args.chunks, args.comment_chars, not args.split_empty)

    logger.info('Files splitted successfully')
    exit(0)


def split_file(file, chunks, comment_chars = [], ignore_empty = True):
    """Splits a text file into the sepecified chunks number.

    :param file: File to split.
    :type file: str

    :param chunks: Number of files to split the input file
    :type chunks: int

    :param comment_chars: The characters that specifies that a line is commented
    :type comment_chars: list[char]

    :param ignore_empty: Specify if empty files should be ignored. ``True`` by
        default
    :type ignore_empty: bool

    :returns: The generated out chunks
    :rtype: list[str]
    """
    logger = logging.getLogger('splitter.split_file')

    num_in_line = 0
    num_out_line = 0

    logger.info('Splitting file %s', file)

    logger.debug('Comment chars %s', comment_chars)

    if comment_chars:
        comment_re_text = '^\s*[{chars}]'.format(chars = ''.join(comment_chars))
        logger.debug('Line discard regexp %s', comment_re_text)
        comment_re = re.compile(comment_re_text)

    # Create output files
    out_file_list = [ "{original}.{num}".format(original = file, num = num)
                            for num in range(1, chunks + 1) ]
    out_files = [ open(f, 'w') for f in out_file_list ]

    # Filter file
    with open(file, 'r') as f:
        for line in f:
            num_in_line = num_in_line + 1

            # Filter blanks and comments
            if ignore_empty and not line.strip() or \
               comment_chars and comment_re.match(line):
                logger.debug('Discarding [%s] - "%s"', num_in_line, line.strip())
                continue

            # Write into corresponding file
            out_file_num = num_out_line % chunks
            num_out_line = num_out_line + 1
            out_files[out_file_num].write(line)
            logger.debug('Inserting  [%s] - "%s" in file %s', num_in_line, line.strip(), out_file_list[out_file_num])

    # Close output files
    for f in out_files:
        f.close()

    logger.debug('Output files - %s', out_file_list)
    return out_file_list


# Main execution
if (__name__ == "__main__"):
    sys.exit(main())
