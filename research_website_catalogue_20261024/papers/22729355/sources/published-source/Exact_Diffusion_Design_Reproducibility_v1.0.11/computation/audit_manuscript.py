#!/usr/bin/env python3
"""Literal source audit for labels, citations, theorem types, provenance, and scope."""
from __future__ import annotations
import csv
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
files=[ROOT/'manuscript'/'main.tex',ROOT/'manuscript'/'supplement.tex',
       ROOT/'external_audit'/'theorem_summary.tex',ROOT/'external_audit'/'proof_skeleton.tex']
texts={str(p.relative_to(ROOT)):p.read_text() for p in files}
alltext='\n'.join(texts.values())
clean='\n'.join(line.split('%',1)[0] for line in alltext.splitlines())
main=texts['manuscript/main.tex']; supp=texts['manuscript/supplement.tex']
summary=texts['external_audit/theorem_summary.tex']
skeleton=texts['external_audit/proof_skeleton.tex']

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
cff=(ROOT/'CITATION.cff').read_text()
bibkeys=set(re.findall(r'@\w+\{([^,]+),',bib))
missing_cites=sorted(set(cites)-bibkeys)
if missing_cites: raise AssertionError(f'missing bib keys {missing_cites}')

for marker in (
    'version: "1.0.11"',
    'date-released: "2026-09-06"',
    'maximally-collective-stable-turing-v1.0.11',
    '10.5281/zenodo.21753404',
    '10.5281/zenodo.22559244',
    'authors:',
):
    if marker not in cff:
        raise AssertionError(f'CITATION.cff lacks release marker {marker}')
if not all(marker in main for marker in (
    'version 1.0.11 tagged release source tree',
    '10.5281/zenodo.21753404',
    '10.5281/zenodo.22559244',
)):
    raise AssertionError('data statement does not distinguish the current tag, concept DOI, and preceding version DOI')

for marker in (
    r'\textbf{Keywords:}',
    r'\textbf{2020 Mathematics Subject Classification:}',
    r'\IfFileExists{journal_review_mode.tex}',
    r'\usepackage[mathlines]{lineno}',
):
    if marker not in main:
        raise AssertionError(f'main source lacks submission marker {marker}')
if 'The author assumes responsibility for all content.' not in ' '.join(main.split()):
    raise AssertionError('main source lacks the required author-responsibility sentence')

# The standalone theorem exports are independently distributed proof objects.
# Their generic diffusion-ray statements must carry the diagonal-diffusion and
# singular-Jacobian hypotheses used by the determinant expansion.
summary_diffusion=summary.split(
    r'\paragraph{Principal-minor diffusion-ray theorem.}',1
)[1].split(r'\paragraph{Exact network diffusion law',1)[0]
skeleton_diffusion=skeleton.split(
    r'\section*{2. Principal-minor diffusion-ray theorem and exact network law}',1
)[1].split(r'For $A_m(a,b)H$',1)[0]
for name,section in (
    ('theorem summary',summary_diffusion),
    ('proof skeleton',skeleton_diffusion),
):
    if r'D=\diag(d_1,\ldots,d_n)' not in section or r'd_j>0' not in section:
        raise AssertionError(f'{name} omits positive diagonal diffusion')
    if r'D\succ0' in section:
        raise AssertionError(f'{name} retains an overbroad generic D hypothesis')
if r'\det J=0' not in skeleton_diffusion:
    raise AssertionError('proof skeleton factors out s without assuming det J=0')

# The ordered variable declarations are part of the exact polynomial identity,
# not descriptive metadata.
unit_certificate=json.loads(
    (ROOT/'independent_verifier'/'improved_modulus_certificate.json').read_text()
)
pareto_certificate=json.loads(
    (ROOT/'independent_verifier'/'pareto_all_m_certificate.json').read_text()
)
ordered_variables=(
    ('unit homogeneous',unit_certificate['homogeneous']['variables'],['x','z']),
    ('unit spatial',unit_certificate['improved_mode']['variables'],['x','z','s']),
    ('scaled homogeneous',pareto_certificate['modulus']['homogeneous']['variables'],['x','z']),
    ('scaled spatial',pareto_certificate['modulus']['spatial']['variables'],['x','z','s']),
)
for name,actual,expected in ordered_variables:
    if actual != expected:
        raise AssertionError(f'{name} certificate variable order {actual!r} != {expected!r}')
