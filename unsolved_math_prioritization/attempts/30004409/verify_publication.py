#!/usr/bin/env python3
"""Exact public-path auxiliary replay after fixed external authentication.
Imported smooth topology is not certified by this finite checker.
"""
import argparse,ast,hashlib,json,os,subprocess,sys
from pathlib import Path

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
def unstream(s):
    need(type(s) is dict and set(s)=={'type','bytes','sha256','text'},'typed complete stream schema')
    need(s['type']=='inline_utf8' and type(s['text']) is str and type(s['bytes']) is int and s['bytes']>=0,'stream types')
    b=s['text'].encode();need(len(b)==s['bytes'] and sha(b)==s['sha256'],'stream exact content');return b

def exact_json_equal(actual,expected,path='result'):
    need(type(actual) is type(expected),'exact JSON type mismatch '+path)
    if type(expected) is dict:
        need(set(actual)==set(expected),'exact JSON object keys '+path)
        for k in expected:exact_json_equal(actual[k],expected[k],path+'.'+k)
    elif type(expected) is list:
        need(len(actual)==len(expected),'exact JSON list length '+path)
        for i,(x,y) in enumerate(zip(actual,expected)):exact_json_equal(x,y,path+'['+str(i)+']')
    else:need(actual==expected,'exact JSON value mismatch '+path)

def compare_fresh_reference(fresh,reference):
    keys={'label','script','arguments','optimization','exit_code','stdout','stderr'}
    need(type(fresh) is dict and type(reference) is dict and set(fresh)==set(reference)==keys,'run comparison exact keys')
    for k in ['label','script','arguments','optimization','exit_code']:exact_json_equal(fresh[k],reference[k],'run.'+k)
    newout,oldout=unstream(fresh['stdout']),unstream(reference['stdout'])
    newerr,olderr=unstream(fresh['stderr']),unstream(reference['stderr'])
    if reference['exit_code']==0:exact_json_equal(load(newout),load(oldout),'stdout_json')
    need(newout==oldout,'exact complete stdout bytes differ');need(newerr==olderr,'exact complete stderr bytes differ')
    exact_json_equal(fresh,reference,'complete_run')
    return {'complete_stdout_bytes_equal':True,'complete_stderr_bytes_equal':True,'recursive_json_types_and_values_equal':True}

INDEPENDENT_MUTATIONS={'split_extension':'both half-turn lifts square to central full turn','commuting_generators':'quaternion conjugation relation','single_orientation_reversal':'64 Dahm homomorphism cases','central_detected':'64 Dahm homomorphism cases','wrong_exchange_lift':'eight distinct universal-cover endpoints','wrong_exchange_rotation':'correct exact half-turn rotations','connected_eightfold_cover':'eight decorations form two connected four-sheeted components'}
SUBMITTED_MUTATIONS={'wrong_scalar_product':'Q8 associativity','false_trivial_kernel':'Dahm kernel equals central C2','wrong_exchange_endpoint':'exchange preserves normal orientations'}
def cases():
    return [('author_positive','original/check_groups.py',[],0,None),('independent_positive','audit/independent_cover_check.py',[],0,None)]+[('independent_'+n,'audit/independent_cover_check.py',[n],1,f) for n,f in INDEPENDENT_MUTATIONS.items()]+[('submitted_'+n,'mutants/submitted_'+n+'.py',[],1,f) for n,f in SUBMITTED_MUTATIONS.items()]

LAUNCHER="from pathlib import Path; import sys; sys.argv=sys.argv[1:]; p=sys.argv[0]; exec(compile(Path(p).read_bytes(),p,'exec'),{'__name__':'__main__','__file__':p})"

