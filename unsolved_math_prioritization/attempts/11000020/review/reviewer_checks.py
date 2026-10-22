#!/usr/bin/env python3
"""Independent integrity, extraction, arithmetic, and Sylow-projection controls.

This does NOT reproduce the published MSSV existence/fullness classification.
Run with the sibling packet/ and source/ directories available.
"""
from pathlib import Path
from fractions import Fraction
from itertools import combinations_with_replacement
import hashlib
import json
import re
import subprocess

BASE = Path(__file__).resolve().parent.parent
REVIEW = BASE / 'review'
PACKET = BASE / 'packet'
SOURCE = BASE / 'source'
FROZEN = '441c21fe437955edfaedf0a13f32c25115d1ce1cc0f849c2e4a5b8c1b3941794'
assertions = 0

def check(condition, label):
    global assertions
    assertions += 1
    if not condition:
        raise AssertionError(label)

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

manifest_data = (PACKET / 'manifest.json').read_bytes()
check(sha256(manifest_data) == FROZEN, 'exact input freeze')
manifest = json.loads(manifest_data)
for item in manifest['files']:
    data = (PACKET / item['file']).read_bytes()
    check(sha256(data) == item['sha256'], 'packet digest: ' + item['file'])
    check(len(data) == item['bytes'], 'packet size: ' + item['file'])
remote = json.loads((REVIEW / 'REMOTE_PACKET.json').read_text())
check(len(remote['files']) == 9, 'nine remote files')
check(set(x['name'] for x in remote['files']) == set(p.name for p in PACKET.iterdir() if p.is_file()), 'exact local/remote file set')
for item in remote['files']:
    data = (PACKET / item['name']).read_bytes()
    check(git_blob(data) == item['sha'], 'remote blob match: ' + item['name'])
    check(len(data) == item['size'], 'remote byte count: ' + item['name'])
sources = json.loads((PACKET / 'source_manifest.json').read_text())['sources']
for item in sources:
    data = (SOURCE / item['file']).read_bytes()
    check(sha256(data) == item['sha256'], 'source digest: ' + item['file'])
    check(len(data) == item['bytes'], 'source byte count: ' + item['file'])

# Fresh extraction, rather than trusting the author-created .txt intermediates.
def pdf_page(file, page):
    result = subprocess.run(['pdftotext', '-f', str(page), '-l', str(page), '-layout', str(SOURCE / file), '-'], check=True, capture_output=True, text=True)
    return result.stdout

farb = pdf_page('mcgbook.pdf', 30)
check('Problem 2.19' in farb, 'source target')
check(farb.index('Problem 2.19') < farb.index('A Hurwitz surface') < farb.index('Question 2.20'), 'source boundary')
scope_v1 = pdf_page('mssv2002v1.pdf', 14)
scope_v2 = pdf_page('mssv2002.pdf', 15)
for scope in (scope_v1, scope_v2):
    flat = ' '.join(scope.split())
    check('There exists a G-curve' in flat, 'existence language')
    check('G is the full automorphism group' in flat, 'fullness language')
    check('7.2' in flat, 'correct section')
ids = [(128,138), (128,136), (128,134), (128,75)]
for version in ('mssv2002v1.pdf', 'mssv2002.pdf'):
    table = pdf_page(version, 17)
    check('Genus 9' in table and ('δ = 0' in table or 'δ=0' in table), 'genus and dimension')
    for row, (order,index) in zip(range(5,9), ids):
        pattern = rf'\b{row}\s+\({order},\s*{index}\)\s+\(2,\s*4,\s*8\)'
        check(re.search(pattern, table) is not None, f'{version} row {row}')
schweizer = ' '.join(pdf_page('schweizer2017.pdf', 5).split())
check('If G is nilpotent' in schweizer and re.search(r'16\(g\s*−\s*1\)', schweizer) is not None, 'classical bound cited')
check('Theorems 1.8.4 and 2.1.2' in schweizer, 'original theorem numbers')
positive = ' '.join(pdf_page('reyes_speziali2025.pdf', 5).split())
check('Assume g odd and different from 21.' in positive, 'odd-genus exception')
check('Theorem 3.1.' in positive and 'Assume g even.' in positive, 'positive theorem identified')

