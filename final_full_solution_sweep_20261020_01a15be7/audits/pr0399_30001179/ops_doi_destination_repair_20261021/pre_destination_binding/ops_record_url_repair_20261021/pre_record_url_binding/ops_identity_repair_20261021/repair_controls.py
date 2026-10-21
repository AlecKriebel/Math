#!/usr/bin/env python3
"""Independent append, concept/version, short-alias and exact directory controls."""
import copy,json,io,socket,subprocess,sys,tempfile
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch
from controls_support import HERE,implementation
KIND='canonical' if '--canonical' in sys.argv else 'proposed'
B,P,G,I,V,L,D=implementation(KIND)
CASES=[];PROVIDERS=[]

def check(value,message):
    if not value:raise RuntimeError('CONTROL CHECK FAILED: '+message)

def forbidden(*a,**k):
    PROVIDERS.append(True);raise RuntimeError('ACTUAL PROVIDER FORBIDDEN')

def write(p,v):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False)+'\n')

def expect(name,fn,ok=False):
    try:result=fn()
    except Exception as ex:
        CASES.append({'case':name,'expected':'accept' if ok else 'reject','actual':'reject','reason':str(ex)[:300]})
        check(not ok,name+' unexpectedly rejected '+str(ex))
    else:
        CASES.append({'case':name,'expected':'accept' if ok else 'reject','actual':'accept'})
        check(ok,name+' unexpectedly accepted')

def family_and_spelling():
    target={'id':999,'conceptrecid':'888','conceptdoi':'10.5281/ZENODO.888','metadata':{'relations':{'version':[{'parent':{'pid_type':'recid','pid_value':'888'}}]}}}
    expect('actual_typed_concept_version_schema',lambda:check(B.record_identity_ids(target,999)==[888,999],'exact family ID set'),True)
    for field,value in [('conceptrecid',True),('conceptrecid',888.0),('conceptrecid','0888'),('conceptrecid','0'),('conceptdoi','10.5281/zenodo.0888'),('conceptdoi','https://doi.org/10.5281/zenodo.888')]:
        v=copy.deepcopy(target);v[field]=value
        expect('family_unparsed_'+field+repr(value),lambda v=v:B.record_identity_ids(v,999))
    for value in [{'version':[{'parent':{'pid_type':'recid','pid_value':'887'}}]},{'version':{}},{'version':[{'parent':{'pid_type':'doi','pid_value':'10.5281/zenodo.888'}}]}, {'version':[{'parent':{'pid_type':'recid','pid_value':True}}]}, {'version':[{}]}]:
        v=copy.deepcopy(target);v['metadata']['relations']=value
        expect('typed_version_parent_reject_'+repr(value),lambda v=v:B.record_identity_ids(v,999))
    for value in ['10.5281/zenodo.0999','10.5281/zenodo.9990','10.5281/zenodo.999x','10.5281/zenodo.999/other','10.5281/zenodo.999%30','10.5281/ＺＥＮＯＤＯ.999','10.5281/zenodo.９９９']:
        expect('no_cast_no_unicode_fold_'+value,lambda value=value:check(not B.target_in_row([value],999),'distinct DOI spelling remains distinct'),True)
    expect('literal_leading_zero_suffix_preserved',lambda:check('10.5281/zenodo.0999' in B.inspect_identity('10.5281/ZENODO.0999')['canonical_names'],'no automatic suffix integer cast'),True)
    for value in ['10.5281/zenodo.888','https://doi.org/10.5281/zenodo%2E888','https://zenodo.org/records/888']:
        expect('concept_version_conservative_lead_'+value,lambda value=value:check(B.target_in_row([value],999,[888,999]),'family review lead'),True)
    for value in ['10.5281%2Fzenodo.999','10.5281%252Fzenodo.999','https://zenodo.org/records/999']:
        r=B.inspect_identity(value)
        expect('review_only_no_general_URI_equivalence_'+value,lambda r=r:check('10.5281/zenodo.999' not in r['canonical_names'] and '10.5281/zenodo.999' in r['review_names'],'review-only alias remains distinct classification'),True)


def collector_short_alias(work):
    root=work/'short_collector';root.mkdir()
    write(root/'raw/pr0399/ledger_live.json',{'values':[B.HEADERS]})
    for n,value in enumerate(['10/abc','https://shortdoi.org/abc','https://doi.org/abc','https://doi.org/10/abc']):
        rows=[B.HEADERS,['ordinal lead','','10.5281/zenodo.999',value]]
        with patch.object(P,'ROOT',root),patch.object(P,'PRIVATE',root/str(n)),patch.object(P,'verify_destination',lambda:None),patch.object(P,'read_command',lambda *a:{'values':rows}):
            expect('actual_collector_unresolved_alias_even_before_allocation_'+value,lambda:P.gather('before_integration',B.ORIGINAL))


