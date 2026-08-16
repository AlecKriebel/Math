#!/usr/bin/env python3
from __future__ import annotations
import json, sys, importlib.util, pathlib
from fractions import Fraction
from math import sqrt
import sympy as sp
ROOT=pathlib.Path(__file__).resolve().parents[1]
LOCAL=ROOT/'independent_verifier'

def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path); mod=importlib.util.module_from_spec(spec); sys.modules[name]=mod; spec.loader.exec_module(mod); return mod
cd=load('flagship_stable_core',LOCAL/'stable_core.py')

def texfrac(s):
    s=str(s)
    if '/' in s and not any(c in s for c in '+-*()A'):
        a,b=s.split('/',1); return rf'\frac{{{a}}}{{{b}}}'
    return s.replace('*',r'\,')

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

# finite table
rows=[]
for m in range(3,11):
    H=cd.Hsum(m)
    eta=sp.N(cd.ell_Dr_formula(m,H)/cd.ell_r_formula(m,H),9)
    cub=sp.N(cd.cubic_num_formula(m,H)/cd.ell_r_formula(m,H),9)
    amp=sp.N(sp.sqrt(-(cd.ell_Dr_formula(m,H)/cd.ell_r_formula(m,H))/(cd.cubic_num_formula(m,H)/cd.ell_r_formula(m,H))),9)
    r=m-2
    unit=sp.Rational(23,63)*(91*m-183)
    bd=sp.Rational(2093,63)/sp.sqrt(3)*sp.sqrt(r)
    bh=sp.sqrt(3*r)*sp.Rational(91*r-1,91*r)
    prod=sp.Rational(23,63)*(91*r-1)
    lb=sp.sqrt(8*r)
    rows.append((m,m+1,float(unit),float(bd),float(bh),float(prod),float(lb),float(eta),float(cub),float(amp)))
lines=[r'\begin{tabular}{rrrrrrrrrr}',r'\toprule',
       r'$m$&$n$&$\chi_D^{\rm unit}$&$\chi_D^{\rm bal}$&$\chi_H^{\rm bal}$&product&lower&$\eta_m$&$c_m$&$\sqrt{-\eta_m/c_m}$\\',r'\midrule']
for row in rows:
    m,n,*vals=row
    lines.append(f'{m}&{n}&'+ '&'.join(f'{v:.4g}' for v in vals)+r'\\')
lines += [r'\bottomrule',r'\end{tabular}']
(ROOT/'data/contrast_table.tex').write_text('\n'.join(lines)+'\n')
# csv
import csv
with open(ROOT/'figures/contrast_table.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['m','n','chiD_unit','chiD_balanced','chiH_balanced','product','minimax_lower','eta','cubic','amplitude_coefficient']); w.writerows(rows)

# certificate tables
D=json.load(open(LOCAL/'improved_modulus_certificate.json'))
P=json.load(open(LOCAL/'pareto_all_m_certificate.json'))
parts=[
 cert_table('35-term homogeneous certificate',D['homogeneous']['variables'],D['homogeneous']['terms']),
 cert_table('77-term improved-profile spatial certificate',D['improved_mode']['variables'],D['improved_mode']['terms']),
 cert_table('34-term Pareto homogeneous certificate',P['modulus']['homogeneous']['variables'],P['modulus']['homogeneous']['terms'],True),
 cert_table('84-term Pareto spatial certificate',P['modulus']['spatial']['variables'],P['modulus']['spatial']['terms'],True),
]
(ROOT/'data/certificate_tables.tex').write_text('\n\n'.join(parts)+'\n')
print('TABLES_GENERATED')
