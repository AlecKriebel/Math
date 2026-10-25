#!/usr/bin/env python3
"""Print human-inspectable scalar certificates with explicit sign conventions."""
from __future__ import annotations
import argparse
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parents[1]
m,u,nu,v=sp.symbols('m u nu v', integer=True)

def coeffs(expr,var,shift_var,shift):
    P=sp.Poly(sp.expand(expr.subs(var,shift_var+shift)),shift_var)
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
Lm=(2729945147827667886720*m**5-27755132420474170999952*m**4+
112813395868533457497683*m**3-229153280695458887386228*m**2+
232620996871721820873517*m-94412163900120968220300)
Pr=(68605040480814208768*m**4-550882186169626030957*m**3+
1658612632937449670852*m**2-2219226476204103501323*m+
1113379274975809565700)
Pc=(652054120726848*m**4-5151971981328467*m**3+
15265080924982572*m**2-20102347725659113*m+9927281930180400)
# The exact lower comparison for N_m^ref-1/100, written in nu=m-2 and
# subsequently shifted by nu=v+1.
Pref=(3790502986637265684840*nu**5-974216530468600286489*nu**4-
53103567440921218871*nu**3-576386186827093561*nu**2+
3649732858601219*nu+55281268032918)
Pupper=(-sp.Rational(189709065,2)*nu**3-507201030*nu**2-
935658*nu+58481)

parts=[
 tex_list('Unit-profile boundary denominator',
          r'''The polynomial being certified is
\[
 \mathcal Q_m=589180301m^3-3500015940m^2
 +6930529579m-4574434500.
\]
After $m=u+3$, the following coefficients are listed in descending powers
of $u$:''',coeffs(Q3,m,u,3))+
 r'''\noindent Every coefficient is positive, so $\mathcal Q_m>0$ for
$m\ge3$.  There is no external sign prefactor.''',
 tex_list('Unit-profile critical-denominator bound',
          r'''The auxiliary polynomial is
\[
 633906000m^2-2491895430m+2448652733.
\]
After $m=u+3$, the following coefficients are listed in descending powers
of $u$:''',coeffs(unit_aux,m,u,3))+
 r'''\noindent Every coefficient is positive, so the polynomial is positive
for $m\ge3$.  There is no external sign prefactor.''',
 tex_list('Unit-profile cubic numerator lower bound',
          r'''The polynomial being certified is
\[
\begin{split}
 L_m={}&2729945147827667886720m^5
 -27755132420474170999952m^4\\
 &+112813395868533457497683m^3
 -229153280695458887386228m^2\\
 &+232620996871721820873517m
 -94412163900120968220300.
\end{split}
\]
This is the exact clearing polynomial defined in \eqref{eq:Lmpoly}.
Its rational identity is
\[
 R_m+C_m\frac{m-2}{90m-179}
 =\frac{L_m}{286118780220(8m-17)(90m-179)\mathcal Q_m}.
\]
After $m=u+3$, the following coefficients are listed in descending powers
of $u$:''',coeffs(Lm,m,u,3))+
 r'''\noindent Every coefficient is positive, so $L_m>0$ for $m\ge3$.
It enters the clearing identity with a positive denominator and no external
negative prefactor.''',
 tex_list('Reference coefficient $R_m$',
          r'''Define
\ifsiadsreview
\[
\begin{split}
 P_R(m)={}&68605040480814208768m^4
 -550882186169626030957m^3\\
 &+1658612632937449670852m^2
 -2219226476204103501323m\\
 &+1113379274975809565700.
\end{split}
\]
\[
 R_m=\frac{P_R(m)}{286118780220(8m-17)\mathcal Q_m}.
\]
\else
\[
\begin{split}
 P_R(m)={}&68605040480814208768m^4
 -550882186169626030957m^3\\
 &+1658612632937449670852m^2
 -2219226476204103501323m\\
 &+1113379274975809565700,
\end{split}
\qquad
 R_m=\frac{P_R(m)}{286118780220(8m-17)\mathcal Q_m}.
\]
\fi
After $m=u+3$, the following coefficients of $P_R$ are listed in descending
powers of $u$:''',coeffs(Pr,m,u,3))+
 r'''\noindent Every coefficient is positive.  The denominator is positive
for $m\ge3$, and there is no external negative prefactor; hence $R_m>0$.''',
 tex_list('Unit-profile coefficient $C_m$',
          r'''Define
\[
\begin{split}
 P_C(m)={}&652054120726848m^4-5151971981328467m^3\\
 &+15265080924982572m^2-20102347725659113m
 +9927281930180400,
\end{split}
\]
\[
 C_m=-\frac{215P_C(m)}{11645046(8m-17)\mathcal Q_m}.
\]
After $m=u+3$, the following coefficients of $P_C$ are listed in descending
powers of $u$:''',coeffs(Pc,m,u,3))+
 r'''\noindent Every coefficient is positive.  Since the denominator is
positive and the external prefactor is $-215$, this proves $C_m<0$.''',
 tex_list('Reference cubic margin',
          r'''Let $\nu=m-2$ and define
\[
\begin{split}
 P_{\rm ref}(\nu)={}&3790502986637265684840\nu^5
 -974216530468600286489\nu^4\\
 &-53103567440921218871\nu^3
 -576386186827093561\nu^2\\
 &+3649732858601219\nu+55281268032918,
\end{split}
\]
\[
 D_{\rm ref}(\nu)=715296950550(8\nu-1)(90\nu+1)
 (589180301\nu^3+35065866\nu^2+629431\nu+3306).
\]
The exact comparison is
\[
 N_m^{\rm ref}-\frac1{100}\ge
 \frac{P_{\rm ref}(\nu)}{D_{\rm ref}(\nu)}.
\]
After $\nu=v+1$, the following coefficients of $P_{\rm ref}$ are listed in
descending powers of $v$:''',coeffs(Pref,nu,v,1))+
 r'''\noindent Every coefficient is positive, and $D_{\rm ref}(\nu)>0$ for
$\nu\ge1$.  There is no external sign prefactor.  Hence
$N_m^{\rm ref}>1/100$.''',
 tex_list('Gauge upper-bound tail',
          r'''Let $\nu=m-2$.  The exact rational expression being bounded is
\[
 \tau_m(L)=-\frac{A_\tau}{15876(8\nu-1)B_\tau},
\]
where
\[
\begin{split}
 A_\tau={}&1494249120\mathfrak h_mL\nu^2
 -69786990\mathfrak h_mL\nu+108738630L\nu^2\\
 &+1214388L\nu-8521L-125249670\nu^2+1031940\nu,
\end{split}
\]
\[
 B_\tau=32760\mathfrak h_mL\nu+32760L\nu^2+4L-4095\nu.
\]
The signed upper-bound polynomial is
\[
 P_{\rm up}(\nu)=-\frac{189709065}{2}\nu^3-507201030\nu^2
 -935658\nu+58481.
\]
The following coefficients are listed in descending powers of $\nu$:''',
          sp.Poly(Pupper,nu).all_coeffs())+
 r'''\noindent This is a signed coefficient list, not a coefficientwise
positivity certificate.  Direct differentiation gives
\[
 P_{\rm up}'(\nu)=-\frac{569127195}{2}\nu^2
 -1014402060\nu-935658<0\qquad(\nu\ge0),
\]
and $P_{\rm up}(2)=-2789453215<0$.  Thus $P_{\rm up}(\nu)<0$ for
$\nu\ge2$.  There is no external negative prefactor reversing this
conclusion.''',
 r'''\paragraph{The signed scalar $S_m$.}
This sign is certified separately from $P_C$.  With
\[
 S_m=-\frac{4(1760850\mathfrak h_m-10253)}{462105},
\qquad \frac1{91}\le\mathfrak h_m<\frac1{90},
\]
the exact comparisons
\[
 \frac{1760850}{91}-10253>0,
 \qquad
 \frac4{462105}\left(\frac{1760850}{90}-10253\right)<\frac1{10},
\]
give $-1/10<S_m<0$.  The displayed expression itself carries the external
negative prefactor $-4$, which reverses the positive bracket and proves the
upper sign.  Combining $N_m^{\rm ref}>1/100$, $S_m>-1/10$, and
$\tau_m(L)<1/20$ gives $N_m(L)>1/200$.'''
]
sign_table_text='\n\n'.join(parts)+'\n'

