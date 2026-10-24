#!/usr/bin/env python3
"""Reproducible bounded local search in larger odd abelian groups.

Every successful witness is exact. Failure of this heuristic is UNKNOWN, never
an obstruction. All samples and their construction categories are retained.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import itertools
import json
import math
from pathlib import Path
import random
import time
from search import addition_table, coordinates, group_label, find_cycle


def utc(): return datetime.now(timezone.utc).isoformat()


def local_cycle(vertices, plus, rng, max_steps=30000, restarts=5):
    n=len(vertices)
    total_steps=0
    best=n
    for restart in range(restarts):
        path=[0]+rng.sample(vertices[1:],n-1)
        counts=Counter(plus[path[i]][path[(i+1)%n]] for i in range(n))
        score=n-len(counts)
        best=min(best,score)
        if score==0: return path, {'steps':total_steps,'restarts':restart,'best_deficiency':0}
        for step in range(max_steps):
            total_steps+=1
            # Reverse a proper segment not containing the anchored vertex.
            left,right=sorted(rng.sample(range(1,n),2))
            if left==1 and right==n-1: continue
            a,b,c,d=path[left-1],path[left],path[right],path[(right+1)%n]
            changes=Counter([plus[a][c],plus[b][d]])
            changes.subtract([plus[a][b],plus[c][d]])
            delta_distinct=sum(int(counts.get(color,0)+delta>0)-int(counts.get(color,0)>0) for color,delta in changes.items())
            newscore=score-delta_distinct
            # Equal-score moves explore plateaux. Rare uphill moves escape traps.
            uphill_probability=0.01 if step < max_steps*0.9 else 0.001
            if newscore <= score or rng.random()<uphill_probability**(newscore-score):
                path[left:right+1]=reversed(path[left:right+1])
                for color,delta in changes.items():
                    counts[color]+=delta
                    if counts[color]==0: del counts[color]
                score=newscore
                best=min(best,score)
                if score==0:
                    return path, {'steps':total_steps,'restarts':restart,'best_deficiency':0}
    return None, {'steps':total_steps,'restarts':restarts,'best_deficiency':best}


def samples(moduli, seed, random_per_size):
    q=math.prod(moduli)
    rng=random.Random(seed)
    labels={}
    def add(vertices,label):
        mask=sum(1<<v for v in vertices)
        if mask&1 and mask.bit_count()>2:
            labels.setdefault(mask,set()).add(label)
    full=set(range(q))
    add(full,'whole_group')
    for v in range(1,q): add(full-{v},'every_single_nonzero_omission')
    if q<=27:
        for omitted in itertools.combinations(range(1,q),2): add(full-set(omitted),'every_pair_nonzero_omission')
    # Every union containing the zero coset of each coordinate-prefix subgroup,
    # provided its quotient has at most 9 cosets; otherwise random coset unions.
    for rank in range(1,len(moduli)):
        h=math.prod(moduli[:rank])
        cosets=[set(range(k*h,(k+1)*h)) for k in range(q//h)]
        quotient_order=len(cosets)
        if quotient_order<=9:
            for bits in range(1 << (quotient_order-1)):
                union=set(cosets[0])
                for i in range(1,quotient_order):
                    if bits>>(i-1)&1: union.update(cosets[i])
                add(union,f'all_prefix_rank{rank}_coset_unions')
        else:
            for _ in range(50):
                union=set(cosets[0])
                for coset in cosets[1:]:
                    if rng.randrange(2): union.update(coset)
                add(union,f'50_sampled_prefix_rank{rank}_coset_unions')
    # Initial coordinate boxes; include every endpoint length combination.
    for lengths in itertools.product(*(range(1,m+1) for m in moduli)):
        add((v for v in range(q) if all(x<length for x,length in zip(coordinates(v,moduli),lengths))), 'all_initial_coordinate_boxes')
    # Centrally symmetric subsets contain 0 and are unions of pairs {v,-v}.
    plus=addition_table(moduli)
    pairs=[]
    seen={0}
    for v in range(1,q):
        if v in seen: continue
        neg=next(w for w in range(1,q) if plus[v][w]==0)
        pairs.append({v,neg}); seen.update((v,neg))
    for _ in range(100):
        chosen={0}
        for pair in pairs:
            if rng.randrange(2): chosen.update(pair)
        add(chosen,'100_sampled_centrally_symmetric_sets')
    # Uniform samples in every cardinality 3..q. Deduplicate explicitly.
    for n in range(3,q+1):
        for _ in range(random_per_size):
            add([0]+rng.sample(range(1,q),n-1), f'{random_per_size}_uniform_samples_per_size')
    return labels


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--random-per-size',type=int,default=8)
    ap.add_argument('--seed',type=int,default=211302026)
    args=ap.parse_args(); args.output.mkdir(parents=True,exist_ok=True)
    groups=[(3,3,3),(5,5),(3,9),(7,7),(3,3,3,3),(5,5,5)]
    summary={'started_utc':utc(),'seed':args.seed,'method':'bounded randomized 2-opt local search, with complete DFS only for n<=9','finite_samples_only':True,'groups':[]}
    for gi,moduli in enumerate(groups):
        groupstart=time.perf_counter()
        label=group_label(moduli); plus=addition_table(moduli); q=len(plus)
        labels=samples(moduli,args.seed+gi,args.random_per_size)
        rng=random.Random(args.seed+1000+gi)
        path=args.output/(label+'.jsonl')
        unknown=[]; stats=[]
        with path.open('w') as out:
            out.write(json.dumps({'format':'odd-rainbow-cycle-v1','moduli':moduli,'order':q,'fixed_start':0,'domain':'listed_samples','attempted_subsets':len(labels),'covered_subsets':len(labels),'seed':args.seed+gi,'random_per_size':args.random_per_size})+'\n')
            for mask,categories in sorted(labels.items()):
                vertices=[v for v in range(q) if mask>>v&1]
                started=time.perf_counter()
                if len(vertices)<=9:
                    cycle,st=find_cycle(vertices,plus)
                    st['method']='complete_dfs'
                else:
                    cycle,st=local_cycle(vertices,plus,rng)
                    st['method']='bounded_2opt'
                st.update({'mask':mask,'n':len(vertices),'elapsed_seconds':time.perf_counter()-started})
                stats.append(st)
                if cycle is None:
                    unknown.append({'mask':mask,'vertices':vertices,'categories':sorted(categories),**st})
                else:
                    out.write(json.dumps({'mask':mask,'cycle':cycle,'categories':sorted(categories)},separators=(',',':'))+'\n')
                if len(stats)%100==0: print(f'{label}: {len(stats)}/{len(labels)}, unknown={len(unknown)}, elapsed={time.perf_counter()-groupstart:.2f}s',flush=True)
        result={'group':label,'moduli':moduli,'order':q,'attempted_subsets':len(labels),'found_witnesses':len(labels)-len(unknown),'unknown':unknown,'elapsed_seconds':time.perf_counter()-groupstart,'max_search_seconds':max(s['elapsed_seconds'] for s in stats),'total_local_steps':sum(s.get('steps',0) for s in stats),'max_local_steps':max(s.get('steps',0) for s in stats),'hardest_by_time':max(stats,key=lambda s:s['elapsed_seconds'])}
        summary['groups'].append(result)
        # A sample failure changes coverage to the successful lines only; it is
        # not silently counted among witnesses or called a counterexample.
        if unknown:
            lines=path.read_text().splitlines(); header=json.loads(lines[0]); header['covered_subsets']=result['found_witnesses']; lines[0]=json.dumps(header); path.write_text('\n'.join(lines)+'\n')
        print(json.dumps(result),flush=True)
        (args.output/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
    summary['finished_utc']=utc()
    (args.output/'summary.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')

if __name__=='__main__': main()
