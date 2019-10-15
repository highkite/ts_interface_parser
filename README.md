# Typescript Interface Parser (and to JSON converter)

The typescript interface parser parses interfaces defined in typescript and outputs a JSON object describing the interfaces.

![Preview](./documentation/render1571132256134.gif "Example Preview")

## Features

- output to file and to stdio
- comments are also considered and provided by the JSON representation
- supports a wide range of typescript syntax (if you find something missing please file a feature request)
- can be easily integrated in your own program for parsing typescript interfaces

## Table of Contents

1. [Installation](#Installation)
      1. [Pypi](#Pypi)
      1. [Manual Installation](#ManualInstallation)
      1. [Running the Unit Tests](#unittest)
2. [The JSON Representation](#json)
      1. [Translation of Attributes](#attributes)
      1. [Indexed Attributes](#index)
      1. [Function Attributes](#function)

### MISC

I needed to communicate with a server via RPC from a Python client, but all valid messages were specified in Typescript interfaces. There were a huge number of different messages and I slowly got bored translating the interfaces manually. So I implemented this translator. Hope it will serve you, as well as it served me.

## <a name="Installation"></a>Installation

### <a name="Pypi"></a>Pypi

```
pip install ts-interface-parser
```

### <a name="ManualInstallation"></a>Manual installation

Clone the repo and install the requirements with
`pip install -r requirements.txt`. Than type `python3 ts_interface_parser.py -h` to get an overview of the possible options.

### <a name="unittest"></a>Running the Unit Tests

```
python3 -m unittest test.test_parser.TestParser
```

## <a name="json"></a>The JSON Representation

The general translation works as follows:

```
/**
* <some comment>
*/
interface <interface_name> extends <extension_a>, <extension_b> {
        <attribute_1> : <type_1>;
}
```

is translated to

```
{
        "<interface_name>" : {
                "description" : "<some comment>",
                "extends": [
                        "<extension_a>",
                        "<extension_b>"
                ]
                "<attribute_1> : {
                        "type" : [
                                "<type_1>"
                        ]
                }
        }
}
```

The comment becomes the decsription and potential extensions are provided in the `extends` field. For every specified attribute an object is added referenced by the name of the attribute. Here `<attribute_1>`.

### <a name="attributes"></a>Translation of Attributes

In the following I give examples of different attribute definitions and how those are translated into JSON.

```
interface <interface_name> {
        <attribute_name_1> : <type_1> | <type_2>; // <comment_1>
        /**
        * <comment_2>
        */
        <attribute_name_2> : {
                <attribute_name_3> : <type_3>
        }

        <attribute_name_4>? : <type_4>;

        const <attribute_name_5> : <type_5>;

        readonly <attribute_name_6> : <type_6>;

        <attribute_name_7> : "value 1" | "value 2";
}
```

is translated to

```
{
        "<interface_name>" : {
                "<attribute_name_1>" : {
                        "description" : "<comment_1">,
                        "type" : [
                                "type_1",
                                "type_2"
                        ]
                },
                "<attribute_name_2>" : {
                        "description" : "<comment_2">,
                        "type": {
                                "<attribute_name_3>" : {
                                        "type" : [
                                                "type_3"
                                        ]
                                }
                        }
                },
                "<attribute_name_4>" : {
                        "optional" : true,
                        "type" : [
                                "<type_4>"
                        ]
                },
                "<attribute_name_5>" : {
                        "constant" : true,
                        "type" : [
                                "<type_5>"
                        ]
                },
                "<attribute_name_6>" : {
                        "readonly" : true,
                        "type" : [
                                "<type_6>"
                        ]
                },
                "<attribute_name_7>" : {
                        "type" : [
                                "'value 1'",
                                "'value 2'",
                        ]
                }
        }
}
```

#### <a name="index"></a>Indexed Attributes

```
interface ReadonlyStringArray {
        [index: number]: string;
}
```

The indexed attribute is named with the variable name within the square brackets. The attribute has a field `indexed` which contains the index type and the type the index is refering to.

```
{
        "ReadonlyStringArray": {
                "index": {
                        "indexed": {
                                "type": [
                                        "number"
                                ]
                        },
                        "type": [
                                "string"
                        ]
                }
        }
}
```

#### <a name="function"></a>Function Attributes

Functions are marked by a field `function` in the JSON representation of the function. Thus

```
interface ClockInterface {
        setTime(d: Date): void;
}
```

translates to

```
{
        "ClockInterface": {
                "setTime": {
                        "function": true,
                        "parameters": {
                                "d": {
                                        "type": [
                                                "Date"
                                        ]
                                }
                        },
                        "type": [
                                "void"
                        ]
                }
}
```

For anonymous function declarations, as for instance:

```
interface SearchFunc{
        (source: string, subString: string): boolean;
}
```

This interface is translated to:

```
{
        "SearchFunc": {
                "anonymous_function": {
                    "function": true,
                    "parameters": {
                        "source": {
                            "type": [
                                "string"
                            ]
                        },
                        "subString": {
                            "type": [
                                "string"
                            ]
                        }
                    },
                    "type": [
                        "boolean"
                    ]
                }
        }
}
```
