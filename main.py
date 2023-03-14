from collections import Counter
import json
import requests

from bs4 import BeautifulSoup

import contractions

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service

import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

from log import Logger


logger = Logger(enable_stream_handler=True)

CHROME_DRIVER_PATH = './chromedriver'
EXTERNAL_RESOURCES_PATH = 'resources.json'
WORD_COUNT_PATH = 'word_count.json'
CFC_URL = 'https://www.cfcunderwriting.com'

nltk_packages = ['punkt', 'wordnet', 'averaged_perceptron_tagger']
for package in nltk_packages:
    try:
        nltk.data.find(package)
    except LookupError:
        nltk.download(package)


def __capture_http_requests(url):
    try:
        chromedriver_service = Service(executable_path=CHROME_DRIVER_PATH)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--headless')

        caps = DesiredCapabilities.CHROME
        caps['goog:loggingPrefs'] = {'performance': 'ALL'}

        driver = webdriver.Chrome(service=chromedriver_service,
                                  options=chrome_options,
                                  desired_capabilities=caps)
    except Exception as e:
        logger.error(f'Initializing webdriver: {e}')
        return None

    try:
        driver.get(url)
    except Exception as e:
        logger.error(f'Trying to retrieve URL: {e}')
        driver.quit()
        return None

    try:
        network_logs = driver.get_log('performance')
    except Exception as e:
        logger.error(f'Retrieving performance logs: {e}')
        driver.quit()
        return None

    try:
        driver.quit()
    except Exception as e:
        logger.error(f'Closing webdriver: {e}')
        return None

    return network_logs


def __extract_external_resources(network_logs):
    resources = {
        'Image': [],
        'Media': [],
        'Font': [],
        'Stylesheet': [],
        'Script': []
    }

    for log in network_logs:
        try:
            message = json.loads(log['message'])['message']
        except Exception as e:
            logger.error(f'Trying to extract message from network logs: {e}')

        if 'method' not in message or \
           message['method'] != 'Network.requestWillBeSent':
            continue

        if 'params' not in message or 'request' not in message['params']:
            continue

        resource_url = message['params']['request']['url']
        if resource_url.startswith(CFC_URL):
            continue

        resource_type = message['params']['type']
        if resource_type not in resources:
            continue

        resources[resource_type].append(resource_url)

    return resources


def capture_external_resources(url):
    network_logs = __capture_http_requests(url)
    resources = __extract_external_resources(network_logs)
    with open(EXTERNAL_RESOURCES_PATH, 'w') as f:
        json.dump(resources, f, indent=4)


def extract_hyperlinks(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all('a')

    return links


def find_privacy_policy(links):
    privacy_policy_url = CFC_URL

    for link in links:
        if link.text.strip().lower() == 'privacy policy':
            privacy_policy_url = privacy_policy_url + link['href']
            break

    return privacy_policy_url


def __get_visible_text(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logging.error(f'Fetching {url}: {e}')
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')

    text = ''
    for tag in soup.find_all(['p', 'h1', 'h2', 'h3']):
        if tag.text.strip():
            text = text + tag.text.lower()

    return text


def __get_word_list(text):
    # Expand contractions
    expanded_words = []
    for word in text.split(' '):
        expanded_words.append(contractions.fix(word))

    expanded_text = ' '.join(expanded_words)

    # Tokenization
    words = word_tokenize(expanded_text)

    # Remove words containing nun-alphabet
    words = [word for word in words if word.isalpha()]

    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    pos_tags = nltk.pos_tag(words)
    lemmatized_words = []
    for word, pos in pos_tags:
        if pos.startswith('NN'):
            lemmatized_words.append(lemmatizer.lemmatize(word, pos='n'))
        elif pos.startswith('VB'):
            lemmatized_words.append(lemmatizer.lemmatize(word, pos='v'))
        elif pos.startswith('JJ'):
            lemmatized_words.append(lemmatizer.lemmatize(word, pos='a'))
        elif pos.startswith('R'):
            lemmatized_words.append(lemmatizer.lemmatize(word, pos='r'))
        else:
            lemmatized_words.append(lemmatizer.lemmatize(word))

    return lemmatized_words


def calculate_word_frequency(url):
    text = __get_visible_text(url)
    words = __get_word_list(text)
    word_counts = Counter(words)
    sorted_word_counts = dict(sorted(word_counts.items(),
                                     key=lambda x: x[1],
                                     reverse=True))

    with open('word_count.json', 'w') as f:
        json.dump(sorted_word_counts, f, indent=4)


def main():
    logger.info(f'Capturing external resources...')
    capture_external_resources(CFC_URL)
    logger.info(f'Check the file `{EXTERNAL_RESOURCES_PATH}` out.')

    links = extract_hyperlinks(CFC_URL)
    privacy_policy_url = find_privacy_policy(links)
    
    logger.info(f'Calculate word frequency in privacy policy page...')
    calculate_word_frequency(privacy_policy_url)
    logger.info(f'Check the file `{WORD_COUNT_PATH}` out.')


if __name__ == "__main__":
    main()
