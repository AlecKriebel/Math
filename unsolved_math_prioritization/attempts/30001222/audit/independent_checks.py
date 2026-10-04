#!/usr/bin/env python3
"""Independent authored checks. Does not import or execute the author's checker.

Multiplication is obtained by string rewriting. Hochschild 1-cocycles are
computed from all basis-pair Leibniz equations on n*n arbitrary linear-map
coefficients, rather than from relations on generator images.
"""
import itertools
import json
from functools import lru_cache

class Rank:
    def __init__(self,p): self.p=p; self.rows={}; self.count=0
    def push(self,row):
        self.count+=1
        row={k:v%self.p for k,v in row.items() if v%self.p}
        while row:
            c=min(row); a=row[c]
            if c not in self.rows:
                z=pow(a,-1,self.p)
                self.rows[c]={k:v*z%self.p for k,v in row.items()}
                return
            for k,v in self.rows[c].items():
                r=(row.get(k,0)-a*v)%self.p
                if r: row[k]=r
                else: row.pop(k,None)
    def __len__(self): return len(self.rows)
    def kernel(self,n):
        out=[]
        for f in range(n):
            if f in self.rows: continue
            v={f:1}
            for c,row in sorted(self.rows.items(),reverse=True):
                val=-sum(a*v.get(k,0) for k,a in row.items() if k!=c)%self.p
                if val:v[c]=val
            out.append(v)
        return out

def add(row,k,v): row[k]=row.get(k,0)+v

