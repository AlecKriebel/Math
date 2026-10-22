#!/usr/bin/env python3
"""Raw portable-program receipts, re-pinned semantic attacks and independent reconciliation."""
from pathlib import Path
import hashlib,json,re,shutil,sys
from fractions import Fraction as F
from command_runner import run,ROOT
A=ROOT.parents[1];P=A/'preprint_v1_1';K=ROOT/'fixtures/semantic_copy'
def need(p,msg):
    if not p:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def repin():
    p=K/'MANIFEST.json';obj=json.loads(p.read_text())
    for r in obj['files']:
        b=(K/r['path']).read_bytes();r.update(bytes=len(b),sha256=sha(b))
    p.write_text(json.dumps(obj,indent=2)+'\n')
def main():
    scripts=json.loads((P/'kit/EXPECTED_RESULTS.json').read_text())
    for flags,tag in (([],'normal'),(['-O'],'O'),(['-OO'],'OO')):
        for script,expected in scripts.items():
            name='raw_'+script[:-3]+'_'+tag
            r=run(name,[sys.executable,'-I','-B',*flags,P/'kit/scripts'/script])
            need(r['expectation_met'] and r['stdout_bytes']==expected['bytes'] and r['stdout_sha256']==expected['sha256'],'raw diagnostic mismatch')
    ours=json.loads((ROOT/'commands/independent_normal.stdout').read_text())
    supplied=json.loads((ROOT/'commands/raw_check_analytic_independent_normal.stdout').read_text())
    actual={(tuple('T' if x=='E' else x for x in r['pair']),r['q'],r['character_sign']):r for r in supplied['scalar_checks']}
    for r in ours['germs']:
        s=actual[(tuple(r['pair']),r['q'],r['zeta'])]
        need(r['order']==s['order'] and F(r['leading'])==F(s['leading_in_t_minus_1']),'independent scalar mismatch')
        need(list(map(F,r['P']))==list(map(F,s['P'])) and list(map(F,r['Q']))==list(map(F,s['Q'])),'independent exponent mismatch')
    # Parse the manuscript rows and compare directly against this review's graph data.
    graphs={(''.join(g['left']),''.join(g['right'])):g for p in ours['partitions'] for g in p['graphs']}
    table=[]
    for line in (P/'paper.tex').read_text().splitlines():
        if not re.match(r'^\$[ABCDT]+/[ABCDT]+\$ &',line):continue
        cells=line.split(' & ');direction=re.findall(r'[ABCDT]+',cells[1]);g=graphs[tuple(direction)]
        witness=list(re.findall(r'\(([ABCDT]),([ABCDT])\)',cells[2])[0]);Y=[list(x) for x in re.findall(r'\(([ABCDT]),([ABCDT])\)',cells[3])]
        need(sorted(Y)==sorted(g['Y']),'independent entire-Y table discrepancy')
        need(any(e['x']==witness and e['y']==[] for e in g['edges']),'independent witness discrepancy')
        table.append(direction)
    need(len(table)==15,'manuscript table row count')
    attacks=('readiness','priority','endpoint','paper_Y','expected_digest')
    for attack in attacks:
        if K.exists():shutil.rmtree(K)
        shutil.copytree(P/'kit',K,copy_function=shutil.copyfile)
        if attack in ('readiness','priority'):
            p=K/'STATUS.json';obj=json.loads(p.read_text())
            if attack=='readiness':obj['publication_ready']=True
            else:obj['priority_overlap_Luo_Zha']='CLEARED'
            p.write_text(json.dumps(obj,indent=2)+'\n')
        if attack=='endpoint':
            p=K/'scripts/check_analytic_independent.py';s=p.read_text();need("'A': (0, 2)" in s,'endpoint fixture target');p.write_text(s.replace("'A': (0, 2)","'A': (0, 1)",1))
        if attack=='paper_Y':
            p=K/'paper.tex';s=p.read_text();needle='$(A,B),(A,D)$';need(needle in s,'paper fixture target');p.write_text(s.replace(needle,'$(A,B),(A,C)$',1))
        if attack=='expected_digest':
            p=K/'EXPECTED_RESULTS.json';obj=json.loads(p.read_text());obj['check_analytic_independent.py']['sha256']='0'*64;p.write_text(json.dumps(obj,indent=2)+'\n')
        repin()
        for flags,tag in (([],'normal'),(['-O'],'O'),(['-OO'],'OO')):
            r=run('semantic_'+attack+'_'+tag,[sys.executable,'-I','-B',*flags,K/'scripts/verify_kit.py'],expected=1)
            need(r['expectation_met'],'re-pinned semantic attack accepted')
    # Use the native uploader's early LOCAL check branch, no credentials or service client.
    for name,path in [('native_local_versioned',A/'publication/zenodo-deposit-v1_1.json'),('native_local_candidate',P/'zenodo-deposit.json')]:
        r=run(name,['/usr/bin/env','-i','PATH=/opt/homebrew/bin:/usr/bin:/bin',sys.executable,'-I','-B',A.parents[2]/'zenodo_deposit_tool/zenodo.py','check',path])
        need(r['expectation_met'],'native LOCAL parse failure')
    need((ROOT/'commands/native_local_versioned.stdout').read_bytes()==(ROOT/'commands/native_local_candidate.stdout').read_bytes(),'native local object mismatch')
    (ROOT/'SUPPLEMENT_RESULTS.json').write_text(json.dumps(dict(status='PASS',raw_diagnostic_runs=15,independent_exact_scalar_matches=40,independent_full_Y_rows=15,re_pinned_semantic_attack_runs=15,native_LOCAL_checks=2,no_service_calls=True),indent=2)+'\n')

if __name__=='__main__':main()
