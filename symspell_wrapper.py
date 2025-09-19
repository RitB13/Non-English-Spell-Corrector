try:
    from symspellpy.symspellpy import SymSpell, Verbosity
    HAVE_SYMSPELL = True
except Exception:
    HAVE_SYMSPELL = False

from bktree import BKTree, levenshtein

class CandidateProvider:
    def __init__(self, dict_words, max_edit_distance=2):
        self.max_edit = max_edit_distance
        self.dict_words = dict_words
        if HAVE_SYMSPELL:
            max_edit = max_edit_distance
            self.sym = SymSpell(max_dictionary_edit_distance=max_edit, prefix_length=7)
            # build dictionary from dict_words: frequency 1 by default
            # SymSpell expects a file or add_dictionary_entry
            for w in dict_words:
                self.sym.create_dictionary_entry(w, 1)
        else:
            self.tree = BKTree(dict_words, distance_fn=levenshtein)

    def get_candidates(self, word, topn=10):
        if HAVE_SYMSPELL:
            results = self.sym.lookup(word, Verbosity.CLOSEST, max_edit_distance=self.max_edit)
            # results: list of SuggestItem objects (term, distance, count)
            return [(r.term, r.distance) for r in results][:topn]
        else:
            # fallback - query BK-tree with increasing radius until some candidates found
            radius = self.max_edit
            res = self.tree.query(word, radius)
            res.sort(key=lambda x:x[1])
            return res[:topn]
