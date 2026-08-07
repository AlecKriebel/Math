#!/usr/bin/env python3
"""Independent journal-package and PDF audit."""
from __future__ import annotations
from pathlib import Path
from zipfile import ZipFile
import json,re,subprocess
ROOT=Path(__file__).resolve().parents[3]
SUB=ROOT/'submission'; PAPER=ROOT/'source'/'paper'

def pages(path):
    out=subprocess.check_output(['pdfinfo',str(path)],text=True)
    m=re.search(r'^Pages:\s+(\d+)$',out,re.M);assert m,path
    return int(m.group(1))

def fonts(path):
    out=subprocess.check_output(['pdffonts',str(path)],text=True).splitlines()[2:]
    assert out,path
    assert all(row.split()[4]=='yes' for row in out if row.split()),path

def main():
    required={
      'Generic_Identifiability_STC_Level2_JC.pdf':48,
      'Cover_Letter.pdf':1,'Cover_Letter_JMB.pdf':1,'Cover_Letter_BMB.pdf':1,
      'Referee_Guide.pdf':2,
    }
    for name,n in required.items():
        path=SUB/name;assert path.exists() and pages(path)==n,(name,pages(path) if path.exists() else None);fonts(path)
    assert (PAPER/'main.pdf').read_bytes()==(SUB/'Generic_Identifiability_STC_Level2_JC.pdf').read_bytes()
    with ZipFile(SUB/'LaTeX_TikZ_Source.zip') as z:
        names=set(z.namelist());assert 'paper/main.tex' in names and 'paper/references.bib' in names
        assert sum(name.startswith('paper/figures/') and name.endswith('.tex') for name in names)==8
        assert sum(name.startswith('paper/sections/') and name.endswith('.tex') for name in names)>=15
    with ZipFile(SUB/'STC_JC_Reproducibility.zip') as z:
        names=set(z.namelist())
        for name in [
          'reproducibility/verify_quick.sh','reproducibility/verify_full.sh',
          'reproducibility/exact_release/verify_release.py',
          'reproducibility/publication/src/regenerate_nonroot_algebra.py',
          'reproducibility/publication/src/verify_multitriangle_exclusion.py',
          'reproducibility/publication/review/review_multitriangle_exclusion.cpp',
          'reproducibility/publication/certificates/multitriangle_exclusion.json',
          'reproducibility/publication/certificates/all_level2_strengthening.json',
          'reproducibility/publication/src/regenerate_cycle_algebra.py',
          'reproducibility/publication/review/review_directed_pair_universe.cpp',
          'transcripts/clean_quick_verification.txt',
          'transcripts/clean_full_verification.txt',
          'transcripts/clean_pointwise_cut_adversarial.txt',
          'review/MATHEMATICAL_SCOPE_AND_RELEASE_AUDIT.md']:
            assert name in names,name
        assert b'AUTHOR-READY QUICK VERIFICATION PASSED' in z.read('transcripts/clean_quick_verification.txt')
        assert b'AUTHOR-READY FULL INDEPENDENT VERIFICATION PASSED' in z.read('transcripts/clean_full_verification.txt')
        assert b'\"status\": \"VERIFIED\"' in z.read('transcripts/clean_pointwise_cut_adversarial.txt')
    text='\n'.join(p.read_text(errors='replace') for p in PAPER.rglob('*.tex'))
    assert 'Proposition~2.26 in the April 2025 version' in text
    assert 'restored support' in text
    assert 'Artificial-intelligence systems are not authors' in text
    assert 'Ardiyansyah2021' in text
    assert 'complete structural $\\Tmove$-equivalence class' in text
    assert 'not asserted to equal the set of topologies whose stochastic images contain' in text
    assert 'adversarial AI-assisted review processes' in text
    for forbidden in (
      'all distinct compatible encodings',
      'returns exactly the observational-equivalence class of the input distribution',
      'independent adversarial reviewers',
      'only intrinsic topological uncertainty',
      'sole unavoidable ambiguity'):
        assert forbidden not in text, forbidden
    print(json.dumps({'status':'VERIFIED','paper_pages':48,'referee_guide_pages':2,'cover_letter_pages':1,'tikz_figures':8,'component_archives_openable':True,'fonts_embedded':True},indent=2,sort_keys=True))
    print('ALL INDEPENDENT SUBMISSION-PACKAGE CHECKS PASSED')
if __name__=='__main__':main()
