#!/usr/bin/env python3
"""Replays exact arithmetic and meaningful inventory/semantic negative controls."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

def need(ok,msg):
    if not ok:
        raise RuntimeError(msg)

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    need(len(sys.argv)==4,'usage: test_packet.py ROOT MANIFEST_SHA CHECKER_SHA')
    root=Path(sys.argv[1]).absolute()
    manifest_pin,checker_pin=sys.argv[2:]
    need(sha(root/'MANIFEST.json')==manifest_pin,'pre-execution manifest pin')
    need(sha(root/'verify_packet.py')==checker_pin,'pre-execution checker pin')
    need(not root.is_symlink(),'symlink packet')
    results=[]
    def run(label,target,ok=True,opt=False,mp=manifest_pin,cp=checker_pin,cwd=None,env=None):
        cmd=[sys.executable,'-I','-S','-B']+(['-O'] if opt else [])
        cmd += [str(target/'verify_packet.py'),str(target),mp,cp]
        r=subprocess.run(cmd,capture_output=True,text=True,cwd=cwd,env=env,timeout=30)
        need((r.returncode==0)==ok,label+': unexpected exit '+r.stdout+r.stderr)
        results.append({'control':label,'accepted':r.returncode==0,'expected_acceptance':ok,
                        'result':'PASS'})
    run('normal',root)
    run('optimized',root,opt=True)
    with tempfile.TemporaryDirectory(prefix='structural controls ',dir=root.parent) as td:
        base=Path(td)
        moved=base/'relocated packet with spaces'
        shutil.copytree(root,moved)
        hostile=base/'hostile cwd'
        hostile.mkdir()
        (hostile/'json.py').write_text('raise RuntimeError("hostile import")\n')
        env=dict(os.environ,PYTHONPATH=str(hostile))
        run('relocation spaces hostile cwd and PYTHONPATH',moved,cwd=hostile,env=env)
        run('optimized relocation',moved,opt=True,cwd=hostile,env=env)
        def variant(label,mutate,repin=False):
            v=base/label
            shutil.copytree(root,v)
            mutate(v)
            mp=manifest_pin
            if repin:
                m=json.loads((v/'MANIFEST.json').read_text())
                m['files']={n:sha(v/n) for n in m['files']}
                (v/'MANIFEST.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
                mp=sha(v/'MANIFEST.json')
            run(label,v,ok=False,mp=mp)
        variant('extra member',lambda v:(v/'unexpected.txt').write_text('x'))
        variant('missing member',lambda v:(v/'ARITHMETIC_DATA.json').unlink())
        variant('changed source metadata',lambda v:(v/'RETRIEVAL_LEDGER.json').write_text('[]\n'))
        variant('changed checker',lambda v:(v/'verify_packet.py').write_text((v/'verify_packet.py').read_text()+'\n# changed\n'))
        def symlink(v):
            f=v/'ARITHMETIC_DATA.json'
            f.unlink()
            f.symlink_to(root/'ARITHMETIC_DATA.json')
        variant('symlink member',symlink)
        def change(v,key,value):
            f=v/'ARITHMETIC_DATA.json'
            d=json.loads(f.read_text());d[key]=value;f.write_text(json.dumps(d)+'\n')
        variant('untrusted arithmetic mutation',lambda v:change(v,'polynomial_ascending',[9,-8,2,0,1,-2,1]))
        variant('semantic arithmetic after deliberate repin',lambda v:change(v,'polynomial_ascending',[9,-8,2,0,1,-2,1]),True)
        variant('wrong target after deliberate repin',lambda v:change(v,'target',30002365),True)
        variant('historical firstness overclaim after deliberate repin',lambda v:change(v,'historical_firstness_certified',True),True)
        def wrong_rank(v):
            f=v/'ARITHMETIC_DATA.json';d=json.loads(f.read_text());d['expected']['centered_rank']=3;f.write_text(json.dumps(d)+'\n')
        variant('rank conclusion mutation after deliberate repin',wrong_rank,True)
        def frozen(v):
            f=v/'INITIAL_STRATEGY_FROZEN.md';f.write_text(f.read_text()+'\nChanged initial record\n')
        variant('changed independent freeze after deliberate repin',frozen,True)
        def unavailable(v):
            f=v/'RETRIEVAL_LEDGER.json';d=json.loads(f.read_text())
            for r in d:
                if r['id']=='ribet1980':r['status']='failed'
            f.write_text(json.dumps(d)+'\n')
        variant('necessary primary access mutation after deliberate repin',unavailable,True)
    print(json.dumps({'result':'PASS','controls':results,'count':len(results),
                      'interpretation':'Finite integrity and consistency controls; no geometric theorem formalization.'},indent=2))

if __name__=='__main__':
    main()
