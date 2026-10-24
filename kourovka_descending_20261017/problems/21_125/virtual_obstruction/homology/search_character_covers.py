#!/usr/bin/env python3
"""Search explicit integral invariant characters for a cover detecting a1."""
from check_iterated_covers import analyze
from fractions import Fraction as Q
import argparse, json, random, math
from pathlib import Path

p=argparse.ArgumentParser(); p.add_argument('--rank',type=int,default=5); p.add_argument('--trials',type=int,default=100); p.add_argument('--output',type=Path,required=True); args=p.parse_args()
m=args.rank; q=2**m; perms=[[v^(1<<i) for v in range(q)] for i in range(m)]; r=1
while r<m: r*=2
initial=analyze(m,perms,r,characters=True)
chars=[{int(k):int(v) for k,v in x.items()} for x in initial['invariant_characters']]
rng=random.Random(2112505); checks=[]; found=None
for trial in range(args.trials):
    if trial<len(chars): ell=chars[trial]; chosen=[trial]
    else:
        chosen=rng.sample(range(len(chars)),rng.randint(2,min(8,len(chars))))
        ell={}
        for j in chosen:
            for k,v in chars[j].items(): ell[k]=ell.get(k,0)+v
    cochain={tuple(e):ell.get(j,0)%2 for j,e in enumerate(initial['basis_edges'])}
    lifted=[[perms[i][v]+q*((s+cochain.get((v,i),0))%2) for s in range(2) for v in range(q)] for i in range(m)]
    result=analyze(m,lifted,2*r)
    visible=result['witnesses'][0]['visible']
    checks.append({'trial':trial,'chosen_integral_character_indices':chosen,'a1_visible':visible,'b1':result['H1_subgroup_Q_dimension']})
    if visible:
        found={'result':result,'cochain':{str(v)+','+str(i):x for (v,i),x in cochain.items() if x},'integral_character':{str(k):v for k,v in ell.items() if v},'chosen':chosen}
        print('FOUND',trial,chosen,result['H1_subgroup_Q_dimension'],flush=True); break
    if trial%10==0: print('trial',trial,'no a1',flush=True)
args.output.write_text(json.dumps({'scope':'Finite exact cover search, not a proof of persistent invisibility','initial':initial,'trials':checks,'found':found},indent=2)+'\n')
