#!/usr/bin/env python3
"""Exact, standard-library checks for OWR-3400-006 partial results.

No stable equivalence is constructed or inferred from matching invariants.
Run: python verify.py > verification_results.json
"""
from itertools import product
import json

CHECKS = {}
def check(condition, label):
    CHECKS[label] = CHECKS.get(label, 0) + 1
    if not condition:
        raise AssertionError(label)

def rref(rows, p, width=None):
    if width is None:
        width = len(rows[0]) if rows else 0
    a = [[v % p for v in row] for row in rows if any(v % p for v in row)]
    pivots, r = [], 0
    for c in range(width):
        j = next((j for j in range(r, len(a)) if a[j][c]), None)
        if j is None:
            continue
        a[r], a[j] = a[j], a[r]
        inv = pow(a[r][c], -1, p)
        a[r] = [(v * inv) % p for v in a[r]]
        for j in range(len(a)):
            if j != r and a[j][c]:
                t = a[j][c]
                a[j] = [(v - t*w) % p for v, w in zip(a[j], a[r])]
        pivots.append(c)
        r += 1
        if r == len(a):
            break
    return a[:r], pivots

def rank(rows, p):
    return len(rref(rows, p)[1])

def kernel(rows, p, width):
    rr, pivots = rref(rows, p, width)
    basis = []
    for f in range(width):
        if f in pivots:
            continue
        v = [0]*width
        v[f] = 1
        for row, col in zip(rr, pivots):
            v[col] = -row[f] % p
        basis.append(v)
    return basis

class Algebra:
    """x*y=q*y*x, x^a=0,y^b=0; optional x^3=beta*x^2*y^2."""
    def __init__(self, p, a, b, q, beta=0):
        self.p, self.a, self.b, self.q, self.beta = p, a, b, q, beta
        if beta:
            assert (p,a,b,q)==(3,3,3,2)
        self.basis = list(product(range(a), range(b)))
        self.index = {m:i for i,m in enumerate(self.basis)}
        self.n = a*b
        self.zero = [0]*self.n
        self.one = self.unit(0)
        self.x = self.unit(self.index[(1,0)])
        self.y = self.unit(self.index[(0,1)])
        self.top = self.index[(a-1,b-1)]
        self.table=[]
        for i,j in self.basis:
            row=[]
            for k,l in self.basis:
                coeff=pow(q,-j*k,p)
                u,v=i+k,j+l
                if beta and (u,v)==(3,0):
                    row.append((self.top, coeff*beta%p))
                elif u<a and v<b:
                    row.append((self.index[(u,v)],coeff))
                else:
                    row.append(None)
            self.table.append(row)

    def unit(self,i):
        return [int(j==i) for j in range(self.n)]
    def add(self,u,v,c=1):
        return [(a+c*b)%self.p for a,b in zip(u,v)]
    def mul(self,u,v):
        out=[0]*self.n
        for i,a in enumerate(u):
            if not a: continue
            for j,b in enumerate(v):
                t=self.table[i][j]
                if b and t:
                    k,c=t;out[k]=(out[k]+a*b*c)%self.p
        return out
    def power(self,u,e):
        out=self.one
        for _ in range(e): out=self.mul(out,u)
        return out
    def dword(self,word,dx,dy):
        out=self.zero
        for i,letter in enumerate(word):
            v=self.one
            for j,w in enumerate(word):
                v=self.mul(v,(dx if w=='x' else dy) if i==j else (self.x if w=='x' else self.y))
            out=self.add(out,v)
        return out
    def dmatrix(self,dx,dy):
        # Columns are derivations of monomials.
        return [self.dword('x'*i+'y'*j,dx,dy) for i,j in self.basis]
    def apply(self,D,u):
        out=self.zero
        for c,v in zip(u,D):
            if c: out=self.add(out,v,c)
        return out

    def verify_associativity(self):
        def compose(t,k,right):
            if t is None:return None
            i,c=t
            s=self.table[i][k] if right else self.table[k][i]
            if s is None:return None
            j,d=s
            return j,c*d%self.p
        for i,j,k in product(range(self.n),repeat=3):
            check(compose(self.table[i][j],k,True)==compose(self.table[j][k],i,False),'associativity')

    def invariants(self):
        n,p=self.n,self.p
        self.verify_associativity()
        check(self.mul(self.x,self.y)==[(self.q*c)%p for c in self.mul(self.y,self.x)],'quantum_relation')
        check(self.power(self.y,self.b)==self.zero,'y_power_relation')
        check(self.power(self.x,self.a)==[self.beta*int(i==self.top)%p for i in range(n)],'x_power_relation')
        pairing=[[0 if t is None or t[0]!=self.top else t[1] for t in row] for row in self.table]
        check(pairing==list(map(list,zip(*pairing))),'symmetric_trace')
        check(rank(pairing,p)==n,'nondegenerate_trace')
        columns=[]
        for i in range(n):
            u=self.unit(i)
            columns.append(self.add(self.mul(u,self.x),self.mul(self.x,u),-1)+self.add(self.mul(u,self.y),self.mul(self.y,u),-1))
        centre=kernel(list(map(list,zip(*columns))),p,n)
        inner_dim=rank(columns,p)
        check(inner_dim==n-len(centre),'inner_equals_codim_centre')
        columns=[]
        for i in range(2*n):
            dx=self.unit(i) if i<n else self.zero
            dy=self.unit(i-n) if i>=n else self.zero
            rx=self.add(self.dword('x'*self.a,dx,dy),self.dword('xxyy',dx,dy),-self.beta)
            ry=self.dword('y'*self.b,dx,dy)
            rq=self.add(self.dword('xy',dx,dy),self.dword('yx',dx,dy),-self.q)
            columns.append(rx+ry+rq)
        derivs=kernel(list(map(list,zip(*columns))),p,2*n)
        for v in derivs:
            dx,dy=v[:n],v[n:]
            D=self.dmatrix(dx,dy)
            for i,j in product(range(n),repeat=2):
                u,w=self.unit(i),self.unit(j)
                check(self.apply(D,self.mul(u,w))==self.add(self.mul(D[i],w),self.mul(u,D[j])),'all_basis_leibniz')
        radical=set(range(1,n)); layers=[n]; current=set(range(n))
        while current:
            new={t[0] for i in current for j in radical if (t:=self.table[i][j]) is not None}
            if current==new: raise AssertionError('radical not nilpotent')
            layers.append(len(new));current=new
        return {'field':p,'a':self.a,'b':self.b,'q':self.q,'beta':self.beta,
                'dimension':n,'center_dimension':len(centre),'inner_derivation_dimension':inner_dim,
                'derivation_dimension':len(derivs),'HH1_dimension':len(derivs)-inner_dim,
                'radical_power_dimensions':layers,'radical_layer_dimensions':[a-b for a,b in zip(layers,layers[1:])]}

