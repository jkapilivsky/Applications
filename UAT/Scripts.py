import bs4 as bs
import json, xlrd, requests
import pandas as pd
import time

from Results_html import basic_info_html, localization_html, v2migration_html

def get_source_code(url, mod_header=False):
    if mod_header:
        headers = {'v2header': 'true'}
        request = requests.get(url, headers=headers)
        soup = bs.BeautifulSoup(request.text, "lxml")
    else:
        request = requests.get(url)
        soup = bs.BeautifulSoup(request.text, "lxml")

        if '<Response [301]>' in request.history:
            print(True)

    return soup

def find_adobe(url):
    soup = get_source_code(url)
    adobe = soup.find_all(
        'script', src='https://assets.adobedtm.com/f621f149f278de13c57fa7bfeaddccafd7f1bda7/satelliteLib-fb69f0a9f50708c2a6a9431adb15862288e326cc.js')
    return adobe

def calls_datalayer(url, mod_header=False):
    soup = get_source_code(url, mod_header)
    datalayer_json = None
    for scripts in soup.find_all('script', type="text/javascript"):
        if 'legacyPageName' in scripts.text:
            datalayer_string = ''
            counter = 0
            for c in scripts.text:  # grabs just the JSON
                if c == '{':
                    counter += 1
                if counter > 0:
                    datalayer_string += c
                if c == '}':
                    counter -= 1
            datalayer_json = json.loads(datalayer_string)
    return datalayer_json

class Datalayer_Values():
    def __init__(self, url, modheader=False):
        self.page_name = calls_datalayer(url, modheader)['page']['legacyPageName']
        self.majorVersion = calls_datalayer(url, modheader)['site']['majorVersion']
        # self.siteID = calls_datalayer(url, modheader)['site']['SiteID']
        # self.country = calls_datalayer(url, modheader)['site']['country']
        # self.language = calls_datalayer(url, modheader)['site']['language']

class ExcelData:
    def __init__(self, excel_file, tab_name):
        self.excel_file = excel_file
        self.tab_name = tab_name

    def open_excel(self):
        book = xlrd.open_workbook(self.excel_file)
        sheet = book.sheet_by_name(self.tab_name)
        data = [[sheet.cell_value(r, c) for c in range(sheet.ncols)] for r in range(sheet.nrows)]
        return data

class Get_Basic_Info():
    def __init__(self, excel_file, tab_name):
        self.excel_file = ExcelData(excel_file, tab_name).open_excel()
        self.tab_name = 'Sheet1'
        self.df = pd.DataFrame(columns=['URL', 'Adobe firing', 'Page name'])
        self.page_count = 0
        self.adobe_passed = True
        self.pagename_passed = True

    def url_loop(self, update_textedit, update_progressbar):
        # Get length of for loop
        url_total = len(self.excel_file)

        for url in range(1, url_total):  # (skips row 1 headers)
            # Create a temp dataframe to append to final df that will be returned
            df_temp = pd.DataFrame([[self.excel_file[url][0],'Yes', Datalayer_Values(self.excel_file[url][0]).page_name]],
                                   columns=['URL','Adobe firing', 'Page name'])

            self.df = self.df.append(df_temp)

            # find DTM script!
            if find_adobe(self.excel_file[url][0]) == '':
                self.adobe_passed = False


            # Check to make sure there is a page name
            if Datalayer_Values(self.excel_file[url][0]).page_name == '':
                self.pagename_passed = False

####################################################HTML BLOCK############################################################################
            # Logic to determine if URL passed or failed
            if self.adobe_passed and self.pagename_passed:
                update_textedit(basic_info_html(self.adobe_passed, self.pagename_passed) %
                                (str(url) + " " + self.excel_file[url][0], 'green', 'Passed', 'Yes', Datalayer_Values(self.excel_file[url][0]).page_name))

            elif self.adobe_passed is False and self.pagename_passed:
                update_textedit(basic_info_html(self.adobe_passed, self.pagename_passed) %
                                (str(url) + " " + self.excel_file[url][0], 'red', 'Failed', 'Yes'))

            elif self.adobe_passed and self.pagename_passed is False:
                update_textedit(basic_info_html(self.adobe_passed, self.pagename_passed) %
                                (str(url) + " " + self.excel_file[url][0], 'red', 'Failed', Datalayer_Values(self.excel_file[url][0]).page_name))

            else:
                update_textedit(basic_info_html(self.adobe_passed, self.pagename_passed) %
                                (str(url) + " " + self.excel_file[url][0], 'red', 'Failed', 'Yes', Datalayer_Values(self.excel_file[url][0]).page_name))
