#!/usr/bin/env python3
"""Exact external checks for the partial Lean development (standard library only).

This script does not invoke Lean and cannot certify any Lean declaration. It
reconstructs the ambient bracket from the raw transvectants via direct_flag.py,
validates the scaled table, checks the new left inverse with Fraction arithmetic,
and checks the cleared generation data against the original exact DAG. It also
compares the corresponding finite Lean literals, never treating a source hash as
a mathematical proof. Deliberate corruptions must fail at an equation check.
"""
from __future__ import annotations
import copy
import hashlib
import itertools
import json
import math
import platform
import re
import sys
import time
from fractions import Fraction as F
from pathlib import Path
import direct_flag as ambient

ROOT=Path(__file__).resolve().parents[1]
P,D=1009,31
class EvidenceError(RuntimeError): pass

def require(ok:bool, label:str):
    if not ok: raise EvidenceError(label)

def read(name:str): return json.loads((ROOT/'data'/name).read_text())
def dense(v): return [v.get(i,F(0)) for i in range(D)]
def sparse(v): return {i:F(x) for i,x in enumerate(v) if x}

def adapted(a):
    b=list(a)
    b[2]=a[1]+a[3];b[3]=a[2]
    for j in (4,10,27): b[j]=a[1]+a[j]
    return b

def inv_adapted(b):
    a=list(b)
    a[2]=b[3];a[3]=b[2]-b[1]
    for j in (4,10,27): a[j]=b[j]-b[1]
    return a

def weighted_basis(j):
    a=[0]*D;a[j]=P**(2+(0 if j<2 else 1 if j==2 else 2))
    return sparse(adapted(a))

def scaled_check():
    data=read('group_lie_presentation.json')
    terms=data['bracket_terms_i_lt_j']
    by_pair={}
    for i,j,k,c in terms:
        require(0<=i<j<D and 0<=k<D and c!=0,'invalid scaled term')
        require(k not in by_pair.setdefault((i,j),{}),'duplicate scaled output')
        by_pair[i,j][k]=c
    require(len(terms)==199,'wrong scaled term count')
    for i in range(D):
        a=[int(i==j) for j in range(D)]
        require(inv_adapted(adapted(a))==a,'adapted inverse failure')
    for i,j in itertools.combinations(range(D),2):
        output=inv_adapted(dense(ambient.bracket(weighted_basis(i),weighted_basis(j))))
        ell=[output[k]/P**(2+(0 if k<2 else 1 if k==2 else 2)) for k in range(D)]
        require(all(v.denominator==1 for v in ell),'nonintegral ell bracket')
        require(sparse(ell)==by_pair.get((i,j),{}),f'ell bracket mismatch {i,j}')
    # The emitted table is an ordinary integer list, not a claimed match by hash.
    lean=(ROOT/'Kourovka/Lattice/ScaledData.lean').read_text()
    captured=re.findall(r'\(\s*(\d+)\s*,\s*(\d+)\s*,\s*(\d+)\s*,\s*\(?(-?\d+)(?:\s*:\s*Int)?\)?\s*\)',lean)
    literal=[[int(t) for t in a] for a in captured]
    require(literal==terms,'scaled Lean literal differs from archived JSON')
    return {'basis_pairs':465,'nonzero_terms':199,'adapted_inverse_vectors':31,'lean_literal_matched':True}

def inner_matrix():
    matrix=[[F(0) for _ in range(30)] for _ in range(D*D)]
    for i,j,k,c in read('group_lie_presentation.json')['bracket_terms_i_lt_j']:
        if i<30: matrix[k*D+j][i]+=c
        if j<30: matrix[k*D+i][j]-=c
    return matrix

def verify_inner(data, matrix):
    rows=data['selected_rows']
    require(len(rows)==30 and len(set(rows))==30,'inner selection invalid')
    # Rational strings or explicit [numerator, denominator] pairs are read exactly.
    arr=data.get('inverse',data.get('left_inverse'))
    if arr is None: raise EvidenceError('missing inverse entries')
    require(len(arr)==30 and all(len(row)==30 for row in arr),'inverse dimensions')
    inv=[[F(*a) if isinstance(a,list) else F(a) for a in row] for row in arr]
    minor=[matrix[r] for r in rows]
    for i,j in itertools.product(range(30),repeat=2):
        v=sum((inv[i][k]*minor[k][j] for k in range(30)),F(0))
        require(v==int(i==j),f'inner left inverse equation {i,j}')
    return inv

def inner_check():
    data=read('inner_left_inverse.json');mat=inner_matrix();inv=verify_inner(data,mat)
    lean=(ROOT/'Kourovka/Certificates/InnerWitnessData.lean').read_text()
    stanza=lean.split('def inverseCoeff',1)[1].split('/-- Actual inner',1)[0]
    matches=re.findall(r'\|\s*(\d+),\s*(\d+)\s*=>\s*\(?(-?\d+)(?:/(\d+))?\)?',stanza)
    coefficients={(int(i),int(j)):F(int(n),int(d or 1)) for i,j,n,d in matches}
    require(len(coefficients)==142,'inverse Lean nonzero count')
    require(all(coefficients.get((i,j),0)==inv[i][j] for i in range(30) for j in range(30)),
            'inverse Lean literals differ from checked data')
    row_text=lean.split('def selectedRow',1)[1].split('def inverseCoeff',1)[0]
    rows=[int(i)*31+int(j) for i,j in re.findall(r'\((\d+),(\d+)\)',row_text)]
    require(rows==data['selected_rows'],'inner row Lean literals mismatch')
    bad=copy.deepcopy(data)
    name='inverse' if 'inverse' in bad else 'left_inverse'
    z=bad[name][0][0];bad[name][0][0]=str(F(z)+1)
    try: verify_inner(bad,mat)
    except EvidenceError as e:
        require(str(e).startswith('inner left inverse equation'),'mutation rejected for wrong reason')
    else: raise EvidenceError('bad inverse accepted')
    return {'rows':30,'columns':30,'rational_equations':900,'nonzero_inverse_entries':142,
            'wrong_inverse_rejected':True,'lean_literals_matched':True}

