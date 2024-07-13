
# NEWS_URL = "https://apnews.com/"
NEWS_URL = "https://www.nbcnews.com/"
PICTURES_PATH = "output/pictures/"
OUTPUT_BASE_PATH = "output/"
LOGGING_PATH = "output/logs/"

# My Selectors
SELECTOR_HAMBURGER_MENU = "//button[@aria-label='news navigation and search']"
SELECTOR_SEARCH_FIELD = "//input[@placeholder='Search NBC News']"
SELECTOR_SORT_BY_TEXT = "//div[contains(text(), 'Sort by:')]"
SELECTOR_OPTIONS_SORT_BY = "//div[contains(@class, 'gsc-orderby')]/div[contains(@class, 'gsc-option-menu-container') and preceding-sibling::div[contains(text(), 'Sort by:')]]"
SELECTOR_OPTION_BY_DATE = "//div[@class='gsc-option' and text()='Date']"
SELECTOR_PAGINATION_SECTION = "//div[@tabindex='0' and contains(text(), '1')]"
SELECTOR_PAGINATION_TEMPLATE = "//div[@aria-label='Page {count}']"

SELECTOR_ROOT_RESULTS_SECTION = "//div[@id='___gcse_0']/div/div/div/div[5]/div[2]/div"
SELECTOR_SEARCH_RESULTS = "//div[@class='gsc-webResult gsc-result']"