for section_name,parameter in (('homogeneous','U'),('spatial','A')):
    required=f'coefficient_in_{parameter}_ascending'
    for row in pareto_certificate['modulus'][section_name]['terms']:
        recognized={
            key for key in ('coefficient_in_U_ascending','coefficient_in_A_ascending')
            if key in row
        }
        if recognized != {required}:
            raise AssertionError(
                f'scaled {section_name} row {row.get("powers")!r} has coefficient '
                f'fields {sorted(recognized)!r}; expected only {required!r}'
            )

# Keep the structured comparison table aligned with its named columns.
with (ROOT/'literature'/'theorem_comparison.csv').open(newline='') as handle:
    comparison_rows=list(csv.DictReader(handle))
conradi=next(
    (row for row in comparison_rows if row['Prior result']=='Conradi-Mincheva-Uecker 2026'),
    None,
)
if conradi is None:
    raise AssertionError('literature comparison lacks Conradi-Mincheva-Uecker 2026')
for field,expected in (
    ('Exact diffusion law','no'),
    ('Nonlinear branch','numerical continuation'),
    ('Stable branch','numerically stable segments'),
):
    if conradi[field] != expected:
        raise AssertionError(f'Conradi comparison column {field!r} is {conradi[field]!r}')

certificate_table=(ROOT/'data'/'certificate_tables.tex').read_text()
if re.search(r'\d+/\d+[AU](?:\^\{\d+\})?',certificate_table):
    raise AssertionError('ambiguous slash fraction adjacent to a certificate parameter')
if len(re.findall(r'\d+A/\d+',certificate_table)) != 50:
    raise AssertionError('unexpected count of unambiguous rational-A table entries')

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
           r'Lyapunov--Schmidt coefficients',r'2\^\{m-2\}',
           r'z\s*=\s*\\mathsf\s*H_m\s*\(L\)\s*x',
           r'r_i\s*=\s*\\frac\{K_\{i-1\}\}\{K_i\}',
           r'c\s*=\s*\\frac\{91L\}\{90\}',
           r'\\nu\s*=\s*1\s*\+\s*\(2-t\)\\varepsilon',
           r'u\s*=\s*1\s*\+\s*\(2-t\)\\varepsilon',
           r'The dashed outline marks the principal species set',
           r's_\*\s*\(H,D\)',r'explicit two-parameter Jacobian image',
           r'topology-wide over-realizations theorem',
           r'physical fixed-mass vector becomes',
           r'reduces\s*\$?\\max\s*\(\\chi_D,\\chi_H\)',
           r'reduces the larger of the two contrasts',
           r'two surviving cycle covers',
           r'two\s+feed-forward chain fragments,\s*followed by',
           r'or equivalently the exact infimum of']
for pat in forbidden:
    if re.search(pat,clean,re.I): raise AssertionError(f'obsolete wording: {pat}')

# The subscripted symbols r_m and ell_m denote scalar X_m components.  Reject
# their former use in whole-vector operations while leaving component
# definitions such as r_m=-2/9 and ell_m=18368/7335 untouched.
ill_typed_whole_vector_patterns = (
    r'\\ell_m\s*\^\s*T',
    r'\\widetilde\s*\{?\\ell_m\}?',
    r'\\operatorname\{span\}\s*\\?\{\s*r_m(?:\\cos|\s*\\?\})',
    r'\\operatorname\{span\}\s*\\?\{\s*\\ell_m(?:\\cos|\s*\\?\})',
    r'D_m\s*r_m(?:\\cos|\b)',
    r'\\Delta(?:_m)?\s*r_m\b',
    r'\(A_m-(?:D_m|\\Delta_m?)\)\s*r_m\b',
    r'\(A_m-\\Delta_m?\)v\s*=\s*r_m\b',
)
for pat in ill_typed_whole_vector_patterns:
    if re.search(pat,clean):
        raise AssertionError(f'component symbol used as a whole vector: {pat}')

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
for name,section in (("main",main_flat),("supplement",supp_flat)):
    if 'componentwise strictly positive' not in section:
        raise AssertionError(f'{name} does not close componentwise positivity of the branch')
    if not re.search(
        r'\\chi_D\(L\)>\\chi_H\(L\).*?uniquely minimized.*?\$L=L_0\$',
        section,
        re.S,
    ):
        raise AssertionError(f'{name} does not state the exact within-family minimax conclusion')
if 'measures equilibrium concentration-scale separation' not in main_flat:
    raise AssertionError('chi_H scale-separation qualification is missing')
if main.count(r'0<|I|<m') < 3:
    raise AssertionError('nonempty principal-set domain is not explicit throughout Section 3')
if not re.search(
    r'\\min\\left\\\{\|I\|:\\varnothing\\neI\\subseteq\[n\],\\alphaS\(J_\{I,I\}\)>0',
    ''.join(main.split()),
):
    raise AssertionError('localization minimum is not restricted to nonempty principal sets')
