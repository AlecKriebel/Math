#!/usr/bin/env python3
"""Compile saved current source and record actual time separately from epoch."""
from pathlib import Path
import datetime,hashlib,json,os,shutil,subprocess
ROOT=Path(__file__).resolve().parent

def main():
    context=json.loads((ROOT.parent/'CURRENT_PR1268_CONTEXT.json').read_text())
    if context.get('schema')!='math-pr1268-current-context-v1' or context.get('pr')!=1268 or context.get('problem_id')!=10900050 or context.get('original_head')!='cecd7da6e8b5bb84b4294e169d940189b269a956':raise RuntimeError('Explicit current compilation context required')
    epoch=context.get('source_date_epoch')
    if not isinstance(epoch,str) or not epoch.isdigit():raise RuntimeError('Explicit SOURCE_DATE_EPOCH required')
    compiler=shutil.which('tectonic')
    if not compiler:raise RuntimeError('Tectonic unavailable; preserve source and obtain an actual compile receipt')
    source=ROOT/'manuscript/main.tex';before=hashlib.sha256(source.read_bytes()).hexdigest()
    version=subprocess.check_output([compiler,'--version'],text=True).strip()
    out=ROOT/'output/pdf';out.mkdir(parents=True,exist_ok=True)
    scratch=ROOT.parent/'_local/texcache';scratch.mkdir(parents=True,exist_ok=True)
    env=dict(os.environ,XDG_CACHE_HOME=str(scratch),SOURCE_DATE_EPOCH=epoch)
    result=subprocess.run([compiler,'--keep-logs','--outdir',str(out),str(source)],capture_output=True,text=True,env=env)
    (ROOT/'COMPILE_STDOUT.txt').write_text(result.stdout);(ROOT/'COMPILE_STDERR.txt').write_text(result.stderr)
    if result.returncode:raise RuntimeError(result.stderr)
    if hashlib.sha256(source.read_bytes()).hexdigest()!=before:raise RuntimeError('Source changed during compilation')
    receipt={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'compiler':str(Path(compiler).resolve()),'version':version,'compiler_sha256':hashlib.sha256(Path(compiler).read_bytes()).hexdigest(),'source_sha256':before,'pdf_sha256':hashlib.sha256((out/'main.pdf').read_bytes()).hexdigest(),'returncode':result.returncode,'source_date_epoch':epoch,'source_date_epoch_meaning':'Chosen reproducible build stamp only; at_utc is actual receipt time. No completion/publication time or byte determinism is inferred from the stamp.','reproduction_scope':'Current source compiled successfully. Exact PDF bytes require matching compiler/cache/environment.'}
    (ROOT/'COMPILE_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
