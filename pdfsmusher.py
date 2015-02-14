#!/usr/bin/env python

"""
Simple utility to concatenate a group of PDFs together into a single file.

Usage:

    pdfsmusher LOCATION SELECTION OUTPUT_FILENAME --prefix PREFIX

    - Take the comma separated list SELECTION
    - For each ITEM in SELECTION, will generate a filename consisting of: PREFIX + ITEM + '.pdf'
    - And concatenate all of these files intput OUTPUT_FILENAME

    Example:

    pdfsmusher.py tests/test_questions "foo,bar" cat.pdf --prefix q

    Will store the contents of tests/test_questions/qfoo.pdf, and tests/test_questions/qbar.pdf to cat.pdf

Note:

    You can use --warn to relax the 'stop on missing' error.

"""

import argparse
import os
import sys

from pyPdf import PdfFileWriter, PdfFileReader

PARSER = argparse.ArgumentParser()

PARSER.add_argument("location", help="Location of .pdfs.")
PARSER.add_argument(
    "selection",
    help="Comma separated list of filenames (without '.pdf') to smush.")
PARSER.add_argument("output_filename", help="Output file.")
PARSER.add_argument("--prefix", help="Prefix for all files.", default="")
PARSER.add_argument(
    "--warn",
    help="Will warn of missing files, but won't terminate.",
    action="store_true")

ARGS = PARSER.parse_args()

PAGE_COUNT = 0


def build_list(base_dir, prefix, filenames, extension):
    """
    Creates a list of by joining base_dir, prefix, filename and extension for each filename in the array filenames.
    """
    return [
        os.path.join(
            base_dir,
            (prefix +
             filename)) +
        '.' +
        extension for filename in filenames]


def split_filenames(filenames):
    """
    Splits a string of comma separated strings into an array.
    """
    return filenames.strip().split(',')


def cat_pdf(in_pdf, out_pdf):
    """
    Concatenates all pages in in_pdf (PdfFileReader) into out_pdf (PdfFileWriter)
    """
    page_count = 0
    for page_number in range(in_pdf.numPages):
        out_pdf.addPage(in_pdf.getPage(page_number))
        page_count += 1
    return page_count


def smush_pdfs(output_filename, filenames):
    """
    Takes the list of build filenames and cats them into one pdf: output_filename.
    """
    page_count = 0
    output_pdf = PdfFileWriter()

    for filename in filenames:

        if os.path.exists(filename):
            current_file = PdfFileReader(file(filename, "rb"))
            page_count += cat_pdf(current_file, output_pdf)

        else:
            print "*** Missing: \'" + filename + "\' ***"
            if not ARGS.warn:
                sys.exit('Terminating')

    output_pdf.write(file(output_filename, "wb"))
    return page_count


def main():
    """
    Entry point.
    """
    filenames = split_filenames(ARGS.selection)
    question_files = build_list(ARGS.location, ARGS.prefix, filenames, 'pdf')

    page_count = smush_pdfs(ARGS.output_filename, question_files)
    print " Wrote %d pages to %s." % (page_count, ARGS.output_filename)

if __name__ == '__main__':
    main()
