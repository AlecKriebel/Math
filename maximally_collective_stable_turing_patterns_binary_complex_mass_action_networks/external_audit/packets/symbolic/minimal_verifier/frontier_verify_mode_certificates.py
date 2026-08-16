#!/usr/bin/env python3
from __future__ import annotations
import json,argparse
from pathlib import Path
import sympy as sp

def even(expr,y,z):
    out=0
    for (k,),coef in sp.Poly(sp.expand(expr),y).terms():
        assert k%2==0; out+=coef*z**(k//2)
    return sp.expand(out)

def generate():
    x,y,z,s,A=sp.symbols('x y z s A',real=True);lam=x+sp.I*y;B=sp.Rational(1,3)
    P=lam**4+12*lam**3+42*lam**2+47*lam+16;R=5*lam**2+33*lam+16
    Eh=sp.expand((1+A*x+B*z)*even(P*sp.conjugate(P),y,z)-even(R*sp.conjugate(R),y,z))
    q0=sp.Rational(91,90);t=1+s
    g1=lam+2+t*sp.Rational(23,63);gm=lam+5+t*sp.Rational(1,7);gz=lam+4+t*sp.Rational(16,45)
    F=sp.expand(g1*gm*gz-4*g1-4*gm+gz);G=sp.expand(gz*(4*g1+gm)-36)
    Em=sp.expand(q0**2*(1+A*x+B*z)*even(F*sp.conjugate(F),y,z)-even(G*sp.conjugate(G),y,z))
    return Eh,Em,(x,z,s,A)

def verify(path:Path):
    data=json.loads(path.read_text());Eh,Em,(x,z,s,A)=generate()
    for sec,expr,vars in [('homogeneous',Eh,[x,z]),('spatial',Em,[x,z,s])]:
        supplied=data['modulus'][sec]
        assert supplied['term_count']==len(sp.Poly(expr,*vars).terms())
        table={tuple(t['powers']):[sp.Rational(v) for v in t['coefficient_in_A_ascending']] for t in supplied['terms']}
        for mon,c in sp.Poly(expr,*vars).terms():
            p=sp.Poly(c,A); coeff=list(reversed(p.all_coeffs()))
            assert table[mon]==coeff
            assert all(v>=0 for v in coeff) and any(v>0 for v in coeff)
    assert data['modulus']['homogeneous']['term_count']==34
    assert data['modulus']['spatial']['term_count']==84

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('certificate',nargs='?',default=str(Path(__file__).resolve().parent/'pareto_all_m_certificate.json'));a=p.parse_args()
    verify(Path(a.certificate));print('VERIFY_MODE_CERTIFICATES_PASS')
