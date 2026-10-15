#!/usr/bin/env python3
"""Seal only the explicit public review allowlist; never stage or publish."""
from pathlib import Path
import datetime,hashlib,json
HERE=Path(__file__).resolve().parent
PUBLIC=[
 '.gitignore','AUDIT.md','RESULT.json','RESEARCH_LOG.md','INDEPENDENT_DERIVATION.md',
 'PRIORITY_AND_SOURCE_CHECK.md','CODE_AND_RESULTS_REVIEW.md','authenticate.py',
 'fetch_sources.py','fetch_neighbors.py','independent_controls.py','replay.py',
 'fresh_guard_controls.py','live_check.py','rebuild_archive.py','seal.py',
 'AUTHENTICATION_start.json','AUTHENTICATION_end.json','ARCHIVE_REBUILD_RECEIPT.json',
 'INDEPENDENT_CONTROL_RESULTS.json','SOURCE_ACCESS_RECEIPTS.json','SOURCE_NEIGHBOR_ACCESS.json',
 'SOURCE_AND_CODE_RECEIPT.json','REPLAY_normal.json','REPLAY_O.json','REPLAY_OO.json',
 'REPLAY_env2.json','REPLAY_RECEIPT.json','PACKAGE_GUARD_REPLAY.json','PACKET_GUARD_REPLAY.json',
 'FRESH_GUARD_RESULTS.json','PDF_REPRODUCTION_RECEIPT.json','LIVE_start_RECEIPT.json',
 'LIVE_end_RECEIPT.json','METADATA_LOCAL_CHECK.json','METADATA_BINDING_RECEIPT.json',
]
def main():
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 result=json.loads((HERE/'RESULT.json').read_text())
 if result['required_issues'] or result['optional_issues'] or result['clean_for_publication'] is not True:raise RuntimeError('result not clean')
 actual={p.name for p in HERE.iterdir() if p.is_file() and p.name!='MANIFEST.json'}
 if actual!=set(PUBLIC):raise RuntimeError('public file mismatch '+repr(actual^set(PUBLIC)))
 records={}
 for name in PUBLIC:
  p=HERE/name;b=p.read_bytes()
  if p.suffix=='.json':json.loads(b,parse_constant=lambda s:(_ for _ in ()).throw(RuntimeError('nonfinite JSON')))
  records[name]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 manifest={'schema_version':1,'utc':now,'reviewer':'full_package_02','pr':908,
  'problem_id':'30006191','reviewed_freeze_sha256':result['freeze_sha256'],
  'public_allowlist':PUBLIC+['MANIFEST.json'],'manifest_self_excluded':True,
  'intentional_public_files':records,'raw_source_distribution':False,
  'excluded':['MANIFEST.json self-fingerprint','private_sources/**','tmp/**','all raw PDFs/source text/renders/screenshots/search and API datasets'],
  'publication_policy':'Stage only the explicit public allowlist, never recursively stage this review folder. No Git or publication action is performed by this script.'}
 encoded=(json.dumps(manifest,indent=2)+'\n').encode();(HERE/'MANIFEST.json').write_bytes(encoded)
 for name,r in records.items():
  b=(HERE/name).read_bytes()
  if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']:raise RuntimeError('sealed bytes changed '+name)
 print(json.dumps({'public_artifacts_excluding_manifest':len(records),'manifest_sha256':hashlib.sha256(encoded).hexdigest(),'clean_for_publication':True}))
if __name__=='__main__':main()
