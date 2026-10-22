#!/usr/bin/env python3
"""Replay scoped mathematics after authentication by the fixed external bootstrap."""
import argparse
import ast
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys


def need(ok,label):
    if not ok:raise ValueError(label)

def pairs(items):
    out={}
    for k,v in items:need(k not in out,'duplicate JSON key');out[k]=v
    return out

def load(b):return json.loads(b.decode('utf-8'),object_pairs_hook=pairs,parse_constant=lambda x:need(False,'nonfinite JSON'))
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(b):return {'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def stream(b):return {'type':'inline_utf8','bytes':len(b),'sha256':sha(b),'text':b.decode('utf-8')}

def exact_json_equal(actual,expected,path='$'):
    need(type(actual) is type(expected),'exact JSON type mismatch at '+path)
    if type(expected) is dict:
        need(set(actual)==set(expected),'exact JSON keys mismatch at '+path)
        for k in sorted(expected):exact_json_equal(actual[k],expected[k],path+'.'+k)
    elif type(expected) is list:
        need(len(actual)==len(expected),'exact JSON list length mismatch at '+path)
        for i,(a,e) in enumerate(zip(actual,expected)):exact_json_equal(a,e,path+'['+str(i)+']')
    else:need(actual==expected,'exact JSON value mismatch at '+path)

def compare_output(actual_stdout,actual_stderr,expected_stdout,expected_stderr):
    # Type-exact recursion precedes the byte comparison so bool/int substitutions,
    # nested extra keys and formerly unchecked fields are independently rejected.
    exact_json_equal(load(actual_stdout),load(expected_stdout))
    need(actual_stdout==expected_stdout,'complete fresh stdout bytes differ from pinned reference')
    need(actual_stderr==expected_stderr,'complete fresh stderr bytes differ from pinned reference')

def check_scope(root):
    s=load((root/'SCOPE.json').read_bytes())
    scalar={'schema':'dynamic-transport-scoped-acceptance-v1','problem_id':30003937,'rank':1068,'source_problem_code':'OWR-16414-001','decision':'ACCEPT_CORRECTED_SCOPED_PARTIAL_RESULTS','outcome':'exhausted','approaches':5,'corrected_file_count':13}
    false_keys=['full_target_resolved','complete_candidate','novelty_claim','positive_initial_density_counterexample','specialized_local_theorem_disproved','journal_version_proof_compared','source_bodies_delivered','dataset_contents_delivered','private_coordination_delivered','original_full_packet_delivered']
    true_keys=['continuation_requires_valid_local_restart','L2_uniqueness_only_for_existing_regular_trajectories']
    need(set(s)==set(scalar)|set(false_keys)|set(true_keys)|{'default_checks','accepted_results','open_gaps'},'scope exact schema')
    for k,v in scalar.items():need(type(s[k]) is type(v) and s[k]==v,'scope scalar '+k)
    for k in false_keys:need(s[k] is False,'unsupported scope promotion '+k)
    for k in true_keys:need(s[k] is True,'missing qualification '+k)
    need(s['default_checks']=={'original_full_reproduction':'NOT_RUN','full_original_patch_roundtrip':'NOT_RUN','source_pdf_rehash':'NOT_RUN','corpus_rehash':'NOT_RUN'},'honest absent-input statuses')
    need(s['accepted_results']==['conditional entropy energy estimate on an existing regular trajectory','conditional positive Holder endpoint and restart implication','narrower L2 uniqueness among existing regular trajectories','convex dissipation and one frozen bounded-state variational step','explicit interval and radial-ball convergence','nongauge potential nonconvergence in the enlarged degenerate class only'],'accepted result scope')
    need(s['open_gaps']==['general multidimensional global continuation','whole-trajectory potential compactness and selection','measure-minimizer hypotheses and stronger density topology'],'open gaps')
    c=root/'current';p=load((root/'PROVENANCE.json').read_bytes())
    need(set(x.name for x in c.iterdir())==set(p['current_files']) and len(p['current_files'])==13,'exact corrected thirteen files')
    for name,expected in p['current_files'].items():
        need('/' not in name and name not in ('.','..'),'current path')
        need(pin((c/name).read_bytes())==expected,'preserved corrected file pin '+name)
    status=load((c/'STATUS.json').read_bytes());need(type(status['problem_id']) is int and status['problem_id']==30003937 and type(status['substantive_proof_search_approaches']) is int and status['substantive_proof_search_approaches']==5 and status['outcome']=='exhausted','current status')
    for k in ['full_target_resolved','complete_candidate','novelty_claim']:need(status[k] is False,'current scope promotion')
    need(status['audit_qualification']=='Continuation requires a valid local restart theorem; the inspected preprint uses an unjustified generic Holder modulus estimate. Conditional entropy and explicit cases retain their stated scope.','restart caveat')
    for path,raw_pin,prefix in [('audit/AUDIT.md','historical_audit','publication_audit_preamble_bytes'),('audit/CORRECTIONS.patch','historical_contextual_patch','publication_patch_preamble_bytes')]:
        b=(root/path).read_bytes();n=p[prefix];need(type(n) is int and n>0 and pin(b[n:])==p[raw_pin],'preserved audit or patch bytes')
    patch=(root/'audit/CORRECTIONS.patch').read_text();need('REJECTED OR SUPERSEDED' in patch.split('--- original/')[0],'patch rejection preamble')
    for path in ['verify_publication.py','current/check_claims.py','audit/independent_checks.py']:
        need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse((root/path).read_text()))),'assert-free verification code')
    return s

