#!/usr/bin/env python3
"""Exact discovery/audit of the d=4 polynomial SOS. Not Lean verification."""
from exact_preflight import *
import sys

def run_first_sos():
    ck=Checks(); one={EMPTY:ONE}
    a0={((1,),()):ONE}; a1={((2,),()):ONE}
    bob=[{((),(y+1,)):ONE} for y in range(5)]
    u=poly_mul(poly_star(a0),a1)
    s=(zeta(1)-zeta(-1))/(2*zeta(4)); k=zeta(2)+zeta(-2)
    m=2/s
    def add(*p):return poly_add(*p)
    def sc(c,p):return poly_scale(c,p)
    def mul(*p):
        v=one
        for q in p:v=poly_mul(v,q)
        return v
    def sq(p):return mul(poly_star(p),p)
    squares=[]; terms=[]
    for y in range(4):
        t=sc(zeta(4*y),u);t2=mul(t,t);t3=mul(t2,t)
        p=sc(s,add(one,sc(2+k,t),t2))
        q=sc(s/2,add(sc(-k,one),sc(2+k,t),sc(2+k,t2),sc(-k,t3)))
        f=add(mul(add(one,t),poly_star(a0)),sc(-1,mul(p,bob[y])))
        g=add(mul(t,poly_star(a0)),sc(-1,mul(q,bob[y])))
        cross=sc(s,add(mul(poly_star(add(one,t)),p),sc(k,mul(poly_star(t),q))))
        ck.eq(f'cross factorization y={y}',cross,add(one,t))
        squares.append(sc(s/2,add(sq(f),sc(k,sq(g)))))
        op=mul(add(a0,sc(zeta(4*y),a1)),bob[y])
        terms.append(sc(Q(1,2),add(op,poly_star(op))))
    lhs=add(sc(m,one),sc(-1,add(*terms)));rhs=add(*squares)
    ck.eq('first reduced exact polynomial SOS',lhs,rhs)
    ab=mul(a0,bob[4]);res=add(one,sc(-1,ab))
    alhs=add(lhs,one,sc(Q(-1,2),add(ab,poly_star(ab))))
    arhs=add(rhs,sc(Q(1,2),sq(res)))
    ck.eq('first augmented exact polynomial SOS',alhs,arhs)
    ck.different('wrong first SOS prefactor rejected',lhs,sc(2,rhs))
    ck.different('no same-party Alice commutation',mul(a0,a1),mul(a1,a0))
    ck.different('no same-party Bob commutation',mul(bob[0],bob[1]),mul(bob[1],bob[0]))
    ck.eq('s-square',s*s,(2-k)/4);ck.eq('k-square',k*k,Cyclo.coerce(2))
    ck.eq('bound identity',m,4*(2+k)*s)
    return {'status':'exact_symbolic_algebra_passed_NOT_LEAN','kernel_checked':False,
      'timestamp_utc':datetime.now(timezone.utc).isoformat(),'checks_passed':len(ck.passed),
      'check_names':ck.passed,'reduced_gap_terms':len(lhs),'augmented_gap_terms':len(alhs),
      'relations':'Alice and Bob each free unitaries; ONLY cross-party commutation; no order-four or dimension restriction',
      'formalization_note':'This tests an exact algebraic SOS, not kernel checking or positive-state interpretation.'}
if __name__=='__main__':
    result=run_first_sos(); out=Path(sys.argv[1])
    out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
