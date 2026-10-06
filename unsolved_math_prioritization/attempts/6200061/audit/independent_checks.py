#!/usr/bin/env python3
"""Independent frozen-archive, algebra, relocation and mutation checks.
No third-party dependencies; no network and no external writes beyond temp dirs.
Run: python3 independent_checks.py PATH_TO_AUTHOR_SAFE_FREEZE.zip
Optional: --corpora CATALOG_JSON PROBLEMS_JSON REPORTS_JSON
"""
import argparse
from fractions import Fraction as F
import hashlib
import io
import itertools
import json
import math
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

SHA='9d404dd597724c207e50afe80f97ec7f4b66e8c957193972fe2011c8853563d8'
MANIFEST_SHA='fc47e35e492d41ab4b1b1a49e3ed43bf4d5a275861e1f90e3028691b9d099f03'
REVIEW='19d550c8dd1630a33ab9f57396a75f3ff318fe849cdf8d4a4ad32469fe9fb258'
ROSTER={'README.md','PROOF.md','APPROACHES.md','IDENTITY.json','SOURCES.json','RESULTS.json','verify.py','test_suite.py','MANIFEST.json'}

def need(ok,message):
    if not ok: raise ValueError(message)
def digest(b): return hashlib.sha256(b).hexdigest()
def pair(q): return [q.numerator,q.denominator]
def run(root, optimized=False, suite=False):
    return subprocess.run([sys.executable]+(['-O'] if optimized else [])+[str(root/('test_suite.py' if suite else 'verify.py'))],cwd='/',capture_output=True,text=True,timeout=45)
def rehash(root,name):
    p=root/'MANIFEST.json';m=json.loads(p.read_text());b=(root/name).read_bytes()
    m['files'][name]={'bytes':len(b),'sha256':digest(b)};p.write_text(json.dumps(m,sort_keys=True))
def edit(root,name,fn):
    p=root/name;x=json.loads(p.read_text());fn(x);p.write_text(json.dumps(x,sort_keys=True));rehash(root,name)
def rewrite(root,name,b):
    (root/name).write_bytes(b);rehash(root,name)
def tree_data(r,n):
    count=(2*r)*(2*r-1)**(n-1)
    return {'rank':r,'depth':n,'cylinder_count':count,'cylinder_mass':pair(F(1,count)),
      'diameter_to_Q':pair(F(1,(2*r-1)**n)),'regularity_ratio':pair(F(2*r-1,2*r))}
def algebra(root):
    x=json.loads((root/'RESULTS.json').read_text());c=x['certificate']
    # Independently reconstruct the stated Bernstein polynomial in monomials.
    bern=[F(80),F(106),F(2038,15),F(168),F(1026,5),F(282),F(574)]
    poly=[sum(bern[i]*math.comb(6,i)*math.comb(6-i,k-i)*(-1)**(k-i) for i in range(k+1)) for k in range(7)]
    expected=[F(80),F(156),F(58),F(-32),F(66),F(164),F(82)]
    need(poly==expected,'Bernstein reconstruction');need(all(v>0 for v in bern),'Bernstein positivity')
    need(c['polynomial_monomial_coefficients']==[pair(v) for v in poly],'monomial data')
    need(c['polynomial_bernstein_coefficients']==[pair(v) for v in bern],'Bernstein data')
    # Derive model squared distances directly; do not import the author verifier.
    for k,row in enumerate(x['dyadic_samples'],1):
        t=F(1,2**k);d2=t**4/(1+t**4);y=1+2*t
        out2=(y*y-1)**2/(2*(1+y**4));r2=out2/d2
        need(row=={'k':k,'t':pair(t),'ratio_squared':pair(r2),'t_squared_ratio_squared':pair(t*t*r2)},'dyadic data')
        need(t*t*r2>=F(4,41),'model lower bound')
    need(len(x['dyadic_samples'])==80,'sample count')
    # Full polynomial identity also checked at 7 exact points, sufficient in degree <= 6.
    for t in map(F,range(7)):
        need(sum(poly[i]*t**i for i in range(7))==82*(1+t)**2*(1+t**4)-(1+(1+2*t)**4),'degree-six identity')
    trees=[tree_data(r,n) for r in range(2,9) for n in range(1,13)]
    need(x['free_tree_cylinders']==trees,'all cylinder data')
    coords=[0,1,3,7,8]
    ds=[[max(abs(coords[(i+h)%5]-coords[(j+h)%5]) for h in range(5)) for j in range(5)] for i in range(5)]
    defect=max(abs(abs(coords[(i+h)%5]-coords[(j+h)%5])-abs(coords[i]-coords[j])) for i,j,h in itertools.product(range(5),repeat=3))
    need(x['finite_supremum_example']=={'group':'cyclic_order_5','coordinates':coords,'additive_defect':defect,'invariant_metric':ds},'supremum data')
    # General multiplier regression; no claim that these rational multipliers occur in every surface.
    multipliers=[F(1001,1000),F(3,2),F(2),F(7,3),F(10)]
    for a,t in itertools.product(multipliers,[F(1,2**k) for k in range(0,31)]):
        b=a-1;r2=((b+a*t)**2-b*b)**2*(1+t**4)/(t**4*(1+b**4)*(1+(b+a*t)**4))
        lower=4*a*a*b*b/((1+b**4)*(1+(a+b)**4))
        need(t*t*r2>=lower,'general-multiplier inequality')
    # Exact Euclidean power-map distortion on triples spanning both signs.
    grid=list(map(F,range(-8,9)));qs_checks=0
    for a,b,c0 in itertools.permutations(grid,3):
        t=abs(a-b)/abs(a-c0);h=lambda z:z*abs(z)
        need(abs(h(a)-h(b))/abs(h(a)-h(c0))<=2*t*(2+t),'power-map QS regression')
        qs_checks+=1
    return {'bernstein_coefficients':7,'degree_six_identity_points':7,'dyadic_samples':80,'tree_cylinders':84,'supremum_group_order':5,'general_multiplier_samples':155,'power_map_distinct_triples':qs_checks,'geometry_formalized':False,'finite_samples_role':'regression_only'}
