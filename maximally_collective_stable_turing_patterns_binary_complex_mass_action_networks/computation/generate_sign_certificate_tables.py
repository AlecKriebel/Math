#!/usr/bin/env python3
"""Print human-inspectable shifted coefficient lists for load-bearing signs."""
from __future__ import annotations
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
m,u,r=sp.symbols('m u r', integer=True)

def coeffs(expr,var,shift):
    z=sp.symbols('z')
    P=sp.Poly(sp.expand(expr.subs(var,z+shift)),z)
    return [sp.factor(c) for c in P.all_coeffs()]

def tex_list(name,statement,vals):
    lines=[rf'\paragraph{{{name}.}} {statement}',r'\[',r'\begin{gathered}']
    chunk=[]
    for i,c in enumerate(vals):
        chunk.append(str(c))
        if len(chunk)==3 or i==len(vals)-1:
            lines.append(r',\quad '.join(chunk)+(r',' if i<len(vals)-1 else '')+r'\\')
            chunk=[]
    lines += [r'\end{gathered}',r'\]']
    return '\n'.join(lines)

Q3=589180301*m**3-3500015940*m**2+6930529579*m-4574434500
unit_aux=633906000*m**2-2491895430*m+2448652733
unit_cubic=(2729945147827667886720*m**5-27755132420474170999952*m**4+
112813395868533457497683*m**3-229153280695458887386228*m**2+
232620996871721820873517*m-94412163900120968220300)
Pc=(652054120726848*m**4-5151971981328467*m**3+
15265080924982572*m**2-20102347725659113*m+9927281930180400)
# N0-1/100 lower bound from frontier verifier, written in r=m-2 and shifted r=z+1.
q=589180301*(r+2)**3-3500015940*(r+2)**2+6930529579*(r+2)-4574434500
R=(68605040480814208768*(r+2)**4-550882186169626030957*(r+2)**3+
1658612632937449670852*(r+2)**2-2219226476204103501323*(r+2)+1113379274975809565700)/(sp.Integer(286118780220)*(8*(r+2)-17)*q)
C=-sp.Integer(215)*(652054120726848*(r+2)**4-5151971981328467*(r+2)**3+
15265080924982572*(r+2)**2-20102347725659113*(r+2)+9927281930180400)/(sp.Integer(11645046)*(8*(r+2)-17)*q)
Hup=r/(90*r+1)
numN0=sp.factor(sp.fraction(sp.factor(R+C*Hup-sp.Rational(1,100)))[0])
Pupper=sp.expand((-1040195520+sp.Rational(5,4)*756272790)*r**3-507201030*r**2-935658*r+58481)

parts=[
 tex_list('Unit-profile boundary denominator',
          'After $m=z+3$, the coefficients of the cubic denominator are',coeffs(Q3,m,3)),
 tex_list('Unit-profile critical-denominator bound',
          'After $m=z+3$, the auxiliary quadratic has coefficients',coeffs(unit_aux,m,3)),
 tex_list('Unit-profile cubic numerator lower bound',
          'After $m=z+3$, the decisive degree-five polynomial has coefficients',coeffs(unit_cubic,m,3)),
 tex_list('Equilibrium-scaled coefficient sign',
          'After $m=z+3$, the polynomial whose sign gives $S_m<0$ has coefficients',coeffs(Pc,m,3)),
 tex_list('Reference cubic margin',
          r'After $\nu=z+1$, the numerator proving $N_m^{\mathrm{ref}}>1/100$ has coefficients',coeffs(numN0,r,1)),
 tex_list('Gauge upper-bound tail',
          r'For $\nu\ge2$, the polynomial upper bound used in $\tau_m(L)<1/20$ has coefficients',sp.Poly(Pupper,r).all_coeffs()),
 r'''\paragraph{Remaining scalar comparisons.}
The certificate also checks exactly
\[
 \frac{1760850}{91}-10253>0,
 \qquad
 \frac4{462105}\left(\frac{1760850}{90}-10253\right)<\frac1{10},
\]
which give $-1/10<S_m<0$, and combines
$N_m^{\rm ref}>1/100$, $S_m>-1/10$, and
$\tau_m(L)<1/20$ to obtain $N_m(L)>1/200$.'''
]
(ROOT/'data'/'sign_certificate_tables.tex').write_text('\n\n'.join(parts)+'\n')
print('SIGN_CERTIFICATE_TABLES_GENERATED')
