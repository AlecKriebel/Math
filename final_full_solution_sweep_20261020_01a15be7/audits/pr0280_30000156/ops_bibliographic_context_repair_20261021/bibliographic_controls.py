#!/usr/bin/env python3
"""Actual isolated proposed helpers; synthetic providers plus cached sheet read."""
from contextlib import ExitStack
import hashlib
import json
from pathlib import Path
import socket
import subprocess
import sys
import tempfile
from unittest.mock import patch
import controls_support as S

BASE='OWR 10/2016 pp.479–481. https://doi.org/10.4171/OWR/2016/10'
VALID=[BASE,'owr 10/2016; 10.4171/owr/2016/10',
       'OWR\t10/2016. DOI:10.4171/OWR/2016/10',
       '10.4171/OWR/2016/10 — OWR 10/2016',
       '(OWR 10/2016) https://doi.org/10.4171/OWR/2016/10?download=1#page',
       'OWR 10/2025 ; https://doi.org/10.4171/OWR/2025/10',
       'OWR 10/2016 https://doi.org/10.4171/OWR/2016/10 ; unrelated 10.1234/example']
AMBIGUOUS=[
 '10/2016','doi:10/2016','10/2016 date','a fraction 10/2016','OWR 10/2016',
 'OWR 10/2016; 10.4171/OWR/2015/10','OWR 10/2016; 10.4171/OWR/2016/11',
 'OWR 10/2016; 10.4171/OWR/2016/010','OWR 10/2016; 10.4171/OWR/2016/100',
 'OWR 10/2016; 10.4171/OWR/2016/10.extra','OWR 10/2016; 10.4171/OWR/2016/10/extra',
 'OWR 10/2016; 110.4171/OWR/2016/10','OWR 10/2016; 10.4171/OWR/20160/10',
 'OWR 10/2016; 10.4171/OWR/2016/10 ; 10.4171/OWR/2016/10',
 'OWR 10/2016; 10.4171/OWR/2016/10 ; 10.4171/OWR/2017/10',
 'OWR 10/2016; OWR 10/2016; 10.4171/OWR/2016/10',
 'OWR 10/2016; 10.4171/OWR/2016/10 ; 10.4171/OWR/bad/10',
 'OWR 10/2016; 10.4171/%4fWR/2016/10',
 '%4fWR 10/2016; 10.4171/OWR/2016/10',
 'OWR 10%2f2016; 10.4171/OWR/2016/10',
 'OTHER 10/2016; 10.4171/OWR/2016/10',
 'OWR 10/2016extra; 10.4171/OWR/2016/10',
 BASE+' ; 10/2017',BASE+' ; doi:10/2016',BASE+' ; 10/abcde',
 BASE+' ; 10%2Fabcde',BASE+' ; 10%252fabcde',
 BASE+' ; https://shortdoi.org/abcde',BASE+' ; https://doi.org/abcde',
 BASE+' ; https://doi.org/10/2016',BASE+' ; 10/2016/extra',
 BASE+' ; 10/2016_foo',BASE+' ; 10/９９９',BASE+' ; 10/',
 BASE+' ; https://zenodo.org/unknown',
 BASE+' ; 10.4171/%4fWR/2017/10',BASE+' ; %31%30.4171/OWR/2016/10',
 BASE+' ; 10.4171%252fOWR%252f2017%252f10',
 BASE+' ; //shortdoi.org/abcde',BASE+' ; https://shortdoi.org:443/abcde',
 BASE+' ; //doi.org/abcde',BASE+' ; https://DOI.ORG:443/./abcde',
 BASE+' ; https://doi.org/10/2016/',BASE+' ; shortdoi.org/abcde',
 BASE+' ; shortdoi.org./abcde',BASE+' ; https:/shortdoi.org/abcde',
 BASE+' ; https:/doi.org/abcde',BASE+' ; https://shortdoi.org\\evil/abcde']
CASES=[]