def result_check(e,level):
    need(type(e) is dict and set(e)=={'label','script','arguments','optimization','exit_code','stdout','stderr'},'run schema')
    opts={c[0]:c for c in cases()};need(e['label'] in opts,'known label');label,script,args,rc,fail=opts[e['label']]
    need(type(e['optimization']) is int and e['optimization']==level and type(e['exit_code']) is int and e['exit_code']==rc,'run mode and exit')
    exact_json_equal(e['arguments'],args);need(e['script']==script,'script identity')
    out,err=unstream(e['stdout']),unstream(e['stderr'])
    if rc:
        need(out==b'' and err.startswith(b'Traceback (most recent call last):\n') and err.endswith(('RuntimeError: '+fail+'\n').encode()),'named semantic failure')
        need(b'/workspace/' not in err and b'/tmp/' not in err,'public-only traceback')
        return None
    need(err==b'','unexpected positive stderr');v=load(out)
    need(v['status']=='PASS' and type(v['uid']) is int and v['uid']==1000 and type(v['optimization']) is int and v['optimization']==level,'checker identity')
    if label=='author_positive':
        exact_json_equal(v,{'status':'PASS','uid':1000,'optimization':level,'q8_order_distribution':{'1':1,'2':1,'4':6},'signed_order_distribution':{'1':1,'2':5,'4':2},'dahm_image_order':4,'dahm_kernel_order':2,'q8_associativity_cases':512,'dahm_homomorphism_cases':64,'scope':'Auxiliary finite checks only; smooth topology is a credited theorem input.'})
    else:
        exact_json_equal(v,{'status':'PASS','uid':1000,'optimization':level,'mutant':'none','presentation_associativity_cases':512,'dahm_homomorphism_cases':64,'quaternion_lift_cases':64,'rotation_cover_cases':64,'sections_rejected':8,'motion_group_order':8,'dahm_image_order':4,'dahm_kernel_order':2,'labelled_group_order':4,'oriented_labelled_group_order':2,'full_decoration_sheets':8,'cover_components':2,'connected_cover_sheets':4,'limits':'Finite algebra and cover data only; smooth topology is imported.'})
    return v

def run_cases(root,level,references=None):
    rows=[];flags=[] if level==0 else ['-O' if level==1 else '-OO']
    for label,script,args,rc,fail in cases():
        p=subprocess.run([sys.executable,'-I','-S','-B',*flags,'-c',LAUNCHER,script,*args],cwd=root,capture_output=True,timeout=60)
        e={'label':label,'script':script,'arguments':args,'optimization':level,'exit_code':p.returncode,'stdout':stream(p.stdout),'stderr':stream(p.stderr)}
        result_check(e,level)
        if references is not None:compare_fresh_reference(e,references[(level,label)])
        rows.append(e)
    return rows

EXPECTED_SCOPE = {'Dahm_image': 'C2 x C2', 'Dahm_kernel': 'C2', 'RAAG': 'Z^2', 'approach_limit': 5, 'approaches': 0, 'dataset_contents_delivered': False, 'decision': 'ACCEPT_PRIOR_KNOWN_LITERAL_NEGATIVE_RESULT', 'fresh_corpus_rehash_during_publication': 'NOT_RUN', 'fresh_pdf_rehash_during_publication': 'NOT_RUN', 'fresh_pdf_retrieval_during_publication': 'NOT_RUN', 'full_decoration_cover_components': 2, 'full_decoration_cover_sheets': 8, 'general_forest_formula_solved': False, 'labelled_unoriented_cover_degree': 2, 'labelled_unoriented_fundamental_group': 'C4', 'literal_source_full_R3_quotient': True, 'motion_group': 'Q8', 'novelty_claim': False, 'oriented_labelled_connected_cover_degree': 4, 'oriented_labelled_fundamental_group': 'C2', 'outcome': 'already_solved', 'prior_known_credit': True, 'private_coordination_delivered': False, 'problem_id': 30004409, 'rank': 1073, 'revised_conjecture_solved': False, 'schema': 'hopf-tree-scoped-acceptance-v1', 'single_edge_in_source_scope': True, 'smooth_Q8_theorem_explicitly_imported': True, 'smooth_topology_machine_verified': False, 'source_bodies_delivered': False, 'source_problem_code': 'OWR-17471-016'}

