# Scraper

## Environment

Here is the environment information for this project:
- Operating system: Linux Ubuntu
- Python version: 3.8.10
- Chrome version: 111
- ChromeDriver version: 111.0.5563.64

Note that the project already contains a ChromeDriver, but if you encounter any issues, you can download the appropriate version of ChromeDriver for your system from the [official website](https://chromedriver.chromium.org/downloads).

## Installation

To install the required dependencies for this project, use the following commands in the terminal:

```shell
$ pip install beautifulsoup4
$ pip install contractions
$ pip install selenium
$ pip install nltk
```

This will install the following packages:

- `beautifulsoup4`: A library for parsing HTML and XML documents.
- `contractions`: A library for expanding English language contractions.
- `selenium`: A library for automating web browsers.
- `nltk`: The Natural Language Toolkit, a library for working with human language data.

Make sure you have `pip` installed before running these commands.

## Usage

To use the scraper, run the following command in the terminal:

```shell
$ python3 main.py
```

The program will generate two output files:
- *resources.json*: This file will contain the external resources of the index webpage in JSON format, organized by type. Here's an example of the expected structure:
    ```
    {
        "Image": [],
        "Media": [],
        "Font": [],
        "Stylesheet": [],
        "Script": []
    }
    ```
- *word_count.json*: This file will contain the case-insensitive word frequency count for the privacy policy page. Here's an example of the expected structure:
    ```
    {
        "to": 112,
        "you": 67,
        "the": 60,
        "your": 58,
        "of": 55
    }
    ```

## Run Tests

To run the tests for the *main.py* program, use the following command in the terminal:

```shell
$ python3 -m unittest -v tests/test_main.py
```

## File Structure

```
📦scraper
 ┣ 📂tests
 ┃ ┗ 📜test_main.py
 ┣ 📜log.py
 ┗ 📜main.py
 ```

Project *scraper* contains the following files and directories:

- *tests*: A directory containing *test_main.py*, a file with tests for the *main.py* program.
- *log.py*: A logging system module that provides three levels of logging: `INFO`, `DEBUG`, and `ERROR`.
- *main.py*: The main program used to scrape the website.
