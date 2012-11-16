#!/usr/bin/env python
"""
Recipe from `Fill Paragraph (Python recipe)`_

.. _Fill Paragraph (Python recipe):
    http://code.activestate.com/recipes/134571-fill-paragraph/

"""
from __future__ import unicode_literals
import argparse
import re
import sys
import random


def justify_line(line, width):
    """Stretch a line to width by filling in spaces at word gaps.

    The gaps are picked randomly one-after-another, before it starts
    over again.

    """
    i = []
    while 1:
        # line not long enough already?
        if len(' '.join(line)) < width:
            if not i:
                # index list is exhausted
                # get list if indices excluding last word
                i = range(max(1, len(line) - 1))
                # and shuffle it
                random.shuffle(i)
            # append space to a random word and remove its index
            line[i.pop(0)] += ' '
        else:
            # line has reached specified width or wider
            return ' '.join(line)


def fill_paragraphs(text, width=80, justify=0):
    """Split a text into paragraphs and wrap them to width linelength.

    Optionally justify the paragraphs (i.e. stretch lines to fill width).

    Inter-word space is reduced to one space character and paragraphs are
    always separated by two newlines. Indention is currently also lost.

    """
    # split taxt into paragraphs at occurences of two or more newlines
    paragraphs = re.split(r'\n\n+', text)
    for i in range(len(paragraphs)):
        # split paragraphs into a list of words
        words = paragraphs[i].strip().split()
        line = []
        new_par = []
        while 1:
            if words:
                if len(' '.join(line + [words[0]])) > width and line:
                    # the line is already long enough -> add it to paragraph
                    if justify:
                        # stretch line to fill width
                        new_par.append(justify_line(line, width))
                    else:
                        new_par.append(' '.join(line))
                    line = []
                else:
                    # append next word
                    line.append(words.pop(0))
            else:
                # last line in paragraph
                new_par.append(' '.join(line))
                line = []
                break
        # replace paragraph with formatted version
        paragraphs[i] = '\n'.join(new_par)
    # return paragraphs separated by two newlines
    return '\n\n'.join(paragraphs)


def main():
    # options
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'text', nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin
    )
    args = parser.parse_args()
    print fill_paragraphs(args.text.read().decode('utf-8'))


if __name__ == '__main__':
    main()