# Regenerate the printed boundary-triad Routh--Hurwitz gap from the defining
# coefficients.  Keeping this display generated prevents transcription drift.
a,b,h1,hm,hz=sp.symbols('a b h_1 h_m h_Z', positive=True)
c1=a*h1+4*a*hm+b*h1+b*hm+4*b*hz
c2=a*(4*a*h1*hm+7*b*h1*hm+4*b*h1*hz+16*b*hm*hz)
c3=16*a*a*b*h1*hm*hz
gap=sp.Poly(sp.expand((c1*c2-c3)/a),a,b,h1,hm,hz)
gap_terms=[]
for monomial,coefficient in gap.terms():
    assert coefficient>0
    term=coefficient
    for variable,power in zip((a,b,h1,hm,hz),monomial):
        term*=variable**power
    gap_terms.append(sp.latex(term))
assert len(gap_terms)==14
rows=['+'.join(gap_terms[i:i+4]) for i in range(0,len(gap_terms),4)]
triad=[r'\begin{align*}',r'c_1c_2-c_3={}&a\bigl('+rows[0]+r'\\']
triad.extend(r'&+'+row+(r'\\' if i<len(rows)-1 else r'\bigr).')
             for i,row in enumerate(rows[1:],start=1))
triad.append(r'\end{align*}')
triad_text='\n'.join(triad)+'\n'


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--check',action='store_true',
        help='fail unless both generated TeX files already match exactly',
    )
    parser.add_argument(
        '--check-sign-table',type=Path,
        help='fail unless the specified sign-table TeX matches exact generation',
    )
    parser.add_argument(
        '--check-triad-table',type=Path,
        help='fail unless the specified boundary-triad TeX matches exact generation',
    )
    args=parser.parse_args()
    outputs={
        ROOT/'data'/'sign_certificate_tables.tex':sign_table_text,
        ROOT/'data'/'triad_routh_gap.tex':triad_text,
    }
    if args.check_sign_table is not None:
        candidate=args.check_sign_table
        if not candidate.is_file() or candidate.read_text()!=sign_table_text:
            raise SystemExit(f'STALE_GENERATED_SIGN_TABLE: {candidate}')
        print('SIGN_CERTIFICATE_TABLE_FRESH')
        return
    if args.check_triad_table is not None:
        candidate=args.check_triad_table
        if not candidate.is_file() or candidate.read_text()!=triad_text:
            raise SystemExit(f'STALE_GENERATED_TRIAD_TABLE: {candidate}')
        print('TRIAD_ROUTH_TABLE_FRESH')
        return
    if args.check:
        stale=[str(path.relative_to(ROOT)) for path,text in outputs.items()
               if not path.is_file() or path.read_text()!=text]
        if stale:
            raise SystemExit('STALE_GENERATED_CERTIFICATE_TABLES: '+', '.join(stale))
        print('SIGN_CERTIFICATE_TABLES_FRESH')
        return
    for path,text in outputs.items():
        path.write_text(text)
    print('SIGN_CERTIFICATE_TABLES_GENERATED')


if __name__=='__main__':
    main()