####################################################HTML BLOCK END###########################################################################

            # Page counter
            self.page_count += 1
            time.sleep(.5)

            if self.page_count % 5 == 0:
                time.sleep(5)

            # Get percentage of progress through for loop. url-1 to remove headers
            update_progressbar(self.page_count / (url_total - 1))

        # Reset page count
        self.page_count = 0
        return self.df


class Localization_Info():
    def __init__(self, excel_file, tab_name, country_code):
        self._excel_file = ExcelData(excel_file, tab_name).open_excel()
        self._tab_name = 'Sheet1'
        self._country = country_code
        self._df = pd.DataFrame(columns=['Adobe firing', 'Page name', 'CountryCode'])
        self._page_count = 0
        self.adobe_passed = True
        self.countrycode_passed = True
        self.pagename_passed = True

    def url_loop(self, update_textedit, update_progressbar):
        self._url_total = len(self._excel_file)

        for url in range(1, self._url_total):
            column_one_page = Datalayer_Values(self._excel_file[url][0])
            column_two_page = Datalayer_Values(self._excel_file[url][1])

            # find DTM script!
            if find_adobe(self._excel_file[url][0]) == '':
                self.adobe_passed = False

            # Check that the country code is correct
            if column_two_page.page_name[0:2] != self._country:
                self.countrycode_passed = False

            # Check that pages names are identical (excluding country code [2:])
            if column_one_page.page_name[2:] == column_two_page.page_name[2:]:
                self.pagename_passed = False

            df_temp = pd.DataFrame([['Yes', Datalayer_Values(self._excel_file[url][0]).page_name, self._country]],
                                   columns=['Adobe firing', 'Page name', 'CountryCode'])
            self._df = self._df.append(df_temp)

####################################################HTML BLOCK############################################################################
            # Logic to determine if URL passed or failed
            if self.adobe_passed and self.pagename_passed and self.countrycode_passed:
                update_textedit(localization_html(self.adobe_passed, self.pagename_passed, self.countrycode_passed) %
                                (str(url) + " " + self._excel_file[url][0], 'green', 'Passed'))

            elif self.adobe_passed is False and self.pagename_passed and self.countrycode_passed:
                update_textedit(localization_html(self.adobe_passed, self.pagename_passed, self.countrycode_passed) %
                                (str(url) + " " + self._excel_file[url][0], 'red', 'Failed', 'No'))

            elif self.adobe_passed is False and self.pagename_passed is False and self.countrycode_passed:
                update_textedit(localization_html(self.adobe_passed, self.pagename_passed, self.countrycode_passed) %
                                (str(url) + " " + self._excel_file[url][0], 'red', 'Failed', 'No', column_two_page.page_name[2:]))

            elif self.adobe_passed is False and self.pagename_passed and self.countrycode_passed is False:
                update_textedit(localization_html(self.adobe_passed, self.pagename_passed, self.countrycode_passed) %
                                (str(url) + " " + self._excel_file[url][0], 'red', 'Failed', 'No', column_two_page.page_name[0:2]))

            elif self.adobe_passed and self.pagename_passed is False and self.countrycode_passed:
                update_textedit(localization_html(self.adobe_passed, self.pagename_passed, self.countrycode_passed) %
                                (str(url) + " " + self._excel_file[url][0], 'red', 'Failed', column_two_page.page_name[2:]))

            elif self.adobe_passed and self.pagename_passed is False and self.countrycode_passed is False:
                update_textedit(localization_html(self.adobe_passed, self.pagename_passed, self.countrycode_passed) %
                                (str(url) + " " + self._excel_file[url][0], 'red', 'Failed', column_two_page.page_name[0:2], column_two_page.page_name[2:]))

            elif self.adobe_passed is False and self.pagename_passed is False and self.countrycode_passed is False:
                update_textedit(localization_html(self.adobe_passed, self.pagename_passed, self.countrycode_passed) %
                                (str(url) + " " + self._excel_file[url][0], 'red', 'Failed', 'No', column_two_page.page_name[0:2], column_two_page.page_name[2:]))
