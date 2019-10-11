#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse

from lark import Lark
tsParser = Lark(r"""
    int: INTERFACE CNAME "{" typedef* "}"

    typedef : comment* CNAME ":" type ";"

    comment: /\/\*([^\/]*)\*\//

    type : "string"
        | "number"
        | "any"

    INTERFACE: "interface"

    %import common.CNAME
    %import common.WS
    %import common.NEWLINE
    %ignore WS
    %ignore NEWLINE
    """, start='int', debug=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Typescript Interface Parser")
    parser.add_argument('file', metavar='file', type=str, help='The path to the file that ONLY contains the typescript interface')

    args = parser.parse_args()

    if not os.path.isfile(args.file):
        print("File {} does not exists".format(args.file))
        sys.exit(0)

    content = None

    with open(args.file, "r") as var:
        content = var.read()

    if content is None:
        print("File is empty")
        sys.exit(0)

    print("PROGRAM TO PARSE: {}".format(content))

    print(tsParser.parse(content).pretty())
