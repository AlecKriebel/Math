#!/usr/bin/env python3
"""Exact geometry verification; no assertions or third-party dependencies."""
import argparse
from fractions import Fraction as Q
import json
from pathlib import Path
import re
import sys

class Invalid(ValueError):
    pass

def need(ok, message):
    if not ok: raise Invalid(message)

def fields(obj, keys, label):
    need(type(obj) is dict and set(obj)==set(keys), label+': unexpected schema')

def integer(x, label):
    need(type(x) is int,label+': integer required')
    return x

def rat(x):
    need(type(x) is str and re.fullmatch(r'-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?',x) is not None,
         'canonical rational string required')
    q=Q(x);need(str(q)==x,'noncanonical rational');return q

def no_duplicates(items):
    d={}
    for k,v in items:
        need(k not in d,'duplicate JSON key: '+k);d[k]=v
    return d

def reject_constant(s):
    raise Invalid('nonfinite JSON number: '+s)

def load(path):
    return json.loads(Path(path).read_text(),object_pairs_hook=no_duplicates,parse_constant=reject_constant)

def generated(d):
    need(type(d) is int and 2<=d<=64,'implementation dimension outside 2..64')
    k=d-1;boxes=[];witnesses=[]
    for q in range(3*k):
        j,r=divmod(q,3)
        bounds=[['-1','1'] for _ in range(k)]+[[str(2*q),str(2*q+1)]]
        bounds[j]=['-1','0'] if r==1 else ['0','1']
        boxes.append({'id':q,'coordinate':j,'role':r,'bounds':bounds})
        a=[Q(0)]*k;b=[Q(0)]*k;s=6*j
        if r==0:a[j]=Q(-s-4);b[j]=Q(1)
        elif r==1:a[j]=Q(1)
        else:a[j]=Q(s+1);b[j]=Q(-1)
        witnesses.append({'omitted':q,'intercepts':list(map(str,a)),'slopes':list(map(str,b)),
                          'epsilon_max':str(Q(1,6*k+2)),
                          'hits':[{'box':h,'t':str(Q(4*h+1,2))} for h in range(3*k) if h!=q]})
    return {'schema':'isolated-box-pinning-v1','problem_id':30001066,
            'classification':'partial_bound_counterexample','dimension':d,
            'claimed_minimal_size':3*k,'boxes':boxes,'deletion_witnesses':witnesses}

def verify(data):
    fields(data,['schema','problem_id','classification','dimension','claimed_minimal_size','boxes','deletion_witnesses'],'root')
    need(data['schema']=='isolated-box-pinning-v1','wrong schema')
    need(type(data['problem_id']) is int and data['problem_id']==30001066,'wrong problem')
    need(data['classification']=='partial_bound_counterexample','overclaimed classification')
    d=integer(data['dimension'],'dimension');need(2<=d<=64,'implementation dimension outside 2..64')
    k=d-1;n=3*k
    need(integer(data['claimed_minimal_size'],'size')==n,'wrong size claim')
    need(type(data['boxes']) is list and len(data['boxes'])==n,'wrong box count')
    need(type(data['deletion_witnesses']) is list and len(data['deletion_witnesses'])==n,'missing deletion witnesses')
    boxes={};groups={j:{} for j in range(k)}
    for box in data['boxes']:
        fields(box,['id','coordinate','role','bounds'],'box')
        i=integer(box['id'],'box id');j=integer(box['coordinate'],'coordinate');r=integer(box['role'],'role')
        need(0<=i<n and i not in boxes,'duplicate or out of range box')
        need(0<=j<k and 0<=r<3 and r not in groups[j],'duplicate or invalid triple member')
        bounds=box['bounds'];need(type(bounds) is list and len(bounds)==d,'wrong bounds dimension')
        parsed=[]
        for pair in bounds:
            need(type(pair) is list and len(pair)==2,'malformed interval')
            lo,hi=map(rat,pair);need(lo<hi,'box is not full dimensional');parsed.append((lo,hi))
        for h,(lo,hi) in enumerate(parsed[:-1]):
            need(lo<=0<=hi,'axis does not meet a transverse interval')
            if h==j:need(hi==0 if r==1 else lo==0,'missing active sign constraint')
        boxes[i]=(j,r,parsed);groups[j][r]=i
    # Strict separation of longitudinal slabs certifies disjoint closed boxes.
    for i in range(n):
        for h in range(i):
            ai,bi=boxes[i][2][-1];ah,bh=boxes[h][2][-1]
            need(bi<ah or bh<ai,'boxes lack strict longitudinal separation')
    # These hypotheses imply uniqueness by the affine interpolation proof.
    for j in range(k):
        need(set(groups[j])=={0,1,2},'incomplete triple')
        t=[boxes[groups[j][r]][2][-1] for r in range(3)]
        need(t[0][1]<t[1][0] and t[1][1]<t[2][0],'triple not strictly ordered')
    seen=set();hit_count=0
    for w in data['deletion_witnesses']:
        fields(w,['omitted','intercepts','slopes','epsilon_max','hits'],'witness')
        missing=integer(w['omitted'],'omitted');need(0<=missing<n and missing not in seen,'duplicate or invalid deletion')
        seen.add(missing)
        need(type(w['intercepts']) is list and type(w['slopes']) is list and len(w['intercepts'])==k and len(w['slopes'])==k,'wrong motion dimension')
        a=list(map(rat,w['intercepts']));b=list(map(rat,w['slopes']));e=rat(w['epsilon_max'])
        need(e>0,'nonpositive motion interval');need(any(a) or any(b),'motion is stationary')
        need(type(w['hits']) is list and len(w['hits'])==n-1,'missing hits');hit_ids=set()
        for hit in w['hits']:
            fields(hit,['box','t'],'hit');i=integer(hit['box'],'hit box')
            need(0<=i<n and i!=missing and i not in hit_ids,'duplicate or invalid hit')
            hit_ids.add(i);t=rat(hit['t']);bound=boxes[i][2]
            need(bound[-1][0]<=t<=bound[-1][1],'witness outside slab')
            for h in range(k):
                v=e*(a[h]+b[h]*t);lo,hi=bound[h]
                need(lo<=v<=hi and lo<=0<=hi,'trajectory leaves a retained box')
            # Convex intervals and the endpoints epsilon=0,e certify all real epsilon.
            hit_count+=1
        need(hit_ids==set(range(n))-{missing},'incomplete deletion coverage')
        j,r,bound=boxes[missing];ta,tb=bound[-1]
        va=a[j]+b[j]*ta;vb=a[j]+b[j]*tb
        need(min(va,vb)>0 if r==1 else max(va,vb)<0,'motion not proved to miss omitted box')
    need(seen==set(range(n)),'incomplete family of deletions')
    return {'dimension':d,'boxes':n,'pairwise_disjoint':True,'unique_global_transversal':True,
            'minimal_pinning':True,'continuous_deletion_certificates':n,'exact_hit_certificates':hit_count,
            'candidate_2d_minus_1_refuted':n>2*d-1}

def main():
    p=argparse.ArgumentParser();p.add_argument('certificate',nargs='?',type=Path,default=Path(__file__).with_name('certificate.json'))
    p.add_argument('--generated-dimension',type=int);args=p.parse_args()
    data=generated(args.generated_dimension) if args.generated_dimension is not None else load(args.certificate)
    print(json.dumps({'status':'PASS','result':verify(data)},sort_keys=True))

if __name__=='__main__':
    try:main()
    except (Invalid,ValueError,TypeError,KeyError,IndexError,OSError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
