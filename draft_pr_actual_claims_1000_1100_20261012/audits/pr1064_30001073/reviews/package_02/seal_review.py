from pathlib import Path
import hashlib,json,datetime
W=Path(__file__).resolve().parent;R=W.parents[1]
def require(c,m):
    if not c:raise ValueError(m)
def pin(p,root):
    b=p.read_bytes();return {'path':str(p.relative_to(root)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
inputs=json.loads((W/'INPUT_CUSTODY.json').read_text())
for x in inputs['candidate']+inputs['original_files']:
    y=pin(R/x['path'],R);require(y==x,'end input changed '+x['path'])
private=[pin(p,W) for p in sorted((W/'private').rglob('*')) if p.is_file()]
(W/'PRIVATE_EVIDENCE_PINS.json').write_text(json.dumps({'scope':'Identities only; private source extracts and renders remain excluded from distributed review outputs.','records':private},indent=2)+'\n')
outputs=[pin(p,W) for p in sorted(W.rglob('*')) if p.is_file() and not p.relative_to(W).as_posix().startswith(('private/','tmp/','__pycache__/')) and p.name not in ['OUTPUT_PINS.json','SEAL.json']]
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
out={'sealed_utc':utc,'scope':'All authored terminal whole02 review outputs except this pin file and separate SEAL; third-party/source-derived private evidence and scratch excluded. No candidate readiness authorization.','completed_percent':100,'publication_ready':False,'issues_updated':False,'zero_actionable_findings':False,'counts':{'P0':0,'P1':0,'P2':0,'P3':1},'entries':outputs}
(W/'OUTPUT_PINS.json').write_text(json.dumps(out,indent=2)+'\n')
seal={'utc':utc,'scope':'Independent separate seal of complete whole02 review. Does not hash itself.','output_pins':pin(W/'OUTPUT_PINS.json',W),'report':pin(W/'REPORT.md',W),'verdict':pin(W/'VERDICT.json',W),'candidate_inputs_unchanged':len(inputs['candidate']),'original_inputs_unchanged':len(inputs['original_files']),'counts':out['counts'],'publication_ready':False,'issues_updated':False,'needs_repair_and_new_fresh_whole_review':True,'ascending_hold_after_pr':1032}
(W/'SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
for x in outputs:require(pin(W/x['path'],W)==x,'output changed')
require(pin(W/'OUTPUT_PINS.json',W)==seal['output_pins'],'pin seal changed')
print(json.dumps({'pass':True,'outputs':len(outputs),'private_evidence_records':len(private),'output_pins_sha256':seal['output_pins']['sha256'],'report_sha256':seal['report']['sha256'],'verdict_sha256':seal['verdict']['sha256'],'counts':out['counts']},indent=2))
