#!/usr/bin/env python3
"""No candidate imports. Exact leading-minor reconstruction of all Schur pivots."""
from pathlib import Path
from fractions import Fraction as Q
import json,hashlib,argparse

def need(x,m):
    if not x:raise ValueError(m)

def determinant(a):
    # Fraction-free forward elimination; a zero column handles singular controls.
    a=[list(r)for r in a];n=len(a);prev=1;sign=1
    if not n:return 1
    for k in range(n-1):
        if not a[k][k]:
            pivot=next((i for i in range(k+1,n)if a[i][k]),None)
            if pivot is None:return 0
            a[k],a[pivot]=a[pivot],a[k];sign=-sign
        value=a[k][k]
        for i in range(k+1,n):
            for j in range(k+1,n):
                nom=a[i][j]*value-a[i][k]*a[k][j]
                need(nom%prev==0,'nonexact fraction-free step');a[i][j]=nom//prev
        for i in range(k+1,n):a[i][k]=0
        prev=value
    return sign*a[-1][-1]

def inv(w):return[-a for a in reversed(w)]
def comm(a,b):return a+b+inv(a)+inv(b)
def main():
    p=argparse.ArgumentParser();p.add_argument('--packet',type=Path,required=True);a=p.parse_args();root=a.packet
    c=comm([1,1],[2,2]);d=[-1,-1]+c+[1,1];e=[-2,-2]+c+[2,2]
    raw=comm(comm(c,d),comm(d,e));word=[]
    for x in raw:
        if word and word[-1]==-x:word.pop()
        else:word.append(x)
    cert=json.loads((root/'certificate.json').read_bytes());need(word==cert['word'],'nested word')
    runs=[]
    for x in word:
        if runs and abs(x)==runs[-1][0]:runs[-1][1]+=1 if x>0 else-1
        else:runs.append([abs(x),1 if x>0 else-1])
    need([v for _,v in runs]==cert['syllables'],'runs')
    N=sum(abs(v)for _,v in runs[1::2]);G=[[0]*N for _ in range(N)];start=0
    for (_,aa),(_,bb)in zip(runs[::2],runs[1::2]):
        G[start][start]+=aa
        for k in range(abs(bb)):
            x=(start+k)%N;y=(x+1)%N;sign=1 if bb>0 else-1
            for i,j,v in[(x,x,-sign),(y,y,-sign),(x,y,sign),(y,x,sign)]:G[i][j]+=v
        start+=abs(bb)
    need(G==cert['goeritz'],'entire reconstructed matrix')
    # All leading minors are nonzero for this fixed witness, so their ratios
    # recover the scalar Schur pivots without using the author's elimination.
    minors=[1]+[determinant([row[:k]for row in G[:k]])for k in range(1,N+1)]
    need(all(minors),'zero leading minor')
    pivots=[str(Q(y,x))for x,y in zip(minors,minors[1:])]
    need(pivots==cert['goeritz_pivots'],'all 48 Schur pivots')
    inertia=[sum(Q(p)>0 for p in pivots),sum(Q(p)<0 for p in pivots),0]
    need(inertia==[23,25,0]and minors[-1]==-7154819319988224,'inertia/determinant')
    labels=[0,1,2];counts={(0,1):0,(0,2):0,(1,2):0}
    for s in word:
        j=abs(s)-1;counts[tuple(sorted(labels[j:j+2]))]+=1 if s>0 else-1
        labels[j],labels[j+1]=labels[j+1],labels[j]
    need(labels==[0,1,2]and all(v==0 for v in counts.values()),'pure/linking')
    for m,expected in [([],1),([[0]],0),([[0,1],[1,0]],-1),([[1,1],[1,1]],0),([[0,2,0],[3,4,1],[1,0,5]],-28)]:need(determinant(m)==expected,'determinant control')
    print(json.dumps({'status':'PASS_INDEPENDENT_LEADING_MINORS','dimension':N,'word_length':len(word),'goeritz_inertia':inertia,'goeritz_determinant':minors[-1],'leading_minors':minors,'all48_pivots_matched':True,'pivots':pivots,'determinant_controls':5,'pure_permutation':labels,'pairwise_crossing_sums':list(counts.values()),'scope':'Finite matrix/group-word computation; diagram formula/topology/priority not certified.'},indent=2))
if __name__=='__main__':main()
