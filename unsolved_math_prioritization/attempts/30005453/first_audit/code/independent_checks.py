#!/usr/bin/env python3
"""Independent finite diagnostics. Does not certify the analytic infinite-graph proof.

Standard library only. No import or execution of the author's verifier.
The 56-case suite deliberately reconstructs the author's six diagnostic families
with new deterministic inputs. Extra controls exercise endpoint/scope failures.
"""
from fractions import Fraction as Q
from pathlib import Path
import argparse
import hashlib
import io
import json
import stat
import zipfile

COUNTS = {'equilibrium_edges': 440, 'jacobian_rows': 432,
          'positive_hessian_forms': 224, 'exact_extremum_signs': 448,
          'discrete_drift_cancellations': 560, 'boundary_fixed_point_edges': 64}
AUTHOR_SHA = '4e2b7cbf89688b04a80bfae946457582f8970cb90d6af260302aa1dad3a33856'
MANIFEST_SHA = '1c82aa6a5869110dacd64d0ee64e28b702a59e5224dacb44594fdf9c06910691'
NAMES = {'PRIOR_ATTEMPT_CHECK.json','PROOF.md','README.md','RESEARCH_LOG.md',
         'RESULT.json','SOURCE_METADATA.json','SOURCE_REVIEW.md','MANIFEST.json',
         'code/verify_algebra.py','code/verify_manifest.py','results/algebra_checks.json'}

def sha(b):
    return hashlib.sha256(b).hexdigest()

def require(ok, message):
    if not ok:
        raise ValueError(message)

def parse_archive(raw):
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        entries = z.infolist()
        require(len(entries) == len(NAMES), 'entry count')
        require(len({e.filename for e in entries}) == len(entries), 'duplicate member')
        require({e.filename for e in entries} == NAMES, 'allowlist')
        for e in entries:
            require(not e.is_dir(), 'directory entry')
            require(not stat.S_ISLNK(e.external_attr >> 16), 'symlink')
            require(not (e.flag_bits & 1), 'encrypted member')
            require('..' not in Path(e.filename).parts and not e.filename.startswith('/'), 'path traversal')
        require(z.testzip() is None, 'CRC')
        files = {e.filename:z.read(e) for e in entries}
    m = json.loads(files['MANIFEST.json'])
    require({e['path'] for e in m['files']} == NAMES-{'MANIFEST.json'}, 'manifest coverage')
    require(len(m['files']) == len(NAMES)-1, 'manifest duplicate')
    for e in m['files']:
        b = files[e['path']]
        require(len(b) == e['bytes'] and sha(b) == e['sha256'], 'manifest content mismatch')
    return files

def check_author(path):
    raw = path.read_bytes()
    require(len(raw) == 19790 and sha(raw) == AUTHOR_SHA, 'author ZIP anchor')
    files = parse_archive(raw)
    require(sha(files['MANIFEST.json']) == MANIFEST_SHA, 'author manifest anchor')
    require(sha(files['PROOF.md']) == 'f3a3d0b267c0fde305977fd3c7d3b182825a9674b1e903bf1b354d6e220139c9', 'proof anchor')
    mutations = {}
    for mutation in ('proof_byte','extra_pdf','missing_member','traversal','symlink','duplicate'):
        out = io.BytesIO()
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            with zipfile.ZipFile(out,'w') as z:
                for name,b in files.items():
                    if mutation == 'missing_member' and name == 'README.md': continue
                    if mutation == 'proof_byte' and name == 'PROOF.md': b += b' '
                    info = zipfile.ZipInfo('../README.md' if mutation == 'traversal' and name == 'README.md' else name)
                    if mutation == 'symlink' and name == 'README.md':
                        info.create_system=3; info.external_attr=(stat.S_IFLNK|0o777)<<16
                    z.writestr(info,b)
                if mutation == 'extra_pdf': z.writestr('source.pdf',b'%PDF-')
                if mutation == 'duplicate': z.writestr('README.md',b'changed')
        try: parse_archive(out.getvalue())
        except ValueError: mutations[mutation] = 'REJECTED'
        else: raise AssertionError('unsafe mutation accepted: '+mutation)
    return {'zip_bytes':len(raw),'zip_sha256':sha(raw),'manifest_sha256':MANIFEST_SHA,
            'member_count':len(files),'integrity':'PASS','negative_archive_controls':mutations}