def controls(root,tmp):
    baseline=[]
    for opt in [False,True]:
        p=run(root,opt);need(p.returncode==0,p.stderr);baseline.append(json.loads(p.stdout))
    suite=run(root,suite=True);need(suite.returncode==0,suite.stderr)
    # Independent corruption roster; every rejecting case must fail in both modes.
    cases=[
      ('raw_proof_edit',lambda r:(r/'PROOF.md').write_text('not the original proof')),
      ('missing_results',lambda r:(r/'RESULTS.json').unlink()),
      ('extra_pdf',lambda r:(r/'copied_source.pdf').write_bytes(b'%PDF forbidden')),
      ('extra_directory',lambda r:(r/'extra').mkdir()),
      ('wrong_problem_rehashed',lambda r:edit(r,'IDENTITY.json',lambda j:j.update(problem_id=6200062))),
      ('wrong_rank_rehashed',lambda r:edit(r,'IDENTITY.json',lambda j:j.update(rank=811))),
      ('wrong_review_rehashed',lambda r:edit(r,'IDENTITY.json',lambda j:j.update(full_review_sha256='0'*64))),
      ('solved_rehashed',lambda r:edit(r,'IDENTITY.json',lambda j:j.update(general_conjecture_solved=True))),
      ('unmarked_refutation_rehashed',lambda r:edit(r,'IDENTITY.json',lambda j:j['scope_flags'].update(existential_attainment_disproved=True))),
      ('sample_generalization_rehashed',lambda r:edit(r,'IDENTITY.json',lambda j:j['scope_flags'].update(finite_samples_are_general_proof=True))),
      ('missing_corpus_metadata_rehashed',lambda r:edit(r,'IDENTITY.json',lambda j:j['source_corpora'].pop())),
      ('negative_bernstein_rehashed',lambda r:edit(r,'RESULTS.json',lambda j:j['certificate']['polynomial_bernstein_coefficients'].__setitem__(2,[-1,1]))),
      ('false_bound_rehashed',lambda r:edit(r,'RESULTS.json',lambda j:j['certificate'].update(squared_growth_lower_bound=[5,1]))),
      ('false_sample_rehashed',lambda r:edit(r,'RESULTS.json',lambda j:j['dyadic_samples'][10].update(ratio_squared=[1,1]))),
      ('false_cylinder_rehashed',lambda r:edit(r,'RESULTS.json',lambda j:j['free_tree_cylinders'][0].update(regularity_ratio=[1,1]))),
      ('false_supremum_rehashed',lambda r:edit(r,'RESULTS.json',lambda j:j['finite_supremum_example'].update(additive_defect=0))),
      ('noncanonical_fraction_rehashed',lambda r:edit(r,'RESULTS.json',lambda j:j['certificate'].update(squared_growth_lower_bound=[8,82]))),
      ('source_inclusion_rehashed',lambda r:edit(r,'SOURCES.json',lambda j:j['sources'][0].update(included_in_package=True))),
      ('duplicate_json_key_rehashed',lambda r:rewrite(r,'IDENTITY.json',b'{"schema":1,'+(r/'IDENTITY.json').read_bytes()[1:])),
      ('nonfinite_json_rehashed',lambda r:rewrite(r,'IDENTITY.json',(r/'IDENTITY.json').read_bytes().replace(b'"schema": 1',b'"schema": NaN'))),
      ('manifest_inflation',lambda r:(r/'MANIFEST.json').write_text((r/'MANIFEST.json').read_text().replace('PARTIAL_NOT_SOLVED','SOLVED'))),
    ]
    def symlink(r):
        p=r/'PROOF.md';b=p.read_bytes();p.unlink();q=tmp/'outside_proof';q.write_bytes(b);p.symlink_to(q)
    cases.append(('symlink_member',symlink))
    results=[]
    for name,fn in cases:
        r=tmp/name;shutil.copytree(root,r);fn(r)
        for opt in [False,True]:
            p=run(r,opt);need(p.returncode!=0 and 'VERIFICATION FAILED:' in p.stderr,'mutation accepted '+name)
        results.append({'case':name,'normal':'rejected','optimized':'rejected'})
    # Deliberately demonstrate the documented semantic boundary of a standalone verifier.
    limits=[
      ('rehashed_mathematical_prose',lambda r:rewrite(r,'PROOF.md',(r/'PROOF.md').read_bytes().replace(b'b=a-1>0',b'b=0'))),
      ('rehashed_plausible_corpus_hash',lambda r:edit(r,'IDENTITY.json',lambda j:j['source_corpora'][0].update(sha256='0'*64))),
      ('rehashed_source_title',lambda r:edit(r,'SOURCES.json',lambda j:j['sources'][0].update(title='Incorrect scholarly title'))),
    ]
    blind=[]
    for name,fn in limits:
        r=tmp/name;shutil.copytree(root,r);fn(r)
        for opt in [False,True]:
            p=run(r,opt);need(p.returncode==0,'standalone scope changed '+name)
        badzip=tmp/(name+'.zip')
        with zipfile.ZipFile(badzip,'w',zipfile.ZIP_DEFLATED) as zz:
            for f in sorted(r.iterdir()): zz.write(f,'kleinian_boundary_6200061/'+f.name)
        for opt in [False,True]:
            p=subprocess.run([sys.executable]+(['-O'] if opt else [])+[str(Path(__file__).resolve()),str(badzip)],cwd='/',capture_output=True,text=True,timeout=15)
            need(p.returncode!=0 and 'frozen archive external identity' in p.stderr,'external pin accepted '+name)
        blind.append({'case':name,'standalone_normal':'accepted','standalone_optimized':'accepted','pinned_archive_normal':'rejected','pinned_archive_optimized':'rejected','classification':'documented scope limitation; cannot match pinned frozen archive'})
    return {'relocated_baseline':baseline,'author_test_suite':json.loads(suite.stdout),'independent_rejection_cases':results,'independent_rejection_runs':len(results)*2,'semantic_limit_cases':blind,'semantic_limit_runs':len(blind)*2}