def append_independent(work):
    root=work/'append';root.mkdir();desired=D.desired_row(999);base=[B.HEADERS]
    public={'record':999,'all_public_file_bytes_match_reviewed':True,'doi_resolution':{'status':200},'release_manifest_sha256':B.RELEASE_SHA}
    aliases=['10.5281/ZENODO.999','https://doi.org/10.5281/zenodo%2E999','10.5281%2Fzenodo.999','10.5281%252Fzenodo.999','https://zenodo.org/records/999','10/abc','https://shortdoi.org/abc','10.5281/zenodo.888']
    def run(label,before,after,exempt=False,expected=0,ok=False):
        for p in root.glob('*.json'):p.unlink()
        write(root/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',{'ledger_leads':[{'values_sha256':B.digest(r),'disposition':'distinct_non_target'} for r in before[1:]] if exempt else []})
        write(root/'ZENODO_PUBLIC_FILE_VERIFICATION.json',{'synthetic':True})
        gate={'started_utc':B.stamp(),'receipt':'synthetic','ledger_sha256':B.digest(before),'expected_identity_record_ids':[888,999]};calls=[];reads=iter([before,after])
        def gws(action,params,body):
            check(action=='append' and (root/'LEDGER_APPEND_INTENT.json').exists(),'one intent precedes synthetic append');calls.append(body)
            return {'updates':{'updatedRows':1,'updatedColumns':4,'updatedData':{'values':[desired]}}}
        with patch.object(D,'AUDIT',root),patch.object(D,'require_release_clearance',lambda:None),patch.object(D,'verify_live',lambda *a:public),patch.object(D,'collect',lambda *a,**k:(gate,{})),patch.object(D,'read',lambda *a:next(reads)),patch.object(D,'gws',gws):
            expect(label,lambda:D.append_verified('a'*40,999),ok)
        check(len(calls)==expected,label+' exact append count');CASES[-1]['synthetic_append_calls']=len(calls)
        if not ok:check(not (root/'LEDGER_PUBLICATION_VERIFICATION.json').exists(),'no false unique verification after rejection')
    for alias in aliases:
        row=['Other wording','','',alias]
        run('independent_append_alias_alone_'+alias,base+[row],base+[row,desired])
        run('independent_append_contradictory_exemption_'+alias,base+[row],base+[row,desired],True)
        run('independent_append_alias_plus_exact_'+alias,base+[row,desired],base+[row,desired])
        run('independent_readback_alias_duplicate_'+alias,base,base+[row,desired],expected=1)
    run('independent_literal_idempotence',base+[desired],base+[desired],ok=True)
    run('independent_absence_single_append',base,base+[desired],expected=1,ok=True)


def family_pipeline(work):
    import integrated_controls as S
    target={'id':999,'conceptrecid':'888','conceptdoi':'10.5281/ZENODO.888',
        'metadata':{'title':B.TITLE,'relations':{'version':[{'parent':{'pid_type':'recid','pid_value':'888'}}]}},'files':[]}
    for number,alias in enumerate(['10.5281/zenodo.888','10.5281/ZENODO.888','https://zenodo.org/records/888']):
        for exempt in [False,True]:
            def run(alias=alias,number=number,exempt=exempt):
                result=S.run_pipeline(work/('family'+str(number)+str(exempt)),(B,P,G,V,D),[['Otherwise unrelated','','',alias]],True,exempt=exempt,target_record=target)
                check(result['expected_identity_record_ids']==[888,999],'family IDs derived from actual target record fields')
                check(result['collector_matching_rows']==1 and not result['gate_accepted'] and result['append_calls']==0,'conservative family row blocks before exemption/mutation')
            expect('actual_collector_gate_typed_family_'+alias+str(exempt),run,True)
    def exact():
        result=S.run_pipeline(work/'family_exact',(B,P,G,V,D),[D.desired_row(999)],True,target_record=target)
        check(result['expected_identity_record_ids']==[888,999] and result['gate_accepted'] and result['append_calls']==0 and result['append_returned_verified'],'literal current row stays idempotent with family fields')
    expect('actual_family_metadata_literal_row_idempotent',exact,True)


def directory_inventory(work):
    original=I.originals();selected=I.selection();added={**original,**{n:('100644','blob',I.blob_sha(v)) for n,v in selected.items()}}
    def ent(sig):return {'mode':sig[0],'type':sig[1],'sha':sig[2]}
    def dirs(names):
        result={}
        for name in names:
            parts=Path(name).parts
            for j in range(1,len(parts)):result['/'.join(parts[:j])]={'mode':'040000','type':'tree','sha':'e'*40}
        return result
    originals={**{n:ent(v) for n,v in original.items()},**dirs(original)}
    empty={'mode':'040000','type':'tree','sha':'4b825dc642cb6eb9a060e54bf8d69288fbee4904'}
    base={'retained.txt':ent(('100644','blob','f'*40)),'kept_empty':copy.deepcopy(empty),'kept_empty/nested':copy.deepcopy(empty)}
    complete={**copy.deepcopy(base),**{n:ent(v) for n,v in added.items()},**dirs(added)}
    def run(label,change=lambda b,m,o:None,ok=False,branch=False):
        b,m,o=copy.deepcopy(base),copy.deepcopy(complete),copy.deepcopy(originals);change(b,m,o)
        maps={'base':b,'integrated':m,B.ORIGINAL:o}
        def subtree(commit,path,recursive=True):
            if path==B.PROBLEM:return maps[commit]
            if path=='':return {'unsolved_math_prioritization':{'mode':'040000','type':'tree','sha':commit},'other':ent(('100644','blob','a'*40))}
            if path=='unsolved_math_prioritization':return {'attempts':{'mode':'040000','type':'tree','sha':commit},'QUEUE.md':ent(('100644','blob',commit)),'other':ent(('100644','blob','a'*40))}
            return {'30001179':{'mode':'040000','type':'tree','sha':commit},'other':{'mode':'040000','type':'tree','sha':'a'*40}}
        def blob(c,p):return I.BASELINE_ROW if c in {'base',B.ORIGINAL_PARENT} else I.DESIRED_ROW
        with patch.object(I,'subtree',subtree),patch.object(I,'blob',blob),patch.object(I,'api',lambda *a:{'parents':[{'sha':B.ORIGINAL_PARENT}]}):
            expect(label,lambda:I.verify_integrated_tree('base','integrated',B.ORIGINAL),ok)
    run('full_verifier_keeps_existing_nested_empty_trees',ok=True)
    for name,change in [('added_empty_tree',lambda b,m,o:m.update(hidden_empty=copy.deepcopy(empty))),
        ('added_nested_empty_tree',lambda b,m,o:m.update({'preprint/hidden_empty':copy.deepcopy(empty)})),
        ('deleted_existing_empty_tree',lambda b,m,o:m.pop('kept_empty')),
        ('deleted_nested_empty_tree',lambda b,m,o:m.pop('kept_empty/nested')),
        ('renamed_empty_tree',lambda b,m,o:m.update(renamed=m.pop('kept_empty'))),
        ('moved_empty_tree',lambda b,m,o:m.update({'preprint/moved':m.pop('kept_empty/nested')})),
        ('directory_mode_changed',lambda b,m,o:m['kept_empty'].update(mode='100644')),
        ('original_directory_missing',lambda b,m,o:m.pop('independent_reviews')),
        ('unsafe_directory_alias',lambda b,m,o:m.update({'hidden//alias':copy.deepcopy(empty)}))]:
        run('full_verifier_rejects_'+name,change)
    def original_empty(b,m,o):o['original_empty']=copy.deepcopy(empty);m['original_empty']=copy.deepcopy(empty)
    run('preserves_original_empty_tree_union',original_empty,True)
    # Direct branch-overlay check still compares actual recursive directories.
    def branch_good():
        maps={B.ORIGINAL:originals,'new':{**originals,**{n:ent(('100644','blob',I.blob_sha(v))) for n,v in selected.items()},**dirs(selected)}}
        with patch.object(I,'subtree',lambda c,p:maps[c]):I.verify_directory_overlay(B.ORIGINAL,'new',selected)
    expect('branch_overlay_exact_ancestors',branch_good,True)


def main():
    with ExitStack() as guards:
        guards.enter_context(patch.object(socket,'socket',forbidden));guards.enter_context(patch.object(subprocess,'run',forbidden));guards.enter_context(patch.object(V,'urlopen',forbidden))
        for name in ['request','create','upload','update','publish','get']:guards.enter_context(patch.object(B.zenodo.ZenodoClient,name,forbidden))
        with tempfile.TemporaryDirectory(dir=HERE,prefix='repair_controls_') as tmp:
            work=Path(tmp);family_and_spelling();collector_short_alias(work);append_independent(work);family_pipeline(work);directory_inventory(work)
    check(not PROVIDERS,'zero actual providers')
    result={'implementation':KIND,'optimization':sys.flags.optimize,'controls':len(CASES),'accepted':sum(x['actual']=='accept' for x in CASES),'rejected':sum(x['actual']=='reject' for x in CASES),'all_controls_passed':True,'actual_provider_attempts':len(PROVIDERS),'cases':CASES,'scope':'Actual helper functions under synthetic provider boundaries; literal desired-row equality retained; family and reserved/nested/record aliases are conservative leads only.'}
    name='TARGETED_CONTROLS_OPTIMIZED.json' if sys.flags.optimize else 'TARGETED_CONTROLS.json';write(HERE/name,result);print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2))
if __name__=='__main__':main()
