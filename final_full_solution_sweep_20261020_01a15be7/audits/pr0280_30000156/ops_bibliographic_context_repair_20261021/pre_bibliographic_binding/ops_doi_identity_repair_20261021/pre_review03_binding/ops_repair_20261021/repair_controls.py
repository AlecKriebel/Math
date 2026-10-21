#!/usr/bin/env python3
"""P280-OPS-01/02 current guards: actual functions, synthetic boundaries, no assert."""
import copy
from contextlib import ExitStack
import json
from pathlib import Path
import subprocess
import sys
import tempfile
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
sys.path.insert(0,str(AUDIT))
import ops_binding as B
import publication_live_gates as G
import record_publication_ledger as D
import verify_published_files as V
CASES=[]
PROVIDER_CALLS=[]


def check(value,message):
    if not value:raise RuntimeError('CONTROL CHECK FAILED: '+message)


def forbidden(*args,**kwargs):
    PROVIDER_CALLS.append(True)
    raise RuntimeError('ACTUAL PROVIDER ACCESS FORBIDDEN')


def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True)+'\n')


def expect(label,fn,ok=False):
    try:value=fn()
    except Exception as ex:
        CASES.append({'case':label,'expected':'accept' if ok else 'reject','actual':'reject',
                      'exception':type(ex).__name__,'reason':str(ex)})
        check(not ok,label+' unexpectedly rejected '+str(ex))
    else:
        CASES.append({'case':label,'expected':'accept' if ok else 'reject','actual':'accept'})
        check(ok,label+' unexpectedly accepted')


def root_reconciliation():
    return {'pr':280,'root_identity_reconciliation_complete':True,'unresolved_leads':[],
            'release_manifest_sha256':B.RELEASE_SHA,'account_leads':[],'ledger_leads':[],
            'unrelated_local_state_exemptions':[]}


def gate_fixture(root,expected=999):
    records=([{'id':999,'metadata':{'title':B.TITLE},'files':[]}] if expected is not None else [])
    write(root/'account_complete.json',{'total':len(records),'records':records})
    return {'ledger_sha256':B.digest([B.HEADERS]),'started_utc':B.stamp(),'completed_utc':B.stamp(),
            'phase':'before_ledger' if expected else 'before_integration','expected_pr_head':'a'*40,
            'expected_deposit_id':expected,'read_only':True,'release_manifest_sha256':B.RELEASE_SHA,
            'release_files':B.release()['files'],'account_positive_control':'PASS_23174283',
            'raw_receipts':str(root),'receipt':str(root/'gate.json'),
            'account_complete_sha256':B.sha((root/'account_complete.json').read_bytes()),
            'account_complete_total':len(records),'unexpected_account_matches':[],
            'ledger_matches':[],'local_deposit_state_matches':[]}


