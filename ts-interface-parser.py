#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import json
import argparse
import lark

from lark import Lark, Transformer

class TsToJson(Transformer):
    def comment(self, elements):
        return {"description" : str(elements[0])}

    def tstype(self, elements):
        ret_val = []

        for element in elements:
            if type(element) == lark.lexer.Token and element.type == "CNAME":
                ret_val.append(str(element))
            elif type(element) == lark.tree.Tree and element.data == "conjunction":
                cs = [str(child) for child in element.children]
                ret_val.append({"conjunction" : cs})
            elif type(element) == lark.tree.Tree:
                ret_val[-1] = ret_val[-1] + "[]"
            elif type(element) == dict:
                ret_val.append(element)
            else:
                ret_val.append(str(element))


        return {"type" : ret_val}

    def optional(self, elements):
        return {"optional" : True}

    def typedef(self, elements):
        ret_dict = {}

        name = None

        for element in elements:
            if type(element) == dict and "description" in element:
                ret_dict["description"] = element["description"]
            elif type(element) == dict and "type" in element:
                ret_dict["type"] = element["type"]
            elif type(element) == dict and "optional" in element:
                ret_dict["optional"] = True
            else:
                name = str(element)

        if name is None:
            raise Exception("Has no name")

        return {name : ret_dict}

    def int(self, elements):
        elements = [i for i in elements if not str(i) == "export" and not str(i) == "interface"]

        descr = None
        name = None
        start_index = 1

        if type(elements[0]) == dict and "description" in elements[0]:
            descr = elements[0]["description"]
            name = str(elements[1])
            start_index = 2
        else:
            name = str(elements[0])

        if name is None:
            raise Exception("Has no name")

        ret_val = {name : {"description" :descr}}

        for i in range(start_index, len(elements)):
            ret_val[name].update(elements[i])

        return ret_val


tsParser = Lark(r"""
    int: comment? EXPORT? INTERFACE CNAME "{" typedef* "}"

    typedef : comment? CNAME optional? ":" tstype (";" | ",")?

    optional : "?"

    comment: /\/\*((.|\s)*?)\*\//

    tstype : (CNAME | ESCAPED_STRING | OTHER_ESCAPED_STRINGS | "{" typedef* "}" | conjunction) isarray? ("|" (CNAME | ESCAPED_STRING | OTHER_ESCAPED_STRINGS | "{" typedef* "}" | conjunction )isarray?)*

    isarray : "[]"

    conjunction : "(" CNAME ( "&" CNAME)* ")"

    INTERFACE: "interface"
    EXPORT: "export"

    OTHER_ESCAPED_STRINGS : "'" _STRING_ESC_INNER "'"

    %import common.CNAME
    %import common.WS
    %import common.NEWLINE
    %import common.ESCAPED_STRING
    %import common._STRING_ESC_INNER
    %ignore WS
    %ignore NEWLINE
    """, start='int')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Typescript Interface Parser")
    parser.add_argument('file', metavar='file', type=str, help='The path to the file that ONLY contains the typescript interface')
    parser.add_argument('-p', '--parse_tree', action='store_true', help="Pretty print the parse tree.")

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

    if args.parse_tree:
        print(tree.pretty())

    print(json.dumps(TsToJson().transform(tree), indent=4, sort_keys=True))
