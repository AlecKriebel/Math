#!/usr/bin/env python3
"""Read-only independent finite-algebra, custody, and exact-closure checks.

No author program is imported or executed. No network or service is accessed.
The analytic L2 proof and limitations are in REPORT.md; this is not a proof
assistant certificate for arbitrary measurable fields.
"""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import gzip
import hashlib
import json

ROOT = Path(__file__).resolve().parent
HEAD = 'e026f83da374407d6a020949feb738460b76aea3'
BASE = '4b27092a448d53b61408355ce44ec38d103a1ce4'


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(name):
    return json.loads((ROOT / name).read_text())


def rank(rows):
    a = [list(map(F, row)) for row in rows]
    if not a:
        return 0
    cols = len(a[0])
    require(all(len(row) == cols for row in a), 'ragged matrix')
    pivot = 0
    for col in range(cols):
        j = next((j for j in range(pivot, len(a)) if a[j][col]), None)
        if j is None:
            continue
        a[pivot], a[j] = a[j], a[pivot]
        d = a[pivot][col]
        a[pivot] = [x / d for x in a[pivot]]
        for j in range(len(a)):
            if j != pivot and a[j][col]:
                d = a[j][col]
                a[j] = [x - d*y for x, y in zip(a[j], a[pivot])]
        pivot += 1
        if pivot == len(a):
            break
    return pivot


def gram(rows, residue=None, n=2):
    cols = range(len(rows[0]))
    if residue is not None:
        cols = [j for j in cols if j % n == residue]
    return [[sum((F(a[j])*F(b[j]) for j in cols), F(0))
             for b in rows] for a in rows]


def criterion(rows, n=2):
    return rank(gram(rows)) == sum(rank(gram(rows, k, n)) for k in range(n))


def direct_half_translation(rows):
    # Actual n=2 multiplier D = diag((-1)^ell), no Gramian used here.
    shifted = [[F(x) * (-1 if j % 2 else 1) for j, x in enumerate(row)]
               for row in rows]
    return rank(rows + shifted) == rank(rows)


def spectral_stability(rows, n):
    # For general n, use the spectral projections of the n-root multiplier.
    base = rank(rows)
    return all(rank(rows + [[x if j % n == k else 0
                             for j, x in enumerate(row)] for row in rows])
               == base for k in range(n))


def mm(a, b):
    return [[sum((x*y for x, y in zip(row, col)), F(0))
             for col in zip(*b)] for row in a]


def matrix_checks():
    counts = {}
    passed_invariant = 0
    for r, c, alphabet, name in [(2, 3, (-1, 0, 1), 'ternary_2_by_3'),
                                 (3, 4, (0, 1), 'binary_3_by_4')]:
        count = 0
        for entries in product(alphabet, repeat=r*c):
            rows = [list(entries[i*c:(i+1)*c]) for i in range(r)]
            answer = direct_half_translation(rows)
            require(criterion(rows) == answer, 'rank/direct D disagreement')
            # The Gramian row-rank identity is also checked independently.
            require(rank(gram(rows)) == rank(rows), 'Gram rank identity')
            count += 1
            passed_invariant += int(answer)
        counts[name] = count
    require(sum(counts.values()) == 4825, 'exhaustive count')

    a = [[F(1,2), F(1,2), F(1,2), F(1,2)],
         [F(1,2), F(-1,2), F(1,2), F(-1,2)]]
    b = [[F(1,2), F(1,2), F(1,2), F(1,2)],
         [F(1,2), F(1,2), F(-1,2), F(-1,2)]]
    eye = [[F(1), F(0)], [F(0), F(1)]]
    require(gram(a) == eye and gram(b) == eye, 'normalized controls')
    require(all(bool(x) for row in a+b for x in row), 'same support controls')
    require(criterion(a) and direct_half_translation(a), 'invariant A')
    require(not criterion(b) and not direct_half_translation(b), 'noninvariant B')
    g0, g1 = gram(a, 0), gram(a, 1)
    require(mm(g0,g0) == g0 and mm(g1,g1) == g1, 'normalized projections')
    require(mm(g0,g1) == [[F(0),F(0)],[F(0),F(0)]], 'orthogonal projections')
    require(mm(gram(b,0), gram(b,0)) != gram(b,0), 'nonprojection control')
    unnormalized = [[1,1], [0,1]]
    require(criterion(unnormalized), 'unnormalized full space is invariant')
    require(sum(row[0]*row[1] for row in unnormalized) != 0,
            'orthogonality without normalization must fail')
    dependent = [[1,0],[2,0]]
    require(rank(gram(dependent)) == 1 and criterion(dependent), 'dependent guard')
    zero = [[0,0],[0,0]]
    require(rank(gram(zero)) == 0 and criterion(zero), 'zero guard')
    # Trace additivity always holds and cannot replace rank additivity.
    require(sum(gram(b,k)[i][i] for k in range(2) for i in range(2)) == 2
            and not criterion(b), 'trace-as-rank negative control')
    scalar_cases = 0
    for n in range(1,6):
        for pattern in product((0,1), repeat=6):
            rows = [list(pattern)]
            active = {j % n for j, x in enumerate(pattern) if x}
            expected = len(active) <= 1
            require(criterion(rows,n) == expected, 'scalar active-residue rule')
            require(spectral_stability(rows,n) == expected, 'scalar spectral test')
            scalar_cases += 1
    require(scalar_cases == 320, 'scalar count')

    # Exact Gaussian-rational arithmetic, independent of floating complex.
    def z(x=0,y=0): return (F(x),F(y))
    def add(x,y): return (x[0]+y[0],x[1]+y[1])
    def mul(x,y): return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])
    def conj(x): return (x[0],-x[1])
    def zsum(xs):
        ans=z()
        for x in xs: ans=add(ans,x)
        return ans
    def zmm(x,y):
        return [[zsum(mul(a,b) for a,b in zip(row,col)) for col in zip(*y)]
                for row in x]
    def zg(x, hermitian=True):
        return [[zsum(mul(a,conj(b) if hermitian else b) for a,b in zip(s,t))
                 for t in x] for s in x]
    u = [[z(F(3,5)),z(0,F(4,5))],[z(0,F(4,5)),z(F(3,5))]]
    za = zmm(u, [[z(x) for x in row] for row in a])
    ze = [[z(1),z()],[z(),z(1)]]
    require(zg(za) == ze, 'Hermitian conjugation control')
    require(zg(za,False) != ze, 'bilinear Gram must be rejected')
    return {'exhaustive_counts':counts, 'total_exhaustive':4825,
            'invariant_exhaustive':passed_invariant, 'scalar_cases_n_1_through_5':320,
            'guards':['zero','dependent','same_support_opposite_invariance',
                      'trace_is_not_rank','normalization_required_for_column_orthogonality',
                      'Hermitian_conjugation','all_zero_scalar_at_most_one'],
            'closure_counterexample':'analytic proof in REPORT.md, no numerical substitute',
            'all_explicit_require_guards_active':True}


