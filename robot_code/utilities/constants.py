
# NEWS_URL = "https://apnews.com/"
NEWS_URL = "https://www.nbcnews.com/"

# paths
PICTURES_PATH = "output/pictures/"
OUTPUT_BASE_PATH = "output/"
LOGGING_PATH = "output/logs/"
FINAL_REPORT_PATH = "output/final_report/"
FINAL_REPORT_FILE_PATH_TEMPLATE = FINAL_REPORT_PATH+"FINAL_REPORT_{date}.xlsx"
FINAL_ZIP_FILE_TEMPLATE = OUTPUT_BASE_PATH+"Final_results_{time_stamp}.zip"

# MESSAGES
LOG_INFO_TEMPLATE = "\nProcess Executed Correctly:\n**********\n{message}\n**********\n\nFunction Executed:\n**********\n{function_name}\n**********\n\nFrom File:\n**********\n{file_name}\n**********"
LOG_FAILED_TEMPLATE = "\nProcess Failed Error:\n**********\n{message}\n**********\n\nFunction Executed:\n**********\n{function_name}\n**********\n\nFrom File:\n**********\n{file_name}\n**********"

# Selector initial page
SELECTOR_HAMBURGER_MENU = "//button[@aria-label='news navigation and search']"
SELECTOR_SEARCH_BUTTON = "//use[@xlink:href='#icon-magnify']"

# Selector second page to search the phrase
SELECTOR_SEARCH_FIELD = "//input[@placeholder='Search NBC News']"

# selectors 3rd page

# sort by date the results
SELECTOR_SORT_BY_TEXT = "//div[contains(text(), 'Sort by:')]"
# SELECTOR_OPTIONS_SORT_BY = "//div[contains(@class, 'gsc-orderby')]/div[contains(@class, 'gsc-option-menu-container') and preceding-sibling::div[contains(text(), 'Sort by:')]]"
SELECTOR_OPTIONS_SORT_BY = "//div[preceding-sibling::div[contains(text(), 'Sort by:')]]"
# SELECTOR_OPTION_BY_DATE = "//div[@class='gsc-option' and text()='Date']"
SELECTOR_OPTION_BY_DATE = "//div[contains(text(), 'Date')]"

# to get pagination information about the search results
SELECTOR_PAGINATION_SECTION = "//div[@tabindex='0' and contains(text(), '1')]"
SELECTOR_PAGINATION_TEMPLATE = "//div[@aria-label='Page {count}']"

# to get the results information
# SELECTOR_ROOT_RESULTS_SECTION = "#___gcse_0"
SELECTOR_ROOT_RESULTS_SECTION = "id:___gcse_0"
# SELECTOR_ROOT_RESULTS_SECTION = "xpath://div[@id='___gcse_0']/div/div/div/div[5]/div[2]"
# SELECTOR_ROOT_RESULTS_SECTION = "//div[@class='gsc-resultsbox-visible']"
SELECTOR_SEARCH_RESULTS = "//div[@class='gsc-webResult gsc-result']"