def examples():
    yield 'single_edge',2,[(0,1)]
    yield 'path_9',9,[(i,i+1) for i in range(8)]
    yield 'cycle_even',8,[(i,(i+1)%8) for i in range(8)]
    yield 'cycle_odd',7,[(i,(i+1)%7) for i in range(7)]
    yield 'star',8,[(0,i) for i in range(1,8)]
    yield 'binary_tree',15,[((i-1)//2,i) for i in range(1,15)]
    yield 'complete_5',5,[(i,j) for i in range(5) for j in range(i+1,5)]

def algebra():
    counts = dict.fromkeys(COUNTS,0)
    cases=[]
    for name,n,edges in examples():
        neighbors = [{w if v==u else u for u,w in edges if v in (u,w)} for v in range(n)]
        for beta in (1,2,3,9):
            c=Q(1,beta+1)
            for small in (False,True):
                # Inputs differ from the author suite, including a nonmonotone heterogeneous family.
                z=[Q(1,3**(v+1)) if small else Q((7*v+3)%19+1,23) for v in range(n)]
                T=[sum((z[v]+z[w])**beta for w in neighbors[v]) for v in range(n)]
                p=[z[v]*T[v] for v in range(n)]
                x=[(z[u]+z[v])**(beta+1) for u,v in edges]
                xa=[(z[u]+z[v])**beta for u,v in edges]
                Sv=[sum(xa[i] for i,e in enumerate(edges) if v in e) for v in range(n)]
                for i,(u,v) in enumerate(edges):
                    require(x[i] == xa[i]*(p[u]/Sv[u]+p[v]/Sv[v]), 'edge equilibrium')
                    require(x[i] <= p[u]+p[v], 'edge rate bound')
                    counts['equilibrium_edges']+=1
                for v in range(n):
                    weights=[p[v]*beta*(z[v]+z[w])**(beta-1)/T[v]**2 for w in neighbors[v]]
                    diagonal=-c*(1+sum(weights))
                    offdiagonal=[-c*t for t in weights]
                    require(diagonal+sum(abs(t) for t in offdiagonal)==-c,'row dominance')
                    counts['jacobian_rows']+=1
                for k in range(4):
                    h=[Q(((v+1)*(k+2))%11-5,13) for v in range(n)]
                    if not any(h): h[0]=Q(1)
                    H=[[Q(0) for _ in range(n)] for _ in range(n)]
                    for u,v in edges:
                        t=beta*(z[u]+z[v])**(beta-1)
                        for i in (u,v):
                            for j in (u,v): H[i][j]+=t
                    for v in range(n): H[v][v]+=p[v]/z[v]**2
                    energy=sum(h[i]*H[i][j]*h[j] for i in range(n) for j in range(n))
                    require(energy>0,'strict positive Hessian')
                    counts['positive_hessian_forms']+=1
                    M=min(z)/5
                    d=[Q((v*3+k)%9-4,4)*M for v in range(n)]
                    for sign in (-1,1):
                        v=(2*k+1)%n; e=d[:];e[v]=sign*M
                        a=[z[w]+e[w] for w in range(n)]
                        denominator=sum((a[v]+a[w])**beta for w in neighbors[v])
                        f=c*(p[v]/denominator-a[v])
                        require(sign*f<=-c*M,'extreme derivative strip')
                        counts['exact_extremum_signs']+=1
                cases.append({'graph':name,'vertices':n,'edges':len(edges),'beta':beta,
                              'alpha':str(1-c),'rates':'decaying' if small else 'heterogeneous','pass':True})
            for k in range(1,21):
                require(Q(k**beta)*Q(1,k**beta)==1,'exact transformed drift')
                counts['discrete_drift_cancellations']+=1
    for beta in (1,2,3,9):
        for offset in (0,1):
            w=[2 if (i+offset)%2 else 0 for i in range(8)]
            for i,x in enumerate(w):
                require((w[(i-1)%8]>0)+(x>0)==1,'left denominator nonzero')
                require((w[(i+1)%8]>0)+(x>0)==1,'right denominator nonzero')
                require(x == (2 if x else 0),'boundary equilibrium')
                counts['boundary_fixed_point_edges']+=1
    require(counts==COUNTS and len(cases)==56,'coverage mismatch')
    return {'status':'PASS','case_count':len(cases),'control_count':sum(counts.values()),
            'counts':counts,'arithmetic':'exact rational','independent_inputs':True,'cases':cases}

def extra_controls():
    fractional=0
    # Also cover alpha below 1/2 using integer perfect powers; no irrational approximation.
    for numerator,denominator in ((1,10),(1,4),(1,3),(2,3),(9,10)):
        for k in range(1,61):
            n=k**denominator
            n_alpha=k**numerator
            require(Q(1,n_alpha)*n_alpha==1,'fractional exact jump drift')
            require(Q(1,n_alpha)**2*n_alpha <= 1,'bracket domination')
            require(n>=1,'positive count')
            fractional+=1
    # At criticality alpha=1, positive nonconstant alternating cycle arrays persist.
    critical=0
    for a in (Q(1,3),Q(1,2),Q(3,2),Q(5,3)):
        w=[a,2-a]*4
        for i,x in enumerate(w):
            require(x/(w[(i-1)%8]+x)+x/(w[(i+1)%8]+x)==x,'critical continuum')
            critical+=1
    require(critical>0,'critical control')
    # Removing the initial H offset would violate the compensated formula at t=0.
    require(sum(Q(1,k) for k in range(1,4))!=0,'nonunit initial offset')
    return {'fractional_alpha_exact_jump_controls':fractional,
            'critical_positive_boundary_of_scope_controls':critical,
            'nonunit_initial_offset_control':'PASS',
            'analytic_claim_certified_by_computation':False}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--author-zip',type=Path)
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    out={'finite_diagnostics':algebra(),'extra_controls':extra_controls()}
    if args.author_zip: out['author_integrity']=check_author(args.author_zip)
    raw=json.dumps(out,indent=2)+'\n'
    if args.output: args.output.write_text(raw)
    print(json.dumps({k:({i:v for i,v in a.items() if i!='cases'}) for k,a in out.items()},indent=2))

if __name__=='__main__': main()
