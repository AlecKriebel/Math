"""Authenticate only this audit's explicit safe authored payload."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re

R=Path(__file__).resolve().parent
P=R.parent
HEAD='a7571ddbbbe2de3600b96bd7ccccf86e4d5748e7'
def pin(p):
    b=p.read_bytes()
    return dict(bytes=len(b),sha256=sha256(b).hexdigest())
def save(n,d):
    (R/n).write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
now=datetime.now(timezone.utc).isoformat()
m=json.loads((P/'SOURCE_MANIFEST.json').read_text())
assert m['head']==HEAD
checks=[]
for x in m['files']:
    a=pin(P/'source'/x['path'])
    assert a==dict(bytes=x['bytes'],sha256=x['sha256'])
    checks.append(dict(path=x['path'],**a,matches_pin=True))
assert len(checks)==21
save('INPUT_CHECK.json',dict(timestamp_utc=now,head=HEAD,pr=888,problem_id='30005079',
    original_effort='1/5',all21_source_pins_match=True,checks=checks,
    native_pair_pin=pin(P/'private_native/canonical_pair.json'),
    source_manifest_pin=pin(P/'SOURCE_MANIFEST.json'),other_family_reports_read=False))
pdfs=[]
for x in json.loads((P/'source/SOURCE_MANIFEST.json').read_text())['primary_sources']:
    if x['filename'] in ['owr2022_17.pdf','miao_wang_solitons_v4.pdf','miao_wang_optimal_v2.pdf']:
        a=pin(P/'private_sources'/x['filename'])
        assert a==dict(bytes=x['bytes'],sha256=x['sha256'])
        pdfs.append(dict(url=x['url'],private_path='../private_sources/'+x['filename'],**a))
extra=[('2409.15718v3','2409.15718v3'),('2411.07864v1','2411.07864v1'),
    ('2603.09269v2','2603.09269v2'),('2406.06176v2','2406.06176v2'),
    ('2103.06439latest','2103.06439v6'),('2305.05366latest','2305.05366v1'),
    ('2206.04880latest','2206.04880v5'),('2401.13999v1','2401.13999v1'),
    ('2601.15576latest','2601.15576v2')]
for local,ident in extra:
    f=R/'private_tmp'/(local+'.pdf')
    assert f.read_bytes().startswith(b'%PDF-')
    pdfs.append(dict(url='https://arxiv.org/pdf/'+ident,private_path='private_tmp/'+f.name,**pin(f)))
f=R/'private_tmp/tian_zhu_jems_vor.pdf'
assert f.read_bytes().startswith(b'%PDF-')
pdfs.append(dict(url='https://ems.press/content/serial-article-files/53327',private_path='private_tmp/'+f.name,**pin(f)))
assert len(pdfs)==13
meta=['fetch_receipt.json','crossref_optimal.json','crossref_solitons.json',
    'openalex_optimal.json','openalex_solitons.json','openalex_citers_optimal.json',
    'openalex_citers_solitons.json','openalex_search_solitons.json','li_li_vor.html',
    'miao_wang_solitons_vor.html','miao_wang_optimal_vor_xml.html',
    'crossmark_optimal.html','crossmark_solitons.html']
prior_meta={x['private_path']:x for x in json.loads((R/'EXTERNAL_SOURCE_PINS.json').read_text())['metadata_receipts']} if (R/'EXTERNAL_SOURCE_PINS.json').exists() else {}
meta_pins=[]
for n in meta:
    f=R/'private_tmp'/n
    key='private_tmp/'+n
    if f.exists():meta_pins.append(dict(private_path=key,**pin(f),retained=True))
    else:meta_pins.append(dict(**{k:v for k,v in prior_meta[key].items() if k not in ['retained','removed_reason']},retained=False,removed_reason='Own discovery-index or subscription-preview body removed for disk pressure after inspection; hash retained.'))
save('EXTERNAL_SOURCE_PINS.json',dict(timestamp_utc=now,primary_pdf_bodies=pdfs,
    primary_pdf_body_count=13,distinct_primary_works=12,
    metadata_receipts=meta_pins,
    scope='Relevant primary sections inspected. Metadata and HTML previews are not journal bodies.',
    all_copied_sources_private=True))
ledger=json.loads((R/'SEARCH_LEDGER.json').read_text())
q=sum(len(b['queries']) for b in ledger['batches'])
save('FINAL_STATUS.json',dict(timestamp_utc=now,head=HEAD,pr=888,problem_id='30005079',
    family='priority_recent_01',family_completion_estimate_percent=100,
    status='BOUNDED_RECENT_PRIORITY_AUDIT_COMPLETE',verified_complete_prior_example_found=False,
    priority_established=False,continued_openness_established=False,
    strongest_adverse_lead='Li–Li 2103.06439v6 Section 6 p.36 case (2): explicit first H-degeneration; rational rank unverified.',
    search_query_count=q,primary_pdf_body_count=13,distinct_primary_works=12,
    citation_census_exhaustive=False,full_journal_body_comparison_complete=False,
    suggested_scope='Authored construction from specified prior inputs; no first-example or continued-openness claim.',
    mathematical_disposition_override=False,whole_package_clearance=False,
    other_family_reports_read=False,external_individual_communication=False,
    git_index_ref_config_remote_zenodo_mutation=False,authoring_marker_810_rerun=False))
names=['PROVISIONAL_FREEZE.md','REPORT.md','SEARCH_LEDGER.json','EDITION_AND_ACCESS.json',
    'RESEARCH_LOG.md','verify_audit.py','INPUT_CHECK.json','EXTERNAL_SOURCE_PINS.json','FINAL_STATUS.json']
findings=[]
for n in names:
    s=(R/n).read_text()
    if n!='verify_audit.py':
        for category,pattern in [('email',r'\b[\w.%+-]+@[\w.-]+\.[A-Za-z]{2,}\b'),('user_path',r'/Users/[^\s]+')]:
            if re.search(pattern,s):findings.append(dict(file=n,category=category))
assert not findings
save('PRIVACY_CHECK.json',dict(timestamp_utc=now,status='PASS',findings=findings,
    checked_authored_payloads=names,copied_sources_in_safe_payload=False,
    raw_native_pair_in_safe_payload=False,checker_self_regex_excluded=True,
    strategy='Explicit allowlist; copied bodies, raw metadata and extractions excluded.'))
names.append('PRIVACY_CHECK.json')
save('SAFE_PAYLOAD_MANIFEST.json',dict(timestamp_utc=now,head=HEAD,pr=888,problem_id='30005079',
    self_excluded='SAFE_PAYLOAD_MANIFEST.json',payload_count=len(names),
    files=[dict(path=n,**pin(R/n)) for n in names],excluded=['private_tmp/**','SAFE_PAYLOAD_MANIFEST.json'],
    purpose='Authored audit only; no mathematical acceptance or publication permission.'))
for x in json.loads((R/'SAFE_PAYLOAD_MANIFEST.json').read_text())['files']:
    assert pin(R/x['path'])==dict(bytes=x['bytes'],sha256=x['sha256'])
print(json.dumps(dict(source_files_verified=21,primary_pdf_bodies=13,queries=q,
    safe_payload_count=len(names),privacy='PASS',manifest=pin(R/'SAFE_PAYLOAD_MANIFEST.json')),indent=2))
