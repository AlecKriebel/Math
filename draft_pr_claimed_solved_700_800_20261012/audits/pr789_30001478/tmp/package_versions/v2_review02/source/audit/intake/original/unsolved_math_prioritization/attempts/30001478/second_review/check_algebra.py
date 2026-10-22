#!/usr/bin/env python3
"""Independent exact source-tensor and convention checks; standard library only.

No author/auditor code is imported. Tests supplement the written universal proof.
"""
import json
import sys


def need(ok, message):
    if not ok:
        raise ValueError(message)


# A polynomial is a dictionary from sorted strings of commuting variables to Z.
def plus(*polys):
    out = {}
    for p in polys:
        for mon, coeff in p.items():
            out[mon] = out.get(mon, 0) + coeff
    return {m: c for m, c in out.items() if c}


def times(*polys):
    out = {'': 1}
    for p in polys:
        new = {}
        for m, c in out.items():
            for n, d in p.items():
                mn = ''.join(sorted(m+n))
                new[mn] = new.get(mn, 0) + c*d
        out = {m: c for m, c in new.items() if c}
    return out


def scale(c, p):
    return {m: c*v for m, v in p.items() if c*v}


ONE, A, B, X, Y = {'': 1}, {'a': 1}, {'b': 1}, {'x': 1}, {'y': 1}

# Fresh transcription of the source displays, as (coefficient, parameter, word).
# The commutative parameter symbol is separate from the NONCOMMUTATIVE word.
RELATIONS = [
    [(1,'a','11'),(-1,'','13'),(1,'','31'),(-1,'a','33')],
    [(1,'a','12'),(-1,'','14'),(1,'','32'),(-1,'a','34')],
    [(1,'a','21'),(-1,'','23'),(1,'','41'),(-1,'a','43')],
    [(1,'a','22'),(-1,'','24'),(1,'','42'),(-1,'a','44')],
    [(1,'b','11'),(-1,'','12'),(1,'','41'),(-1,'b','42')],
    [(1,'b','13'),(-1,'','14'),(1,'','43'),(-1,'b','44')],
]
Q = [(1,'b','XX'),(-1,'','XY'),(1,'','YX'),(-1,'b','YY')]


def nc_collect(terms):
    out = {}
    for c, parameter, word in terms:
        key = (parameter, word)
        out[key] = out.get(key, 0) + c
    return {k: v for k, v in out.items() if v}


def twist_q(theta):
    variables = {'X': X, 'Y': Y}
    return plus(*(times({p:c},variables[w[0]],theta[w[1]]) for c,p,w in Q))


def symbolic_checks():
    substitution = {'1':'X','2':'Y','3':'X','4':'Y'}
    images = [nc_collect([(c,p,''.join(substitution[v] for v in w))
                          for c,p,w in relation]) for relation in RELATIONS]
    need(images == [{},{},{},{},nc_collect(Q),nc_collect(Q)],
         'The six substituted relations are not 0,0,0,0,Q,Q')
    need(nc_collect([(1,'','XY')]) != nc_collect([(1,'','YX')]),
         'Word order must not commute')
    theta = {'X':plus(X,times(B,Y)), 'Y':plus(times(B,X),Y)}
    need(not twist_q(theta), 'Pullback twist does not annihilate Q')
    inverse_lift = {'X':plus(X,scale(-1,times(B,Y))),
                    'Y':plus(Y,scale(-1,times(B,X)))}
    need(twist_q(inverse_lift) == plus(scale(2,times(B,X,X)),
                                     scale(-2,times(B,Y,Y))),
         'Inverse-lift residual is not the expected nonzero polynomial')
    need(twist_q({'X':X,'Y':Y}) == plus(times(B,X,X),scale(-1,times(B,Y,Y))),
         'Untwisted residual is not the expected nonzero polynomial')
    changed = []
    linear = {'X':['U','V'],'Y':['V']}
    for c,p,w in Q:
        changed.extend((c,p,u+v) for u in linear[w[0]] for v in linear[w[1]])
    expected = [(1,'b','UU'),(1,'b','UV'),(-1,'','UV'),
                (1,'b','VU'),(1,'','VU')]
    need(nc_collect(changed)==nc_collect(expected), 'Ore relation change failed')
    # beta = 1 and beta = -1 are genuinely singular boundaries.
    at_one = [(c,'',w) for c,p,w in Q]
    at_minus_one = [(c*(-1 if p=='b' else 1),'',w) for c,p,w in Q]
    factor_one=[(c*d,'',u+v) for c,u in [(1,'X'),(1,'Y')]
                            for d,v in [(1,'X'),(-1,'Y')]]
    factor_minus_one=[(-c*d,'',u+v) for c,u in [(1,'X'),(-1,'Y')]
                                   for d,v in [(1,'X'),(1,'Y')]]
    need(nc_collect(at_one)==nc_collect(factor_one), 'beta=1 boundary')
    need(nc_collect(at_minus_one)==nc_collect(factor_minus_one), 'beta=-1 boundary')
    R={'r':1}
    rp=plus(R,ONE); rm=plus(R,scale(-1,ONE))
    need(plus(times(rp,rp),scale(-1,times(rm,rm)))==scale(4,R),
         'Fractional parameter determinant numerator must be 4 rho')
    need({m:c%2 for m,c in rp.items()}=={m:c%2 for m,c in rm.items()},
         'Fractional parameter numerator/denominator collapse in characteristic 2')
    # Noncommutative product has no VU self-overlap; irreducibles are U^i V^j.
    need('VU'[0] != 'VU'[-1], 'Unexpected rewriting self-overlap')
    return {
        'source_relation_count': 6,
        'quotient_images': ['0','0','0','0','Q','Q'],
        'twist_pullback_residual': '0',
        'inverse_lift_residual': '2 beta (X^2-Y^2)',
        'ordinary_product_residual': 'beta (X^2-Y^2)',
        'ore_change': 'beta U^2 + (beta-1) UV + (beta+1) VU',
        'journal_determinant_numerator': '4 rho',
        'journal_fractional_change_collapses_in_characteristic_two': True,
        'excluded_boundary_factorizations': ['Q(1)=(X+Y)(X-Y)',
                                              'Q(-1)=-(X-Y)(X+Y)'],
    }


