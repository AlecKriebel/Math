#!/usr/bin/env python3
"""Independent automata diagnostics, stdlib only. No author imports.
Finite checks support the audit; they do not prove PRZ or arbitrary k.
Run: python3 -I -B independent_automata.py
"""
from collections import deque
from itertools import product
import json

ALPHABET = '01'
GRAPHS = {
    'full': ((0, '0', 0), (0, '1', 0)),
    'even': ((0, '0', 0), (0, '1', 1), (1, '1', 0)),
    'golden': ((0, '0', 0), (0, '1', 1), (1, '0', 0)),
    'period_two': ((0, '0', 1), (1, '1', 0)),
    'singleton': ((0, '0', 0),),
}
checks = 0

def require(value, claim):
    global checks
    checks += 1
    if not value:
        raise AssertionError(claim)


def all_words(maximum):
    for n in range(maximum + 1):
        for w in product(ALPHABET, repeat=n):
            yield ''.join(w)


def nfa_states(edges):
    return frozenset(s for u, a, v in edges for s in (u, v))


def advance(edges, current, letter):
    return frozenset(v for u, a, v in edges if a == letter and u in current)


def language_dfa(edges):
    """Reachable subset DFA with explicit dead state if reachable."""
    initial = nfa_states(edges)
    subsets, lookup, rows = [initial], {initial: 0}, []
    for s in subsets:
        row = []
        for a in ALPHABET:
            t = advance(edges, s, a)
            if t not in lookup:
                lookup[t] = len(subsets)
                subsets.append(t)
            row.append(lookup[t])
        rows.append(tuple(row))
    return tuple(rows), frozenset(i for i, q in enumerate(subsets) if q)


def run(rows, word, initial=0):
    for a in word:
        initial = rows[initial][ALPHABET.index(a)]
    return initial


def member(edges, word):
    rows, accept = language_dfa(edges)
    return run(rows, word) in accept


def bad_dfa(target, width, table):
    """DFA state = output-language DFA state plus delayed input symbols."""
    target_rows, target_final = language_dfa(target)
    states, index, rows, final = [(0, '')], {(0, ''): 0}, [], set()
    for i, (output_state, pending) in enumerate(states):
        if output_state not in target_final:
            final.add(i)
        row = []
        for a in ALPHABET:
            buffer = pending + a
            out = output_state
            if len(buffer) == width:
                out = target_rows[out][ALPHABET.index(table[buffer])]
                buffer = buffer[1:]
            nxt = (out, buffer)
            if nxt not in index:
                index[nxt] = len(states)
                states.append(nxt)
            row.append(index[nxt])
        rows.append(tuple(row))
    return tuple(rows), frozenset(final)


def image(word, width, table):
    return ''.join(table[word[i:i + width]] for i in range(max(0, len(word) - width + 1)))


def canonical(edges, n):
    allowed = [w for w in all_words(n) if len(w) == n and member(edges, w)]
    return tuple((w[:-1], w[-1], w[1:]) for w in allowed)


def intersection_witness(left, right, right_final):
    """All vertices initial/final in left NFA, no word length cutoff."""
    queue = deque((u, 0) for u in sorted(nfa_states(left)))
    previous = {s: None for s in queue}
    for state in queue:
        if state[1] in right_final:
            return ''
    while queue:
        state = queue.popleft()
        u, q = state
        for source, a, dest in left:
            if source != u:
                continue
            nxt = (dest, right[q][ALPHABET.index(a)])
            if nxt in previous:
                continue
            previous[nxt] = (state, a)
            if nxt[1] in right_final:
                letters, back = [], nxt
                while previous[back] is not None:
                    back, a = previous[back]
                    letters.append(a)
                return ''.join(reversed(letters))
            queue.append(nxt)
    return None


def common_monoid(left_rows, right_rows):
    """Transformations on a disjoint union, including the identity."""
    offset = len(left_rows)
    generators = tuple(tuple(r[j] for r in left_rows) + tuple(offset+r[j] for r in right_rows)
                       for j in range(len(ALPHABET)))
    identity = tuple(range(offset + len(right_rows)))
    elements, index, representative = [identity], {identity: 0}, ['']
    for i, transform in enumerate(elements):
        for j, letter_map in enumerate(generators):
            nxt = tuple(letter_map[transform[s]] for s in range(len(identity)))
            if nxt not in index:
                index[nxt] = len(elements)
                elements.append(nxt)
                representative.append(representative[i] + ALPHABET[j])
    return elements, representative


