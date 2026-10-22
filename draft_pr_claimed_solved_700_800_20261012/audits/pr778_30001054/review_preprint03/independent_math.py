"""Fresh finite audit: oriented order relations, without importing reviewed code."""
from collections import Counter
from itertools import permutations, product
import json
from random import Random


def need(ok, why):
    if not ok:
        raise RuntimeError(why)


def opposite(state):
    return tuple(-x for x in state[::-1])


def orders(state):
    return {(state[i], state[j]) for i in range(len(state))
            for j in range(i + 1, len(state))}


def inspect(word):
    n = len(word[0]) // 2
    length = 4 * n * (n - 1)
    symbols = set(range(1, n + 1)) | set(range(-n, 0))
    if len(word) != length:
        return None
    if any(len(s) != 2 * n or set(s) != symbols or
           any((i, -i) not in orders(s) for i in range(1, n + 1)) for s in word):
        return None
    if any(word[(k + length // 2) % length] != opposite(s)
           for k, s in enumerate(word)):
        return None
    events = []
    for a, b in zip(word, word[1:] + word[:1]):
        # One reversed relative-order relation is equivalent to one adjacent
        # transposition, independently of position-difference implementations.
        gained = orders(b) - orders(a)
        lost = orders(a) - orders(b)
        if len(gained) != 1 or lost != {(y, x) for x, y in gained}:
            return None
        pair, = gained
        if abs(pair[0]) == abs(pair[1]):
            return None
        events.append(pair)
    least = next(d for d in range(1, length + 1)
                 if all(word[(k + d) % length] == s for k, s in enumerate(word)))
    return dict(least=least, events=events, mixed=sum(x * y < 0 for x, y in events),
                once=len(set(events)) == length)


def main():
    states = tuple(p for p in permutations((1, -1, 2, -2))
                   if p.index(1) < p.index(-1) and p.index(2) < p.index(-2))
    counts = Counter()
    for half in product(states, repeat=4):
        word = half + tuple(map(opposite, half))
        r = inspect(word)
        if r is None:
            continue
        counts['period8_weak_including_nonprimitive'] += 1
        if r['least'] != 8:
            continue
        counts['primitive'] += 1
        counts['switch_once'] += r['once']
        counts['zero_mixed'] += r['mixed'] == 0
        separated = any(s in ((1, -1, 2, -2), (2, -2, 1, -1)) for s in word)
        counts['separated'] += separated
        need(not separated or r['once'], 'separated word violates lemma')
        need(r['once'] or r['mixed'] == 0, 'unreported n2 intermediate class')
    a, b, c = (1, 2, -1, -2), (1, 2, -2, -1), (2, 1, -2, -1)
    witness = (a, b, a, b, c, b, c, b)
    r = inspect(witness)
    need(r['least'] == 8 and r['mixed'] == 0, 'witness fails')
    need(r['events'] == [(-2,-1),(-1,-2),(-2,-1),(2,1),
                         (1,2),(2,1),(1,2),(-1,-2)], 'printed events differ')
    symmetry = 0
    for rev, rename, phase in product((False, True), (False, True), range(8)):
        w = witness[::-1] if rev else witness
        if rename:
            w = tuple(tuple((3 - abs(x)) * (1 if x > 0 else -1) for x in s) for s in w)
        w = w[phase:] + w[:phase]
        q = inspect(w)
        need(q is not None and q['mixed'] == 0 and q['least'] == 8, 'symmetry')
        symmetry += 1
    need({k:counts[k] for k in ('primitive','switch_once','zero_mixed','separated')}
         == {'primitive':48,'switch_once':16,'zero_mixed':32,'separated':16},
         'printed primitive counts differ: '+str(counts))
    controls = []
    rng = Random(30001054)
    for n in range(2, 10):
        for trial in range(4):
            labels = list(range(1, n + 1)); rng.shuffle(labels)
            start = tuple(x for i in labels for x in (i, -i))
            target = opposite(start)
            rank = {x:k for k,x in enumerate(target)}
            path = [start]
            while path[-1] != target:
                s = list(path[-1])
                inversions = [k for k in range(len(s)-1) if rank[s[k]] > rank[s[k+1]]]
                k = rng.choice(inversions)
                need(abs(s[k]) != abs(s[k+1]), 'same-body inversion')
                s[k],s[k+1] = s[k+1],s[k]
                path.append(tuple(s))
            word = tuple(path[:-1]) + tuple(map(opposite, path[:-1]))
            q = inspect(word)
            need(q is not None and q['once'] and q['least'] == len(word), 'positive boundary')
            half = len(word)//2
            for k in range(half):
                x,y = q['events'][k]
                need(q['events'][k+half] == (-y,-x), 'second-half event transport')
            controls.append({'n':n,'trial':trial,'length':len(word),'least':q['least'],
                             'all_ordered_types_once':True,'transport_checked':True})
    print(json.dumps({'status':'PASS','method':'relative-order relation differences',
                      'first_halves':6**4,'counts':dict(counts),'witness':r,
                      'symmetries':symmetry,'separated_controls':controls,
                      'limit':'Finite controls supplement, and do not replace, all-n proof.'},
                     sort_keys=True,indent=2))


if __name__ == '__main__':
    main()
