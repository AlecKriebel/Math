import json,sys,subprocess
from pathlib import Path
from itertools import combinations
from groups import generated,save
from lattice_opt import load
BASE=Path(__file__).resolve().parents[1];DATA=BASE/'data'

def binary_icosahedral(p):
    I=(1,0,0,1);Z=(p-1,0,0,p-1);A=(0,p-1,1,0)
    def mul(a,b):return ((a[0]*b[0]+a[1]*b[2])%p,(a[0]*b[1]+a[1]*b[3])%p,(a[2]*b[0]+a[3]*b[2])%p,(a[2]*b[1]+a[3]*b[3])%p)
    def pow_(a,k):
        x=I
        for _ in range(k):x=mul(x,a)
        return x
    for a in range(p):
      for b in range(p):
        for c in range(p):
          B=(a,b,c,(1-a)%p)
          if (a*(1-a)-b*c)%p!=1:continue
          if pow_(mul(A,B),5)!=Z:continue
          e,t=generated([A,B],I,mul)
          if len(e)!=120:continue
          return (A,B),(e,t)
    raise ValueError('no generators found')

def closure(tab,gens):
    h={0};q=[0]
    for x in q:
        for g in gens:
            y=int(tab[x,g])
            if y not in h:h.add(y);q.append(y)
    return h

for p in [29,11]:
    name=f'BI_{p}';gens,group=binary_icosahedral(p);els,tab=group
    save(name,group,DATA)
    subprocess.run([str(BASE/'src/enumerate_subgroups'),str(DATA/f'{name}_table.txt'),str(DATA/f'{name}_subgroups.json')],check=True)
    order4=[x for x in range(1,120) if tuple(els[int(tab[x,x])])==(p-1,0,0,p-1)]
    triple=None
    for y,z in combinations(order4[1:],2):
        s=[order4[0],y,z]
        sizes=sorted(len(closure(tab,[s[i] for i in range(3) if i!=j])) for j in range(3))
        if sizes==[8,12,20] and len(closure(tab,s))==120:triple=s;break
    assert triple
    info={'p':p,'generators':gens,'complement_order':120,'independent_triple_indices':triple,'independent_triple_matrices':[els[x] for x in triple], 'pair_orders':[len(closure(tab,[s for s in triple if s!=x])) for x in triple]}
    L=load(name,DATA)
    info['normal_subgroups']=[L.subs[i]['elements'] for i in L.normals]
    info['odd_subgroup_orders']=sorted(set(len(h['elements']) for h in L.subs if len(h['elements'])%2))
    lines=[(1,a) for a in range(p)]+[(0,1)]
    line_stabs=[]
    for v in lines:
        stab=[i for i,h in enumerate(els) if ((h[0]*v[0]+h[1]*v[1])*v[1]-(h[2]*v[0]+h[3]*v[1])*v[0])%p==0]
        line_stabs.append(stab)
    info['line_stabilizer_orders']=sorted(set(map(len,line_stabs)))
    info['line_stabilizers']=line_stabs
    (DATA/f'{name}_structure.json').write_text(json.dumps(info,indent=2)+'\n')
    print(json.dumps({k:v for k,v in info.items() if k not in ['normal_subgroups','line_stabilizers']},indent=2))
