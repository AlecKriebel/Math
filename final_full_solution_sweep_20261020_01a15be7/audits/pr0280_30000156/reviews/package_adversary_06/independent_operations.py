#!/usr/bin/env python3
"""Review06 additional actual-function adversaries; provider boundaries forbidden."""
from contextlib import ExitStack
from pathlib import Path
from unittest.mock import patch
import json,types,sys,tempfile,copy,socket,subprocess,hashlib
A=Path(__file__).resolve().parents[2];P=A.parents[1]/'private/pr0280_package06'
sys.path.insert(0,str(A))
import ops_binding as B
import repository_integration as I
import prepublication_check as C
import verify_published_files as V
import record_publication_ledger as D
def ck(v,m):
    if not v:raise RuntimeError(m)
def load_fixture(name):
    src=A/'final_robustness_repair_20261021'/name
    mod=types.ModuleType('review06_'+name[:-3]);mod.__file__=str(src);sys.modules[mod.__name__]=mod
    exec(compile(src.read_bytes(),str(src),'exec'),mod.__dict__);return mod
RC=load_fixture('revision_controls.py');DC=load_fixture('doi_destination_controls.py')
cases=[];attempts=[]
def forbidden(*a,**kw):attempts.append(True);raise RuntimeError('Actual provider forbidden')
def reject(fn,label):
    try:fn()
    except (RuntimeError,KeyError,ValueError,TypeError) as e:cases.append({'case':label,'result':'reject','reason':str(e)})
    else:raise RuntimeError('Hostile case accepted: '+label)

def main():
    with ExitStack() as guard:
        guard.enter_context(patch.object(subprocess,'run',forbidden));guard.enter_context(patch.object(socket,'socket',forbidden))
        guard.enter_context(patch.object(V,'urlopen',forbidden))
        with tempfile.TemporaryDirectory(dir=P,prefix='extra_ops_') as t:
            root=Path(t)
            for name in ['PUBLICATION_REVISION_COMMIT.json','PUBLICATION_REVISION_PUSH_INTENT.json','PUBLICATION_REVISION_OUTCOME.json','PUBLICATION_REVISION_UNCERTAIN.json']:
                f=RC.Fixture(root/('orphan_'+name))
                with f.contexts():
                    RC.write(f.root/name,{'orphan':True});reject(lambda:I.revise(I.REVISION_BASE),'orphan_'+name)
                    ck(not f.posts and not f.patches,'orphan caused provider mutation')
            for mode in ['intent_only','commit_no_push','conflict_push_commit','conflict_push_binding','changed_child_after_push','changed_branch_after_push','changed_local_release_after_push']:
                f=RC.Fixture(root/mode)
                with f.contexts():
                    if mode in ['intent_only','commit_no_push','conflict_push_commit','conflict_push_binding']:
                        binding=I.revision_binding()[2]
                        RC.write(f.root/'PUBLICATION_REVISION_INTENT.json',{'pr':280,'binding':binding,'branch_endpoint':I.revision_ref(f.api('pulls/280'))})
                        if mode!='intent_only':RC.write(f.root/'PUBLICATION_REVISION_COMMIT.json',{'commit':f.child,'binding':binding})
                        if mode.startswith('conflict'):
                            RC.write(f.root/'PUBLICATION_REVISION_PUSH_INTENT.json',{'commit':('e'*40 if mode=='conflict_push_commit' else f.child),'binding':({} if mode=='conflict_push_binding' else binding)})
                    else:
                        I.revise(I.REVISION_BASE)
                        if mode=='changed_child_after_push':f.trees[f.child][next(iter(f.current))]['sha']='tampered'
                        if mode=='changed_branch_after_push':f.branch='codex/wrong-after-push'
                        if mode=='changed_local_release_after_push':(f.publication/'README.md').write_text('changed')
                    posts=len(f.posts);patches=len(f.patches)
                    reject(lambda:I.revise(I.REVISION_BASE),mode)
                    ck(len(f.posts)==posts and len(f.patches)==patches,'partial/conflict silently retried mutation')
            f=RC.Fixture(root/'changed_main_source')
            with f.contexts():
                main='e'*40;f.trees[main]=copy.deepcopy(f.trees[B.ORIGINAL]);f.trees[main][next(iter(f.originals))]['sha']='changed-by-main'
                reject(lambda:I.verify_integrated_tree(main,f.child,I.REVISION_BASE),'changed_main_selected_source')
            for i,url in enumerate(['https://zenodo.org:443./records/999','https://zenodo.org/records/999;foo','https://zenodo.org/records/999%00','https://zenodo.org/records/999\\','https://zenodo.org\t/records/999','https://zenodο.org/records/999','https://zenodo.org/records/+999','https://zenodo.org/records/999.json','https://zenodo.org/records/999/../999','https://zenodo.org:443@evil.invalid/records/999']):
                reject(lambda url=url:V.verify_doi_destination(999,{'http_status':200,'resolved_url':url}),'new_destination_'+str(i))
                for forged in [False,True]:
                    r=DC.pipeline(root/('doi_'+str(i)+'_'+str(forged)),url,forged)
                    ck(not r['accepted'] and r['synthetic_appends']==r['synthetic_upstream_gates']==0,'new actual pipeline destination bypass')
                    cases.append({'case':'destination_pipeline_'+str(i),'forged_upstream':forged,**r})
            report='OWR-14218-004 / problem 30003060: Solotar, Koszul Calculus, OWR 10/2016 pp.479–481. https://doi.org/10.4171/OWR/2016/10'
            ck(not B.inspect_identity(report)['ambiguous_encoding'],'actual bibliographic cell still blocked')
            cases.append({'case':'actual_bibliographic_cell','result':'accept','identities':sorted(B.row_identity_leads([report]))})
            for i in range(4):
                row=['generic']*4;row[i]=report;ck(not B.row_identity_leads(row),'bibliographic text false lead')
                for extra in [' 10/abcde',' https://shortdoi.org/abcde',' 10%2fabcde',' https://doi.org/abcde',' 10/2016']:
                    row[i]=report+extra;reject(lambda row=row:B.row_identity_leads(row),'bibliographic_plus_alias_'+str(i)+'_'+extra)
                row[i]=report+' https://zenodo.org/records/0999/files/source.zip'
                ck(B.target_in_row(row,999),'source context hid real target URL');cases.append({'case':'context_preserves_target_'+str(i),'result':'target_detected'})
                row[i]=report.replace('/OWR/2016/10','/OWR/2017/10')
                reject(lambda row=row:B.row_identity_leads(row),'mismatched_source_year_'+str(i))
            reject(B.require_release_clearance,'current_false_root_clearance')
    ck(not attempts,'actual provider boundary attempted')
    output={'status':'PASS','optimization':sys.flags.optimize,'controls':len(cases),'actual_provider_attempts':len(attempts),'cases':cases,'fixture_scope':'Reviewed original fixture data interfaces reused, new adversarial scenarios; actual canonical functions unchanged.'}
    (Path(__file__).parent/('INDEPENDENT_OPERATIONS_OPTIMIZED.json' if sys.flags.optimize else 'INDEPENDENT_OPERATIONS.json')).write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({k:v for k,v in output.items() if k!='cases'}))
if __name__=='__main__':main()
