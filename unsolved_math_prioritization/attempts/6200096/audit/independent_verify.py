#!/usr/bin/env python3
"""Independent exact diagnostics, with no imports from the authored verifier.

The all-elements/topological argument is in INDEPENDENT_AUDIT.md. These finite
checks are diagnostic and are not substituted for that proof.
"""
from fractions import Fraction
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys
import tarfile

EXPECTED_MANIFEST = 'ddc7550f12c0b732ac42a5eb1238002d1877950b4d74d8a81ba98ccd15632f99'
EXPECTED_ARCHIVE = '9b7ff841bdde3323e364149fb5081e09e5a9942295296f19eb1d5648a3757571'
COUNTS = {}


def check(group, condition):
    if not condition:
        raise AssertionError(group)
    COUNTS[group] = COUNTS.get(group, 0) + 1


def normal(word):
    """Collect the central letter, reducing the remaining free-group word."""
    center, stack = 0, []
    for letter in word:
        if letter == 'c':
            center += 1
        elif letter == 'C':
            center -= 1
        elif stack and stack[-1] == letter.swapcase():
            stack.pop()
        else:
            stack.append(letter)
    return center, ''.join(stack)


def inverse(word):
    return word.swapcase()[::-1]


def maps(k, backwards=False):
    ck = 'c' * k if k >= 0 else 'C' * (-k)
    positive = {'c': 'C', 'a': ck + 'a',
                'b': 'adA' if backwards else 'd',
                'd': 'b' if backwards else 'Aba'}
    return positive | {x.upper(): inverse(w) for x, w in positive.items()}


def replace(word, mapping):
    return ''.join(mapping[letter] for letter in word)


def algebra():
    # Work with raw words in all four generators, including the central one.
    # This differs from the author's reduced-free-word implementation.
    tested = 0
    for length in range(5):
        for letters in product('cCaAbBdD', repeat=length):
            word = ''.join(letters)
            for k in (-3, 0, 1, 2):
                f, back = maps(k), maps(k, True)
                check('inverse_forward', normal(replace(replace(word, f), back)) == normal(word))
                check('inverse_backward', normal(replace(replace(word, back), f)) == normal(word))
                check('square_inner', normal(replace(replace(word, f), f)) == normal('A' + word + 'a'))
            tested += 1
    for k in range(-17, 18):
        f = maps(k)
        for x in 'abd':
            check('central_relations', normal(replace('c' + x + 'C' + x.upper(), f)) == (0, ''))
        for n in range(-21, 22):
            w = ('c' * n if n >= 0 else 'C' * (-n)) + 'A'
            fixed = normal(replace(w, f)) == normal(w)
            check('fixed_square_parity', fixed == (2*n == -k))
    check('noninner', normal(replace('c', maps(1))) != normal('c'))
    return tested


EDGES = {'e': ('u', 'v'), 'f': ('v', 'u'), 'B': ('u', 'u'), 'D': ('v', 'v')}
DELTA = {'e': 'f', 'f': 'e', 'B': 'D', 'D': 'B'}


def kappa(edge, t):
    return t if edge == 'e' else Fraction(0)


def lam(edge, t):
    # Continuous real lift of kappa(delta x)-kappa(x), with values 0 at u, -1 at v.
    return {'e': -t, 'f': t-1, 'B': Fraction(0), 'D': Fraction(-1)}[edge]


def F(point, backwards=False, twist=1):
    s, edge, t = point
    next_edge = DELTA[edge]
    return ((-s + twist*kappa(next_edge if backwards else edge, t)) % 1, next_edge, t)


def geometry():
    grid = sorted({Fraction(i, d) for d in range(1, 11) for i in range(d+1)})
    tested = 0
    for edge, (start, end) in EDGES.items():
        for t, vertex in ((Fraction(0), start), (Fraction(1), end)):
            check('lambda_gluing', lam(edge, t) == (0 if vertex == 'u' else -1))
            check('kappa_gluing', kappa(edge, t) % 1 == 0)
        for t in grid:
            check('lambda_lift', (kappa(DELTA[edge], t)-kappa(edge,t)-lam(edge,t)) % 1 == 0)
            for s in grid[:-1]:
                point = (s, edge, t)
                check('geometric_inverse', F(F(point), backwards=True) == point)
                check('geometric_reverse_inverse', F(F(point, backwards=True)) == point)
                check('geometric_square', F(F(point)) == ((s+lam(edge,t)) % 1, edge, t))
                check('zero_twist_involution', F(F(point,twist=0),twist=0) == point)
                tested += 1
    # A concrete point witnesses that F itself is not an involution.
    point = (Fraction(0), 'e', Fraction(1, 2))
    check('not_strict_involution', F(F(point)) != point)
    return {'grid_size': len(grid), 'points_tested': tested}