# Generic nilpotent obstruction independent of the author's four-case code.
# Project xyz=1 to a Sylow p factor. If only one factor is nonidentity, impossible.
# If exactly two are nonidentity they are mutual inverses and have equal order.
def valuations(n):
    answer = {}
    p = 2
    while p*p <= n:
        while n % p == 0:
            answer[p] = answer.get(p,0) + 1
            n //= p
        p += 1
    if n > 1:
        answer[n] = answer.get(n,0) + 1
    return answer

def passes_sylow_projection(triple):
    factors = [valuations(n) for n in triple]
    for p in set().union(*(set(f) for f in factors)):
        nonzero = [f[p] for f in factors if p in f]
        if len(nonzero) == 1 or (len(nonzero) == 2 and nonzero[0] != nonzero[1]):
            return False
    return True

def triangle_deficit(t):
    return Fraction(1) - sum((Fraction(1,n) for n in t), Fraction(0))

# The manual inequalities in REVIEW.md prove that bad triples must lie below 24.
# Enumerating all sorted triples through 100 separately tests boundaries/tails.
bad = []
boundary = []
for t in combinations_with_replacement(range(2,101),3):
    d = triangle_deficit(t)
    if 0 < d < Fraction(1,8):
        bad.append(t)
    elif d == Fraction(1,8):
        boundary.append(t)
check(len(bad) == 22, '22 forbidden hyperbolic triples')
check(max(max(t) for t in bad) == 23, 'strict bound endpoint')
for t in bad:
    check(not passes_sylow_projection(t), 'Sylow obstruction: ' + repr(t))
check(set(boundary) == {(2,3,24),(2,4,8)}, 'all triangle equality candidates')
check(not passes_sylow_projection((2,3,24)), 'reject mixed-prime boundary')
check(passes_sylow_projection((2,4,8)), 'retain valid 2-group boundary')
check(not passes_sylow_projection((2,3,7)), 'negative control: Hurwitz signature')
check(passes_sylow_projection((2,3,6)), 'nonhyperbolic control: C6 triple')
check(triangle_deficit((2,3,6)) == 0, 'positivity essential')

# Remaining quotient cases. These numerical controls supplement manual monotonicity.
check(2*2-2 >= Fraction(1,8), 'h>=2')
check(1-Fraction(1,2) >= Fraction(1,8), 'h=1 with branching')
check(-2+5*(1-Fraction(1,2)) >= Fraction(1,8), 'sphere r>=5')
check(-2+3*(1-Fraction(1,2))+(1-Fraction(1,3)) == Fraction(1,6), 'sphere r=4 positive minimum')
check(-2+4*(1-Fraction(1,2)) == 0, 'sphere r=4 excluded all-2 case')
check(Fraction(1)-3*Fraction(1,4) >= Fraction(1,8), 'a>=4 tail')
check(Fraction(1)-Fraction(1,3)-2*Fraction(1,4) >= Fraction(1,8), 'a=3 b>=4 tail')
check(Fraction(1)-Fraction(1,2)-2*Fraction(1,6) >= Fraction(1,8), 'a=2 b>=6 tail')
check(triangle_deficit((2,4,8)) == Fraction(1,8), 'attained deficit')
check(128*triangle_deficit((2,4,8)) == 2*9-2, 'genus-9 RH')
check(16*(9-1) == 128 == 2**7, 'maximal nilpotent order')
check(len(set(ids)) == 4, 'four distinct library identifiers')

author_run = subprocess.run(['python3',str(PACKET/'verify.py')],check=True,capture_output=True,text=True)
author = json.loads(author_run.stdout)
check(author == json.loads((PACKET/'verifier_output.json').read_text()), 'author output replay')
check(author['assertions'] == 69 and author['status'] == 'PASS', 'author PASS')
(REVIEW/'AUTHOR_REPLAY.json').write_text(json.dumps(author,indent=2,sort_keys=True)+'\n')
output = {
    'status':'PASS', 'assertions':assertions,
    'input_manifest_sha256':FROZEN,
    'remote_packet_files_verified':len(remote['files']),
    'source_pdf_hashes_verified':len(sources),
    'fresh_pdf_extraction_checks':True,
    'forbidden_triangle_signatures':bad,
    'nilpotent_equality_triangle_candidates':[t for t in boundary if passes_sylow_projection(t)],
    'independent_obstruction':'Sylow projections of xyz=1: one nonidentity factor impossible; exactly two must have equal p-orders.',
    'classification_reproduced':False,
    'author_assertions_replayed':author['assertions'],
}
print(json.dumps(output,indent=2,sort_keys=True))
