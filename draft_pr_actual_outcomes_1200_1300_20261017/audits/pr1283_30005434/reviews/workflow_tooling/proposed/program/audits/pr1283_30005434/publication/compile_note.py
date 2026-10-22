#!/usr/bin/env python3
"""Compile saved current source and record actual time separately from epoch."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,runpy
ROOT=Path(__file__).resolve().parent

def main():
    context=json.loads((ROOT.parent/'CURRENT_PR1283_CONTEXT.json').read_text())
    if context.get('schema')!='math-pr1283-current-context-v1' or context.get('pr')!=1283 or context.get('problem_id')!=30005434 or context.get('original_head')!='4624244af725a80a2b7faf111f6b1ca62aaefe37' or context.get('original_branch')!='dot/semibrace-30005434-complete-existence-20261011' or context.get('original_body_sha256')!='d60b38cf473a47e035624677092725f307da72628f935f80147622a28aef6f93' or context.get('edition_mode') not in {'preserve_submitted','documented_correction'}:raise RuntimeError('Explicit current compilation context required')
    epoch=context.get('source_date_epoch')
    if epoch!='1792195200':raise RuntimeError('Explicit SOURCE_DATE_EPOCH required')
    # First compilation precedes PDF/receipt hashes. Authenticate actual inputs
    # and target gates here; complete document bindings are required by build.
    v=runpy.run_path(str(ROOT/'verification/verify.py'));v['metadata_contract'](context['metadata'])
    anchors=context.get('gate_bindings',{})
    if set(anchors)!={'math_gate_sha256','priority_adjudication_sha256','submitted_snapshot_sha256'}:raise RuntimeError('Explicit compilation gate bindings required')
    for filename,key in [('MATH_GATE.json','math_gate_sha256'),('PRIORITY_ADJUDICATION.json','priority_adjudication_sha256'),('SUBMITTED_SNAPSHOT.json','submitted_snapshot_sha256')]:
        path=ROOT.parent/filename
        if hashlib.sha256(path.read_bytes()).hexdigest()!=anchors[key]:raise RuntimeError('Compilation gate anchor differs '+filename)
        obj=json.loads(path.read_text());v['fixture_boundary'](ROOT.parent,obj)
        if filename=='SUBMITTED_SNAPSHOT.json':v['authenticate_snapshot'](ROOT.parent/'submitted',obj)
        else:
            if obj.get('pr')!=1283 or obj.get('problem_id')!=30005434 or obj.get('original_head')!='4624244af725a80a2b7faf111f6b1ca62aaefe37' or obj.get('status')!='PASS':raise RuntimeError('Actual compilation PASS gate required '+filename)
            if filename=='PRIORITY_ADJUDICATION.json' and (obj.get('firstness_claim') is not False or obj.get('current_openness_claim') is not False or obj.get('novelty_clearance') is not False or obj.get('mathematical_gate_sha256')!=anchors['math_gate_sha256']):raise RuntimeError('Compilation priority disclosures required')
    v['authenticate_source_bindings'](ROOT.parent,ROOT.parent,context)
    compiler=shutil.which('tectonic')
    if not compiler:raise RuntimeError('Tectonic unavailable; preserve source and obtain an actual compile receipt')
    source=ROOT/'manuscript/main.tex';before=hashlib.sha256(source.read_bytes()).hexdigest()
    version=subprocess.check_output([compiler,'--version'],text=True).strip()
    out=ROOT/'output/pdf';out.mkdir(parents=True,exist_ok=True)
    scratch=ROOT.parent/'reviews/workflow_tooling/_local';scratch.mkdir(parents=True,exist_ok=True)
    texcache=Path('/Users/alec/Documents/Math/draft_pr_actual_outcomes_1200_1300_20261017/audits/pr1274_2307072/reviews/workflow_tooling/_local/texcache')
    env=dict(os.environ,XDG_CACHE_HOME=str(texcache),SOURCE_DATE_EPOCH=epoch)
    result=subprocess.run([compiler,'--only-cached','--keep-logs','--outdir',str(out),str(source)],capture_output=True,text=True,env=env)
    (scratch/'COMPILE_STDOUT.txt').write_text(result.stdout);(scratch/'COMPILE_STDERR.txt').write_text(result.stderr)
    if result.returncode:raise RuntimeError(result.stderr)
    if hashlib.sha256(source.read_bytes()).hexdigest()!=before:raise RuntimeError('Source changed during compilation')
    receipt={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'compiler':str(Path(compiler).resolve()),'version':version,'compiler_sha256':hashlib.sha256(Path(compiler).read_bytes()).hexdigest(),'source_sha256':before,'pdf_sha256':hashlib.sha256((out/'main.pdf').read_bytes()).hexdigest(),'returncode':result.returncode,'source_date_epoch':epoch,'source_date_epoch_meaning':'Chosen reproducible build stamp only; at_utc is actual receipt time. No completion/publication time or byte determinism is inferred from the stamp.','reproduction_scope':'Current source compiled successfully. Exact PDF bytes require matching compiler/cache/environment.'}
    (ROOT/'COMPILE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
