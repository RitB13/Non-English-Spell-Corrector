import os, csv, argparse
from preprocess import normalize
from phonetic import phonetic_similarity
from bktree import levenshtein

try:
    from symspell_wrapper import CandidateProvider
    HAVE_SYMSPELL_WRAPPER = True
except Exception:
    from symspell_wrapper import CandidateProvider
    HAVE_SYMSPELL_WRAPPER = False

def load_dict(path):
    with open(path, encoding='utf8') as f:
        return [line.strip() for line in f if line.strip()]

def load_freq_csv(path):
    freq = {}
    if not os.path.exists(path):
        return freq
    with open(path, encoding='utf8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        for row in reader:
            if len(row) >= 2:
                freq[row[0].strip()] = int(row[1])
    return freq

def normalized_edit_score(a, b):
    if a is None or b is None:
        return 0.0
    na, nb = normalize(a), normalize(b)
    if na == nb:
        return 1.0
    d = levenshtein(na, nb)
    return 1 - (d / max(len(na), len(nb))) if max(len(na), len(nb)) else 0.0

def score_candidate(input_word, candidate_word, freq_map, max_freq, alpha, beta, gamma):
    p_sim = phonetic_similarity(input_word, candidate_word)
    ed_sim = normalized_edit_score(input_word, candidate_word)
    f = freq_map.get(normalize(candidate_word), 0)
    freq_norm = f / max_freq if max_freq > 0 else 0.0
    final = alpha*p_sim + beta*ed_sim + gamma*freq_norm
    return final

def main(args):
    dict_words = load_dict(os.path.join(args.root, 'data', 'reference.txt'))
    inputs = load_dict(os.path.join(args.root, 'data', 'errors.txt'))
    freq_map = load_freq_csv(os.path.join(args.root, 'data', 'freqs.csv'))
    max_freq = max(freq_map.values()) if freq_map else 0
    provider = CandidateProvider(dict_words, max_edit_distance=args.maxedit)

    alpha, beta, gamma = args.alpha, args.beta, args.gamma
    output_rows = []

    for w in inputs:
        # Get candidate list
        candlist = provider.get_candidates(w, topn=args.topn)
        scored = []
        for cand, rawdist in candlist:
            score = score_candidate(w, cand, freq_map, max_freq, alpha, beta, gamma)
            scored.append((score, cand))
        # pick top-1
        top1 = max(scored, key=lambda x:x[0])[1] if scored else w
        # if score too low, keep original
        if not scored or max(scored, key=lambda x:x[0])[0] < args.threshold:
            top1 = w
        output_rows.append([w, top1])

    # Write simple corrected CSV
    out_path = os.path.join(args.root, 'corrected_output.csv')
    with open(out_path, 'w', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerow(['File_Error', 'Corrected'])
        for row in output_rows:
            writer.writerow(row)

    print('Corrected output written to', out_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default='.', help='project root')
    parser.add_argument('--topn', type=int, default=3)
    parser.add_argument('--maxedit', type=int, default=2)
    parser.add_argument('--alpha', type=float, default=0.5)
    parser.add_argument('--beta', type=float, default=0.4)
    parser.add_argument('--gamma', type=float, default=0.1)
    parser.add_argument('--threshold', type=float, default=0.35)
    args = parser.parse_args()
    main(args)
