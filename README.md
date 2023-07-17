# Pylang

`main.py`

```python
from Pylang import Lang

lang = Lang(langDir="./lang", defaultLang="en_EN")

print(lang.t('MAIN.btn')) # return Button

```

- langDir     : is path folder contain all file lang
- defaultLang : is default lang load


`./lang/en_EN.json`

```json

{
  "LONG_LANG": "English",
  "MAIN": {
    "btn": "Button"
  }
}

```

LONG_LANG is a name of langage
