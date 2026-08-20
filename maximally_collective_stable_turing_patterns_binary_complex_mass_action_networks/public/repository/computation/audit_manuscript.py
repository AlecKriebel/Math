#!/usr/bin/env python3
"""Literal source audit for labels, citations, theorem types, provenance, and scope."""
from __future__ import annotations
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
files=[ROOT/'manuscript'/'main.tex',ROOT/'manuscript'/'supplement.tex',
       ROOT/'external_audit'/'theorem_summary.tex',ROOT/'external_audit'/'proof_skeleton.tex']
texts={str(p.relative_to(ROOT)):p.read_text() for p in files}
alltext='\n'.join(texts.values())
clean='\n'.join(line.split('%',1)[0] for line in alltext.splitlines())
main=texts['manuscript/main.tex']; supp=texts['manuscript/supplement.tex']

labels=set(re.findall(r'\\label\{([^}]+)\}',clean))
refs=[]
for group in re.findall(r'\\(?:c|C)?ref\{([^}]+)\}',clean): refs += [x.strip() for x in group.split(',')]
missing=sorted(set(refs)-labels)
if missing: raise AssertionError(f'missing labels {missing}')
dups=sorted({x for x in labels if len(re.findall(r'\\label\{'+re.escape(x)+r'\}',clean))>1})
if dups: raise AssertionError(f'duplicate labels {dups}')

cites=[]
for group in re.findall(r'\\cite\{([^}]+)\}',clean): cites += [x.strip() for x in group.split(',')]
bib=(ROOT/'manuscript'/'references.bib').read_text()
bibkeys=set(re.findall(r'@\w+\{([^,]+),',bib))
missing_cites=sorted(set(cites)-bibkeys)
if missing_cites: raise AssertionError(f'missing bib keys {missing_cites}')

# Semantic environment-type audit for explicit numbered references.
envs={}
for typ in ('theorem','proposition','lemma','corollary','remark','definition'):
    for body in re.findall(r'\\begin\{'+typ+r'\}(.*?)\\end\{'+typ+r'\}',clean,re.S):
        prefix={'theorem':'thm','proposition':'prop','lemma':'lem',
                'corollary':'cor','remark':'rem','definition':'def'}[typ]+':'
        for lab in re.findall(r'\\label\{([^}]+)\}',body):
            if lab.startswith(prefix): envs[lab]=typ
# The theorem-like environments share a counter.  Without alias counters,
# cleveref can silently print the wrong environment type, so require an
# explicit semantic noun for every theorem-like reference.
for group in re.findall(r'\\(?:c|C)ref\{([^}]+)\}',clean):
    named=[x.strip() for x in group.split(',') if x.strip() in envs]
    if named:
        raise AssertionError(f'theorem-like cleveref reference remains: {named}')
# Reject brittle literal number references as well.
if re.search(r'\b(?:Theorem|Proposition|Lemma|Corollary|Remark)\s+\d+\.\d+',clean):
    raise AssertionError('literal numbered environment reference remains')

required_title='Exact Diffusion Design for Maximally Collective Stable Turing Patterns'
for name,text in texts.items():
    if required_title not in text:
        raise AssertionError(f'final title missing from {name}')

forbidden=[r'\bT-ALG\b',r'\bPhase\s+[IVX]+\b',r'reaction-minimal',r'minimum reaction count',
           r'bounded.catalog',r'square-root-balanced',r'right panel',r'one-bad-minor diffusion theorem',
           r'one-bad-minor matrix theorem',r'universal trade-off',
           r'universal minimax lower bound',r'universal necessary bounds?',
           r'universal cost',r'globally optimal',r'biological cost',
           r'price paid in concentrations',r'All listed coefficients are nonnegative',
           r'polynomial whose sign gives\s*\$?S_m\$?\s*<\s*0',
           r'q_m\s*\(L\)\s*=',r'\\mathcal\s*H_m',r'\\nu\s*=\s*z\s*\+\s*1',
           r'conservation-compatible Lyapunov--Schmidt reduction',
           r'Lyapunov--Schmidt coefficients']
for pat in forbidden:
    if re.search(pat,clean,re.I): raise AssertionError(f'obsolete wording: {pat}')

# A robustness statement may not vary kinetic and equilibrium data as though
# they were independent coordinates while preserving the same equilibrium.
for match in re.finditer(r'rates,\s*equilibrium coordinates',clean,re.I):
    context=clean[max(0,match.start()-240):match.end()+240]
    if not re.search(r'(?:positive-equilibrium|equilibrium[- ]realization)\s+manifold',context,re.I):
        raise AssertionError('unqualified rate/equilibrium perturbation remains')

flat=' '.join(clean.split())
required_patterns=[
 r'every\s+principal\s+(?:Jacobian\s+)?(?:subsystem|block).*?below\s+order\s+\$n-1\$.*?Hurwitz',
 r'locally\s+exponentially\s+asymptotically\s+stable',
 r'binary-complex',r'synthetic',r'fixed-mass',r'principal-minor diffusion ray',
 r'complete region.*?not classified here',r'wave instability',r'b=2a',r'N_m\(L\)>1/200']
for pat in required_patterns:
    if not re.search(pat,flat,re.I): raise AssertionError(f'missing scope pattern {pat}')

abstract=main.split('\\begin{abstract}',1)[1].split('\\end{abstract}',1)[0]
if '\\cite' in abstract or '\\ref' in abstract: raise AssertionError('abstract contains citation/reference')
plain=re.sub(r'\\[a-zA-Z]+(?:\[[^]]*\])?(?:\{[^{}]*\})?',' ',abstract)
plain=re.sub(r'[$\\{}^_~]',' ',plain)
words=re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*",plain)
if not 150 <= len(words) <= 250: raise AssertionError(f'abstract words {len(words)}')

