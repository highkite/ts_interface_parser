import unittest
import re
from ts_interface_parser import transform


class TestParser(unittest.TestCase):
    def assertEqualJSON(self, first, second, msg=""):
        first = re.sub(r"\s+", "", first)
        second = re.sub(r"\s+", "", second)
        self.assertEqual(first, second, msg)

    def test_simple_interface(self):
        idata = """
            interface LabeledValue {
                label: string;
            }
        """
        target = """{
    "LabeledValue": {
        "label": {
            "type": [
                "string"
            ]
        }
    }
}"""
        self.assertEqual(transform(idata), target)

    def test_optional_properties(self):
        idata = """
            interface SquareConfig {
                color?: string;
                width?: number;
            }
        """
        target = """{
    "SquareConfig": {
        "color": {
            "optional": true,
            "type": [
                "string"
            ]
        },
        "width": {
            "optional": true,
            "type": [
                "number"
            ]
        }
    }
}"""
        self.assertEqual(transform(idata), target)

    def test_readonly_properties(self):
        idata = """
            interface Point {
				readonly x: number;
				readonly y: number;
			}
        """
        target = """{
        "Point": {
            "x": {
                "readonly": true,
                "type": [
                    "number"
                ]
            },
            "y": {
                "readonly": true,
                "type": [
                    "number"
                ]
            }
        }
}"""
        self.assertEqualJSON(transform(idata), target)

    def test_const_properties(self):
        idata = """
            interface Point {
				const x: number;
				const y: number;
			}
        """
        target = """{
        "Point": {
            "x": {
                "constant": true,
                "type": [
                    "number"
                ]
            },
            "y": {
                "constant": true,
                "type": [
                    "number"
                ]
            }
        }
}"""
        self.assertEqualJSON(transform(idata), target)

    def test_string_index_signature(self):
        idata = """
			interface SquareConfig {
				color?: string;
				width?: number;
				[propName: string]: any;
			}
        """
        target = """{
         "SquareConfig": {
            "color": {
                "optional": true,
                "type": [
                    "string"
                ]
            },
            "propName": {
                "indexed": {
                    "type": [
                        "string"
                    ]
                },
                "type": [
                    "any"
                ]
            },
            "width": {
                "optional": true,
                "type": [
                    "number"
                ]
            }
        }
}"""
        self.assertEqualJSON(transform(idata), target)

    def test_indexable_types(self):
        idata = """
			interface NotOkay {
				[y: number]: Animal;
				[x: string]: Dog;
			}
        """
        target = """{
    "NotOkay": {
        "x": {
            "indexed": {
                "type": [
                    "string"
                ]
            },
            "type": [
                "Dog"
            ]
        },
        "y": {
            "indexed": {
                "type": [
                    "number"
                ]
            },
            "type": [
                "Animal"
            ]
        }
    }
}"""
        self.assertEqualJSON(transform(idata), target)

    def test_indexable_different_types(self):
        idata = """
			interface NumberOrStringDictionary {
				[index: string]: number | string;
				length: number;
				name: string;
            }
        """
        target = """{
         "NumberOrStringDictionary": {
            "index": {
                "indexed": {
                    "type": [
                        "string"
                    ]
                },
                "type": [
                    "number",
                    "string"
                ]
            },
            "length": {
                "type": [
                    "number"
                ]
            },
            "name": {
                "type": [
                    "string"
                ]
            }
        }
}"""
        self.assertEqualJSON(transform(idata), target)

    def test_indexable_readonly_types(self):
        idata = """
			interface ReadonlyStringArray {
                readonly [index: number]: string;
			}
        """
        target = """{
        "ReadonlyStringArray": {
            "index": {
                "indexed": {
                    "type": [
                        "number"
                    ]
                },
                "readonly": true,
                "type": [
                    "string"
                ]
            }
        }
}"""
        self.assertEqualJSON(transform(idata), target)

    def test_extensions(self):
        idata = """
			interface Square extends Shape {
                sideLength: number;
			}
        """
        target = """{
         "Square": {
            "extends": [
                "Shape"
            ],
            "sideLength": {
                "type": [
                    "number"
                ]
            }
        }
}"""
        self.assertEqualJSON(transform(idata), target)

    def test_multiple_extensions(self):
        idata = """
			interface Square extends Shape, PenStroke {
				sideLength: number;
			}
        """
        target = """{
	"Square": {
		"extends": [
			"Shape",
			"PenStroke"
		],
		"sideLength": {
			"type": [
				"number"
			]
		}
	}
}"""
        self.assertEqualJSON(transform(idata), target)

    def test_inline_comment(self):
        idata = """
			interface NumberOrStringDictionary {
				[index: string]: number | string;
				length: number;    // ok, length is a number
				name: string;      // ok, name is a string
            }
        """
        print(transform(idata))

    def test_function_types(self):
        idata = """
			interface SearchFunc{
				(source: string, subString: string): boolean;
			}
        """
        print(transform(idata))

    def test_named_function_types(self):
        idata = """
			interface ClockInterface {
				currentTime: Date;
				setTime(d: Date): void;
			}
        """
        print(transform(idata))
