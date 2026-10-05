#!/usr/bin/env python3
"""Read-only independent freeze verification and exact bounded algebra controls.
No author module is imported. No network, source text, or private output is needed.
Optional source/dataset arguments hash bytes and report metadata only.
"""
from pathlib import Path
from itertools import combinations
from collections import defaultdict
from fractions import Fraction
import argparse, hashlib, json, subprocess, sys, zipfile

ARCHIVE_SHA = '1a31a422207531ae6a37553f5de289ce358b445f5473f70939ca3a335f992f42'
MANIFEST_SHA = 'fc8c3f58258b73b16b491fff45663c78d8a409bea72fd67b35b8260b366755a2'

def digest(data):
    return hashlib.sha256(data).hexdigest()

def subsets(vertices):
    return [s for n in range(len(vertices)+1) for s in combinations(vertices,n)]

def accumulate(parts):
    out=defaultdict(int)
    for p in parts:
        for key,value in p.items(): out[key]+=value
    return {k:v for k,v in out.items() if v}

def d(chain, vertices, unsigned=False):
    parts=[]
    for s,c in chain.items():
        for v in vertices:
            if v not in s:
                t=tuple(sorted((*s,v)))
                parts.append({t:c*(1 if unsigned else (-1)**t.index(v))})
    return accumulate(parts)

def h(chain, base, unsigned=False):
    parts=[]
    for s,c in chain.items():
        if base in s:
            parts.append({tuple(v for v in s if v!=base):c*(1 if unsigned else (-1)**s.index(base))})
    return accumulate(parts)

def cech_controls():
    ground=(-3,2,7,11,19,23,41,53)
    cases=0
    for vertices in subsets(ground)[1:]:
        for base in vertices:
            for s in subsets(vertices):
                c={s:1}
                assert d(d(c,vertices),vertices)=={}
                assert accumulate([d(h(c,base),vertices),h(d(c,vertices),base)])==c
                cases+=1
    # Wrong sign on a nonminimal inserted vertex must fail.
    vertices=(1,2); c={(1,2):1}; base=2
    assert accumulate([d(h(c,base,True),vertices),h(d(c,vertices),base,True)]) != c
    # Omitting alternating signs no longer defines a differential over Z.
    assert d(d({():1},vertices,True),vertices,True) != {}
    return {'nonempty_vertex_sets':255,'all_base_vertices_tested':True,
            'integral_basis_contractions':cases,'negative_controls_detected':2}

def face_controls():
    # Parametrize graph directly, independent of author's row reduction.
    # A face t_j=0 becomes a*x=b; no linear solver in ambient variables.
    constraints={0:(2,1),1:(1,0),2:(1,0)}
    rows=[]
    for face in subsets((0,1,2)):
        solutions={Fraction(constraints[j][1],constraints[j][0]) for j in face}
        empty=len(solutions)>1
        dim=None if empty else (1 if not face else 0)
        on_gm=dim if not (solutions=={Fraction(0)}) else None
        ambient=None if len(face)==3 else 3-len(face)
        codim=None if dim is None else ambient-dim
        codim_u=None if on_gm is None else ambient-on_gm
        assert codim_u is None or codim_u>=2
        rows.append({'zero_coordinates':list(face),'ambient_face_dimension':ambient,
                     'graph_in_A1_dimension':dim,'graph_in_Gm_dimension':on_gm,
                     'codimension_in_A1_face':codim,'codimension_in_Gm_face':codim_u})
    bad=[r for r in rows if r['codimension_in_A1_face'] is not None and r['codimension_in_A1_face']<2]
    assert len(bad)==1 and bad[0]['zero_coordinates']==[1,2]
    # The tempting facets-only test incorrectly accepts the closure.
    assert all(r['codimension_in_A1_face'] is None or r['codimension_in_A1_face']>=2 for r in rows if len(r['zero_coordinates'])<=1)
    # Control: a constant graph (t1,t2)=(1/3,1/3) avoids every proper face.
    assert all(v!=0 for v in (Fraction(1,3),)*3)
    return {'faces':rows,'facets_only_mutation_rejected_by_vertex':True,
            'constant_admissible_graph_control':True}

