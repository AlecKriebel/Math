#!/usr/bin/env python3
"""Exercise the frozen interface in clean folders and against real corruptions."""
from pathlib import Path
import copy, datetime, hashlib, json, shutil, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parent
AUDIT=ROOT.parent
SOURCE=AUDIT/'verification_research'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    data=json.loads((SOURCE/'specimen.json').read_text())
    data['ordinary_five_witness']=dict(zip(['a','b','c','d','e','a1','a2','b1','d1','e1','e2'],[1,5,3,1,5,3,4,2,4,2,3]))
    (SOURCE/'specimen.json').write_text(json.dumps(data,indent=2)+'\n')
    receipts=[];controls=[]
    local=AUDIT/'_local';local.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=local,prefix='interface-') as tmp:
        folder=Path(tmp)
        shutil.copyfile(SOURCE/'verify.py',folder/'verify.py')
        for flags in [[],['-O'],['-OO']]:
            (folder/'specimen.json').write_text(json.dumps(data,indent=2)+'\n')
            run=subprocess.run([sys.executable,'-B',*flags,str(folder/'verify.py')],capture_output=True,text=True)
            if run.returncode:raise RuntimeError(run.stderr)
            receipts.append({'flags':flags,'status':'PASS','result_sha256':sha(folder/'results.json')})
        if len({r['result_sha256'] for r in receipts})!=1:raise RuntimeError('nondeterministic optimized modes')
        shutil.copyfile(folder/'results.json',SOURCE/'results.json')
        for case in ['edge_removed','list_changed','list_cardinality','invalid_witness','wrong_claim_count','boolean_label']:
            broken=copy.deepcopy(data)
            if case=='edge_removed':broken['edges'].pop()
            elif case=='list_changed':broken['lists']['a1']=[1,2,3,4,5]
            elif case=='list_cardinality':broken['lists']['a'].pop()
            elif case=='invalid_witness':broken['ordinary_five_witness']['b']=broken['ordinary_five_witness']['a']
            elif case=='wrong_claim_count':broken['expected_counts']['common_5']=9
            elif case=='boolean_label':broken['lists']['a'][0]=True
            for flags in [[],['-O'],['-OO']]:
                (folder/'specimen.json').write_text(json.dumps(broken,indent=2)+'\n')
                run=subprocess.run([sys.executable,'-B',*flags,str(folder/'verify.py')],capture_output=True,text=True)
                if run.returncode==0:raise RuntimeError('accepted corrupted input: '+case+str(flags))
                controls.append({'case':case,'flags':flags,'rejected':True})
    report={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'primary_runs':receipts,'external_real_input_corruptions':controls,'scope':'Current deterministic verification interface; finite counts do not prove universal/infinite claims or novelty.','verifier_sha256':sha(SOURCE/'verify.py'),'specimen_sha256':sha(SOURCE/'specimen.json'),'controls_scope':'All18 real corrupted-input runs and all3 pristine modes executed against the exact recorded verifier and specimen, in a disposable clean folder. Expected-count outputs explicitly checked.'}
    (SOURCE/'REPLAY_AND_CONTROLS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'primary_runs':receipts,'rejected_controls':len(controls)}))

if __name__=='__main__':main()
