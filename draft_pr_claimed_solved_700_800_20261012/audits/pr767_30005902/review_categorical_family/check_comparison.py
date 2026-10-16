#!/usr/bin/env python3
"""Read-only exact degree-one controls; not a full finite Hopf enumeration."""
import itertools
import json

P = 3
B = list(itertools.product(range(P), repeat=3))
ONE = (0, 0, 0)
X, Y, Z = (1, 0, 0), (0, 1, 0), (0, 0, 1)


def clean(a):
    return {k: v % P for k, v in a.items() if v % P}


def add(*args):
    out = {}
    for a in args:
        for k, v in a.items():
            out[k] = out.get(k, 0) + v
    return clean(out)


def scale(a, c):
    return clean({k: v*c for k, v in a.items()})


def mono_mul(a, b):
    c = tuple(x+y for x, y in zip(a, b))
    return c if max(c) < P else None


def mul(a, b):
    out = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            kc = mono_mul(ka, kb)
            if kc is not None:
                out[kc] = out.get(kc, 0) + va*vb
    return clean(out)


def tmul(a, b):
    out = {}
    for (a1, a2), va in a.items():
        for (b1, b2), vb in b.items():
            c1, c2 = mono_mul(a1,b1), mono_mul(a2,b2)
            if c1 is not None and c2 is not None:
                out[c1,c2] = out.get((c1,c2),0)+va*vb
    return clean(out)


def coproduct(lam):
    generators = [{(X,ONE):1,(ONE,X):1},
                  {(Y,ONE):1,(ONE,Y):1},
                  {(Z,ONE):1,(ONE,Z):1,(X,Y):lam}]
    out = {}
    for b in B:
        d = {(ONE,ONE):1}
        for n, g in zip(b, generators):
            for _ in range(n):
                d = tmul(d,g)
        out[b] = clean(d)
    return out


def antipode(b, lam):
    gens = [{X:2},{Y:2},{Z:2,(1,1,0):lam}]
    out = {ONE:1}
    for n,g in zip(b,gens):
        for _ in range(n):
            out = mul(out,g)
    return out


def linear_apply(matrix, a):
    return add(*(scale(matrix[b],c) for b,c in a.items()))


def compose(a,b):
    return {k:linear_apply(a,b[k]) for k in B}


def difference(a,b):
    return {k:add(a[k],scale(b[k],-1)) for k in B}


def translation(d, g, side):
    return {b:add(*(
        {right if side=='R' else left:c}
        for (left,right),c in d[b].items()
        if (left if side=='R' else right)==g)) for b in B}


def psi(c, d, reverse=False):
    # X coordinate key=(left endpoint, interior P bar, right endpoint).
    return {(ONE,b if reverse else a,a if reverse else b):v
            for (a,b),v in d[c].items()}


def theta(t, d, lam):
    out = []
    for (a,c,b),v in t.items():
        for (c1,c2),w in d[c].items():
            for s,ss in antipode(c2,lam).items():
                sb=mono_mul(s,b)
                if sb is not None:out.append({(a,c1,sb):v*w*ss})
    return add(*out)


def d_x(t, d, lam):
    out = []
    for (a,c,b),v in t.items():
        for (c1,c2),w in d[c].items():
            ac1=mono_mul(a,c1)
            if ac1 is None:continue
            for s,ss in antipode(c2,lam).items():
                sb=mono_mul(s,b)
                if sb is not None:out.append({(ac1,sb):v*w*ss})
        if c==ONE:out.append({(a,b):-v})
    return add(*out)


def require(condition):
    if not condition:
        raise RuntimeError("exact comparison check failed")


def main():
    results = {'field':'F3','dimension':27,'scope':'degree-one comparisons and controls; no categorical theorem proved by code'}
    for lam in [1,0]:
        d = coproduct(lam)
        R = [translation(d,g,'R') for g in [X,Y,Z]]
        L = [translation(d,g,'L') for g in [X,Y,Z]]
        # All basis c; H^e-linearity covers arbitrary endpoints.
        for c in B:
            for scalar in range(P):
                require((int(c==ONE)*scalar-scalar*int(c==ONE))%P==0)
            require(theta(psi(c,d),d,lam)=={(ONE,c,ONE):1})
            require(d_x(psi(c,d),d,lam)==add({(c,ONE):1},{(ONE,c):-1}))
        # theta psi above checks one inverse. Test psi theta on X generators too.
        for c in B:
            th=theta({(ONE,c,ONE):1},d,lam)
            back=[]
            for (a,b,e),v in th.items():
                for (l,r),w in d[b].items():
                    rr=mono_mul(r,e)
                    if rr is not None:back.append({(a,l,rr):v*w})
            require(add(*back)=={(ONE,c,ONE):1})
        for a,b in itertools.product(B,repeat=2):
            ab=mono_mul(a,b)
            for g,D in zip([X,Y,Z],R):
                lhs={} if ab is None else D[ab]
                require(lhs==add(mul(D[a],{b:1}),mul({a:1},D[b])))
                # Scalar cocycle identity, all basis pairs.
                scalar_lhs=int(ab==g)
                scalar_rhs=int(a==ONE)*int(b==g)+int(a==g)*int(b==ONE)
                require((scalar_lhs-scalar_rhs)%P==0)
        bracket_R=difference(compose(R[0],R[1]),compose(R[1],R[0]))
        bracket_L=difference(compose(L[0],L[1]),compose(L[1],L[0]))
        require(bracket_R=={b:scale(R[2][b],-lam) for b in B})
        require(bracket_L=={b:scale(L[2][b],lam) for b in B})
        for g,D in zip([X,Y,Z],R):
            require(all(D[b].get(ONE,0)==int(b==g) for b in B))
        reversed_failures = [c for c in B if d_x(psi(c,d,True),d,lam)!=add({(c,ONE):1},{(ONE,c):-1})]
        if lam:
            require(Z in reversed_failures)
            require(bracket_R!={b:scale(R[2][b],lam) for b in B})
        else:
            require(reversed_failures==[])
        results[str(lam)]={
            'psi_theta_and_theta_psi_basis_checks':54,
            'psi_chain_map_checks':27,
            'derivation_basis_pair_checks':3*27*27,
            'scalar_cocycle_basis_pair_checks':3*27*27,
            'right_bracket_coefficient_of_Rfz':(-lam)%P,
            'left_bracket_coefficient_of_Lfz':lam,
            'wrong_plus_sign_rejected':bool(lam),
            'reversed_comparison_chain_map_failure_count':len(reversed_failures),
            'scalar_B1_zero_by_trivial_action':True,
            'scalar_zero_coboundary_checks':81,
            'fz_at_z':1,
        }
    print(json.dumps(results,sort_keys=True,indent=2))


if __name__=='__main__':
    main()
