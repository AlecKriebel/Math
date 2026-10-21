#!/usr/bin/env python3
"""Independent exact local binding/source receipt; no network or outside-source reads."""
from pathlib import Path
import datetime
import hashlib
import json
import stat

A=Path(__file__).resolve().parents[1];R=A/'package_review_01'
T=A.parents[1]/'work/pr822_revision_r1'
def need(c,m):
    if not c:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_bytes())
mapping=read(A/'PREPARED_PR_MAPPING_R1.json')
need(mapping['expected_head']=='c9fd5a0462d1fa98f21aa7037f7a5e061fbbee9c'
     and mapping['pr']==822 and mapping['problem_id']==30001168,'mapping identity')
need(len(mapping['files'])==163,'mapping file count')
seen=set()
prefix='unsolved_math_prioritization/attempts/30001168/'
for row in mapping['files']:
    p=Path(row['local_path'])
    need(p.is_relative_to(T),'mapping path outside explicit tree')
    relative=p.relative_to(T).as_posix()
    need(row['repo_path']==prefix+relative and relative not in seen,'mapping destination')
    seen.add(relative)
    need(stat.S_ISREG(p.lstat().st_mode) and sha(p)==row['sha256'],'mapping digest')
need(seen=={p.relative_to(T).as_posix() for p in T.rglob('*') if p.is_file()},'mapping completeness')
receipt=read(A/'LOCAL_PR_ASSEMBLY_R1.json')
need(sha(T/'PUBLICATION_MANIFEST.json')==receipt['outer_manifest_sha256'],'outer receipt digest')
source=read(A/'SOURCE_MANIFEST.json')
need(source['original_head']==mapping['expected_head'] and len(source['files'])==42,'source identity')
for row in source['files']:
    p=A/'source'/row['path']
    need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'source frozen bytes')
    q=T/'publication_20261013/verification_package/source'/row['path']
    need(q.read_bytes()==p.read_bytes(),'assembly frozen source identity')
corpus=read(A/'priority_audit_01/CORPUS_MANIFEST.json');checked=0;pdfs=[]
for row in corpus['files']:
    p=(A/'priority_audit_01'/row['relative_private_path']).resolve()
    need(p.is_relative_to(A/'priority_audit_01/private_sources'),'raw corpus path escapes')
    need(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'raw corpus digest')
    checked+=1
    if p.suffix=='.pdf':pdfs.append({'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p)})
need(len(pdfs)==26 and len({row['sha256'] for row in pdfs})==25,'public corpus version counts')
metadata=read(A/'preprint/metadata.json')
need(metadata==read(A/'preprint/zenodo-deposit.json')['metadata']
     ==read(T/'PUBLICATION_METADATA.json')['zenodo_metadata'],'metadata copies differ')
need(metadata['creators']==[{'name':'Kriebel, Alec','affiliation':'Independent researcher',
     'orcid':'0009-0001-9320-500X'}] and metadata['license']=='cc-by-4.0'
     and metadata['publication_type']=='preprint','author/license/status')
source_inspections=[
 {'file':'private_sources/OWR_2009_06.pdf','locators':'printed 421-422, PDF 67-68; item16 Conjectures1-2',
  'inspection':'target formula, normalization, round L2 operator, quantifiers, adjacent scope'},
 {'file':'private_sources/Ammann_Jammes_author_20081208.pdf',
  'locators':'pp1-3 Theorems1.2/1.3, pp5-6 Example1, pp7-8 section3.2, pp9-10 Theorem4.1, p14 refs2/6',
  'inspection':'construction sufficient after explicit fixed cap and all-index Dirichlet modes; fixed-index theorem alone not heat claim'},
 {'file':'priority_audit_01/private_sources/historical/morpurgo_2002_inspected_web_sections.txt',
  'locators':'captured manuscript sections: Proposition2.3, transform16, Lemma2.4, Theorem4.1/Corollary4.2',
  'inspection':'partial author manuscript capture, not full PDF/VOR; convex continuous transformed traces do not directly evaluate fixed heat time or its nonlinear maximum'},
 {'file':'priority_audit_01/private_sources/historical/branson_2007_sigma.pdf',
  'locators':'printed pp26-27, equations26-27 and limitations',
  'inspection':'even-dimensional regularized-zeta sign/inconclusive determinant argument; cannot transfer to three-dimensional heat maximum'},
 {'file':'priority_audit_01/private_sources/broader/ammann_humbert_arxiv_v2.pdf',
  'locators':'pp1-4 introduction, normalization, Definition1.3 and Theorems1.4-1.6',
  'inspection':'infima of fixed eigenvalues/generalized-metric minimizers, not growing-mode heat mass'},
 {'file':'priority_audit_01/private_sources/broader/humbert_petrides_premoselli_arxiv_v2.pdf',
  'locators':'pp5-7 generalized eigenvalues, invariants and Theorems1.1-1.2; theorem1.7',
  'inspection':'fixed-index extremals under unique-continuation hypothesis; for Yamabe nonround sphere theorem requires n>=7; no n3 heat maximum'},
 {'file':'private_sources/Zhao_2012_08757v2.pdf','locators':'pp1-3 Theorem1.1 and Remarks1.2',
  'inspection':'Laplace-Beltrami heat kernels, small bounded conformal perturbation, nonsharp unspecified constants; distinct Yamabe operator/functional'},
 {'file':'priority_audit_01/private_sources/synthesis/frank2020_review.pdf',
  'locators':'section4.6 pp20-22, Lemma15, Conjecture16 and sphere reconstruction',
  'inspection':'GGM reconstruction constant sphere potentials; count counterexamples in d>=7 do not provide nonround n3 positive-normalized heat weight'},
 {'file':'priority_audit_01/private_sources/synthesis/corso_ried2025.pdf',
  'locators':'pp4-7 Theorems1.4/1.6, Table2 and normalization',
  'inspection':'method-specific upper count/LT bounds, not a converse lower heat example or exact sharp heat comparator'}]
for row in source_inspections:
    p=A/row['file'];row['sha256']=sha(p);row['bytes']=p.stat().st_size
result={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS',
        'mapping_files_verified':len(seen),'original_files_verified':42,'raw_corpus_files_verified':checked,
        'raw_pdf_copies':len(pdfs),'distinct_raw_pdf_bytes':len({p['sha256'] for p in pdfs}),
        'outer_manifest_sha256':sha(T/'PUBLICATION_MANIFEST.json'),'metadata_identity':True,
        'author_ORCID_CCBY_preprint_verified':True,'independent_source_passages':source_inspections,
        'prior_verdicts_not_used_as_mathematical_truth':True,'historical_firstness_certified':False,
        'current_openness_certified':False,'novel_geometric_or_spectral_mechanism_certified':False,
        'priority_gap':'Bounded corpus non-detection only; final/older unavailable versions and exhaustive current-citation census remain open.'}
(R/'BINDINGS_AND_PRIORITY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='independent_source_passages'},indent=2))
