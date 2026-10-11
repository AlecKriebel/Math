#!/usr/bin/env python3
"""Exact finite certificates and opt-in private-input verification; no network."""
import argparse
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations
import json
from math import comb
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent

def need(condition, message):
    if not condition:
        raise ValueError(message)

def read_json(path):
    return json.loads(path.read_text(encoding='utf-8'))

def digest(path):
    raw = path.read_bytes()
    return {'bytes': len(raw), 'sha256': sha256(raw).hexdigest()}

def check_manifest():
    manifest = read_json(ROOT / 'MANIFEST.json')
    need(manifest['schema'] == 1, 'manifest schema')
    rows = manifest['files']
    need(len(rows) == len({row['name'] for row in rows}), 'duplicate manifest entry')
    expected = {row['name'] for row in rows} | {'MANIFEST.json'}
    need(expected == {p.name for p in ROOT.iterdir()}, 'unexpected or missing member')
    for row in rows:
        name = row['name']
        need('/' not in name and '\\' not in name and name not in {'.', '..'}, 'unsafe member')
        p = ROOT / name
        need(p.is_file() and not p.is_symlink(), 'not a regular member')
        need(digest(p) == {k: row[k] for k in ('bytes', 'sha256')}, 'member digest: ' + name)

def determinant(a, b, c):
    return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

def inside_sign(p, a, b, c):
    d = [determinant(a,b,p), determinant(b,c,p), determinant(c,a,p)]
    return all(x > 0 for x in d) or all(x < 0 for x in d)

def area2(a, b, c):
    return abs(a[0]*b[1]+b[0]*c[1]+c[0]*a[1]-a[1]*b[0]-b[1]*c[0]-c[1]*a[0])

def inside_area(p, a, b, c):
    parts = [area2(p,a,b), area2(p,b,c), area2(p,c,a)]
    return all(parts) and sum(parts) == area2(a,b,c)

def validate_points(points):
    need(all(isinstance(p,list) and len(p)==2 and all(type(x) is int for x in p) for p in points), 'integer point format')
    need(len(points) == len({tuple(p) for p in points}), 'duplicate point')
    for t in combinations(range(len(points)),3):
        need(determinant(*(points[i] for i in t)) != 0, 'not in general position')

def triangle_data(points):
    validate_points(points)
    rows = []
    for t in combinations(range(len(points)),3):
        a,b,c = [points[i] for i in t]
        interior = []
        for j,p in enumerate(points):
            if j in t:
                continue
            first = inside_sign(p,a,b,c)
            need(first == inside_area(p,a,b,c), 'containment implementations disagree')
            if first:
                interior.append(j)
        rows.append((t,tuple(interior)))
    return rows

def mono_rows(rows, colors):
    return [(t,interior) for t,interior in rows if len({colors[i] for i in t})==1]

