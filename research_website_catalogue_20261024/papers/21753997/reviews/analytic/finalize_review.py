from pathlib import Path
import datetime, hashlib, json, shutil, sys

here = Path(__file__).resolve().parent
paper = here.parent.parent
sources = paper/'sources'
release = sources/'published-source/AlecKriebel-Math-26f7e00/weakly_reversible_continuum_no_common_factor/releases/v2.0'
stamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

def sha(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest()

def write(name,data):
    (here/name).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')

receipt=json.loads((sources/'receipt.json').read_text())
asset_checks=[]
for entry in receipt['files']:
    path=sources/entry['name']
    current=sha(path)
    assert current==entry['sha256'] and path.stat().st_size==entry['bytes']
    asset_checks.append({'path':str(path.relative_to(paper)), 'sha256':current,'bytes':path.stat().st_size})
assert sha(sources/'record.json')==receipt['record_sha256']
selected=[]
for archive in receipt['archives']:
    for entry in archive['members']:
        if entry.get('extracted'):
            path=sources/'published-source'/entry['path']
            assert sha(path)==entry['sha256'] and path.stat().st_size==entry['bytes']
            selected.append({'path':str(path.relative_to(paper)), 'sha256':entry['sha256']})
assert len(selected)==126
before=json.loads((here/'published-support-before.json').read_text())
assert all(sha(release/name)==digest for name,digest in before.items())
assert all(sha(here/'replay-work/v2.0'/name)==digest for name,digest in before.items())
write('source-integrity-final.json', {'completed_utc':stamp,'status':'PASS','assets':asset_checks,
    'record_sha256':sha(sources/'record.json'),'receipt_sha256':sha(sources/'receipt.json'),
    'selected_extracted_files_rehashed':selected,'release_and_replay_copy_unchanged':True,
    'release_files_count':len(before),'unrelated_projects_read':False})

cache=here/'primary-sources';cache.mkdir(exist_ok=True)
primary=[]
for name,url,expected,pages,scope in [
    ('boros-craciun-yu','https://pollyyu.web.illinois.edu/manuscripts/2020-WR%20systems%20with%20infinitely%20many%20steady%20states.pdf','e63bdc76a0d3f712c8e0b54f527a8f8a1e9969930248db7527b8c91abe0fcace',10,'pp.1–3 definitions/context, Section5 p.8 exact question and rate flexibility'),
    ('feliu-henriksson-pascual-escudero','https://arxiv.org/pdf/2412.17798v3','fb711f96966a225b12a49ce1f130a89e000c9d2e7d54becf6cf7158865927a54',30,'v3 dated14May2026: pp.2–3,9–11,13–14; Theorems3.1/3.4 and Corollaries3.5/3.13 interface only')]:
    raw=paper/'reviews/scope/.reference-cache'/(name+'.pdf')
    assert sha(raw)==expected
    for ext in ['pdf','txt']:
        shutil.copyfile(raw.with_suffix('.'+ext),cache/(name+'.'+ext))
    primary.append({'name':name,'url':url,'pdf_path':'primary-sources/'+name+'.pdf',
        'sha256':expected,'bytes':raw.stat().st_size,'pdf_pages':pages,'reading_scope':scope,
        'online_primary_url_opened_in_this_review':True,
        'full_primary_proof_reproduced':False,
        'original_acquisition_receipt':'../scope/primary_source_receipts.json'})
write('primary-source-bindings.json',{'bound_at_utc':stamp,'sources':primary})

with (here/'RESEARCH_LOG.md').open('a') as stream:
    stream.write('\n## '+stamp+' — 100% of assigned analytic review\n\nAll current claims and necessary mathematical support reviewed; sixty independent exact controls and all four published mathematical layers plus three ancillary checks passed. Exact irrational-kernel counterexample preserved to the unrestricted real-rate reading of Theorem3.1; the rational-rate formulation and central constructive claims remain supported. No source repairs or publication actions. Full original archive and all126 extracted named-work files rehashed unchanged. Final report records scope and source limits, and defers the unqualified printed domain statement for root disposition.\n')

exclude={'verdict.json','artifact-manifest.json'}
artifacts={str(path.relative_to(here)):sha(path) for path in here.rglob('*')
    if path.is_file() and path.name not in exclude and 'replay-work' not in path.parts and '__pycache__' not in path.parts}
write('artifact-manifest.json',artifacts)
pdf=release/'output/pdf/manuscript-v2.0.0.pdf'
write('verdict.json',{
    'record_id':'21753997','review_role':'independent_analytic','completed_at_utc':stamp,
    'completion_percent':100,'status':'DEFER_UNQUALIFIED_DOMAIN_STATEMENT',
    'mathematical_core_status':'PASS_AT_RATIONAL_RATE_INTERPRETATION',
    'claim_scope':'Four-dimensional fixed-support conic-preserving kernel over Q (and corresponding base extension); strict positive cone; explicit integer constructions with geometric gcd1 and radical conic-plus15point steady ideals; fixed-family positive-integral maximum/sum optima; frozen-only exact transverse spectral classification; stated structural lower bounds.',
    'finding':{'id':'DOMAIN-1','location':'PDF pp.4–5 Theorem3.1, together with real-rate convention on p.2',
        'severity':'narrow_domain_quantifier_issue_not_refutation_of_central_construction',
        'fact':'An irrational positive-rate kernel perturbation leaves the clean rational field unchanged, contradicting the iff with rational free parameters if the input rate vector is unrestricted real.',
        'evidence':'domain-counterexample.json','rational_rate_reading_valid':True,
        'full_real_rate_input_reading_valid_as_printed':False,'source_repaired':False},
    'source_binding':{'receipt_sha256':sha(sources/'receipt.json'),'record_sha256':sha(sources/'record.json'),
        'assets':asset_checks,'primary_pdf':{'path':str(pdf.relative_to(paper)),'sha256':sha(pdf),'pages':14},
        'main_source_sha256':sha(release/'source/MANUSCRIPT_V2.md'),'all126_selected_work_files_rehashed_unchanged':True},
    'evidence':{'independent_exact_checks':60,'published_mathematical_layers_passed':4,
        'additional_published_checks_passed':['frozen cleanroom','minimality arithmetic','release metadata'],
        'report_sha256':sha(here/'REVIEW.md'),'artifact_manifest_sha256':sha(here/'artifact-manifest.json')},
    'independence':{'fresh_controls_before_helper_inspection':True,'sibling_reports_read':False,
        'dedicated_historical_prose_verdicts_read':False,
        'incidental_required_support_status_exposure':'Current manuscript Sections10–11 and executable support comments/status fixtures; not relied upon.'},
    'limitations':['Not human peer review','No novelty or priority certification','No global network-support optimality','No detailed-balance inference','No ambient-rate robustness','No global nonlinear attraction or clean-family stability inference','Theorem3.1 coefficient-field interpretation requires explicit root disposition'],
    'sources_modified':False,'publication_actions':False,'outreach':False
})
for name in ['REVIEW.md','verdict.json','artifact-manifest.json']:
    print(name,sha(here/name))
