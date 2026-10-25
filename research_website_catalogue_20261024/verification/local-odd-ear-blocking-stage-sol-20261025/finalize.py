"""Retain an actual read-only preseal result, then seal the complete own payload.

This program deliberately refuses to replace an existing manifest or seal.
It does not render, replay controls, or change any external artifact.
"""
from pathlib import Path
import datetime,hashlib,json,subprocess,sys
O=Path(__file__).resolve().parent
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def binding(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(p,obj):p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
if (O/'MANIFEST.json').exists() or (O/'SEAL.json').exists():raise RuntimeError('final envelope already exists; do not overwrite')
cmd=[sys.executable,'-B',str(O/'verify_stage.py'),'--preseal'];start=now()
r=subprocess.run(cmd,capture_output=True,timeout=90)
(O/'READONLY_PRESEAL.stdout').write_bytes(r.stdout);(O/'READONLY_PRESEAL.stderr').write_bytes(r.stderr)
write(O/'READONLY_PRESEAL.execution.json',{'started_utc':start,'finished_utc':now(),'command':cmd,'exit_code':r.returncode,'stderr_bytes':len(r.stderr),'campaigns_replayed':False})
if r.returncode!=0 or r.stderr:raise RuntimeError('actual read-only preseal failed; exact failure retained')
result=json.loads(r.stdout)
if result['status']!='PASS' or result['checks_passed']!=253:raise RuntimeError('unexpected actual preseal result')
payload=sorted((p for p in O.rglob('*') if p.is_file()),key=lambda p:str(p.relative_to(O)))
manifest={'utc':now(),'kind':'EXACT_OWN_PRIVATE_TWO_RECORD_STAGE_PAYLOAD','record_ids':['23576280','23331258'],'payload_file_count':len(payload),'excludes_only':['MANIFEST.json','SEAL.json'],'files':[{'relative_path':str(p.relative_to(O)),**binding(p)} for p in payload]}
write(O/'MANIFEST.json',manifest)
seal={'utc':now(),'status':'PRIVATE_TWO_RECORD_STAGE_SEALED_FOR_ROOT_REVIEW','record_ids':['23576280','23331258'],'manifest':binding(O/'MANIFEST.json'),'payload_file_count':len(payload),'report':binding(O/'REPORT.md'),'custom_verdict':binding(O/'VERDICT.json'),'read_only_verifier':binding(O/'verify_stage.py'),'actual_preseal_result':binding(O/'READONLY_PRESEAL.stdout'),'private_overlay_files':10,'predicted_integrated_public_files':524,'predicted_index_items':70,'predicted_sitemap_URLs':71,'protected_fresh_baseline_bindings':3863,'current_public516_preserved':True,'actual_target_checks_per_mode':136,'actual_source_controls_per_mode':39,'actual_public_content_rejections':76,'actual_old67_checks':3901,'actual_complete_renderer_executions':134,'independent_editorial_authorship_claimed':False,'root_independent_code_audit_pending':True,'production_integration_authorized':False,'HTTP_browser_native_publication_gates_granted':False,'follow_up':None,'completion_estimate_percent_for_this_private_stage':100,'overall203_complete':False}
write(O/'SEAL.json',seal)
print(json.dumps({'utc':seal['utc'],'manifest':binding(O/'MANIFEST.json'),'seal':binding(O/'SEAL.json'),'payload_file_count':len(payload),'status':seal['status']}))