def check_sources(root):
    m=load((root/'current/SOURCE_MANIFEST.json').read_bytes())
    need(m['schema']==1 and type(m['problem_id']) is int and m['problem_id']==30003937,'source manifest identity')
    for k in ['source_bodies_in_payload','source_dataset_contents_in_payload','private_coordination_in_payload']:need(m[k] is False,'source-free declaration')
    need(type(m['sources']) is list and len(m['sources'])==9,'nine source metadata records')
    ids=set()
    for e in m['sources']:
        need(type(e['source_id']) is str and e['source_id'] not in ids,'unique source ids');ids.add(e['source_id'])
        need(type(e['pdf_bytes']) is int and e['pdf_bytes']>0 and re.fullmatch('[0-9a-f]{64}',e['pdf_sha256']) is not None,'source public pin types')
        for k in ['public_url','associated_pdf_url']:need(e[k].startswith('https://'),'public source URL')
    return {'records':len(ids),'fresh_pdf_rehash':'NOT_RUN','fresh_corpus_rehash':'NOT_RUN','scope':'Public metadata inspected; input source bytes are not distributed.'}

def output_reference(root,e):
    need(type(e) is dict and set(e)=={'type','path','bytes','sha256'},'typed output reference')
    need(e['type']=='relative_file' and type(e['path']) is str and re.fullmatch(r'verification/runs/[A-Za-z0-9_.-]+',e['path']) is not None,'output reference path')
    need(type(e['bytes']) is int and e['bytes']>=0,'output byte count type')
    b=(root/e['path']).read_bytes();need(len(b)==e['bytes'] and sha(b)==e['sha256'],'full output reference bytes')
    return b

