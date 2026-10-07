#!/usr/bin/env python3
"""Run normal/optimized, isolated/relocated replay and non-vacuous mutation controls."""
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def run(args, cwd):
    p = subprocess.run([sys.executable] + args, cwd=cwd, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return {'returncode':p.returncode, 'stdout':p.stdout.strip(), 'stderr':p.stderr.strip()}

def need(value, message):
    if not value: raise ValueError(message)

def main():
    results = {'positive':[], 'negative':[]}
    with tempfile.TemporaryDirectory(prefix='asep_certificate_') as td:
        td = Path(td); relocated = td/'relocated'; relocated.mkdir()
        for name in ['check_certificate.py','certificate.json']:
            shutil.copy2(ROOT/name, relocated/name)
        checker = str(relocated/'check_certificate.py')
        for flags in [[],['-O'],['-I','-S'],['-I','-S','-O']]:
            r = run(flags+[checker,'--cross-window'], td)
            need(r['returncode']==0, 'valid replay rejected: '+str(flags))
            results['positive'].append({'flags':flags,'relocated':True,**r})
        original = json.loads((relocated/'certificate.json').read_text())
        def reject(name, value):
            file = relocated/(name+'.json'); file.write_text(json.dumps(value))
            for flags in [[],['-I','-S','-O']]:
                r=run(flags+[checker,'--certificate',str(file)],td)
                need(r['returncode']!=0 and 'certificate differs' in r['stderr'],
                     'mutation accepted or failed outside mathematical check: '+name)
                results['negative'].append({'name':name,'flags':flags,'rejected':True})
        c=copy.deepcopy(original); c['cases'][0]['leading_coefficient']='1/2'; reject('wrong_sign',c)
        c=copy.deepcopy(original); c['cases'].pop(); c['case_count']-=1; reject('missing_case',c)
        c=copy.deepcopy(original); c['cases'][0]['covariance_taylor_in_tau'][0]=['0','1']; reject('nonzero_lower_q_term',c)
        c=copy.deepcopy(original); c['delta']='1'; reject('unsupported_time_bound',c)
        c=copy.deepcopy(original); c['cases'][0]['A_truth_table']=0; reject('wrong_increasing_event',c)
        source=(relocated/'check_certificate.py').read_text()
        old='rate = (F(1),) if x else (F(0), F(1))'
        need(source.count(old)==1,'model mutation target not unique')
        altered=relocated/'wrong_left_rate.py'
        altered.write_text(source.replace(old,'rate = (F(1),) if x else (F(0),)'))
        for flags in [[],['-I','-S','-O']]:
            r=run(flags+[str(altered)],td)
            need(r['returncode']!=0 and 'certificate differs' in r['stderr'],
                 'changed dynamics not rejected by coefficient recomputation')
            results['negative'].append({'name':'left_rate_deleted','flags':flags,'rejected':True})
    print(json.dumps(results,indent=2))

if __name__=='__main__': main()