####################################################HTML BLOCK END###########################################################################
            self._page_count += 1
            time.sleep(.025)
            update_progressbar(self._page_count / (self._url_total - 1))


class V2_Migration():
    def __init__(self, excel_file, tab_name, modheader):
        self._excel_file = ExcelData(excel_file, tab_name).open_excel()
        self._tab_name = 'Sheet1'
        self._modheader = modheader
        self._df = pd.DataFrame(columns=['Adobe firing', 'Page name', 'modheader'])
        self._page_count = 0
        self.adobe_passed = True
        self.majorversion_passed = True
        self.pagename_passed = True

    def url_loop(self, update_textedit, update_progressbar):
        url_total = len(self._excel_file)

        for url in range(1, url_total):
            column_one_page = Datalayer_Values(self._excel_file[url][0])
            column_two_page = Datalayer_Values(self._excel_file[url][1], self._modheader)

            # find DTM script!
            # find DTM script!
            if find_adobe(self._excel_file[url][0]) == '':
                self.adobe_passed = False

            # Check that majorVerison is 2
            if column_two_page.majorVersion != '2':
                self.majorversion_passed = False

            # Check that pages names are identical
            if column_one_page.page_name == column_two_page.page_name:
                self.pagename_passed = False

####################################################HTML BLOCK############################################################################
            # Logic to determine if URL passed or failed
            if self.adobe_passed and self.pagename_passed and self.majorversion_passed:
                update_textedit(v2migration_html(self.adobe_passed, self.pagename_passed, self.majorversion_passed) % (
                    str(url) + " " + self._excel_file[url][0], 'green', 'Passed'))

            elif self.adobe_passed is False and self.pagename_passed and self.majorversion_passed:
                update_textedit(v2migration_html(self.adobe_passed, self.pagename_passed, self.majorversion_passed) % (
                    str(url) + " " + self._excel_file[url][0], 'red', 'Failed', 'No'))

            elif self.adobe_passed is False and self.pagename_passed is False and self.majorversion_passed:
                update_textedit(v2migration_html(self.adobe_passed, self.pagename_passed, self.majorversion_passed) % (
                    str(url) + " " + self._excel_file[url][0], 'red', 'Failed', 'No',
                    Datalayer_Values(self._excel_file[url][0]).page_name))

            elif self.adobe_passed is False and self.pagename_passed and self.majorversion_passed is False:
                update_textedit(v2migration_html(self.adobe_passed, self.pagename_passed, self.majorversion_passed) % (
                    str(url) + " " + self._excel_file[url][0], 'red', 'Failed', 'No',
                    column_two_page.majorVersion))

            elif self.adobe_passed and self.pagename_passed is False and self.majorversion_passed:
                update_textedit(v2migration_html(self.adobe_passed, self.pagename_passed, self.majorversion_passed) % (
                    str(url) + " " + self._excel_file[url][0], 'red', 'Failed',
                    Datalayer_Values(self._excel_file[url][0]).page_name))

            elif self.adobe_passed and self.pagename_passed is False and self.majorversion_passed is False:
                update_textedit(v2migration_html(self.adobe_passed, self.pagename_passed, self.majorversion_passed) % (
                    str(url) + " " + self._excel_file[url][0], 'red', 'Failed',
                    Datalayer_Values(self._excel_file[url][0]).page_name, column_two_page.majorVersion))

            else:  # All failed
                update_textedit(v2migration_html(self.adobe_passed, self.pagename_passed, self.majorversion_passed) % (
                    str(url) + " " + self._excel_file[url][0], 'red', 'Failed', 'Yes',
                    Datalayer_Values(self._excel_file[url][0]).page_name, column_two_page.majorVersion))
####################################################HTML BLOCK END###########################################################################

            self._page_count += 1
            time.sleep(1)
            update_progressbar(self._page_count / (url_total - 1))

