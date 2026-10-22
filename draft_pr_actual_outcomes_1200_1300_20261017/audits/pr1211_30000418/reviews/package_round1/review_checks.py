#!/usr/bin/env python3
"""Candidate-aware independent package checks. All writes stay in this review."""
from pathlib import Path
from itertools import product
import copy
import datetime
import hashlib
import json
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE / 'extracted'
PUB = HERE.parents[1] / 'publication'
def digest(path):
    b = path.read_bytes()
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
def require(c, message):
    if not c:
        raise RuntimeError(message)
def bindings(folder, entries, key):
    for e in entries:
        actual = digest(folder/e[key])
        require(actual['sha256'] == e['sha256'], 'digest mismatch '+e[key])
        if 'bytes' in e:
            require(actual['bytes'] == e['bytes'], 'size mismatch '+e[key])
    return len(entries)
def factor_count(lists):
    """Enumerate only the spine, then exactly count independent leaf stars.

    This uses the drawn construction directly, not candidate graph/CSP code.
    """
    total = 0
    for a,b,c,d,e in product(*(lists[v] for v in 'abcde')):
        if any(abs(x-y)<2 for x,y in [(a,b),(b,c),(c,d),(d,e)]):
            continue
        if a == c or b == d or c == e:
            continue
        left = [x for x in lists['a1'] if abs(x-a)>=2 and x!=b]
        left2 = [x for x in lists['a2'] if abs(x-a)>=2 and x!=b]
        right = [x for x in lists['e1'] if abs(x-e)>=2 and x!=d]
        right2 = [x for x in lists['e2'] if abs(x-e)>=2 and x!=d]
        pair_left = sum(x!=y for x,y in product(left,left2))
        pair_right = sum(x!=y for x,y in product(right,right2))
        single_b = sum(abs(x-b)>=2 and x!=a and x!=c for x in lists['b1'])
        single_d = sum(abs(x-d)>=2 and x!=c and x!=e for x in lists['d1'])
        total += pair_left*pair_right*single_b*single_d
    return total

