"""Verify this review and originals without file/network/Git writes."""
from pathlib import Path
from io import BytesIO,StringIO
import hashlib,json,zipfile,sys,argparse,runpy,contextlib,builtins,io
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent;P=E.parents[1];S=P/'sources'
ap=argparse.ArgumentParser();ap.add_argument('--rerun-controls',action='store_true');a=ap.parse_args()
def need(v,x):
 if not v:raise RuntimeError(x)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rows_ok(rows):
 for x in rows:
  p=Path(x['path']);p=p if p.is_absolute() else E/p
  need(p.stat().st_size==x['bytes'] and digest(p)==x['sha256'],'binding:'+str(p))
seal=json.loads((E/'SEAL.json').read_text());need(digest(E/'MANIFEST.json')==seal['manifest_sha256'],'scope_seal');mf=json.loads((E/'MANIFEST.json').read_text());rows_ok(mf['files']);rows_ok(json.loads((E/'CACHE_MANIFEST.json').read_text())['files']);rows_ok(json.loads((E/'ORIGINAL_BINDINGS.json').read_text())['files'])
ss=json.loads((S/'SOURCE_SEAL.json').read_text());need(digest(S/'SOURCE_MANIFEST.json')==ss['manifest_sha256'],'final_source_seal');sm=json.loads((S/'SOURCE_MANIFEST.json').read_text())
for x in sm['files']:need((S/x['path']).stat().st_size==x['bytes'] and digest(S/x['path'])==x['sha256'],'source:'+x['path'])
ready=json.loads((S/'SOURCE_READY.json').read_text());api=json.loads((S/'record.raw.json').read_text());latest=json.loads((S/'latest.raw.json').read_text());versions=json.loads((S/'versions.raw.json').read_text());need(str(api['id'])==str(latest['id'])=='23146753' and versions['hits']['total']==1,'record_latest_versions');need(ready['version']==api['metadata']['version']=='1.0','API_edition')
for item,obj in zip(ready['all_assets'],api['files']):
 b=Path(item['path']).read_bytes();need(item['original_api_file_object']==obj and len(b)==item['bytes']==obj['size'] and hashlib.md5(b).hexdigest()==item['md5'] and obj['checksum']=='md5:'+item['md5'] and hashlib.sha256(b).hexdigest()==item['sha256'],'whole_original_asset')
transport=json.loads((S/'api-and-file-receipts.json').read_text());need(len(transport)==5 and all(x['status']==200 and x['headers'] for x in transport),'actual_five_transports')
for x in transport:b=Path(x['path']).read_bytes();need(len(b)==x['bytes'] and hashlib.sha256(b).hexdigest()==x['sha256'],'transport_payload')
inventory=json.loads((S/'archive-members.json').read_text());need(len(inventory['members'])==13 and len(inventory['archive_containers'])==1,'archive_complete_inventory')
with zipfile.ZipFile(S/'mtp2-edge-closure-verification.zip') as z:
 actual=[x for x in z.infolist() if not x.is_dir()];need(len(actual)==13 and z.testzip() is None,'actual_ZIP_CRC')
 for x in actual:
  b=z.read(x);matches=[v for v in inventory['members'] if v['member']==x.filename];need(len(matches)==1,'member_identity');m=matches[0];need(len(b)==m['bytes'] and hashlib.sha256(b).hexdigest()==m['sha256'] and m['CRC32']==f'{x.CRC:08x}' and Path(m['extracted_path']).read_bytes()==b,'member_CRC_hash_original_extraction')
need((S/'mtp2-edge-closure-note.pdf').read_bytes()==(S/'published-source/output/pdf/mtp2_edge_closure.pdf').read_bytes(),'embedded_selected_reader_identity')
rerun=[]
if a.rerun_controls:
 rbw=Path.write_bytes;rtw=Path.write_text;ro=builtins.open;rio=io.open;captured={}
 def capture(p,text,*args,**kwargs):
  need(p.resolve().is_relative_to(E),'own_control_write_scope');captured[p.name]=text;return len(text)
 def blockbytes(*args,**kwargs):raise RuntimeError('unexpected_bytes_write')
 def guarded(file,mode='r',*args,**kwargs):
  need(not any(x in mode for x in 'wax+'),'unexpected_file_write');return ro(file,mode,*args,**kwargs)
 Path.write_text=capture;Path.write_bytes=blockbytes;builtins.open=guarded;io.open=guarded
 try:
  for script,out in [('independent_controls.py','INDEPENDENT_CONTROLS.json'),('facial_support_controls.py','FACIAL_SUPPORT_CONTROLS.json')]:
   with contextlib.redirect_stdout(StringIO()):runpy.run_path(str(E/script),run_name='__main__')
   got=json.loads(captured[out]);want=json.loads((E/out).read_text());got.pop('utc');want.pop('utc');need(got==want,'recomputed_own_control:'+script);rerun.append(script)
 finally:Path.write_bytes=rbw;Path.write_text=rtw;builtins.open=ro;io.open=rio
print(json.dumps({'status':'PASS','scope_owned':len(mf['files']),'scope_cache':len(json.loads((E/'CACHE_MANIFEST.json').read_text())['files']),'protected_originals':len(json.loads((E/'ORIGINAL_BINDINGS.json').read_text())['files']),'source_manifest_bindings':len(sm['files']),'archive_members_CRC_compared':13,'own_controls_recomputed_without_writes':rerun,'source_or_primary_programs_executed':False,'network_or_Git_operations':False}))
