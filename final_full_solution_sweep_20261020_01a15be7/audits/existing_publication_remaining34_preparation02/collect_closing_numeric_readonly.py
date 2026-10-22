"""Dated closing numeric43-column CLI reads only; no action-data adoption."""
from pathlib import Path
import json,hashlib,subprocess,gzip,datetime,os,base64
O=Path(__file__).resolve().parent
ns={'__file__':str(O/'source/bootstrap.py'),'__name__':'_closing_captured_boot'};exec(compile((O/'source/bootstrap.py').read_bytes(),ns['__file__'],'exec',optimize=0),ns)
SOURCE='5f2a18359d2006783b20650584c2f4560b915f2907c6129b1db4c49488f224c8';M,verify=ns['load_verified'](SOURCE);C=M['ops_core'];N=M['numeric'];cfg=json.loads((O/'RUNTIME_CONFIGURATION.json').read_bytes());client=cfg['programs']['gws'];p=Path(client['path']);assert len(p.read_bytes())==client['bytes']and C.sha(p.read_bytes())==client['sha256'];captures=[];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
class Reads:
 def gws(self,parts,params,body=None):
  assert parts in [['get'],['values','batchGetByDataFilter']]
  cmd=[client['path'],'sheets','spreadsheets',*parts,'--params',json.dumps(params)]
  if body is not None:cmd+=['--json',json.dumps(body)]
  r=subprocess.run(cmd,capture_output=True,timeout=120);captures.append({'command':cmd,'returncode':r.returncode,'stdout_base64':base64.b64encode(r.stdout).decode(),'stderr_base64':base64.b64encode(r.stderr).decode()});assert r.returncode==0;return C.strict_json(r.stdout)
numeric=N.observe(Reads());old=json.loads(gzip.decompress((O/'private/numeric_complete.json.gz').read_bytes()));sameprefix=C.typed_equal(numeric['values'][:len(old['values'])],old['values'])and C.typed_equal(numeric['formulas'][:len(old['formulas'])],old['formulas']);same_metadata=C.typed_equal(old['metadata'],numeric['metadata']);plan=json.loads((O/'PROPOSAL.json').read_bytes());gate=json.loads(gzip.decompress((O/'private/REVIEWED_GATE_PROPOSED.json.gz').read_bytes()));allowed={(d['pr'],d['kind'],d['body_sha256'])for d in gate['semantic_decisions']};leads=[]
for num,row in enumerate(numeric['values'][len(old['values']):],len(old['values'])+1):
 for i in plan['items']:
  hits=C.recursive_identity_hits(row,i)
  if hits:leads.append({'row_number':num,'target_pr':i['pr'],'full_row_canonical_sha256':C.sha(C.canonical(row)),'matched':hits,'dated_old_gate_contains':(i['pr'],'sheet',C.sha(C.canonical(row)))in allowed,'individual_root_independent_adoption':False})
body={'started':start,'finished':datetime.datetime.now(datetime.timezone.utc).isoformat(),'numeric':numeric,'original_raw_cli_transports':captures,'dated_only':True,'action_authority':False};raw=(json.dumps(body,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode();compressed=gzip.compress(raw,mtime=0);assert sum(p.lstat().st_blocks*512 for p in[O,*O.rglob('*')])+len(compressed)+65536<=10*1024*1024;assert os.statvfs(O).f_bavail*os.statvfs(O).f_frsize-len(compressed)>150*1024*1024;q=O/'private/CLOSING_NUMERIC_COMPLETE_AND_RAW.json.gz';assert not q.exists();q.write_bytes(compressed);assert gzip.decompress(q.read_bytes())==raw
out={'started':start,'finished':body['finished'],'rows':len(numeric['values']),'old_rows':len(old['values']),'old_full43_prefix_typed_unchanged':sameprefix,'full_metadata_unchanged':same_metadata,'numeric_gid':1254632077,'columns':43,'full_allocated_rows':N.target(numeric['metadata'])['gridProperties']['rowCount'],'raw_complete':{'path':str(q.relative_to(O)),'sha256':C.sha(raw),'bytes':len(raw)},'new_matching_pairs':leads,'new_matching_pairs_require_fresh_individual_adoption':True,'this_is_not_complete_current_owned_local_public_gate':True,'dated_only':True,'action_authority':False};(O/'CLOSING_NUMERIC_READONLY.json').write_text(json.dumps(out,ensure_ascii=False,sort_keys=True,indent=2)+'\n');verify();print(json.dumps({k:out[k]for k in['rows','old_rows','old_full43_prefix_typed_unchanged','full_metadata_unchanged','dated_only']}))
