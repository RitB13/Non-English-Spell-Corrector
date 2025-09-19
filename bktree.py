from collections import defaultdict

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
        current = [i] + [0]*len(b)
        for j, cb in enumerate(b, start=1):
            ins = previous[j] + 1
            dele = current[j-1] + 1
            sub = previous[j-1] + (0 if ca == cb else 1)
            current[j] = ins if ins < dele else dele
            if sub < current[j]:
                current[j] = sub
        previous = current
    return previous[-1]

class BKNode:
    def __init__(self, word):
        self.word = word
        self.children = {}  # distance -> BKNode

class BKTree:
    def __init__(self, words=None, distance_fn=None):
        self.distance = distance_fn or levenshtein
        self.root = None
        if words:
            it = iter(words)
            try:
                first = next(it)
                self.root = BKNode(first)
            except StopIteration:
                return
            for w in it:
                self.add(w)

    def add(self, word):
        if self.root is None:
            self.root = BKNode(word)
            return
        node = self.root
        while True:
            d = self.distance(word, node.word)
            if d in node.children:
                node = node.children[d]
            else:
                node.children[d] = BKNode(word)
                break

    def query(self, word, max_dist):
        if self.root is None:
            return []
        candidates = [self.root]
        result = []
        while candidates:
            node = candidates.pop()
            d = self.distance(word, node.word)
            if d <= max_dist:
                result.append((node.word, d))
            low = d - max_dist
            high = d + max_dist
            for dist_k, child in node.children.items():
                if low <= dist_k <= high:
                    candidates.append(child)
        return result
