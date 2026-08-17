#!/usr/bin/env python3
from __future__ import annotations
import csv, json, pathlib
import sympy as sp

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "current_profile_exact.json"


def sx(s: str) -> sp.Expr:
    return sp.sympify(s, locals={"sqrt": sp.sqrt})


def fnum(s: str, sig: int = 6) -> str:
    return f"{float(sp.N(sx(s), 18)):.{sig}g}"


def texfrac(s: str) -> str:
    s = str(s)
    if "/" in s and not any(c in s for c in "+-*()A"):
        a, b = s.split("/", 1)
        return rf"\frac{{{a}}}{{{b}}}"
    return s.replace("*", r"\,")


def polyA(coeffs):
    out=[]
    for k,c in enumerate(coeffs):
        if c=='0': continue
        ct=texfrac(c)
        if k==0: out.append(ct)
        elif k==1: out.append(('' if c=='1' else ct)+r'A')
        else: out.append(('' if c=='1' else ct)+rf'A^{{{k}}}')
    return '+'.join(out) or '0'


def cert_table(title, variables, terms, pareto=False):
    cols=''.join('r' for _ in variables)+'l'
    lines=[rf'\subsubsection*{{{title}}}',rf'\begin{{longtable}}{{{cols}}}',
           ' & '.join([rf'$\deg_{{{v}}}$' for v in variables]+['coefficient'])+r'\\',r'\toprule',r'\endfirsthead',
           ' & '.join([rf'$\deg_{{{v}}}$' for v in variables]+['coefficient'])+r'\\',r'\toprule',r'\endhead']
    for t in terms:
        coeff=polyA(t['coefficient_in_A_ascending']) if pareto else texfrac(t['coefficient'])
        lines.append(' & '.join([str(x) for x in t['powers']]+[rf'${coeff}$'])+r'\\')
    lines += [r'\bottomrule',r'\end{longtable}']
    return '\n'.join(lines)


def main():
    payload=json.loads(DATA.read_text())
    rows=payload['rows']
    lines=[r'\begin{tabular}{rrrrrrrrrr}',r'\toprule',
       r'$m$&$n$&$\chi_D^{\rm unit}$&$\chi_D^{\rm scale}$&$\chi_H^{\rm scale}$&product&lower&$\eta_m$&$c_m$&$\sqrt{-\eta_m/c_m}$\\',r'\midrule']
    csvrows=[]
    for z in rows:
        vals=[z['chi_D_unit']['decimal'],z['chi_D_scale']['decimal'],z['chi_H_scale']['decimal'],
              z['product']['decimal'],z['lower']['decimal'],z['eta']['decimal'],z['cubic']['decimal'],z['amplitude_coefficient']['decimal']]
        lines.append(f"{z['m']}&{z['n']}&"+'&'.join(fnum(x,6) for x in vals)+r'\\')
        csvrows.append([z['m'],z['n']]+[float(sp.N(sx(x),18)) for x in vals])
    lines += [r'\bottomrule',r'\end{tabular}']
    (ROOT/'data'/'contrast_table.tex').write_text('\n'.join(lines)+'\n')
    with open(ROOT/'figures'/'contrast_table.csv','w',newline='') as f:
        w=csv.writer(f)
        w.writerow(['m','n','chiD_unit','chiD_scale','chiH_scale','product','minimax_lower','eta','cubic','amplitude_coefficient'])
        w.writerows(csvrows)

    iv=ROOT/'independent_verifier'
    D=json.load(open(iv/'improved_modulus_certificate.json'))
    P=json.load(open(iv/'pareto_all_m_certificate.json'))
    parts=[
      cert_table('35-term homogeneous certificate',D['homogeneous']['variables'],D['homogeneous']['terms']),
      cert_table('77-term improved-profile spatial certificate',D['improved_mode']['variables'],D['improved_mode']['terms']),
      cert_table('34-term equilibrium-scaled homogeneous certificate',P['modulus']['homogeneous']['variables'],P['modulus']['homogeneous']['terms'],True),
      cert_table('84-term equilibrium-scaled spatial certificate',P['modulus']['spatial']['variables'],P['modulus']['spatial']['terms'],True),
    ]
    (ROOT/'data'/'certificate_tables.tex').write_text('\n\n'.join(parts)+'\n')
    print('TABLES_GENERATED_FROM_CURRENT_PROFILE')

if __name__=='__main__':
    main()