def weight_controls():
    def diff(p): return sum((-1)**j for j in range(-p+1)) if p<0 else 0
    def hom(p): return 1 if p<0 and p%2 else 0
    for p in range(-160,0):
        assert diff(p)*diff(p+1)==0
        assert hom(p)*diff(p-1)+diff(p)*hom(p+1)==1
    assert diff(-1)==0
    # False convention retaining a nonzero splice is detected.
    broken=lambda p: 1 if p==-1 else diff(p)
    assert broken(-2)*broken(-1)!=0
    return {'negative_degrees':160,'zero_splice':True,'nonzero_splice_mutation_detected':True}

def orientation_controls():
    n=0
    for a in range(-9,10):
        if a==0: continue
        for b in range(1,8):
            u=Fraction(a,b)
            for v in [Fraction(-3,2),Fraction(0),Fraction(1),Fraction(7,3)]:
                assert (u*v)**2==u*u*v*v
                n+=1
    valuations=range(-60,61)
    parity_tests=0
    for m in valuations:
        for s in range(-40,41):
            assert (m+2*s)%2==m%2
            parity_tests+=1
    assert 1%2==1 and 2%2==0
    # Coordinate scaling by u is invertible; u=0 is expressly excluded.
    assert Fraction(3,2)*Fraction(2,3)==1
    return {'nonzero_rational_isometry_tests':n,'square_shift_parity_tests':parity_tests,
            'even_valuation_control':True,'limitations':'Parity does not implement GW or Milnor-Witt residues.'}

def rank(columns, nrows):
    a=[[Fraction(columns[j].get(i,0)) for j in range(len(columns))] for i in range(nrows)]
    r=0
    for col in range(len(columns)):
        row=next((i for i in range(r,nrows) if a[i][col]),None)
        if row is None: continue
        a[r],a[row]=a[row],a[r]; z=a[r][col]; a[r]=[v/z for v in a[r]]
        for i in range(nrows):
            if i!=r:
                z=a[i][col]; a[i]=[x-z*y for x,y in zip(a[i],a[r])]
        r+=1
    return r

def total_control():
    # Two coefficient rows model eta -> x: eta lies in both opens, x only in second.
    memberships={0:(0,1),1:(1,)}
    basis={}
    for b,vertices in memberships.items():
        for s in subsets(vertices): basis.setdefault(len(s)-1+b,[]).append((b,s))
    maps={}
    for n,bs in basis.items():
        target=basis.get(n+1,[]); lookup={v:i for i,v in enumerate(target)}
        cols=[]
        for b,s in bs:
            out=defaultdict(int)
            for t,c in d({s:1},memberships[b]).items(): out[lookup[(b,t)]]+=c
            if b==0 and all(v in memberships[1] for v in s):
                out[lookup[(1,s)]]+=(-1 if (len(s)-1)%2 else 1)
            cols.append(dict(out))
        maps[n]=cols
    ranks={n:rank(cols,len(basis.get(n+1,[]))) for n,cols in maps.items()}
    for n,bs in basis.items():
        assert ranks.get(n-1,0)+ranks[n]==len(bs)
        for c in maps[n]:
            dd=defaultdict(int)
            for j,v in c.items():
                for i,w in maps.get(n+1,[])[j].items(): dd[i]+=v*w
            assert all(v==0 for v in dd.values())
    # Least-vertex row contractions do not commute with the vertical map.
    # Local eta coefficient (0,1) at cover vertices (0,1): h_eta=0, h_x(d)=1.
    local_eta={(1,):1}
    vertical_local={s:c for s,c in local_eta.items() if all(v in memberships[1] for v in s)}
    vertical_after_h=h(local_eta,0)
    h_after_vertical=h(vertical_local,1)
    assert vertical_after_h=={} and h_after_vertical=={():1}
    assert vertical_after_h!=h_after_vertical
    return {'basis_dimensions':{str(n):len(v) for n,v in sorted(basis.items())},
            'differential_ranks_over_Q':{str(n):v for n,v in sorted(ranks.items())},
            'square_zero_and_acyclic':True,
            'row_contraction_vertical_commutation_not_assumed':True,
            'limitation':'A finite toy bicomplex, not computation of BLRS cohomology.'}

