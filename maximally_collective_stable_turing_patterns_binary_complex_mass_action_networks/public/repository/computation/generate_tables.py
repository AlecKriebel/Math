#!/usr/bin/env python3
from __future__ import annotations
import argparse, csv, json, pathlib
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
        return rf"{a}/{b}"
    return s.replace("*", r"\,")


def polynomial(coeffs, variable):
    out=[]
    for k,c in enumerate(coeffs):
        if c=='0': continue
        ct=texfrac(c)
        if k==0: out.append(ct)
        elif k==1: out.append(('' if c=='1' else ct)+variable)
        else: out.append(('' if c=='1' else ct)+rf'{variable}^{{{k}}}')
    return '+'.join(out) or '0'


def cert_table(title, variables, terms, declared_count, pareto=False):
    powers=[tuple(term['powers']) for term in terms]
    if len(terms)!=declared_count:
        raise ValueError(f'{title}: declared {declared_count} terms but found {len(terms)} rows')
    if any(len(monomial)!=len(variables) for monomial in powers):
        raise ValueError(f'{title}: a monomial has the wrong number of exponents')
    if len(set(powers))!=len(powers):
        raise ValueError(f'{title}: duplicate monomial row')
    cols=''.join('r' for _ in variables)+'l'
    lines=[rf'\subsubsection*{{{title}}}',rf'\begin{{longtable}}{{{cols}}}',
           ' & '.join([rf'$\deg_{{{v}}}$' for v in variables]+['coefficient'])+r'\\',r'\toprule',r'\endfirsthead',
           ' & '.join([rf'$\deg_{{{v}}}$' for v in variables]+['coefficient'])+r'\\',r'\toprule',r'\endhead']
    for t in terms:
        if pareto:
            key='coefficient_in_U_ascending' if 'coefficient_in_U_ascending' in t else 'coefficient_in_A_ascending'
            coeff=polynomial(t[key], 'U' if key.endswith('_U_ascending') else 'A')
        else:
            coeff=texfrac(t['coefficient'])
        lines.append(' & '.join([str(x) for x in t['powers']]+[rf'${coeff}$'])+r'\\')
    lines += [r'\bottomrule',r'\end{longtable}']
    return '\n'.join(lines)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        '--check-certificate-table',type=pathlib.Path,
        help='fail unless the specified modulus-certificate TeX matches exact generation',
    )
    args=parser.parse_args()
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
    iv=ROOT/'independent_verifier'
    D=json.load(open(iv/'improved_modulus_certificate.json'))
    P=json.load(open(iv/'pareto_all_m_certificate.json'))
    parts=[
      cert_table('35-term homogeneous certificate',D['homogeneous']['variables'],D['homogeneous']['terms'],D['homogeneous']['term_count']),
      cert_table('77-term improved-profile spatial certificate',D['improved_mode']['variables'],D['improved_mode']['terms'],D['improved_mode']['term_count']),
      cert_table(r'22-term equilibrium-scaled homogeneous certificate ($U=A-1/4$)',P['modulus']['homogeneous']['variables'],P['modulus']['homogeneous']['terms'],P['modulus']['homogeneous']['term_count'],True),
      cert_table('84-term equilibrium-scaled spatial certificate',P['modulus']['spatial']['variables'],P['modulus']['spatial']['terms'],P['modulus']['spatial']['term_count'],True),
    ]
    certificate_text='\n\n'.join(parts)+'\n'
    if args.check_certificate_table is not None:
        candidate=args.check_certificate_table
        if not candidate.is_file() or candidate.read_text()!=certificate_text:
            raise SystemExit(f'STALE_GENERATED_MODULUS_TABLE: {candidate}')
        print('MODULUS_CERTIFICATE_TABLE_FRESH')
        return
    (ROOT/'data'/'contrast_table.tex').write_text('\n'.join(lines)+'\n')
    with open(ROOT/'figures'/'contrast_table.csv','w',newline='') as f:
        w=csv.writer(f, lineterminator='\n')
        w.writerow(['m','n','chiD_unit','chiD_scale','chiH_scale','product','minimax_lower','eta','cubic','amplitude_coefficient'])
        w.writerows(csvrows)
    (ROOT/'data'/'certificate_tables.tex').write_text(certificate_text)
    print('TABLES_GENERATED_FROM_CURRENT_PROFILE')

if __name__=='__main__':
    main()
