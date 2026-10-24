#!/usr/bin/env python3
"""Bounded conflict-focused swap search for previous UNKNOWN samples.

Also reuses certificates under exact group translations. Does not certify
nonexistence on failure. The original summary is retained as experiment history.
"""
from collections import Counter
from datetime import datetime,timezone
import json
import random
import time
from pathlib import Path
from search import addition_table
from verify import verify_file


def swap_search(vertices,plus,rng,max_steps=10000,restarts=3):
    n=len(vertices); best=n; total=0
    for restart in range(restarts):
        cycle=[0]+rng.sample(vertices[1:],n-1)
        colors=[plus[cycle[i]][cycle[(i+1)%n]] for i in range(n)]
        counts=Counter(colors); score=n-len(counts); best=min(best,score)
        if score==0: return cycle,{'steps':total,'restart':restart,'best_deficiency':0}
        for step in range(max_steps):
            total+=1
            # Choose a vertex incident with a duplicated color, then swap it.
            bad=[i for i,c in enumerate(colors) if counts[c]>1]
            edge=rng.choice(bad)
            i=rng.choice((edge,(edge+1)%n))
            if i==0: i=1 if edge==0 else n-1
            j=rng.randrange(1,n)
            if i==j: continue
            affected={(i-1)%n,i,(j-1)%n,j}
            old=[colors[e] for e in affected]
            def vertex(k):
                k%=n
                return cycle[j] if k==i else cycle[i] if k==j else cycle[k]
            new=[plus[vertex(e)][vertex(e+1)] for e in affected]
            changes=Counter(new); changes.subtract(old)
            newscore=score-sum(int(counts.get(c,0)+d>0)-int(counts.get(c,0)>0) for c,d in changes.items())
            uphill=0.003
            if newscore<=score or rng.random()<uphill**(newscore-score):
                cycle[i],cycle[j]=cycle[j],cycle[i]
                for e,c in zip(affected,new): colors[e]=c
                for c,d in changes.items():
                    counts[c]+=d
                    if counts[c]==0: del counts[c]
                score=newscore; best=min(best,score)
                if score==0: return cycle,{'steps':total,'restart':restart,'best_deficiency':0}
    return None,{'steps':total,'restart':restarts,'best_deficiency':best}


def main():
    root=Path(__file__).parent/'larger_samples'
    original=json.loads((root/'summary.json').read_text())
    report={'started_utc':datetime.now(timezone.utc).isoformat(),'method':'exact natural full-group cycle; translation reuse for one-point complements; bounded conflict-focused swaps otherwise','groups':[]}
    for group in original['groups']:
        path=root/(group['group']+'.jsonl'); rows=[json.loads(s) for s in path.read_text().splitlines()]; header=rows[0]; records={r['mask']:r for r in rows[1:]}; q=header['order']; full=(1<<q)-1; plus=addition_table(header['moduli']); rng=random.Random(211303000+q)
        missing=group['unknown']; rescued=[]; remaining=[]; started=time.perf_counter()
        # Whole group is immediate by triangular mixed-radix carry inversion.
        if full not in records:
            cycle=list(range(q)); assert len({plus[cycle[i]][cycle[(i+1)%q]] for i in range(q)})==q
            records[full]={'mask':full,'cycle':cycle,'categories':['whole_group'],'method':'natural_mixed_radix'}
        # Work one-point complements before the others, allowing reuse by translation.
        for item in sorted(missing,key=lambda x:(x['n']!=q-1,x['mask'])):
            mask=item['mask']
            if mask in records:
                rescued.append({'mask':mask,'method':records[mask].get('method','existing')}); continue
            cycle=None; stats={}
            if mask.bit_count()==q-1:
                candidates=[r for r in records.values() if r['mask'].bit_count()==q-1]
                if candidates:
                    source=candidates[0]; old_missing=(full^source['mask']).bit_length()-1; new_missing=(full^mask).bit_length()-1
                    delta=next(v for v in range(q) if plus[old_missing][v]==new_missing)
                    cycle=[plus[v][delta] for v in source['cycle']]; z=cycle.index(0); cycle=cycle[z:]+cycle[:z]
                    stats={'method':'translated_witness','source_mask':source['mask'],'translation':delta}
            if cycle is None:
                cycle,stats=swap_search(item['vertices'],plus,rng)
                stats['method']='bounded_conflict_swap'
            if cycle is None:
                remaining.append({**item,'rescue_stats':stats})
                print(group['group'],item['n'],'still UNKNOWN',stats,flush=True)
            else:
                records[mask]={'mask':mask,'cycle':cycle,'categories':item['categories'],**stats}
                rescued.append({'mask':mask,**stats})
        header['covered_subsets']=len(records)
        path.write_text('\n'.join(json.dumps(x,separators=(',',':')) for x in [header,*[records[k] for k in sorted(records)]])+'\n')
        checked=verify_file(path)
        result={'group':group['group'],'previous_unknown':len(missing),'rescued':rescued,'remaining_unknown':remaining,'found_witnesses':len(records),'elapsed_seconds':time.perf_counter()-started,'verification':checked}
        report['groups'].append(result)
        (root/'rescue_summary.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
        print(group['group'],len(missing),'previous unknown;',len(rescued),'rescued;',len(remaining),'still unknown;',f'{time.perf_counter()-started:.2f}s',flush=True)
    report['finished_utc']=datetime.now(timezone.utc).isoformat()
    (root/'rescue_summary.json').write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')

if __name__=='__main__': main()
