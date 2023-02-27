import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from iso4 import abbreviate
import nltk


def check_auth_num(this_entry):
    """
    Reformat the author list according to the journal's style guide:

        "List all authors in the reference when there are six or fewer. When there are more than six, list only
        the first, for example 'Wang ZZ and 6 others'."

    :param this_entry: the entry to check and re-write if needed
    :return:
    """

    if 'author' in this_entry.keys():
        authors = entry['author'].split(' and ')  # add space around 'and'

        if len(authors) > 6:
            authstr = authors[0] + ' and {{{}}} others'.format(len(authors) - 1)
            print('{} author changed to "{}"'.format(entry['ID'], authstr))

            # enclose in extra braces to force bibtex to include number
            this_entry.update({'author': '{' + authstr + '}'})

    return this_entry


# download the files needed for iso4
nltk.download('wordnet')

with open('example.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file)

for entry in bib_database.entries:
    # first, check the author number and rewrite if needed
    entry = check_auth_num(entry)

    # then, check the journals
    if 'journal' in entry.keys():
        new_fmt = abbreviate(entry['journal'])

        # for some reason, it abbreviates "Remote" as "Remote."
        if 'Remote.' in new_fmt:
            new_fmt = new_fmt.replace('Remote.', 'Remote')
        print('{} journal changed to "{}"'.format(entry['ID'], new_fmt))

        entry.update({'journal': new_fmt})

# now, write the changes to a new file
writer = BibTexWriter()
with open('reformatted.bib', 'w') as bibfile:
    bibfile.write(writer.write(bib_database))
