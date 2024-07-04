from unittest import TestCase
from word_matcher import WordsMatcher

class WordMatcherTestCase(TestCase):
    '''
    Simple unit tests for WordMatcher class.
    '''
    def setUp(self):
        self.ignorecase_matcher = WordsMatcher('test_input.txt', 'test_vocab.txt', ignore_case=True, output=False)
        self.matcher = WordsMatcher('test_input.txt', 'test_vocab.txt', ignore_case=False, output=False)

    def test_word_matcher_build_vocabulary(self):
        '''
        Test if WordMatcher builds vocabulary correctly.
        '''
        expected_ignorecase_vocab = {
            'aardvark',
            'aardvarks',
            'aardwolf',
            'aardwolves'
        }
        expected_vocab = {
            'aardvark',
            'aardvarks',
            'aardwolf',
            'Aardwolf',
            'aardwolves'
        }
        self.assertEqual(self.ignorecase_matcher.vocabs, expected_ignorecase_vocab)
        self.assertEqual(self.matcher.vocabs, expected_vocab)
    
    def test_ignorecase_word_matcher_match_words(self):
        '''
        Test if ignore case word matcher matches words correctly
        '''
        expected_matched_words = {'aardvark': [14], 'aardvarks': [15], 'aardwolf': [16, 18, 20], 'aardwolves': [17, 19, 21]}
        matched_words = self.ignorecase_matcher.match()
        self.assertEqual(matched_words, expected_matched_words)
    
    def test_word_matcher_match_words(self):
        '''
        Test if (not ignorecase) word matcher matches words correctly
        '''
        expected_matched_words = {'aardvark': [14], 'aardvarks': [15], 'aardwolf': [16], 'aardwolves': [17], 'Aardwolf': [18, 20]}
        matched_words = self.matcher.match()
        self.assertEqual(matched_words, expected_matched_words)
