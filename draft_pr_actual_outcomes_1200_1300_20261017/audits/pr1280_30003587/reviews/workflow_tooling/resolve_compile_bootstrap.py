from pathlib import Path
import json,hashlib,datetime,shutil
R=Path(__file__).resolve().parent;A=R.parents[1];T=A.parents[1];D=R/'deployed';P=D/'audits/pr1280_30003587/publication'
p=P/'compile_note.py';s=p.read_text().replace("context=runpy.run_path(str(ROOT/'verification/verify.py'))['load_context'](ROOT.parent)","context=json.loads((ROOT.parent/'CURRENT_PR1280_CONTEXT.json').read_text())")
needle="    compiler=shutil.which('tectonic')"
replacement="""    # First compilation precedes PDF/receipt hashes. Authenticate actual inputs
    # and target gates here; complete document bindings are required by build.
    v=runpy.run_path(str(ROOT/'verification/verify.py'));v['metadata_contract'](context['metadata'])
    anchors=context.get('gate_bindings',{})
    if set(anchors)!={'math_gate_sha256','priority_adjudication_sha256','submitted_snapshot_sha256'}:raise RuntimeError('Explicit compilation gate bindings required')
    for filename,key in [('MATH_GATE.json','math_gate_sha256'),('PRIORITY_ADJUDICATION.json','priority_adjudication_sha256'),('SUBMITTED_SNAPSHOT.json','submitted_snapshot_sha256')]:
        path=ROOT.parent/filename
        if hashlib.sha256(path.read_bytes()).hexdigest()!=anchors[key]:raise RuntimeError('Compilation gate anchor differs '+filename)
        obj=json.loads(path.read_text())
        if filename=='SUBMITTED_SNAPSHOT.json':v['authenticate_snapshot'](ROOT.parent/'submitted',obj)
        else:
            if obj.get('pr')!=1280 or obj.get('problem_id')!=30003587 or obj.get('original_head')!='f5085a4c954f814cde1bc3be0727ff30373aea95' or obj.get('status')!='PASS':raise RuntimeError('Actual compilation PASS gate required '+filename)
            if filename=='PRIORITY_ADJUDICATION.json' and (obj.get('firstness_claim') is not False or obj.get('current_openness_claim') is not False):raise RuntimeError('Compilation priority disclosures required')
    compiler=shutil.which('tectonic')"""
if needle not in s:raise RuntimeError('compile bootstrap marker missing')
s=s.replace(needle,replacement);p.write_text(s)
p=P/'workflow_regression.py';s=p.read_text();s=s.replace("    run=subprocess.run([sys.executable,'-B',str(pub/'compile_note.py')],env=env,capture_output=True,text=True);need(run.returncode==0,run.stderr)","    compilation_context=copy.deepcopy(context);compilation_context.pop('document_bindings');save(audit/'CURRENT_PR1280_CONTEXT.json',compilation_context)\n    run=subprocess.run([sys.executable,'-B',str(pub/'compile_note.py')],env=env,capture_output=True,text=True);need(run.returncode==0,run.stderr)")
p.write_text(s)
for name in ['compile_note.py','workflow_regression.py']:shutil.copyfile(P/name,A/'publication'/name)
r=json.loads((R/'ACTUAL_DEPLOYMENT_RECEIPT.json').read_text());r['at_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();r['compile_bootstrap']='Actual target metadata and bound PASS math/priority/snapshot inputs required; future document_bindings may be omitted until actual compilation/layout. Build requires complete context.'
for entry in r['files']:
 b=Path(entry['path']).read_bytes();entry.update(bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
(R/'ACTUAL_DEPLOYMENT_RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n')