for exact in ['2\\le i\\le m-2','3\\le i\\le m-1','n=m+1','m=n-1']:
    if exact not in clean: raise AssertionError(f'missing convention {exact}')

for entry in re.split(r'(?=@\w+\{)',bib):
    if not entry.strip(): continue
    key=re.search(r'@\w+\{([^,]+),',entry).group(1)
    if key!='ConradiMinchevaUecker2026' and not re.search(r'doi\s*=\s*\{[^}]+\}',entry,re.I):
        raise AssertionError(f'no DOI for {key}')

# Numerical provenance: stale values/profiles must not appear in claim-facing source.
claim_files=[ROOT/'manuscript'/'main.tex',ROOT/'manuscript'/'supplement.tex',ROOT/'external_audit'/'theorem_summary.tex',ROOT/'external_audit'/'proof_skeleton.tex',ROOT/'data'/'contrast_table.tex']
claim_text='\n'.join(p.read_text() for p in claim_files)
for stale in ('0.1054','1.311','57/56','1589m','227m-451'):
    if stale in claim_text: raise AssertionError(f'stale numerical artifact {stale}')
if '143636/7451873' not in (ROOT/'data'/'current_profile_exact.json').read_text():
    raise AssertionError('mandatory m=3 eta regression missing')

for marker in ('22 nonzero monomials',r'\nu L^2\ge5/4',
               r'q_3=(\lambda+7)(\lambda^2+5\lambda+2)'):
    if marker not in clean:
        raise AssertionError(f'missing repaired-proof marker {marker}')
triad=(ROOT/'data'/'triad_routh_gap.tex').read_text()
if '16 b^{2} h_{1} h_{Z}^{2}' not in triad:
    raise AssertionError('generated triad Routh gap is missing the h_1 h_Z^2 term')

# Proof-exposition audit.  Exact algebra is independently reconstructed by
# frontier_verify_exposition_identities.py; these markers ensure that the
# corresponding rational bridges, rather than detached coefficient lists,
# are actually visible in the source manuscript.
supp_flat=' '.join(line.split('%',1)[0].strip() for line in supp.splitlines())
main_flat=' '.join(line.split('%',1)[0].strip() for line in main.splitlines())
required_supplement_markers=(
    r'\subsection{Coefficientwise-nonnegative modulus certificates}',
    r'\subsection{Signed scalar and rational-function certificates}',
    r'P_R(m)',r'P_C(m)',r'R_m=\frac{P_R(m)}',r'C_m=-\frac{215P_C(m)}',
    '286118780220', '11645046', '90m-179',
    r'R_m+C_m\mathfrak h_m',r'P_{\rm ref}(\nu)',r'D_{\rm ref}(\nu)',
    '715296950550',r'N_m^{\rm ref}-\frac1{100}',
    r'S_m=-\frac{4(1760850\mathfrak h_m-10253)}{462105}',
    r'\tau_m(L)=-\frac{A_\tau}{15876(8\nu-1)B_\tau}',
    r'P_{\rm up}(\nu)',r'P_{\rm up}(2)=-2789453215',
    r'E_{77}(x,z,s)',r'E_{84}(x,z,s;A)',r'E_{22}(x,z;U)',r'E_{35}(x,z)',
    '77 displayed coefficients', '84 coefficients', '22 coefficient',
    '35 coefficients',
)
for marker in required_supplement_markers:
    if marker not in supp_flat:
        raise AssertionError(f'missing printed certificate marker {marker}')

for coefficient in (
    '68605040480814208768','1113379274975809565700',
    '652054120726848','9927281930180400',
    '2729945147827667886720','94412163900120968220300',
    '3790502986637265684840','55281268032918',
    '569127195','1014402060','935658',
):
    if coefficient not in supp_flat:
        raise AssertionError(f'missing exact certificate coefficient {coefficient}')

if not re.search(
    r'\\chi_D\(L\)\\chi_H\(L\)\s*=\s*\\chi_D\^\{\\rm unit\}\(m\)',
    main_flat,
):
    raise AssertionError('fixed contrast-product identity is not printed')
if 'measures equilibrium concentration-scale separation' not in main_flat:
    raise AssertionError('chi_H scale-separation qualification is missing')
if main.count(r'0<|I|<m') < 3:
    raise AssertionError('nonempty principal-set domain is not explicit throughout Section 3')
if 'selected positive realization' not in main_flat:
    raise AssertionError('Corollary 3.3 does not scope stable patterns to a selected realization')
if 'one-dimensional center-manifold normal form is' not in main_flat:
    raise AssertionError('dynamical amplitude equation is not identified as a center-manifold normal form')
if r'(0,\mathcal L)' not in main or r'q_k^2=(k\pi/\mathcal L)^2' not in main:
    raise AssertionError('physical interval length is not consistently written as mathcal L')
profiles_figure = re.search(
    r'\\begin\{figure\}\[H\].*?\\label\{fig:profiles\}.*?\\end\{figure\}',
    main,
    re.S,
)
if profiles_figure is None:
    raise AssertionError('Figure 3 lacks hard placement after the numerical-method paragraph')
if not re.search(
    r'perturb positive steady fluxes and equilibrium coordinates.*?positive-equilibrium realization manifold',
    supp_flat,
    re.I,
):
    raise AssertionError('robustness perturbations are not restricted to the realization manifold')

print('MANUSCRIPT_AUDIT_PASS')
print('labels',len(labels),'references',len(refs),'bibkeys',len(bibkeys),'citations',len(cites),'abstract_words',len(words))
