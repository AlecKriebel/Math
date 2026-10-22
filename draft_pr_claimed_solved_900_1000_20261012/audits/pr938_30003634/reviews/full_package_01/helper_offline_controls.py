"""Bounded offline tests of inspected helper logic; no operational main calls."""
import ast, copy, datetime, hashlib, importlib.util, json, pathlib, types
from authenticate import A,C,O,HEAD,FREEZE,MANIFEST,require,sha
P=A.parent.parent
def module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
def dump(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(obj,indent=2)+'\n')
def extract(m,path,start_name,stop_name,parameters,name):
    tree=ast.parse(path.read_text());main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    def assignment(n,key):return isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==key for t in n.targets)
    i=next(i for i,n in enumerate(main.body) if assignment(n,start_name));j=next(i for i,n in enumerate(main.body) if assignment(n,stop_name))
    body=copy.deepcopy(main.body[i:j]);body.append(ast.Return(value=ast.Call(func=ast.Name(id='locals',ctx=ast.Load()),args=[],keywords=[])))
    fn=ast.FunctionDef(name=name,args=ast.arguments(posonlyargs=[],args=[ast.arg(arg=p) for p in parameters],kwonlyargs=[],kw_defaults=[],defaults=[]),body=body,decorator_list=[])
    tree=ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[]));ns=m.__dict__.copy();exec(compile(tree,str(path)+':extracted','exec'),ns);return ns[name],ns
def reviews():
    helper=module('review_accept_offline',P/'accept_pr938.py');freeze=json.loads((C/'PREPUBLICATION_FREEZE.json').read_text())
    gate,ns=extract(helper,P/'accept_pr938.py','reviews','disposition',['args','freeze'],'gate')
    fixture=O/'private/helper_fixtures/reviews';fixture.mkdir(parents=True,exist_ok=True);ns['A']=fixture;ns['D']=fixture/'publication'
    def make(n,issues=None,sealed=True):
        folder=fixture/'reviews'/('full_package_'+str(n).zfill(2));folder.mkdir(parents=True,exist_ok=True)
        result={'pr':938,'problem_id':'30003634','original_pr_head':HEAD,'clean_context':True,'full_reproducer_completed':True,'started_utc':f'2026-10-15T08:{n:02d}:00+00:00','completed_utc':f'2026-10-15T08:{n:02d}:30+00:00','candidate_revision':1,'candidate_pins':{'freeze':FREEZE,'manifest':MANIFEST,'pdf':freeze['files']['output/pdf/note.pdf']['sha256']},'inspected_helper_hashes':freeze['future_helpers'],'required_issues':issues or [],'optional_issues':[],'clean_for_preprint':not bool(issues),'mathematical_remaining_gap_for_stated_theorem':None,'prior_issue_resolution':{}}
        dump(folder/'RESULT.json',result)
        records={}
        if sealed:
            b=(folder/'RESULT.json').read_bytes();records={'RESULT.json':{'bytes':len(b),'sha256':sha(b)}}
        dump(folder/'MANIFEST.json',{'files':records,'explicit_public_allowlist':list(records)})
        return str(n)+':'+sha((folder/'MANIFEST.json').read_bytes())
    def invoke(specs):return gate(types.SimpleNamespace(review=specs,freeze=FREEZE),freeze)
    a,b=make(1),make(2);require(len(invoke([a,b])['reviews'])==2,'valid gate fixture')
    hidden=make(2,[{'id':'HIDDEN-R2','finding':'Unresolved issue in omitted round'}]);third=make(3)
    skipped=invoke([a,third]);require(len(skipped['reviews'])==2 and not skipped['prior_ids'],'skip counterexample')
    u1,u2=make(1,sealed=False),make(2,[{'id':'R-UNSEALED','finding':'Original unsealed failure'}],sealed=False)
    original_pin=u2.split(':')[1]
    file=fixture/'reviews/full_package_02/RESULT.json';r=json.loads(file.read_text());r.update(required_issues=[],clean_for_preprint=True);dump(file,r)
    unsealed=invoke([u1,u2]);require(sha((file.parent/'MANIFEST.json').read_bytes())==original_pin,'unsealed map changed')
    return [{'case':'valid_consecutive_sealed_reviews','accepted':True},
            {'case':'round01_and03_omit_unresolved_round02','accepted_by_current_gate':True,'required_fix':'Require complete chronological consecutive round history, including every intervening required/optional issue.'},
            {'case':'empty_allowlist_with_unsealed_mutated_RESULT','accepted_by_current_gate':True,'external_manifest_pin_unchanged':True,'required_fix':'Require RESULT.json and mandatory review artifacts in authenticated public map before loading decisive verdict.'}]