# GF(4)=GF(2)[w]/(w^2+w+1), encoded by two-bit integers.
def fm(a,b):
    out=0
    while b:
        if b&1: out ^= a
        b >>= 1
        a <<= 1
        if a&4: a ^= 7
    return out


def fp(a,n):
    out=1
    for _ in range(n): out=fm(out,a)
    return out


def product(a,b):
    out=[0]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b): out[i+j] ^= fm(x,y)
    return out


def rank(rows,ncols):
    pivots={}
    for original in rows:
        row=list(original)
        for j in range(ncols):
            if not row[j]: continue
            if j in pivots:
                multiple=row[j]
                row=[x^fm(multiple,y) for x,y in zip(row,pivots[j])]
            else:
                inv=fp(row[j],2)
                row=[fm(x,inv) for x in row]
                need(row[j]==1,'GF(4) pivot inverse is wrong')
                pivots[j]=row
                break
    return len(pivots)


def characteristic_two_checks():
    need(all(fm(x,fp(x,2))==1 for x in (1,2,3)), 'GF(4) inverse check failed')
    need(fm(2,2)==3 and fm(2,3)==1,'GF(4) defining polynomial failed')
    result=[]
    for beta in (2,3):
        need(1^fm(beta,beta)!=0, 'The GF(4) matrix is singular')
        # theta^n(X), theta^n(Y) start at X,Y.
        tx,ty=[1,0],[0,1]
        rows=[[1]]
        degrees=[]
        for n in range(9):
            r=rank(rows,n+1)
            need(r==n+1, 'Twisted word image fails to span degree '+str(n))
            degrees.append({'degree':n,'word_count':len(rows),'rank':r})
            rows=[product(row,t) for row in rows for t in (tx,ty)]
            tx,ty=([tx[i]^fm(beta,ty[i]) for i in range(2)],
                   [fm(beta,tx[i])^ty[i] for i in range(2)])
        # Direct Ore relation in the degree-two twisted polynomial algebra.
        sx,sy=[1,beta],[beta,1]
        U=[1,1]; V=[0,1]
        tu=[sx[i]^sy[i] for i in range(2)]
        vu=product(V,tu); uv=product(U,sy); uu=product(U,tu)
        r=fm(beta,fp(1^beta,2))
        need(vu==[uv[i]^fm(r,uu[i]) for i in range(3)], 'Characteristic-2 Ore identity')
        result.append({'beta_encoding':beta,'degrees':degrees,'ore_identity':'PASS'})
    return result


def main():
    need(len(sys.argv)==1,'No arguments accepted')
    result={'status':'PASS','symbolic':symbolic_checks(),
            'gf4_checks':characteristic_two_checks(),
            'finite_controls_do_not_replace_universal_proof':True}
    print(json.dumps(result,sort_keys=True,indent=2))


if __name__=='__main__':
    try: main()
    except Exception as error:
        print('FAIL: '+str(error),file=sys.stderr)
        sys.exit(1)
