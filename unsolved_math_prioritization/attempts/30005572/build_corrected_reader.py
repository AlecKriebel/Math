#!/usr/bin/env python3
"""Build an explicit packaging-only derivative without touching input bytes."""
import hashlib,json,shutil,sys
from pathlib import Path
src=Path(sys.argv[1]);dst=Path(sys.argv[2]);
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(x,m):
 if not x:raise RuntimeError(m)
need(not dst.exists(),'destination already exists');shutil.copytree(src,dst)
old=[
'Acceptance was reported in the task update; the formal independent report was still being written at freeze.',
'Accepted with the main theorem as reported; formal documentary receipt pending.']
new=[
'The corrected three-file package is formally accepted by the included internal review A16 at exactly this restricted scope.',
'Formally accepted with the corrected three-file package by the included internal review A16.']
rows=[]
for filename in ['PROOF_INDEX.md','PRESERVATION_INVENTORY.json']:
 p=dst/filename;txt=p.read_text();need(txt.count(old[0])==1 and txt.count(old[1])==2,'unexpected status occurrences');
 for a,b in zip(old,new):txt=txt.replace(a,b)
 p.write_text(txt);rows.append({'path':filename,'input_sha256':h(src/filename),'output_sha256':h(p),'input_bytes':(src/filename).stat().st_size,'output_bytes':p.stat().st_size,'change':'Replace the three stale preliminary P25-P27 acceptance-status statements with the existing formal A16 receipt; mathematical scope sentences retained.'})
p=dst/'README.md';txt=p.read_text();txt+='\n## Packaging status correction\n\nThis separately preserved derivative corrects stale preliminary acceptance-status wording for P25–P27 in the index and preservation inventory. The completed formal internal report A16 was already included and pins all three proof texts. All proofs, qualifications, internal review reports, checks, and source metadata are unchanged from the input reader. See the [explicit change mapping](PACKAGING_CORRECTIONS.json). VALIDATION.json and REPLAY_RESULTS.json retain the original assembly records; independent packaging verification is supplied with this derivative.\n';p.write_text(txt);rows.append({'path':'README.md','input_sha256':h(src/'README.md'),'output_sha256':h(p),'input_bytes':(src/'README.md').stat().st_size,'output_bytes':p.stat().st_size,'change':'Add a packaging-only provenance note, correction mapping link, and attribution of historical assembly validation.'})
receipt={'schema_version':1,'date_utc':'2026-10-14','kind':'Packaging-only status correction; zero new mathematical passes','input_reader_manifest_sha256':h(src/'FILE_MANIFEST.json'),'input_reader_sha256sums_sha256':h(src/'SHA256SUMS'),'finding':'Preliminary P25-P27 documentary-status sentences remained stale after A16 had been completed and included. There was no missing formal acceptance and no mathematical claim was enlarged.','changes':rows,'metadata_regenerated':['FILE_MANIFEST.json','SHA256SUMS'],'retained_unchanged':['READER.md','CORRECTIONS.md','REFERENCES.md','REFERENCES.json','SANITIZATION_INVENTORY.json','VALIDATION.json','REPLAY_RESULTS.json','all 34 proof and addendum files','both mandatory mathematical qualifications','all 22 internal review reports','all 21 check scripts and expected outputs'],'proof_transformation_count_from_accepted_originals':5,'additional_proof_transformation_count':0,'original_research_and_input_reader_modified':False,'full_problem_status':'UNSOLVED','novelty_claim':False}
(dst/'PACKAGING_CORRECTIONS.json').write_text(json.dumps(receipt,indent=2)+'\n')
manifest=json.loads((src/'FILE_MANIFEST.json').read_text());manifest['edition']+='; packaging-status corrected derivative';manifest['packaging_derivative_of_manifest_sha256']=h(src/'FILE_MANIFEST.json');files=[]
for p in sorted(dst.rglob('*')):
 if p.is_file() and p.name not in ['FILE_MANIFEST.json','SHA256SUMS']:files.append({'path':str(p.relative_to(dst)),'bytes':p.stat().st_size,'sha256':h(p)})
manifest['files']=files;manifest['file_count_excluding_manifest_and_checksums']=len(files);(dst/'FILE_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
lines=[h(p)+'  '+str(p.relative_to(dst)) for p in sorted(dst.rglob('*')) if p.is_file() and p.name!='SHA256SUMS'];(dst/'SHA256SUMS').write_text('\n'.join(lines)+'\n')
print(json.dumps({'manifest_sha256':h(dst/'FILE_MANIFEST.json'),'checksums_sha256':h(dst/'SHA256SUMS'),'files':len(lines)+1,'changed_existing_files':len(rows)+2,'new_files':1},indent=2))
