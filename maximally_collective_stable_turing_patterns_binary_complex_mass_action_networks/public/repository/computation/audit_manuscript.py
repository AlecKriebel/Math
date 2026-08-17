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
        for lab in re.findall(r'\\label\{([^}]+)\}',body): envs[lab]=typ
# Named cleveref references are allowed; reject stale literal "Theorem 3.1" etc.
if re.search(r'\b(?:Theorem|Proposition|Lemma|Corollary|Remark)\s+\d+\.\d+',clean):
    raise AssertionError('literal numbered environment reference remains')

required_title='Exact Diffusion Design for Maximally Collective Stable Turing Patterns'
for name,text in texts.items():
    if required_title not in text:
        raise AssertionError(f'final title missing from {name}')

forbidden=[r'\bT-ALG\b',r'\bPhase\s+[IVX]+\b',r'reaction-minimal',r'minimum reaction count',
           r'bounded.catalog',r'square-root-balanced',r'right panel',r'one-bad-minor diffusion theorem',
           r'one-bad-minor matrix theorem']
for pat in forbidden:
    if re.search(pat,clean,re.I): raise AssertionError(f'obsolete wording: {pat}')

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

print('MANUSCRIPT_AUDIT_PASS')
print('labels',len(labels),'references',len(refs),'bibkeys',len(bibkeys),'citations',len(cites),'abstract_words',len(words))
