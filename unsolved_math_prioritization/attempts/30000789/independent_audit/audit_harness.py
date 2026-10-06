#!/usr/bin/env python3
"""Replay the independent checker and challenge temporary mutated copies."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
ROOT=Path(__file__).resolve().parent

def demand(value,message):
    if not value: raise ValueError(message)

def run(script,cwd,optimized):
    return subprocess.run([sys.executable,'-B']+(['-O'] if optimized else [])+[str(script)],cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)

def main():
    expected=(ROOT/'independent_results.json').read_bytes();source=(ROOT/'independent_check.py').read_text()
    mutations=[
        ('reversed_sharp','out[a,b]+=x','out[a,b]-=x'),
        ('factor_two_normalization','Q(n,I)==(n-1)*I','Q(n,I)==2*(n-1)*I'),
        ('wrong_apex_scalar','ae==u/(n*(n-1))','ae==u/(2*n*(n-1))'),
        ('wrong_selfdual_projection','zip([2,-1,-1],vectors)','zip([3,-1,-1],vectors)'),
        ('wrong_mixed_cubic','==33*ell and ip(cross,H)+ip(QH,V)==18*ell','==34*ell and ip(cross,H)+ip(QH,V)==18*ell')]
    positive=[];negative=[]
    with tempfile.TemporaryDirectory(prefix='ricci-auditor-replay-') as td:
        base=Path(td)
        for optimized in [False,True]:
            mode='optimized' if optimized else 'normal'
            for location in ['original','relocated']:
                script=ROOT/'independent_check.py'
                if location=='relocated':
                    folder=base/(mode+'_'+location);folder.mkdir();script=folder/'independent_check.py';shutil.copyfile(ROOT/'independent_check.py',script)
                r=run(script,base,optimized)
                demand(r.returncode==0 and r.stdout==expected,mode+' '+location+' replay failed: '+r.stderr.decode())
                positive.append({'mode':mode,'location':location,'status':'PASS','exact_output_match':True})
            for label,before,after in mutations:
                demand(source.count(before)==1,'Ambiguous mutation '+label)
                script=base/(mode+'_'+label+'.py');script.write_text(source.replace(before,after))
                r=run(script,base,optimized)
                demand(r.returncode!=0,'Mutation accepted: '+label)
                negative.append({'mode':mode,'case':label,'status':'REJECTED','exception':r.stderr.decode().strip().splitlines()[-1]})
    print(json.dumps({'status':'PASS','positive_replays':positive,'independent_code_mutation_rejections':negative,'scope':'Regression controls do not establish the unresolved global Weyl bound.'},sort_keys=True,indent=2))
if __name__=='__main__':main()
