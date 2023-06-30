# Pylang

`main.py`

```py
from Pylang import Lang

lang = Lang(langDir="./lang", type='yaml', defaultLang="en_EN")

print(lang.t('MAIN.btn')) # return Button

```

- langDir     : is path folder contain all file lang
- type        : is format file lang (json or yaml)
- defaultLang : is default lang load


`./lang/en_EN.yml`

```yml
LONG_LANG: "English"

MAIN:
    btn: Button

```

LONG_LANG is a name of langage