def graph_paths():
    # Edges are signed tokens, rather than the author's integer representation.
    basis = {'a': [('e',1),('f',1)], 'b': [('B',1)],
             'd': [('f',-1),('D',1),('f',1)]}
    p = [('f',-1)]
    def invert(path):
        return [(edge,-sign) for edge,sign in path[::-1]]
    def reduced(path):
        out=[]
        for edge,sign in path:
            if out and out[-1] == (edge,-sign): out.pop()
            else: out.append((edge,sign))
        return out
    def expand(word):
        out=[]
        for x in word:
            out += basis[x.lower()] if x.islower() else invert(basis[x.lower()])
        return reduced(out)
    def endpoint(path,start):
        vertex=start
        for edge,sign in path:
            a,b=EDGES[edge]
            if sign<0:a,b=b,a
            check('path_incidence',vertex==a)
            vertex=b
        return vertex
    check('basepoint_path',endpoint(p,'u')=='v')
    for g,word in [('a','a'),('b','d'),('d','Aba')]:
        loop=basis[g]
        check('basis_loops',endpoint(loop,'u')=='u')
        moved=[(DELTA[edge],sign) for edge,sign in loop]
        actual=reduced(p+moved+invert(p))
        check('basepoint_image_loop',endpoint(actual,'u')=='u')
        check('basepoint_images',actual==expand(word))
        check('central_winding',sum(sign for edge,sign in loop if edge=='e')==(g=='a'))


def binding(packet, archive):
    raw=(packet/'SHA256SUMS.json').read_bytes()
    check('manifest_binding', hashlib.sha256(raw).hexdigest()==EXPECTED_MANIFEST)
    items=json.loads(raw)['files']
    expected={'SHA256SUMS.json'}
    for item in items:
        data=(packet/item['path']).read_bytes()
        check('payload_bytes',len(data)==item['bytes'])
        check('payload_hash',hashlib.sha256(data).hexdigest()==item['sha256'])
        expected.add(item['path'])
    actual={str(p.relative_to(packet)) for p in packet.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
    check('packet_inventory',actual==expected)
    archive_data=archive.read_bytes()
    check('archive_bytes',len(archive_data)==12868)
    check('archive_binding',hashlib.sha256(archive_data).hexdigest()==EXPECTED_ARCHIVE)
    with tarfile.open(archive) as tar:
        files={m.name:m for m in tar.getmembers() if m.isfile()}
        check('archive_inventory',set(files)=={'packet/'+p for p in expected})
        for name,m in files.items():
            check('archive_payloads',tar.extractfile(m).read()==(packet/name.removeprefix('packet/')).read_bytes())
    import tempfile
    with tempfile.TemporaryDirectory() as temp:
        out=Path(temp)/'replayed.json'
        proc=subprocess.run([sys.executable,str(packet/'verify.py'),'--output',str(out)],check=True,capture_output=True,text=True)
        summary=json.loads(proc.stdout)
        check('author_assertion_count',summary['assertions']==632826)
        check('author_result_bytes',out.read_bytes()==(packet/'CONTROL_RESULTS.json').read_bytes())
    return {'payloads_verified':len(items),'author_replay':summary,'author_result_byte_identical':True}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--packet',type=Path)
    parser.add_argument('--archive',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    result={'schema':1,'target_id':6200096,'result':'PASS','raw_words_tested':algebra(),
            'geometry':geometry()}
    graph_paths()
    if args.packet:
        if not args.archive:parser.error('--archive is required with --packet')
        result['binding']=binding(args.packet,args.archive)
    result['assertions_by_category']=COUNTS
    result['assertions']=sum(COUNTS.values())
    result['scope']='Finite diagnostics only; the complete argument is in INDEPENDENT_AUDIT.md.'
    encoded=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(encoded)
    print(encoded,end='')

if __name__=='__main__':main()
