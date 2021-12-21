"""
Shorten import statements!

Example, BEFORE:

someFolder
|-- string_func
|   |-- __init__.py
|   |      ^ Empty file
|   |-- stringToUpper.py
|   |-- stringToLower.py
|   `-- strengthLength.py
`-- example1.py
        ^ import string_func.stringLength

Example, AFTER:

someFolder
|-- string_func
|   |-- __init__.py
|   |      ^ from .stringLength import stringLength
|   |-- stringToUpper.py
|   |-- stringToLower.py
|   `-- strengthLength.py
`-- example1.py
        ^ import string_func

"""