def profile(word, k):
    left, right = k // 2, k-k//2
    return frozenset((word[max(0, i-left):i], word[i:i+right]) for i in range(len(word)))


def profile_summary(word, k):
    """Sufficient long-word invariants used in the proof."""
    return (word[:k-1] if k > 1 else '', word[-k+1:] if k > 1 else '',
            frozenset(word[i:i+k] for i in range(max(0, len(word)-k+1))))


def fixed_three_signature(word):
    # For k=3, complete profiles = prefix2, suffix2, factors3 for long words.
    if len(word) < 3:
        return ('short', word)
    return ('long', word[:2], word[-2:], frozenset(word[i:i+3] for i in range(len(word)-2)))


def signature_step(signature, letter):
    if signature[0] == 'short':
        return fixed_three_signature(signature[1] + letter)
    _, prefix, suffix, factors = signature
    return ('long', prefix, (suffix+letter)[-2:], factors | {suffix+letter})


def exact_profile_three_collision(edges, bad_rows, bad_final):
    """Finite closure of word signatures x L-DFA x B-DFA; any length."""
    rows, good_final = language_dfa(edges)
    initial = (0, 0, ('short', ''))
    queue = deque([initial]); reached = {initial}; good, bad = {}, {}
    witness = {initial: ''}
    while queue:
        q, b, signature = state = queue.popleft()
        word = witness[state]
        key = profile(word, 3)
        if q in good_final:
            good.setdefault(key, word)
        if b in bad_final:
            bad.setdefault(key, word)
        if key in good and key in bad:
            return {'good': good[key], 'bad': bad[key], 'states_explored': len(reached)}
        for j, a in enumerate(ALPHABET):
            nxt = (rows[q][j], bad_rows[b][j], signature_step(signature, a))
            if nxt not in reached:
                reached.add(nxt); queue.append(nxt); witness[nxt] = word+a
    return {'good': None, 'bad': None, 'states_explored': len(reached)}


def connector(edges, left, right):
    queue = deque(['']); seen = set()
    while queue:
        middle = queue.popleft()
        current = nfa_states(edges)
        for a in left+middle:
            current = advance(edges, current, a)
        if current in seen:
            continue
        seen.add(current)
        final = current
        for a in right:
            final = advance(edges, final, a)
        if final:
            return left+middle+right
        for a in ALPHABET:
            if advance(edges, current, a):
                queue.append(middle+a)
    raise AssertionError('no connector')


