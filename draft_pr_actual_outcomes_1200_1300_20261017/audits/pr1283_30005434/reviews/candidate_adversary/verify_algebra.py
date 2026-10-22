#!/usr/bin/env python3
"""Independent bounded consistency checks; not a universal proof or formal certification.
Enumerate all labelled commutative idempotent binary tables, not natural posets.
Uses explicit exceptions; stable output under normal, -O, and -OO execution.
"""
import argparse
import itertools
import json
import sys

class VerificationError(Exception):
    pass

def require(condition, message):
    if not condition:
        raise VerificationError(message)

def check_meet(m):
    n=len(m)
    require(all(len(row)==n for row in m), 'meet shape')
    require(all(isinstance(v,int) and 0<=v<n for row in m for v in row), 'meet closure')
    for x in range(n):
        require(m[x][x]==x, f'meet idempotence {(x,)}')
        for y in range(n):
            require(m[x][y]==m[y][x], f'meet commutativity {(x,y)}')
            for z in range(n):
                require(m[m[x][y]][z]==m[x][m[y][z]],f'meet associativity {(x,y,z)}')

def all_meets(n):
    pairs=[(x,y) for x in range(n) for y in range(x+1,n)]
    for values in itertools.product(range(n),repeat=len(pairs)):
        m=[[x if x==y else -1 for y in range(n)] for x in range(n)]
        for (x,y),v in zip(pairs,values):
            m[x][y]=m[y][x]=v
        if all(m[m[x][y]][z]==m[x][m[y][z]] for x in range(n) for y in range(n) for z in range(n)):
            yield m

def le(m,x,y):
    return m[x][y]==x

def tops(m):
    return [e for e in range(len(m)) if all(le(m,x,e) for x in range(len(m)))]

def construction(m,e,wrong=False):
    return [[e if le(m,x,y) else (y if wrong else m[x][y]) for y in range(len(m))] for x in range(len(m))]

def l1_tables(n,e):
    free=[(x,y) for x in range(n) for y in range(n) if x!=e and y!=e and x!=y]
    for values in itertools.product(range(n),repeat=len(free)):
        p=[[e for y in range(n)] for x in range(n)]
        p[e]=list(range(n))
        for (x,y),v in zip(free,values):
            p[x][y]=v
        yield p

def joint_fast(m,p,e):
    # All p supplied here already satisfy the row/column/diagonal L1 constraints.
    n=len(m)
    for x in range(n):
        for y in range(n):
            if (p[x][y]==e and p[y][x]==e)!=(x==y):
                return False
    for x in range(n):
        for y in range(n):
            for z in range(n):
                if p[x][m[y][z]]!=m[p[x][y]][p[x][z]]:
                    return False
                if p[m[x][y]][z]!=p[p[x][y]][p[x][z]]:
                    return False
                if p[p[x][y]][p[x][z]]!=p[p[y][x]][p[y][z]]:
                    return False
    return True

def verify(m,p,e,joint=True):
    check_meet(m)
    n=len(m)
    require(0<=e<n,'distinguished element absent')
    require(len(p)==n and all(len(row)==n for row in p),'multiplication shape')
    require(all(isinstance(v,int) and 0<=v<n for row in p for v in row),'multiplication closure')
    for x in range(n):
        require(p[e][x]==x,f'S2 {(x,)}')
        require(p[x][e]==e,f'S4 {(x,)}')
        if joint:
            require(p[x][x]==e,f'L1 diagonal {(x,)}')
        for y in range(n):
            if joint:
                require((p[x][y]==e and p[y][x]==e)==(x==y),f'L3 {(x,y)}')
            for z in range(n):
                require(p[x][m[y][z]]==m[p[x][y]][p[x][z]],f'S1 {(x,y,z)}')
                require(p[m[x][y]][z]==p[p[x][y]][p[x][z]],f'S3 {(x,y,z)}')
                if joint:
                    require(p[p[x][y]][p[x][z]]==p[p[y][x]][p[y][z]],f'L2 {(x,y,z)}')
    if joint:
        require(e in tops(m),'necessity: e not top')
        for x in range(n):
            for y in range(n):
                require((p[x][y]==e)==le(m,x,y),f'order equality {(x,y)}')

def check_translation_absorption(m,p):
    n=len(m)
    for a in range(n):
        for x in range(n):
            if le(m,a,x):
                for z in range(n):
                    require(p[a][p[x][z]]==p[a][z],f'F_a F_x absorption {(a,x,z)}')

def diamond():
    return [[x&y for y in range(4)] for x in range(4)]

