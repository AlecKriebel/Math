from pathlib import Path,PurePosixPath
import json,zipfile,hashlib,datetime,re
E=Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7');O=E/'reviews/range0344_0396_adversary';P=E/'private/pr0344_0396_review'
rows=[];faults=[]
for n in [344,356,359,364,367]:
 d=P/f'pr{n:04d}_public';r=json.loads((d/'record.json').read_text());rv=json.loads((E/f'PR{n:04d}_PUBLICATION_VERIFICATION.json').read_text());f=next(d.glob('*.zip'));z=zipfile.ZipFile(f)
 names=z.namelist();assert len(names)==len(set(names));assert all(not PurePosixPath(x).is_absolute() and '..' not in PurePosixPath(x).parts for x in names)
 assert z.testzip() is None
 manifest='verification/MANIFEST.json' if n==367 else next(x for x in names if x.count('/')==1 and (x.endswith('/MANIFEST.json') or x.endswith('/FILE_MANIFEST.json')))
 mf=json.loads(z.read(manifest));parent=str(PurePosixPath(manifest).parent)+'/'
 decl=mf['files'];decl=[dict(path=k,**v) for k,v in decl.items()] if isinstance(decl,dict) else decl
 entries=[]
 for q in decl:
  path=parent+q['path'];b=z.read(path)
  entries.append({'path':path,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'length_matches':len(b)==q['bytes'],'sha256_matches':hashlib.sha256(b).hexdigest()==q['sha256']})
 declared=set(x['path'] for x in entries);scope=set(x for x in names if x.startswith(parent));extra=sorted(set(names)-scope)
 checks={'no_duplicate_members':len(names)==len(set(names)),'all_crc_pass':z.testzip() is None,'exact_manifest_scope_members':scope==declared|{manifest},'all_declared_sizes_hashes':all(x['length_matches'] and x['sha256_matches'] for x in entries),'record_title_matches_root':r['metadata']['title']==rv['title'],'record_doi_matches_root':r['doi']==rv['doi'],'record_published':r['state']=='done','exact_record_file_names':set(x['key'] for x in r['files'])==set(x['name'] for x in rv['files']),'exact_archive_members_root':names==next(x['members'] for x in rv['files'] if x['name']==f.name)}
 for q in rv['files']:
  b=(d/q['name']).read_bytes();checks['root_payload_'+q['name']]=len(b)==q['size'] and hashlib.sha256(b).hexdigest()==q['sha256'] and 'md5:'+hashlib.md5(b).hexdigest()==q['checksum']
 if n==367:checks['separate_tex_exactly_one']=extra==['fixed_generator_classification.tex']
 else:checks['manifest_scope_is_entire_archive']=not extra
 for k,v in checks.items():
  if not v:faults.append({'pr':n,'check':k})
 rows.append({'pr':n,'record':r['id'],'manifest_path':manifest,'manifest_sha256':hashlib.sha256(z.read(manifest)).hexdigest(),'declared_payload_count':len(decl),'manifest_scope_member_count':len(scope),'archive_member_count':len(names),'separate_files':[{'path':x,'bytes':len(z.read(x)),'sha256':hashlib.sha256(z.read(x)).hexdigest()} for x in extra],'checks':checks,'payloads':entries})
(O/'publication_payload_checks.json').write_text(json.dumps({'checked_at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Manifest and identity coverage only. No historic proof or priority re-audit.','publications':rows,'faults':faults},indent=2)+'\n')
print(json.dumps({'publications':[{'pr':r['pr'],'declared_payloads':r['declared_payload_count'],'manifest_scope':r['manifest_scope_member_count'],'archive_members':r['archive_member_count'],'separate':r['separate_files']} for r in rows],'faults':faults},indent=2))
