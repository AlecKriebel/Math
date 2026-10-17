#!/usr/bin/env python3
"""Finite indexing checks for the all-size folding-fibre proof. No radius inference."""
from itertools import product,combinations
from functools import lru_cache
from pathlib import Path
import json,sys

def require(condition,context):
    if not condition: raise RuntimeError(context)
def inv(p):return tuple(p.index(v)+1 for v in range(1,len(p)+1))
def S(p):return tuple(len(p)+1-v for v in inv(p)[::-1])
def skew(a,b):return tuple(v+len(b) for v in a)+tuple(b)
def std(p):
    ranks={v:i+1 for i,v in enumerate(sorted(p))}
    return tuple(ranks[v] for v in p)
def avoids(p,t):
    return not any(std(tuple(p[i] for i in inds))==t for inds in combinations(range(len(p)),len(t)))
def bar(w):return ''.join('L' if x=='U' else 'U' for x in w[::-1])
@lru_cache(None)
def validate_edge(A,C,w,greedy):
    require(w.count('U')==len(A) and w.count('L')==len(C),('word sizes',A,C,w))
    require(avoids(A,(2,1,3)) and avoids(C,(2,1,3)),('states',A,C))
    low=S(C);u=iter(v+len(C) for v in A);l=iter(low)
    p=tuple(next(u) if c=='U' else next(l) for c in w)
    require(avoids(p,(1,3,2,4)),('avoidance',A,C,w,p))
    if greedy:
        pos=p.index(len(C));inds=[i for i,c in enumerate(w) if c=='U']
        require(any(i<pos<j and p[i]<p[j] for i,j in combinations(inds,2)),('witness',A,C,w))
    return True

def source(W,R,bits):
    active=list(range(2,W,2));states=[(1,2)]*(R*(2*W-2)+1)
    for r in range(R):
        start=r*(2*W-2)
        for k,j in enumerate(active):
            eps=bits[r*len(active)+k]
            idx=start+(j-1 if eps else 2*W-1-j)
            states[idx]=(2,3,1)
    words=[]
    for A,C in zip(states,states[1:]):
        require(not(len(A)==3 and len(C)==3),('adjacent active',A,C))
        w='ULLU'+('U' if len(A)==3 else 'L' if len(C)==3 else '')
        validate_edge(A,C,w,True);words.append(w)
    return tuple(states),tuple(words)

def fold(W,R,states,words):
    outstates=[() for _ in range(W)];outwords=['' for _ in range(W-1)]
    for r in range(R):
        start=r*(2*W-2)
        for j in range(1,W+1):
            up=states[start+j-1];down=states[start+2*W-1-j]
            outstates[j-1]=skew(outstates[j-1],skew(up,inv(down)))
        for j in range(1,W):
            outwords[j-1]+=words[start+j-1]+bar(words[start+2*W-2-j])
    return tuple(outstates),tuple(outwords)

def reconstruct(states,words):
    actual=[A if i%2==0 else S(A) for i,A in enumerate(states)]
    xpos=[]
    for i in range(0,len(states),2):
        if i+1==len(states):xpos.extend((i,k) for k in range(len(actual[i])));continue
        its=[iter([(c,k) for k in range(len(actual[c]))]) for c in (i,i+1)]
        xpos.extend(next(its[0 if t=='U' else 1]) for t in words[i])
    ydesc=[(0,k) for k in sorted(range(len(actual[0])),key=lambda k:actual[0][k],reverse=True)]
    for i in range(1,len(states),2):
        order=lambda c:[(c,k) for k in sorted(range(len(actual[c])),key=lambda k:actual[c][k],reverse=True)]
        if i+1==len(states):ydesc.extend(order(i));continue
        its=[iter(order(c)) for c in (i,i+1)]
        ydesc.extend(next(its[0 if t=='U' else 1]) for t in words[i])
    require(set(xpos)==set(ydesc) and len(xpos)==len(ydesc),('reconstruct labels',states))
    val={pt:len(xpos)-i for i,pt in enumerate(ydesc)}
    return tuple(val[pt] for pt in xpos)

def canonical(p):
    remaining=list(enumerate(p));out=[]
    while remaining:
        if len(out)%2==0:
            vals=sorted(v for i,v in remaining)
            m=0
            for t in range(1,len(vals)+1):
                q=std(tuple(v for i,v in remaining if v>=vals[-t]))
                if not avoids(q,(2,1,3)):break
                m=t
            take=[pt for pt in remaining if pt[1]>=vals[-m]]
        else:
            m=0
            for t in range(1,len(remaining)+1):
                if not avoids(std(tuple(v for i,v in remaining[:t])),(1,3,2)):break
                m=t
            take=remaining[:m]
        patt=std(tuple(v for i,v in take));out.append(patt if len(out)%2==0 else S(patt))
        chosen=set(take);remaining=[pt for pt in remaining if pt not in chosen]
    return tuple(out)

rows=[];checked_sources=0;fully_reconstructed=0
for W in range(3,8):
    for R in range(1,4):
        a=(W-1)//2;n=R*(4*W-4+a)+2
        seen_sources=set();images=set()
        for bits in product((0,1),repeat=R*a):
            states,words=source(W,R,bits)
            require(sum(map(len,states))==n,('source size',W,R,bits))
            require((states,words) not in seen_sources,('source collision',W,R,bits));seen_sources.add((states,words))
            outstates,outwords=fold(W,R,states,words);images.add((outstates,outwords))
            if n<=25:
                p=reconstruct(states,words)
                require(avoids(p,(1,3,2,4)),('full source avoidance',W,R,bits,p))
                require(canonical(p)==states,('full source canonical',W,R,bits,p))
                fully_reconstructed+=1
            checked_sources+=1
        require(len(images)==1 and len(seen_sources)==2**(R*a),('fibre count',W,R))
        outstates,outwords=next(iter(images))
        require(sum(map(len,outstates))==R*(4*W+a),('fold size',W,R))
        for A,C,w in zip(outstates,outstates[1:],outwords):validate_edge(A,C,w,False)
        guarded=tuple(skew((1,2),A) for A in outstates);guardwords=tuple('ULLU'+w for w in outwords)
        for A,C,w in zip(guarded,guarded[1:],guardwords):validate_edge(A,C,w,True)
        if sum(map(len,guarded))<=30:
            q=reconstruct(guarded,guardwords)
            require(avoids(q,(1,3,2,4)) and canonical(q)==guarded,('guarded full recovery',W,R,q))
        rows.append({'width':W,'excursions':R,'active_levels':a,'source_size':n,'source_count':len(seen_sources),'distinct_folded_images':len(images),'turn_duplication':4*R-2,'guarded_output_size':R*(4*W+a)+2*W})
result={'scope':'Finite indexing diagnostics only; all-size theorem proved separately. No uniform-law or growth inference.','all_checks_passed':True,'source_paths_checked':checked_sources,'full_permutations_reconstructed_and_greedily_checked':fully_reconstructed,'distinct_local_checks':validate_edge.cache_info().currsize,'rows':rows}
out=Path(__file__).with_name(sys.argv[1] if len(sys.argv)>1 else 'FOLDING_FIBRE_CHECKS.json');out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
