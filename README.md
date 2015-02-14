# pdfsmusher

Create a single pdf from multiple pdf files.

## Example Usage:

    pdfsmusher.py ~/exam "1,2,3,bonus" mytest.pdf --prefix Q

Will combine:
- ~/exam/Q1.pdf
- ~/exam/Q2.pdf
- ~/exam/Q3.pdf
- ~/exam/Qbonus.pdf

into a single file: *mytest.pdf*

## Getting Help:

    pdfsmusher.py --help

## Required Modules

- pypdf

## Misc:

- Style verified with:

    `pylint -rn pdfsmusher.py --max-line-length 120`

- Formatted with:

    `autopep8 --in-place --aggressive --aggressive pdfsmusher.py`
