import gzip
import re
import sys


def preprocess_text(text):
    """Preprocess text by normalizing hyphenated words."""
    hyphen_pattern = re.compile(r'\b(\w+)\s*-\s*(\w+)\b')
    text = hyphen_pattern.sub(r'\1-\2', text)
    return text


def tokenize(text):
    """Tokenize text into sentences and words, respecting punctuation."""
    punctuation_pattern = re.compile(r'([.!?])')
    token_pattern = re.compile(r'\w+(?:-\w+)*|\'\w+|\w+\'(?:s|\w*)|[^\w\s]')
    text = punctuation_pattern.sub(r'\1\n', text)
    sentences = text.split('\n')
    for sentence in sentences:
        tokens = token_pattern.findall(sentence)
        yield tokens


def main(file_path):
    """Main function to read, preprocess and tokenize text from a gzip file."""
    with gzip.open(file_path, 'rt') as file:
        text = file.read()
        text = preprocess_text(text)
        for tokens in tokenize(text):
            print(' '.join(tokens))


if __name__ == '__main__':
    """Entry point of the script, requires a file path as an argument."""
    if len(sys.argv) != 2:
        print("Usage: python extract_sents.py <filepath>")
        sys.exit(1)
    main(sys.argv[1])