def direct(root,modules,rows,exempt):
    B,P,G,V,D=modules;root.mkdir();before=[B.HEADERS]+rows;desired=D.desired_row(999);appends=[]
    gate={'started_utc':B.stamp(),'ledger_sha256':B.digest(before),'receipt':str(root/'gate.json')}
    S.write(root/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',{'ledger_leads':[{'values_sha256':B.digest(r),'disposition':'distinct_non_target'} for r in rows] if exempt else []})
    S.write(root/'ZENODO_PUBLIC_FILE_VERIFICATION.json',{'synthetic':True})
    public={'record':999,'all_public_file_bytes_match_reviewed':True,'doi_resolution':{'status':200},'release_manifest_sha256':B.RELEASE_SHA}
    def append(*args):appends.append(args);raise RuntimeError('Unexpected duplicate mutation')
    with patch.object(D,'AUDIT',root),patch.object(D,'require_release_clearance',lambda:True),\
         patch.object(D,'verify_live',lambda i:public),patch.object(D,'collect',lambda *a,**k:(gate,{})),\
         patch.object(D,'read',lambda *a:before),patch.object(D,'gws',append):
        try:D.append_verified('a'*40,999)
        except RuntimeError as error:reason=str(error)
        else:raise RuntimeError('Independent append accepted unresolved code')
    S.check(not appends,'zero synthetic append for unresolved code')
    return reason


def before_allocation(root,modules,rows,exempt):
    B,P,G,V,D=modules;root.mkdir();reads=[]
    def read(args):reads.append(args);return {'values':[B.HEADERS]+rows}
    with patch.object(P,'ROOT',root),patch.object(P,'PRIVATE',root/'private'),patch.object(P,'REPO',root),\
         patch.object(P,'verify_destination',lambda:True),patch.object(P,'read_command',read),\
         patch.object(P.zenodo,'token_for',lambda *a:'synthetic'),patch.object(P.zenodo,'ZenodoClient',lambda *a:(_ for _ in ()).throw(RuntimeError('Reached account after unresolved identity'))):
        try:P.gather('before_integration','a'*40,None)
        except RuntimeError as error:S.check('review' in str(error).lower(),'collector must reject identity before account/allocation')
        else:raise RuntimeError('Collector hid unresolved code')
    S.check(len(reads)==1,'only cached synthetic sheet boundary reached')
    S.write(root/'account_complete.json',{'total':0,'records':[]})
    S.write(root/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',{'pr':280,'root_identity_reconciliation_complete':True,
       'unresolved_leads':[],'release_manifest_sha256':B.RELEASE_SHA,'account_leads':[],'unrelated_local_state_exemptions':[],
       'ledger_leads':[{'values_sha256':B.digest(r),'disposition':'distinct_non_target'} for r in rows] if exempt else []})
    gate={'started_utc':B.stamp(),'completed_utc':B.stamp(),'phase':'before_integration','expected_pr_head':'a'*40,
       'expected_deposit_id':None,'read_only':True,'release_manifest_sha256':B.RELEASE_SHA,'release_files':B.release()['files'],
       'account_positive_control':'PASS_23174283','raw_receipts':str(root),'receipt':str(root/'gate.json'),
       'account_complete_sha256':B.sha((root/'account_complete.json').read_bytes()),'account_complete_total':0,
       'unexpected_account_matches':[],'ledger_matches':[{'row':i+2,'values':r} for i,r in enumerate(rows)],'local_deposit_state_matches':[]}
    S.write(root/'gate.json',gate)
    with patch.object(G,'AUDIT',root):
        try:G.reconcile(gate,'before_integration','a'*40,None)
        except RuntimeError as error:S.check('review' in str(error).lower(),'gate independently rejects ambiguity before digest')
        else:raise RuntimeError('Gate hid unresolved code')