def equality():
    m=module('release_verify_offline',C/'verify_package.py');tree=ast.parse((C/'verify_package.py').read_text())
    worker=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='worker')
    comparison=next(n for n in ast.walk(worker) if isinstance(n,ast.Compare) and isinstance(n.left,ast.Name) and n.left.id=='author')
    expected=ast.literal_eval(comparison.comparators[0]);changed=copy.deepcopy(expected);changed['n']=True;changed['m']=3.0;changed['goeritz_inertia'][2]=False
    ordinary=changed==expected;strict=False
    try:m.equivalent(changed,expected)
    except RuntimeError:strict=True
    require(ordinary and strict,'scalar equality control')
    return {'case':'author_summary_bool_float_substitution','plain_equality_accepts':ordinary,'strict_recursive_equivalent_rejects':strict,'frozen_author_verifier_unchanged_and_emits_ints':True,'classification':'optional consistency hardening to match README scalar-type claim'}
def merge_description():
    m=module('merge_offline',P/'merge_pr938.py');gate,ns=extract(m,P/'merge_pr938.py','decision','snapshot',[],'preflight')
    fixture=O/'private/helper_fixtures/merge';fixture.mkdir(parents=True,exist_ok=True)
    freeze={'files':{},'pr_description_sha256':sha(b'Accepted description')};dump(fixture/'publication/PREPUBLICATION_FREEZE.json',freeze)
    dump(fixture/'PUBLICATION_DISPOSITION.json',{'decision':'PREPARE_ALL_FINITE_DERIVED_DEPTH_RESEARCH_NOTE'})
    dump(fixture/'ACCEPTANCE.json',{'accepted':True,'original_pr_head':HEAD,'full_package_reviews':[{},{}],'freeze_sha256':sha((fixture/'publication/PREPUBLICATION_FREEZE.json').read_bytes())})
    ns['A']=fixture;ns['view']=lambda:{'headRefOid':HEAD,'state':'OPEN','isDraft':True,'body':'Changed unreviewed description'}
    result=gate();require(result['pr']['body']=='Changed unreviewed description','merge description counterexample')
    fields=[]
    m.run=lambda args: (fields.append(args[-1]) or json.dumps({'headRefOid':HEAD}))
    m.view()
    require(all('body' not in field.split(',') for field in fields),'unexpected merge description check')
    return {'case':'merge_preflight_changed_description','preflight_accepts_changed_body':True,'view_requests_body':False,'required_fix':'Read live body and compare exact accepted freeze hash before ready/merge.'}
