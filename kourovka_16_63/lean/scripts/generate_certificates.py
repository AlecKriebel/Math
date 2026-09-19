#!/usr/bin/env python3
"""Reconstruct the TWO new witnesses without SymPy, NumPy, Lean, or network.

By default compare the new witness files with deterministic reconstruction.
--write-generated rewrites ONLY integral_generation_certificate.json and
inner_left_inverse.json. It never changes the original paper artifacts or Lean
proof source. A generated witness is not a Lean proof; run the sound checker and
compile its acceptance declarations offline.
"""
from __future__ import annotations
import argparse,json,math,sys
from fractions import Fraction as F
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def load(name):return json.loads((ROOT/'data'/name).read_text())
def demand(p,msg):
    if not p:raise ValueError(msg)

def inner():
    terms=load('group_lie_presentation.json')['bracket_terms_i_lt_j']
    M=[[F(0) for _ in range(30)] for _ in range(961)]
    for i,j,k,c in terms:
        if i<30:M[k*31+j][i]+=c
        if j<30:M[k*31+i][j]-=c
    # Greedy lexicographic independent rows, with explicit rational reductions.
    basis={};rows=[]
    for i,row in enumerate(M):
        a=list(row)
        for pivot,b in sorted(basis.items()):
            c=a[pivot]
            if c:a=[x-c*y for x,y in zip(a,b)]
        pivot=next((j for j,x in enumerate(a) if x),None)
        if pivot is None:continue
        c=a[pivot];a=[x/c for x in a];basis[pivot]=a;rows.append(i)
        if len(rows)==30:break
    demand(len(rows)==30,'inner directions are not independent')
    A=[M[r]+[F(int(i==j)) for j in range(30)] for i,r in enumerate(rows)]
    for j in range(30):
        r=next((r for r in range(j,30) if A[r][j]),None)
        demand(r is not None,'selected minor singular')
        A[j],A[r]=A[r],A[j]
        c=A[j][j];A[j]=[x/c for x in A[j]]
        for r in range(30):
            if r==j:continue
            c=A[r][j]
            if c:A[r]=[x-c*y for x,y in zip(A[r],A[j])]
    demand(all(A[i][j]==int(i==j) for i in range(30) for j in range(30)),'inverse elimination failed')
    inv=[a[30:] for a in A]
    demand(all(sum(inv[i][k]*M[rows[k]][j] for k in range(30))==int(i==j)
          for i in range(30) for j in range(30)),'left inverse equation failed')
    return {'format':'inner-derivation-left-inverse-v1','selected_rows':rows,
            'inverse':[[str(a) for a in row] for row in inv],
            'source_count':30,'matrix_rows':961}

def integral_generation():
    d=load('generation_dag.json');terms=load('lie31_brackets.json')['terms']
    den=[];val=[]
    for k,n in enumerate(d['nodes']):
        op=n['op']
        if op=='input':
            dd=1;vv=[0]*31
            for j,a,b in d['input_vectors'][n['index']]:
                demand(b==1,'input not integral');vv[j]=a
        elif op=='scale':
            j=n['arg'];demand(j<k,'forward reference')
            dd=den[j]*n['denominator'];vv=[n['numerator']*a for a in val[j]]
        else:
            a,b=n['left'],n['right'];demand(max(a,b)<k,'forward reference')
            if op=='add':
                dd=math.lcm(den[a],den[b]);ca=dd//den[a];cb=dd//den[b]
                vv=[ca*x+cb*y for x,y in zip(val[a],val[b])]
            elif op=='bracket':
                dd=den[a]*den[b];vv=[0]*31
                for i,j,z,c in terms:vv[z]+=c*(val[a][i]*val[b][j]-val[a][j]*val[b][i])
            else:raise ValueError('unknown DAG operation')
        demand(dd>0 and dd%1009!=0,'denominator is not a p-adic unit')
        den.append(dd);val.append(vv)
    for t in d['targets']:
        k,j=t['node'],t['basis_index']
        demand(val[k]==[den[k]*int(i==j) for i in range(31)],'basis target failed')
    return {'denominators':den,'integer_node_values':val,'targets':d['targets'],
            'source':'generation_dag.json','status':'externally reconstructed; Lean proof source uncompiled'}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--write-generated',action='store_true')
    args=ap.parse_args()
    outcomes=[]
    for name,producer in [('inner_left_inverse.json',inner),('integral_generation_certificate.json',integral_generation)]:
        data=producer();path=ROOT/'data'/name
        if args.write_generated:path.write_text(json.dumps(data,indent=2)+'\n')
        else:demand(json.loads(path.read_text())==data,'reconstruction differs: '+name)
        outcomes.append({'file':name,'action':'rewritten' if args.write_generated else 'matched'})
    print(json.dumps({'status':'EXACT_WITNESS_REGENERATION_PASSED','lean_invoked':False,
                      'not_a_formal_proof':True,'outputs':outcomes},indent=2))
    return 0
if __name__=='__main__':sys.exit(main())
