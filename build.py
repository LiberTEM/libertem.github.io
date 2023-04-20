#!/usr/bin/env python3
from typing import List
import json
import click
import os


def format_entry(a):
    entry = "**"
    if 'displayname' in a:
        entry += a['displayname']
    if 'affiliation' in a:
        entry += " (%s)" % a['affiliation']
    entry += "**"
    if 'orcid' in a:
        entry += " [ORCID](https://orcid.org/%s)" % a['orcid']
    if 'github' in a:
        entry += " [GitHub](https://github.com/%s)" % a['github']

    if 'contribution' in a:
        entry += "\n: %s" % a['contribution']

    entry += "\n\n"
    return entry


INTRO = """
# Acknowledgements

We are very grateful for your continuing support for LiberTEM!

Please help us keeping these lists up-to-date and complete! If you feel that
you should be listed here, please contact us or open a pull request.
We are grateful for every contribution, and if your contribution
is not listed here we'd like to extend our apologies and update
this as soon as possible.
"""


@click.command()
@click.option(
    '--project',
    type=click.Path(file_okay=False, dir_okay=True),
    multiple=True,
)
@click.option(
    '--out',
    type=click.File('w', encoding='utf-8'),
    default='acknowledgements.md',
)
def main(project: List[click.Path], out: click.File):
    def author(d):
        return d['authorname']

    out.write("---\ntitle: Acknowledgements\n---\n")

    out.write(INTRO)

    out.write("## Jump to project\n")

    for p in project:
        p_basename = os.path.basename(os.path.normpath(p))
        out.write(f"- [{p_basename}](#{p_basename.lower()})\n")

    for p in project:
        p_basename = os.path.basename(os.path.normpath(p))
        creators = os.path.join(p, 'packaging', 'creators.json')
        with open(creators, "r") as f:
            creators_list = sorted(json.load(f), key=author)
        contributors = os.path.join(p, 'packaging', 'contributors.json')
        with open(contributors, 'r') as f:
            contributors_list = sorted(json.load(f), key=author)

        out.write(f'## {p_basename}\n\n')
        out.write('### Creators\n')
        out.write(
            'The following people in alphabetical order contributed to'
            ' source code, documentation, design and management '
            'following our [Authorship Policy]'
            '(https://libertem.github.io/LiberTEM/authorship.html)\n\n'
        )
        for c in creators_list:
            out.write(format_entry(c))

        out.write('## Contributors\n')
        out.write(
            f'The following people in alphabetical order contributed to '
            f'the {p_basename} project in other ways.\n\n'
        )
        for c in contributors_list:
            out.write(format_entry(c))


if __name__ == '__main__':
    main()
