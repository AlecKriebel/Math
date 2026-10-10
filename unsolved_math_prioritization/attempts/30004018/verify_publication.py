#!/usr/bin/env python3
"""Source-free replay; execute only after fixed external authentication."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys


def need(ok,label):
    if not ok:raise ValueError(label)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(b):return {'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def stream(b):return {'type':'inline_utf8','bytes':len(b),'sha256':sha(b),'text':b.decode('utf-8')}
def pairs(items):
    result={}
    for k,v in items:need(k not in result,'duplicate JSON key');result[k]=v
    return result
def load(b):return json.loads(b.decode('utf-8'),object_pairs_hook=pairs,parse_constant=lambda x:need(False,'nonfinite JSON'))
def exact_json_equal(actual,expected,path='$'):
    need(type(actual) is type(expected),'exact JSON type mismatch at '+path)
    if type(expected) is dict:
        need(set(actual)==set(expected),'exact JSON keys mismatch at '+path)
        for k in sorted(expected):exact_json_equal(actual[k],expected[k],path+'.'+k)
    elif type(expected) is list:
        need(len(actual)==len(expected),'exact JSON list length mismatch at '+path)
        for i,(a,e) in enumerate(zip(actual,expected)):exact_json_equal(a,e,path+'['+str(i)+']')
    else:need(actual==expected,'exact JSON value mismatch at '+path)
def parse_output(b):
    # Each producer emits JSON Lines, including single-line JSON producers.
    return [load(line) for line in b.splitlines() if line.strip()]
def compare_output(actual_stdout,actual_stderr,expected_stdout,expected_stderr):
    exact_json_equal(parse_output(actual_stdout),parse_output(expected_stdout))
    need(actual_stdout==expected_stdout,'complete fresh stdout bytes differ from pinned reference')
    need(actual_stderr==expected_stderr,'complete fresh stderr bytes differ from pinned reference')
def output_reference(e):
    need(type(e) is dict and set(e)=={'type','bytes','sha256','text'},'typed output reference exact keys')
    need(e['type']=='inline_utf8' and type(e['text']) is str,'inline UTF-8 output required')
    need(type(e['bytes']) is int and e['bytes']>=0 and type(e['sha256']) is str,'output pin types')
    b=e['text'].encode();need(len(b)==e['bytes'] and sha(b)==e['sha256'],'full output reference bytes')
    return b

MUTATIONS=['exterior-sign','wrong-weight','wrong-parity','class-implies-object','wrong-moment','drop-total-arrow','action-rank-is-algebra-rank','omit-Koszul-sign']
KINDS=['original','independent','frozen']+['mutation:'+m for m in MUTATIONS]
def command(root,kind,mode):
    flags=[] if mode==0 else ['-O' if mode==1 else '-OO']
    prefix=[sys.executable,'-I','-S','-B',*flags]
    if kind=='original':return prefix+[str(root/'original/check_examples.py')]
    if kind=='independent':return prefix+[str(root/'audit/independent_checks.py')]
    if kind=='frozen':return prefix+[str(root/'audit/verify_frozen.py'),str(root/'original')]
    need(kind.startswith('mutation:') and kind.split(':')[1] in MUTATIONS,'recognized mutation kind')
    return prefix+[str(root/'audit/independent_checks.py'),'--mutation',kind.split(':')[1]]
def validate_output(kind,mode,code,out,err):
    need(type(mode) is int and mode in (0,1,2),'actual optimization type')
    need(type(code) is int and code==(1 if kind.startswith('mutation:') else 0),'expected process exit')
    need(err==b'','empty stderr expected')
    rows=parse_output(out);need(bool(rows),'nonempty JSON output')
    if kind=='original':
        exact_json_equal(rows,[{'status':'PASS','checks':678,'uid':1000,'python_optimize':mode,'independent_rank_oracle':'minors','mutation_controls':'exterior sign and total rank rejected','scope':'finite diagnostic examples only'}])
    elif kind=='frozen':
        need(len(rows)==1 and rows[0]['status']=='PASS' and type(rows[0]['files']) is dict and len(rows[0]['files'])==6,'six-file original identity output')
    else:
        exact_json_equal(rows[0],{'event':'runtime','uid':1000,'optimize':mode,'mutation':kind.split(':')[1] if kind.startswith('mutation:') else 'none','implementation':'independent Bareiss-minors rank'})
        last=rows[-1];need(last['event']=='complete' and last['status']==('FAIL' if kind.startswith('mutation:') else 'PASS'),'independent final status')
        need(type(last['uid']) is int and last['uid']==1000 and type(last['optimize']) is int and last['optimize']==mode,'independent runtime identity')
        if kind=='independent':need(type(last['checks']) is int and last['checks']==3885,'independent guard count')
    return rows

def check_scope(root):
    expected={'accepted_results': ['Credited A_1=S_1 consequence and normalized known inclusion S_k subset A_k.', 'Strict objectwise-span versus simultaneous reduced-class-kernel distinction in gl(1|1).', 'Reverse-DS counterexample only in a gl(1|1) direct-sum Levi diagnostic.', 'Externally decomposable tensor products and universal-cohomology specialization diagnostics retain restricted scope.'], 'approaches': 5, 'correction_required': False, 'dataset_contents_delivered': False, 'decision': 'ACCEPT_UNCHANGED_SCOPED_PARTIAL_AUDIT', 'default_absent_inputs': {'corpus_rehash': 'NOT_RUN', 'source_pdf_rehash': 'NOT_RUN'}, 'full_target_resolved': False, 'independent_audit_preserved': True, 'limits': ['Finite calculations do not verify imported representation-theory theorems.', 'No full-conjecture counterexample or complete candidate.', 'No comprehensive openness, novelty, or priority certificate.', 'No sixth substantive proof-search approach.'], 'novelty_claim': False, 'original_preserved': True, 'outcome': 'exhausted', 'private_coordination_delivered': False, 'problem_id': 30004018, 'rank': 1070, 'remaining_gap': 'Full integral category O: A_k subset S_k for 2<=k<=min(m,n).', 'schema': 'duflo-socle-scope-v1', 'source_bodies_delivered': False, 'source_problem_code': 'OWR-16635-003', 'historical_runner_caveat': 'The preserved audit runner without its optional PDF directory has an empty source-check list but retains a generic historical rehash sentence; it is not the current source-free default. Fresh PDF and corpus rehash are NOT_RUN.'}
    s=load((root/'SCOPE.json').read_bytes());exact_json_equal(s,expected)
    p=load((root/'PROVENANCE.json').read_bytes())
    need(p['schema']=='duflo-socle-provenance-v1' and type(p['problem_id']) is int and p['problem_id']==30004018,'provenance identity')
    for directory,count in [('original',6),('audit',8)]:
        entries=p[directory+'_files'];need(type(entries) is dict and len(entries)==count,'preserved file count')
        need(set(x.name for x in (root/directory).iterdir())==set(entries),'preserved complete inventory')
        for name,expected_pin in entries.items():exact_json_equal(pin((root/directory/name).read_bytes()),expected_pin)
    need(sha((root/'audit/MANIFEST.json').read_bytes())=='6811b52e0cfc1e131831be4c4b99c9424b83189fb2c8d9fc2460f967e128dfd4','reviewed audit manifest literal pin')
    for directory in ['original','audit']:
        m=load((root/directory/'MANIFEST.json').read_bytes());need(m['algorithm']=='sha256','historical manifest algorithm')
        need(set(m['files'])==set(p[directory+'_files'])-{'MANIFEST.json'},'historical complete manifest coverage')
        for n,e in m['files'].items():exact_json_equal(e,{k:pin((root/directory/n).read_bytes())[k] for k in ['bytes','sha256']})
    for n in ['original/check_examples.py','audit/independent_checks.py','audit/verify_frozen.py','verify_publication.py']:
        need(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse((root/n).read_text()))),'assert-free replay')
    return s

def check_references(root):
    r=load((root/'verification/REPRODUCTION.json').read_bytes())
    need(set(r)=={'schema','uid','euid','fresh','historical_receipts_reused','default_absent_inputs','readonly','runs'},'reference receipt exact schema')
    exact_json_equal({k:r[k] for k in ['schema','uid','euid','fresh','historical_receipts_reused','default_absent_inputs']},{'schema':'duflo-socle-fresh-runs-v1','uid':1000,'euid':1000,'fresh':True,'historical_receipts_reused':False,'default_absent_inputs':{'source_pdf_rehash':'NOT_RUN','corpus_rehash':'NOT_RUN'}})
    need(type(r['readonly']) is dict and set(r['readonly'])=={'directory_create_denials','file_write_open_denials','includes_actual_queue'},'readonly schema')
    need(type(r['readonly']['directory_create_denials']) is int and r['readonly']['directory_create_denials']>=3,'reference directory denial count')
    need(type(r['readonly']['file_write_open_denials']) is int and r['readonly']['file_write_open_denials']>=15 and r['readonly']['includes_actual_queue'] is True,'reference file denial count')
    expected={(kind,mode) for kind in KINDS for mode in [0,1,2]};seen={}
    need(type(r['runs']) is list and len(r['runs'])==len(expected),'all kind/mode reference runs')
    for e in r['runs']:
        need(type(e) is dict and set(e)=={'kind','optimization','exit_code','stdout','stderr'},'run exact schema')
        need(type(e['kind']) is str and type(e['optimization']) is int,'reference identity types')
        key=(e['kind'],e['optimization']);need(key in expected and key not in seen,'unique kind/mode reference')
        out=output_reference(e['stdout']);err=output_reference(e['stderr']);validate_output(*key,e['exit_code'],out,err);seen[key]=e
    return seen

def verify(root,queue):
    need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000 required')
    scope=check_scope(root);references=check_references(root)
    proof=load((root/'QUEUE_PROOF.json').read_bytes());exact_json_equal(pin(queue.read_bytes()),proof['after'])
    rows=[]
    for kind in KINDS:
        r=subprocess.run(command(root,kind,sys.flags.optimize),cwd=root,capture_output=True,timeout=90)
        expected=references[(kind,sys.flags.optimize)]
        validate_output(kind,sys.flags.optimize,r.returncode,r.stdout,r.stderr)
        compare_output(r.stdout,r.stderr,output_reference(expected['stdout']),output_reference(expected['stderr']))
        rows.append({'kind':kind,'optimization':sys.flags.optimize,'exit_code':r.returncode,'full_stdout_stderr_match_pinned_reference':True,'recursive_exact_json_types_match':True,'stdout':stream(r.stdout),'stderr':stream(r.stderr)})
    return {'schema':'duflo-socle-replay-v1','status':'PASS_SCOPED_PARTIAL_RESULTS','problem_id':30004018,'outcome':'exhausted','approaches':5,'full_target_resolved':False,'novelty_claim':False,'uid':os.getuid(),'euid':os.geteuid(),'optimization':sys.flags.optimize,'default_absent_inputs':scope['default_absent_inputs'],'fresh_replays':rows}

if __name__=='__main__':
    try:
        p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--queue',required=True,type=Path);a=p.parse_args()
        print(json.dumps(verify(a.root.absolute(),a.queue.absolute()),indent=2,sort_keys=True))
    except Exception as e:print('REJECT: '+type(e).__name__+': '+str(e),file=sys.stderr);sys.exit(1)
