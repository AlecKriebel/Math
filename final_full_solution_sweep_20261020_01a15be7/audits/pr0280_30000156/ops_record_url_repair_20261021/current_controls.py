#!/usr/bin/env python3
"""Whole-route and independent append safeguards, real current bodies, synthetic only."""
from contextlib import ExitStack
import copy
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
from unittest.mock import patch
import controls_support as S
CASES=[]
ALIASES=[
'https://zenodo.org/record/999/', 'https://zenodo.org:443/records/999',
'https://zenodo.org/records/./999', 'https://zenodo.org/records/999/export/json',
'https://ZENODO.ORG:443/record/999/?download=1#details',
'https://zenodo.org:443/records/./999?download=1#files',
'https://zenodo.org:443/records/999/export/json?x=1#metadata',
'https://zenodo.org/record/999/#files','https://zenodo.org/records/999/export/json#metadata',
'http://zenodo.org:80/record/999/', '//zenodo.org/records/999',
'https://zenodo.org./records/999','https://www.ZENODO.ORG:0443/records/999/',
'https://zenodo.org//records///999//export//json/?x=1#fragment',
'https://zenodo.org/records/%2e/999','https://zenodo.org/%72ecords/%39%39%39',
'https://zenodo.org/records/1/../999/export/json',
'https://ZENODO.ORG.:0443//api//records/%2e/999//export//json/?x=1#fragment',
'zenodo.org./record/999/','https://zenodo.org/RECORDS/999/versions/all',
'https://zenodo.org/records/000999/files/a.pdf',
'https://zenodo.org/records/999/new-future-subresource/a/b']
AMBIGUOUS=[
'https:/zenodo.org/records/999','https://zenodo%2eorg/records/999',
'https://%7Aenodo.org/records/999','https://www%2ezenodo.org/records/999',
'https://zenodo.org%2E/records/999',
'https://zenodo.org:8443/records/999','https://zenodo.org:bad/records/999',
'https://zenodo.org:/records/999','https://zenodo.org:99999/records/999',
'https://user@zenodo.org/records/999','https://user:password@zenodo.org/records/999',
'https://zenodo.org../records/999','https://[zenodo.org]/records/999',
'https:///zenodo.org/records/999','ftp://zenodo.org/records/999',
'//zenodo.org:80/records/999','https://zenodo.org/records%2F999',
'https://zenodo.org/records/%2539%2539%2539','https://zenodo.org/records/999%GG',
'https://zenodo.org/records/999%00','https://zenodo.org\\evil/records/999',
'https://zenodo.org/search?q=999','https://zenodo.org/',
'https://zenodo.org/api/record/999','https://zenodo.org/records/',
'https://zenodo.org/records/999abc','https://zenodo.org/records/999.other',
'https://zenodo.org/records/９９９','https://zenodo.org/records/../..',
'https://zenodo.org/records/'+('9'*70),
'https://zenodo.org/records/0', 'https://zenodo.org/records/%GG',
'https://shortdoi.org/abcde','https://doi.org/abcde','10/abcde']
DISTINCT=[
'https://zenodo.org/record/9990/','https://zenodo.org:443/records/1999',
'https://zenodo.org/records/./9999/export/json',
'https://zenodo.org/records/%39%39%39%30','https://zenodo.org/records/999/../9990',
'https://zenodo.org/records/1999?record=999#999',
'10.5281/zenodo.0999','10.5281/zenodo.9990','10.5281/zenodo.1999',
'10.5281/zenodo.999abc','10.5281/zenodo.999/extra',
'https://evilzenodo.org/records/999','https://zenodo.org.evil.invalid/records/999',
'https://zenodo.org@evil.invalid/records/999','https://zenodo．org/records/999']
RECOGNIZED=['https://zenodo.org/records/999','https://zenodo.org/record/999',
'https://zenodo.org/records/999/files/paper.pdf','https://zenodo.org/records/999?download=1#files',
'https://zenodo.org/api/records/999?x=1#metadata','10.5281/ZENODO.999',
'https://doi.org/10.5281/zenodo%2E999']


