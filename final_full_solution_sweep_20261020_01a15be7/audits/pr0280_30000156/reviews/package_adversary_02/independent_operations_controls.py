#!/usr/bin/env python3
"""Independent actual-helper counterexamples; every service boundary synthetic."""
from pathlib import Path
import copy,hashlib,importlib,json,subprocess,sys,tempfile
from contextlib import ExitStack
from unittest.mock import patch
BASE=Path(__file__).resolve().parent
AUDIT=BASE.parents[1]
sys.path.insert(0,str(AUDIT))
import ops_binding as B
import publication_live_gates as G
import record_publication_ledger as D
import verify_published_files as V

def forbidden(*a,**k):raise RuntimeError('Unmocked external operation forbidden')
def write(p,x):p.write_text(json.dumps(x)+'\n')

def main():
    report=[]
    with ExitStack() as s:
        s.enter_context(patch.object(subprocess,'run',forbidden));s.enter_context(patch.object(V,'urlopen',forbidden))
        for name in ['request','create','upload','update','publish','get']:
            s.enter_context(patch.object(B.zenodo.ZenodoClient,name,forbidden))
        with tempfile.TemporaryDirectory(dir=BASE,prefix='independent_ops_') as temp:
            root=Path(temp);identifier=999;row=D.desired_row(identifier)
            before=[B.HEADERS,row];after=before+[row]
            recon={'pr':280,'root_identity_reconciliation_complete':True,'unresolved_leads':[],
                'release_manifest_sha256':B.RELEASE_SHA,'account_leads':[],
                'ledger_leads':[{'values_sha256':B.digest(row),'disposition':'distinct_non_target'}]}
            write(root/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',recon)
            write(root/'ZENODO_PUBLIC_FILE_VERIFICATION.json',{'synthetic':True})
            account={'total':1,'records':[{'id':identifier,'metadata':{'title':B.TITLE},'files':[]}]}
            write(root/'account_complete.json',account)
            gate={'ledger_sha256':B.digest(before),'started_utc':B.stamp(),'completed_utc':B.stamp(),
                'phase':'before_ledger','expected_pr_head':'a'*40,'expected_deposit_id':identifier,
                'read_only':True,'release_manifest_sha256':B.RELEASE_SHA,'release_files':B.release()['files'],
                'account_positive_control':'PASS_23174283','raw_receipts':str(root),'receipt':str(root/'gate.json'),
                'account_complete_sha256':B.sha((root/'account_complete.json').read_bytes()),
                'account_complete_total':1,'unexpected_account_matches':[],
                'ledger_matches':[{'row':2,'values':row}],'local_deposit_state_matches':[]}
            write(root/'gate.json',gate)
            public={'record':identifier,'all_public_file_bytes_match_reviewed':True,'doi_resolution':{'status':200},'release_manifest_sha256':B.RELEASE_SHA}
            reads=iter([before,after]);appends=[]
            def append(action,params,body):
                if action!='append':raise RuntimeError('Unexpected synthetic action')
                appends.append(copy.deepcopy(body))
                return {'updates':{'updatedRows':1,'updatedColumns':4,'updatedData':{'values':[row]}}}
            with patch.object(G,'AUDIT',root):
                acceptance=G.reconcile(gate,'before_ledger','a'*40,identifier,True)
            with patch.object(D,'AUDIT',root),patch.object(D,'require_release_clearance',lambda:True),\
                 patch.object(D,'verify_live',lambda i:public),patch.object(D,'collect',lambda *a,**k:(gate,acceptance)),\
                 patch.object(D,'read',lambda *a:next(reads)),patch.object(D,'gws',append):
                try:
                    D.append_verified('a'*40,identifier)
                except Exception as ex:outcome={'exception':type(ex).__name__,'message':str(ex)}
                else:outcome={'accepted':True}
            report.append({'case':'existing_exact_target_row_marked_as_root_distinct_non_target',
                'preexisting_exact_DOI_rows':1,'synthetic_append_calls':len(appends),
                'actual_gate_reconcile_accepted':True,'gate_target_rows':acceptance['target_rows'],
                'appended_exact_target_again':appends==[{'majorDimension':'ROWS','values':[row]}],
                'outcome':outcome,'actual_provider_access':False,
                'expected_safety':'No append should occur when the exact target DOI/row is already present, regardless of a contradictory root exemption.'})
            # A completely classified distinct account record can still block
            # every phase solely because its unrelated local state matches the
            # deliberately broad model keyword. Preserve that state; no writes.
            other={'id':101,'metadata':{'title':'Synthetic birational work on a different problem'},'files':[{'key':'other.pdf','checksum':'md5:synthetic','size':1}]}
            for expected in [None,999]:
                records=[other]+([{'id':999,'metadata':{'title':B.TITLE},'files':[]}] if expected else [])
                a={'total':len(records),'records':records};write(root/'account_complete.json',a)
                c={'pr':280,'root_identity_reconciliation_complete':True,'unresolved_leads':[],
                    'release_manifest_sha256':B.RELEASE_SHA,'ledger_leads':[],
                    'account_leads':[{'record':101,'disposition':'distinct_non_target','metadata_and_files_sha256':B.digest(B.identity_projection(other))}]}
                write(root/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',c)
                g={**gate,'phase':'before_integration' if expected is None else 'before_publish',
                    'expected_deposit_id':expected,'account_complete_total':len(records),
                    'account_complete_sha256':B.sha((root/'account_complete.json').read_bytes()),
                    'ledger_matches':[],'unexpected_account_matches':[{'id':101}],
                    'local_deposit_state_matches':[]}
                write(root/'gate.json',g)
                with patch.object(G,'AUDIT',root):
                    clean=G.reconcile(g,g['phase'],'a'*40,expected)
                    g['local_deposit_state_matches']=[{'path':'.zenodo-state/metadata-101-production.json','sha256':'a'*64,'deposit_id':101}]
                    write(root/'gate.json',g)
                    try:G.reconcile(g,g['phase'],'a'*40,expected)
                    except Exception as ex:failure={'exception':type(ex).__name__,'message':str(ex)}
                    else:failure={'accepted':True}
                report.append({'case':'classified_distinct_record_unrelated_local_state_blocks',
                    'expected_target_id':expected,'without_local_state_accepted':True,
                    'metadata_and_entire_files_projection_bound':True,
                    'with_known_distinct_local_state':failure,'actual_provider_access':False})
    return report

if __name__=='__main__':print(json.dumps(main(),indent=2))
