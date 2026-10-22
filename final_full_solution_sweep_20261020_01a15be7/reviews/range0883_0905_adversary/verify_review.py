#!/usr/bin/env python3
"""Read-only bounded review and final-seal verification. Never reads mutable root files."""
import pathlib,json,hashlib,sys
W=pathlib.Path(__file__).resolve().parent
def read(p):return json.loads((W/p).read_text())
def require(ok,msg):
 if not ok:raise SystemExit('FAIL: '+msg)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
for item in read('INPUT_COHERENCE.json'):
 for key,value in item.items():
  if isinstance(value,bool):require(value,f"PR{item['pr']} input coherence {key}")
s=read('SCOPE_CHECKS.json')['results'];require([x['pr'] for x in s]==list(range(883,906)),'exact23 PR interval')
for x in s:
 n=x['pr'];require(x['paths_equal'] and x['rows_equal'] and not x['cache_blob_mismatches'],f'PR{n} pinned paths/rows/non-null cached blobs')
 require(len(x['bindings'])==x['path_count'] and all(b['head_blob'] for b in x['bindings']),f'PR{n} complete scientific head blobs')
 require(x.get('explicit_status_verified',x.get('claimed_status_verified')),f'PR{n} own explicit status')
 if x['cache_unbound_blobs']:require(x.get('coverage_head_blob_bindings_equal') is True,f'PR{n} missing cache blobs independently rebound')
 if 'actual_merge_parents' in x:require(x['merge_second_parent_is_head'] and x['merge_first_parent_paths_equal'],f'PR{n} merged context')
p=read('PACKAGE_CHECKS.json')['results'];require([x['pr'] for x in p]==[883,885,888,894,904,905],'six publication packages')
for x in p:
 n=x['pr'];require(x['safety']['safe_unique_regular'] and x['safety']['crc_bad_member'] is None,f'PR{n} archive safety/CRC')
 for k in ['manifest_matches_receipt','closed_manifest','all_payloads_match','original_namespace_exact','all_originals_match','all_pdf_pins_verified']:require(x[k],f'PR{n} {k}')
 require(all(v['equal'] for v in x['manuscript_copy_checks']),f'PR{n} actual manuscript copies')
 require(all(v['equal'] and v['distinct_from_actual_note'] for v in x['historical_fixture_checks']),f'PR{n} disclosed historical fixture')
 for q in x['nested_archive_safety']:require(q.get('safe_unique_regular',q.get('safe_unique_regular_or_directory')) and q.get('crc_bad_member') is None,f'PR{n} nested archive safety')
for x in read('SOURCE_INVENTORY_CHECKS.json'):
 for k,v in x.items():
  if isinstance(v,bool):require(v,f"PR{x['pr']} source inventory {k}")
for x in read('METADATA_ALIGNMENT.json'):
 for k in ['published','record_id_equal','doi_equal','title_equal_receipt','description_equal_receipt','public_file_set_equal','creator_orcid_present']:require(x[k],f"PR{x['pr']} metadata {k}")
 if x['archive_metadata_exists']:require(x['archive_metadata_title_equal'] and x['archive_description_equal_after_apostrophe_normalization'],f"PR{x['pr']} archived metadata semantic identity")
for x in read('PUBLIC_FETCH_CHECKS.json'):
 require(x['doi_resolution'].get('status')==200 and x['doi_resolution']['url'].rstrip('/')==f"https://zenodo.org/records/{x['record']}",f"PR{x['pr']} DOI resolution")
 require(len(x['files'])==2 and all(v['provider_checksum_equal'] and v['expected_receipt_equal'] for v in x['files']),f"PR{x['pr']} actual public files")
for x in read('LEDGER_CHECKS.json')['checks']:require(x['doi_unique_exact_row'] and x['pr_reference_present'] and (x['problem_id_present'] or x['pr']==885),f"PR{x['pr']} fresh exact ledger identity")
require(all(x['bounded_identity_pass'] for x in read('DOCUMENT_SCOPE_REVIEW.json')['results']),'manual model/disclosure alignment')
require(read('GLOBAL_CUSTODY.json')['fixed_interval_dispositions_unchanged'],'fixed dispositions unchanged during moving root run')
if '--unsealed' not in sys.argv:
 final=read('FINAL_SEAL.json');pm=read('PUBLIC_MANIFEST.json');private=read('PRIVATE_MANIFEST_SEAL.json');cm=read(private['manifest_path'])
 for path,expected in final['pins'].items():require(pin(W/path)==expected,'final seal '+path)
 require(pin(W/private['manifest_path'])=={'bytes':private['bytes'],'sha256':private['sha256']},'detached complete-manifest pin')
 for x in pm['files']:require(pin(W/x['path'])=={'bytes':x['bytes'],'sha256':x['sha256']},'public manifest '+x['path'])
 for x in cm['files']:require(pin(W/x['path'])=={'bytes':x['bytes'],'sha256':x['sha256']},'complete manifest '+x['path'])
 actual={str(p.relative_to(W)) for p in W.rglob('*') if p.is_file()};listed={x['path'] for x in cm['files']};require(actual==listed|set(cm['excluded_seal_metadata']),'complete manifest exact file closure')
 public={p for p in actual if p.split('/')[0] not in ('inputs','downloads_private')};require(public=={x['path'] for x in pm['files']}|{'PUBLIC_MANIFEST.json','FINAL_SEAL.json'},'public projection exact file closure')
 require(not any(x['path'].split('/')[0] in ('inputs','downloads_private') for x in pm['files']),'private raw bodies excluded')
print('PASS: PR883–905 bounded disposition/publication identity review'+(' (unsealed semantic check)' if '--unsealed' in sys.argv else '; public and complete manifests and final seal verified'))