def main():
    results = {'at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'review_boundary': 'Candidate-aware new package reviewer; no discovery or wholly blind independence claimed.'}
    files = ['Tree_Five_List_Note_v1.0.pdf', 'Tree_Five_List_Verification_v1.0.zip', 'manuscript/main.tex']
    results['candidate'] = {n:digest(PUB/n) for n in files}
    receipt = json.loads((PUB/'BUILD_RECEIPT.json').read_text())
    for n,k in [(files[0],'pdf'),(files[1],'verification_zip')]:
        require(results['candidate'][n]['sha256']==receipt[k]['sha256'], 'receipt '+n)
        require(results['candidate'][n]['bytes']==receipt[k]['bytes'], 'receipt bytes '+n)
    manifest = json.loads((ROOT/'MANIFEST.json').read_text())
    with zipfile.ZipFile(PUB/files[1]) as archive:
        actual_members=archive.namelist()
        require(len(set(actual_members))==len(actual_members),'duplicate zip names')
        require(set(actual_members)=={e['path'] for e in manifest['files']}|{'MANIFEST.json'},'root manifest exact completeness')
    results['root_manifest_members'] = bindings(ROOT,manifest['files'],'path')
    require(digest(ROOT/'MANIFEST.json')['sha256']==receipt['manifest_sha256'],'manifest external pin')
    require((ROOT/'manuscript/main.tex').read_bytes()==(PUB/'manuscript/main.tex').read_bytes(),'manuscript equality')
    require(digest(ROOT/'manuscript/main.tex')['sha256']==receipt['manuscript_source_sha256'],'source external pin')
    corrected = json.loads((ROOT/'corrected_edition/MANIFEST.json').read_text())
    results['corrected_manifest_members'] = bindings(ROOT/'corrected_edition',corrected['entries'],'file')
    require(set(corrected['members'])=={e['file'] for e in corrected['entries']}|{'MANIFEST.json'},'corrected manifest completeness')
    accept = json.loads((ROOT/'corrected_edition/ACCEPTANCE.json').read_text())
    for n,meta in accept['current_document_bindings'].items():
        require(digest(ROOT/'corrected_edition'/n)==meta,'current corrected binding '+n)
    results['corrected_acceptance_current_bindings'] = len(accept['current_document_bindings'])
    freeze = json.loads((ROOT/'independent_family/FREEZE_MANIFEST.json').read_text())
    for n,sha in freeze['artifacts'].items():
        require(digest(ROOT/'independent_family'/n)['sha256']==sha,'input-family freeze '+n)
    require((ROOT/'independent_family/FREEZE_SHA256.txt').read_text().split()[0]==digest(ROOT/'independent_family/FREEZE_MANIFEST.json')['sha256'],'freeze pin')
    results['independent_freeze_members'] = len(freeze['artifacts'])
    for family,fn in [('independent','FREEZE.json'),('adversary','FROZEN_FINDINGS.json')]:
        frozen=json.loads((ROOT/'priority'/family/fn).read_text())
        results['priority_'+family+'_freeze_members']=bindings(ROOT/'priority'/family,frozen['files'],'path')
    runs=[]
    for flags in [[],['-O'],['-OO']]:
        run=subprocess.run([sys.executable,'-B',*flags,str(ROOT/'verify.py')],capture_output=True,text=True)
        require(run.returncode==0,'primary pristine '+str(flags)+run.stderr)
        require((ROOT/'results.json').read_bytes()==(ROOT/'expected_results.json').read_bytes(),'all result bytes '+str(flags))
        runs.append({'flags':flags,'returncode':run.returncode,'results':digest(ROOT/'results.json')})
    results['fresh_primary_modes']=runs
    specimen=json.loads((ROOT/'specimen.json').read_text())
    names=specimen['vertices']
    results['independent_spine_factorization_counts']={str(k):factor_count({v:list(range(1,k+1)) for v in names}) for k in range(1,7)}
    results['independent_spine_factorization_bad_lists']=factor_count(specimen['lists'])
    require(list(results['independent_spine_factorization_counts'].values())==[0,0,0,0,8,6336], 'independent counts')
    require(results['independent_spine_factorization_bad_lists']==0,'independent bad instance')
    controls=HERE/'controls'
    controls.mkdir(exist_ok=True)
    (controls/'verify.py').write_bytes((ROOT/'verify.py').read_bytes())
    mutations={
        'deleted_edge':lambda s:s['edges'].pop(),
        'changed_tree_edge':lambda s:s['edges'].__setitem__(-1,['c','e2']),
        'changed_list_value':lambda s:s['lists']['a1'].__setitem__(-1,7),
        'list_cardinality_four':lambda s:s['lists']['a1'].pop(),
        'invalid_edge_witness':lambda s:s['ordinary_five_witness'].__setitem__('b',1),
        'invalid_distance_two_witness':lambda s:s['ordinary_five_witness'].__setitem__('a2',3),
        'outside_list_witness':lambda s:s['ordinary_five_witness'].__setitem__('a1',99),
        'boolean_list_value':lambda s:s['lists']['a'].__setitem__(0,True),
        'boolean_witness_value':lambda s:s['ordinary_five_witness'].__setitem__('a',True),
        'changed_count_metadata':lambda s:s['expected_counts'].__setitem__('common_5',7),
    }
    records=[]
    for name,mutate in mutations.items():
        data=copy.deepcopy(specimen)
        mutate(data)
        (controls/'specimen.json').write_text(json.dumps(data))
        for flags in [[],['-O'],['-OO']]:
            run=subprocess.run([sys.executable,'-B',*flags,str(controls/'verify.py')],capture_output=True,text=True)
            require(run.returncode!=0,'corruption accepted '+name+str(flags))
            records.append({'case':name,'flags':flags,'rejected':True,'final_error':run.stderr.strip().splitlines()[-1]})
    results['real_math_input_corruptions']=records
    # Corrupt actual extracted members and restore exact bytes after every probe.
    byte_cases=[]
    for rel in ['specimen.json','manuscript/main.tex','independent_family/results.json']:
        target=ROOT/rel
        saved=target.read_bytes()
        try:
            target.write_bytes(saved+b' ')
            run=subprocess.run([sys.executable,'-B',str(ROOT/'replay.py')],capture_output=True,text=True)
            require(run.returncode!=0,'root corruption accepted '+rel)
            byte_cases.append({'member':rel,'rejected':True,'final_error':run.stderr.strip().splitlines()[-1]})
        finally:
            target.write_bytes(saved)
    target=ROOT/'manuscript/main.tex'
    saved=target.read_bytes()
    try:
        require(b'eleven-vertex' in saved,'same-size probe target')
        target.write_bytes(saved.replace(b'eleven-vertex',b'twelve-vertex',1))
        run=subprocess.run([sys.executable,'-B',str(ROOT/'replay.py')],capture_output=True,text=True)
        require(run.returncode!=0,'same-size corruption accepted')
        byte_cases.append({'member':'manuscript/main.tex','case':'same-size altered theorem title','rejected':True,'final_error':run.stderr.strip().splitlines()[-1]})
    finally:
        target.write_bytes(saved)
    results['manifest_real_member_corruptions']=byte_cases
    # Restore clean extraction bindings and independently replay frozen priority data.
    results['restored_root_manifest_members']=bindings(ROOT,manifest['files'],'path')
    for family,script in [('independent','check_fiala_comparison.py'),('adversary','check_fiala_figure4.py')]:
        run=subprocess.run([sys.executable,'-B',script],cwd=ROOT/'priority'/family,capture_output=True,text=True)
        require(run.returncode==0,'priority comparison '+family+run.stderr)
        results['priority_'+family+'_fresh_comparison']={'returncode':0,'stdout':run.stdout.strip()}
    results['status']='PASS'
    (HERE/'CHECKS.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps({'status':'PASS','manifest_members':results['root_manifest_members'],'mathematical_corruption_runs':len(records),'byte_corruption_runs':len(byte_cases),'independent_counts':results['independent_spine_factorization_counts']},indent=2))
if __name__=='__main__':
    main()