def check_receipts(root):
    r=load((root/'verification/REPRODUCTION.json').read_bytes())
    need(r['schema']=='dynamic-transport-fresh-runs-v1' and r['uid']==1000 and type(r['uid']) is int,'fresh receipt identity')
    need(r['historical_original_runs_reused'] is False and r['default_absent_inputs']=={'original_full_reproduction':'NOT_RUN','full_original_patch_roundtrip':'NOT_RUN','source_pdf_rehash':'NOT_RUN','corpus_rehash':'NOT_RUN'},'receipt fresh and absent-input scope')
    need(type(r['runs']) is list and len(r['runs'])==6,'six fresh proof-code runs')
    expected={(who,mode) for who in ['current','independent'] for mode in [0,1,2]};seen=set()
    for e in r['runs']:
        key=(e['kind'],e['optimization']);need(key in expected and key not in seen,'receipt run identity');seen.add(key)
        need(type(e['optimization']) is int and type(e['exit_code']) is int and e['exit_code']==0,'receipt exit and mode')
        b=output_reference(root,e['stdout']);need(output_reference(root,e['stderr'])==b'','receipt stderr')
        o=load(b);need(o['uid']==1000 and type(o['uid']) is int and o['status']=='passed','fresh checker receipt result')
        if e['kind']=='current':
            need(o['python_optimization']==e['optimization'] and o['readonly_required'] is True and o['readonly']=={'actual_write_probes':True,'directory_create_denied':True,'existing_file_write_open_denials':13},'current readonly receipt')
        else:
            need(o['optimization']==e['optimization'] and o['readonly']['actual_directory_create_denied'] is True and o['readonly']['actual_file_write_open_denials']==3,'independent readonly receipt')
    return {'fresh_preserved_runs':len(seen),'full_stdout_stderr_verified':True}

def run_code(root,name):
    flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
    r=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/name),'--require-readonly'],cwd=root,capture_output=True,timeout=60)
    need(r.returncode==0 and r.stderr==b'','fresh replay '+name+': '+r.stderr.decode('utf-8','replace'))
    kind='current' if name.startswith('current/') else 'independent'
    receipt=load((root/'verification/REPRODUCTION.json').read_bytes())
    matching=[e for e in receipt['runs'] if e['kind']==kind and type(e['optimization']) is int and e['optimization']==sys.flags.optimize]
    need(len(matching)==1,'one pinned full-output reference per kind and mode')
    expected_stdout=output_reference(root,matching[0]['stdout'])
    expected_stderr=output_reference(root,matching[0]['stderr'])
    compare_output(r.stdout,r.stderr,expected_stdout,expected_stderr)
    data=load(r.stdout);need(data['status']=='passed' and data['uid']==1000,'fresh replay result')
    if name.startswith('current/'):
        need(data['python_optimization']==sys.flags.optimize,'current mode')
        need(data['readonly']=={'actual_write_probes':True,'directory_create_denied':True,'existing_file_write_open_denials':13},'current actual readonly probes')
        need(data['checks']['mathematics']['degenerate']['strict_positivity_satisfied'] is False,'degenerate exclusion')
    else:
        need(data['optimization']==sys.flags.optimize and data['readonly']['actual_file_write_open_denials']==3,'independent actual readonly probes')
        need(len(data['semantic_controls']['rejected_semantic_overclaims'])==9 and data['semantic_controls']['Holder_counterexample']['ratio_lower_bound']=='128','independent semantic controls')
    return {'script':name,'exit_code':r.returncode,'full_stdout_stderr_match_pinned_reference':True,'recursive_exact_json_types_match':True,'stdout':stream(r.stdout),'stderr':stream(r.stderr)}

def verify(root,queue):
    need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000 required')
    scope=check_scope(root);sources=check_sources(root);receipts=check_receipts(root)
    proof=load((root/'QUEUE_PROOF.json').read_bytes());need(pin(queue.read_bytes())==proof['after'],'actual queue bytes')
    runs=[run_code(root,'current/check_claims.py'),run_code(root,'audit/independent_checks.py')]
    return {'schema':'dynamic-transport-mathematical-replay-v1','status':'PASS_SCOPED_PARTIAL_RESULTS','problem_id':30003937,'outcome':'exhausted','approaches':5,'full_target_resolved':False,'novelty_claim':False,'uid':os.geteuid(),'optimization':sys.flags.optimize,'default_absent_inputs':scope['default_checks'],'sources':sources,'receipts':receipts,'fresh_replays':runs}

if __name__=='__main__':
    try:
        p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--queue',required=True,type=Path);a=p.parse_args()
        print(json.dumps(verify(a.root.absolute(),a.queue.absolute()),indent=2,sort_keys=True))
    except Exception as e:print('REJECT: '+type(e).__name__+': '+str(e),file=sys.stderr);sys.exit(1)
