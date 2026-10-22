#!/usr/bin/env python3
"""Seal only reviewer02 artifacts and verify unchanged frozen inputs; no providers."""
from pathlib import Path
import hashlib,json,datetime
Q=Path(__file__).resolve().parent;A=Q.parents[1];P=A.parents[1]/'private/pr0399_package_adversary_02'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def entry(p,root):return {'path':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':sha(p)}
def need(v,m):
 if not v:raise RuntimeError(m)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
expected=json.loads((A/'publication_operations_preparation/MANIFEST.json').read_text())
need(sha(A/'publication_operations_preparation/MANIFEST.json')=='ad5c2339d915d8fe33f4ffbdab2d528d9258a394e70a66437d2b615ab70a3e9d','operations seal changed')
checks=[]
for e in expected['files']+expected['immutable_inputs']:
 actual=entry(A/e['path'],A);need(actual==e,'input changed '+e['path']);checks.append({'before_sealed_expected':e,'after_observed':actual,'unchanged':True})
lead=A/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json';need(sha(lead)=='af763826f5e22bb64887496eada7e4aaa9c944faf45db3a0c93386b9833fbe39','root lead changed')
(Q/'FINAL_INPUT_PRESERVATION.json').write_text(json.dumps({'timestamp_utc':now,'operations42_and_immutable26_unchanged':checks,'root_lead':entry(lead,A),'release_manifest':entry(A/'preprint/publication/RELEASE_FILES.json',A),'scope':'Before is the independently checked immutable preparation seal; after is actual final observation. No live template outside399 is included. No mutation claimed or performed.'},indent=2)+'\n')
(Q/'PRIVATE_CUSTODY_MANIFEST.json').write_text(json.dumps({'timestamp_utc':now,'root':str(P),'scope':'Ignored private original-source download, source-page/manuscript renders, extracted bundle and scoped control outputs; no third-party bodies in authored public review.','files':[entry(p,P)for p in sorted(P.rglob('*'))if p.is_file()]},indent=2)+'\n')
exclude={'AUTHORED_FILE_MANIFEST.json','AUTHORED_FILE_MANIFEST.sha256'}
files=[entry(p,Q)for p in sorted(Q.rglob('*'))if p.is_file()and p.name not in exclude]
v={'schema':1,'sealed_at_utc':now,'review_completion_percent':100,'verdict':'REPAIR_REQUIRED','scope':'All reviewer02 authored public artifacts. Only manifest and checksum excluded; private custody independently listed. No canonical/provider/Git state mutations or publication authorization.','files':files}
manifest=Q/'AUTHORED_FILE_MANIFEST.json';manifest.write_text(json.dumps(v,indent=2)+'\n');(Q/'AUTHORED_FILE_MANIFEST.sha256').write_text(sha(manifest)+'  AUTHORED_FILE_MANIFEST.json\n')
for e in files:need(entry(Q/e['path'],Q)==e,'own seal entry mismatch')
print(json.dumps({'timestamp_utc':now,'artifacts':len(files),'manifest_sha256':sha(manifest),'verdict':'REPAIR_REQUIRED','review_completion_percent':100}))
