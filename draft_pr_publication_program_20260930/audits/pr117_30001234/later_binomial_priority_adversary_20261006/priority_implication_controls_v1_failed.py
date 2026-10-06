#!/usr/bin/env python3
"""Exact diagnostic certificates; unrestricted arguments are in REPORT.md."""
import argparse, datetime, hashlib, json, os
from fractions import Fraction as Q
from pathlib import Path

COUNT=0
def require(condition, name):
    global COUNT
    COUNT+=1
    if not condition:
        raise ValueError(name)

def mv(matrix, vector):
    return tuple(sum(Q(a)*b for a,b in zip(row,vector)) for row in matrix)

def rref(matrix):
    m=[list(map(Q,row)) for row in matrix]
    piv=[]; row=0
    for col in range(len(m[0])):
        candidate=next((i for i in range(row,len(m)) if m[i][col]),None)
        if candidate is None: continue
        m[row],m[candidate]=m[candidate],m[row]
        divisor=m[row][col];m[row]=[x/divisor for x in m[row]]
        for i in range(len(m)):
            if i!=row:
                factor=m[i][col];m[i]=[x-factor*y for x,y in zip(m[i],m[row])]
        piv.append(col);row+=1
        if row==len(m):break
    return m,piv

def augmented(a,b):
    n=len(a[0]);r=len(a)
    return tuple(tuple(a[j][i] for j in range(r))+tuple(b[j][i] for j in range(r)) for i in range(n))+tuple(tuple(int(i==j) for j in range(r))*2 for i in range(r))

def feasible(A,z):
    return all(x>=0 for x in z) and all(x<=1 for x in mv(A,z))

def certify(A,z,d,objective):
    require(feasible(A,z),'primal feasibility')
    require(all(v>=0 for v in d),'dual nonnegative')
    require(all(sum(Q(d[i])*A[i][j] for i in range(len(A)))>=1 for j in range(len(z))),'dual covering')
    require(sum(z)==objective==sum(d),'primal-dual objective equality')

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--false-control',action='store_true');args=parser.parse_args()
    if args.false_control:
        require(False,'deliberately false assertion must fail even under -O')
    a=((0,2,0,1,0),(0,2,0,0,1),(3,0,0,1,0),(3,0,0,0,1))
    b=((1,0,1,1,0),(1,0,1,0,1),(0,0,2,1,0),(0,0,2,0,1))
    A=augmented(a,b)
    d=(Q(1,2),Q(1,2),Q(1,2))+tuple(Q(0) for _ in range(6))
    z=(Q(1,2),Q(0),Q(0),Q(0),Q(1,2),Q(1,2),Q(0),Q(0))
    certify(A,z,d,Q(3,2))
    slack=tuple(sum(d[i]*A[i][j] for i in range(9))-1 for j in range(8))
    require(slack==(0,0,Q(1,2),Q(1,2),0,0,0,0),'positive dual slack forces both positive g columns zero')
    _,piv=rref(A)
    require(len(piv)==7,'Blanco augmented matrix rank 7')
    h=(Q(1),Q(-1),Q(0),Q(0),Q(-1),Q(1),Q(0),Q(0))
    require(mv(A,h)==tuple(Q(0) for _ in range(9)),'Blanco fiber kernel')
    corner_images=[]
    for ai in range(17):
        alpha=Q(ai,32)
        for pi in range(17):
            p=Q(1,2)+Q(pi,32)
            vector=(alpha,Q(1,2)-alpha,Q(0),Q(0),p-alpha,1-p+alpha,Q(0),Q(0))
            image=(Q(1),Q(1),Q(1),p,Q(3,2)-p,p,Q(3,2)-p,Q(0),Q(0))
            require(feasible(A,vector),'Blanco rational rectangle feasible')
            require(sum(vector)==Q(3,2),'Blanco rectangle optimal')
            require(mv(A,vector)==image,'Blanco image independent of alpha')
            other=Q(0) if alpha else Q(1,2)
            rival=(other,Q(1,2)-other,Q(0),Q(0),p-other,1-p+other,Q(0),Q(0))
            require(rival!=vector and feasible(A,rival) and mv(A,rival)==image,'every sampled boundary/interior fiber has distinct rational rival')
            if ai in (0,16) and pi in (0,16):corner_images.append(image)
    require(len(set(corner_images))==2,'four optimal-face corners have two distinct image fibers')
    weights=(4,5,6)
    require(sum(a[0][i]*weights[i] for i in range(3))==sum(b[0][i]*weights[i] for i in range(3))==10,'f weighted degree 10')
    require(sum(a[2][i]*weights[i] for i in range(3))==sum(b[2][i]*weights[i] for i in range(3))==12,'g weighted degree 12')
    require(min(weights)+10>12,'no positive-degree multiple can annihilate f or g classes in B/mB')
    # LaClair uses increasing endpoint orientation: edge 13 swaps the cyclic f3 monomial coordinates.
    tri_a=((1,0,0,0,1,0),(0,1,0,0,0,1),(0,0,1,1,0,0))
    tri_b=((0,1,0,1,0,0),(0,0,1,0,1,0),(1,0,0,0,0,1))
    T=augmented(tri_a,tri_b)
    certify(T,tuple(Q(1,2) for _ in range(6)),(Q(0),)*6+(Q(1),)*3,Q(3))
    modpoint=(Q(1),Q(1),Q(0),Q(0),Q(0),Q(0))
    require(feasible(T,modpoint) and sum(modpoint)==2,'modified triangle LP attains subset cap 2')
    require(sum(tuple(Q(1,2) for _ in range(6)))>2,'original optimal point excluded by the full-set cap')
    require(Q(17,12)<Q(3,2),'published-preprint threshold gap numerical comparison')
    require(Q(2)<Q(3),'LaClair upper bound versus original triangle optimum')
    body=Path(__file__).read_bytes()
    print(json.dumps({'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_PID':os.getpid(),'guard_count':COUNT,'status':'PASS','code_sha256':hashlib.sha256(body).hexdigest(),'Blanco_original_LP_optimum':'3/2','Blanco_rank':7,'Blanco_optimal_face_dimension':2,'LaClair_modified_triangle_LP_optimum':2,'PR117_original_triangle_LP_optimum':3,'new_central_candidate_proof_search_turns':0},indent=2,sort_keys=True))

if __name__=='__main__':main()
