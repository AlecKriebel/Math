"""Own completed-source custody check; reading judgment is explicitly first-party, not automated."""
from pathlib import Path
import ast,datetime as dt,hashlib,json,os,stat,sys
P=Path(__file__).absolute().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def need(v,m):
 if not v:raise ValueError(m)
def ref(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode))
checks=[]
for d in sorted(P.glob('actual_*_capture')):
 if d.name=='actual_completed_source_check_capture':continue
 c=json.loads((d/'CAPTURE.json').read_bytes());need(c['actual_execution'] is True and c['completed'] is True and c['exit_code']==0 and type(c['pid']) is int and c['source_unchanged'] is True,'genuine completed own source child')
 need(sha((d/'PRELAUNCH_SOURCE.py').read_bytes())==c['source_sha256'],'whole prelaunch source')
 for n in ('stdout','stderr'):
  b=(d/c[n]['path']).read_bytes();need(len(b)==c[n]['bytes'] and sha(b)==c[n]['sha256'],'whole streams')
 checks.append(dict(capture=ref(d/'CAPTURE.json'),actual_child=c['pid']))
r=json.loads((P/'FINAL_ARTICLE_EXTRACTION.json').read_bytes());f=Path(r['source']['path']);b=f.read_bytes();need(len(b)==r['source']['bytes']==596169 and sha(b)==r['source']['sha256']=='478c879b6fea91b1aa17b0ea90172c10e01432b90e11c0873881f864151fdafc' and stat.S_IMODE(f.stat().st_mode)==420,'exact unchanged supplied source fullmode')
e=Path(r['private_text']['path']).read_bytes();need(len(e)==r['private_text']['bytes'] and sha(e)==r['private_text']['sha256'] and e.count(b'\f')==30,'entire privately retained extraction stream')
for n in ('COMPONENT_RENDER.json','TOPOLOGY_PAGE6_RENDER.json','FINAL_ARTICLE_RENDER.json'):
 z=json.loads((P/n).read_bytes())
 for v in z['rows']:
  b=Path(v['private_png']).read_bytes();need(len(b)==v.get('png_bytes',v.get('bytes')) and sha(b)==v.get('png_sha256',v.get('sha256')),'exact private selected rendering')
for v in json.loads((P/'COMPONENT_READ_LEDGER.json').read_bytes())['rows']:
 for n in ('pdf','txt'):
  x=v[n];b=Path(x['path']).read_bytes();need(len(b)==x['bytes'] and sha(b)==x['sha256'] and stat.S_IMODE(Path(x['path']).stat().st_mode)==x['full_mode'],'unchanged reused primary source')
for f in P.glob('*.py'):ast.parse(f.read_text(),filename=str(f))
need(not (P/'SOURCE_MANIFEST.json').exists(),'no fabricated ROOT closure');need((P/'.gitignore').read_bytes()==b'/private_cache/\n','private corpus exclusion')
verdict=json.loads((P/'VERDICT.json').read_bytes());need(verdict['complete_final_article_read'] is True and verdict['named_source_hold_retirement_recommended'] is True and verdict['new_mathematical_independence_credit']==0 and verdict['ROOT_read_or_approval_claimed'] is False,'exact qualified judgment')
out=dict(schema='pr18-own-completed-access-source-custody/v1',actual_pid=os.getpid(),actual_argv=sys.argv,utc=dt.datetime.now(dt.timezone.utc).isoformat(),status='PASS_SOURCE_CUSTODY_ONLY',captures=checks,whole_final_source=ref(Path(r['source']['path'])),private_extraction_bytes=len(e),private_extraction_sha256=sha(e),complete_final_pages=30,all_python_sources_AST_parsed=True,root_helpers_executed=False,root_source_manifest_absent=True,mathematical_or_priority_acceptance=False)
b=(json.dumps(out,indent=2)+'\n').encode()
with (P/'COMPLETED_SOURCE_CHECKS.json').open('xb') as q:q.write(b)
print(json.dumps(dict(status=out['status'],actual_pid=os.getpid(),result_sha256=sha(b),completed_captures=len(checks))))
