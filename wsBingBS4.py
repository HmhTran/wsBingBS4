# Import libraries
import requests
from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import urllib.parse

import shutil
import sys
from os import path
from pathlib import Path

from datetime import datetime, date, timezone, timedelta
from dateutil import tz
import time

import re

from collections import deque
import json

#from enum import Enum
from aenum import Enum, NoAlias, OrderedEnum, Constant

from dataclasses import dataclass, field
from typing import Any, Callable, ClassVar, Dict, List, Union, Optional
import functools

#from unicodedata import *
#dashB = bytes('‑', 'utf-8')
#dashU = ord('‑')
#dash = str(dashB, 'utf-8')
#dash = dashB.decode('utf-8')
#dash = b"\xe2\x80\x91".decode("utf-8")
#print('‑' == chr(8209))
#print(name(8209))

#dash  = '‑'
#space = '\xa0'
#dash  = str(b"\xe2\x80\x91", "utf-8")
#space = str(b"\xc2\xa0", "utf-8")
#space = str(b"\xa0", "latin1")

#NON_BREAKING_HYPEN  = '\u2011'
#NO_BREAK_SPACE      = '\u00a0'
#nbhy = '&#8209'
#nbsp = '&nbsp'
#nbhy = '\u2011'
#nbsp = '\u00a0'

class K(Constant):
    NBHY = '\u2011'
    NBSP = '\u00a0'

#print('‑' == NON_BREAKING_HYPEN)
#print('\xa0' == NO_BREAK_SPACE)
#sys.exit()

# strTest = "xxx<hr>xxxabcxxx<hr>xxxijkxxx<hr>xxx"
# length = len(strTest)
# print(length)

# end = strTest.rfind("<hr>")
# print(end)

# isIn = strTest.rfind("ijk", 0, end)
# print(isIn)

# start = strTest.rfind("<hr>", 0, isIn)
# print(start)

# strTest = strTest[0:start] + strTest[end:]
# print(strTest)

def replaceAtIndex(string, idxStart, lenSep, substr):
    if lenSep < 1:
        return string

    idxEnd = idxStart + lenSep
    
    if idxEnd < len(string):
        return string[:idxStart] + substr + string[idxEnd:]
    else:
        return string[:idxStart] + substr
    
    return string

class OrderedValueEnum(Enum):
    def __eq__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ == other._value_
        return False
    
    def __ne__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ != other._value_
        return False
        
    def __ge__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ >= other._value_
        return False
    
    def __gt__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ > other._value_
        return False
    
    def __le__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ <= other._value_
        return False
    
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self._value_ < other._value_
        return False

class OrderedValueReversedEnum(OrderedValueEnum):        
    def __ge__(self, other):
        return super().__le__(other)
    
    def __gt__(self, other):
        return super().__lt__(other)
    
    def __le__(self, other):
        return super().__ge__(other)
    
    def __lt__(self, other):
        return super().__gt__(other)
        
class Bing_Mkt_Error(Exception):
    """A custom exception used to report errors in use of BING_MKT class"""

#@dataclass
class Bing_Mkt(OrderedValueReversedEnum, settings=NoAlias):
    INTERNATIONAL = -8
    NEW_ZEALAND = 12
    AUSTRALIA = 10
    JAPAN = 9
    KOREA = 9
    CHINA = 8
    HONG_KONG = 8
    TAIWAN = 8
    PHILIPPINES = 8
    MALAYSIA = 8
    INDONESIA = 7
    INDIA = 5
    RUSSIA = 3
    FINLAND = 3
    TURKEY = 3
    SOUTH_AFRICA = 2
    GERMANY = 1
    FRANCE = 1
    SPAIN = 1
    ITALY = 1
    SWITZERLAND = 1
    NETHERLANDS = 1
    BELGIUM = 1
    POLAND = 1
    AUSTRIA = 1
    SWEDEN = 1
    NORWAY = 1
    DENMARK = 1
    UNITED_KINGDOM = 0
    BRAZIL = -3
    ARGENTINA = -3
    CHILE = -4
    CANADA_ENGLISH = -5
    CANADA_FRENCH = -5
    MEXICO = -6
    UNITED_STATES = -8
    CHINA_ENGLISH = -8
    
    #__listPrefix__: ClassVar[List[str]] = field(default=['united ', 'new ', 'hong ', 'south '], init=False, repr=False)
    #__listLang__: ClassVar[List[str]] = field(default=['english', 'french'], init=False, repr=False)
    #__listMiddle__: ClassVar[List[str]] = field(default=[' ‑ ', ' - ', ' ‑', ' -', '‑ ', '- ', '‑', '-'], init=False, repr=False)
    #__listSpace__: ClassVar[List[str]] = field(default=[' ‑ ', ' - '], init=False, repr=False)
    
    __listPrefix__ = ['united', 'new', 'hong', 'south']
    __listLang__   = ['english', 'french']
    __setDash__    = {K.NBHY, '-'}
    __setSpace__   = {K.NBSP, ' ', '\x09', '\x0c', '\x0d'}
    
    @classmethod
    def from_string(cls, string: str) -> "BING_MKT":
        if not isinstance(string, str):
            raise BING_MKT_Error('Input must be string')
        
        s = string.lstrip().rstrip().lower()
        
        # for prefix in cls.__listPrefix__:
            # if s.startswith(prefix) and s[len(prefix)] in cls.__listSpace__:
                # s = replaceAtIndex(s, len(prefix), 1, '_')
                # break
        
        # for lang in cls.__listLang__:
            # if s.endswith(lang):
                # rLenLang = -len(lang)
                
                # # for middle in cls.__listMiddle__:
                    # # rLenStart = rLenEnd-len(middle)
                    
                    # # if s[rLenStart:rLenEnd] == middle:
                        # # s = replaceAtIndex(s, len(s) + rLenStart, len(middle), '_')
                        # # break
                
                # rLen = 0
                # if s[rLenLang-1] in cls.__listDash__:
                    # if s[rLenLang-2] not in cls.__listSpace__:
                        # rLen = -1
                    # else:
                        # rLen = -2
                # elif s[rLenLang-2] in  cls.__listDash__ and s[rLenLang-1] in  cls.__listSpace__:
                    # if s[rLenLang-3] in cls.__listSpace__:
                        # rLen = -3
                    # else:
                        # rLen = -2
                
                # s = replaceAtIndex(s, len(s) + rLenLang + rLen, -rLen, '_')
                # break
        
        prefix = ''
        if any(s.startswith(prefix := pf) for pf in cls.__listPrefix__):
            s = replaceAtIndex(s, len(prefix), 1, '_')
        
        lang = ''
        if any(s.endswith(lang := lg) for lg in cls.__listLang__):
            rLenLang = -len(lang)
            
            rLen = 0            
            if s[rLenLang-1] in cls.__setDash__:
                if s[rLenLang-2] not in cls.__setSpace__:
                    rLen = -1
                else:
                    rLen = -2
            elif s[rLenLang-2] in  cls.__setDash__ and s[rLenLang-1] in  cls.__setSpace__:
                if s[rLenLang-3] in cls.__setSpace__:
                    rLen = -3
                else:
                    rLen = -2
            
            s = replaceAtIndex(s, len(s) + rLenLang + rLen, -rLen, '_')
        
        mapping = iter(cls.__members__.items())
        next(mapping)
        for name, member in mapping:
            if s == name.lower():
                return member
        else:
            return cls.INTERNATIONAL

#e = Bing_Mkt.CHINA_ENGLISH
#print(Bing_Mkt.from_string('China‑English'))
#print(Bing_Mkt.CHINA_ENGLISH == Bing_Mkt.INTERNATIONAL)
#listTest = [(0,'b'), (1,'a'), (2,'a'), (3,'a'), (4,'c')]
#print(min(reversed(listTest), key = lambda x: x[1]))
#sys.exit()

