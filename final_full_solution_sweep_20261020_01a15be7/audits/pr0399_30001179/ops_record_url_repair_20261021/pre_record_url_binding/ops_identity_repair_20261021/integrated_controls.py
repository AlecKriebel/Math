#!/usr/bin/env python3
"""Frozen/current and PROPOSED actual-function identity pipelines; synthetic only."""
import copy
from contextlib import ExitStack
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
from unittest.mock import patch

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
FROZEN=HERE/'pre_review02_binding'
sys.path.insert(0,str(HERE))
import doi_identity as R
KIND='canonical' if '--canonical' in sys.argv else 'proposed'
CASES=[]
ACTUAL_PROVIDER_ATTEMPTS=[]


def check(value,message):
    if not value:raise RuntimeError('CONTROL CHECK FAILED: '+message)


def forbidden(*args,**kwargs):
    ACTUAL_PROVIDER_ATTEMPTS.append(True)
    raise RuntimeError('REAL PROVIDER ACCESS FORBIDDEN')


def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def implementation(proposed):
    from controls_support import implementation as load
    B,P,G,I,V,L,D=load(KIND if proposed else 'frozen')
    return B,P,G,V,D


def scalar_controls():
    positive=[
        '10.5281/zenodo.999','10.5281/ZENODO.999','doi:10.5281/ZeNoDo.999',
        'https://DOI.ORG/10.5281/ZENODO.999','Notes: see (10.5281/ZeNoDo.999).',
        'https://doi.org/10.5281/%7a%65%6E%6F%64%6F.%39%39%39',
        'https://doi.org/10.5281/zenodo%2E999','https://doi.org/10%2E5281/zenodo.999',
        'https://doi.org/10.5281%2FZENODO%2E999','10.5281%252FZeNoDo%252E999',
        'https://doi.org/10.5281/zenodo.999?download=1','10.5281/zenodo.999#section',
        'See zenodo.999 in Notes','https://zenodo.org/records/999','https://zenodo.org/record/999',
        'https://zenodo.org/api/records/999','https://zenodo.org/records/999/files/paper.pdf',
        'https://zenodo.org/records/000999','https://doi.org/10.5281/zenodo.999...',
        'https://doi.org/10.5281/zenodo.999; next result']
    negative=[
        '10.5281/zenodo.9990','10.5281/zenodo.1999','10.5281/zenodo.999123',
        '10.5281/zenodo.0999','10.5281/zenodo.999abc','10.5281/zenodo.999-other',
        '10.5281/zenodo.999_copy','10.5281/zenodo.999.other','10.5281/zenodo.999/extra',
        '10.5281/zenodo.999.0','10.52810/zenodo.999','110.5281/zenodo.999',
        '10.1234/zenodo.999','x10.5281/zenodo.999','10.5281/ＺＥＮＯＤＯ.999',
        '10.5281/zenodo.９９９','https://zenodo.org.evil/records/999',
        'https://evilzenodo.org/records/999','https://zenodo.org/records/9990',
        'https://doi.org/10.5281/zenodo.999%30','https://doi.org/10.5281/zenodo.999%61',
        'https://doi.org/10.5281/zenodo.999%2Eother','999 alone is not a DOI']
    for value in positive:
        check(R.target_in_row(['','',value,''],999),'positive identity lead '+value)
        CASES.append({'case':'scalar_positive','value':value,'actual':'lead'})
    for value in negative:
        check(not R.target_in_row(['','',value,''],999),'no partial-ID or suffix match '+value)
        CASES.append({'case':'scalar_non_target','value':value,'actual':'no_target_lead'})
    for value in ['10/abc','https://doi.org/abc','https://shortdoi.org/abc','10.5281/zenodo.999%GG','https://doi.org/10.5281/zenodo.999'+('%25'*2)+'GG',
                  'https://doi.org/10.5281'+('%25'*10)+'2Fzenodo.999']:
        try:R.target_in_row([value],999)
        except RuntimeError:CASES.append({'case':'ambiguous_encoding_fails_closed','value':value,'actual':'reject'})
        else:raise RuntimeError('Unresolved encoding silently ignored')
    for value in ['10.5281/ZENODO.999','https://doi.org/10.5281/zenodo%2E999']:
        inspected=R.inspect_identity(value)
        check('10.5281/zenodo.999' in inspected['canonical_names'],'narrow canonical representation')
    for value in ['https://doi.org/10.5281%2FZENODO.999','10.5281%252Fzenodo.999','https://zenodo.org/records/999']:
        inspected=R.inspect_identity(value)
        check('10.5281/zenodo.999' not in inspected['canonical_names'] and '10.5281/zenodo.999' in inspected['review_names'],
              'reserved/nested/record alias remains review-only')
    CASES.append({'case':'canonical_vs_review_only_distinction','actual':'preserved'})
    return positive,negative


