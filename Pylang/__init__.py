import pathlib, locale
import re as regex
from typing import Literal
from .error import MinssingKeyError, NotFoundDefaultLang, MatchLangError, NotLangLoaded

from ruamel.yaml import YAML
import json


class Lang:

    langDir: str
    type: Literal["json", "yaml"]

    defaultLang: str = "en_EN"
    selectedLang: str
    sysLang: str
    loadedLang: list[str] = []
    longLangKey: str = "LONG_LANG"
    reLang: regex.Pattern

    indexSelectedLang: int

    sepKey: str = "."

    lang: dict = {}

    def __init__(self, langDir: str, type: Literal["json", "yaml"] = "yaml", defaultLang: str = "en_EN") -> 'Lang':

        self.reLang = regex.compile(r"^[a-z]{2}_[A-Z]{2}$")

        self.langDir = langDir

        if type in ["json", "yaml"]:
            self.type = type

        try:
            if bool(self.reLang.match(defaultLang)):
                self.defaultLang = defaultLang
            else:
                self.defaultLang = "en_EN"
        except TypeError:
            self.defaultLang = "en_EN"

        self.selectedLang = self.defaultLang

        self.loadLangFile()
        self.checkLangFile()
        self.checkSameKey()
        self.__updateIndexSelectedLang()

    def __updateIndexSelectedLang(self):

        for i, l in enumerate(self.loadedLang):
            if self.selectedLang == l:
                self.indexSelectedLang = i

    def __flatten(self, object: dict, parentKey='', sep='_>') -> dict:
        items = []
        for k, v in object.items():

            newKey = parentKey + sep + k if parentKey else k

            if isinstance(v, dict):
                items.extend(self.__flatten(v, newKey, sep=sep).items())
            else:
                items.append((newKey, v))
        return dict(items)

    def __extractKey(self, object: dict) -> list:
        key = []

        for k in object.keys():
            key.append(k)
        return key

    def checkSameKey(self) -> None:

        template = self.__extractKey(self.__flatten(self.lang[self.selectedLang]))

        for l in self.loadedLang:
            if l == self.selectedLang:
                continue
            
            compare = self.__extractKey(self.__flatten(self.lang[l]))
            for k in template:
                if k not in compare:
                    raise MinssingKeyError(f"{k} in {l}")

    def checkLangFile(self):

        try:
            _ = self.lang[self.selectedLang]
        except KeyError:
            raise NotFoundDefaultLang(self.selectedLang)

    def loadLangFile(self):

        if self.type == "json": ext: list = ["*.json"]
        if self.type == "yaml": ext: list = ["*.yml", "*.yaml"]

        for fileExt in ext:
            for file in pathlib.Path(self.langDir).glob(fileExt):

                fileName = pathlib.Path(file).stem

                if bool(self.reLang.match(fileName)):
                    with open(file, 'r', encoding='utf8') as contentFile:
                        if self.type == "json": self.lang[fileName] = json.load(contentFile)
                        if self.type == "yaml": self.lang[fileName] = YAML(typ="safe", pure=True).load(contentFile)

                        self.loadedLang.append(fileName)
                else:
                    raise MatchLangError(fileName)


    def t(self, key: str, index: int = 0) -> str:

        return self.translate(key, index)

    def translate(self, key: str, index: int = 0) -> str:

        temp = None

        try:
            for i, k in enumerate(key.split(self.sepKey)):
                
                if i != 0:
                    temp = temp[k]
                else:
                    temp = self.lang[self.selectedLang][k]
        except KeyError:
            return key

        if isinstance(temp, str):
            return temp

        if isinstance(temp, list):
            return temp[index]

        return key

    #SETTER
    def setSeparatorKey(self, sepKey: str) -> None:

        if not len(sepKey) > 1:
            self.sepKey = sepKey

    def setLang(self, lang: str) -> None:

        try:
            if bool(self.reLang.match(lang)):
                self.selectedLang = lang
            else:
                self.selectedLang = self.defaultLang
        except TypeError:
            self.selectedLang = self.defaultLang

        self.checkLangFile()
        self.__updateIndexSelectedLang()

    def setLongLangKey(self, longLangKey) -> None:
        self.longLangKey = longLangKey

    #GETTER
    def getLocaleSys(self) -> str:
        return locale.getdefaultlocale()[0]

    def getLocaleShort(self, longLang: str) -> str:

        for l in self.loadedLang:

            if self.lang[l][self.longLangKey] == longLang:
                return l

        return ""

    def getLocaleLong(self, shortLang: str) -> str:

        if bool(self.reLang.match(shortLang)):

            if shortLang in self.loadedLang:
                try:
                    return self.lang[shortLang][self.longLangKey]
                except KeyError:
                    raise MinssingKeyError(f"{self.longLangKey}")
            else:
                raise NotLangLoaded(f"lang {shortLang} is not loaded")
        else:
            raise MatchLangError(shortLang)

    def getLocalesLong(self) -> list:
        temp = []

        for l in self.loadedLang:
            temp.append(self.lang[l][self.longLangKey])

        return temp

    def getLocalesShort(self) -> list:
        return self.loadedLang

    def getIndexDefaultLang(self) -> int:
        return self.indexSelectedLang







