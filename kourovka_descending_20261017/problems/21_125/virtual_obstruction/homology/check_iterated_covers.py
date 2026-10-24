#!/usr/bin/env python3
"""Iterated explicit graph covers with exact invariant rational characters."""
import argparse, collections, json, math
from fractions import Fraction as Q
from pathlib import Path
from check_characteristic_covers import theta_words, span_basis, sparse_reduce, dot, add, encode


def analyze(m, perms, r, characters=False):
    q=len(perms[0]); assert all(sorted(p)==list(range(q)) for p in perms)
    paths={0:[]}; queue=collections.deque([0]); tree=set()
    while queue:
        v=queue.popleft()
        for i in range(m):
            w=perms[i][v]
            if w not in paths:
                paths[w]=paths[v]+[i]; tree.add((v,i)); queue.append(w)
    assert len(paths)==q
    edges=[(v,i) for v in range(q) for i in range(m) if (v,i) not in tree]
    ind={e:j for j,e in enumerate(edges)}; n=len(edges)
    tw=theta_words(m,r)
    def walk(word,start=0):
        v=start; out={}
        for i in word:
            j=ind.get((v,i))
            if j is not None: out[j]=out.get(j,0)+1
            v=perms[i][v]
        return v,out
    mapped_paths=[]
    for v in range(q):
        end,chain=walk([j for i in paths[v] for j in tw[i]])
        assert end==v, ('vertex map not identity',m,r,v,end)
        mapped_paths.append(chain)
    cols=[]
    for (v,i),j in ind.items():
        w=perms[i][v]; end,chain=walk(tw[i],v)
        assert end==w
        cols.append(add((1,mapped_paths[v]),(1,chain),(-1,mapped_paths[w]),(-1,{j:1})))
    basis=span_basis(cols)
    witnesses=[]
    for i in range(m):
        v=perms[i][0]; power=1
        while v:
            v=perms[i][v]; power+=1; assert power<=q
        end,target=walk([i]*power); assert end==0
        rem=sparse_reduce(target,basis)
        if not rem:
            witnesses.append({'generator':i+1,'power':power,'visible':False}); continue
        free=min(rem); ell={free:Q(1)}
        for pivot,row in sorted(basis.items(),reverse=True):
            val=-sum(x*ell.get(k,0) for k,x in row.items() if k!=pivot)
            if val: ell[pivot]=val
        val=dot(ell,target); assert val
        ell={k:x/val for k,x in ell.items()}
        assert dot(ell,target)==1
        assert all(dot(ell,c)==0 for c in cols)
        witnesses.append({'generator':i+1,'power':power,'visible':True,'functional':encode(ell)})
    invariant_characters=[]
    if characters:
        for free in range(n):
            if free in basis: continue
            ell={free:Q(1)}
            for pivot,row in sorted(basis.items(),reverse=True):
                val=-sum(x*ell.get(k,0) for k,x in row.items() if k!=pivot)
                if val: ell[pivot]=val
            scale=math.lcm(*(x.denominator for x in ell.values()))
            intell={k:int(scale*x) for k,x in ell.items()}
            divisor=math.gcd(*intell.values())
            intell={k:x//divisor for k,x in intell.items()}
            assert all(dot(intell,c)==0 for c in cols)
            invariant_characters.append(encode(intell))
    return {'invariant_characters':invariant_characters,'m':m,'fiber_cover_degree':q,'stable_letter_power':r,'subgroup_index':q*r,
            'fiber_rank':n,'H1_subgroup_Q_dimension':1+n-len(basis),'basis_edges':edges,
            'permutations':perms,'theta_word_lengths':list(map(len,tw)),'witnesses':witnesses}


def double_cover(result, generator):
    witness=result['witnesses'][generator-1]; assert witness['visible']
    ell={int(k):Q(v) for k,v in witness['functional'].items()}
    scale=math.lcm(*(x.denominator for x in ell.values()))
    cochain={tuple(e):int(scale*ell.get(j,0))%2 for j,e in enumerate(result['basis_edges'])}
    old=result['permutations']; q=result['fiber_cover_degree']; m=result['m']
    perms=[[old[i][v] + q*((s+cochain.get((v,i),0))%2) for s in range(2) for v in range(q)] for i in range(m)]
    return perms,2*result['stable_letter_power'], {'generator':generator,'integer_character_scale':scale,'cochain':{str(v)+','+str(i):x for (v,i),x in cochain.items() if x}}

if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--rank',type=int,default=5); parser.add_argument('--steps',type=int,default=1); parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args(); m=args.rank; q=2**m; perms=[[v^(1<<i) for v in range(q)] for i in range(m)]
    r=1
    while r<m: r*=2
    current=analyze(m,perms,r); results=[current]; extensions=[]
    print('initial',m,current['H1_subgroup_Q_dimension'],[w['generator'] for w in current['witnesses'] if w['visible']],flush=True)
    for step in range(args.steps):
        # Use a2 whenever available: test whether its detection can reveal a1.
        perms,r,extension=double_cover(current,2); extensions.append(extension)
        current=analyze(m,perms,r); results.append(current)
        print('extension',step+1,current['subgroup_index'],current['H1_subgroup_Q_dimension'],[w['generator'] for w in current['witnesses'] if w['visible']],flush=True)
    args.output.write_text(json.dumps({'scope':'Selected iterated invariant-character covers; finite experiments do not establish virtual specialness or universal invisibility','results':results,'extensions':extensions},indent=2)+'\n')
