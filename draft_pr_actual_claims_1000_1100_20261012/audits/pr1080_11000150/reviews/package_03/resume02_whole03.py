#!/usr/bin/env python3
"""Distinct continuation preserving the initial failed ENOSPC receipt and driver."""
from pathlib import Path
import json,sys,hashlib,shutil,subprocess,time,datetime,ast,importlib.util
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1];DELIVERY=BASE/'preprint_v1_0';SCRATCH=HERE/'scratch'
KIT=SCRATCH/'clean_check/verification_kit';RECEIPTS=HERE/'RESUME02_COMMAND_RECEIPTS.jsonl'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(cmd,cwd=HERE,expected=0,label=None):
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
    r=subprocess.run([str(x) for x in cmd],cwd=cwd,capture_output=True,text=True,timeout=180)
    row={'utc':start,'label':label,'argv':[str(x) for x in cmd],'cwd':str(cwd),'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'elapsed_seconds':time.monotonic()-t,'expected':expected,'free_bytes_after':shutil.disk_usage(HERE).free}
    with RECEIPTS.open('a') as f:f.write(json.dumps(row)+'\n')
    if not (r.returncode==0 if expected==0 else r.returncode!=0):raise RuntimeError(json.dumps(row))
    return row

for opt in [False,True]:
    prefix=[sys.executable,'-I','-B']+(['-O'] if opt else [])
    for script in ['verify.py','run_checks.py','fault_checks.py']:
        run(prefix+[KIT/script],KIT)
    output=SCRATCH/('resume-O.zip' if opt else 'resume.zip')
    run(prefix+[KIT/'build_archive.py','--output',output],KIT)
    run(['cmp',DELIVERY/'verification_kit.zip',output],KIT)
    run(prefix+[KIT/'verify.py','--require-binding','--binding',DELIVERY/'EXTERNAL_BINDING.json','--pdf',DELIVERY/'preprint.pdf','--archive',DELIVERY/'verification_kit.zip'],KIT)
    output.unlink()
    for repeat in range(3):
        for fault in ['word_conjugation','parity','erasing']:
            r=run(prefix+[KIT/'run_checks.py','--fault',fault],KIT,'nonzero',f'direct-inner-diagnostic-{repeat}')
            if 'portable reviewer guard' not in r['stderr']:raise RuntimeError('Unrelated inner fault failure')
    r=run(prefix+[HERE/'independent_checks03.py'])
    (HERE/('INDEPENDENT_RESULTS_O.json' if opt else 'INDEPENDENT_RESULTS.json')).write_text(r['stdout'])
    for fault in ['omit_conjugates','wrong_parity']:
        r=run(prefix+[HERE/'independent_checks03.py',fault],expected='nonzero')
        if 'Independent' not in r['stderr']:raise RuntimeError('Independent fault failed for unrelated reason')

run([sys.executable,'-I','-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',DELIVERY/'deposit_metadata.json'])
(SCRATCH/'compiled').mkdir(exist_ok=True)
run(['tectonic','--outdir',SCRATCH/'compiled',KIT/'preprint.tex'],KIT)
run(['pdfinfo',DELIVERY/'preprint.pdf'])
run(['pdftoppm','-r','95','-png',DELIVERY/'preprint.pdf',SCRATCH/'page'])

spec=importlib.util.spec_from_file_location('whole03_full_output',KIT/'run_checks.py');mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
math=[]
for kind,(relative,expected_hash) in mod.PROGRAMS.items():
    source=KIT/relative
    if sha(source)!=expected_hash:raise RuntimeError('source hash')
    work=SCRATCH/('full-'+kind);work.mkdir();copied=work/source.name;shutil.copyfile(source,copied)
    if kind=='surface':
        d=work/'inputs/git';d.mkdir(parents=True)
        for p in (KIT/'originals/submitted').iterdir():shutil.copyfile(p,d/p.name)
    ns={'__name__':'whole03_full_output_capture','__file__':str(copied)}
    exec(compile(mod.adapt(kind,source.read_text(),None),str(copied),'exec'),ns)
    if kind in ['word','priority']:local=ns['main']()
    if kind=='priority':
        tree=ast.parse(source.read_text());main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
        expr=next(n.value for n in main.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='result' for t in n.targets))
        actual=eval(compile(ast.Expression(expr),str(copied),'eval'),ns,dict(local,verified=[]))
        expected=json.loads((source.parent/'CONTROL_RESULTS.json').read_text());exclusions=['frozen_inputs_reverified']
    else:
        name='WORD_CONTROL_RESULTS.json' if kind=='word' else 'SANITY_RESULTS.json'
        actual=json.loads((work/name).read_text());expected=json.loads((source.parent/name).read_text());exclusions=['timestamp'] if kind=='surface' else []
    for key in exclusions:actual.pop(key,None);expected.pop(key,None)
    if actual!=expected:raise RuntimeError('Full mathematical comparison '+kind)
    math.append({'kind':kind,'source_sha256':expected_hash,'excluded_fields':exclusions,'full_mathematical_output':actual,'matches_preserved':True})
(HERE/'FULL_MATHEMATICAL_OUTPUT_COMPARISON.json').write_text(json.dumps(math,indent=2)+'\n')
print(json.dumps({'status':'PASS','commands':sum(1 for _ in RECEIPTS.open())}))