def check_certificate():
    cert = read_json(ROOT / 'certificate.json')
    need(cert['problem_id'] == 3081, 'wrong problem')
    need(cert['scope'] == 'local obstruction only; no asymptotic counterexample', 'scope mismatch')
    points, colors = cert['points'], cert['colors']
    need(len(points) == len(colors) == 8, 'witness size')
    need(all(type(c) is int and c in (0,1) for c in colors), 'color format')
    need(Counter(colors) == {0:4,1:4}, 'not balanced')
    rows = triangle_data(points)
    mono = mono_rows(rows,colors)
    expected = [(tuple(r['vertices']),tuple(r['inside'])) for r in cert['monochromatic_triangles']]
    need(mono == expected, 'interior certificate mismatch')
    need(len(mono) == 8, 'mono count')
    need(all(len(interior)==1 and colors[interior[0]]!=colors[t[0]] for t,interior in mono), 'one opposite-color interior point')
    need(cert['E0'] == sum(not interior for _,interior in mono) == 0, 'E0')
    need(cert['E1'] == sum(len(interior)==1 for _,interior in mono) == 8, 'E1')
    # All colorings of this fixed point set; these are finite checks of known bounds.
    for mask in range(1 << len(points)):
        col = [(mask >> i)&1 for i in range(len(points))]
        onecolor = mono_rows(rows,col)
        e0 = sum(not interior for _,interior in onecolor)
        e01 = sum(len(interior)<=1 for _,interior in onecolor)
        r = max(sum(col),len(col)-sum(col)); b = len(col)-r
        need(3*e0 >= r*max(r-b-2,0), 'discrepancy bound failed')
        need(3*e01 >= r*max(r-2-b//2,0), 'almost-empty fan bound failed')
    # Exact independent thinning enumeration at p=1/2, using original triangle list.
    sum_reduced_empty = 0
    for retained in range(1 << len(points)):
        for t,interior in mono:
            if all(retained & (1<<i) for i in t) and all(not (retained & (1<<j)) for j in interior):
                sum_reduced_empty += 1
    lhs = Fraction(sum_reduced_empty,1<<len(points))
    rhs = sum((Fraction(1,2)**(3+len(interior)) for _,interior in mono),Fraction(0))
    need(lhs == rhs == Fraction(1,2), 'thinning identity')
    return {'points':8,'orientation_triples':len(rows),'colorings_checked':256,'subsets_checked':256,'E0':0,'E1':8,'thinning_expectation':'1/2'}

def check_family():
    answers = []
    for k in range(1,16):
        red = [[2*i,2*i*i] for i in range(-k,k+1)]
        q = [0,1]
        r = len(red)
        all_rows = triangle_data(red+[q])
        red_rows = [(t,x) for t,x in all_rows if r not in t]
        blocked = sum(bool(interior) for _,interior in red_rows)
        need(blocked == k*k, 'family one-blocked count')
        need(sum(not interior for _,interior in red_rows) == comb(r,3)-k*k, 'family empty count')
        incidences = 0
        for pivot in range(r):
            cyclic = [(pivot+j)%r for j in range(1,r)]
            fans = [(pivot,cyclic[j],cyclic[j+1]) for j in range(r-2)]
            hit = sum(inside_sign(q,*(red[i] for i in t)) for t in fans)
            need(hit == 1, 'family per-pivot blocking')
            incidences += hit
        need(incidences == r, 'family blocker reuse')
        answers.append({'k':k,'red_points':r,'blocked_fan_incidences':incidences,'E0':comb(r,3)-k*k,'E1':k*k})
    return answers

def check_corpora(args):
    paths = [args.catalog,args.problems,args.reports]
    if not any(paths):
        return 'not requested'
    need(all(paths), 'all three corpus paths required')
    gate = read_json(ROOT / 'CORPUS_GATE.json')
    loaded = {}
    for key,path in zip(('catalog','problems','reports'),paths):
        p = Path(path)
        need(digest(p) == gate['corpora'][key]['digest'], 'corpus digest: '+key)
        loaded[key] = read_json(p)
        need(len(loaded[key]) == gate['corpora'][key]['entries'], 'corpus count: '+key)
    cat = [x for x in loaded['catalog'] if str(x.get('id'))=='3081']
    records = [x for x in loaded['problems'] if str(x.get('id'))=='3081']
    need(len(cat)==len(records)==1,'unique exact ID')
    v=records[0]; report=loaded['reports'].get(v['problem_number'],{})
    need(v['problem_number']==cat[0]['problem_number']=='OPG-2435','problem-number mismatch')
    need(cat[0]['rank']==926,'catalog rank')
    need('OPG-2435' not in loaded['reports'] and report == {},'unexpected report')
    pair=sha256(json.dumps([v,report],sort_keys=True).encode()).hexdigest()
    need(pair==gate['exact_pair_sha256']==cat[0]['review_hash'],'full pair hash')
    return {'complete_corpora_verified':True,'exact_pair_sha256':pair,'research_report_absent':True}

def check_sources(directory):
    if directory is None:
        return 'not requested; metadata integrity checked only'
    metadata = read_json(ROOT / 'SOURCE_VERIFICATION.json')
    count = 0
    for source in metadata['retrievals']:
        if source.get('status') != 200:
            continue
        p=Path(directory)/source['filename']
        need(digest(p)=={key:source[key] for key in ('bytes','sha256')}, 'source bytes: '+source['filename'])
        count += 1
    return {'source_files_verified':count}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ('catalog','problems','reports','source-dir'):
        parser.add_argument('--'+name)
    args=parser.parse_args()
    check_manifest()
    output={'status':'PASS','certificate':check_certificate(),'family':check_family(),'corpora':check_corpora(args),'sources':check_sources(args.source_dir),'scope':'finite exact certificates; no asymptotic solution'}
    print(json.dumps(output,sort_keys=True,indent=2))

if __name__=='__main__':
    try:
        main()
    except (ValueError,KeyError,OSError,TypeError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        sys.exit(1)
