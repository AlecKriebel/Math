"""Independent private exact-family/source-path predicates; no production run."""
from pathlib import Path
import hashlib,json,datetime as dt,re,os
F=Path(__file__).absolute().parent
A=F.parent
COUNT=0
NEG=[]
OBS=[]
def need(v,m):
    global COUNT
    COUNT+=1
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def gate(root,literal,pin):
    need(type(literal) is str and type(pin) is str,'Typed source path/digest')
    p=Path(literal)
    need(p.is_absolute() and p.is_file() and not p.is_symlink(),'Absolute regular source')
    need(p.parent==root/'acceptance_preparation_family_v3' and p.name=='seal_final_evidence.py','Only literal new V3 source family and sealer filename')
    need(all(not q.is_symlink() for q in p.parents),'No symlink ancestor')
    need(sha(p.read_bytes())==pin,'Exact source SHA')
    return True
def reject(label,root,literal,pin):
    try:gate(root,literal,pin)
    except ValueError:NEG.append(label)
    else:raise ValueError('Accepted negative '+label)
def fn(text,start,end):return text[text.index(start):text.index(end,text.index(start))]
def main():
    source=F/'seal_final_evidence.py';pin=sha(source.read_bytes());need(gate(A,str(source),pin),'Genuine actual V3 source path positive')
    for n in ['acceptance_preparation_family','acceptance_preparation_family_v2']:
        reject('unpromoted_'+n,A,str(A/n/'seal_final_evidence.py'),pin)
    for literal in [str(F/'../acceptance_preparation_family_v3/seal_final_evidence.py'),str(F/'../../pr48_2961/acceptance_preparation_family_v3/seal_final_evidence.py'),str(F/'seal_final_evidence.py')+'/../seal_final_evidence.py','seal_final_evidence.py']:
        reject('traversal_or_relative_'+literal,A,literal,pin)
    reject('wrong_source_filename',A,str(F/'verify_post_acceptance.py'),sha((F/'verify_post_acceptance.py').read_bytes()))
    for value in ['0'*64,'',None,True,1]:reject('wrong_source_digest_'+repr(value),A,str(source),value)
    d=F/'private_path_fixtures_v3';d.mkdir(exist_ok=False)
    direct=d/'direct_source_link.py';direct.symlink_to(source)
    try:reject('actual_direct_source_symlink',A,str(direct),pin);OBS.append({'kind':'direct_symlink','actual_created':True,'rejected':True,'link':direct.relative_to(F).as_posix(),'target':source.relative_to(F).as_posix()})
    finally:direct.unlink()
    root=d/'model_audit';root.mkdir();target=root/'regular_source';target.mkdir();(target/'seal_final_evidence.py').write_bytes(b'private model sealer bytes\n');p=root/'acceptance_preparation_family_v3';p.symlink_to(target,target_is_directory=True)
    try:reject('actual_exact_parent_symlink_ancestor',root,str(p/'seal_final_evidence.py'),sha((target/'seal_final_evidence.py').read_bytes()));OBS.append({'kind':'symlink_ancestor_at_exact_expected_parent','actual_created':True,'rejected':True,'link':p.relative_to(F).as_posix()})
    finally:p.unlink()
    p.mkdir();model=p/'seal_final_evidence.py';model.write_bytes(b'private model sealer bytes\n');mpin=sha(model.read_bytes());need(gate(root,str(model),mpin),'Exact private V3 parent positive after removing symlink')
    reject('wrong_source_body_at_exact_parent',root,str(model),'0'*64)
    # Inspect operative text and complete body identity; never import/compile it.
    operator=(F/'capture_root_final_operation.py').read_text();folders=re.findall(r"script\.parent == A / '([^']+)'",operator);need(folders==['acceptance_preparation_family_v3'],'One exact current operator folder')
    need("script.name == 'seal_final_evidence.py'" in operator and 'assert all(not parent.is_symlink() for parent in script.parents)' in operator,'Filename and symlink ancestors are operative')
    need(operator.index('assert all(not parent.is_symlink()')<operator.index('dest.mkdir(')<operator.index('subprocess.Popen(argv'),'Reject unsafe source before capture creation/child launch')
    need('assert sha(source) == args.script_sha256' in operator and "argv = ['/usr/bin/python3', '-B', str(script), *tail]" in operator,'Original source SHA and literal argv chain retained')
    old=A/'acceptance_preparation_family_v2';guard=(F/'pr48_guards.py').read_text();oldguard=(old/'pr48_guards.py').read_text()
    for start,end in [('def write(','\n\ndef dump('),('def fresh_check(','\n\ndef native_git_snapshot')]:need(fn(guard,start,end)==fn(oldguard,start,end),'Supported M1 mechanism unchanged')
    for n in ['integrate_reviewed_partial.py','state_mirror_reconciliation.py','verify_post_acceptance.py','seal_final_evidence.py','ROOT_POST_CONTRACT.json']:need((F/n).read_bytes()==(old/n).read_bytes(),'Unrelated helper/science/accounting unchanged')
    need("'pr48-acceptance-source-closure/v3':" in guard and "inputs['actual_predecessor_PR47_completed'] is True" in guard,'V3 closure and genuine actual47 source binding')
    result={'schema':'pr48-private-exact-family-path-controls/v3','status':'PASS_PRIVATE_PATH_PREDICATES_ONLY','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'assertions':COUNT,'expected_negative_controls':NEG,'symlink_observations':OBS,'genuine_current_V3_sealer_path':str(source),'genuine_current_V3_sealer_sha256':pin,'operator_folder':'acceptance_preparation_family_v3','source_closure_schema':'pr48-acceptance-source-closure/v3','M1_write_fresh_check_unchanged':True,'actual_PR47_predecessor_completed':True,'production_imported_compiled_executed':False,'sealer_launched':False,'capture_root_final_operator_launched':False,'future48_ROOT_approval_created':False,'independent_SOURCE_review_supplied':False,'new_substantive_attempts':0,'audit_turns':0,'full_target_discovery_percent':0}
    with (F/'PRIVATE_PATH_CONTROLS_RESULT.json').open('x') as h:h.write(json.dumps(result,sort_keys=True,indent=2)+'\n');h.flush();os.fsync(h.fileno())
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
