#!/usr/bin/env python3
"""Actual subprocess positive and adversarial controls in three interpreter modes."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent

def need(condition,message):
    if not condition: raise ValueError(message)

def run(flags,path=None,extra=None):
    cmd=[sys.executable,'-I','-S','-B',*flags,str(ROOT/'verify.py')]
    if path is not None: cmd+=['--input',str(path)]
    if extra: cmd+=extra
    return subprocess.run(cmd,text=True,capture_output=True,timeout=60)

def main():
    original=json.loads((ROOT/'CLAIMS.json').read_text())
    bad=[]
    for key,value in [('problem_id',10300012),('problem_id',True),('catalog_id','AMR-102-0012'),('rank',1005),('status','claimed_solved'),('turns_used',4),('turns_used',True),('turns_budget',6),('general_solution',True),('novelty_claim',True),('independent_review','accepted'),('claim_ids',original['claim_ids'][:-1]),('verification_scope','proof verified')]:
        x=dict(original); x[key]=value; bad.append(json.dumps(x))
    x=dict(original); x['extra']='unrecognized'; bad.append(json.dumps(x))
    x=dict(original); del x['problem_id']; bad.append(json.dumps(x))
    bad += ['{','[]','null','true','{"x":NaN}',json.dumps(original)[:-1]+',"problem_id":10300011}',json.dumps(original)+'garbage','\ufeff'+json.dumps(original)]
    positive=negative=0
    baseline=None
    with tempfile.TemporaryDirectory(prefix='sublamination-controls-') as td:
        t=Path(td)
        for flags in ([],['-O'],['-OO']):
            p=run(flags)
            need(p.returncode==0 and not p.stderr,'positive subprocess failed')
            if baseline is None: baseline=p.stdout
            need(p.stdout==baseline,'optimization changed positive result')
            positive+=1
            good=t/'good.json'; good.write_text(json.dumps(original))
            p=run(flags,good)
            need(p.returncode==0 and p.stdout==baseline and not p.stderr,'explicit good input failed')
            positive+=1
            for i,body in enumerate(bad):
                f=t/('bad'+str(i)+'.json'); f.write_text(body)
                p=run(flags,f)
                need(p.returncode!=0 and not p.stdout and p.stderr,'bad input accepted or wrong channel')
                negative+=1
            p=run(flags,t/'missing.json')
            need(p.returncode!=0 and not p.stdout and p.stderr,'missing input accepted'); negative+=1
            link=t/'link.json'
            if link.exists() or link.is_symlink(): link.unlink()
            link.symlink_to(good)
            p=run(flags,link)
            need(p.returncode!=0 and not p.stdout and p.stderr,'symlink input accepted'); negative+=1
            p=run(flags,extra=['--unknown-flag'])
            need(p.returncode!=0 and not p.stdout and p.stderr,'unknown flag accepted'); negative+=1
        print(json.dumps({'status':'PASS_ADVERSARIAL_CONTROLS','positive_subprocesses':positive,'rejected_subprocesses':negative,'inner_modes':['normal','-O','-OO'],'author_result':json.loads(baseline)},sort_keys=True))

if __name__=='__main__':
    try: main()
    except (ValueError,OSError,subprocess.SubprocessError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr); sys.exit(2)