def generation_check():
    dag=read('generation_dag.json');cert=read('integral_generation_certificate.json')
    require(ambient.verify_dag(dag),'original generation DAG failure')
    den=[];vals=[]
    for k,n in enumerate(dag['nodes']):
        op=n['op']
        if op=='input':
            v=dense((ambient.X,ambient.Y)[n['index']]);d=1
        elif op=='scale':
            a=n['arg'];require(a<k,'forward reference')
            d=den[a]*n['denominator'];v=[n['numerator']*x for x in vals[a]]
        elif op=='add':
            a,b=n['left'],n['right'];require(max(a,b)<k,'forward reference')
            d=math.lcm(den[a],den[b]);v=[d//den[a]*x+d//den[b]*y for x,y in zip(vals[a],vals[b])]
        elif op=='bracket':
            a,b=n['left'],n['right'];require(max(a,b)<k,'forward reference')
            d=den[a]*den[b];v=dense(ambient.bracket(sparse(vals[a]),sparse(vals[b])))
        else: raise EvidenceError('unknown generation operation')
        require(math.gcd(d,P)==1,'generation denominator not a p-adic unit')
        den.append(d);vals.append(v)
    def validate_stored(candidate):
        require(den==candidate['denominators'],'integer denominator list mismatch')
        require(vals==candidate['integer_node_values'],'integer node vector mismatch')
    validate_stored(cert)
    for a in dag['targets']:
        k,j=a['node'],a['basis_index']
        require(vals[k]==[den[k]*int(i==j) for i in range(D)],'integer generator target')
    lean=(ROOT/'Kourovka/Lattice/IntegralWords.lean').read_text()
    literals=re.findall(r'theorem eval_(\d+)\s*:\s*ev g\d+\s*=\s*!\[([^]]+)\]',lean)
    require(len(literals)==88,'integer vector literal count')
    for idx,contents in literals:
        got=[int(x.strip().strip('()')) for x in contents.split(',')]
        require(got==vals[int(idx)],f'integer generation literal {idx}')
    corrupted=copy.deepcopy(cert);corrupted['integer_node_values'][0][0]+=1
    try: validate_stored(corrupted)
    except EvidenceError as e:
        require(str(e)=='integer node vector mismatch','mutation rejected for wrong reason')
    else: raise EvidenceError('bad integer certificate unexpectedly matched')
    return {'nodes':len(vals),'targets':31,'all_denominators_padic_units':True,
            'lean_vector_literals_matched':True,'wrong_vector_rejected':True}

def scalar_controls():
    cases=0
    for c in range(1,15):
        for q in range(1,15):
            kernel=[x for x in range(c*q) if c*x%(c*q)==0]
            image=[q*t for t in range(c)]
            require(kernel==image,'scalar kernel not all representatives')
            require([x//q for x in kernel]==list(range(c)),'scalar inverse')
            cases+=1
    return {'complete_scalar_kernels':cases,'includes_c_one_q_one':True}

# Small exact checks of Dynkin signs and the action identity on the same integer Lie ring.
def word_eval(t,values):
    return values[t] if isinstance(t,int) else ambient.bracket(word_eval(t[0],values),word_eval(t[1],values))
def word_degree(t):return 1 if isinstance(t,int) else word_degree(t[0])+word_degree(t[1])
def expansion(t):
    if isinstance(t,int):return [(1,(t,))]
    a,b=map(expansion,t)
    return [(c*d,u+v) for c,u in a for d,v in b]+[(-c*d,v+u) for c,u in a for d,v in b]
def dynkin_word(w,values):
    if not w:return {}
    if len(w)==1:return values[w[0]]
    return ambient.bracket(values[w[0]],dynkin_word(w[1:],values))
def dynkin_check():
    atoms=[0,1,2,3]
    words=atoms+[(a,b) for a in atoms for b in atoms]
    words += [(a,b) for a in words[:20] for b in words[:20]]
    values={0:ambient.X,1:ambient.Y,2:ambient.unit('U0'),3:ambient.unit('V4')}
    for t in words:
        out={}
        for c,w in expansion(t):out=ambient.add(out,ambient.scale(c,dynkin_word(w,values)))
        require(out==ambient.scale(word_degree(t),word_eval(t,values)),'Dynkin sign/degree test')
    return {'lie_words':len(words),'maximum_degree':max(map(word_degree,words)),
            'scope':'finite exact controls, not the general Lean theorem'}

def main():
    start=time.perf_counter()
    out={'status':'EXTERNAL_CHECKS_IN_PROGRESS','lean_invoked':False,'lean_certification':False,
         'python_version':platform.python_version()}
    try:
        out['scaled_bracket']=scaled_check()
        out['inner_inverse']=inner_check()
        out['integral_generation']=generation_check()
        out['scalar_kernels']=scalar_controls()
        out['dynkin_controls']=dynkin_check()
        out['status']='EXACT_EXTERNAL_EVIDENCE_PASSED_NOT_LEAN_CERTIFICATION'
        rc=0
    except Exception as e:
        out['status']='EXTERNAL_EVIDENCE_FAILED';out['error']=str(e);rc=2
    out['measured_wall_seconds']=time.perf_counter()-start
    print(json.dumps(out,indent=2))
    return rc
if __name__=='__main__':sys.exit(main())