def main():
    report = {'scope': 'Independent finite diagnostics; no arbitrary-k or PRZ proof inferred.'}
    identity = {'0':'0', '1':'1'}
    controls = {}
    for name, edges in GRAPHS.items():
        for n in range(2, 5):
            graph = canonical(edges, n)
            for w in all_words(7):
                actual = member(graph, w)
                if len(w) < n:
                    expected = member(edges, w)
                else:
                    expected = all(member(edges, w[i:i+n]) for i in range(len(w)-n+1))
                require(actual == expected, 'canonical appended-label graph language')
            bad_rows, bad_final = bad_dfa(edges, 1, identity)
            witness = intersection_witness(graph, bad_rows, bad_final)
            require((witness is not None) == (name == 'even'), 'identity positive/negative control')
            controls[name+str(n)] = witness
    report['canonical_identity_controls'] = controls
    # Exhaustive, independently built bad DFAs versus direct finite-word outputs.
    cases = 0
    for name in ('even', 'golden', 'period_two', 'singleton'):
        edges = GRAPHS[name]
        for output in product(ALPHABET, repeat=4):
            table = dict(zip(('00', '01', '10', '11'), output))
            rows, final = bad_dfa(edges, 2, table)
            for w in all_words(8):
                require((run(rows, w) in final) == (not member(edges, image(w, 2, table))), 'bad DFA matches direct word computation, including short words')
            for domain in (edges, canonical(edges, 3)):
                w = intersection_witness(domain, rows, final)
                if w is not None:
                    require(member(domain, w) and not member(edges, image(w, 2, table)), 'exact intersection certificate')
            cases += 1
    report['width_two_rule_cases'] = cases
    # Shared monoid recognition is tested on all its reachable transformations.
    shared = {}
    for name in ('even', 'golden', 'period_two', 'singleton', 'full'):
        edges = GRAPHS[name]
        left, good_final = language_dfa(edges)
        right, bad_final = bad_dfa(edges, 1, identity)
        transforms, reps = common_monoid(left, right)
        for t, w in zip(transforms, reps):
            require((t[0] in good_final) == member(edges, w), 'monoid recognizes allowed words')
            require((t[len(left)]-len(left) in bad_final) == (not member(edges, w)), 'same monoid recognizes bad words')
        shared[name] = {'size':len(transforms), 'k':4*(len(transforms)+1)}
    report['common_monoids'] = shared
    # All word pairs with the same proof invariant have equal published profiles.
    words = list(all_words(8))
    groups_checked = 0
    for k in range(1, 5):
        classes = {}
        for w in words:
            if len(w) < max(k, 2*k-2):
                continue
            signature = profile_summary(w, k)
            require(signature not in classes or classes[signature] == profile(w,k), 'factor/boundary invariant implies profile equality')
            classes[signature] = profile(w,k)
        groups_checked += len(classes)
    report['profile_invariant_classes'] = groups_checked
    # Exact finite closure detects collisions for the non-SFT even shift and
    # emptiness for the SFT controls; this is not bounded word enumeration.
    collisions = {}
    for name in GRAPHS:
        edges = GRAPHS[name]
        rows, final = bad_dfa(edges, 1, identity)
        c = exact_profile_three_collision(edges, rows, final)
        require((c['good'] is not None) == (name == 'even'), 'exact LT[3] separation control')
        if c['good'] is not None:
            require(member(edges, c['good']) and not member(edges, c['bad']) and profile(c['good'],3) == profile(c['bad'],3), 'LT[3] collision certificate')
        collisions[name] = c
    report['exact_LT3_controls'] = collisions
    # Saturation checks include k odd/even and a nonmixing irreducible target.
    saturation = {}
    for n in (2,3,4):
        edges = GRAPHS['even']; graph = canonical(edges,n)
        rows, final = bad_dfa(edges,1,identity)
        obstruction = intersection_witness(graph,rows,final)
        U = ''
        for w in all_words(n):
            if len(w) == n and member(edges,w):
                U = connector(edges,U,w)
        while len(U)<2*n:
            U = connector(edges,U,U)
        good = connector(edges,U,U)
        bad = connector(graph,connector(graph,U,obstruction),U)
        require(member(edges,good) and member(graph,bad) and not member(edges,bad), 'saturated good/bad memberships')
        require(profile(good,n)==profile(bad,n), 'saturated equality in the imported convention')
        saturation[str(n)]={'U_length':len(U),'good_length':len(good),'bad_length':len(bad),'obstruction':obstruction}
    report['saturation_controls'] = saturation
    # Different completions of the same widened identity on golden mean.
    edges=GRAPHS['golden']; blocks=[w for w in all_words(3) if len(w)==3]
    absent=[w for w in blocks if not member(edges,w)]
    for values in product(ALPHABET,repeat=len(absent)):
        table={w:w[1] for w in blocks};table.update(dict(zip(absent,values)))
        rows,final=bad_dfa(edges,3,table)
        require(intersection_witness(canonical(edges,3),rows,final) is None,'all width-three completions agree on canonical neighborhood')
    report['completion_variants']=2**len(absent)
    # Negative controls deliberately break preconditions or a necessary boundary.
    require(profile('01010',3)!=profile('010101',3) and { '01010'[i:i+3] for i in range(3)}=={'010101'[i:i+3] for i in range(4)},'factor-set-only mutation must be detected')
    dangling=((0,'0',0),(1,'1',0))
    require(member(dangling,'1') and not member(((0,'0',0),),'1'),'untrimmed graph mutation must be detected')
    require(member(GRAPHS['golden'],'1') and not advance(GRAPHS['golden'],frozenset({1}),'1'),'one-initial-state mutation must be detected')
    require(intersection_witness(canonical(GRAPHS['even'],3),*bad_dfa(GRAPHS['even'],1,{'0':'0','1':'0'})) is None,'nononto constant positive extension control')
    report['negative_controls']='PASS: factor-only, untrimmed-graph, single-initial-state mutations detected; nononto constant does not imply equality.'
    report['status']='PASS';report['checks']=checks
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