def downloadImage(imgUrl, dirDest=None):
    if dirDest:
        if not isinstance(dirDest, Path):
            dirDest = Path(dirDest)
        
        if not dirDest.is_dir():
            #print('Directory does not exist')
            os.mkdirs(dirDest)
    else:
        dirDest = Path('')
        
    r = requests.get(imgUrl, stream = True)
    
    fileName = imgUrl.split("/")[-1]
    pathDest = dirDest / fileName
    
    if path.isfile(pathDest):
        print('Image already exists: ', fileName)
        return
    
    if r.status_code == 200:
        r.raw.decode_content = True
        
        with open(pathDest, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
        
        print('Image sucessfully Downloaded: ', fileName)
    else:
        print('Image Couldn\'t be retreived:  ', fileName, '; ', r.status_code)

def findStrInHref(tag, s, r):
    if not (tag.has_attr('href') and isinstance(s, str)):
        return -1
    
    link = tag.get('href')
    if not r:
        return link.find(s)
    else:
        return link.rfind(s)

def isLandscape(url):
    errMsg = "Invalid Bing image url"
    
    if not isinstance(url, str):
        raise ValueError(errMsg)
        
    limit = -len(url)
    
    idStart = -4
    if url[idStart:] != '.jpg':
        print(url, url[idStart:])
        raise ValueError(errMsg)
    
    i = idStart - 1
    
    if not url[i].isdigit():
        while i >= limit and not url[i] == "_":
            if not url[i].isalnum():
                print(url, url[i])
                raise ValueError(errMsg)            
            i-=1
        
        if i == limit-1 or not url[i-1].isdigit() or url[i+1:] == '.jpg':
            print(url, i)
            raise ValueError(errMsg)
        
        idStart = i
        i-=1
    i-=1
    
    while i >= limit and url[i].isdigit():
        i-=1
    
    if url[i] != 'x':
        print(url, url[i])
        raise ValueError(errMsg)
        
    idX = i
    
    i-=1
    while i >= limit and url[i].isdigit():
        i-=1
        
    if url[i] != '_' or not url[i+1].isdigit() or not url[i-1].isalnum():
        print(url, url[i])
        raise ValueError(errMsg)
    
    return int(url[i+1 : idX]) >= int(url[idX+1 : idStart])

def getImageNameFromUrl(url):
    if not isinstance(url, str):
        return ''
        
    return url[url.rfind('/')+1:url.rfind('_')]
    
def findPrevIndImg(nameImage, listTags):
    indexStart = 0
    nameStart = ''
    
    for index, tag in enumerate(listTags):
        nameStart = tag.name
        if nameStart != 'a':
            indexStart = index
            break
        
    isPrevHref = False
    prevInd = 0
    i = indexStart
    
    for index, tag in enumerate(listTags, start=0):
        if index < indexStart:
            continue
        
        if (tag.name == nameStart) and isPrevHref:
            prevInd = i
        
        if tag.name == 'a' and tag.has_attr('href'):
            link = tag.get('href')
            if '.jpg' == link[-4:] and nameImage == getImageNameFromUrl(tag.get('href')):
                return prevInd
            else:
                isPrevHref = True
                
        else:
            isPrevHref = False
        
        i += 1
        
    return i

def getIndexDatePoints(date, dataTags):
    indexStart = -1
    
    isStartOfDiv = False
    indexStartTemp = -1
    tagContent = ""
    dateContent = ""
    for index, tag in enumerate(dataTags):
        
        if tag.name == 'th':
            tagContent = tag.contents[0]
            
            if not isStartOfDiv:
                isStartOfDiv = True
            
                dateContent = tagContent[0:-2]
                if (indexStart < 0):
                    if dateContent > date:
                        indexStartTemp = index
                    elif dateContent == date:
                        indexStart = index
                if dateContent < date:
                    return indexStart, index
            
            else:
                if tagContent[4] == K.NBHY:
                    dateContent = tagContent[0:-2]
                    if indexStart < 0 and dateContent == date:
                        indexStart = indexStartTemp
                
        elif tag.name != 'th':
            isStartOfDiv = False
    return 0, len(dataTags)

def searchBingSpotLight(tag):
    if  tag.has_attr('color'):
        if tag['color'] == 'blue' and tag.string != None:
            return True
        elif tag['color'] == 'darkgreen' or tag['color'] == '#56251F':
            return True
    elif tag.name == 'h2':
        return True
    elif tag.name == 'a' and (tag.has_attr('target') or tag.get('href').find('./SpotLight-') > -1) and tag.get('href').rfind('_1080x1920.jpg') < 0:
        return True

def strainBingPost(tag, attrs):
    if  tag == 'th':
        return True;
    elif 'color' in attrs:
        return attrs['color'] == '#56251F' or attrs['color'] == 'darkgreen' or attrs['color'] == 'green'
    elif tag == 'a' and 'href' not in attrs:
        return True
    elif tag == 'a' and 'href' in attrs:
        link = attrs['href']
        if '.jpg' in link:
            if isLandscape(link):
                return True
            else:
                return True
        else:
            return True
    else:
        return False
        
def strainBingPost_S(tag, attrs):
    if  tag == 'th':
        return True;
    elif tag == 'a' and 'href' in attrs:
        link = attrs['href']
        if link.endswith('.jpg'):
            if isLandscape(link):
                return True
            else:
                return False
        elif link.endswith('.html'):
            return True
        else:
            return False
    else:
        return False
        
def searchBingRandom(tag):
    if  tag.name == 'th':
        return True;
    elif tag.has_attr('color'):
        return tag['color'] == '#56251F' or tag['color'] == 'darkgreen' or (tag['color'] == 'green' and tag.parent.name != 'a')
    elif tag.name == 'a' and not tag.has_attr('href'):
        return True
    elif tag.name == 'a' and tag.has_attr('href'):
        link = tag.get('href')
        if '.jpg' in link:
            #dims = re.search('\d+x\d+', re.search('_\d+x\d+.*\.jpg$', link).group()).group().split('x')
            #if int(dims[0]) > int(dims[1]):
            if isLandscape(link):
                return True
            else:
                return True
        # elif './Random-' in tag.get('href'):
            # if ">" in tag.font.text:
                # return True
            # else:
                # return False
        else:
            return True
    else:
        return False

# urlBing = 'http://www.binghomepagewallpapers.x10host.com'
# dirDest = 'outputBing/'

# urlBingB = 'http://www.binghomepagewallpapers.x10host.com/BingPost-0'
# urlBingR = 'http://www.binghomepagewallpapers.x10host.com/Random-0'
# urlBingS = 'http://www.binghomepagewallpapers.x10host.com/SpotLight-0'

# listImageLink = deque()

# BACKWARD = 0
# FORWARD = 1

# linkCur = ''

def checkLinkNext(linkNext, linkCur, flag):
    if not linkCur:
        return True
    
    if not linkNext[-7:-5].isdecimal():
        return False
    
    if flag:
        return linkNext >= linkCur
    else:
        return linkNext <= linkCur

#flagCrawl = True
#flagDir = FORWARD

# recentBing = {
    # "Post": "",
    # "Random": "",
    # "SpotLight": ""
# }

msgErrValueISO = "Invalid isoformat string"

def isIsoFormat(dateStr):
    try:
        date.fromisoformat(dateStr)
    except ValueError:
        return False
    
    return True

cSet = {'-', K.NBHY}
def formatDateStrISO(dateStr, c):
    if c not in cSet:
        return dateStr
    
    return dateStr[:4] + c + dateStr[5:7] + c + dateStr[8:10]

def isLoaded(listData):
    if len(listData) <= 11:
        return False
    else:
        tag = listData[-1]
        if not tag.has_attr("href"):
            return False
        else:
            link = tag.get("href")
            if not (link.endswith(".html") and (link[-7:-5].isdecimal() or link[-9:-5] == "home")):
                return False
    
    return True
                    
def scrapePost(dateStr, recentPost, flagCrawl, flagDir, fp, session=None):
    if not isIsoFormat(dateStr):
        print("dateStr:", msgErrValueISO)
        return False
    
    dateStr = formatDateStrISO(dateStr, K.NBHY)
    
    n = 1
    maxCount = 12
    
    if flagDir == FORWARD:
        linkNext = './BingPost-01.html'
    else:
        linkNext = './BingPost-20.html'

    linkCur = ''

    #fName = 'BingPost' + str(int(time.time())) +'.txt'
    #fName = destOut + '/' + 'BingPost' + str(n) + '.txt'
    #fName = dirDest + 'BingPostOutput.txt'
    #f = open(fName, 'a', encoding='utf-8')

    #f.write('\n' + datetime.now().strftime('%B %#d, %Y %X') + '\n')

    # resp = requests.head(url)
    # print(resp.headers)

    # headers = {"Range": "bytes=2063-2123"} 
    # resp = requests.get(url, headers=headers)
    # resp.encoding = 'utf-8'
    # print(resp.text)

    # pageMax = resp.text[resp.text.rfind("</i>")-1]
    # print(pageMax)
    
    listImageLink = deque()
    
    while linkNext and checkLinkNext(linkNext, linkCur, flagDir):
        if not flagCrawl:
            url = urlBingB + str(n) + '.html'
        else:
            url = urlBing + linkNext[1:]
        
        if session:
            resp = session.get(url)
        else:
            resp = requests.get(url)
        
        if resp.status_code != 200:
            print(resp.status_code, end="")
            if not resp:
                print(":", linkNext, "Not Found")
                return False
            else:
                print()
        
        resp.encoding = 'utf-8'
        
        # try:
            # text = resp.content.decode('utf-8')
        # except:
            # text = resp.content.decode(resp.apparent_encoding)
        
        linkCur = linkNext
        linkNext = ''
        
        onlyDataTagsWP = SoupStrainer(strainBingPost)
        #page = BeautifulSoup(text, 'html.parser')
        dataTags = BeautifulSoup(resp.text, 'html.parser', parse_only = onlyDataTagsWP)
        if not isLoaded(dataTags.contents):
            print("Cannot access", linkCur)
            return False
        
        #listData = page.find_all(searchBingRandom)
        
        # linkNext = listData.pop().get('href')
        # if flagCrawl and flagDir == BACKWARD:
            # linkNext = listData.pop().get('href')
        # else:
            # del listData[-1]
        # if not flagCrawl:
            # linkNext = ''
        
        i = 0
        count = 0
        #length = len(dataTags)
        #length = findPrevIndImg(recentBing['Post'], dataTags)
        #length = findPrevIndImg('StarWarsSeal', dataTags)
        #length = findPrevIndImg('Alesund', dataTags)
        start, length = getIndexDatePoints(dateStr, dataTags)
        
        iterTags = iter(dataTags)
        tag = next(iterTags)
        i+=1
        
        #while tag.name == 'a':
        while tag.name == 'a' or i < start:
            tag = next(iterTags)
            i+=1
        
        while count < maxCount and i < length:            
            isDate = False
            dateList = []
            
            while tag.name == 'th':
                date = (tag.contents[0])[0:-1]
                if date.startswith(dateStr):
                    isDate = True
                tag = next(iterTags)
                i+=1
                date += (tag.contents[0]).lstrip()
                tag = next(iterTags)
                i+=1
                date = date.replace('\xa0', ' ')
                date = date.replace('‑', '-')
                date = date.replace(' / ', '/')
                date = date.replace(' - ', '-')
                
                dateList.append(date)
            
            if isDate:
                fp.write('\n')
                for date in dateList:
                    fp.write(date+"\n")
            
            title = ''
            while tag.has_attr('color') and tag['color'] != 'darkgreen':
                title = tag.contents[0]
                if len(title) == 2:
                    title += ':'
                else:
                    title = '   '                    
                tag = next(iterTags)
                i+=1
                title += ' '
                tag = next(iterTags)
                i+=1
                title += tag.contents[0]
                tag = next(iterTags)
                i+=1
                if isDate:
                    fp.write(title+"\n")
            
            while tag.name == 'font':
                if isDate:
                    fp.write(tag.contents[0]+"\n")
                tag = next(iterTags)
                i+=1
            
            while tag.name == 'a' and not tag.has_attr('href'):
                if isDate:
                    fp.write(tag.contents[0]["src"][-9:-4] + ": " + tag["title"] + ": " + tag["data-content"] + '\n')
                tag = next(iterTags)
                i+=1
            
            while tag.name == 'a' and (link := tag.get('href')) and link.rfind('.jpg') == -1:
                if isDate:
                    fp.write(link + '\n')
                tag = next(iterTags)
                i+=1
                        
            listImgSize = []
            title = ''
            isOtherSizes = {"logo": False, "UHD": False, "phone": False, "phoneLogo": False}
            while tag.name == 'a' and (link := tag.get('href')) and link.rfind('.jpg') >= 0:
                link =  tag.get('href')
                listImgSize.append(link)
                
                imgEnd = link[-8:-4]
                if isLandscape(link):
                    if imgEnd == "1200":
                        isOtherSizes["logo"] = True
                    elif imgEnd[0].isdigit() and imgEnd > "1200":
                        isOtherSizes["UHD"] = True
                    else:
                        title = link[link.rfind('/')+1:link.rfind('_')]
                else:
                    if imgEnd == "logo":
                        isOtherSizes["phoneLogo"] = True
                    else:
                        isOtherSizes["phone"] = True
                
                # if link.rfind('1080') >= 0:
                    # title = link[link.rfind('/')+1:link.rfind('_')] + ' (no logo)\n'
                # elif link.rfind('1200') >= 0 and listImgSize[0].rfind('1080') >= 0:
                    # title = title[0:-11] + '\n'
                
                tag = next(iterTags)
                i+=1
            
            if isDate:
                urlEnd = "\n"
                if any(isOtherSizes.values()):
                    urlEnd = " (" + ', '.join([size for size, isSize in isOtherSizes.items() if isSize]) + ")" + urlEnd
                fp.write(title + urlEnd)  
            listImageLink.append(listImgSize)
            
            if tag.name == 'a':
                link = tag.get('href')
                try:
                    tag = next(iterTags)
                    i+=1
                            
                    if flagCrawl:
                        if flagDir == FORWARD:
                            linkNext = tag.get('href')
                        else:
                            linkNext = link
                except StopIteration:
                    if flagCrawl:
                        if not ((flagDir == FORWARD) ^ (linkCur[-6] == '1')):
                            linkNext = link
            count+=1
    #f.close()

    # for imgL in reversed(listImageLink):
       # print(imgL)
    
    listPost = recentPost["list"]
    mapping = {k: v for v, k in enumerate(listPost)}
    listImageLink = sorted(listImageLink, key = lambda x: mapping.get(getImageNameFromUrl(x[0]), -1), reverse=True)
    
    # while listImageLink:
        # for imgLink in listImageLink.pop():
            # downloadImage(urlBing + imgLink[1:], dirDest)
    
    return True
    
def collectPost(dateStr, recentPost, flagCrawl, flagDir, session=None):
    if not isIsoFormat(dateStr):
        print("dateStr:", msgErrValueISO)
        return False
    
    dateStr = formatDateStrISO(dateStr, K.NBHY)
    
    n = 1
    
    if flagDir == FORWARD:
        linkNext = './BingPost-01.html'
    else:
        linkNext = './BingPost-20.html'

    linkCur = ''
    
    listCol = deque()
    isPast = False
    
    while linkNext and checkLinkNext(linkNext, linkCur, flagDir):
        if not flagCrawl:
            url = urlBingB + str(n) + '.html'
        else:
            url = urlBing + linkNext[1:]
        
        if session:
            resp = session.get(url)
        else:
            resp = requests.get(url)
        
        if resp.status_code != 200:
            print(resp.status_code, end="")
            if not resp:
                print(":", linkNext, "Not Found")
                return False
            else:
                print()
        
        resp.encoding = 'utf-8'
                
        linkCur = linkNext
        linkNext = ''
        
        onlyDataTags = SoupStrainer(strainBingPost_S)
        dataTags = BeautifulSoup(resp.text, 'html.parser', parse_only = onlyDataTags)
        if not isLoaded(dataTags.contents):
            print("Cannot access", linkCur)
            return False
        
        zLength = len(dataTags) - 1
        
        enumTags = enumerate(dataTags)
        i, tag = next(enumTags)
        
        while tag.name == 'a' and i < zLength:
            i, tag = next(enumTags)
        
        while i < zLength:
            
            isTh = False
            isToday = False
            while tag.name == 'th':
                date = tag.contents[0][:-2]
                if not isTh:
                    isTh = True
                    isPast = date < dateStr                    
                    if isPast:
                        break
                i, tag = next(enumTags)
                
                if date == dateStr:
                    country = min((Bing_Mkt.from_string(s) for s in tag.contents[0].split(K.NBSP + '/ ')))
                    isToday = True
                
                i, tag = next(enumTags)
                                    
            
            if isPast:
                break
            
            link = ''
            while tag.name == 'a' and tag.has_attr('href') and (link := tag.get('href')).endswith('.jpg'):
                if tag.contents[0].name == 'img':
                    if isToday:
                        listCol.appendleft((getImageNameFromUrl(link), country))
                i, tag = next(enumTags)
            
            if tag.name == 'a':
                link = tag.get('href')
                try:
                    i, tag = next(enumTags)
                    if flagCrawl:
                        if flagDir == FORWARD:
                            linkNext = tag.get('href')
                        else:
                            linkNext = link
                except StopIteration:
                    if flagCrawl:
                        if not ((flagDir == FORWARD) ^ (linkCur[-6] == '1')):
                            linkNext = link
    
    listCol = sorted(listCol, key=lambda item: item[1])
    
    listPost = recentPost["list"]
    sPost = set(listPost)
    listPost.extend(item[0] for item in listCol if item[0] not in sPost)
    
    return True

def printPost(recentPost, fp):
    listPost = recentPost["list"]
    
    fp.write('\n')
    for post in reversed(listPost):
        fp.write(post + '\n')

def urlBingJson(qFormat, qIdx, qN, qMkt):
    return 'https://www.bing.com/HPImageArchive.aspx' + '?format=' + qFormat + '&idx=' + str(qIdx) + '&n=' + str(qN) + '&mkt=' + qMkt

tzToday = tz.tzlocal()
#tzToday = tz.gettz('America/Los_Angeles')
#bingMkt = [('zh-cn', 'en'), ('fr-ca', 'fr')]
bingMkt = ("en-ww", "pt-br", "en-ca", "fr-ca", "zh-cn", "en-cn", "fr-fr", "de-de", "en-in", "it-it", "ja-jp", "es-es", "en-gb", "en-us")
def jsonPost(dateStr, fp, session, todayStr=None):
    if not todayStr:
        today = datetime.now(tz=tzToday).date()
    else:
        if not isIsoFormat(todayStr):
            print("todayStr:", msgErrValueISO)
            return
        
        today = date.fromisoformat(todayStr)
    
    if not isIsoFormat(dateStr):
        print("dateStr:", msgErrValueISO)
        return
    
    dateISO = date.fromisoformat(dateStr)
    
    days = (today - dateISO).days
    if (days < 0) or (days > 14):
        return
    
    xI = max(days-7, 0)
    xN = min(1+days, 8)
    
    cookiesDict = {}
    if session:
        for cookie in iter(session.cookies):
            cookiesDict[cookie.name] = cookie
    
    for mkt in bingMkt:
        urlJson = urlBingJson('js', xI, xN, mkt)
        #urlJson = urlBingJson('js', xI, xN, mkt[0])
        #r = s.get('https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-cn')
        
        if session:
            if mkt == "zh-cn": cookiesDict["ENSEARCH"].value = "BENVER=0"
            r = session.get(urlJson)
            if mkt == "zh-cn": cookiesDict["ENSEARCH"].value = "BENVER=1"
        else:
            jar = requests.cookies.RequestsCookieJar()
            val = "BENVER=1" if mkt != "zh-cn" else "BENVER=0"
            jar.set("ENSEARCH", val, domain="bing.com", path="/HPImageArchive.aspx")
            r = requests.get(urlJson, cookies=jar)
        
        if r.status_code != 200:
            print(r.status_code + ": JSON not found")
            break
        
        j = json.loads(r.text)
        
        fp.write('\n')
        image = j['images'][xN-1]
        urlBase = image['urlbase']
        name = urlBase[11:urlBase.find('_', 12)]
        title = image['copyright']
        iSep = title.rfind(" (", 0, title.rfind('©'))
        pid = urlBase[urlBase.rfind('_')+1:]
        hsh = image['hsh']
        
        fp.write(mkt + '\n')
        fp.write(mkt[:2] + ': ')
        fp.write(title[:iSep] + '\n')
        fp.write(title[iSep+1:] + '\n')
        fp.write(name + '\n')
        fp.write(pid + '\n')
        fp.write(hsh + '\n')


# resp = sess.get("http://binghomepagewallpapers.x10host.com/SpotLight-04.html")
# if resp.status_code != 200:
    # print(resp.status_code + ': Page Not Found')
    # sys.exit()
        
# resp.encoding = 'utf-8'
    
# page = BeautifulSoup(resp.text, 'html.parser')
# if len(page) == 0:
    # sys.exit()

# def searchTest(tag):
    # if tag.name == "h2":
        # return True;
    # elif tag.name == "font" and tag.has_attr("color") and tag["color"] == "#56251F":
        # return True
    # else:
        # return False

# font = iter(page.find_all(searchTest))
# tag = next(font)

# while tag.name != "h2" or tag.string != "Western Australia":
    # tag = next(font)

# print(tag)
# text = next(font)
# print(text)

# contents = iter(text.contents)
# c = next(contents)

# while c.name != "i":
    # c = next(contents)

# print(c)
# print(*c, sep="\n")
# sys.exit()

def strTagToFStr(strTag, mList, tSet, flags=[False]):
    s = ""
    
    for c in strTag:
        if not isinstance(c, str):
            t = c.name
            
            if t == 'br':
                c = '\n'
            else:
                if t == 'a':
                    mList.append(c.get('href'))
                elif t == 'i':
                    pass
                
                end = "\\" + t.upper()
                
                p = ""
                if t in tSet:
                    p = end
                    flags[0] = True
                
                tSet.add(t)
                f = [False]                
                c = p + "\\" + t + strTagToFStr(c, mList, tSet, f)
                
                if not f[0]:
                    c += end
                    tSet.remove(t)
        s += c
    
    return s

def fStrToStr(fStr):
    return re.sub(r"\\[a-z]", "", fStr, flags=re.I)

def test_strTagToFStr(html):
    strTag = BeautifulSoup(html, 'html.parser')
    
    mList = []
    tSet = {strTag.name}
    
    for c in strTag:
        #print(c)
        s = strTagToFStr(c, mList, tSet)
    
    print('\n' + s)
    print(*mList, sep='\n')
    return s, mList

# text = "<font color=\"#56251F\">The very first performance held at Harpa Concert Hall in <a href=\"https://www.bing.com/search?q=reykjavik+iceland&amp;form=wsbs03\">Reykjavík, <a href=\"https://www.bing.com/search?q=iceland&amp;form=wsbs03\">Iceland</a>, might never have happened if the government hadn’t stepped in to fund the  construction. Work began on Harpa in 2007, but the financial crisis hit Iceland a year later, and the build was put on hold. While plans for additional office structures and a luxury hotel were abandoned, tax revenues covered the tab for the concert hall, which was finally completed in 2011. Home to the Iceland Symphony Orchestra and the Icelandic Opera, the concert hall won the 2013 <a href=\"https://www.bing.com/search?q=mies+van+der+rohe&amp;form=wsbs03\">Mies van der Rohe</a> Award, the European Union’s prize for contemporary architecture.</a></font>"
# s0, mList0 = test_strTagToFStr(text)

# s = fStrToStr(s0)
# print('\n' + s)

# text = "<font color=\"#56251F\">The very first performance held at Harpa Concert Hall in <a href=\"https://www.bing.com/search?q=reykjavik+iceland&amp;form=wsbs03\">Reykjavík, </a><a href=\"https://www.bing.com/search?q=iceland&amp;form=wsbs03\">Iceland</a>, might never have happened if the government hadn’t stepped in to fund the  construction. Work began on Harpa in 2007, but the financial crisis hit Iceland a year later, and the build was put on hold. While plans for additional office structures and a luxury hotel were abandoned, tax revenues covered the tab for the concert hall, which was finally completed in 2011. Home to the Iceland Symphony Orchestra and the Icelandic Opera, the concert hall won the 2013 <a href=\"https://www.bing.com/search?q=mies+van+der+rohe&amp;form=wsbs03\">Mies van der Rohe</a> Award, the European Union’s prize for contemporary architecture.</font>"
# s1, mList1 = test_strTagToFStr(text)  

# print('\n' + str(s == fStrToStr(s1)))

# text = "<font color=\"#56251F\">The very first performance held at Harpa Concert Hall in <a href=\"https://www.bing.com/search?q=reykjavik+iceland&amp;form=wsbs03\">Reykjavík, <a href=\"https://www.bing.com/search?q=iceland&amp;form=wsbs03\">Iceland</a>, might never have happened if the government hadn’t stepped in to fund the  construction. Work began on Harpa in 2007, but the financial crisis hit Iceland a year later, and the build was put on hold. While plans for additional office structures and a luxury hotel were abandoned, tax revenues covered the tab for the concert hall, which was finally completed in 2011. Home to the Iceland Symphony Orchestra and the Icelandic Opera, the concert hall won the 2013 <a href=\"https://www.bing.com/search?q=mies+van+der+rohe&amp;form=wsbs03\">Mies van der Rohe Award, the European Union’s prize for contemporary architecture.</a></a></font>"
# s2, mList2 = test_strTagToFStr(text) 

# text = "<font color=\"#56251F\">The trees lining the roadway in our image are <i><a href=\"https://www.bing.com/search?q=eucalyptus+diversicolors&amp;form=wsbs03\">Eucalyptus diversicolors</a>—</i>more widely known as karri trees. Karris are common around the wetter southern regions of <a href=\"https://www.bing.com/search?q=western+australia&amp;form=wsbs03\">Western Australia</a>. They're the tallest trees in the state, and among the tallest in the world. Some of these soaring eucalyptus trees are said to reach up to a whopping 295 feet high. Only one-fifth of virgin karri forest growth remains, and a series of national parks have been established, in part, to protect the extraordinary groves of giants. The ribbon of road we see here runs through a portion of <a href=\"https://www.bing.com/search?q=greater+beedelup+national+park&amp;form=wsbs03\">Greater Beedelup National Park</a>, a nature reserve that also features a <a href=\"https://www.bing.com/images/search?q=beedelup+falls+western+australia&amp;form=wsbs03\">scenic waterfall</a> nestled among the trees.</font>"
# s3, mList3 = test_strTagToFStr(text)

# fName = dirDest + 'BingSpotLightOutput.txt'
# f = open(fName, 'a', encoding='utf-8')
# f.write('\n' + s3 + '\n')
# for m in mList3:
    # f.write(m + '\n')
# f.close()

# text = "<font color=\"#56251F\">s0 <a href=\"h0\">a0</a> s1 <a href=\"h1\">a1</a> s2 <a href=\"h2\">a2</a> s3</font>"
# text = "<font color=\"#56251F\">s0 <a href=\"h0\">a0 s1 <a href=\"h1\">a1</a> s2 <a href=\"h2\">-<a href=\"h\">a2</a>-</a> s3</font>"
# sT, mListT = test_strTagToFStr(text)
# print('\n' + fStrToStr(sT))

# sys.exit()

# i=0
# for tag in listTags:
    # if i == indStop+12:
        # print(tag.text == ' ')
        # break
    # i+=1
    
#print(*listTags, sep='\n')
#ParanalStars

# listTest = ['a','b','c','d','e']
# iterTest = iter(listTest)

# next(iterTest)
# next(iterTest)

# listTest[2] = 'f'

# for i in iterTest:
    # print(i)
# sys.exit()

# teststr = "<font color=\"#56251F\">The very first performance held at Harpa Concert Hall in <a href=\"https://www.bing.com/search?q=reykjavik+iceland&amp;form=wsbs03\">Reykjavík, </a><a href=\"https://www.bing.com/search?q=iceland&amp;form=wsbs03\">Iceland</a>, might never have happened if the government hadn’t stepped in to fund the  construction. Work began on Harpa in 2007, but the financial crisis hit Iceland a year later, and the build was put on hold. While plans for additional office structures and a luxury hotel were abandoned, tax revenues covered the tab for the concert hall, which was finally completed in 2011. Home to the Iceland Symphony Orchestra and the Icelandic Opera, the concert hall won the 2013 <a href=\"https://www.bing.com/search?q=mies+van+der+rohe&amp;form=wsbs03\">Mies van der Rohe</a> Award, the European Union’s prize for contemporary architecture.</font>"
# tstr = BeautifulSoup(teststr, 'html.parser')
# #print(tstr)
# #t = next(iter(tstr))
# t = tstr.find('font')
# t = iter(t.contents)
# print(next(t))
# # for c in t.contents:
    # # print(c)
# sys.exit()

# s = requests.session()
# s.cookies.set("ENSEARCH", "BENVER=1", domain="bing.com")

# r = s.get('https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-cn')

# print(r.text)

# d0 = datetime(year=2021, month=5, day=31, hour=3, minute=0, second=0)
# d1 = datetime(year=2021, month=6, day=1, hour=2, minute=59, second=59)

# dt = d1-d0
# print(str(dt))
# print(repr(dt))

# print(dt.days)

# s.close()
#sys.exit()

# def testSpotLight():
    # fName = dirDest + 'BingSpotLightOutput.txt'
    # f = open(fName, 'a', encoding='utf-8')

    # f.write('\n' + datetime.now().strftime('%B %#d, %Y %X') + '\n')
    
    # f.write('\n')
    # f.write('Underneath the Pont de la Concorde in Paris, France\n')
    # f.write('(© BRENAC PHOTOGRAPHY/500px )\n')
    # f.write('Tons of traffic rolls over this arch bridge connecting the Right Bank and Left Bank in Paris. If you were down here below the bridge and floating on the \\Seine\\ with the photographer, you’d hear the rumble above. But listen even closer and you might hear the echo of history. Building began on the Pont de la Concorde in 1787 and not even the \\French Revolution\\, which erupted two years later, could stop this span. In fact, stones from the dismantled Bastille (a loathed Paris fortress and prison destroyed by revolutionaries in 1789) were used in the bridge’s construction. We can almost hear the sounds of hooves and carriage wheels now.\n')
    # f.write('https://www.bing.com/search?q=Seine+River&form=wsbs03\n')
    # f.write('https://www.bing.com/search?q=French+Revolution&form=wsbs03\n')
    # f.write('https://www.bing.com/images//search?q=Concorde+Bridge+Paris+France&filters=IsConversation:%22True%22+BTWLKey:%22ConcordeBridgeParisFrance%22+BTWLType:%22Trivia%22&trivia=0&form=EMSDS0&first=1&tsc=ImageHoverTitle\n')
    # f.write('https://www.bing.com/maps?q=Concorde+Bridge+Paris+France&FORM=HDRSC4\n')
    # f.write('ConcordeBridgeParisFrance\n')
    
    # f.write('\n')
    # f.write('Garni Gorge, Armenia\n')
    # f.write('(© Photography Aubrey Stoll / Moment / Getty Images)\n')
    # f.write('Although the views from a distance are stellar, the real treasures of Garni Gorge are revealed only by a deeper exploration. Within this river-carved canyon in central \\Armenia\\ are cliffs known as the \'\\Symphony of the Stones\\.\' Massive basalt columns stand out from hill faces in neat, soaring rows, resembling the ranks of pipe organs. Standing atop a nearby promontory is something equally spectacular, but this time it\'s human-made. Believed to have been paid for by \\Emperor Nero\\, the \\Temple of Garni\\ dates back more than 2,000 years and is Armenia\'s only standing \\Greco-Roman\\ colonnaded building. Toppled by an earthquake in 1679, the temple was rebuilt using mostly original materials in 1975.\n')
    # f.write('https://www.bing.com/search?q=armenia&form=wsbs03\n')
    # f.write('https://www.bing.com/images/search?q=symphony+of+stones+garni+armenia&form=wsbs03\n')
    # f.write('https://www.bing.com/search?q=emperor+nero&form=wsbs03\n')
    # f.write('https://www.bing.com/search?q=temple+of+garni+armenia&form=wsbs03\n')
    # f.write('https://www.bing.com/search?q=greco-roman+world&form=wsbs03\n')
    # f.write('https://www.bing.com//images//search?q=symphony+of+stones+garni+armenia&filters=IsConversation:%22True%22+BTWLKey:%22GarniGorgeArmenia%22+BTWLType:%22Trivia%22&trivia=0&qft=+filterui:photo-photo&FORM=EMSDS0\n')
    # f.write('https://www.bing.com/maps?osid=28e95b8f-f7bd-4ed6-9cfc-0bd89e9e6fa7&cp=43.777853~29.166838&lvl=4&style=h&imgid=f38b5e82-63bb-4e4c-9373-ad449bee3bc2&v=2&sV=2&form=wsbs02\n')
    # f.write('GarniGorgeArmenia\n')
    
    # f.write('\n')
    # f.write('Windows of the Harpa Concert Hall in Reykjavík, Iceland\n')
    # f.write('(© Fexel / Adobe Stock)\n')
    
    # text = "<font color=\"#56251F\">The very first performance held at Harpa Concert Hall in <a href=\"https://www.bing.com/search?q=reykjavik+iceland&amp;form=wsbs03\">Reykjavík, <a href=\"https://www.bing.com/search?q=iceland&amp;form=wsbs03\">Iceland</a>, might never have happened if the government hadn’t stepped in to fund the  construction. Work began on Harpa in 2007, but the financial crisis hit Iceland a year later, and the build was put on hold. While plans for additional office structures and a luxury hotel were abandoned, tax revenues covered the tab for the concert hall, which was finally completed in 2011. Home to the Iceland Symphony Orchestra and the Icelandic Opera, the concert hall won the 2013 <a href=\"https://www.bing.com/search?q=mies+van+der+rohe&amp;form=wsbs03\">Mies van der Rohe</a> Award, the European Union’s prize for contemporary architecture.</a></font>"
    # font = BeautifulSoup(text, 'html.parser').find('font')
    
    # markList = []
    # s = ''
    # contents = iter(font.contents)
    # tempC = []
    # while contents:            
        # for c in contents:
            # if not isinstance(c, str):
                # if c.name == 'br':
                    # c = '\n'
                # else:
                    # if c.name == 'a':
                        # mark = c.get('href')
                    # elif c.name == 'i':
                        # mark = '(i)'
                    
                    # tempC = c.contents
                    # c = c.contents[0]
                    # if not isinstance(c, str):
                        # mark = mark + ' (i)'
                        
                        # tempC = c.contents
                        # c = c.contents[0]
                    # markList.append(mark)
                    # c = '\\' + c + '\\'
            # s = s + c
            # if len(tempC) > 1:
                # tempC = iter(tempC)
                # next(tempC)
                # break
        # else:
            # tempC = None
            
        # contents = tempC
        # tempC = []
        
    # f.write(s + '\n')
    # for mark in markList:
        # f.write(mark + '\n')
            
    # f.write('https://www.bing.com/images//search?q=Harpa+Concert+Hall+Reykjavik+Iceland&filters=IsConversation:%22True%22+BTWLKey:%22HarpaReykjavikIceland%22+BTWLType:%22Trivia%22&trivia=0&form=EMSDS0&first=1&tsc=ImageHoverTitle\n')
    # f.write('https://www.bing.com/maps?q=Harpa+Concert+Hall+Reykjavik+Iceland&FORM=HDRSC4\n')
    # f.write('HarpaReykjavikIceland\n')
    
    # f.close()
# testSpotLight()
# sys.exit()

#listPost = ['AnnularEclipse', 'XenoBlade']
#collectPost("2021‑06‑10", listPost)
#print(listPost)
#sys.exit()

# flagCrawl = True
# flagDir = FORWARD

# recentBing["Post"] = "HartlandPoint"
# recentBing["Random"] = "ChapecoenseSupporters"
# recentBing["SpotLight"] = "LavaCliffsCanaryIslands"

# # with open('wsBingCache.json', 'r') as fR:
    # # recentBing = json.load(fR)
    
# # temp = recentBing["Post"]
# # recentBing["Post"] = {"time" : "", "list": []}
# # recentBing["Post"]["time"] = temp

# # with open('wsBingCache.json', 'w') as fW:
    # # json.dump(recentBing, fW, indent=4)

# # sys.exit()

# # session = None
# # session = requests.Session()
# # session.cookies.set("ENSEARCH", "BENVER=1", domain="bing.com", path="/HPImageArchive.aspx")

# # print(s.cookies)
# # jar = requests.cookies.RequestsCookieJar()
# # jar.set("ENSEARCH", "BENVER=1", domain="bing.com", path="/HPImageArchive.aspx")
# # r=requests.get('https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-cn', cookies=jar)
# # print(json.loads(r.text))
# # sys.exit()

# # print(datetime.now(tz=tzToday).tzname())
# # sys.exit()

# # fName = dirDest + 'BingPostOutput.txt'
# # with open(fName, 'a', encoding='utf-8') as fp:
    # # #fp.write('\n' + 'June 14, 2021 03:21:43' + '\n')
            
    # # #printPost(["SpiritMaligne", "DragonBoatFestival2021", "LavenderBlooms", "LargestFlag"], fp)
    # # jsonPost('2021-06-14', fp, s)
# # sys.exit()
 
# with open('wsBingCache.json', 'r') as fR:
    # recentBing = json.load(fR)

# #tzPST = timezone(timedelta(hours=-8), 'PST')
# #tzPDT = timezone(timedelta(hours=-7), 'PDT')
# #tzNow = tzPDT
# tzNow = tz.tzlocal()
# #yesterday = timedelta(days=-1)
# tomorrow = timedelta(days=1)

# #present = datetime.now(timezone) + yesterday
# #present = datetime.now(tzPDT)

# recentPost = recentBing["Post"]

# timestamp = datetime.fromisoformat(recentPost["time"])
# dateStr = timestamp.strftime('%Y-%m-%d')
# #dateStr = dateStr[:4] + nbhy + dateStr[5:7] + nbhy + dateStr[8:10]

# # fName = dirDest + 'BingPostOutput.txt'
# # with open(fName, 'a', encoding='utf-8') as fp:
    # # fp.write('\n' + datetime.now().strftime('%B %#d, %Y %X') + '\n')
    # # scrapePost(dateStr, fp, session)
# # sys.exit()

# collectPost(dateStr, recentPost, flagCrawl, flagDir, session)

# if datetime.now(tzNow) >= timestamp:
    # #dateStr = timestamp.strftime('%Y‑%m‑%d')
    # #dateStr = dateStr.replace('-', '‑')
    
    # fName = dirDest + 'BingPostOutput.txt'
    # with open(fName, 'a', encoding='utf-8') as fp:
        # fp.write('\n' + datetime.now().strftime('%B %#d, %Y %X') + '\n')
            
        # printPost(recentPost, fp)
        # jsonPost(dateStr, fp, session)
    
        # scrapePost(dateStr, recentPost, flagCrawl, flagDir, fp, session)
    
    # timestamp += tomorrow
    # recentBing["Post"]["time"] = timestamp.isoformat()
    
    # recentBing["Post"]["list"] *= 0
    

# #sys.exit()

def scrapeSpotLight(recentSpotLight, flagCrawl, flagDir, fp, session=None):
    n = 1
    maxCount = 10
    
    if flagDir == FORWARD:
        linkNext = './SpotLight-01.html'
    else:
        linkNext = './SpotLight-05.html'
    
    linkCur = ''
    
    #fName = 'BingSpotLight' + str(int(time.time())) +'.txt'
    #fName = destOut + '/' + 'BingSpotLight' + str(n) + '.txt'
    #fName = dirDest + 'BingSpotLightOutput.txt'
    #fp = open(fName, 'a', encoding='utf-8')
    
    #fp.write('\n' + datetime.now().strftime('%B %#d, %Y %X') + '\n')
    
    # resp = requests.head(url)
    # print(resp.headers)
    
    # headers = {"Range": "bytes=2063-2123"} 
    # resp = requests.get(url, headers=headers)
    # resp.encoding = 'utf-8'
    # print(resp.text)
    
    # pageMax = resp.text[resp.text.rfind("</i>")-1]
    # print(pageMax)
    
    listImageLink = deque()
    markList = []
    tagSet = {"font"}
    
    while linkNext and checkLinkNext(linkNext, linkCur, flagDir):
        if not flagCrawl:
            url = urlBingS + str(n) + '.html'
        else:
            url = urlBing + linkNext[1:]
        
        if session:
            resp = session.get(url)
        else:
            resp = requests.get(url)
        
        if resp.status_code != 200:
            print(resp.status_code, end="")
            if not resp:
                print(":", linkNext, "Not Found")
                return False
            else:
                print()
        
        resp.encoding = 'utf-8'
        linkCur = linkNext
        
        page = BeautifulSoup(resp.text, 'html.parser')
        
        listData = page.find_all(searchBingSpotLight)
        if not isLoaded(listData):
            print("Cannot access", linkCur)
            return
        
        linkNext = listData.pop().get('href')
        if flagCrawl and flagDir == BACKWARD:
            linkNext = listData.pop().get('href')
        else:
            del listData[-1]
        if not flagCrawl:
            linkNext = ''
        # if not flagCrawl:
            # linkNext = ''
            # del listData[-1]
        # elif flagDir == FORWARD:
            # del listData[-1]
        # else:
            # linkNext = listData.pop().get('href')
        print(linkNext)
        
        i = 0
        count = 0
        #length = len(listData)
        length = findPrevIndImg(recentSpotLight["image"], listData)
        #length = findPrevIndImg('BodrumTurkey', listData)
        
        if length < len(listData):
            linkNext = ''
        
        while count < maxCount and i < length:
            fp.write('\n')
            
            #for x in range(3):
            # for x in range(2):
                # if (listData[i].name == 'font' and listData[i]['color'] == '#56251F'):
                    # break
            #while not (listData[i].has_attr('color') and listData[i].get('color').find('#56251F') > -1)
                #fp.write(listData[i].contents[0] + '\n')
                #i+=1
                
            while not ((listData[i].name == 'font' and listData[i]['color'] == '#56251F') or listData[i].has_attr('href')):
                fp.write(listData[i].contents[0] + '\n')
                i+=1
            
            if not listData[i].has_attr('href'):
                s = strTagToFStr(listData[i], markList, tagSet)
                
                # s = ''
                # contents = iter(listData[i].contents)
                # tempC = []
                # while contents:            
                    # for c in contents:
                        # if not isinstance(c, str):
                            # if c.name == 'br':
                                # c = '\n'
                            # else:
                                # if c.name == 'a':
                                    # mark = c.get('href')
                                # elif c.name == 'i':
                                    # mark = '(i)'
                                
                                # tempC = c.contents
                                # c = c.contents[0]
                                # if not isinstance(c, str):
                                    # if c.name == 'a':
                                        # mark = mark + ' ' + c.get('href')
                                    # elif c.name == 'i':
                                        # mark += ' (i)'
                                    
                                    # tempC = c.contents
                                    # c = c.contents[0]
                                # markList.append(mark)
                                # c = '\\' + c + '\\'
                        # s += c
                        # if len(tempC) > 1:
                            # tempC = iter(tempC)
                            # next(tempC)
                            # break
                    # else:
                        # tempC = None
                        
                    # contents = tempC
                    # tempC = []
                    
                fp.write(s + '\n')
                for mark in markList:
                    fp.write(mark + '\n')
                markList *= 0
                i+=1
            
            while listData[i].has_attr('href'):
                link =  listData[i].get('href')
                
                if link.find('_1920x1080.jpg') != -1:
                    listImageLink.append(link)
                    link = link[link.rfind('/')+1:link.find('_')]
                
                if link[0] == '.':
                    link = urlBing + link[1:]
                fp.write(link+ '\n')
                i+=1
                
                if i == length:
                    break
            # if i != length:
                # fp.write("\n")
            count+=1
    #fp.close()

    # for imgL in reversed(listImageLink):
       # print(imgL)
    
    if listImageLink:
        recentSpotLight["image"] = getImageNameFromUrl(listImageLink[0])
    
    # while listImageLink:
        # downloadImage(urlBing + listImageLink.pop()[1:], dirDest)
    
    #listImageLink *= 0

def scrapeRandom(recentRandom, flagCrawl, flagDir, fp, session=None):
    n = 1
    maxCount = 10

    if flagDir == FORWARD:
        linkNext = './Random-01.html'
    else:
        linkNext = './Random-05.html'

    linkCur = ''

    #fName = 'BingRandom' + str(int(time.time())) +'.txt'
    #fName = destOut + '/' + 'BingRandom' + str(n) + '.txt'
    #fName = dirDest + 'BingRandomOutput.txt'
    #fp = open(fName, 'a', encoding='utf-8')
    
    #fp.write('\n' + datetime.now().strftime('%B %#d, %Y %X') + '\n')
    
    # resp = requests.head(url)
    # print(resp.headers)
    
    # headers = {"Range": "bytes=2063-2123"} 
    # resp = requests.get(url, headers=headers)
    # resp.encoding = 'utf-8'
    # print(resp.text)
    
    # pageMax = resp.text[resp.text.rfind("</i>")-1]
    # print(pageMax)
    
    listImageLink = deque()
    
    while linkNext and checkLinkNext(linkNext, linkCur, flagDir):
        if not flagCrawl:
            url = urlBingR + str(n) + '.html'
        else:
            url = urlBing + linkNext[1:]
        
        if session:
            resp = session.get(url)
        else:
            resp = requests.get(url)
        
        if resp.status_code != 200:
            print(resp.status_code, end="")
            if not resp:
                print(":", linkNext, "Not Found")
                return False
            else:
                print()
        
        resp.encoding = 'utf-8'
        linkCur = linkNext
        
        page = BeautifulSoup(resp.text, 'html.parser')
        
        listData = page.find_all(searchBingRandom)
        if not isLoaded(listData):
            print("Cannot access", linkCur)
            return
        
        linkNext = listData.pop().get('href')
        if flagCrawl and flagDir == BACKWARD:
            linkNext = listData.pop().get('href')
        else:
            del listData[-1]
        if not flagCrawl:
            linkNext = ''
        # if not flagCrawl:
            # linkNext = ''
            # del listData[-1]
        # elif flagDir == FORWARD:
            # del listData[-1]
        # else:
            # linkNext = listData.pop().get('href')
        print(linkNext)
        
        i = 0
        count = 0
        #length = len(listData)
        length = findPrevIndImg(recentRandom["image"], listData)
        #length = findPrevIndImg('JapanHitachinaka', listData)
        
        if length < len(listData):
            linkNext = ''
        
        while count < maxCount and i < length:
            fp.write('\n')
            
            while listData[i].name == 'th':
                date = (listData[i].contents[0])[0:-1]
                i+=1
                date += (listData[i].contents[0]).lstrip()
                i+=1
                date = date.replace('\xa0', ' ')
                date = date.replace('‑', '-')
                date = date.replace(' / ', '/')
                date = date.replace(' - ', '-')
                fp.write(date+"\n")
            
            # while listData[i].has_attr('color'):
                # fp.write(listData[i].contents[0]+"\n")
                # i+=1
            
            title = ''
            while listData[i].has_attr('color') and listData[i]['color'] != 'darkgreen':
                title = listData[i].contents[0]
                if len(title) == 2:
                    title += ':'
                else:
                    title = '   '
                i+=1
                title += ' '
                i+=1
                title += listData[i].contents[0]
                i+=1
                fp.write(title+"\n")
            
            while listData[i].name == 'font' and i < len(listData) :
                fp.write(listData[i].contents[0]+"\n")
                i+=1
            
            while (not listData[i].has_attr('href') and i < len(listData) and listData[i].name != 'th'):
                tag = listData[i]
                fp.write(tag.contents[0]["src"][-9:-4] + ": " + tag["title"] + ": " + tag["data-content"] + '\n')
                i+=1
            
            while listData[i].has_attr('href') and (link :=  listData[i].get('href')) and link[-4:] != '.jpg' and i < len(listData) and listData[i].name != 'th':
                fp.write(link + '\n')
                i+=1
            
            listImgSize = []
            imgUrl = ""
            isOtherSizes = {"logo": False, "UHD": False, "phone": False, "phoneLogo": False}
            while listData[i].has_attr('href') and i < len(listData) and listData[i].name != 'th':
                # link = listData[i].get('href')
                # if link.rfind('.jpg') > -1:
                    # listImgSize.append(link)
                    
                    # if link.rfind('1200') > -1 and listImgSize[0].rfind('1080') > -1:
                        # fp.write(urlBing + link[1:] + "\n")
                        # #pass
                    # else:
                        # fp.write(urlBing + link[1:] + "\n")
                # else:
                    # fp.write(link + '\n')
                link = listData[i].get('href')
                listImgSize.append(link)
                
                imgEnd = link[-8:-4]
                if isLandscape(link):
                    if imgEnd == "1200":
                        isOtherSizes["logo"] = True
                    elif imgEnd[0].isdigit() and imgEnd > "1200":
                        isOtherSizes["UHD"] = True
                    else:imgUrl = urlBing + link[1:]
                else:
                    if imgEnd == "logo":
                        isOtherSizes["phoneLogo"] = True
                    else:
                        isOtherSizes["phone"] = True
                # if link.find('1920x1080.jpg') != -1:
                    # #link = link[link.rfind('/')+1:link.find('_')]
                    # if i != length-1 and listData[i+1].has_attr('href'):
                        # if listData[i+1].get('title').find('logo') != -1:
                            # listImageLink.append(listData[i+1].get('href'))
                            # i+=1
                        # #else:
                            # #link = link + ' (no logo)'
                        
                # if link[0] == '.':
                    # listImageLink.append(link)
                    # link = urlBing + link[1:]
                # fp.write(link+"\n")
                i+=1
                
                if i == length:
                    break
            
            urlEnd = "\n"
            if any(isOtherSizes.values()):
                urlEnd = " (" + ', '.join([size for size, isSize in isOtherSizes.items() if isSize]) + ")" + urlEnd
            fp.write(imgUrl + urlEnd)
            
            if listImgSize:
                listImageLink.append(listImgSize)
            # if i != length:
                # fp.write("\n")
            count+=1
    #fp.close()
    
    # for imgL in reversed(listImageLink):
       # print(imgL)
    
    if listImageLink:
        recentRandom["image"] = getImageNameFromUrl(listImageLink[0][0])
    
    # while listImageLink:
        # for imgLink in listImageLink.pop():
            # downloadImage(urlBing + imgLink[1:], dirDest)
    
    return True

# with open('wsBingCache.json', 'w') as fW:
    # json.dump(recentBing, fW, indent=4)

# sys.exit()

urlBing = 'http://www.binghomepagewallpapers.x10host.com'
dirDest = 'outputBing/'

urlBingB = 'http://www.binghomepagewallpapers.x10host.com/BingPost-0'
urlBingR = 'http://www.binghomepagewallpapers.x10host.com/Random-0'
urlBingS = 'http://www.binghomepagewallpapers.x10host.com/SpotLight-0'

BACKWARD = 0
FORWARD = 1

def scrapeBing(session=None):
    flagCrawl = True
    flagDir = FORWARD
    
    fName = "wsBingCache.json"
    with open(fName, "r") as fR:
        recentBing = json.load(fR)
    
    recentPost = recentBing["Post"]
    
    timestamp = datetime.fromisoformat(recentPost["time"])
    dateStr = timestamp.strftime('%Y-%m-%d')
    
    #tzPST = timezone(timedelta(hours=-8), 'PST')
    #tzPDT = timezone(timedelta(hours=-7), 'PDT')
    #tzNow = tzPDT
    tzNow = tz.tzlocal()
    #yesterday = timedelta(days=-1)
    tomorrow = timedelta(days=1)
    
    status = False
    
    collectPost(dateStr, recentPost, flagCrawl, flagDir, session)
    
    if datetime.now(tzNow) >= timestamp:
        fName = dirDest + "BingPostOutput.txt"
        with open(fName, "a", encoding="utf-8") as fp:
            fp.write('\n' + datetime.now().strftime('%B %#d, %Y %X') + '\n')
            
            printPost(recentPost, fp)
            jsonPost(dateStr, fp, session)
            
            status = scrapePost(dateStr, recentPost, flagCrawl, flagDir, fp, session)
        
        if status:
            timestamp += tomorrow
            recentPost["time"] = timestamp.isoformat()
        
            recentPost["list"] *= 0
    
    recentRandom = recentBing["Random"]
    fName = dirDest + "BingRandomOutput.txt"
    with open(fName, "a", encoding="utf-8") as fp:
        fp.write('\n' + datetime.now().strftime('%B %#d, %Y %X') + '\n')
        scrapeRandom(recentRandom, flagCrawl, flagDir, fp, session)
    
    recentSpotLight = recentBing["SpotLight"]
    fName = dirDest + "BingSpotLightOutput.txt"
    with open(fName, "a", encoding="utf-8") as fp:
        fp.write('\n' + datetime.now().strftime('%B %#d, %Y %X') + '\n')
        scrapeSpotLight(recentSpotLight, flagCrawl, flagDir, fp, session)
    
    fName = "wsBingCache.json"
    with open(fName, 'w') as fW:
        json.dump(recentBing, fW, indent=4)
        
def setUpSession(session):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0'}
    session.headers.update(headers)
    session.cookies.set("ENSEARCH", "BENVER=1", domain="bing.com", path="/HPImageArchive.aspx")
    
def main():
    with requests.Session() as session:
        setUpSession(session)
        scrapeBing(session)

if __name__ == "__main__":
    main()
    