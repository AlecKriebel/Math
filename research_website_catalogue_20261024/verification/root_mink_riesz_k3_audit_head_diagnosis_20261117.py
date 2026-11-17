from pathlib import Path
from datetime import datetime,timezone
import copy,hashlib,json,re
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
S=P/'verification/mink-riesz-k3-stage-sol-20261117'
O=P/'verification/root-mink-riesz-k3-audit-head-diagnosis-20261117.json'
assert not O.exists()
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
assert sha(S/'FINAL.json')=='2aa8bb250f77212d60903f69f64390f86a8ce7544218453b2d169c957d8e588f'
assert sha(S/'OWNED_MANIFEST.json')=='cd6b884ff5efce7c5873307cdc7bf308b72c801c3ba5868660ba261dcc22c8dc'
A=P/'verification/mink-riesz-k3-stage-audit-sol-20261117/audit_private.py'
assert sha(A)=='39fe5f73831676dca34930af27c4e1dc6315556e1f2cbedbbe2317a4353a34d8'
def edit(old,rows):
 parts=[];cursor=0
 for r in sorted(rows,key=lambda r:(r['start_byte'],r['end_byte'])):
  a,b=r['start_byte'],r['end_byte'];assert cursor<=a<=b<=len(old)
  assert old[a:b]==r['old_UTF8'].encode()
  parts += [old[cursor:a],r['new_UTF8'].encode()];cursor=b
 return b''.join(parts)+old[cursor:]
observations=[]
for x in json.loads((S/'HEAD_ACTIVATION.json').read_text())['pages']:
 writer=P/('verification/'+x['family']+'-editorial-sol-20261117')
 model=json.loads((writer/'page-model.json').read_text());old=(writer/'head.html').read_bytes()
 page=S/'candidate-public/research'/model['deployment_proposal']['slug']/'index.html'
 actual=re.search(rb'<head>.*?</head>\n',page.read_bytes(),re.S).group()
 style=b'<link rel="stylesheet" href="/research/research.css">\n';script=b'<script type="application/ld+json">'
 assert old.count(style)==old.count(script)==1
 rows=copy.deepcopy(x['spans']);slot=[r for r in rows if r['reason']=='canonical and OG URL'];assert len(slot)==1
 assert slot[0]['start_byte']==slot[0]['end_byte']==old.index(style)
 assert edit(old,rows)==actual
 slot[0]['start_byte']=slot[0]['end_byte']=old.index(script)
 alternative=edit(old,rows);assert alternative!=actual
 observations.append({'family':x['family'],'actual_canonical_insertion_anchor':'Before the unchanged shared stylesheet','actual_original_head_byte':old.index(style),'auditor_assumed_original_head_byte':old.index(script),'position_delta_bytes':old.index(script)-old.index(style),'entire_actual_head_equals_all_declared_closed_spans':True,'all_other_spans_identical_in_reader_variant':True,'reader_variant_differs_only_in_canonical_OG_insertion_location':True,'actual_head_SHA256':hashlib.sha256(actual).hexdigest(),'reader_variant_head_SHA256':hashlib.sha256(alternative).hexdigest()})
result={'UTC':datetime.now(timezone.utc).isoformat(),'status':'AUDIT_HEAD_ANCHOR_ASSUMPTION_MISMATCH_CONFIRMED','observations':observations,'original_audit_exit_remains':1,'stage_builder_exit_remains':0,'stage_payload_change_or_builder_retry':False,'audit_reader_import_execution_AST_compile_or_retry':False,'new_scope':'Standalone passive comparison of saved HEAD buffers and exact reviewable spans only','root_reading':'Entire stage435linebuilder and HEAD_ACTIVATION; actual independent reader255–325 and complete literal1200Bstderr','disposition':'Freeze old failed audit with separate truthful closing custody; create distinct continuation with shared-stylesheet anchor derived from actual accepted head/approved spans. One corrected passive audit after full saved-source reading; no producer/payload repair.','follow_up':None,'publication_authority':False}
O.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'three_pages_checked':len(observations),'receipt_SHA256':sha(O)}))
