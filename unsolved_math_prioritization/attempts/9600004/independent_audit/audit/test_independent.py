#!/usr/bin/env python3
"""Relocated, optimization-safe replay and independent non-vacuous controls."""
import copy
import importlib.util
import json
from fractions import Fraction
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent

def require(ok, message):
    if not ok: raise ValueError(message)

def call(script, flags, args, cwd):
    p=subprocess.run([sys.executable,*flags,str(script),*args],cwd=cwd,text=True,capture_output=True)
    return p

def main():
    out={'positive':[],'certificate_controls':[],'dynamics_controls':[]}
    with tempfile.TemporaryDirectory(prefix='independent_asep_') as temp:
        root=Path(temp)/'a directory with spaces';(root/'audit').mkdir(parents=True)
        (root/'original/asymmetric_exclusion_9600004').mkdir(parents=True)
        script=root/'audit/independent_recompute.py'
        shutil.copyfile(HERE/'independent_recompute.py',script)
        certpath=root/'original/asymmetric_exclusion_9600004/certificate.json'
        shutil.copyfile(HERE.parent/'original/asymmetric_exclusion_9600004/certificate.json',certpath)
        for flags in ([],['-O'],['-I','-S'],['-I','-S','-O']):
            p=call(script,flags,[],Path(temp))
            require(p.returncode==0,'valid independent replay rejected: '+p.stderr)
            out['positive'].append({'flags':flags,'relocated':True,'ok':json.loads(p.stdout)['ok']})
        cert=json.loads(certpath.read_text())
        mutations=[]
        def add(name,fn,expected):
            value=copy.deepcopy(cert);fn(value);mutations.append((name,value,expected))
        add('changed_taylor_coefficient',lambda c:c['cases'][0]['covariance_taylor_in_tau'][0].__setitem__(0,'1'),'coefficient mismatch')
        add('changed_leading_sign',lambda c:c['cases'][0].__setitem__('leading_coefficient','1'),'leading metadata mismatch')
        add('deleted_case',lambda c:c['cases'].pop(),'event key coverage mismatch')
        add('duplicate_case',lambda c:c['cases'].append(c['cases'][0]),'duplicate certificate case')
        add('nonincreasing_event',lambda c:c['cases'][0].__setitem__('A_truth_table',1),'event key coverage mismatch')
        add('overlapping_support',lambda c:c['cases'][0].__setitem__('B',c['cases'][0]['A']),'event key coverage mismatch')
        add('unsupported_time_bound',lambda c:c.__setitem__('delta','1'),'time bound mismatch')
        add('incorrect_step',lambda c:c.__setitem__('initial_occupied','all integers > 0'),'step mismatch')
        add('incorrect_rate_normalization',lambda c:c.__setitem__('normalized_time','tau = (p+q)*t'),'normalization mismatch')
        for name,c,expected in mutations:
            path=root/(name+'.json');path.write_text(json.dumps(c))
            for flags in ([],['-I','-S','-O']):
                p=call(script,flags,['--certificate',str(path)],Path(temp))
                require(p.returncode!=0 and expected in p.stderr,'control failed outside expected mathematical check: '+name+' '+p.stderr)
                out['certificate_controls'].append({'name':name,'flags':flags,'rejected':True,'reason':expected})
        for name,arg in [('reversed_rates','--reverse-rates'),('reversed_step','--reverse-step')]:
            for flags in ([],['-I','-S','-O']):
                p=call(script,flags,[arg],Path(temp))
                require(p.returncode!=0 and 'coefficient mismatch' in p.stderr,'dynamics mutation not detected: '+name)
                out['dynamics_controls'].append({'name':name,'flags':flags,'rejected':True,'reason':'coefficient mismatch'})
    spec=importlib.util.spec_from_file_location('audit_recompute',HERE/'independent_recompute.py')
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    # Uniform even parity in first three coordinates, fourth coordinate fixed 0.
    law={0:Fraction(1,4),3:Fraction(1,4),5:Fraction(1,4),6:Fraction(1,4)}
    def mean(masks):return sum(p for s,p in law.items() if s in masks)
    def cov(am,bm):return mean(am&bm)-mean(am)*mean(bm)
    singles=[frozenset(s for s in range(16) if s&(1<<i)) for i in range(4)]
    pairwise=[cov(singles[i],singles[j]) for i in range(4) for j in range(i+1,4)]
    require(max(pairwise)==0,'pairwise control not pairwise independent')
    a=singles[0];b=singles[1]|singles[2]
    witness=cov(a,b)
    require(witness==Fraction(1,8),'full-event witness wrong')
    required_truth=next(t for t,ev in m.antichain_events((0,1)) if ev==b)
    require(required_truth==14,'OR event missing from enumeration')
    out['adversarial_distribution']={'law':'uniform even parity on three coordinates, fourth fixed 0',
        'pairwise_covariances':[str(x) for x in pairwise],
        'disjoint_increasing_witness':'Cov(X1, X2 OR X3)', 'witness_covariance':str(witness),
        'enumeration_includes_witness':True}
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
