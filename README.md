# Typescript Interface Parser (and to JSON converter)

The typescript interface parser parses interfaces defined in typescript and outputs a JSON object describing the interfaces.

## Features

- output to file and to stdio
- comments are also considered and provided by the JSON representation
- supports a wide range of typescript syntax (if you find something missing please file a feature request)
- can be easily integrated in your own program for parsing typescript interfaces

### MISC

I needed to communicate with a server via RPC from a Python client, but all valid messages were specified in Typescript interfaces. There were a huge number of different messages and I slowly got bored translating the interfaces manually. So I implemented this translator. Hope it will serve you, as well as it served me.

## Installation

### Manual installation

Clone the repo and install the requirements with
`pip install -r requirements.txt`. Than type `python3 ts_interface_parser.py -h` to get an overview of the possible options.

## How does it work?

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

### Translation of attributes

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

        <attribute_name_3>? : <type_4>;

        const <attribute_name_4> : <type_5>;

        readonly <attribute_name_5> : <type_6>;
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
                "<attribute_name_3>" : {
                        "optional" : true,
                        "type" : [
                                "<type_4>"
                        ]
                },
                "<attribute_name_4>" : {
                        "constant" : true,
                        "type" : [
                                "<type_5>"
                        ]
                },
                "<attribute_name_5>" : {
                        "readonly" : true,
                        "type" : [
                                "<type_6>"
                        ]
                }
        }
}
```

#### Indexed Attributes

#### Function Attributes
