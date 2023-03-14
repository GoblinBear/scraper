import unittest

from main import __extract_external_resources as extract_external_resources
from main import __get_word_list as get_word_list


class TestMain(unittest.TestCase):
    def test_extract_external_resources(self):
        test_logs = [
            {'message': '{"message": {"method": "Network.requestWillBeSent", "params": {"request": {"url": "https://example.com/image.jpg"}, "type": "Image"}}}'},
            {'message': '{"message": {"method": "Network.requestWillBeSent", "params": {"request": {"url": "https://example.com/stylesheet.css"}, "type": "Stylesheet"}}}'},
            {'message': '{"message": {"method": "Network.requestWillBeSent", "params": {"request": {"url": "https://example.com/invalidresource"}, "type": "InvalidResourceType"}}}'},
            {'message': '{"message": {"method": "Network.requestWillBeSent", "params": {"request": {"url": "https://cfc.com/resource.js"}, "type": "Script"}}}'},
            {'message': '{"message": {"params": {"request": {"url": "https://example.com/missingtype"}}}}'}
        ]
        expected_resources = {
            'Image': ['https://example.com/image.jpg'],
            'Media': [],
            'Font': [],
            'Stylesheet': ['https://example.com/stylesheet.css'],
            'Script': ['https://cfc.com/resource.js']
        }
        result_resources = extract_external_resources(test_logs)
        self.assertEqual(result_resources, expected_resources)

    def test_get_word_list(self):
        # Test case 1: noun
        text = "I have some dogs."
        expected_output = ['I', 'have', 'some', 'dog']
        self.assertEqual(get_word_list(text), expected_output)

        # Test case 2: verb
        text = "I walked to a park today."
        expected_output = ['I', 'walk', 'to', 'a', 'park', 'today']
        self.assertEqual(get_word_list(text), expected_output)

        # Test case 3: adjective
        text = "I am taller than you."
        expected_output = ['I', 'be', 'taller', 'than', 'you']
        self.assertEqual(get_word_list(text), expected_output)

        # Test case 4: adverb
        text = "Which animal runs the fastest?"
        expected_output = ['Which', 'animal', 'run', 'the', 'fast']
        self.assertEqual(get_word_list(text), expected_output)

        # Test case 5: contraction
        text = "I haven't eaten snack!"
        expected_output = ['I', 'have', 'not', 'eat', 'snack']
        self.assertEqual(get_word_list(text), expected_output)
