#!/usr/bin/env python3
"""Independent exact diagnostics; no candidate or peer code is imported.

Free-algebra coefficients are in Z[A,B]. Finite rank checks are diagnostics,
not extrapolated universal proofs. Written tensor-ideal proof is REPORT.md.
"""
import itertools
import json


def need(condition, message):
    if not condition:
        raise ValueError(message)


def clean(p):
    return {m: c for m, c in p.items() if c}


def term(coefficient=1, ae=0, be=0, word=()):
    return {(ae, be, tuple(word)): coefficient} if coefficient else {}


def add(*polynomials):
    out = {}
    for p in polynomials:
        for m, c in p.items():
            out[m] = out.get(m, 0) + c
    return clean(out)


def scale(p, c):
    return clean({m: c*v for m, v in p.items()})


def mul(p, q):
    out = {}
    for (a, b, u), c in p.items():
        for (d, e, v), f in q.items():
            m = (a+d, b+e, u+v)
            out[m] = out.get(m, 0) + c*f
    return clean(out)


def product(*parts):
    out = term()
    for p in parts:
        out = mul(out, p)
    return out


def substitute(p, images):
    out = {}
    for (a, b, word), c in p.items():
        out = add(out, product(term(c, a, b), *(images[i] for i in word)))
    return out


def commute(p):
    out = {}
    for (a, b, word), c in p.items():
        word = tuple(sorted(word))
        m = (a, b, word)
        out[m] = out.get(m, 0) + c
    return clean(out)


A, B = term(ae=1), term(be=1)
x = {i: term(word=(i,)) for i in range(1, 5)}
one = term()


def source_relations():
    # Directly transcribed, expanded literal six relations, before reading code.
    table = [
        [(1,1,0,(1,1)),(-1,0,0,(1,3)),(1,0,0,(3,1)),(-1,1,0,(3,3))],
        [(1,1,0,(1,2)),(-1,0,0,(1,4)),(1,0,0,(3,2)),(-1,1,0,(3,4))],
        [(1,1,0,(2,1)),(-1,0,0,(2,3)),(1,0,0,(4,1)),(-1,1,0,(4,3))],
        [(1,1,0,(2,2)),(-1,0,0,(2,4)),(1,0,0,(4,2)),(-1,1,0,(4,4))],
        [(1,0,1,(1,1)),(-1,0,0,(1,2)),(1,0,0,(4,1)),(-1,0,1,(4,2))],
        [(1,0,1,(1,3)),(-1,0,0,(1,4)),(1,0,0,(4,3)),(-1,0,1,(4,4))],
    ]
    return [add(*(term(c,a,b,w) for c,a,b,w in row)) for row in table]


g = add(product(B,x[1],x[1]), scale(product(x[1],x[2]),-1),
        product(x[2],x[1]), scale(product(B,x[2],x[2]),-1))
commutator = add(product(x[1],x[2]),scale(product(x[2],x[1]),-1))
determinant = add(one,scale(product(B,B),-1))
twist = {1:add(x[1],mul(B,x[2])), 2:add(mul(B,x[1]),x[2])}


def tensor_twist(p):
    """C_n(v1...vn)=v1 T(v2)...T**(n-1)(vn), in the free algebra."""
    longest = max((len(k[2]) for k in p), default=0)
    powers = [{1:x[1],2:x[2]}]
    for _ in range(longest):
        powers.append({i:substitute(powers[-1][i],twist) for i in (1,2)})
    out = {}
    for (a,b,word),c in p.items():
        out = add(out, product(term(c,a,b),*(powers[j][i] for j,i in enumerate(word))))
    return out


class Field:
    def __init__(self, p, extension=False):
        self.p, self.extension = p, extension
        self.order = 4 if extension else p

    def add(self,a,b):
        return a ^ b if self.extension else (a+b)%self.p

    def neg(self,a):
        return a if self.extension else (-a)%self.p

    def mul(self,a,b):
        if not self.extension:
            return a*b%self.p
        out=0
        while b:
            if b&1: out ^= a
            b >>= 1
            a <<= 1
            if a&4: a ^= 7  # z^2+z+1 over F2
        return out

    def power(self,a,n):
        out=1
        for _ in range(n): out=self.mul(out,a)
        return out

    def inverse(self,a):
        need(a!=0,"inverse of zero")
        for b in range(1,self.order):
            if self.mul(a,b)==1: return b
        raise ValueError("not a field")


def rank(rows, field):
    # Sparse row elimination, exact in the chosen finite field.
    pivots={}
    for source in rows:
        row={i:c for i,c in source.items() if c}
        while row:
            j=min(row)
            if j not in pivots:
                inv=field.inverse(row[j])
                pivots[j]={i:field.mul(c,inv) for i,c in row.items()}
                break
            factor=row[j]
            for i,c in pivots[j].items():
                row[i]=field.add(row.get(i,0),field.neg(field.mul(factor,c)))
                if not row[i]: del row[i]
    return len(pivots)


def finite_relation_rank(n,beta,field):
    words=list(itertools.product((1,2),repeat=n))
    index={w:i for i,w in enumerate(words)}
    relation={(1,1):beta,(1,2):field.neg(1),(2,1):1,(2,2):field.neg(beta)}
    rows=[]
    for r in range(n-1):
        for u in itertools.product((1,2),repeat=r):
            for v in itertools.product((1,2),repeat=n-r-2):
                rows.append({index[u+w+v]:c for w,c in relation.items() if c})
    return len(words)-rank(rows,field)


