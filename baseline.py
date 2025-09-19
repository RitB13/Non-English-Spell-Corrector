import argparse, os, sys, heapq, time
from preprocess import normalize

# Pure Python Levenshtein (iterative)
def levenshtein(a, b):
    if a == b:
        return 0
    if len(a) == 0:
        return len(b)
    if len(b) == 0:
        return len(a)
    if len(a) > len(b):
        a, b = b, a
    previous = list(range(len(b) + 1))
    for i, ca in enumerate(a, start=1):
        curr = [i] + [0]*len(b)
        for j, cb in enumerate(b, start=1):
            insert = previous[j] + 1
            delete = curr[j-1] + 1
            subst = previous[j-1] + (0 if ca == cb else 1)
            curr[j] = insert if insert < delete else delete
            if subst < curr[j]:
                curr[j] = subst
        previous = curr
    return previous[-1]

try:
    from rapidfuzz import process, fuzz
    HAVE_RAPIDFUZZ = True
except Exception:
    HAVE_RAPIDFUZZ = False

def load_list(path):
    with open(path, encoding='utf8') as f:
        return [line.strip() for line in f if line.strip()]

def generate_candidates_bruteforce(word, dict_words, topn=3):
    wn = normalize(word)
    heap = []
    for d in dict_words:
        dn = normalize(d)
        dist = levenshtein(wn, dn)
        lengthdiff = abs(len(wn) - len(dn))
        heap.append((dist, lengthdiff, d))
    heap.sort(key=lambda x: (x[0], x[1]))
    return [(w, dist) for dist, _, w in heap[:topn]]

def generate_candidates_rapidfuzz(word, dict_words, topn=3):
    res = process.extract(word, dict_words, scorer=fuzz.ratio, limit=topn)
    return [(r[0], 100 - r[1]) for r in res]

def main(args):
    dict_words = load_list(os.path.join(args.root,'data','reference.txt'))
    inputs = load_list(os.path.join(args.root,'data','errors.txt'))
    out_rows = []
    for w in inputs:
        if HAVE_RAPIDFUZZ:
            cand = generate_candidates_rapidfuzz(w, dict_words, topn=3)
        else:
            cand = generate_candidates_bruteforce(w, dict_words, topn=3)
        while len(cand) < 3:
            cand.append(('', 999))
        out_rows.append([w, cand[0][0], cand[0][1], cand[1][0], cand[1][1], cand[2][0], cand[2][1]])
    import csv
    with open(os.path.join(args.root, 'results_baseline.csv'), 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['input','top1','top1_score','top2','top2_score','top3','top3_score'])
        for r in out_rows:
            writer.writerow(r)
    print('Wrote results to', os.path.join(args.root, 'results_baseline.csv'))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='.', help='project root path')
    args = parser.parse_args()
    main(args)