if 'selected positive realization' not in main_flat:
    raise AssertionError('Corollary 3.3 does not scope stable patterns to a selected realization')
if 'one-dimensional center-manifold normal form is' not in main_flat:
    raise AssertionError('dynamical amplitude equation is not identified as a center-manifold normal form')
if r'(0,\mathcal L)' not in main or r'q_k^2=(k\pi/\mathcal L)^2' not in main:
    raise AssertionError('physical interval length is not consistently written as mathcal L')
for name,section in (("main",main_flat),("supplement",supp_flat)):
    if not re.search(
        r'For\s+\$m=3\$.*?\\\{X_1,X_2\\\}.*?\\\{X_2,X_3\\\}.*?assume\s+\$m\\geq?4\$',
        section,
        re.I,
    ):
        raise AssertionError(f'{name} omits the direct m=3 SCC base case')
for name,section in (("main",main_flat),("supplement",supp_flat)):
    reflection_markers = (
        r'(\mathcal Ru)(\xi)=u(\pi-\xi)',
        'reduced vector field is odd',
    )
    if not all(marker in section for marker in reflection_markers):
        raise AssertionError(f'reflection-equivariant odd normal form is not explicit in the {name}')
    if not re.search(r'\\mathcal R.{0,80}?A\\mapsto-A',section):
        raise AssertionError(f'{name} omits the induced A-to-minus-A reflection action')
    if not re.search(r'(?:exchanged by reflection|reflection exchanges)',section,re.I):
        raise AssertionError(f'{name} omits reflection pairing of the two branches')
for name,section in (("main",main_flat),("supplement",supp_flat)):
    if not re.search(
        r'\\partial_t\\widehat x\s*=\s*\\mathsf H_m\(L\).*?\(1-\\mu\)\\Delta(?:_m)?\\partial_\{\\xi\\xi\}\\widehat x',
        section,
        re.S,
    ):
        raise AssertionError(f'{name} omits the bifurcation parameter in the scaled-family PDE')
for name,section,delta in (
    ("main", main_flat, r"\Delta_m"),
    ("supplement", supp_flat, r"\Delta"),
):
    compact = ''.join(section.split())
    numerator = (
        r'\widetilde\ell(L)^T\mathsfH_m(L)'
        + delta
        + r'r=\ell^T'
        + delta
        + r'r<0'
    )
    if numerator not in compact:
        raise AssertionError(f'{name} omits the transformed transversality numerator')

# Mathematical-precision closures from the final adversarial review.
compact_main=''.join(main.split())
compact_supp=''.join(supp.split())

diffusion_law = main.split(r'\label{thm:diffusionlaw}',1)[1].split(r'\end{theorem}',1)[0]
if r'D=\diag(d_1,\ldots,d_m,d_Z)\succ0' not in ''.join(diffusion_law.split()):
    raise AssertionError('Theorem 5.2 does not quantify its positive diagonal diffusion matrix')
if 'either a singleton, whose corresponding diagonal entry is negative' not in main_flat:
    raise AssertionError('SCC classification does not separate negative singletons from non-singleton blocks')

# The component lists must be assembled into explicitly named full vectors.
# This prevents a future edit from silently reverting r_m or ell_m to a dual
# scalar/vector role.
for name,section in (("main",compact_main),("supplement",compact_supp)):
    for marker,label in (
        (r'r=(r_1,\ldots,r_m,r_Z)^T','right critical-vector definition'),
        (r'\ell=(\ell_1,\ldots,\ell_m,\ell_Z)^T','left critical-vector definition'),
        (r'\widetilde\ell(L)=\mathsfH_m(L)^{-1}\ell','scaled left-vector definition'),
    ):
        if marker not in section:
            raise AssertionError(f'{name} omits the explicit full {label}')

pareto_theorem = main.split(r'\label{thm:pareto}',1)[1].split(r'\end{theorem}',1)[0]
pareto_compact = ''.join(pareto_theorem.split())
if r'On$(0,\pi)$withhomogeneousNeumannboundaryconditions' not in pareto_compact:
    raise AssertionError('Theorem 7.1 does not state its spatial domain and boundary conditions')
physical_scaled_pde=(
    r'\partial_tx=f_m\!\left(\mathsfH_m(L)x\right)+(1-\mu)'
    r'D_m^{\rmphys}(L)\partial_{\xi\xi}x'
)
if physical_scaled_pde not in pareto_compact:
    raise AssertionError('Theorem 7.1 does not print the parameterized physical PDE')
