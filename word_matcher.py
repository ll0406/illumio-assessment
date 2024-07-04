'''
Name: word_matcher.py

Description:
This program loads text from an input file, find matching words from a set of
predefined vocabularies, and output the matched words and their locations to an output file

Author: Li Liu liliu0406@gmail.com
'''
import argparse
import time
from collections import defaultdict
from typing import List, Dict, Set

class WordsMatcher:
    '''
    WordsMatcher class to match predefined words from vocabulary text file in a input text file.
    '''
    def __init__(self, input_file: str, vocab_file: str, ignore_case: bool, output: bool) -> None:
        '''
        Initialize file names, class variables, build vocabs from predefined word file.
        '''
        self.input_file = input_file
        self.vocab_file = vocab_file
        self.ignore_case = ignore_case
        self.output = output
        self.READ_CHUNKSIZE = 1024 * 1024 # 1 MB read chunk size
        self.vocabs = self._build_vocab()

    def match(self) -> Dict[str, List[int]]:
        '''
        Iteratively read from input file (each time reading READ_CHUNKSIZE),
        and store matched word locations in a dictionary.

        Returns
            Dictionary of lists that maps matched word to the matched line numbers in the input file.
        '''
        matched_words = defaultdict(list)
        offset = 1 # 1-based text file line
        # Open input file for reading
        with open(self.input_file) as f:
            while True:
                # Read lines less than READ_CHUNKSIZE
                lines = f.readlines(self.READ_CHUNKSIZE)
                if not lines:
                    break
                # Strip word and record corresponding line number
                words_line = [(line.strip().lower(), i + offset) for i, line in enumerate(lines)] if self.ignore_case \
                    else [(line.strip(), i + offset) for i, line in enumerate(lines)]
                # Append line location of input word matched with predefined vocabulary
                [matched_words[word].append(line) for word, line in words_line if word in self.vocabs]

                offset += len(lines)
        # Output the match result to a text file in the current directory
        if self.output:
            self._output_match_result(matched_words)

        return matched_words

    def _output_match_result(self, matched_words: Dict[str, List[int]]) -> str:
        '''
        Helper function to output the matched result to a timestamped output text file.

        Arguments
            matched_words: Dict[str, List[int]] - Match result that maps matched word to a list of matched line locations
        '''
        output_filename = f'output-{time.time()}.txt'
        with open(output_filename, 'w') as f:
            for word, lines in matched_words.items():
                f.write(f'{word}: {lines}\n')
        print(f'Finished writing match output to {output_filename}')
        return output_filename

    def _build_vocab(self) -> Set[str]:
        '''
        Helper function to build a set of vocabulary from the specified predefined text file.

        Returns
            Set of vocabulary strings
        '''
        vocabs = []
        with open(self.vocab_file) as f:
            while True:
                # Iteratively read READ_CHUNKSIZE lines from the vocabulary file.
                lines = f.readlines(self.READ_CHUNKSIZE)
                if not lines:
                    break
                # Build vocabulary by checking if ignore word case.
                if self.ignore_case:
                    vocabs.extend([line.strip().lower() for line in lines])
                else:
                    vocabs.extend([line.strip() for line in lines])
        return set(vocabs)

def main(args: argparse.ArgumentParser) -> None:
    print(f'-- Start matching predefined words from {args.vocab_file} in input file {args.input_file} --')
    start_time = time.time()
    matcher = WordsMatcher(args.input_file, args.vocab_file, args.ignore_case, args.output)
    matched_words = matcher.match()
    print(f'Found {len(matched_words.keys())} matched words')
    print(f'-- Finished running in {time.time() - start_time:.5f} seconds --')


if __name__ == '__main__':
    # Argparse setup
    parser = argparse.ArgumentParser(
        prog='word_matcher.py',
        description='''
            This program loads text from an input file, find matching words from a set of
            predefined vocabularies, and output the matched words as a separate output.txt file
        ''',
        epilog='Please place input and vocab text files in the same directory of the word_matcher.py')
    parser.add_argument('input_file', metavar='input_file.txt', type=str, help='name of the input text file')
    parser.add_argument('vocab_file', metavar='vocab_file.txt', type=str, help='name of the output text file')
    parser.add_argument('-i', '--ignorecase', dest='ignore_case', action='store_true', default=False, help='ignore case when match words, default to false')
    parser.add_argument('-o', '--output', dest='output', action='store_true', default=False, help='output match result to a txt files, default to false')

    # Invoke main method with parsed arugments
    args = parser.parse_args()
    main(args)