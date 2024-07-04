# Illumio Assessment README
Date: 6/28/2024
Name: Li Liu
Email: liliu0406@gmail.com

## Initial Prompt
Write a program that reads a file and finds matches against a predefined set of words. There can be up to 10K entries in the list of predefined words.

Requirement details:
- Input file is a plain text (ascii) file, every record separated by a new line.
- For this exercise, assume English words only.
- The file size can be up to 20 MB.
- The predefined words are defined in a text file, every word separated by a newline. Use a sample file of your choice for the set of predefined keywords for the exercise.

## Additional Assumptions
1. Each line of input file consists a single English word, and a newline break. (Similar to the predefined keywords file)
2. The match result output of the program will be a map that maps matching predefined words to their line numbers in the input file.
    - For instance, a matching result of `hello: [1, 2, 3]` indicates word `hello` is found in line `1`, `2`, and `3` in the input file.
3. Due to the potential large size of predefined vocabulary, the program shall output the matched result to a separate output text file.
4. Other than the specified input and output files, the program shall accept 2 more optional flags: `-i, --ignorecase` toggles whether the program matches words ignoring case (default to false), and `-o, --output` toggles whether the program outputs the matcing result to a separate time-stamped output text file (default to false).
5. The Python program can be run in a CMD environment (Python 3.11+). The running instructions will be detailed in a later section.
6. The program assumes both input and predefined keyword text files are located in the same directory of the program. Using non-existent file name will cause the program to exit in a `FileNotFoundError` state.

## Files
```
illumio_assessment
|-- __init__.py
|-- README.md
|-- word_matcher.py
|-- test.py
|-- test_input.txt
|-- test_vocab.txt
|-- words_alpha.txt
|-- long_vocab.txt
```
Key files details:
- `word_matcher.py`: Implements the main program logic in `WordMatcher` class. It also consists argument parsing logic so that it can be executed in CMD line to perform word matching.
- `test.py`: Python unit tests that perform blackbox testing on `WordMatcher` class methods.
- `test_input.txt`: Test input text file used in `test.py` unit tests.
- `test_vocab.txt`: Test predefined keywords file used in `test.py` unit tests.
- `words_alpha.txt`: Long input text file consists ~4MB of words separated by newline separator.
- `long_vocab.txt`: Long perdefined keyword file that consists 10K predefined words.

## Runnig Instructions
0. Make sure Python 3.11+ is installed in the current environment.
1. In command line change directory to the `illumio_assessment` directory.
2. Using `words_alpha.txt` and `long_vocab.txt` as an example. Run `python word_matcher.py -i -o words_alpha.txt long_vocab.txt`
    - `-i` toggles the program to ignore case when match words.
    - `-o` toggles the program to output a match result file in the current directory.
3. Expect following similar print messages of the program and a new output text file to be created.
```
-- Start matching predefined words from long_vocab.txt in input file words_alpha.txt --
Finished writing match output to output-1719628129.8368168.txt
Found 10000 matched words
-- Finished running in 0.11213 seconds --
```
4. For more running instructions, please run `python word_matcher.py -h`.
5. It also possible to run with other text input files. Please be sure to include those files in the same directory of `word_matcher.py`.

## Unit Test Instructions
0. Make sure Python 3.11+ is installed in the current environment.
1. In command line change directory to the `illumio_assessment` directory.
2. Execute the unit tests in test.py by running `python -m unittest`.
3. Expect all 3 test cases to pass.

## Key Design Considerations
The key non-functional requirement specified in the prompt is that the input file size can be as large as 20MB, and the predefined keyword file can consist up to 10,000 keywords. To acommendate these requirements and prevent overusing memories, I made sure the program reads files iteratively with a chunksize of 1MB. 
Below is an example from the `word_matcher.py`, in which I deliberately implemented reading the predefined keyword file iteratively.
```python
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
```
## Future Considerations
Future improvement of the program can involve split input and vocabulary files into chunks and parallelize some of the matching tasks to multiple threads/workers to speed up the overall speed. However, Python 3.11 has not yet to remove the Global Interpretor Lock, so a multi-threading implementation of this CPU-bound program is less-likely to improve the overall performance.

Alternative language with better built-in concurrency such as Golang can be considered in the future.