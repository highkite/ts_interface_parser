#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import argparse

from lark import Lark, Transformer

class TsToJson(Transformer):
    def comment(self, elements):
        return {"description" : str(elements[0])}

    def tstype(self, elements):
        return {"type" : str(elements[0])}

    def typedef(self, elements):
        if len(elements) == 3:
            return {str(elements[1]) : {"description" : elements[0]["description"], "type" : elements[2]["type"]}}
        else:
            return {str(elements[0]) : {"description" : "", "type" : elements[1].get("type", "any")}}

    def int(self, elements):
        ret_val = {str(elements[1]) : {}}
        for i in range(2, len(elements)):
            ret_val[str(elements[1])].update(elements[i])

        return ret_val



tsParser = Lark(r"""
    int: INTERFACE CNAME "{" typedef* "}"

    typedef : comment* CNAME ":" tstype ";"

    comment: /\/\*([^\/]*)\*\//

    tstype : CNAME

    INTERFACE: "interface"

    %import common.CNAME
    %import common.WS
    %import common.NEWLINE
    %ignore WS
    %ignore NEWLINE
    """, start='int')

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

    tree = tsParser.parse(content)

    print(json.dumps(TsToJson().transform(tree), indent=4, sort_keys=True))