def center_indices(A,e):
    return [A.index[(0,0)]]+[A.index[t] for t in A.basis if t[0]==e or t[1]==e]

def equal_centers(A,B,indices):
    check(A.basis==B.basis,'common_monomial_indexing')
    for i in indices:
        for j in range(A.n):
            for C in (A,B):
                check(C.table[i][j]==C.table[j][i],'candidate_center_basis_central')
    for i,j in product(indices,repeat=2):
        check(A.table[i][j]==B.table[i][j],'identical_center_multiplication')

def linear_relation_maps(p,q,r):
    # Images x->ax+by, y->cx+dy in the target xy=r*yx.
    good=[];invertible=0
    for a,b,c,d in product(range(p),repeat=4):
        if (a*d-b*c)%p==0:continue
        invertible+=1
        if ((1-q)*a*c)%p or ((1-q)*b*d)%p:continue
        if (a*d*(1-q*pow(r,-1,p))+b*c*(pow(r,-1,p)-q))%p:continue
        good.append([a,b,c,d])
    return {'invertible_matrices_tested':invertible,'relation_preserving_count':len(good)}

def cube_zero_count(A):
    count=0
    # All 3^8 elements in the radical, a small exact finite control.
    for coeffs in product(range(3),repeat=8):
        z=[0]+list(coeffs)
        cube=A.power(z,3)
        a=z[A.index[(1,0)]];b=z[A.index[(0,1)]]
        expected=A.zero
        expected=A.add(expected,A.unit(A.index[(2,1)]),a*a*b)
        expected=A.add(expected,A.unit(A.index[(1,2)]),a*b*b)
        expected=A.add(expected,A.unit(A.top),A.beta*a*a*a)
        check(cube==expected,'cube_formula_all_radical_elements')
        count+=cube==A.zero
    return count

def main():
    A=Algebra(11,6,6,3);B=Algebra(11,6,6,9)
    for q in (3,9):
        check(pow(q,5,11)==1 and all(pow(q,j,11)!=1 for j in range(1,5)),'parameter_order_five')
    check(pow(3,-1,11)==4 and 9 not in (3,4),'parameters_not_inverse')
    invariants=[A.invariants(),B.invariants()]
    equal_centers(A,B,center_indices(A,5))
    check(invariants[0]['center_dimension']==12==invariants[1]['center_dimension'],'center_dimension_parameter_pair')
    maps={str(r):linear_relation_maps(11,3,r) for r in (3,4,9)}
    check(maps['3']['relation_preserving_count']==100,'isomorphism_positive_control')
    check(maps['4']['relation_preserving_count']==100,'inverse_isomorphism_control')
    check(maps['9']['relation_preserving_count']==0,'nonisomorphism_parameter_pair')
    C=Algebra(3,3,3,2);D=Algebra(3,3,3,2,beta=1)
    invariants += [C.invariants(),D.invariants()]
    for actual,expected in zip(invariants,[(36,12,12),(36,12,12),(11,6,8),(10,6,7)]):
        check((actual['derivation_dimension'],actual['center_dimension'],actual['HH1_dimension'])==expected,'predicted_derivation_center_HH1_dimensions')
    check(invariants[0]['radical_layer_dimensions']==invariants[1]['radical_layer_dimensions']==[1,2,3,4,5,6,5,4,3,2,1],'parameter_pair_radical_layers')
    check(invariants[2]['radical_layer_dimensions']==invariants[3]['radical_layer_dimensions']==[1,2,3,2,1],'deformation_pair_radical_layers')
    equal_centers(C,D,[C.index[t] for t in [(0,0),(2,0),(0,2),(2,1),(1,2),(2,2)]])
    counts=[cube_zero_count(C),cube_zero_count(D)]
    check(counts==[3645,2187],'deformation_cube_zero_counts')
    congruences={str(d):{'inverse_pairs':[[r,s] for r in range(1,d) for s in range(1,d) if r*s%d==1],
                          'square_roots_of_one':[r for r in range(1,d) if r*r%d==1]} for d in (9,25,36)}
    print(json.dumps({'status':'PASS_EXACT_PARTIAL_CHECKS','general_problem_resolved':False,
                     'stable_equivalence_constructed':False,'algebras':invariants,
                     'linear_relation_map_controls':maps,'radical_cube_zero_counts':counts,
                     'rank_congruence_controls':congruences,
                     'assertions_by_category':CHECKS,'assertions_total':sum(CHECKS.values())},indent=2,sort_keys=True))

if __name__=='__main__':main()
