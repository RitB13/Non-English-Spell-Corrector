import re, unicodedata
def normalize(word):
    w = str(word or "").strip().lower()
    # remove diacritics
    w = ''.join(ch for ch in unicodedata.normalize('NFKD', w) if not unicodedata.combining(ch))
    # remove non-alnum
    w = re.sub(r'[^a-z0-9]', '', w)
    # collapse repeated letters (allow up to 2)
    w = re.sub(r'(.)\1{2,}', r'\1\1', w)
    return w

if __name__ == '__main__':
    import sys
    for line in sys.stdin:
        print(normalize(line.strip()))
