#!/usr/bin/env python3
"""Exact Gaussian-integer traces; standard-library independent controls."""
from collections import defaultdict
import json

# Gaussian integer (a,b) represents a+i*b.
ZERO=(0,0)
ONE=(1,0)
ROOTS=((1,0),(0,1),(-1,0),(0,-1))
def add(a,b): return (a[0]+b[0],a[1]+b[1])
def mul(a,b): return (a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0])
def conj(a): return (a[0],-a[1])
def torus(lx,ly,flux_quarters=0,hx_quarters=0,hy_quarters=0):
    assert lx>2 and ly>2
    assert (flux_quarters*lx)%4==0, 'simple Landau gauge needs x compatibility'
    g=defaultdict(dict)
    idx=lambda x,y: (x%lx)*ly+(y%ly)
    def edge(a,b,w): g[a][b]=w; g[b][a]=conj(w)
    for x in range(lx):
        for y in range(ly):
            edge(idx(x,y),idx(x+1,y),ROOTS[hx_quarters%4] if x==lx-1 else ONE)
            edge(idx(x,y),idx(x,y+1),ROOTS[(flux_quarters*x+(hy_quarters if y==ly-1 else 0))%4])
    return g
def trace_power(g,k):
    out=ZERO
    for start in g:
        state={start:ONE}
        for _ in range(k):
            nxt=defaultdict(lambda:ZERO)
            for u,v in state.items():
                for w,z in g[u].items(): nxt[w]=add(nxt[w],mul(v,z))
            state=nxt
        out=add(out,state.get(start,ZERO))
    return out
def run():
    cases=[]
    for l in (4,6,8):
        for f in (0,2):
            g=torus(l,l,f)
            got={k:trace_power(g,k) for k in (2,4)}
            assert got[2]==(4*l*l,0)
            expected4=(36 if f==0 else 20)*l*l+(4*l*l if l==4 else 0)
            assert got[4]==(expected4,0),(l,f,got)
            cases.append({'L':l,'flux_quarters':f,'traces':got})
    for l in (4,8):
        g=torus(l,l,1)
        tr4=trace_power(g,4)
        assert tr4==((32 if l==4 else 28)*l*l,0)
        # In the L=4 control T^4=8T^2, checked at every ordered entry.
        if l==4:
            for start in g:
                state={start:ONE}; states={}
                for k in range(1,5):
                    nxt=defaultdict(lambda:ZERO)
                    for u,v in state.items():
                        for w,z in g[u].items(): nxt[w]=add(nxt[w],mul(v,z))
                    state=nxt
                    if k in (2,4): states[k]=dict(state)
                for end in g:
                    a=states[2].get(end,ZERO)
                    assert states[4].get(end,ZERO)==(8*a[0],8*a[1])
        cases.append({'L':l,'flux_quarters':1,'traces':{2:trace_power(g,2),4:tr4}})
    tr8_zero=trace_power(torus(8,8),8)
    tr8_twist=trace_power(torus(8,8,hx_quarters=2),8)
    assert tr8_zero[0]-tr8_twist[0]==4*64 and tr8_zero[1]==tr8_twist[1]==0
    cases.append({'L':8,'zero_face_flux_holonomy_control':{'tr8_untwisted':tr8_zero,'tr8_x_pi':tr8_twist,'difference':256}})
    print(json.dumps({'status':'PASS','arithmetic':'exact Gaussian integers','cases':cases},indent=2,sort_keys=True))
if __name__=='__main__': run()