def main():
    path=S.ROOT/'private/record_route_retrospective/ledger.json';raw=path.read_bytes()
    S.check(hashlib.sha256(raw).hexdigest()=='d513b4cfef1ca47f654a6f677693ae7186f3f193f6d892c5e043ad318c0061b3','exact cached sheet')
    cached=json.loads(raw)['values'];row96=cached[95]
    old=S.implementation(True);frozen_rejections=[]
    for number,row in enumerate(cached,1):
        try:old[0].row_identity_leads(row)
        except RuntimeError:frozen_rejections.append(number)
    S.check(frozen_rejections==[96],'preserved current390 actual false block')
    S.write(S.HERE/('FROZEN_COMPATIBILITY_OPTIMIZED.json' if sys.flags.optimize else 'FROZEN_COMPATIBILITY.json'),
      {'optimization':sys.flags.optimize,'cached_raw_sha256':hashlib.sha256(raw).hexdigest(),'rows':len(cached),'false_block_rows':frozen_rejections,
       'source_sha256':hashlib.sha256((S.FROZEN/'ops_binding.py').read_bytes()).hexdigest(),'provider_attempts':0})
    modules=S.implementation(False);B,P,G,V,D=modules
    with ExitStack() as guards:
        guards.enter_context(patch.object(subprocess,'run',S.forbidden));guards.enter_context(patch.object(socket,'socket',S.forbidden))
        guards.enter_context(patch.object(V,'urlopen',S.forbidden))
        for method in ['request','create','upload','update','publish','get']:guards.enter_context(patch.object(B.zenodo.ZenodoClient,method,S.forbidden))
        with tempfile.TemporaryDirectory(dir=S.SCRATCH,prefix='bibliographic_') as temp:
            root=Path(temp)
            try:S.run_pipeline(root/'old_gather_false_block',old,[row96],False)
            except RuntimeError as error:S.check('review' in str(error).lower(),'old actual gather false block reproduced')
            else:raise RuntimeError('Old actual collector unexpectedly accepted exact row96')
            old_append=direct(root/'old_append_false_block',old,[row96],True)
            S.write(S.HERE/('FROZEN_COMPATIBILITY_OPTIMIZED.json' if sys.flags.optimize else 'FROZEN_COMPATIBILITY.json'),
              {'optimization':sys.flags.optimize,'cached_raw_sha256':hashlib.sha256(raw).hexdigest(),'rows':len(cached),
               'false_block_rows':frozen_rejections,'actual_frozen_gather_false_block':True,'actual_frozen_append_false_block':True,
               'append_reason':old_append,'source_sha256':hashlib.sha256((S.FROZEN/'ops_binding.py').read_bytes()).hexdigest(),'provider_attempts':0})
            for index,row in enumerate(cached,1):
                B.row_identity_leads(row);CASES.append({'case':'actual_cached_row_parses','row':index})
            S.check(B.row_identity_leads(row96)==frozenset({'10.5281/zenodo.23385608'}),'exact real row remains a distinct identity')
            for value in VALID+[row96[0]]:
                for column in range(4):
                    row=['','','',''];row[column]=value
                    for exempt in [False,True]:
                        result=S.run_pipeline(root/str(len(CASES)),modules,[row],True,exempt)
                        S.check(result['collector_matching_rows']==0 and result['gate_accepted'] and result['append_calls']==1 and result['append_returned_verified'],'qualified bibliography accepts absence normally')
                        CASES.append({'case':'qualified_full_pipeline','column':column+1,'exemption':exempt,**result})
            for exempt in [False,True]:
                result=S.run_pipeline(root/str(len(CASES)),modules,[row96],True,exempt)
                S.check(result['collector_matching_rows']==0 and result['gate_accepted'] and result['append_calls']==1 and result['append_returned_verified'],'exact actual row96 pipeline')
                CASES.append({'case':'exact_actual_row96_pipeline','row_sha256':B.digest(row96),'exemption':exempt,**result})
            for value in AMBIGUOUS:
                for column in range(4):
                    row=['birational','','',''];row[column]=value
                    for exempt in [False,True]:
                        direct(root/str(len(CASES)),modules,[row],exempt)
                        CASES.append({'case':'independent_append_unresolved','column':column+1,'exemption':exempt,'value':value,'append_calls':0})
                        before_allocation(root/str(len(CASES)),modules,[row],exempt)
                        CASES.append({'case':'collector_gate_before_allocation','column':column+1,'exemption':exempt,'value':value,'append_calls':0})
            for extra in ['10/abcde','10%252fabcde','https://shortdoi.org/abcde']:
                for column in range(4):
                    row=[BASE,BASE,BASE,BASE];row[column]+=' ; '+extra
                    for exempt in [False,True]:
                        direct(root/str(len(CASES)),modules,[row],exempt)
                        CASES.append({'case':'later_cell_additional_alias_append','column':column+1,'exemption':exempt,'append_calls':0})
                        before_allocation(root/str(len(CASES)),modules,[row],exempt)
                        CASES.append({'case':'later_cell_additional_alias_before_allocation','column':column+1,'exemption':exempt,'append_calls':0})
            for target in ['10.5281/ZENODO.999','https://zenodo.org:443/records/./999/export/json']:
                for column in range(4):
                    row=[BASE,BASE,BASE,BASE];row[column]+=' ; '+target
                    for exempt in [False,True]:
                        result=S.run_pipeline(root/str(len(CASES)),modules,[row],True,exempt)
                        S.check(result['collector_matching_rows']==1 and not result['gate_accepted'] and result['append_calls']==0,'bibliographic context cannot hide target')
                        CASES.append({'case':'adjacent_or_later_target_lead','column':column+1,'exemption':exempt,**result})
            for value in AMBIGUOUS:
                for column in range(4):
                    desired=D.desired_row(999);introduced=['','','',''];introduced[column]=value
                    result=S.run_pipeline(root/str(len(CASES)),modules,[],True,after_override=[B.HEADERS,introduced,desired])
                    S.check(result['append_calls']==1 and not result['append_returned_verified'],'readback unresolved code cannot claim uniqueness')
                    CASES.append({'case':'readback_unresolved','column':column+1,'value':value,**result})
            result=S.run_pipeline(root/str(len(CASES)),modules,[D.desired_row(999)],True)
            S.check(result['gate_accepted'] and result['append_calls']==0 and result['append_returned_verified'],'literal idempotence retained')
            CASES.append({'case':'literal_idempotence',**result})
    S.check(not S.ATTEMPTS,'zero actual providers')
    result={'timestamp':B.stamp(),'optimization':sys.flags.optimize,'proposal_only':True,'publication_ready':False,
      'controls':len(CASES),'all_controls_passed':True,'provider_access_attempts':0,'actual_cached_rows':176,'raw_cached_sha256':hashlib.sha256(raw).hexdigest(),
      'proposed_ops_binding_sha256':hashlib.sha256((S.PROPOSED/'ops_binding.py').read_bytes()).hexdigest(),
      'case_counts':{k:sum(c['case']==k for c in CASES) for k in sorted({c['case'] for c in CASES})},'cases':CASES}
    S.write(S.HERE/('BIBLIOGRAPHIC_CONTROLS_OPTIMIZED.json' if sys.flags.optimize else 'BIBLIOGRAPHIC_CONTROLS.json'),result)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))


if __name__=='__main__':main()