def direct_append(root,modules,alias,column,exempt):
    B,P,G,V,D=modules;root.mkdir();row=['','','',''];row[column]=alias
    before=[B.HEADERS,row];desired=D.desired_row(999);appends=[];reads=iter([before,before+[desired]])
    gate={'started_utc':B.stamp(),'ledger_sha256':B.digest(before),'receipt':str(root/'gate.json')}
    S.write(root/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',{'ledger_leads':[{'values_sha256':B.digest(row),'disposition':'distinct_non_target'}] if exempt else []})
    S.write(root/'ZENODO_PUBLIC_FILE_VERIFICATION.json',{'synthetic':True})
    public={'record':999,'all_public_file_bytes_match_reviewed':True,'doi_resolution':{'status':200},'release_manifest_sha256':B.RELEASE_SHA}
    def append(*args):appends.append(args);raise RuntimeError('Unexpected duplicate append')
    with patch.object(D,'AUDIT',root),patch.object(D,'require_release_clearance',lambda:True),\
         patch.object(D,'verify_live',lambda i:public),patch.object(D,'collect',lambda *a,**k:(gate,{})),\
         patch.object(D,'read',lambda *a:next(reads)),patch.object(D,'gws',append):
        try:D.append_verified('a'*40,999)
        except RuntimeError as error:reason=str(error)
        else:raise RuntimeError('Append bypass layer accepted conflicting/ambiguous official URL')
    S.check(not appends,'independent append must stop before mutation')
    return reason


def before_allocation(root,modules,alias,column,exempt):
    B,P,G,V,D=modules;root.mkdir();row=['birational','','',''];row[column]=alias
    reads=[]
    def read(args):reads.append(args);return {'values':[B.HEADERS,row]}
    with patch.object(P,'ROOT',root),patch.object(P,'REPO',root),patch.object(P,'PRIVATE',root/'private'),\
         patch.object(P,'verify_destination',lambda:True),patch.object(P,'read_command',read),\
         patch.object(P.zenodo,'token_for',lambda *a:'synthetic'),\
         patch.object(P.zenodo,'ZenodoClient',lambda *a:(_ for _ in ()).throw(RuntimeError('Advanced past unresolved identity'))):
        try:P.gather('before_integration','a'*40,None)
        except RuntimeError as error:
            S.check('review' in str(error).lower(),'unknown recognized alias fails for identity review before allocation')
            reason=str(error)
        else:raise RuntimeError('Unknown recognized alias silently passed initial collector')
    S.check(len(reads)==1,'collector stops after full sheet before further providers')
    # The gate independently scans a matched row before digest exemptions even
    # with no expected record ID; no collector shortcut is assumed here.
    S.write(root/'account_complete.json',{'total':0,'records':[]})
    recon={'pr':280,'root_identity_reconciliation_complete':True,'unresolved_leads':[],
           'release_manifest_sha256':B.RELEASE_SHA,'account_leads':[],'unrelated_local_state_exemptions':[],
           'ledger_leads':[{'values_sha256':B.digest(row),'disposition':'distinct_non_target'}] if exempt else []}
    S.write(root/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',recon)
    gate={'started_utc':B.stamp(),'completed_utc':B.stamp(),'phase':'before_integration','expected_pr_head':'a'*40,
          'expected_deposit_id':None,'read_only':True,'release_manifest_sha256':B.RELEASE_SHA,'release_files':B.release()['files'],
          'account_positive_control':'PASS_23174283','raw_receipts':str(root),'receipt':str(root/'gate.json'),
          'account_complete_sha256':B.sha((root/'account_complete.json').read_bytes()),'account_complete_total':0,
          'unexpected_account_matches':[],'ledger_matches':[{'row':2,'values':row}],'local_deposit_state_matches':[]}
    S.write(root/'gate.json',gate)
    with patch.object(G,'AUDIT',root):
        try:G.reconcile(gate,'before_integration','a'*40,None)
        except RuntimeError as error:S.check('review' in str(error).lower(),'gate alias review before exemption/allocation')
        else:raise RuntimeError('Gate silently exempted an unknown official alias before allocation')
    return reason


def main():
    modules=S.implementation(False);B,P,G,V,D=modules
    with ExitStack() as guards:
        guards.enter_context(patch.object(subprocess,'run',S.forbidden));guards.enter_context(patch.object(socket,'socket',S.forbidden))
        guards.enter_context(patch.object(V,'urlopen',S.forbidden))
        for method in ['request','create','upload','update','publish','get']:
            guards.enter_context(patch.object(B.zenodo.ZenodoClient,method,S.forbidden))
        with tempfile.TemporaryDirectory(dir=S.HERE,prefix='new_synthetic_') as temp:
            root=Path(temp)
            for alias in ALIASES:
                for column in range(4):
                    for exempt in [False,True]:
                        row=['','','',''];row[column]=alias
                        result=S.run_pipeline(root/str(len(CASES)),modules,[row],True,exempt)
                        S.check(result['collector_matching_rows']==1 and not result['gate_accepted'] and result['append_calls']==0,'full alias pipeline must reject current identity')
                        CASES.append({'case':'full_pipeline_alias','url':alias,'column':column+1,'exemption':exempt,**result})
                        reason=direct_append(root/str(len(CASES)),modules,alias,column,exempt)
                        CASES.append({'case':'independent_append_alias','url':alias,'column':column+1,'exemption':exempt,'append_calls':0,'reason':reason})
            for alias in AMBIGUOUS:
                for column in range(4):
                    for exempt in [False,True]:
                        reason=direct_append(root/str(len(CASES)),modules,alias,column,exempt)
                        CASES.append({'case':'independent_append_ambiguous','url':alias,'column':column+1,'exemption':exempt,'append_calls':0,'reason':reason})
                        reason=before_allocation(root/str(len(CASES)),modules,alias,column,exempt)
                        CASES.append({'case':'collector_and_gate_before_allocation','url':alias,'column':column+1,'exemption':exempt,'append_calls':0,'reason':reason})
            for alias in DISTINCT:
                S.check(not B.target_in_row([alias],999),'nearby IDs/hostnames are not target')
                result=S.run_pipeline(root/str(len(CASES)),modules,[['','','',alias]],True)
                S.check(result['collector_matching_rows']==0 and result['gate_accepted'] and result['append_calls']==1 and result['append_returned_verified'],'verified absence remains valid for distinct IDs')
                CASES.append({'case':'distinct_identity','value':alias,**result})
            for alias in RECOGNIZED:
                result=S.run_pipeline(root/str(len(CASES)),modules,[['','','',alias]],True)
                S.check(result['collector_matching_rows']==1 and not result['gate_accepted'] and result['append_calls']==0,'seven recognized rejection controls')
                CASES.append({'case':'recognized_rejection_control','value':alias,**result})
            for alias in ALIASES+AMBIGUOUS:
                desired=D.desired_row(999)
                result=S.run_pipeline(root/str(len(CASES)),modules,[],True,after_override=[B.HEADERS,['','','',alias],desired])
                S.check(result['append_calls']==1 and not result['append_returned_verified'],'post-read alias cannot yield false uniqueness')
                CASES.append({'case':'readback_introduced_alias','value':alias,**result})
            desired=D.desired_row(999)
            result=S.run_pipeline(root/str(len(CASES)),modules,[desired],True)
            S.check(result['gate_accepted'] and result['append_calls']==0 and result['append_returned_verified'],'exact literal idempotence')
            CASES.append({'case':'exact_literal_idempotence',**result})
            result=S.run_pipeline(root/str(len(CASES)),modules,[],True)
            S.check(result['append_calls']==1 and result['append_returned_verified'],'empty absence one append')
            CASES.append({'case':'absence_one_append',**result})
            try:B.row_identity_leads(['10.5281/zenodo.999','https://zenodo.org/unknown'])
            except RuntimeError:CASES.append({'case':'later_cell_not_shortcircuited','actual':'review_required'})
            else:raise RuntimeError('First matching cell hid later ambiguous URL')
    S.check(not S.ATTEMPTS,'zero actual providers')
    result={'timestamp':B.stamp(),'optimization':sys.flags.optimize,'controls':len(CASES),'all_controls_passed':True,
            'actual_provider_access_attempts':len(S.ATTEMPTS),'case_counts':{k:sum(c['case']==k for c in CASES) for k in sorted({c['case'] for c in CASES})},'cases':CASES}
    S.write(S.HERE/('CURRENT_CONTROLS_OPTIMIZED.json' if sys.flags.optimize else 'CURRENT_CONTROLS.json'),result)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))


if __name__=='__main__':main()
