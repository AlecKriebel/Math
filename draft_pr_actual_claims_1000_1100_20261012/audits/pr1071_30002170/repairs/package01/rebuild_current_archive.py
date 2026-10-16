from pathlib import Path
import hashlib,json,zipfile,datetime
r=Path('/Users/alec/Documents/Math/draft_pr_actual_claims_1000_1100_20261012/audits/pr1071_30002170');p=r/'NEWpreprint_v1_0';e=r/'repairs/package01'
old=json.loads((e/'before/PACKAGE_MANIFEST.json').read_text());names={z['path'] for z in old['members']};names.remove('CITATION.cff');names.update(['CITATION.txt','CURRENT_STATUS.json','scripts/package_paths.py','REPAIR_NOTES.md','WHOLE01_COPY_EXCLUSIONS.json']);names.update(z['package_copy'] for z in json.loads((p/'INPUT_COPY_MAP.json').read_text())['copies']);members=[]
for n in sorted(names):
 q=p/n
 if not q.is_file() or q.is_symlink():raise RuntimeError('unsafe '+n)
 members.append({'path':n,'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()})
old['members']=members;old['policy']+='; repaired regular/nonsymlink manifest bootstrap; current plain scholarly citation; safe unchanged whole01 output copies and exact historical before-byte resolution.'
(p/'PACKAGE_MANIFEST.json').write_text(json.dumps(old,indent=2)+'\n')
az=p/'PR1071_preprint_v1_0_support.zip'
with zipfile.ZipFile(az,'w',compression=zipfile.ZIP_STORED,allowZip64=False) as z:
 for n in sorted(names|{'PACKAGE_MANIFEST.json'}):
  inf=zipfile.ZipInfo(n,date_time=(2026,10,14,0,0,0));inf.create_system=3;inf.external_attr=0o100644<<16;inf.compress_type=zipfile.ZIP_STORED;z.writestr(inf,(p/n).read_bytes())
sha=hashlib.sha256(az.read_bytes()).hexdigest();(p/(az.name+'.sha256')).write_text(sha+'  '+az.name+'\n')
b=json.loads((e/'before/UPLOAD_BINDINGS.json').read_text());b['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();b['archive'].update(bytes=az.stat().st_size,sha256=sha);b['manifest_sha256']=hashlib.sha256((p/'PACKAGE_MANIFEST.json').read_bytes()).hexdigest();b['self_reference']+=' CURRENT_STATUS.json governs repaired review state; original STATUS is historical.';(p/'UPLOAD_BINDINGS.json').write_text(json.dumps(b,indent=2)+'\n')
print(json.dumps({'members':len(members)+1,'archive_bytes':az.stat().st_size,'archive_sha256':sha}))
