import urllib
import tkinter as tk
import time
import codecs
import csv
from bs4 import BeautifulSoup
import re
from fuzzywuzzy import fuzz


def writeTestResults(string):
    """used for writing test outputs to a test file - not a key part of the script """
    testOut = 'testOut.txt'
    with codecs.open(testOut, 'w', 'utf-8') as x:
        x.write(string)

def getCommonWords():
    with open('commonWords.txt') as f:
        lines = f.read().splitlines()

    commonWords = []
    for word in lines:
        commonWords.append(word.upper())
    return commonWords

def getDatabaseList():
    databaseList = 'zeroTitleDatabases.csv'
    with open(databaseList, 'r') as f:
        reader = csv.reader(f)
        databases = list(reader)
    return databases

def writeResults(exportResults):
    outputFile = 'results.csv'
    with codecs.open(outputFile, 'a', encoding='utf-8') as out:
        a = csv.writer(out, delimiter=',', quoting=csv.QUOTE_ALL)
        a.writerows(exportResults)

def extractResults(pageSource):
    if 'No Packages</strong> Found. Please revise your search and review your filter selections' in pageSource:
        dbs = [[0,'No Results']]
        return dbs

    soup = BeautifulSoup(pageSource, 'html.parser')
    td = soup.find_all('td')
    p = soup.find_all(href=re.compile('packageDetail'))
    p = str(p).replace('<strong>', '').replace('</strong>', '')
    # writeTestResults(p)
    # return p

    pres = p.split('</a>,')
    dbs = []
    for res in pres:
        res = res.replace('\t','').replace('\n','')
#         parse the holdings/packageDetail/ID"> from the Database Name and return the results as a pair, then return the list of lists
        packageID = re.search('\d+"',res)
        packageID = packageID.group()
        packageID = int(packageID.replace('"',''))

        packageName = re.search('>',res)
        packageName = res[packageName.start()+1:].replace('</a>','').replace(']','').replace('&amp;','&')
        dbs.append([packageID,packageName])

        # print([packageID,packageName])
    return dbs

def getUserNamePassword():
    """create a file called userNamePassword.txt Put the username on the first line and password on the second"""
    with open('userNamePassword.txt') as f:
        unpw = f.read().splitlines()

    return unpw

def scraper():
    root = tk.Tk()
    root.withdraw()

    commonWords = getCommonWords()

    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver import ActionChains

    # estalbish login
    driver = webdriver.Chrome()
    driver.get("http://eadmin.ebscohost.com/")
    assert "EBSCOadmin" in driver.title

    userNamePassword = getUserNamePassword()

    useridentry = userNamePassword[0]
    password = userNamePassword[1]

    # find the login elements
    userid = driver.find_element_by_name("UserName")
    pw = driver.find_element_by_name("Password")

    # enter the login details
    userid.clear()
    userid.send_keys(useridentry)
    pw.clear()
    pw.send_keys(password)
    # press enter
    pw.send_keys(Keys.RETURN)

    databaseList = getDatabaseList()
    for d in databaseList:
        # skip the labels
        if d[0] == 'Database Code':
            continue
        databaseCode = d[0]
        databaseProvider = d[2]

        defaultDatabaseName = d[1]
        searchDatabaseName = defaultDatabaseName
    #     only want the first 3 words on the database name...
        dx = searchDatabaseName.split()
        for word in dx:
            if word.upper() in commonWords:
                dx.remove(word)
                searchDatabaseName = searchDatabaseName.replace(word, '')

        if len(dx) > 3:
            # find the length of the string that is the first three full words
            dLength = searchDatabaseName.find(dx[2])+len(dx[2])
            searchDatabaseName = searchDatabaseName[:dLength]
        # encode the default database name
        searchDatabaseName = searchDatabaseName.replace('  ',' ').replace(':','').replace('-',' ').replace('&','and').replace('(','').replace(')','')

        searchDatabaseName = urllib.parse.quote_plus(searchDatabaseName)
        testURL = "http://admin.ebscohost.com/adminweb/holdings/packages?searchTerm="+searchDatabaseName+"&resultsPerPage=100&pageIndex=1&selShowType=0&contentType=0&sortType=1&pubType=0"

    # open test website then wait 3 seconds
        driver.get(testURL)
        time.sleep(3)

        pageSource = driver.page_source
        res = extractResults(pageSource)

        finalResults = []
        for r in res:
            if r[0] != str(0):
                r.insert(0, databaseProvider)
                r.insert(0, defaultDatabaseName)
                r.insert(0, databaseCode)
                matchRatio = fuzz.ratio(defaultDatabaseName,r[-1])
                r.append(matchRatio)
                if matchRatio > 80:
                    finalResults.append(r)
        if len(finalResults) == 0:
            finalResults.append([databaseCode, defaultDatabaseName, databaseProvider, '0', 'Results - No Matches','0'])

        writeResults(finalResults)

    driver.close()
    print("done!")

scraper()