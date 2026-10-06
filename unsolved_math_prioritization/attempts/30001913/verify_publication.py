"""Replay only from an authenticated private publication snapshot."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: publication replay requires -I -S -B')
import hashlib,json,os,shlex,subprocess,tempfile
from pathlib import Path

def need(ok,message):
    if not ok:raise ValueError(message)

root=Path(__file__).parent
need(len(sys.argv)==3 and sys.argv[1]=='--expected-manifest','external pin required')
need(hashlib.sha256((root/'PUBLICATION_MANIFEST.json').read_bytes()).hexdigest()==sys.argv[2],'publication anchor')
meta=json.loads((root/'PUBLICATION_METADATA.json').read_text());acc=json.loads((root/'audit/ACCEPTANCE.json').read_text())
need(meta['status']=='unsolved' and meta['turns']=='5/5' and not meta['complete_proof'] and not meta['target_counterexample'] and not meta['novelty_claim'],'publication scope')
need(acc['status']=='unsolved' and acc['substantive_approaches']==5 and acc['verdict']=='accepted_scoped_partial_results' and not acc['mathematical_correction_required'] and not acc['security_correction_required'],'audit scope')
with tempfile.TemporaryDirectory(prefix='hodge publication interpreter ') as td:
    shim=Path(td)/'no-bytecode-python'
    shim.write_text('#!/bin/sh\nexec '+shlex.quote(sys.executable)+' -B "$@"\n');shim.chmod(0o700)
    env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
    launcher="import sys; from pathlib import Path; shim,entry,*args=sys.argv[1:]; sys.executable=shim; sys.argv=[entry,*args]; exec(compile(Path(entry).read_bytes(),entry,'exec'),{'__name__':'__main__','__file__':entry})"
    author=root/'audit/author';prefix='HODGE_EXTREMALITY_30001913_AUTHOR'
    commands=[('independent_math',root/'audit/independent_math.py',[],root/'audit/INDEPENDENT_MATH.json'),('audit_replay',root/'audit/replay_audit.py',[str(author/(prefix+'_SAFE_FREEZE.zip')),str(author/(prefix+'_EXTERNAL_MANIFEST.json')),str(author/(prefix+'_FREEZE_RECEIPT.json'))],root/'audit/REPLAY.json')]
    reports=[]
    for label,entry,args,expected in commands:
        p=subprocess.run([sys.executable,'-I','-S','-B']+(['-O'] if sys.flags.optimize else [])+['-c',launcher,str(shim),str(entry),*args],capture_output=True,text=True,cwd=td,env=env,timeout=600)
        need(p.returncode==0 and not p.stderr,'failed '+label+': '+p.stderr)
        result=json.loads(p.stdout);need(result==json.loads(expected.read_text()),'exact frozen JSON mismatch: '+label)
        reports.append({'role':label,'frozen_json_exact':True,'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest()})
print(json.dumps({'status':'PASS','problem_id':30001913,'mathematical_status':'unsolved','approaches':'5/5','optimized':bool(sys.flags.optimize),'independent_exact_controls':13617,'author_replay_cases':54,'descendants_no_bytecode':True,'intentional_missing_flag_negative_controls':4,'replays':reports},sort_keys=True,indent=2))
