#!/usr/bin/env python3
"""Independent static artifact/correction inspection, no receipt-path recursion."""
import collections,datetime,hashlib,json,pathlib,stat,sys,zipfile
F=pathlib.Path(__file__).resolve().parent;A=F.parents[1];P=A/'publication';R=F/'_local/extracted'
def need(c,m):
 if not c: raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(b):return {'bytes':len(b),'sha256':sha(b)}
def rowcheck(b,r,size='bytes'):need(bind(b)=={'bytes':r[size],'sha256':r['sha256']},'binding mismatch')
def safe(s):
 p=pathlib.PurePosixPath(s);need(isinstance(s,str) and s and not p.is_absolute() and '..' not in p.parts and str(p)==s and '\\' not in s,'unsafe path');return s
def main():
 build=json.loads((P/'BUILD_RECEIPT.json').read_text());context=json.loads((A/'CURRENT_PR1280_CONTEXT.json').read_text());snap=json.loads((A/'SUBMITTED_SNAPSHOT.json').read_text())
 for name,expected in [('manuscript/main.tex','c9e6a6c1661a0a235644bd10e642a7d57a253c7d40c52e1a794ea29869697545'),('Diagonal_Actions_Strong_Approximate_Innerness_Note_v1.0.pdf','42285ef1e7f0f7f7fa98b5879b2f9b46000609db2a50ff3e28ab37465ce684f7'),('Diagonal_Actions_Strong_Approximate_Innerness_Verification_v1.0.zip','f7aa63de23c1acfcc4b0d6d43576356a2934ec323f281349ae8949b184bf170b')]:need(sha((P/name).read_bytes())==expected,'actual artifact mismatch '+name)
 R.mkdir(parents=True,exist_ok=True)
 with zipfile.ZipFile(P/build['verification_zip']['path']) as z:
  entries=z.infolist();names=[x.filename for x in entries];need(len(names)==245 and len(set(names))==245,'ZIP duplicates/count');need(len({x.casefold() for x in names})==245,'case collision')
  for x in entries:
   safe(x.filename);need(not x.is_dir() and not stat.S_ISLNK(x.external_attr>>16),'nonregular ZIP member');target=R/x.filename;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(x))
 manifest=json.loads((R/'MANIFEST.json').read_text());need(sha((R/'MANIFEST.json').read_bytes())==build['verification_anchors']['manifest'],'outside manifest mismatch')
 need({r['path'] for r in manifest['files']}==set(names)-{'MANIFEST.json'} and len(manifest['files'])==244,'root inventory mismatch')
 for e in manifest['files']:rowcheck((R/safe(e['path'])).read_bytes(),e)
 for n,key in [('CURRENT_PR1280_CONTEXT.json','context'),('SUBMITTED_SNAPSHOT.json','snapshot')]:need(sha((R/'provenance'/n).read_bytes())==build['verification_anchors'][key],'outside provenance mismatch')
 need((R/'provenance/CURRENT_PR1280_CONTEXT.json').read_bytes()==(A/'CURRENT_PR1280_CONTEXT.json').read_bytes(),'context bytes differ')
 for e in snap['files']:
  n=pathlib.Path(e['path']).name;b=(A/'submitted'/n).read_bytes();rowcheck(b,e);need((R/'original_submitted'/n).read_bytes()==b,'ZIP original differs');need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==e['git_blob_sha1'],'Git blob mismatch')
 need(len(snap['files'])==9 and snap['parents']==['a72180cf68ed6c9c54360cfd61b7a6567f5a0a5f'],'snapshot identity')
 correction=json.loads((A/'CURRENT_EDITION_CORRECTION.json').read_text());changes=[]
 for folder,key,zipfolder in [('submitted','original_files','original_submitted'),('current_edition','current_files','current_edition')]:
  need(set(correction[key])=={pathlib.Path(e['path']).name for e in snap['files']},'nine-file correction map')
  for n,r in correction[key].items():
   b=(A/folder/n).read_bytes();rowcheck(b,r);need((R/zipfolder/n).read_bytes()==b,'edition ZIP mismatch')
  ed=json.loads((A/folder/'MANIFEST.json').read_text());need(len(ed['files'])==8,'eight nonself edition files')
  for n,r in ed['files'].items():rowcheck((A/folder/n).read_bytes(),r)
 m=json.loads((A/'current_edition/EDITORIAL_CHANGE_MAP.json').read_text());need(m['historical_20261011_editorial_map']==json.loads((A/'submitted/EDITORIAL_CHANGE_MAP.json').read_text()),'historical map changed')
 acceptance=json.loads((A/'current_edition/ACCEPTANCE.json').read_text());need(acceptance['historical_20261011_acceptance']==json.loads((A/'submitted/ACCEPTANCE.json').read_text()),'historical acceptance changed')
 for n,r in m['current_original_markdown'].items():
  old=(A/'submitted'/n).read_bytes();new=(A/'current_edition'/n).read_bytes();rowcheck(old,r);rowcheck(new,m['current_outputs'][n]);oldpos=newpos=0;items=[x for x in m['current_byte_changes'] if x['path']==n]
  for e in items:
   s,t=e['original_byte_range'];u,v=e['current_byte_range'];need(s>=oldpos and u>=newpos and t>=s and v>=u,'unordered span');need(old[oldpos:s]==new[newpos:u],'unchanged gap differs '+n);rowcheck(old[s:t],e['original_fragment']);rowcheck(new[u:v],e['current_fragment']);oldpos=t;newpos=v
  need(old[oldpos:]==new[newpos:],'unchanged suffix differs '+n);changes.append({'path':n,'changed_spans':len(items),'unchanged_gaps_checked':len(items)+1})
 schemas={('files','relative_path','bytes'),('members','path','bytes'),('authored_files','path','bytes'),('files','path','bytes')};families=[]
 for reg in context['authored_freezes']:
  need((reg['entries_key'],reg['path_key'],reg['size_key']) in schemas,'unexpected actual schema');raw=safe(reg['path']);base=safe(reg['base']);b=(R/raw).read_bytes();need(sha(b)==reg['sha256'],'family anchor');obj=json.loads(b);rows=obj[reg['entries_key']];seen=set()
  for row in rows:
   rel=safe(row[reg['path_key']]);need(rel not in seen,'duplicate family member');seen.add(rel);rowcheck((R/base/rel).read_bytes(),row,reg['size_key'])
  families.append({'path':raw,'entries':len(rows),'schema':[reg[k] for k in ['entries_key','path_key','size_key']]})
 need(len(families)==19 and len(context['portable_files'])==217,'actual family/portable counts')
 for e in context['portable_files']:rowcheck((R/safe(e['path'])).read_bytes(),e)
 need(not any(x.startswith('_local/') or '/_local/' in x or x.endswith(('.html','.ps')) for x in names),'private source body in ZIP')
 metadata=json.loads((P/'zenodo-deposit.json').read_text());need(metadata['metadata']==context['metadata'] and len(metadata['metadata'])==11,'metadata exact11');need(metadata['files']==[{'path':build[k]['path']} for k in ['pdf','verification_zip']],'two artifacts')
 for reg in context['authored_freezes'][-2:]:
  need(reg['sha256'] in {'49cbb2fb193320b719bf0732e3b93e82eee99cdff9c55cc755c7109772c1a0c7','9aa1c0aa8544eb0896e0d226015ce7a6b08fbba322d61de9b95a41cc2869a295'},'revision families')
 return {'status':'PASS','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'artifact_bindings':{k:build[k] for k in ['pdf','verification_zip']},'anchors_used':build['verification_anchors'],'zip_members':len(names),'authenticated_root_members':len(manifest['files']),'registered_families':families,'portable_records':len(context['portable_files']),'correction_spans_and_gaps':changes,'metadata_fields':sorted(metadata['metadata']),'scope':'Independent static byte/membership/schema/correction inspection. Literal registered member keys only; absolute input/source inventories were not followed as members. Missing historical inputs are explicitly not reconstructed.'}
if __name__=='__main__':
 result=main();(F/'ARTIFACT_INSPECTION.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in {'registered_families','artifact_bindings'}},indent=2))