def nondistributive(name):
    if name=='M3':
        return [[x if x==y else (y if x==4 else (x if y==4 else 0)) for y in range(5)] for x in range(5)]
    # N5: 0<1<2<4 and 0<3<4.
    rel={(x,x) for x in range(5)}|{(0,x) for x in range(5)}|{(x,4) for x in range(5)}|{(1,2)}
    m=[]
    for x in range(5):
        row=[]
        for y in range(5):
            lower=[z for z in range(5) if (z,x) in rel and (z,y) in rel]
            greatest=[z for z in lower if all((w,z) in rel for w in lower)]
            require(len(greatest)==1,'N5 meet definition')
            row.append(greatest[0])
        m.append(row)
    return m

def run(injection=None):
    b=diamond();p=construction(b,3)
    if injection=='wrong-second-branch':
        verify(b,construction(b,3,wrong=True),3)
        raise VerificationError('failure injection escaped detection')
    if injection=='reverse-order':
        q=[[3 if le(b,y,x) else b[x][y] for y in range(4)] for x in range(4)]
        verify(b,q,3)
        raise VerificationError('failure injection escaped detection')
    rows=[]
    for n in range(1,5):
        count=topcount=projection=constructed=tables=joint=0
        for m in all_meets(n):
            check_meet(m);count+=1
            ts=tops(m);require(len(ts)<=1,'multiple greatest elements')
            for e in range(n):
                verify(m,[list(range(n)) for _ in range(n)],e,joint=False);projection+=1
                for q in l1_tables(n,e):
                    tables+=1
                    if joint_fast(m,q,e):
                        verify(m,q,e);joint+=1
            for e in ts:
                topcount+=1;q=construction(m,e);verify(m,q,e);check_translation_absorption(m,q);constructed+=1
        rows.append({'n':n,'all_commutative_idempotent_tables':n**(n*(n-1)//2),'labelled_meet_semilattices':count,'with_top':topcount,'pointed_projection_checks':projection,'construction_checks':constructed,'L1_tables_considered':tables,'joint_structures':joint})
    controls={}
    try:
        verify(b,construction(b,3,wrong=True),3)
    except VerificationError as err:
        controls['Problem10_second_branch']=str(err)
    else:
        raise VerificationError('Problem10 negative control escaped')
    require(b[1][2]==0 and construction(b,3,True)[1][b[1][2]]==0 and b[construction(b,3,True)[1][1]][construction(b,3,True)[1][2]]==2,'negative-control witness changed')
    for name in ['M3','N5']:
        m=nondistributive(name);q=construction(m,4);verify(m,q,4);check_translation_absorption(m,q);controls[name]='PASS'
    # A 3-element no-top semilattice. Separation is essential to necessity.
    v=[[0,0,0],[0,1,0],[0,0,2]];e=1;q=[[1,1,1],[0,1,2],[1,1,1]]
    verify(v,q,e,joint=False)
    require(all(q[x][x]==e for x in range(3)),'no-separation control diagonal')
    require(not tops(v),'no-separation control unexpectedly has top')
    require(q[0][2]==e and q[2][0]==e,'no-separation witness missing')
    require(all(q[q[x][y]][q[x][z]]==q[q[y][x]][q[y][z]] for x in range(3) for y in range(3) for z in range(3)),'no-separation control cycloid')
    controls['without_L3']={'status':'no-top countermodel','meet':v,'e':e,'multiplication':q,'separation_failure_pair':[0,2]}
    # These finite sets are exact-operation samples of the infinite examples.
    sample=[-1000000000000,-10,-2,-1,0]
    m=[[sample.index(min(x,y)) for y in sample] for x in sample]
    verify(m,construction(m,4),4)
    controls['nonpositive_integer_chain_sample']='PASS; finite sample only'
    return {'status':'PASS','scope':'All labelled commutative idempotent binary tables n<=4; retain associative ones. Exhaustive L1 tables for each resulting semilattice and e. Finite evidence only.','enumeration':rows,'totals':{key:sum(r[key] for r in rows) for key in ['all_commutative_idempotent_tables','labelled_meet_semilattices','with_top','pointed_projection_checks','construction_checks','L1_tables_considered','joint_structures']},'controls':controls}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--inject-failure',choices=['wrong-second-branch','reverse-order']);args=parser.parse_args()
    try:
        result=run(args.inject_failure)
    except VerificationError as err:
        print(json.dumps({'status':'FAIL','error':str(err)},sort_keys=True,separators=(',',':')))
        return 2
    print(json.dumps(result,sort_keys=True,separators=(',',':')))
    return 0

if __name__=='__main__':
    sys.exit(main())