def receipt_links():
    fixture=O/'private/helper_fixtures/receipts';pubdir=fixture/'publication';pubdir.mkdir(parents=True,exist_ok=True)
    freeze={'pr':938,'problem_id':'30003634','original_pr_head':HEAD,'files':{}}
    files=[]
    for name,data in [('note.pdf',b'private PDF fixture'),('bundle.zip',b'private archive fixture')]:
        (pubdir/name).write_bytes(data);freeze['files'][name]={'bytes':len(data),'sha256':sha(data)};files.append({'name':name,'size':len(data),'sha256':sha(data)})
    desc={'metadata':{'title':'offline fixture'},'files':[{'path':'note.pdf','name':'note.pdf'},{'path':'bundle.zip','name':'bundle.zip'}]};dump(pubdir/'zenodo-deposit.json',desc);freeze['files']['zenodo-deposit.json']={'bytes':(pubdir/'zenodo-deposit.json').stat().st_size,'sha256':sha((pubdir/'zenodo-deposit.json').read_bytes())}
    dump(pubdir/'PREPUBLICATION_FREEZE.json',freeze);pin=sha((pubdir/'PREPUBLICATION_FREEZE.json').read_bytes())
    accepted={'accepted':True,'original_pr_head':HEAD,'full_package_reviews':[{},{}],'freeze_sha256':pin,'files':freeze['files']}
    merge={'number':938,'state':'MERGED','headRefOid':HEAD,'mergeCommit':{'oid':'1'*40}}
    publication={'id':12345,'state':'published','doi':'10.5281/zenodo.12345','record_url':'https://zenodo.org/records/12345','files':files}
    intent={'action':'publish','pr':938,'accepted_freeze_sha256':pin,'merged_commit':'1'*40,'descriptor_sha256':freeze['files']['zenodo-deposit.json']['sha256']}
    dump(pubdir/'ZENODO_PUBLISH_INTENT.json',intent);dump(pubdir/'ZENODO_STAGE.json',{'id':12345,'files':files});dump(pubdir/'ZENODO_INSPECT.json',publication)
    tracker={'confirmed':True,'readback_matches':True,'pr':938,'problem_id':'30003634','original_pr_head':HEAD,'merged_head':HEAD,'merge_commit':'1'*40,'accepted_freeze_sha256':pin,'doi':publication['doi'],'zenodo_record_id':12345,'spreadsheet_id':'1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20','gid':1254632077,'tab_title':'Math Puzzles','row':['source','','https://doi.org/'+publication['doi'],'notes'],'updated_range':"'Math Puzzles'!A10:D10"};dump(fixture/'TRACKER_READBACK.json',{'values':[tracker['row']]})
    native={'push_confirmed':True,'published_event':{'id':'30003634','pr':938,'doi':publication['doi'],'original_pr_head':HEAD,'accepted_freeze_sha256':pin,'merged_commit':'1'*40,'zenodo_record_id':12345,'evidence':{'tracker_range':tracker['updated_range']}}}
    rows=[]
    for script in ['append_pr938_tracker.py','update_pr938_publication_ledger.py']:
        m=module('link_'+script.replace('.py',''),P/script);m.verify_receipt_links(fixture,publication,merge,accepted,tracker)
        m.verify_receipt_links(fixture,publication,merge,accepted,tracker,native)
        wrong_native=copy.deepcopy(native);wrong_native['published_event']['zenodo_record_id']=999
        rejected=False
        try:m.verify_receipt_links(fixture,publication,merge,accepted,tracker,wrong_native)
        except RuntimeError:rejected=True
        require(rejected,'crossnative receipt accepted');rows.append({'script':script,'case':'native_cross_publication_record','rejected':True})
        for label,section,key,value in [('publication_cross_ID','publication','id',999),('merge_cross_head','merge','headRefOid','0'*40),('tracker_cross_target','tracker','problem_id','other'),('tracker_cross_gid','tracker','gid',0),('acceptance_cross_freeze','accepted','freeze_sha256','0'*64)]:
            parts={'publication':copy.deepcopy(publication),'merge':copy.deepcopy(merge),'accepted':copy.deepcopy(accepted),'tracker':copy.deepcopy(tracker)};parts[section][key]=value;rejected=False
            try:m.verify_receipt_links(fixture,parts['publication'],parts['merge'],parts['accepted'],parts['tracker'])
            except RuntimeError:rejected=True
            require(rejected,'crossreceipt accepted '+label);rows.append({'script':script,'case':label,'rejected':True})
        # The current tracker receipt checks title/gid, but does not parse its A1
        # returned range. This control is a local-receipt limitation only.
        wrong=copy.deepcopy(tracker);wrong['updated_range']="'Other tab'!A10:D10";m.verify_receipt_links(fixture,publication,merge,accepted,wrong)
        rows.append({'script':script,'case':'tracker_range_other_tab','accepted_by_current_link_checker':True,'classification':'optional destination consistency hardening'})
    ledger=module('ledger_byte_preserve',P/'update_pr938_publication_ledger.py')
    raw='{\n "other" : {"odd spacing": 3},\n "30003634": {"turns_used": 1},\n "tail": [1,2] \n}\n';new=ledger.replace_entry(raw,'30003634',{'turns_used':2})
    require(new.split('"30003634"')[0]==raw.split('"30003634"')[0] and new[new.index(',\n "tail"'):]==raw[raw.index(',\n "tail"'):],'other state entry bytes changed')
    absent='{ "other": 7 }\n';added=ledger.replace_entry(absent,'30003634',{'turns_used':2});require('"other": 7' in added and json.loads(added)['other']==7,'absent selected entry control')
    rows.append({'case':'replace_selected_state_entry','other_entry_bytes_preserved':True,'absent_target_supported':True})
    return rows
def accounting():
    folder=A/'strengthening/unsolved_math_prioritization/attempts/30003634';receipt=json.loads((folder/'NATIVE_TURN_RECEIPT.json').read_text());history=[json.loads(x) for x in (folder/'NATIVE_HISTORY.jsonl').read_text().splitlines()]
    require([r['turns_used'] for r in history]==[0,1,1,2],'native counter sequence');require([x['arguments'][0] for x in receipt['commands']]==['status','turn','status','turn'],'native command sequence')
    require(history[-1]==json.loads((folder/'ATTEMPT_LEDGER.json').read_text()),'native final state differs')
    require(sha((A.parents[2]/'unsolved_math_prioritization/queue.py').read_bytes())==receipt['unmodified_queue_py_sha256'],'shared queue code differs')
    return {'counts':[0,1,1,2],'turn_commands':2,'limit':5,'current_known_turns':2,'original_observed_turns':1,'new_mechanism_turns':1,'verification_turns':0,'third_status_inherits_event_without_count_increment':history[2]['event']=='proof_attempt_turn' and 'candidate_turn' not in history[2],'claim_about_independently_observing_original_processes':False}
def main(output=None):
    out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'operational_main_actions_called':False,'all_mutations_private_fixtures_only':True,'review_gate':reviews(),'scalar_type_control':equality(),'merge_description':merge_description(),'receipt_and_preservation_controls':receipt_links(),'accounting':accounting()}
    if output:dump(pathlib.Path(output),out)
    print(json.dumps(out,indent=2))
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--output');args=ap.parse_args();main(args.output)