if 'physical fixed-mass covector becomes' not in main_flat:
    raise AssertionError('scaled proof does not identify the fixed-mass object as a covector')

scaled_cubic_quotient=(
    r'c_m(L)=\frac{N_m(L)}{\widetilde\ell(L)^Tr}'
)
for name,section in (("main",compact_main),("supplement",compact_supp)):
    if scaled_cubic_quotient not in section:
        raise AssertionError(f'{name} omits the explicit scaled cubic quotient')

derivative_identity=(
    r"\Pi_m'(0)=\frac{7043400m-13600927-7043400\mathfrakh_m}{255150}"
    r"=-\frac{163}{45}\,\ell^Tr>0"
)
for name,section in (("main",compact_main),("supplement",compact_supp)):
    if derivative_identity not in section:
        raise AssertionError(f'{name} omits the all-dimensional selected-zero derivative identity')
for marker,label in (
    (r'\ker\!\left[\mathsfH_m(L)(A_m-\Delta_m)\right]',
     'scaled-family kernel identity'),
    (r'\mathsfH_m(L)(A_m-\Delta_m)v=r',
     'scaled-family generalized-vector contradiction'),
    (r'Fredholmofindexzero','stationary Fredholm interface'),
    (r'(\pi/2)\ell^TD_mr\ne0','Crandall--Rabinowitz transversality pairing'),
    (r'\sum_{|I|=n-1}(-1)^{|I|}\detJ_{I,I}>0',
     'network application order-(n-1) coefficient bridge'),
):
    if marker not in compact_main:
        raise AssertionError(f'main omits {label}')
for name,section in texts.items():
    if not re.search(r'(?:Let\s+\$n\\ge2|For\s+\$n\\ge2)',section):
        raise AssertionError(f'{name} omits the n>=2 diffusion-ray domain')
proof_criterion=(ROOT/'proof_audit'/'exact_diffusion_criterion.tex').read_text()
if 's_*(H,D)' in proof_criterion or 's_*(a,b,H,D)' not in proof_criterion:
    raise AssertionError('proof-audit threshold notation suppresses the flux parameters')

for stale_path in (
    r'\nu=1+(2-t)\varepsilon',
    r'u=1+(2-t)\varepsilon',
):
    if stale_path in ''.join(supp.split()):
        raise AssertionError(f'near-threshold path retains stale notation {stale_path}')
for marker in (
    r'r^{\rm aff}=(r_1,\ldots,r_m,r_Z)^T',
    r'(A_m-D)r^{\rm aff}=0',
    r'd_1=-2+u+p+2q',
    r'd_2=\frac{1+2p-u-v(m-3)/(m-2)}{u+v(m-3)/(m-2)}',
    r'd_i=\frac{v}{(m-2)u+v(m-1-i)}',
    r'd_m=\frac{2u-5p-2q-1}{p}',
    r'd_Z=\frac{2-2p-4q}{q}',
):
    if ''.join(marker.split()) not in ''.join(supp.split()):
        raise AssertionError(f'missing printed near-threshold affine identity {marker}')

for marker in (
    r'u=1+(2-\omega)\varepsilon+\theta\varepsilon^2',
    r'v=\omega\varepsilon-\theta\varepsilon^2',
    r'q=\frac12-\left(\frac12+\omega\right)\varepsilon+\left(\theta-\fracM2\right)\varepsilon^2',
    r'4\left(M+6\omega+3\omega^2-\frac{\omega^2}{m-2}\right)\varepsilon^2',
    r'(\omega,\theta,M)=(2/9,1/2,1)',
    r'd_1=\frac{\varepsilon(3\varepsilon+8)}6',
    r'd_Z-8d_2=\frac{8\varepsilon^2(197-99\varepsilon)}{(9-13\varepsilon)(9\varepsilon^2+32\varepsilon+18)}>0',
    r'\det(\lambda I-A_3+tD_\varepsilon)=\lambda^4+a_1\lambda^3+a_2\lambda^2+a_3\lambda+a_4',
    r'\varepsilon=[1000(1+w)]^{-1}',
    r'q_3(\lambda)=(\lambda+7)(\lambda^2+5\lambda+2)',
):
    if ''.join(marker.split()) not in ''.join(supp.split()):
        raise AssertionError(f'missing omega-renamed near-threshold identity {marker}')
if 'long-circuit complexes associated with the principal species block' not in main_flat:
    raise AssertionError('Figure 1 caption does not describe its dashed complex outline literally')
