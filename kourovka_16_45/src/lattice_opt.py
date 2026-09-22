"""Exact combinatorial models; MILP optimization is exploratory, not a proof certificate.

For each selected meet-irreducible subgroup, an excluded cyclic subgroup must
be excluded by no other selected subgroup. This is exactly meet-irredundancy.
Optional constraints make the intersection trivial or conjugation-invariant.
"""
import json, time
from pathlib import Path
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint
from scipy.sparse import coo_array

class Lattice:
    def __init__(self, table, subgroup_data):
        self.table=table;self.n=len(table);self.full=(1<<self.n)-1
        self.subs=subgroup_data['subgroups'];self.masks=[sum(1<<x for x in h['elements']) for h in self.subs]
        self.lookup={m:i for i,m in enumerate(self.masks)}
        self.mi=[];self.cover={}
        for i,h in enumerate(self.masks):
            if h==self.full:continue
            meet=self.full
            for k in self.masks:
                if h!=k and (h&k)==h:meet&=k
            if meet!=h:self.mi.append(i);self.cover[i]=self.lookup[meet]
        self.inv=[int(np.flatnonzero(table[x]==0)[0]) for x in range(self.n)]
        self.cycs=[];self.cycgen=[];cs={}
        for x in range(1,self.n):
            a=x;mask=1
            while a!=0:mask|=1<<a;a=int(table[a,x])
            if mask not in cs:cs[mask]=len(self.cycs);self.cycs.append(mask);self.cycgen.append(x)
        # Normality is invariance of membership under all inner automorphisms.
        parent=list(range(len(self.cycs)))
        def find(a):
            while parent[a]!=a:parent[a]=parent[parent[a]];a=parent[a]
            return a
        elem_cyc={x:c for c,m in enumerate(self.cycs) for x in [self.cycgen[c]]}
        for c,x in enumerate(self.cycgen):
            for g in range(self.n):
                y=int(table[table[self.inv[g],x],g]);a=y;mask=1
                while a!=0:mask|=1<<a;a=int(table[a,y])
                parent[find(cs[mask])]=find(c)
        roots=sorted(set(find(c) for c in range(len(self.cycs))))
        self.classes=[roots.index(find(c)) for c in range(len(self.cycs))]
        self.normals=[]
        # all subgroup normality flags, independent of the cyclic orbit model
        for i,m in enumerate(self.masks):
            if all((m>>int(table[table[self.inv[g],x],g]))&1 for g in range(self.n) for x in self.subs[i]['generators']):self.normals.append(i)

    def optimize(self,mode='normal',time_limit=60):
        # mode 'arbitrary' returns mu'; 'faithful' returns b_f; 'normal' returns b.
        if self.n==1:return {'mode':mode,'value':0,'optimal':True,'selected':[],'intersection':[0]}
        r=len(self.mi);s=len(self.cycs);nc=max(self.classes)+1
        q=r+s+(nc if mode=='normal' else 0)
        excluded=[[i for i,h in enumerate(self.mi) if not ((self.masks[h]>>x)&1)] for x in self.cycgen]
        rows=[];cols=[];vals=[];lb=[];ub=[]
        def constraint(d,l=-np.inf,u=np.inf):
            j=len(lb)
            for k,v in d.items():
                if v:rows.append(j);cols.append(k);vals.append(v)
            lb.append(l);ub.append(u)
        for e,ex in enumerate(excluded):
            d=len(ex)
            # w_e=1 iff permitted as a unique-exclusion witness. Only implication is needed.
            constraint({**{i:1 for i in ex},r+e:-1},l=0)
            constraint({**{i:1 for i in ex},r+e:d-1},u=d)
            if mode=='faithful':constraint({i:1 for i in ex},l=1)
            if mode=='normal':
                u=r+s+self.classes[e]
                constraint({**{i:1 for i in ex},u:-1},l=0)
                constraint({**{i:1 for i in ex},u:-d},u=0)
        for i in range(r):
            constraint({**{r+e:-1 for e,ex in enumerate(excluded) if i in ex},i:1},u=0)
        A=coo_array((np.array(vals,dtype=float),(np.array(rows,dtype=np.int32),np.array(cols,dtype=np.int32))),shape=(len(lb),q)).tocsc()
        start=time.time()
        result=milp(c=np.array([-1.]*r+[0.]*(q-r)),integrality=np.ones(q),bounds=Bounds(np.zeros(q),np.ones(q)),constraints=LinearConstraint(A,lb,ub),options={'time_limit':time_limit,'mip_rel_gap':0.})
        out={'mode':mode,'optimal':result.status==0,'status':result.message,'seconds':time.time()-start,'variables':q,'constraints':len(lb),'subgroups':len(self.subs),'meet_irreducibles':r,'cyclic_subgroups_nontrivial':s}
        if result.x is not None:
            selected=[self.mi[i] for i in range(r) if result.x[i]>.5];inter=self.full
            for h in selected:inter&=self.masks[h]
            private=[]
            for h in selected:
                rest=self.full
                for k in selected:
                    if k!=h:rest&=self.masks[k]
                witness=rest&~self.masks[h]
                assert witness
                private.append((witness&-witness).bit_length()-1)
            assert mode!='normal' or self.lookup[inter] in self.normals
            assert mode!='faithful' or inter==1
            out.update(value=len(selected),selected=selected,intersection=[x for x in range(self.n) if (inter>>x)&1],witnesses=private,upper_bound=-float(result.mip_dual_bound),gap=float(result.mip_gap))
        return out

def load(name,directory):
    directory=Path(directory)
    tab=np.loadtxt(directory/f'{name}_table.txt',skiprows=1,dtype=np.int32)
    if tab.ndim==0:tab=tab.reshape(1,1)
    return Lattice(tab,json.loads((directory/f'{name}_subgroups.json').read_text()))
