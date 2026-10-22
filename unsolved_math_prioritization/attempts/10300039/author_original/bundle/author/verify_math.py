#!/usr/bin/env python3
"""Finite diagnostics and optional external identities; not mathematical proof."""
import argparse, hashlib, json, pathlib, sys
from fractions import Fraction as F

def require(x,msg):
    if not x: raise ValueError(msg)
def pairs(items):
    out={}
    for k,v in items:
        require(k not in out,'duplicate JSON key'); out[k]=v
    return out
def bad_constant(x): raise ValueError('nonfinite JSON constant')
def read_json(p):
    require(p.is_file() and not p.is_symlink(),'regular input required')
    return json.loads(p.read_text(encoding='utf-8'),object_pairs_hook=pairs,parse_constant=bad_constant)
def digest(b):return hashlib.sha256(b).hexdigest()
def check_file(p,expected):
    require(p.is_file() and not p.is_symlink(),'regular input required')
    b=p.read_bytes(); require(len(b)==expected['bytes'] and digest(b)==expected['sha256'],'external identity mismatch')
    return b

def diagnostics():
    count={k:0 for k in ['horosphere_halfspace','bounded_distance','holder_threshold','endpoint_annuli','ordered_insertions']}
    def ck(k,v):require(v,k+' diagnostic failed');count[k]+=1
    for i in range(1,65):
        r=F(i,65);z=r/2
        ck('horosphere_halfspace',0<z<r<1 and z*z<r*r)
        # Exterior points have small height as well.
        ck('horosphere_halfspace',(2*r)**2+z*z>r*r and z<1)
    for d in range(1,41):
        for R in range(0,11):
            for dist in [F(0),F(R,2),F(R)]:
                low=max(F(0),F(d)-dist)
                ck('bounded_distance',(F(d)+low-dist)/2 >= F(d)-R)
    for b in range(1,9):
        for a in range(1,b+1):
            exponent=b-2*a
            for k in range(1,9):
                term=F(2)**(exponent*k);nxt=F(2)**(exponent*(k+1))
                ck('holder_threshold',(nxt<term)==(F(a,b)>F(1,2)))
                ck('holder_threshold',(nxt==term)==(F(a,b)==F(1,2)))
    for n in range(1,129):
        for j in range(0,9):
            radial=F(n)+F(j,8)
            ck('endpoint_annuli',n<=radial<=n+1 and radial>=n-1)
    for m in range(1,33):
        sites=[F(i,3) for i in range(m)];weights=[F(1,2**(i+1)) for i in range(m)]
        points=[]
        for t,w in zip(sites,weights):
            A=sum((v for s,v in zip(sites,weights) if s<t),F(0))
            points.extend([t+A,t+A+w/2,t+A+w])
        for x,y in zip(points,points[1:]):ck('ordered_insertions',x<y)
        ck('ordered_insertions',sum(weights,F(0))<1)
    return {'kind':'finite_diagnostics_not_geometric_proof','families':count,'total':sum(count.values())}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--problems',type=pathlib.Path);parser.add_argument('--reports',type=pathlib.Path);parser.add_argument('--sources',type=pathlib.Path)
    a=parser.parse_args();require((a.problems is None)==(a.reports is None),'both corpora required together')
    root=pathlib.Path(__file__).resolve().parent;out={'diagnostics':diagnostics(),'corpus_binding':'not_requested','source_binding':'not_requested'}
    if a.problems is not None:
        m=read_json(root/'CORPUS_BINDINGS.json');pb=check_file(a.problems,m['corpora']['problems.json']);rb=check_file(a.reports,m['corpora']['research_results.json'])
        p=json.loads(pb,object_pairs_hook=pairs,parse_constant=bad_constant);r=json.loads(rb,object_pairs_hook=pairs,parse_constant=bad_constant)
        require(type(p)is list and len(p)==m['corpora']['problems.json']['records'],'problem corpus shape')
        require(type(r)is dict and len(r)==m['corpora']['research_results.json']['records'],'report corpus shape')
        selected=[x for x in p if x.get('id')==m['problem_id']];require(len(selected)==1,'target uniqueness');x=selected[0];y=r[m['problem_code']]
        for obj,key in [(x,'problem_record_sha256'),(y,'report_record_sha256'),([x,y],'record_pair_sha256')]:require(digest(json.dumps(obj,sort_keys=True).encode())==m[key],'record binding mismatch')
        require(digest(x['statement'].encode())==m['statement_utf8_sha256'],'statement binding mismatch')
        out['corpus_binding']='full_files_and_exact_target_records_match'
    if a.sources is not None:
        m=read_json(root/'SOURCE_METADATA.json')
        for x in m['documents']:check_file(a.sources/x['filename'],x)
        out['source_binding']='all_five_private_pdf_identities_match'
    print(json.dumps(out,sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(2)
