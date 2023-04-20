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

    for p in project:
        creators = os.path.join(p, 'packaging', 'creators.json')
        with open(creators, "r") as f:
            creators_list = sorted(json.load(f), key=author)
        contributors = os.path.join(p, 'packaging', 'contributors.json')
        with open(contributors, 'r') as f:
            contributors_list = sorted(json.load(f), key=author)

        p_basename = os.path.basename(os.path.normpath(p))

        out.write(f'# {p_basename}\n\n')

        for c in creators_list:
            out.write(format_entry(c))

        for c in contributors_list:
            out.write(format_entry(c))


if __name__ == '__main__':
    main()
