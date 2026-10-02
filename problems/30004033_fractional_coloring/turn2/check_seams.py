#!/usr/bin/env python3
"""Integer-capacity coupling checks and exact K4+ boundary certificates."""
from fractions import Fraction as F
from itertools import combinations, product
from collections import deque
import json

def maxflow(rows,cols):
    # States 00,10,01,11. Compatibility forbids membership in both sides
    # at either newly joined endpoint.
    cap=[[0]*10 for _ in range(10)]
    for i,a in enumerate(rows):cap[8][i]=a
    for j,b in enumerate(cols):cap[4+j][9]=b
    for i in range(4):
        for j in range(4):
            if not i&j:cap[i][4+j]=sum(rows)
    val=0
    while True:
        parent=[-1]*10;parent[8]=8;q=deque([8])
        while q and parent[9]<0:
            u=q.popleft()
            for v in range(10):
                if parent[v]<0 and cap[u][v]>0:parent[v]=u;q.append(v)
        if parent[9]<0:return val
        delta=sum(rows);v=9
        while v!=8:delta=min(delta,cap[parent[v]][v]);v=parent[v]
        v=9
        while v!=8:
            u=parent[v];cap[u][v]-=delta;cap[v][u]+=delta;v=u
        val+=delta

def rank(matrix):
    M=[[F(x) for x in row] for row in matrix]; pivot=0
    for j in range(len(M[0])):
        idx=next((i for i in range(pivot,len(M)) if M[i][j]),None)
        if idx is None: continue
        M[pivot],M[idx]=M[idx],M[pivot]
        z=M[pivot][j]; M[pivot]=[x/z for x in M[pivot]]
        for i in range(len(M)):
            if i!=pivot:
                z=M[i][j]; M[i]=[a-z*b for a,b in zip(M[i],M[pivot])]
        pivot+=1
        if pivot==len(M):break
    return pivot

def check():
    seam=0
    for d in range(2,25):
        for a in range(d//2+1):
            for s,t in product(range(a+1),repeat=2):
                rows=[d-2*a+s,a-s,a-s,s]; cols=[d-2*a+t,a-t,a-t,t]
                assert (maxflow(rows,cols)==d)==(abs(s-t)<=d-2*a)
                seam+=1
    names=list('abcdxyzw');E=[('a','c'),('a','d'),('b','c'),('b','d'),('a','x'),('x','y'),('y','b'),('c','z'),('z','w'),('w','d')]
    indep=[tuple(v for i,v in enumerate(names) if m>>i&1) for m in range(256) if all(not(m>>names.index(a)&1 and m>>names.index(b)&1) for a,b in E)]
    assert max(map(len,indep))==3
    triples=[('a','b','z'),('a','b','w'),('a','y','z'),('a','y','w'),('b','x','z'),('b','x','w'),('c','d','x'),('c','d','y'),('c','x','w'),('c','y','w'),('d','x','z'),('d','y','z')]
    assert set(triples)==set(s for s in indep if len(s)==3)
    equations=[[int(v in I) for I in triples] for v in names]+[[1]*12]
    assert rank(equations)==8
    directions=[[1,-1,-1,1,0,0,0,0,0,0,0,0], [1,-1,0,0,-1,1,0,0,0,0,0,0], [0,0,0,0,0,0,1,-1,-1,1,0,0], [0,0,0,0,0,0,1,-1,0,0,-1,1]]
    assert rank(directions)==4
    assert all(sum(a*b for a,b in zip(row,direction))==0 for row in equations for direction in directions)
    vertices=[];marginal=3
    # The entire feasible family is the affine image of a four-dimensional
    # cube, so these are all its extreme parameter choices.
    for A,B,C,D in product([F(0),F(1,8)],repeat=4):
        p=[A+B,F(1,4)-A-B,F(1,8)-A,A,F(1,8)-B,B,C+D,F(1,4)-C-D,F(1,8)-C,C,F(1,8)-D,D]
        assert min(p)>=0 and sum(p)==1;marginal+=1
        for v in names:assert sum(w for I,w in zip(triples,p) if v in I)==F(3,8);marginal+=1
        cross=[sum(w for I,w in zip(triples,p) if x in I and y in I) for x,y in [('x','z'),('x','w'),('y','z'),('y','w')]]
        assert cross==[F(1,4)-B-D,F(1,8)+B-C,F(1,8)-A+D,A+C];marginal+=1
        assert min(cross)>=0 and max(cross)<=F(1,4) and sum(cross)==F(1,2);marginal+=1
        vertices.append(cross)
    for i in range(4):assert min(v[i] for v in vertices)==0 and max(v[i] for v in vertices)==F(1,4);marginal+=1
    p=[F(1,8) if len(set(I)&set('abcd'))==2 else F(1,16) for I in triples]
    for x,y in [('x','z'),('x','w'),('y','z'),('y','w')]:
        assert sum(w for I,w in zip(triples,p) if x in I and y in I)==F(1,8);marginal+=1
    return {'status':'pass','integer_transport_assertions':seam,'k4plus_assertions':marginal+2,'assertions':seam+marginal+2,'k4plus_independent_sets':len(indep),'k4plus_maximum_independent_sets':len(triples),'limits':'Transport denominators 2..24, all feasible rational single-side overlaps on that grid; all 256 K4+ vertex subsets; 16 parameter-cube corners. Universal statements rest on the written proof.'}
if __name__=='__main__': print(json.dumps(check(),indent=2,sort_keys=True))
