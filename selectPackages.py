import time
import csv

def getUserNamePassword():
    """create a file called userNamePassword.txt Put the username on the first line and password on the second"""
    with open('userNamePassword.txt') as f:
        unpw = f.read().splitlines()
    return unpw

def getPackages():
    packageList = 'packageList.csv'
    with open(packageList, 'r') as f:
        reader = csv.reader(f)
        packages = list(reader)
    return packages

def selectPackages():
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys

    # establish login
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

    packagesList = getPackages()

    for packages in packagesList:

        packageTitle = packages[0]
        testURL = packages[1]
        onlySomeTitles = packages[2]
        omitProxy = packages[3]

        print(str(packageTitle),(testURL),str(onlySomeTitles),str(omitProxy))

        if packageTitle == 'EBSCO Name':
            continue
        # testURL = 'http://admin.ebscohost.com/adminweb/holdings/packageDetail/2745'
        # onlySomeTitles = 0
        # omitProxy = 'No'

        # open package
        driver.get(testURL)
        time.sleep(2)

        # select the "Select Package" element, call it the toggle, press down arrow twice
        toggle = driver.find_element_by_css_selector("#currentHoldingsTarget > div > a")
        toggle.send_keys(Keys.ARROW_DOWN*2)
        time.sleep(1)

        # test to see if the "select entire package" button is available - if not, it is because it is already selected
        select = driver.find_elements_by_link_text('Select Entire Package')
        if len(select) > 0:
            # Find the new element that pops up called select entire package, name it select, and press enter, assumes not selected
            select = driver.find_element_by_link_text('Select Entire Package')
            select.send_keys(Keys.ENTER)
            time.sleep(1)
            # find all the "buttons" on the page - it'll be button 1, send the enter key
            continueButton = driver.find_elements_by_tag_name('button')
            continueButton[1].send_keys(Keys.ENTER)
            print('\tpackage selected')
        else:
            print('\talready selected, continuing...')
        time.sleep(1)

        # find the save button
        saveButton = driver.find_element_by_css_selector('input.btn.btn-warning.evt-save')

        # set the "Allow EBSCO to Add New Titles to the correct value
        ebscoNewTitles = driver.find_element_by_class_name('radio')
        ebscoNewTitlesValue = ebscoNewTitles.is_selected()
        if (onlySomeTitles == 'No' and ebscoNewTitlesValue == True) or (onlySomeTitles == 'Yes' and ebscoNewTitlesValue == False):
            pass
        elif onlySomeTitles == 'No' and ebscoNewTitlesValue == False:
            ebscoNewTitles.send_keys(Keys.SPACE)
            print('\tSetting "Allow EBSCO To Add New Titles to Yes')
            time.sleep(1)
            saveButton.send_keys(Keys.ENTER)
        elif onlySomeTitles == 'Yes' and ebscoNewTitlesValue == True:
            ebscoNewTitles.send_keys(Keys.SPACE)
            print('\tSetting "Allow EBSCO To Add New Titles to No')
            saveButton.send_keys(Keys.ENTER)

        # set the Proxy Server Value
        time.sleep(1)
        proxyServer = driver.find_element_by_css_selector('button.btn.btn-flat.sel-show-type.evt-isSelected-disable')
        saveButton = driver.find_element_by_css_selector('input.btn.btn-warning.evt-save')
        # get the current value of the proxyServer dropdown
        proxyServerValue = proxyServer.text

        # possible values in the dropdown
        n = 'None'
        p = 'EZproxy'
        tp = 'Token Proxy'
        ip = 'Inherited - EZproxy'
        it = 'Inherited - Token Proxy'

        # click the dropdown
        proxyServer.click()
        time.sleep(1)
        # find the listItem elements
        listItems = driver.find_elements_by_css_selector('li.dropdown-item')
        liText = []
        for li in listItems:
            liText.append(li.text)

        n = liText.index('None')
        try:
            i = liText.index(ip)
            t = liText.index(tp)
        except ValueError:
            t = liText.index(p)
            i = liText.index(it)

        if omitProxy == 'Yes' and proxyServerValue in(ip,it):
            listItems[n].click()
            print('\tInherited')
            time.sleep(1)
            saveButton.send_keys(Keys.ENTER)
        elif omitProxy == 'Yes' and proxyServerValue == n:
            pass
        elif omitProxy == 'Yes' and proxyServerValue == tp:
            listItems[n].click()
            print('\tSetting Proxy Server to None')
            time.sleep(1)
            saveButton.send_keys(Keys.ENTER)
        elif omitProxy == 'No' and proxyServerValue in(ip,it) :
            pass
        elif omitProxy == 'No' and proxyServerValue == n:
            listItems[i].click()
            print('\tSetting Proxy Server to Inherited')
            time.sleep(1)
            saveButton.send_keys(Keys.ENTER)
        elif omitProxy == 'No' and proxyServerValue in(tp,p):
            listItems[i].click()
            print('\tSetting Proxy Server to Inherited')
            time.sleep(1)
            saveButton.send_keys(Keys.ENTER)

        # Save at the end
        saveButton = driver.find_element_by_css_selector('input.btn.btn-warning.evt-save')
        saveButton.send_keys(Keys.ENTER)

    driver.close()
    print('Done!')