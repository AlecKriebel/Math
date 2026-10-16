import os, json, hashlib, zipfile, subprocess, pathlib, stat
R=pathlib.Path(__file__).resolve().parent
A=R.parent.parent
P=A/'publication'
sha=lambda x:hashlib.sha256(x).hexdigest()
repo=A.parents[2]
freeze={str(p.relative_to(P)):{'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in P.iterdir() if p.is_file()}
z=zipfile.ZipFile(P/'verification_package.zip')
entries=z.infolist(); prefix='seshadri_counterexample_verification/'
assert len(entries)==102 and len({i.filename for i in entries})==102
payload={}
for i in entries:
 assert i.filename.startswith(prefix)
 name=i.filename[len(prefix):]
 assert not i.is_dir() and not stat.S_ISLNK(i.external_attr>>16)
 pp=pathlib.PurePosixPath(name)
 assert name==pp.as_posix() and not pp.is_absolute() and '..' not in pp.parts
 assert not any(p in {'.cache','sources','scratch','qa','.secrets'} or '.private' in p for p in pp.parts)
 payload[name]=z.read(i)
man=json.loads(payload['MANIFEST.json'])
assert set(man['files'])|{'MANIFEST.json'}==set(payload)
for n,rec in man['files'].items(): assert rec=={'bytes':len(payload[n]),'sha256':sha(payload[n])}
assert payload['MANIFEST.json']==(P/'PACKAGE_MANIFEST.json').read_bytes()
reg=json.loads(payload['SEALS.json']); assert reg==man['nested_seals'] and len(reg)==7
# Separate nested parser, not import of package integrity implementation.
nested=[]
for seal in reg:
 sn=seal['path']; assert sha(payload[sn])==seal['sha256']; base=pathlib.PurePosixPath(sn).parent
 if seal['kind']=='sha256sum':
  records=[(str(base/n),h,None) for h,n in (ln.split('  ',1) for ln in payload[sn].decode().splitlines())]
 elif seal['kind']=='json-files':
  records=[(str(base/r['path']),r['sha256'],r['bytes']) for r in json.loads(payload[sn])['files']]
 else:
  records=[]
  for group,b in [('publication_safe_author_files',base.parent),('publication_safe_audit_files',base)]:
   records += [(str(b/r['path']),r['sha256'],r['bytes']) for r in json.loads(payload[sn])[group]]
 assert len({r[0] for r in records})==len(records)
 for n,h,s in records:
  assert sha(payload[n])==h and (s is None or s==len(payload[n]))
 nested.append({'seal':sn,'entries':len(records),'status':'PASS'})
assert sum(x['entries'] for x in nested)==83
ss=payload['ORIGINAL_SNAPSHOT.json']; assert sha(ss)=='b74088ad62046937bc4835f761a500d7a8f9a39ac4eb0da9e3dcb03143adb6cf'
snap=json.loads(ss); originals=[]
for f in snap['files']:
 n=f['path']; b=payload['original/'+n]
 got=subprocess.run(['git','show',snap['head']+':'+n],cwd=repo,capture_output=True,check=True).stdout
 assert got==b==(A/'original'/n).read_bytes() and sha(b)==f['sha256'] and len(b)==f['size']
 originals.append({'path':n,'git_head':snap['head'],'bytes':len(b),'sha256':sha(b),'git_blob_sha1':subprocess.check_output(['git','rev-parse',snap['head']+':'+n],cwd=repo,text=True).strip(),'status':'PASS'})
assert len(originals)==18
out=R/'.cache'/'extracted'; out.mkdir(parents=True,exist_ok=False)
for n,b in payload.items():
 p=out/n; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b)
result={'status':'PASS','observed_main_head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=repo,text=True).strip(),'freeze':freeze,'zip_members':len(entries),'outer_payloads':len(man['files']),'nested':nested,'nested_entries':sum(x['entries'] for x in nested),'originals':originals,'snapshot_sha256':sha(ss),'extraction_root':str(out),'all_authored_archive_paths_guarded':True}
(R/'FREEZE_AND_INVENTORY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'freeze','originals','nested'}},indent=2))