def check_scope(root):
    s=load((root/'SCOPE.json').read_bytes());exact_json_equal(s,EXPECTED_SCOPE,'scope')
    p=load((root/'PROVENANCE.json').read_bytes())
    for n,e in p['preserved_files'].items():exact_json_equal(pin((root/n).read_bytes()),e,'preserved authored file '+n)
    need(sha((root/'original/MANIFEST.json').read_bytes())=='a9574bdd908b71ac3bb3fda27e68d3818679706e12847e5482b24b6e8540ae3a','original manifest anchor')
    need(sha((root/'historical/AUDIT_MANIFEST.json').read_bytes())=='842c7433b24296f2202fb83069ec94ece951db9e44e383339a74995e6c426b7c','historical audit anchor')
    for n,e in load((root/'original/MANIFEST.json').read_bytes())['files'].items():
        b=(root/'original'/n).read_bytes();exact_json_equal({'bytes':len(b),'sha256':sha(b)},e,'original manifest member')
    for n,e in load((root/'historical/AUDIT_MANIFEST.json').read_bytes())['files'].items():
        if n=='INDEPENDENT_VALIDATION.json':
            need(not (root/'audit'/n).exists(),'historical validation omitted');q=p['omitted_historical_evidence'][n]['pin'];exact_json_equal({k:q[k] for k in e},e,'omitted evidence pin')
        else:
            b=(root/'audit'/n).read_bytes();exact_json_equal({'bytes':len(b),'sha256':sha(b)},e,'historical audit authored member')
    for n in ['original/check_groups.py','audit/independent_cover_check.py','verify_publication.py','bootstrap.py','controls.py']:
        need(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse((root/n).read_text()))),'assert-free code')
    need('connected fourfold cover' in (root/'ACCEPTANCE.md').read_text() and 'degree is four, not two' in (root/'ACCEPTANCE.md').read_text(),'mandatory additive clarification')
    return s

def check_receipts(root):
    r=load((root/'verification/REPRODUCTION.json').read_bytes())
    need(r['schema']=='hopf-tree-fresh-runs-v1' and type(r['uid']) is int and r['uid']==1000,'fresh receipt identity')
    need(r['historical_runs_reused'] is False and r['tested_inputs_before']==r['tested_inputs_after'],'fresh unchanged')
    need(r['readonly']['actual_create_denied'] is True and r['readonly']['actual_existing_write_open_denials']==5,'actual permission probes')
    need(len(r['runs'])==36,'fresh runs inventory');seen=set()
    for e in r['runs']:
        key=(e['optimization'],e['label']);need(key not in seen and key[0] in (0,1,2),'unique mode/label');seen.add(key);result_check(e,key[0])
    need(seen=={(m,c[0]) for m in (0,1,2) for c in cases()},'complete fresh modes/labels')
    return {'fresh_runs':len(seen),'full_stdout_stderr_verified':True,'historical_runs_reused':False}

def verify(root):
    need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000 required');scope=check_scope(root);receipts=check_receipts(root)
    references={(e['optimization'],e['label']):e for e in load((root/'verification/REPRODUCTION.json').read_bytes())['runs']}
    return {'schema':'hopf-tree-mathematical-replay-v1','status':'PASS_PRIOR_KNOWN_LITERAL_NEGATIVE','problem_id':30004409,'outcome':'already_solved','approaches':0,'novelty_claim':False,'general_forest_formula_solved':False,'revised_conjecture_solved':False,'smooth_topology_machine_verified':False,'uid':os.geteuid(),'optimization':sys.flags.optimize,'receipts':receipts,'fresh_outputs_equal_mode_matched_references':True,'fresh_replays':run_cases(root,sys.flags.optimize,references)}
if __name__=='__main__':
    try:
        p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);a=p.parse_args()
        print(json.dumps(verify(a.root.absolute()),indent=2,sort_keys=True))
    except Exception as e:print('REJECT: '+type(e).__name__+': '+str(e),file=sys.stderr);sys.exit(1)