class WordAlgebra:
    def __init__(self,p,e,q,beta=None):
        self.p,self.e,self.q,self.beta=p,e,q,beta
        self.words=['x'*i+'y'*j for i in range(e+1) for j in range(e+1)]
        self.ids={w:i for i,w in enumerate(self.words)}
        self.n=len(self.words)
        self.top=self.n-1
        self.rules=[('yx','xy',pow(q,-1,p)),('y'*(e+1),'',0),
                    ('x'*(e+1),'xxyy' if beta is not None else '',beta or 0)]
        self.table=[[self.normal(w+v) for v in self.words] for w in self.words]
    @lru_cache(None)
    def reduce(self,w,right=False):
        choices=[]
        for a,b,c in self.rules:
            at=w.find(a)
            while at>=0:
                choices.append((at,a,b,c));at=w.find(a,at+1)
        if not choices:return w,1
        at,a,b,c=(max(choices) if right else min(choices))
        if c==0:return '',0
        v,d=self.reduce(w[:at]+b+w[at+len(a):],right)
        return (v,c*d%self.p) if d else ('',0)
    def normal(self,w):
        v,c=self.reduce(w)
        return (self.ids[v],c) if c else None
    def composition(self,t,u,left=False):
        if t is None:return None
        i,c=t
        s=self.table[u][i] if left else self.table[i][u]
        return (s[0],s[1]*c%self.p) if s else None
    def commutator_rank(self):
        mat=Rank(self.p)
        for j in range(self.n):
            for k in range(self.n):
                row={}
                for i in range(self.n):
                    a,b=self.table[i][j],self.table[j][i]
                    if a and a[0]==k:add(row,i,a[1])
                    if b and b[0]==k:add(row,i,-b[1])
                mat.push(row)
        return mat
    def cocycle_rank(self):
        n=self.n;mat=Rank(self.p)
        for i in range(n):
            for j in range(n):
                rows=[{} for _ in range(n)]
                t=self.table[i][j]
                if t:
                    k,c=t
                    for out in range(n):add(rows[out],k*n+out,c)
                for s in range(n):
                    t=self.table[s][j]
                    if t:add(rows[t[0]],i*n+s,-t[1])
                    t=self.table[i][s]
                    if t:add(rows[t[0]],j*n+s,-t[1])
                for row in rows:mat.push(row)
        return mat
    def dual_basis(self):
        n=self.n;p=self.p
        mat=[[int(t is not None and t[0]==self.top)*(t[1] if t else 0) for t in row]
             +[int(i==j) for j in range(n)] for i,row in enumerate(self.table)]
        for c in range(n):
            i=next(i for i in range(c,n) if mat[i][c])
            mat[c],mat[i]=mat[i],mat[c]
            z=pow(mat[c][c],-1,p);mat[c]=[a*z%p for a in mat[c]]
            for i in range(n):
                if i!=c:
                    z=mat[i][c]
                    mat[i]=[(a-z*b)%p for a,b in zip(mat[i],mat[c])]
        return [[mat[j][n+i] for j in range(n)] for i in range(n)]
    def higman(self):
        dual=self.dual_basis();mat=Rank(self.p);images=[]
        for a in range(self.n):
            row={}
            for i in range(self.n):
                for j,c in enumerate(dual[i]):
                    if c:
                        t=self.composition(self.table[i][a],j)
                        if t:add(row,t[0],t[1]*c)
            row={k:v%self.p for k,v in row.items() if v%self.p}
            images.append(row);mat.push(row)
        return mat,images
    def radical_dims(self):
        dims=[self.n];S=set(range(self.n))
        while S:
            S={self.table[i][j][0] for i in S for j in range(1,self.n) if self.table[i][j]}
            dims.append(len(S))
        return dims
    def symbolic_cube(self):
        poly={}
        for i,j,k in itertools.product(range(1,self.n),repeat=3):
            t=self.composition(self.table[i][j],k)
            if t:add(poly,(tuple(sorted((i,j,k))),t[0]),t[1])
        return {key:v%self.p for key,v in poly.items() if v%self.p}
    def run(self):
        critical_words=0
        for n in range(11 if self.n==9 else 14):
            for bits in itertools.product('xy',repeat=n):
                w=''.join(bits)
                assert self.reduce(w,False)==self.reduce(w,True)
                critical_words+=1
        triples=0
        for i,j,k in itertools.product(range(self.n),repeat=3):
            assert self.composition(self.table[i][j],k)==self.composition(self.table[j][k],i,True)
            triples+=1
        assert all((a is None or a[0]!=self.top) and (b is None or b[0]!=self.top) or a==b
                   for i in range(self.n) for j in range(self.n)
                   for a,b in [(self.table[i][j],self.table[j][i])])
        center=self.commutator_rank();cocycles=self.cocycle_rank();H,images=self.higman()
        z=self.n-len(center);der=self.n*self.n-len(cocycles)
        result={'p':self.p,'e':self.e,'q':self.q,'beta':self.beta,'dimension':self.n,
                'derivation_dimension':der,'HH1_dimension':der-len(center),'center_dimension':z,
                'all_basis_leibniz_equations':cocycles.count,'cocycle_equation_rank':len(cocycles),
                'Higman_rank':len(H),'stable_center_dimension':z-len(H),
                'Higman_image_of_one':{self.words[k]:v for k,v in images[0].items()},
                'radical_power_dimensions':self.radical_dims(),
                'left_right_reduction_word_checks':critical_words,'associativity_triples':triples}
        if self.n==9:
            x,y=self.ids['x'],self.ids['y'];top=self.top
            want={((x,x,y),self.ids['xxy']):1,((y,y,x),self.ids['xyy']):1}
            want={(tuple(sorted(v)),k):c for (v,k),c in want.items()}
            if self.beta:want[((x,x,x),top)]=self.beta
            assert self.symbolic_cube()==want
            result['symbolic_cube_identity']=True
            result['symbolic_cube_monomials']=len(want)
            restricted=[]
            for v in cocycles.kernel(self.n*self.n):
                u=[v.get(x*self.n+k,0) for k in range(self.n)]
                w=[v.get(y*self.n+k,0) for k in range(self.n)]
                assert all(u[self.ids[z]]==0 for z in ('','y','xx'))
                assert all(w[self.ids[z]]==0 for z in ('','yy','x'))
                if self.beta:
                    assert (u[x]+w[y])%self.p==0
                    assert (u[self.ids['xxy']]+w[self.ids['xyy']]+w[self.ids['xx']])%self.p==0
                else:assert (u[self.ids['xxy']]+w[self.ids['xyy']])%self.p==0
                restricted.append(u+w)
            image_rank=Rank(self.p)
            for v in restricted:image_rank.push(dict(enumerate(v)))
            assert len(image_rank)==der
            result['displayed_generator_derivation_constraints_verified']=True
        return result

def main():
    algebras=[WordAlgebra(11,5,3),WordAlgebra(11,5,9),WordAlgebra(3,2,2,0),WordAlgebra(3,2,2,1)]
    results=[A.run() for A in algebras]
    common_center_checks=[]
    for A,B in [(algebras[0],algebras[1]),(algebras[2],algebras[3])]:
        KA=A.commutator_rank().kernel(A.n);KB=B.commutator_rank().kernel(B.n)
        assert KA==KB
        assert all(len(v)==1 and list(v.values())==[1] for v in KA)
        ids=[next(iter(v)) for v in KA]
        for i,j in itertools.product(ids,repeat=2):assert A.table[i][j]==B.table[i][j]
        common_center_checks.append({'dimension':A.n,'basis_words':[A.words[i] for i in ids],
                                    'matching_center_products':len(ids)**2})
    assert [(r['derivation_dimension'],r['center_dimension'],r['HH1_dimension'],r['stable_center_dimension'])
            for r in results]==[(36,12,12,11),(36,12,12,11),(11,6,8,6),(10,6,7,6)]
    print(json.dumps({'status':'PASS_INDEPENDENT_WORD_AND_FULL_COCYCLE_CHECKS','results':results,'center_comparisons':common_center_checks},indent=2,sort_keys=True))
if __name__=='__main__':main()