def check_entries(entries, base, excluded=None):
    require(isinstance(entries,list), 'manifest entries type')
    names = [e['file'] for e in entries]
    require(len(names) == len(set(names)), 'duplicate manifest entries')
    for e in entries:
        rel = Path(e['file'])
        require(not rel.is_absolute() and '..' not in rel.parts, 'unsafe manifest path')
        q = base / rel
        require(q.is_file() and not q.is_symlink(), 'manifest member absent or symlink')
        data = q.read_bytes()
        require(len(data) == e['bytes'] and sha(data) == e['sha256'],
                'manifest digest mismatch: '+str(rel))
    actual = set()
    for q in base.rglob('*'):
        require(not q.is_symlink(), 'symlink in sealed closure')
        if q.is_file() and q != excluded:
            actual.add(q.relative_to(base).as_posix())
    require(set(names) == actual, 'sealed file-set mismatch')


def custody_checks():
    b=read_json('PR_BINDING.json')
    require(b['head']==HEAD and b['base']==BASE and b['state']=='open'
            and b['draft'] is True and b['queue_changed'] is False, 'PR binding')
    pr=read_json('private/pr.json')
    require(pr['head']['sha']==HEAD and pr['base']['sha']==BASE
            and pr['state']=='open' and pr['draft'] is True, 'captured PR identity')
    require(sha((pr.get('body') or '').encode())==b['body_sha256'], 'PR body digest')
    final=read_json('private/pr_final.json')
    require(final['head']['sha']==HEAD and final['base']['sha']==BASE
            and final['state']=='open' and final['draft'] is True, 'final PR identity')
    require((final.get('body') or '')==(pr.get('body') or ''), 'PR body changed')
    files=read_json('private/files.json')
    require(len(files)==8 and len(b['eight_blobs'])==8,'eight paths')
    prefix='unsolved_math_prioritization/attempts/30000035/'
    bypath={x['filename']:x for x in files}
    require(len(bypath)==8 and all(x.startswith(prefix) for x in bypath), 'scope')
    require(not any('QUEUE' in x for x in bypath), 'QUEUE excluded')
    for e in b['eight_blobs']:
        f=bypath[e['path']]
        require(f['status']=='added' and f['sha']==e['git_blob_sha'],'GitHub file binding')
        data=(ROOT/'private'/Path(e['path']).name).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==e['git_blob_sha'] and sha(data)==e['sha256']
                and len(data)==e['bytes'], 'exact eight blob bytes')
    manifest=read_json('private/MANIFEST.json')
    require(set(manifest['members'])=={Path(e['path']).name for e in b['eight_blobs']},
            'public manifest membership')
    require(manifest['self_hash_excluded']=='MANIFEST.json','public manifest self rule')
    require(len(manifest['entries'])==7,'public seven payload hashes')
    for e in manifest['entries']:
        data=(ROOT/'private'/e['file']).read_bytes()
        require(len(data)==e['bytes'] and sha(data)==e['sha256'],'public payload hash')

    c=read_json('GWS_CLEARANCE.json')
    data=(ROOT/'private/GWS_FULL43.json').read_bytes()
    require(sha(data)==c['sha256']=='fadcb0e361e60b8267883420bd979f37695303592a800019b65d7cb04ad7e8d1',
            'own fresh tracker digest')
    g=json.loads(data)
    require(g['spreadsheetId']=='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20', 'sheet identity')
    vr=g['valueRanges'][0]
    require(vr['dataFilters']==[{'gridRange':{'endColumnIndex':43,'sheetId':1254632077,
                                         'startColumnIndex':0}}], 'numeric full43 filter')
    values=vr['valueRange']['values']
    require(len(values)==c['rows_including_header']==191 and all(len(r)<=43 for r in values),
            'tracker dimensions')
    require(c['unresolved_duplicate_leads']==[], 'unresolved semantic duplicate lead')
    aliases=read_json('SOURCE_ALIASES.json')
    for token in aliases['tracker_no_hit_tokens']:
        require(not any(token.casefold() in '\t'.join(map(str,r)).casefold() for r in values),
                'uncleared source alias: '+token)
    require('0804.1597' in aliases['tracker_no_hit_tokens'], 'bare arxiv ID guard')

    rec=read_json('PRIMARY_RECEIPT.json')
    for e in rec['sources']:
        raw=(ROOT/'private'/e['name']).read_bytes()
        require(e['http']==200 and len(raw)==e['bytes'] and sha(raw)==e['sha256'],
                'primary receipt mismatch')
    for name in ['original.pdf','arxiv_v3.pdf','chui_sun.pdf']:
        require((ROOT/'private'/name).read_bytes().startswith(b'%PDF-'),'PDF bytes guard')
    require(not (ROOT/'private/published_response.html').read_bytes().startswith(b'%PDF-'),
            'publisher HTML must not be passed off as final PDF')
    require(gzip.decompress((ROOT/'private/source.gz').read_bytes())
            ==(ROOT/'private/arxiv_source.tex').read_bytes(), 'public TeX source binding')
    cross=read_json('private/crossref.json')['message']
    require(cross['DOI']=='10.1007/s00041-009-9068-y'
            and cross['title']==['Invariance of a Shift-Invariant Space'], 'DOI title identity')
    require([x['family'] for x in cross['author']]
            ==['Aldroubi','Cabrelli','Heil','Kornelson','Molter'], 'author identity')
    require(cross['volume']=='16' and cross['issue']=='1' and cross['page']=='60-75'
            and cross['published-print']['date-parts']==[[2010,2]]
            and cross['published-online']['date-parts']==[[2009,4,1]], 'journal dates')
    landing=(ROOT/'private/arxiv_landing.html').read_text()
    require(all(x in landing for x in ['0804.1597v1','0804.1597v2','0804.1597v3']),
            'arxiv version history')
    require('0804.1597v4' not in landing, 'later source version requires new audit')
    # Both nested manifests and every private response body are covered.
    check_entries(read_json('PRIVATE_BODY_SEAL.json')['entries'],ROOT/'private')
    seal_path=ROOT/'REVIEW_SEAL.json'
    require(seal_path.is_file(),'closure seal is required')
    check_entries(read_json('REVIEW_SEAL.json')['entries'],ROOT,excluded=seal_path)
    proposal=read_json('CELL_PROPOSAL.json')
    require(len(proposal['values'])==1 and len(proposal['values'][0])==4
            and proposal['values'][0][1]=='','exact four literal cells and blank B')
    require(proposal['values'][0][2]=='https://doi.org/10.1007/s00041-009-9068-y',
            'existing journal DOI only')
    require(proposal['service_write_performed'] is False,'proposal only')
    return {'head':HEAD,'base':BASE,'eight_added_blobs':8,'queue_changed':False,
            'own_full43_tracker_rows':191,'same_paper_aliases_cleared':True,
            'private_body_and_exact_recursive_closure_seals':'PASS',
            'published_final_pdf_inspected':False,'author_code_executed':False}


def main():
    try:
        require(False, 'deliberate guard probe')
    except RuntimeError:
        pass
    else:
        raise RuntimeError('explicit guard was incorrectly disabled')
    algebra=matrix_checks()
    custody=custody_checks()
    print(json.dumps({'status':'PASS','algebra':algebra,'custody':custody},indent=2,sort_keys=True))


if __name__=='__main__':
    main()