def run():
    relations=source_relations()
    quotient={1:x[1],2:x[2],3:x[1],4:x[2]}
    images=[substitute(f,quotient) for f in relations]
    need(images==[{},{},{},{},g,g],"exact quotient relation images")
    need(all(not substitute(f,{i:x[1] for i in x}) for f in relations),"scalar quotient")
    # C_2 transforms relation to -det(T) times commutator in the free algebra.
    need(tensor_twist(g)==scale(mul(determinant,commutator),-1),"tensor relation identity")
    need(substitute(g,twist)==mul(determinant,g),"simultaneous T preserves relation line")
    need(not commute(tensor_twist(g)),"correct twisted product")
    need(bool(commute(g)),"untwisted multiplication must fail generically")
    inverse_lift={1:add(x[1],scale(mul(B,x[2]),-1)),2:add(scale(mul(B,x[1]),-1),x[2])}
    inverse_image={}
    for (a,b,word),c in g.items():
        inverse_image=add(inverse_image,product(term(c,a,b),x[word[0]],inverse_lift[word[1]]))
    expected=add(term(2,be=1,word=(1,1)),term(-2,be=1,word=(2,2)))
    need(commute(inverse_image)==expected,"inverse convention negative control")
    # Characteristic-free normal-form substitution X=U+V,Y=V.
    uv=substitute(g,{1:add(x[1],x[2]),2:x[2]})
    expected_uv=add(product(B,x[1],x[1]),product(add(B,scale(one,-1)),x[1],x[2]),
                    product(add(B,one),x[2],x[1]))
    need(uv==expected_uv,"division-free change of basis")
    # beta=+/-1 are excluded for a substantive reason: product of nonzero linear forms.
    for b in (-1,1):
        specialized={}
        for (a,e,w),c in g.items():
            specialized=add(specialized,term(c*b**e,a,0,w))
        factors=mul(add(x[1],x[2]),add(x[1],scale(x[2],-1))) if b==1 else scale(mul(add(x[1],scale(x[2],-1)),add(x[1],x[2])),-1)
        need(specialized==factors,"singular parameter factorization")
    # C_n intertwining of each ideal placement, checked over Z[B], not only after commutation.
    placement_count=0
    for n in range(2,7):
        for r in range(n-1):
            for u in itertools.product((1,2),repeat=r):
                for v in itertools.product((1,2),repeat=n-r-2):
                    left=tensor_twist(product(term(word=u),g,term(word=v)))
                    suffix=tensor_twist(term(word=v))
                    for _ in range(r+2): suffix=substitute(suffix,twist)
                    coefficient=scale(one,-1)
                    for _ in range(r+1): coefficient=mul(coefficient,determinant)
                    right=product(coefficient,tensor_twist(term(word=u)),commutator,suffix)
                    need(left==right,"tensor ideal placement identity")
                    placement_count+=1
    # Explicit telescoping certificate for kernel of identifying all four letters.
    telescoping_count=0
    for n in range(1,6):
        for word in itertools.product((1,2,3,4),repeat=n):
            actual=add(term(word=word),term(-1,word=(1,)*n))
            certificate={}
            for j,letter in enumerate(word):
                certificate=add(certificate,product(term(word=word[:j]),
                    add(x[letter],scale(x[1],-1)),term(word=(1,)*(n-j-1))))
            need(actual==certificate,"telescoping kernel certificate")
            telescoping_count+=1
    # Each sign/index perturbation is checked for breaking at least quotient images or tensor identity.
    detected=0
    for i,f in enumerate(relations):
        m=next(iter(f))
        changed=dict(f); changed[m]=-changed[m]
        if substitute(changed,quotient)!=images[i]: detected+=1
    need(detected==6,"six relation sign controls")
    field_cases=[]
    for label,field,beta in [("F4_beta_z",Field(2,True),2),("F4_beta_z_plus_1",Field(2,True),3),
                             ("F5_beta_2",Field(5),2),("F7_beta_2",Field(7),2),("F7_beta_3",Field(7),3)]:
        need(field.add(1,field.neg(field.mul(beta,beta)))!=0,"finite twist determinant")
        dimensions=[finite_relation_rank(n,beta,field) for n in range(9)]
        need(dimensions==list(range(1,10)),"finite quotient dimensions")
        field_cases.append({"field":label,"degrees":list(range(9)),"quotient_dimensions":dimensions})
    return {"status":"PASS","coefficient_ring":"Z[alpha,beta]","six_relation_images":"0,0,0,0,g,g",
            "tensor_ideal_placement_identities":placement_count,"telescoping_kernel_certificates":telescoping_count,
            "relation_sign_controls":detected,"untwisted_target_negative_control":True,
            "inverse_lift_residual":"2 beta(a^2-b^2); zero in characteristic2, not a universal rejection",
            "singular_beta_boundaries_verified":[-1,1],"finite_field_degree_cases":field_cases,
            "finite_cases_are_diagnostics_only":True,"universal_proof":"REPORT.md"}


if __name__=="__main__":
    print(json.dumps(run(),sort_keys=True,indent=2))
