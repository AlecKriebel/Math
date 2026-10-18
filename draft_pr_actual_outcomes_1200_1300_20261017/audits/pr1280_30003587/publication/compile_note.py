#!/usr/bin/env python3
"""Compile saved current source and record actual time separately from epoch."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess,runpy
ROOT=Path(__file__).resolve().parent

def main():
    context=runpy.run_path(str(ROOT/'verification/verify.py'))['load_context'](ROOT.parent)
    if context.get('schema')!='math-pr1280-current-context-v1' or context.get('pr')!=1280 or context.get('problem_id')!=30003587 or context.get('original_head')!='f5085a4c954f814cde1bc3be0727ff30373aea95' or context.get('original_branch')!='publish-diagonal-30003587-20261011' or context.get('original_body_sha256')!='6ab00d803d8a28f0ac3450dc33c69752561482d2f4bb37e29024707c2ef6c213' or context.get('edition_mode')!='preserve_submitted':raise RuntimeError('Explicit current compilation context required')
    epoch=context.get('source_date_epoch')
    if epoch!='1792195200':raise RuntimeError('Explicit SOURCE_DATE_EPOCH required')
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
