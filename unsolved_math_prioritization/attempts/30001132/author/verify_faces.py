#!/usr/bin/env python3
"""Exact integer admissibility enumeration; authored, no external dependencies."""
import itertools,json
from pathlib import Path

def compose(a,b): return tuple(a[x-1] for x in b)
def inverse(a): return tuple(a.index(i)+1 for i in range(1,len(a)+1))
def length(w): return sum(a>b for i,a in enumerate(w) for b in w[i+1:])
def vertex(sigma):
    n=len(sigma)
    return tuple(tuple(i for i in range(1,n+1) if sigma[i-1]>r) for r in range(n))
def diagram(sigma):
    rows=vertex(sigma); out=[]
    for r in range(1,len(sigma)):
        for k,a in enumerate(rows[r]):
            pk=rows[r-1].index(a)
            assert pk in (k,k+1)
            typ='L' if pk==k else 'R'
            j=sigma[a-1]
            root=(r,j) if typ=='L' else (j,r)
            out.append(((r,k),(r-1,pk),root))
    return out

def gamma(sigma,b):
    bi=inverse(b)
    return tuple((a,c) for a,c,(i,j) in diagram(sigma) if bi[i-1]>bi[j-1])
def equal_at(v,eq):
    (r,k),(s,l)=eq; return v[r][k]==v[s][l]
def covers(w):
    n=len(w); ret=[]; l=length(w)
    for i in range(n):
        for j in range(i+1,n):
            u=list(w);u[i],u[j]=u[j],u[i];u=tuple(u)
            if length(u)==l-1: ret.append(u)
    return ret

def implied_eqs(eqs,n):
    # Faces considered contain a simple vertex. Thus the defining equations are
    # independent and their connected equality components give all forced
    # equalities (there is a relative-open neighborhood of that simple vertex).
    nodes=[(r,k) for r in range(n) for k in range(n-r)]
    parent={x:x for x in nodes}
    def root(x):
        while parent[x]!=x: x=parent[x]
        return x
    for a,b in eqs: parent[root(a)]=root(b)
    return {x:root(x) for x in nodes}
def subset_face(eqs_sub,eqs_super,n):
    c=implied_eqs(eqs_sub,n)
    return all(c[a]==c[b] for a,b in eqs_super)

def smooth(w):
    return not any(tuple(sorted(range(4), key=lambda j: w[ix[j]]) .index(j)+1 for j in range(4)) in ((3,4,1,2),(4,2,3,1)) for ix in itertools.combinations(range(len(w)),4))

def run(n):
    ps=list(itertools.permutations(range(1,n+1))); data=[]; bad=[]
    for w in ps:
        good=[];witnesses=[]
        for b in ps:
            s=compose(b,w);g=gamma(s,b)
            assert n*(n-1)//2-len(g)==length(w)
            fails=[]
            for u in covers(w):
                t=compose(b,u); h=gamma(t,b)
                if not subset_face(h,g,n):
                    omitted=[eq for eq in g if not equal_at(vertex(t),eq)]
                    fails.append({'predecessor':u,'sigma_predecessor':t,'vertex_outside':bool(omitted),'violated_equalities':omitted})
            if not fails: good.append(b)
            else: witnesses.append({'b':b,'sigma':s,'face_equalities':g,'failures':fails})
        if not good: bad.append(w)
        data.append({'w':w,'length':length(w),'smooth':smooth(w),'admissible_borels':good,'failed_borels':witnesses})
    return {'n':n,'nonrepresentable':bad,'records':data}
if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--output',default='results.json');args=p.parse_args()
    data=[run(n) for n in (2,3,4)]
    Path(args.output).write_text(json.dumps(data,indent=2)+'\n')
    for r in data:
        print('n=',r['n'],'nonrepresentable=',r['nonrepresentable'])
        for d in r['records']:
            if not d['admissible_borels']:
                print('  w=',d['w'],'length=',d['length'],'smooth=',d['smooth'],'all have vertex obstruction=',all(any(f['vertex_outside'] for f in b['failures']) for b in d['failed_borels']))
