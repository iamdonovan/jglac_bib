# jglac_bib

A simple command-line tool to re-format the entries of a `.bib` file to fit the following requirements for the
[Journal of Glaciology](https://www.cambridge.org/core/journals/journal-of-glaciology):

- list all authors in the reference when there are six or fewer. When there are more than six, list only the first, 
  for example, 'Wang ZZ and 6 others'.
- have all journal names written in their ISO 4 abbreviated form in italics.


## requirements

To use the script, either use the provided `environment.yml` file to create a new conda environment, or use `pip` to
install the following packages:

- [bibtexparser](https://pypi.org/project/bibtexparser/)
- [iso4](https://pypi.org/project/iso4/)


## using the script

From the directory where you have the `.bib` file that needs re-formatting: 

::

    > $path_to_jglac_bib/reformat_bib.py references.bib

This will create a new file, `references_reformatted.bib`, which you can use to re-compile your manuscript.

Alternatively, you can add `$path_to_jglac_bib` to your PATH variable, and use `reformat_bib.py` directly:

::

    > reformat_bib.py reference.bib

