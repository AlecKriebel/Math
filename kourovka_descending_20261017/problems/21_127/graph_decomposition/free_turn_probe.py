#!/usr/bin/env python3
"""Small exact free-group turn-graph LP probe, using Fraction arithmetic.

Exploratory until its topological LP interpretation and dual certificate are
independently checked. No RAAG rationality claim.
"""
from fractions import Fraction as F
from pathlib import Path
from collections import Counter
import json

ROOT=Path(__file__).resolve().parent

def cycles(adj):
    result=[]
    for start in range(len(adj)):
        def dfs(path,used):
            for v in adj[path[-1]]:
                if v==start:
                    result.append(tuple(path))
                elif v>start and v not in used:
                    dfs(path+[v],used|{v})
        dfs([start],{start})
    return result


def piv(tableau,basis,r,col):
    z=tableau[r][col]
    tableau[r]=[x/z for x in tableau[r]]
    pivotrow=tableau[r]
    for i,row in enumerate(tableau):
        if i==r:continue
        a=row[col]
        if a:tableau[i]=[x-a*y for x,y in zip(row,pivotrow)]
    basis[r]=col


def optimize(tableau,basis,allowed):
    limit=0
    while True:
        possible=[j for j in allowed if tableau[-1][j]<0]
        if not possible:return limit
        j=min(possible)
        candidates=[i for i in range(len(basis)) if tableau[i][j]>0]
        if not candidates:raise ValueError('unbounded')
        i=min(candidates,key=lambda r:(tableau[r][-1]/tableau[r][j],basis[r]))
        piv(tableau,basis,i,j);limit+=1
        if limit>100000:raise ValueError('iteration cap')


def simplex(A,b,c):
    m=len(A);n=len(c)
    rows=[]
    for i,(row,rhs) in enumerate(zip(A,b)):
        sign=1 if rhs>=0 else -1
        rows.append([F(sign*x) for x in row]+[F(int(i==j)) for j in range(m)]+[F(sign*rhs)])
    basis=list(range(n,n+m))
    # Maximize -sum artificial variables: objective row is -c then canonicalize.
    objective=[F(0)]*n+[F(1)]*m+[F(0)]
    for row in rows:objective=[x-y for x,y in zip(objective,row)]
    rows.append(objective)
    it1=optimize(rows,basis,range(n+m))
    assert rows[-1][-1]==0,('infeasible',rows[-1][-1])
    # Keep zero artificial basic variables; they must leave before a positive
    # original objective direction can enter. Pivot them out where possible.
    for i in reversed(range(len(basis))):
        if basis[i]<n:continue
        possible=[j for j in range(n) if rows[i][j]]
        if possible:piv(rows,basis,i,min(possible))
        else:
            assert rows[i][-1]==0
            del rows[i];del basis[i]
    rows[-1]=[-F(x) for x in c]+[F(0)]*m+[F(0)]
    for i,j in enumerate(basis):
        a=rows[-1][j]
        if a:rows[-1]=[x-a*y for x,y in zip(rows[-1],rows[i])]
    it2=optimize(rows,basis,range(n))
    x=[F(0)]*n
    for i,j in enumerate(basis):x[j]=rows[i][-1]
    assert all(v>=0 for v in x)
    assert all(sum(F(a)*z for a,z in zip(row,x))==rhs for row,rhs in zip(A,b))
    value=sum(F(k)*z for k,z in zip(c,x))
    assert value==rows[-1][-1]
    # Original art identity columns track the dual row coefficients.
    y=rows[-1][n:n+m]
    assert all(sum(y[i]*A[i][j] for i in range(m))>=c[j] for j in range(n))
    assert sum(y[i]*b[i] for i in range(m))==value
    return value,x,y,[it1,it2]


def main():
    word='aca cAcACCC'.replace(' ','')
    assert word=='acacAcACCC'
    L=len(word)
    E=[(i,j) for i in range(L) for j in range(L) if word[i].swapcase()==word[(j+1)%L]]
    adj=[[] for _ in word]
    for i,j in E:adj[i].append(j)
    C=cycles(adj)
    dual=lambda edge:((edge[1]+1)%L,(edge[0]-1)%L)
    assert all(dual(e) in E and dual(dual(e))==e for e in E)
    representatives=[e for e in E if e<dual(e)]
    assert len(representatives)*2==len(E)
    cv=[Counter(cyc) for cyc in C]
    ce=[Counter(zip(cyc,cyc[1:]+cyc[:1])) for cyc in C]
    A=[[cv[j][i] for j in range(len(C))] for i in range(L)]
    A += [[ce[j][e]-ce[j][dual(e)] for j in range(len(C))] for e in representatives]
    b=[1]*L+[0]*len(representatives)
    val,x,y,it=simplex(A,b,[1]*len(C))
    scl=F(L,4)-val/2
    result={'scope':'Exact finite free-group turn LP, topological interpretation to be independently checked',
            'word':word,'length':L,'directed_turn_edges':E,'dual_edge_representatives':representatives,
            'circuit_count':len(C),'constraint_count':len(A),'phase_iterations':it,
            'max_polygon_count':str(val),'resulting_scl':str(scl),
            'nonzero_primal_circuits':[{'cycle':C[i],'weight':str(t)} for i,t in enumerate(x) if t],
            'dual_weights':[str(t) for t in y],
            'exact_primal_feasible':True,'exact_dual_feasible':True,'matching_objectives':True}
    (ROOT/'free_turn_probe.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['scope','word','circuit_count','constraint_count','phase_iterations','max_polygon_count','resulting_scl']},indent=2))

if __name__=='__main__':main()
