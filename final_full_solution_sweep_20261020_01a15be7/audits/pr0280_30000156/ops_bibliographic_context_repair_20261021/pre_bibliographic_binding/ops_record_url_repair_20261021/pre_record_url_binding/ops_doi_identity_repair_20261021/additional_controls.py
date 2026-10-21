#!/usr/bin/env python3
"""Independent append layer/all columns and actual integration-directory controls."""
from contextlib import ExitStack
import copy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import types
from unittest.mock import patch
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
import integrated_controls as T


def main():
    cases=[]
    old_directory_cases=[]
    with ExitStack() as guards:
        guards.enter_context(patch.object(subprocess,'run',T.forbidden))
        B,P,G,V,D=T.implementation(True)
        guards.enter_context(patch.object(V,'urlopen',T.forbidden))
        for method in ['request','create','upload','update','publish','get']:
            guards.enter_context(patch.object(B.zenodo.ZenodoClient,method,T.forbidden))
        with tempfile.TemporaryDirectory(dir=HERE,prefix='direct_synthetic_') as temp:
            root=Path(temp)
            variants=['10.5281/ZENODO.999','10.5281/ZeNoDo.999','https://doi.org/10.5281/zenodo%2E999',
                'https://doi.org/10.5281%2FZENODO.999','10.5281%252Fzenodo.999',
                'https://zenodo.org/records/999','10/abcde','https://shortdoi.org/abcde','https://doi.org/abcde']
            for index,value in enumerate(variants):
                for column in range(4):
                    work=root/('append'+str(index)+'_'+str(column));work.mkdir()
                    alias=['unrelated','','',''];alias[column]=value
                    before=[B.HEADERS,alias];desired=D.desired_row(999)
                    gate={'ledger_sha256':B.digest(before),'receipt':str(work/'gate.json'),'started_utc':B.stamp()}
                    T.write(work/'ROOT_PREPUBLICATION_LEAD_RECONCILIATION.json',{'ledger_leads':[]})
                    T.write(work/'ZENODO_PUBLIC_FILE_VERIFICATION.json',{'synthetic':True})
                    reads=iter([before,before+[desired]]);appends=[]
                    public={'record':999,'all_public_file_bytes_match_reviewed':True,'doi_resolution':{'status':200},'release_manifest_sha256':B.RELEASE_SHA}
                    def append(*args):appends.append(args);raise RuntimeError('Unexpected duplicate synthetic append')
                    with patch.object(D,'AUDIT',work),patch.object(D,'require_release_clearance',lambda:True),\
                         patch.object(D,'verify_live',lambda i:public),patch.object(D,'collect',lambda *a,**k:(gate,{})),\
                         patch.object(D,'read',lambda *a:next(reads)),patch.object(D,'gws',append):
                        try:D.append_verified('a'*40,999)
                        except RuntimeError:pass
                        else:raise RuntimeError('Independent append silently accepted alias')
                    T.check(not appends,'no append even when upstream gate bypassed')
                    cases.append({'case':'independent_append_alias_all_columns','value':value,'column':column,'append_calls':0})
            # Load the actual proposed repository helper with its canonical
            # read-only location and synthetic tree/blob functions.
            I=types.ModuleType('repository_integration');I.__file__=str(T.AUDIT/'repository_integration.py')
            exec(compile(((T.AUDIT/'repository_integration.py') if '--canonical' in sys.argv else (HERE/'proposed_helpers/repository_integration.py')).read_bytes(),'proposed_repository_integration.py','exec'),I.__dict__)
            OLD=types.ModuleType('old_repository_integration');OLD.__file__=str(T.AUDIT/'repository_integration.py')
            exec(compile((T.FROZEN/'repository_integration.py').read_bytes(),'frozen_repository_integration.py','exec'),OLD.__dict__)
            originals=I.originals();selected=I.selection()
            def tree(mode='040000'):return {'mode':mode,'type':'tree','sha':'synthetic'}
            dirs={'base':{'keepempty':tree(),'nested':tree(),'nested/empty':tree()},
                  B.ORIGINAL:{'checks':tree(),'independent_review':tree()},
                  'merged':{'keepempty':tree(),'nested':tree(),'nested/empty':tree(),'checks':tree(),'independent_review':tree(),'preprint':tree()}}
            leaves={'base':{'previous.txt':('100644','blob','old')},
                    'merged':{'previous.txt':('100644','blob','old'),**originals,**{n:('100644','blob',I.blob_sha(v)) for n,v in selected.items()}}}
            for label,mutation,accepted in [
                ('valid_baseline_emptydirs_plus_new_preprint',lambda d:None,True),
                ('extra_empty_tree',lambda d:d['merged'].update(extra_empty=tree()),False),
                ('missing_baseline_empty_tree',lambda d:d['merged'].pop('keepempty'),False),
                ('missing_nested_empty_tree',lambda d:d['merged'].pop('nested/empty'),False),
                ('extra_nested_empty_tree',lambda d:d['merged'].update({'nested/newempty':tree()}),False),
                ('missing_original_directory',lambda d:d['merged'].pop('checks'),False),
                ('missing_new_preprint_directory',lambda d:d['merged'].pop('preprint'),False),
                ('wrong_directory_mode',lambda d:d['merged'].update(preprint=tree('100644')),False)]:
                fixture=copy.deepcopy(dirs);mutation(fixture)
                def subtree(commit,path,recursive=True):return fixture[commit] if path==B.PROBLEM else {}
                with patch.object(I,'subtree',subtree),patch.object(I,'leaves',lambda c,p:copy.deepcopy(leaves[c])),\
                     patch.object(I,'blob',lambda c,p:I.BASELINE_ROW if c in {'base',B.ORIGINAL_PARENT} else I.DESIRED_ROW),\
                     patch.object(I,'api',lambda *a:{'parents':[{'sha':B.ORIGINAL_PARENT}]}):
                    try:I.verify_integrated_tree('base','merged','head')
                    except RuntimeError as ex:
                        T.check(not accepted,label+' should accept');actual='reject'
                    else:T.check(accepted,label+' must reject');actual='accept'
                cases.append({'case':'actual_integrated_directory_'+label,'actual':actual})
                if label in {'extra_empty_tree','missing_baseline_empty_tree','missing_nested_empty_tree'}:
                    with patch.object(OLD,'subtree',subtree),patch.object(OLD,'leaves',lambda c,p:copy.deepcopy(leaves[c])),\
                         patch.object(OLD,'blob',lambda c,p:OLD.BASELINE_ROW if c in {'base',B.ORIGINAL_PARENT} else OLD.DESIRED_ROW),\
                         patch.object(OLD,'api',lambda *a:{'parents':[{'sha':B.ORIGINAL_PARENT}]}):
                        OLD.verify_integrated_tree('base','merged','head')
                    old_directory_cases.append({'case':label,'frozen_actual_integrated_tree_accepted':True})
            for number,alias in enumerate(['10/abcde','https://shortdoi.org/abcde','https://doi.org/abcde']):
                try:T.run_pipeline(root/('short_pipeline'+str(number)),(B,P,G,V,D),[['Other','','',alias]],True)
                except RuntimeError as ex:
                    T.check('encoding' in str(ex),'recognized unresolved short DOI failure')
                    cases.append({'case':'actual_collector_shortDOI_failclosed','alias':alias,'append_calls':0})
                else:raise RuntimeError('Collector silently ignored shortDOI alias')
            for field in [{'conceptrecid':'998','conceptdoi':'10.5281/zenodo.997'},{'conceptrecid':True},{'conceptrecid':'0998'},{'conceptdoi':'10.5281/zenodo.998.extra'},
                          {'metadata':{'relations':{'version':[{'parent':{'pid_type':'doi','pid_value':'unknown'}}]}}},
                          {'parent':{'id':'not-a-numeric-recid'}}]:
                try:B.record_identity_ids({'id':999,'metadata':{},**field},999)
                except RuntimeError:cases.append({'case':'malformed_recognized_family_relation_fails_closed','field':field})
                else:raise RuntimeError('Malformed recognized family relation ignored')
    T.check(not T.ACTUAL_PROVIDER_ATTEMPTS,'zero provider attempts')
    T.write(HERE/('FROZEN_DIRECTORY_COUNTEREXAMPLES_OPTIMIZED.json' if sys.flags.optimize else 'FROZEN_DIRECTORY_COUNTEREXAMPLES.json'),{'cases':old_directory_cases,'actual_provider_access':False})
    output={'timestamp':B.stamp(),'optimization':sys.flags.optimize,'all_controls_passed':True,'controls':len(cases),'actual_provider_access_attempts':0,'cases':cases}
    T.write(HERE/(('CURRENT_ADDITIONAL_CONTROLS_OPTIMIZED.json' if sys.flags.optimize else 'CURRENT_ADDITIONAL_CONTROLS.json') if '--canonical' in sys.argv else ('ADDITIONAL_CONTROLS_OPTIMIZED.json' if sys.flags.optimize else 'ADDITIONAL_CONTROLS.json')),output)
    print(json.dumps({k:v for k,v in output.items() if k!='cases'},indent=2))


if __name__=='__main__':main()
