#!/usr/bin/env python3
"""Independent finite controls. These do not certify the continuous topology."""
from fractions import Fraction as Q
from itertools import combinations
import json, math, os, sys

def need(value, message):
    if not value: raise RuntimeError(message)

def det_by_subsets(a):
    n=len(a)
    need(n and all(len(r)==n for r in a),'square matrix')
    states={0:Q(1)}
    for row in range(n):
        nxt={}
        for mask,v in states.items():
            for col in range(n):
                if not mask>>col&1:
                    inversions=sum(1 for old in range(col+1,n) if mask>>old&1)
                    key=mask|1<<col
                    nxt[key]=nxt.get(key,Q(0))+v*a[row][col]*(-1)**inversions
        states=nxt
    return states[(1<<n)-1]

def jacobian(xs, directions=(0,0,1,1)):
    rows=[]
    for i,x in enumerate(xs):
        for coord in (0,1):
            r=[Q(0)]*8
            r[i]=Q(directions[i]==coord)
            r[4+2*coord]=-1
            r[5+2*coord]=-x
            rows.append(r)
    return rows

def collinear(points):
    if len(points)<2 or len(set(points))!=len(points): return False
    u=[points[1][i]-points[0][i] for i in range(3)]
    for p in points[2:]:
        v=[p[i]-points[0][i] for i in range(3)]
        if any(u[i]*v[j]!=u[j]*v[i] for i,j in [(0,1),(0,2),(1,2)]):return False
    return True

def main():
    need(sys.flags.isolated==1,'isolated Python required')
    need(os.geteuid()!=0,'non-root required')
    determinants=[]
    for xs in [(0,1,2,3),(-7,-3,2,8),(Q(1,7),Q(3,7),Q(8,7),Q(11,7))]:
        d=det_by_subsets(jacobian(xs)); expected=(xs[1]-xs[0])*(xs[3]-xs[2])
        need(d==expected,'independent determinant identity')
        determinants.append(str(d))
    need(det_by_subsets(jacobian((0,0,2,3)))==0,'collapsed first pair negative control')
    need(det_by_subsets(jacobian((0,1,2,2)))==0,'collapsed second pair negative control')
    need(det_by_subsets(jacobian((0,1,2,3),(0,0,0,0)))==0,'parallel directions negative control')
    # Solve exact affine-offset models independently, without the original checker.
    offsets=[(Q(1,100),Q(2,100)),(Q(-1,100),Q(3,100)),(Q(4,100),Q(-2,100)),(Q(5,100),Q(1,100))]
    D=offsets[1][1]-offsets[0][1]; C=offsets[0][1]
    B=offsets[3][0]-offsets[2][0]; A=offsets[2][0]-2*B
    ts=[]; points=[]
    for i,(y,z) in enumerate(offsets):
        t=A+B*i-y if i<2 else C+D*i-z
        ts.append(t);points.append((Q(i),y+t if i<2 else y,z if i<2 else z+t))
    need(all(abs(t)<Q(1,10) for t in ts) and collinear(points),'small-offset stable transversal')
    wrong=list(points);wrong[-1]=(wrong[-1][0],wrong[-1][1]+Q(1,100),wrong[-1][2])
    need(not collinear(wrong),'off-line point rejected')
    counts=[]
    for n in [4,5,7,11]:
        pts=[(Q(i),Q(0),Q(0)) for i in range(n)]
        count=sum(collinear(t) for t in combinations(pts,4))
        need(count==math.comb(n,4),'marked count')
        counts.append({'contacts':n,'marked_sets':count,'supporting_lines':1})
    # Check every piece of the collapse model at exact interior mesh points.
    checked=0
    for n in [6,7,13,41,101]:
        e=Q(1,n)
        vertices=[(-5*e,25*e*e),(-3*e,Q(0)),(-2*e,e*e),(-e,Q(0)),(Q(0),e*e),(e,Q(0)),(2*e,e*e),(3*e,Q(0)),(5*e,25*e*e)]
        for (x0,y0),(x1,y1) in zip(vertices,vertices[1:]):
            need(x1>x0 and not(y0==y1==0),'graph edges and no axis interval')
            for j in range(17):
                lam=Q(j,16);x=x0+lam*(x1-x0);y=y0+lam*(y1-y0)
                need(abs(y-x*x)<=25*e*e,'collapse interpolation bound')
                checked+=1
        pts=[(j*e,Q(0),Q(0)) for j in (-3,-1,1,3)]
        need(collinear(pts) and not collinear([(x,x*x,z) for x,y,z in pts]),'collapse vs parabola')
    # Rational circle parameters with arbitrary lifted heights: no sampled trisecants.
    points=[]
    for t in map(Q,range(-6,7)):
        x=(1-t*t)/(1+t*t);y=2*t/(1+t*t);z=t**3/(1+t*t)
        need(x*x+y*y==1,'rational unit circle')
        points.append((x,y,z))
    need(all(not collinear(t) for t in combinations(points,3)),'lifted-circle finite control')
    u=(Q(0),Q(1),Q(2));v=(Q(0),Q(1),Q(-2))
    need(sum(a*b for a,b in zip(u,v))/sum(a*a for a in u)==Q(-3,5),'tangent cosine')
    print(json.dumps({'schema':'wild-quadrisecants-independent-exact-v1','uid':os.getuid(),'euid':os.geteuid(),'optimize':sys.flags.optimize,'isolated':sys.flags.isolated,'determinants':determinants,'degenerate_jacobian_controls':3,'exact_affine_offset_transversal':True,'noncollinear_control_rejected':True,'line_counts':counts,'collapse_piece_samples':checked,'lifted_circle_triples':math.comb(len(points),3),'tangent_cosine':'-3/5','main_problem_resolved':False,'formal_certification':False},sort_keys=True))

if __name__=='__main__':main()