def test_ledger_gate(work):
    root=work/'ledger_gate';root.mkdir()
    row=D.desired_row(999)
    ordinary=['Synthetic Vivaldi distinct model','','https://doi.org/10.5281/zenodo.101','Synthetic unrelated article']
    cases=[('exact_target_no_exemption',[row],[],True,True),
           ('exact_target_contradictory_exemption',[row],[row],True,False),
           ('exact_target_no_allowance',[row],[],False,False),
           ('duplicate_exact_target_rows',[row,row],[],True,False),
           ('duplicate_exact_rows_contradictory_exemption',[row,row],[row],True,False),
           ('ordinary_nontarget_digest_exemption',[ordinary],[ordinary],True,True),
           ('absence_target_no_exemptions',[],[],True,True)]
    changed=copy.deepcopy(row);changed[3]='Changed notes'
    notes=['Synthetic unrelated wording','','','See https://doi.org/10.5281/zenodo.999 in Notes']
    for label,value in [('changed_notes_same_DOI',changed),('current_DOI_only_in_Notes',notes)]:
        cases += [(label,[value],[],True,False),(label+'_contradictory_exemption',[value],[value],True,False)]
    for label,rows,exempt,allow,ok in cases:
        recon=root_reconciliation();recon['ledger_leads']=[{'values_sha256':B.digest(r),'disposition':'distinct_non_target'} for r in exempt]
        gate=gate_fixture(root);gate['ledger_matches']=[{'row':n,'values':r} for n,r in enumerate(rows,2)]
        write(root/'gate.json',gate);write(root/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',recon)
        with patch.object(G,'AUDIT',root):
            def invoke():
                acceptance=G.reconcile(gate,gate['phase'],'a'*40,999,allow)
                if rows==[row]:check(acceptance['target_rows']==[{'row':2,'values':row}],'target idempotence counted before exemptions')
                return acceptance
            expect('OPS01_gate_'+label,invoke,ok)


def test_ledger_append(work):
    root=work/'ledger_append';root.mkdir()
    row=D.desired_row(999);ordinary=['Synthetic birational distinct work','','','Unrelated']
    changed=copy.deepcopy(row);changed[3]='Changed notes'
    notes=['Synthetic otherwise unrelated','','','10.5281/zenodo.999 in Notes']
    cases=[('exact_existing_no_exemption',[row],[],True,0),
           ('exact_existing_contradictory_exemption',[row],[row],False,0),
           ('changed_notes_same_DOI',[changed],[],False,0),
           ('changed_notes_exempted',[changed],[changed],False,0),
           ('current_DOI_only_in_Notes',[notes],[],False,0),
           ('current_DOI_in_Notes_exempted',[notes],[notes],False,0),
           ('duplicate_exact_target_rows',[row,row],[],False,0),
           ('duplicates_exempted',[row,row],[row],False,0),
           ('ordinary_exemption_with_existing_target',[ordinary,row],[ordinary],True,0),
           ('absence_target_with_ordinary_exemption',[ordinary],[ordinary],True,1),
           ('absence_target_no_exemption',[],[],True,1)]
    for label,rows,exempt,ok,writes in cases:
        before=[B.HEADERS]+rows
        after=before+([row] if writes else [])
        for name in ['LEDGER_APPEND_INTENT.json','LEDGER_APPEND_RESPONSE.json','LEDGER_PUBLICATION_VERIFICATION.json']:
            if (root/name).exists():(root/name).unlink()
        recon=root_reconciliation();recon['ledger_leads']=[{'values_sha256':B.digest(r),'disposition':'distinct_non_target'} for r in exempt]
        write(root/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',recon)
        write(root/'ZENODO_PUBLIC_FILE_VERIFICATION.json',{'synthetic':True})
        gate=gate_fixture(root);gate['ledger_sha256']=B.digest(before)
        write(root/'gate.json',gate)
        public={'record':999,'all_public_file_bytes_match_reviewed':True,'doi_resolution':{'status':200},'release_manifest_sha256':B.RELEASE_SHA}
        reads=iter([before,after]);appends=[]
        def append(action,params,body):
            check(action=='append','synthetic append action')
            check((root/'LEDGER_APPEND_INTENT.json').exists(),'intent precedes synthetic append')
            appends.append(body)
            return {'updates':{'updatedRows':1,'updatedColumns':4,'updatedData':{'values':[row]}}}
        # Isolate append's OWN guard: deliberately bypass gate.reconcile here.
        with patch.object(D,'AUDIT',root),patch.object(D,'require_release_clearance',lambda:True),\
             patch.object(D,'verify_live',lambda i:public),patch.object(D,'collect',lambda *a,**k:(gate,{})),\
             patch.object(D,'read',lambda *a:next(reads)),patch.object(D,'gws',append):
            expect('OPS01_append_'+label,lambda:D.append_verified('a'*40,999),ok)
        check(len(appends)==writes,label+' exact synthetic append count')
        CASES[-1]['synthetic_append_calls']=len(appends)


def state_fixture(root,expected):
    repo=root/'repo';path=repo/'.zenodo-state/metadata-101-production.json'
    write(path,{'id':101,'metadata':{'title':'Synthetic birational unrelated article'}})
    data=path.read_bytes()
    other={'id':101,'metadata':{'title':'Synthetic birational distinct object'},
           'files':[{'key':'other.pdf','checksum':'md5:synthetic','size':1}]}
    records=[other]+([{'id':999,'metadata':{'title':B.TITLE},'files':[]}] if expected is not None else [])
    write(root/'account_complete.json',{'total':len(records),'records':records})
    gate=gate_fixture(root,expected)
    # gate_fixture writes its own account; restore the full known-distinct inventory.
    write(root/'account_complete.json',{'total':len(records),'records':records})
    gate.update(account_complete_total=len(records),account_complete_sha256=B.sha((root/'account_complete.json').read_bytes()),
                unexpected_account_matches=[{'id':101}],
                local_deposit_state_matches=[{'path':path.relative_to(repo).as_posix(),'sha256':B.sha(data),'deposit_id':101}])
    recon=root_reconciliation()
    recon['account_leads']=[{'record':101,'disposition':'distinct_non_target',
                             'metadata_and_files_sha256':B.digest(B.identity_projection(other))}]
    recon['unrelated_local_state_exemptions']=[{**gate['local_deposit_state_matches'][0],'disposition':'distinct_non_target'}]
    return repo,path,gate,recon


def test_states(work):
    def run(label,mutation=lambda repo,path,g,c:None,ok=False,expected=None):
        root=work/('state_'+str(len(CASES)));root.mkdir()
        repo,path,gate,recon=state_fixture(root,expected)
        mutation(repo,path,gate,recon)
        # Record every synthetic local state's bytes immediately before invoking
        # the actual gate. The gate must preserve even rejecting fixtures.
        states={p.relative_to(repo).as_posix():p.read_bytes() for p in repo.rglob('*') if p.is_file() and not p.is_symlink()}
        write(root/'gate.json',gate);write(root/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',recon)
        with patch.object(G,'AUDIT',root),patch.object(G,'REPO',repo):
            expect('OPS02_'+label,lambda:G.reconcile(gate,gate['phase'],'a'*40,expected),ok)
        after={p.relative_to(repo).as_posix():p.read_bytes() for p in repo.rglob('*') if p.is_file() and not p.is_symlink()}
        check(states==after,label+' unrelated synthetic states preserved')
        CASES[-1]['synthetic_state_files_unchanged']=True
    for expected in [None,999]:
        suffix='_before_integration' if expected is None else '_later_phase'
        run('valid_exact_explicit_exemption'+suffix,ok=True,expected=expected)
        run('no_exemption'+suffix,lambda r,p,g,c:c.update(unrelated_local_state_exemptions=[]),expected=expected)
        run('missing_exemption_field_defaults_reject'+suffix,lambda r,p,g,c:c.pop('unrelated_local_state_exemptions'),expected=expected)
    run('changed_observed_hash',lambda r,p,g,c:g['local_deposit_state_matches'][0].update(sha256='0'*64))
    run('changed_root_hash',lambda r,p,g,c:c['unrelated_local_state_exemptions'][0].update(sha256='0'*64))
    run('changed_actual_bytes',lambda r,p,g,c:p.write_bytes(p.read_bytes()+b' '))
    def changed_actual_id(repo,path,g,c):
        write(path,{'id':102});new=B.sha(path.read_bytes())
        c['unrelated_local_state_exemptions'][0]['sha256']=new
        g['local_deposit_state_matches'][0]['sha256']=new
    run('actual_ID_changed_even_with_rebound_bytes',changed_actual_id)
    run('changed_observed_ID',lambda r,p,g,c:g['local_deposit_state_matches'][0].update(deposit_id=102))
    run('unknown_root_ID',lambda r,p,g,c:c['unrelated_local_state_exemptions'][0].update(deposit_id=102))
    run('current_target_ID_exemption_forbidden',lambda r,p,g,c:c['unrelated_local_state_exemptions'][0].update(deposit_id=999),expected=999)
    run('wrong_disposition',lambda r,p,g,c:c['unrelated_local_state_exemptions'][0].update(disposition='target'))
    run('duplicate_exact_exemption',lambda r,p,g,c:c['unrelated_local_state_exemptions'].append(copy.deepcopy(c['unrelated_local_state_exemptions'][0])))
    def duplicate_id(repo,path,g,c):
        alternate=path.with_name('other-name.json');alternate.write_bytes(path.read_bytes())
        c['unrelated_local_state_exemptions'].append({**c['unrelated_local_state_exemptions'][0],'path':alternate.relative_to(repo).as_posix()})
    run('duplicate_ID_different_path_rejected',duplicate_id)
    run('duplicate_observed_path',lambda r,p,g,c:g['local_deposit_state_matches'].append(copy.deepcopy(g['local_deposit_state_matches'][0])))
    run('contradictory_duplicate_observed_path',lambda r,p,g,c:g['local_deposit_state_matches'].append({**g['local_deposit_state_matches'][0],'deposit_id':102}))
    run('root_entry_missing_path',lambda r,p,g,c:c['unrelated_local_state_exemptions'][0].pop('path'))
    run('observed_entry_missing_path',lambda r,p,g,c:g['local_deposit_state_matches'][0].pop('path'))
    run('root_entry_extra_field',lambda r,p,g,c:c['unrelated_local_state_exemptions'][0].update(extra='unknown'))
    run('observed_entry_extra_field',lambda r,p,g,c:g['local_deposit_state_matches'][0].update(extra='unknown'))
    for name,value in [('bool',True),('float',101.0),('string','101'),('zero',0),('negative',-101)]:
        run('root_ID_exact_integer_'+name,lambda r,p,g,c,value=value:c['unrelated_local_state_exemptions'][0].update(deposit_id=value))
    for name,value in [('absolute','/.zenodo-state/metadata-101-production.json'),
        ('parent_traversal','.zenodo-state/../metadata-101-production.json'),
        ('dot_alias','./.zenodo-state/metadata-101-production.json'),
        ('outside_state','elsewhere/metadata-101-production.json'),
        ('nested','.zenodo-state/nested/metadata-101-production.json'),
        ('wrong_extension','.zenodo-state/metadata-101-production.txt'),('backslash','.zenodo-state\\metadata-101-production.json')]:
        run('unsafe_root_path_'+name,lambda r,p,g,c,value=value:c['unrelated_local_state_exemptions'][0].update(path=value))
    def changed_root_path(repo,path,g,c):
        alternate=path.with_name('other-name.json');alternate.write_bytes(path.read_bytes())
        c['unrelated_local_state_exemptions'][0]['path']=alternate.relative_to(repo).as_posix()
    run('changed_root_path_same_safe_bytes_ID',changed_root_path)
    run('changed_observed_path_same_bytes_ID',lambda r,p,g,c:g['local_deposit_state_matches'][0].update(path='.zenodo-state/other-name.json'))
    def symlink_file(repo,path,g,c):
        alternate=repo/'synthetic-target.json';alternate.write_bytes(path.read_bytes());path.unlink();path.symlink_to(alternate)
    run('symlink_state_file',symlink_file)
    def symlink_dir(repo,path,g,c):
        state_dir=path.parent;alternate=repo/'synthetic-state-dir';state_dir.rename(alternate);state_dir.symlink_to(alternate,target_is_directory=True)
    run('symlink_state_directory',symlink_dir)
    run('missing_state_file',lambda r,p,g,c:p.unlink())
    run('directory_instead_of_state_file',lambda r,p,g,c:(p.unlink(),p.mkdir()))
    run('malformed_SHA',lambda r,p,g,c:c['unrelated_local_state_exemptions'][0].update(sha256='not a hash'))
    run('nonstring_SHA',lambda r,p,g,c:c['unrelated_local_state_exemptions'][0].update(sha256=101))
    run('state_exemptions_wrong_schema',lambda r,p,g,c:c.update(unrelated_local_state_exemptions={}))
    run('observed_states_wrong_schema',lambda r,p,g,c:g.update(local_deposit_state_matches={}))
    run('actual_state_not_JSON',lambda r,p,g,c:p.write_bytes(b'not JSON'))
    run('no_verified_account_binding',lambda r,p,g,c:c.update(account_leads=[]))
    run('account_metadata_and_fullfiles_hash_missing',lambda r,p,g,c:c['account_leads'][0].pop('metadata_and_files_sha256'))
    run('account_bound_projection_changed',lambda r,p,g,c:c['account_leads'][0].update(metadata_and_files_sha256='0'*64))
    run('account_not_explicit_distinct',lambda r,p,g,c:c['account_leads'][0].update(disposition='unreviewed'))
    def mixed_target(repo,path,g,c):
        g['local_deposit_state_matches'].append({'path':'.zenodo-state/current-target.json','sha256':'b'*64,'deposit_id':999})
    run('valid_unrelated_plus_legitimate_target_state',mixed_target,True,999)
    run('valid_unused_exemption_checks_actual_bytes',lambda r,p,g,c:g.update(local_deposit_state_matches=[]),True)


def main():
    with ExitStack() as guards:
        guards.enter_context(patch.object(subprocess,'run',forbidden))
        guards.enter_context(patch.object(V,'urlopen',forbidden))
        for method in ['request','create','upload','update','publish','get']:
            guards.enter_context(patch.object(B.zenodo.ZenodoClient,method,forbidden))
        with tempfile.TemporaryDirectory(dir=HERE,prefix='synthetic_') as temp:
            work=Path(temp)
            test_ledger_gate(work);test_ledger_append(work);test_states(work)
    check(not PROVIDER_CALLS,'zero actual provider attempts')
    result={'timestamp':B.stamp(),'optimization':sys.flags.optimize,'all_controls_passed':True,
            'controls':len(CASES),'accepted':sum(c['actual']=='accept' for c in CASES),
            'rejected':sum(c['actual']=='reject' for c in CASES),'actual_provider_access_attempts':len(PROVIDER_CALLS),
            'cases':CASES,'scope':'Actual repaired gate/append functions with synthetic provider/account/ledger/state fixtures only. Canonical/private/provider state unmodified.'}
    write(HERE/('REPAIR_CONTROLS_OPTIMIZED.json' if sys.flags.optimize else 'REPAIR_CONTROLS.json'),result)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))


if __name__=='__main__':main()