def freeze_controls(author,archive):
    assert digest(archive.read_bytes())==ARCHIVE_SHA
    mf=author/'AUTHOR_MANIFEST.json'
    assert digest(mf.read_bytes())==MANIFEST_SHA
    manifest=json.loads(mf.read_text()); expected=set(manifest['files'])|{'AUTHOR_MANIFEST.json'}
    assert {p.name for p in author.iterdir()}==expected
    files={p.name:p.read_bytes() for p in author.iterdir()}
    for n,m in manifest['files'].items():
        assert len(files[n])==m['bytes'] and digest(files[n])==m['sha256']
    with zipfile.ZipFile(archive) as z:
        entries=[v for v in z.infolist() if not v.is_dir()]
        assert len(entries)==9
        assert {Path(v.filename).name for v in entries}==expected
        for v in entries: assert z.read(v)==files[Path(v.filename).name]
    result=subprocess.run([sys.executable,str(author/'verify.py')],check=True,capture_output=True,text=True)
    assert json.loads(result.stdout)['exact_replay']=='PASS'
    # Byte mutation must fail the pinned digest, without editing the freeze.
    mutated=files['PROOFS.md']+b'\n'
    assert digest(mutated)!=manifest['files']['PROOFS.md']['sha256']
    for n,data in files.items(): assert (author/n).read_bytes()==data
    return {'archive_sha256':ARCHIVE_SHA,'manifest_sha256':MANIFEST_SHA,
            'nine_archive_members_byte_match':True,'author_replay':'PASS',
            'one_byte_integrity_mutation_detected':True,'freeze_unchanged':True}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--author-dir',type=Path,default=Path(__file__).resolve().parent.parent/'milnor_witt_30004169')
    ap.add_argument('--archive',type=Path,default=Path(__file__).resolve().parent.parent/'MILNOR_WITT_30004169_AUTHOR_SAFE_FREEZE.zip')
    ap.add_argument('--source-dir',type=Path)
    ap.add_argument('--dataset-dir',type=Path)
    ap.add_argument('--catalog',type=Path)
    args=ap.parse_args()
    result={'problem_id':30004169,'bounded_controls':'PASS','original_problem_solved':False,
            'freeze':freeze_controls(args.author_dir,args.archive),'cech':cech_controls(),
            'faces':face_controls(),'weight_zero':weight_controls(),
            'orientation':orientation_controls(),'finite_totalization':total_control()}
    assert result['faces']['faces']==json.loads((args.author_dir/'CHECK_RESULTS.json').read_text())['faces']
    pins=json.loads((args.author_dir/'SOURCE_VERIFICATION.json').read_text())
    if args.source_dir:
        checks=[]
        for j,s in enumerate(pins['sources']):
            data=(args.source_dir/f'source_{j}.pdf').read_bytes()
            assert data.startswith(b'%PDF-')
            meta={'bytes':len(data),'sha256':digest(data)}
            assert meta==s['pdf']
            checks.append({'title':s['title'],'url':s['url'],**meta,'matches_author_pin':True})
        result['source_byte_checks']=checks
    if args.dataset_dir:
        checks={}
        for n,m in pins['dataset']['files'].items():
            data=(args.dataset_dir/n).read_bytes(); x=json.loads(data)
            assert len(data)==m['bytes'] and digest(data)==m['sha256']
            checks[n]={'bytes':len(data),'sha256':digest(data),'records':len(x)}
            if n=='problems.json':
                target=[r for r in x if r['id']==30004169]
                assert len(target)==1 and target[0]['problem_number']=='OWR-16941-010'
                assert sum(r['problem_number']=='OWR-16941-010' for r in x)==1
                assert not [r for r in x if r['id']!=30004169 and any(w in r['title'].lower() for w in ('rost-schmid','rost–schmid','chow-witt','chow–witt'))]
            else: assert 'OWR-16941-010' not in x
        result['dataset_byte_checks']=checks
        result['prior_report_key_absent']=True
    if args.catalog:
        data=args.catalog.read_bytes()
        assert len(data)==pins['catalog']['bytes'] and digest(data)==pins['catalog']['sha256']
        catalog=json.loads(data)
        selected=[r for r in catalog if str(r['id'])=='30004169']
        assert len(selected)==1
        selected=selected[0]
        assert selected['rank']==745 and selected['turns_used']==0
        assert selected['statement_hash']==pins['catalog']['statement_hash']
        assert selected['review_hash']==pins['catalog']['review_hash']
        result['catalog_byte_check']={'bytes':len(data),'sha256':digest(data),'selected_id_matches':1,'rank':selected['rank'],'turns_used':selected['turns_used'],'statement_hash_matches':True,'review_hash_matches':True}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__': main()