def corpus(paths):
    data=[Path(p).read_bytes() for p in paths];cat,problems,reports=[json.loads(b) for b in data]
    r=[j for j in problems if str(j['id'])=='6200061'];c=[j for j in cat if str(j['id'])=='6200061'];need(len(r)==len(c)==1,'target uniqueness')
    h=digest(json.dumps([r[0],reports.get(r[0]['problem_number'],{})],sort_keys=True).encode())
    need(h==REVIEW==c[0]['review_hash'],'complete review hash')
    sh=digest(r[0]['statement'].encode());need(sh==c[0]['statement_hash'],'statement hash')
    return {'full_review_sha256':h,'statement_sha256':sh,'rank':c[0]['rank'],'target_matches':True,'corpora':[{'filename':Path(p).name,'bytes':len(b),'sha256':digest(b),'record_count':len(j)} for p,b,j in zip(paths,data,[cat,problems,reports])]}
def main():
    p=argparse.ArgumentParser();p.add_argument('archive');p.add_argument('--corpora',nargs=3);a=p.parse_args()
    raw=Path(a.archive).read_bytes();need(len(raw)==30172 and digest(raw)==SHA,'frozen archive external identity')
    z=zipfile.ZipFile(io.BytesIO(raw));prefix='kleinian_boundary_6200061/'
    names=z.namelist();need(len(names)==len(set(names))==9,'duplicate/member count')
    need(set(names)=={prefix+n for n in ROSTER},'archive roster')
    for member in z.infolist(): need(not stat.S_ISLNK(member.external_attr>>16),'archive symlink')
    man=z.read(prefix+'MANIFEST.json');need(digest(man)==MANIFEST_SHA,'external manifest identity')
    out={'schema':1,'audit_result':'ACCEPTED_PARTIAL_NOT_SOLVED','general_problem_solved':False,'archive':{'filename':Path(a.archive).name,'bytes':len(raw),'sha256':digest(raw),'members':9,'manifest_sha256':digest(man)}}
    with tempfile.TemporaryDirectory(prefix='independent_problem61_') as td:
        tmp=Path(td);root=tmp/'relocated';root.mkdir()
        for name in ROSTER:(root/name).write_bytes(z.read(prefix+name))
        out['algebra']=algebra(root);out['controls']=controls(root,tmp)
    if a.corpora:
        out['corpus_identity']=corpus(a.corpora)
        ident=json.loads(z.read(prefix+'IDENTITY.json'))
        need({j['filename']:j for j in out['corpus_identity']['corpora']}=={j['filename']:j for j in ident['source_corpora']},'complete corpus metadata equality')
        need(out['corpus_identity']['rank']==ident['rank'],'catalog rank equality')
        need(out['corpus_identity']['statement_sha256']==ident['record_statement_sha256'],'statement digest equality')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:print('INDEPENDENT AUDIT FAILED: '+str(e),file=sys.stderr);sys.exit(1)