def run_pipeline(root,modules,rows,proposed,exempt=False,after_override=None,record_extra=None,target_record=None):
    B,P,G,V,D=modules
    row=D.desired_row(999)
    before=[B.HEADERS]+copy.deepcopy(rows)
    after=copy.deepcopy(after_override) if after_override is not None else before+[row]
    root.mkdir()
    repo=root/'repo';repo.mkdir()
    write(root/'raw/pr0399/ledger_live.json',{'checked_at':B.stamp(),'response':{'values':[B.HEADERS]}})
    recon={'pr':399,'root_identity_reconciliation_complete':True,'unresolved_leads':[],
           'release_manifest_sha256':B.RELEASE_SHA,'account_leads':[],
           'ledger_leads':[{'values_sha256':B.digest(r),'disposition':'distinct_non_target'} for r in rows] if exempt else [],
           'unrelated_local_state_exemptions':[]}
    write(root/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',recon)
    write(root/'ZENODO_PUBLIC_FILE_VERIFICATION.json',{'synthetic':True})
    records=[copy.deepcopy(target_record) if target_record is not None else {'id':999,'metadata':{'title':B.TITLE},'files':[]}]
    if record_extra:records[0].update(copy.deepcopy(record_extra))
    class Client:
        base='https://synthetic.invalid'
        def request(self,method,url):
            from urllib.parse import parse_qs,urlsplit
            check(method=='GET','actual account_search uses GET')
            query=parse_qs(urlsplit(url).query).get('q',[''])[0]
            response=search(self,query)
            return {'hits':{'total':response['total'],'hits':response['records']},'links':{}}
    def search(client,query):
        values=([{'id':23174283,'metadata':{'title':'Synthetic Fibonacci control'},'files':[]}]
                if query=='Fibonacci' else records)
        return {'query':query,'total':len(values),'pages':1,'records':copy.deepcopy(values)}
    def command(args):
        if args[0]=='gws':return {'values':copy.deepcopy(before)}
        if args[-1].endswith('/pulls/399'):
            return {'number':399,'state':'closed','merged':True,'draft':False,
                    'head':{'sha':'a'*40,'ref':B.BRANCH,'repo':{'full_name':'AlecKriebel/Math'}},
                    'base':{'ref':'main','repo':{'full_name':'AlecKriebel/Math'}}}
        if args[-1].endswith('/git/ref/heads/main'):return {'object':{'sha':'b'*40}}
        raise RuntimeError('Unexpected synthetic read boundary')
    result={'collector_matching_rows':None,'gate_accepted':False,'append_calls':0,'append_returned_verified':False,'exception':None}
    with ExitStack() as guards:
        guards.enter_context(patch.object(P,'ROOT',root));guards.enter_context(patch.object(P,'PRIVATE',root/'private'))
        guards.enter_context(patch.object(P,'REPO',repo));guards.enter_context(patch.object(P,'verify_destination',lambda:True))
        guards.enter_context(patch.object(P,'read_command',command))
        guards.enter_context(patch.object(P.zenodo,'ZenodoClient',lambda *a:Client()));guards.enter_context(patch.object(P.zenodo,'token_for',lambda *a:'synthetic-not-used'))
        gate=P.gather('before_ledger','a'*40,999)
        result['collector_matching_rows']=len(gate['ledger_matches'])
        result['expected_identity_record_ids']=gate.get('expected_identity_record_ids')
        with patch.object(G,'AUDIT',root):
            try:acceptance=G.reconcile(gate,'before_ledger','a'*40,999,True)
            except Exception as ex:
                result['exception']=str(ex);return result
        result['gate_accepted']=True
        # Existing exact row is read back unchanged; only absent-target paths
        # and intentionally demonstrated frozen bugs append a desired row.
        exact_existing=rows==[row]
        reads=iter([before,before if exact_existing and after_override is None else after])
        public={'record':999,'all_public_file_bytes_match_reviewed':True,'doi_resolution':{'status':200},'release_manifest_sha256':B.RELEASE_SHA}
        def append(action,params,body):
            check(action=='append','only synthetic append boundary')
            result['append_calls']+=1
            check((root/'LEDGER_APPEND_INTENT.json').exists(),'intent before synthetic mutation')
            return {'updates':{'updatedRows':1,'updatedColumns':4,'updatedData':{'values':[row]}}}
        with patch.object(D,'AUDIT',root),patch.object(D,'require_release_clearance',lambda:True),\
             patch.object(D,'verify_live',lambda i:public),patch.object(D,'collect',lambda *a,**k:(gate,acceptance)),\
             patch.object(D,'read',lambda *a:next(reads)),patch.object(D,'gws',append):
            try:
                receipt=D.append_verified('a'*40,999)
                result['append_returned_verified']=receipt['status']=='verified'
            except Exception as ex:result['exception']=str(ex)
    return result


def main():
    positive,negative=scalar_controls()
    for alias in ['10/abcde','https://shortdoi.org/abcde','https://doi.org/abcde','https://doi.org/10/abcde']:
        try:R.target_in_row([alias],999)
        except RuntimeError:CASES.append({'case':'shortDOI_unresolved_fails_closed','value':alias})
        else:raise RuntimeError('Short DOI silently ignored')
    with ExitStack() as guards:
        guards.enter_context(patch.object(subprocess,'run',forbidden))
        with tempfile.TemporaryDirectory(dir=HERE,prefix='synthetic_pipeline_') as tmp:
            work=Path(tmp)
            frozen=implementation(False)
            guards.enter_context(patch.object(frozen[3],'urlopen',forbidden))
            for method in ['request','create','upload','update','publish','get']:
                guards.enter_context(patch.object(frozen[0].zenodo.ZenodoClient,method,forbidden))
            old=[]
            for number,value in enumerate(['10.5281/ZENODO.999','See 10.5281/ZeNoDo.999 in Notes',
                     'https://doi.org/10.5281/%7a%65%6e%6f%64%6f.%39%39%39']):
                rows=[['Otherwise unrelated article','','',value]]
                result=run_pipeline(work/('old'+str(number)),frozen,rows,False)
                check(result['collector_matching_rows']==0 and result['gate_accepted'] and result['append_calls']==1 and result['append_returned_verified'],
                      'exact frozen collector/gate/append/readback duplicate+false uniqueness reproduction')
                old.append({'value':value,**result})
            write(HERE/('FROZEN_COUNTEREXAMPLES_OPTIMIZED.json' if sys.flags.optimize else 'FROZEN_COUNTEREXAMPLES.json'),
                  {'timestamp':frozen[0].stamp(),'optimization':sys.flags.optimize,'frozen_helpers_used':True,'cases':old})
            proposed=implementation(True)
            guards.enter_context(patch.object(proposed[3],'urlopen',forbidden))
            for number,value in enumerate(positive):
                rows=[['Otherwise unrelated article','','',value]]
                result=run_pipeline(work/('lead'+str(number)),proposed,rows,True)
                check(result['collector_matching_rows']==1 and not result['gate_accepted'] and result['append_calls']==0,
                      'proposal complete pipeline must stop every alias/encoding lead '+value)
                CASES.append({'case':'proposed_integrated_identity_lead','value':value,**result})
                result=run_pipeline(work/('exempt'+str(number)),proposed,rows,True,exempt=True)
                check(not result['gate_accepted'] and result['append_calls']==0,'contradictory alias exemption must stop')
                CASES.append({'case':'proposed_integrated_contradictory_exemption','value':value,**result})
            row=proposed[4].desired_row(999)
            result=run_pipeline(work/'idempotent',proposed,[row],True)
            check(result['gate_accepted'] and result['append_calls']==0 and result['append_returned_verified'],'exact original row remains idempotent')
            CASES.append({'case':'proposed_integrated_exact_idempotence',**result})
            result=run_pipeline(work/'absent',proposed,[],True)
            check(result['gate_accepted'] and result['append_calls']==1 and result['append_returned_verified'],'one absence append')
            CASES.append({'case':'proposed_integrated_absence_one_append',**result})
            # A duplicate alias introduced after the last read must invalidate
            # verification rather than yielding a false uniqueness certificate.
            alias=['Other wording','','','10.5281/ZENODO.999']
            result=run_pipeline(work/'readback_duplicate',proposed,[],True,after_override=[proposed[0].HEADERS,alias,row])
            check(result['append_calls']==1 and not result['append_returned_verified'],'post-boundary alias duplicate detected in readback')
            CASES.append({'case':'proposed_integrated_readback_alias_duplicate',**result})
            for number,extra in enumerate([
                    {'conceptrecid':'998','conceptdoi':'10.5281/zenodo.998'},
                    {'metadata':{'title':proposed[0].TITLE,'relations':{'version':[{'parent':{'pid_type':'recid','pid_value':'998'}}]}}},
                    {'parent':{'id':'998'}}]):
                result=run_pipeline(work/('family'+str(number)),proposed,[['Unrelated wording','','10.5281/zenodo.998','']],True,record_extra=extra)
                check(result['collector_matching_rows']==1 and not result['gate_accepted'] and result['append_calls']==0,'concept/version-parent leads stop duplicate append')
                CASES.append({'case':'proposed_integrated_concept_or_parent_lead','extra':extra,**result})
            for number,value in enumerate(negative):
                rows=[['Otherwise unrelated article','','',value]]
                result=run_pipeline(work/('non_target'+str(number)),proposed,rows,True)
                check(result['collector_matching_rows']==0 and result['gate_accepted'] and result['append_calls']==1 and result['append_returned_verified'],
                      'distinct numeric/suffix identity must not be falsely treated as target '+value)
                CASES.append({'case':'proposed_integrated_non_target_boundary','value':value,**result})
    check(not ACTUAL_PROVIDER_ATTEMPTS,'zero actual provider access')
    result={'implementation':KIND,'canonical_files_mutated_by_this_suite':False,'optimization':sys.flags.optimize,
            'controls':len(CASES),'all_controls_passed':True,'actual_provider_access_attempts':0,'cases':CASES,
            'scope':'Actual frozen function bodies and proposed copies, synthetic full collector/gate/append/readback pipelines only; no canonical/provider mutation.'}
    write(HERE/(('CURRENT_CONTROLS_OPTIMIZED.json' if sys.flags.optimize else 'CURRENT_CONTROLS.json') if '--canonical' in sys.argv else ('IDENTITY_PIPELINE_OPTIMIZED.json' if sys.flags.optimize else 'IDENTITY_PIPELINE.json')),result)
    print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))


if __name__=='__main__':main()
