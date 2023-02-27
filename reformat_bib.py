#!/usr/bin/env python
import os
import argparse
import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from iso4 import abbreviate
import nltk


def _argparser():
    _parser = argparse.ArgumentParser(description="Re-format .bib file entries to meet Journal of Glaciology style:\n"
                                                  "\n"
                                                  "  - list all authors in the reference when there are six or fewer.\n"
                                                  "    When there are more than six, list only the first, for example\n"
                                                  "    'Wang ZZ and 6 others'.\n"
                                                  "  - have all journal names written in their ISO 4 abbreviated form\n"
                                                  "    in italics.",
                                      formatter_class=argparse.RawDescriptionHelpFormatter)

    _parser.add_argument('fn_bib', action='store', type=str, help='the name of the bibfile to re-format.')
    _parser.add_argument('-o', '--outname', action='store', type=str, default=None,
                         help='The name of the output file. Defaults to "fn_bib_reformatted.bib"')
    _parser.add_argument('-v', '--verbose', action='store_true',
                         help='Print information about what entries have been changed.')
    return _parser


def check_auth_num(this_entry, _args):
    """
    Reformat the author list according to the journal's style guide:

        "List all authors in the reference when there are six or fewer. When there are more than six, list only
        the first, for example 'Wang ZZ and 6 others'."

    :param this_entry: the entry to check and re-write if needed
    :return:
    """

    if 'author' in this_entry.keys():
        authors = this_entry['author'].split(' and ')  # add space around 'and'

        if len(authors) > 6:
            authstr = authors[0] + ' and {{{}}} others'.format(len(authors) - 1)
            if _args.verbose:
                print('{} author changed to "{}"'.format(this_entry['ID'], authstr))

            # enclose in extra braces to force bibtex to include number
            this_entry.update({'author': '{' + authstr + '}'})

    return this_entry


def main():
    parser = _argparser()
    args = parser.parse_args()

    if args.outname is None:
        base, ext = os.path.splitext(args.fn_bib)
        fn_out = base + '_reformatted' + ext

    # download the files needed for iso4
    nltk.download('wordnet')

    with open(args.fn_bib) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    for entry in bib_database.entries:
        # first, check the author number and rewrite if needed
        entry = check_auth_num(entry, args)

        # then, check the journals
        if 'journal' in entry.keys():
            new_fmt = abbreviate(entry['journal'])

            # for some reason, it abbreviates "Remote" as "Remote."
            if 'Remote.' in new_fmt:
                new_fmt = new_fmt.replace('Remote.', 'Remote')
            if args.verbose:
                print('{} journal changed to "{}"'.format(entry['ID'], new_fmt))

            entry.update({'journal': new_fmt})

    # now, write the changes to a new file
    writer = BibTexWriter()
    with open(fn_out, 'w') as bibfile:
        bibfile.write(writer.write(bib_database))


if __name__ == "__main__":
    main()
