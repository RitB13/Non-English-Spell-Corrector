import re

# Map similar letters / groups -> canonical symbol
PHONETIC_MAP = {
    # vowels to 'A' (we collapse varying vowel spellings)
    'a':'A','aa':'A','e':'A','i':'A','o':'A','u':'A','ai':'A','au':'A',
    # consonant groups (representative)
    'k':'K','kh':'K','g':'K','gh':'K',
    'c':'C','ch':'C','j':'C','jh':'C',
    't':'T','th':'T','d':'T','dh':'T',
    'p':'P','ph':'P','b':'P','bh':'P',
    's':'S','sh':'S','z':'S',
    'n':'N','m':'M','l':'L','r':'R','y':'Y','v':'V','w':'V','h':'H','ng':'N',
}

# We will implement a greedy tokenizer for letter groups e.g., 'kh','gh','ch' etc.
# The approach: normalize input -> iterate looking for longest match from PHONETIC_MAP keys.

# Create a set of pattern keys sorted by length desc for greedy matching:
_PH_KEYS = sorted(PHONETIC_MAP.keys(), key=lambda x: -len(x))

def normalize_input(word):
    # basic input normalization: lowercase, remove non-alnum
    if word is None:
        return ''
    w = str(word).strip().lower()
    w = re.sub(r'[^a-z0-9]', '', w)
    # collapse repeated characters conservatively (allow up to 2)
    w = re.sub(r'(.)\\1{2,}', r'\\1\\1', w)
    return w

def phonetic_hash(word):
    """
    Reduce a word to a short phonetic fingerprint string.
    Example: 'gobhi' -> 'GKMA' (depending on mapping)
    """
    w = normalize_input(word)
    i = 0
    out = []
    while i < len(w):
        matched = False
        # try keys longest-first
        for k in _PH_KEYS:
            if w.startswith(k, i):
                out.append(PHONETIC_MAP[k])
                i += len(k)
                matched = True
                break
        if not matched:
            # character not in map - map single char as itself grouped
            ch = w[i]
            # treat digits as themselves
            if ch.isdigit():
                out.append(ch)
            else:
                out.append(ch.upper())
            i += 1
    # compress repeats in fingerprint
    fp = []
    prev = None
    for c in out:
        if c != prev:
            fp.append(c)
            prev = c
    return ''.join(fp)

# similarity helpers
def lcs_length(a, b):
    # longest common subsequence length (O(n*m) dynamic)
    na, nb = len(a), len(b)
    if na == 0 or nb == 0:
        return 0
    dp = [[0]*(nb+1) for _ in range(na+1)]
    for i in range(1, na+1):
        for j in range(1, nb+1):
            if a[i-1] == b[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = dp[i-1][j] if dp[i-1][j] > dp[i][j-1] else dp[i][j-1]
    return dp[na][nb]

def phonetic_similarity(a, b):
    """
    Return a float in [0,1]. 1.0 = perfect phonetic match.
    Uses LCS on phonetic fingerprints normalized by max length.
    """
    ha = phonetic_hash(a)
    hb = phonetic_hash(b)
    if not ha and not hb:
        return 1.0
    if ha == hb:
        return 1.0
    l = lcs_length(ha, hb)
    denom = max(len(ha), len(hb))
    if denom == 0:
        return 0.0
    return l / denom
