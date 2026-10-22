from pathlib import Path
import importlib.util, json, zipfile, io, hashlib, tempfile, shutil, subprocess, sys, stat
SAFE=Path(__file__).absolute().parent
spec=importlib.util.spec_from_file_location('audit',SAFE/'verify_audit.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
members=a.author_check(SAFE);ext=a.read_json((SAFE/a.AUTHOR_EXTERNAL).read_bytes());result=a.replay(SAFE)
checks=[]
def rejection(label,fn):
 try: fn()
 except (a.Rejected,ValueError,KeyError,TypeError,zipfile.BadZipFile) as e: checks.append({'control':label,'result':'REJECTED','reason':str(e)})
 else: raise RuntimeError('negative accepted: '+label)
def archive(change):
 b=io.BytesIO()
 with zipfile.ZipFile(b,'w',zipfile.ZIP_DEFLATED) as z:
  for n,v in members.items():
   if change=='missing' and n=='SOURCE_METADATA.json': continue
   if change=='path' and n=='REPORT.md': n='../REPORT.md'
   if change=='changed_report' and n=='REPORT.md':v+=b'changed\n'
   if change=='symlink' and n=='REPORT.md':
    i=zipfile.ZipInfo(n);i.create_system=3;i.external_attr=(stat.S_IFLNK|0o777)<<16;z.writestr(i,v)
   else: z.writestr(n,v)
  if change=='extra':z.writestr('extra.txt',b'extra')
  if change=='duplicate':z.writestr('REPORT.md',members['REPORT.md'])
 return b.getvalue()
for mode in ('missing','path','changed_report','symlink','extra','duplicate'):
 rejection('independent_zip_'+mode,lambda m=mode:a.inspect_archive(archive(m),ext))
b=(SAFE/a.AUTHOR_ZIP).read_bytes()
rejection('author_archive_bit_flip',lambda:a.pinned(b[:-1]+bytes([b[-1]^1]),a.AUTHOR_PINS[a.AUTHOR_ZIP],'archive'))
rejection('author_external_manifest_rewrite',lambda:a.pinned((SAFE/a.AUTHOR_EXTERNAL).read_bytes()+b' ',a.AUTHOR_PINS[a.AUTHOR_EXTERNAL],'external'))
rejection('duplicate_json_parser',lambda:a.read_json(b'{"schema_version":1,"schema_version":1}'))
rejection('nonfinite_json_parser',lambda:a.read_json(b'{"v":NaN}'))
# Demonstrate that an internal hash manifest alone is not a trust anchor.
with tempfile.TemporaryDirectory() as tmp:
 p=Path(tmp)
 for n,b in members.items():(p/n).write_bytes(b)
 v=a.read_json((p/'SOURCE_METADATA.json').read_bytes());v['sources'][0]['sha256']='0'*64
 (p/'SOURCE_METADATA.json').write_text(json.dumps(v,indent=2)+'\n')
 m=a.read_json((p/'MANIFEST.json').read_bytes());b=(p/'SOURCE_METADATA.json').read_bytes()
 m['files']['SOURCE_METADATA.json']={'bytes':len(b),'sha256':a.sha(b)}
 (p/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
 run=subprocess.run([sys.executable,'-B',str(p/'verify_release.py')],capture_output=True,text=True)
 if run.returncode: raise RuntimeError('unexpected internal-scope result')
 b=io.BytesIO()
 with zipfile.ZipFile(b,'w') as z:
  for n in members:z.write(p/n,n)
 rejection('rehashed_source_forgery_external_anchor',lambda:a.pinned(b.getvalue(),a.AUTHOR_PINS[a.AUTHOR_ZIP],'archive'))
 result['internal_manifest_scope_probe']={'internal_only_checker_accepts_rehashed_source_metadata':True,'exact_external_archive_pin_rejects':True,'classification':'Expected integrity boundary, not a mathematical or packaging correction. Never use an attacker-replaced manifest as its own trust anchor.'}
result['independent_negative_controls']=checks
result['author_archive_members']=len(members)
result['source_pdfs_or_corpus_in_archive']=False
result['result']='PASS_EXACT_BYTES_REPLAYS_AND_NEGATIVE_CONTROLS'
print(json.dumps(result,indent=2))