for marker in (
    r'\begin{pmatrix}-218/63&-T_{m-1}&-1&2',
    r'\delta_m=\frac{\sigma}{3}\left(T_{m-1}K_2-K_{m-1}\right)',
    r'b^{(2)}_1+\delta_m',
    r'\frac{64\mathcalQ_m}{6615(91m-183)(91m-181)(91m-180)}',
):
    if marker not in ''.join(supp.split()):
        raise AssertionError(f'missing printed w2 boundary-system marker {marker}')
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

for marker,label in (
    ('fixed interval', 'fixed-interval stationary-bifurcation convention'),
    ('do not claim intrinsic finite-wavelength selection', 'finite-wavelength scope qualification'),
    ('numerically continue nonlinear patterned branches', 'Conradi nonlinear numerical comparison'),
    ('numerically stable segments', 'Conradi stable-segment comparison'),
):
    if marker not in main_flat:
        raise AssertionError(f'main omits {label}')

certificate_table=(ROOT/'data'/'certificate_tables.tex').read_text()
if r'\frac{' in certificate_table:
    raise AssertionError('modulus-certificate tables retain stacked rational fractions')

submission_root=ROOT/'submission'
if submission_root.is_dir():
    cover=(submission_root/'journal'/'cover_letter_SIADS.tex').read_text()
    declarations=(submission_root/'journal'/'statements_and_declarations.md').read_text()
    biorxiv_metadata=(submission_root/'biorxiv'/'metadata.yaml').read_text()
    declaration_corpus=' '.join((cover+'\n'+declarations+'\n'+biorxiv_metadata).split())
    for marker,label in (
        ('no specific funding', 'funding declaration'),
        ('no competing interests', 'competing-interest declaration'),
        ('not under consideration by, and has not been submitted to, another journal', 'journal-exclusivity declaration'),
    ):
        if marker not in declaration_corpus:
            raise AssertionError(f'submission materials omit the author-confirmed {label}')
    for stale in ('Author confirmation required', 'author to confirm', 'No funding information supplied'):
        if stale.lower() in declaration_corpus.lower():
            raise AssertionError(f'submission materials retain stale declaration placeholder: {stale}')

# Release PDFs may be accepted only after their final TeX logs pass the same
# warning gate.  Keep the detached journal and cover-letter checks before the
# corresponding copy operations, where a failure can still prevent sealing.
refresh_path=ROOT/'release'/'refresh_packages.sh'
if refresh_path.is_file():
    refresh=refresh_path.read_text()
    gate='release/audit_tex_logs.py'
    if gate not in refresh:
        raise AssertionError('package refresh omits the shared final-TeX-log gate')
    journal_gate=(
        'python "$ROOT/release/audit_tex_logs.py" \\\n'
        '  "$JOURNAL_BUILD/main.log" "$JOURNAL_BUILD/supplement.log" >/dev/null'
    )
    cover_gate=(
        'python "$ROOT/release/audit_tex_logs.py" '
        '"$COVER_BUILD/cover_letter_SIADS.log" >/dev/null'
    )
    ordered_release_boundaries=(
        ('detached journal manuscript', journal_gate,
         'cp "$JOURNAL_BUILD/main.pdf"'),
        ('detached journal supplement', journal_gate,
         'cp "$JOURNAL_BUILD/supplement.pdf"'),
        ('journal cover letter', cover_gate,
         'cp "$COVER_BUILD/cover_letter_SIADS.pdf"'),
    )
    for label,gate_marker,copy_marker in ordered_release_boundaries:
        try:
            gate_position=refresh.index(gate_marker)
            copy_position=refresh.index(copy_marker)
        except ValueError as error:
            raise AssertionError(f'package refresh omits {label} log/copy boundary') from error
        if gate_position >= copy_position:
            raise AssertionError(f'{label} PDF is copied before its final log is audited')
    if '--journal-negative-control' not in refresh:
        raise AssertionError('package refresh omits the journal overfull-box negative control')

replay_path=ROOT/'release'/'one_command_replay.sh'
if replay_path.is_file():
    replay=replay_path.read_text()
    if 'release/audit_tex_logs.py" main.log supplement.log' not in replay:
        raise AssertionError('detached submission source builds omit final-log auditing')
    for marker in ('pdfinfo main.pdf', 'pdfinfo supplement.pdf',
                   'cp "$submission_builds" release/submission_source_builds.txt'):
        if marker not in replay:
            raise AssertionError('detached submission source evidence is not regenerated')

print('MANUSCRIPT_AUDIT_PASS')
print('labels',len(labels),'references',len(refs),'bibkeys',len(bibkeys),'citations',len(cites),'abstract_words',len(words))
