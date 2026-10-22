#!/usr/bin/env python3
"""Probe the actual postmerge program using scratch fixtures and mocked services.

All fabricated records are explicitly tooling fixtures. No Git/service call or
project-state write is performed outside this review family's scratch folder.
"""
from pathlib import Path
import contextlib, copy, hashlib, importlib.util, io, json, os, shutil, sys, types

R=Path(__file__).resolve().parent
A=R.parents[1]
S=R/'scratch/postmerge_probes'
S.mkdir(parents=True,exist_ok=True)
os.environ['TMPDIR']=str(S)
sys.dont_write_bytecode=True

def load(path):
    spec=importlib.util.spec_from_file_location('probe_'+path.stem+str(id(path)),path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def save(p,d):
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')

def probe(case):
    # Detached exact operative helpers populate the scratch fixture; all external operations mocked.
    source=R/'scratch/program/audits/pr1268_10900050/publication'
    w=load(source/'workflow_regression.py')
    root=S/(case+'_'+str(sys.flags.optimize))
    if root.exists():shutil.rmtree(root)
    root.mkdir(exist_ok=True)
    f=w.fixture(root/'fixture')
    with contextlib.redirect_stdout(io.StringIO()):
        p,tracker,_=w.publication_and_tracker_controls(f)
        p['doi_resolution']={'status':'resolved','http_status':200}
        save(f['pub']/'PUBLICATION_RECEIPT.json',p)
        w.update_controls(f,p,tracker)
    u=load(f['pub']/'update_pr_publication.py')
    t=load(f['pub']/'append_tracker.py')
    files,_,_=u.desired_files(f['build'],p,tracker,f['snapshot'])
    body=(f['pub']/'PR_BODY_FINAL.md').read_text()
    head='a'*40; merge='c'*40; first='d'*40; events=[]
    def git(*args,data=None):
        events.append({'mock_git':list(args)})
        if args==('branch','--show-current'):return b'main\n'
        if args[0]=='rev-list':
            if args[-1]==merge:
                return (merge+' '+first+' '+('e'*40 if case=='wrong_merge_parent' else head)+'\n').encode()
            return (head+' '+u.ORIGINAL+'\n').encode()
        if args[0]=='diff-tree':return ('\n'.join(sorted(files))+'\n').encode()
        if args[0]=='show':
            name=args[1].split(':',1)[1]
            return b'changed' if case=='corrupt_merged_blob' and args[1].startswith(merge+':') else files[name]
        if args[0] in {'fetch','update-ref'}:return b''
        raise RuntimeError('Unexpected native Git operation '+str(args))
    u.git=git
    sheet_state=[{'properties':{'sheetId':t.GID,'title':'Renamed original'}},
                 {'properties':{'sheetId':999,'title':'Math Puzzles'}}] if case=='same_title_wrong_gid' else [{'properties':{'sheetId':t.GID,'title':'Math Puzzles'}}]
    if case=='missing_gid':sheet_state=[{'properties':{'sheetId':999,'title':'Math Puzzles'}}]
    rows=[['Original Problem','Solution Chat URL','DOI','Notes'],tracker['row']]
    if case=='duplicate_bare_doi':rows.append(['','',p['doi'],''])
    if case=='duplicate_doi_url':rows.append(['','',p['doi_url'],''])
    if case=='duplicate_PR_url':rows.append(['https://github.com/AlecKriebel/Math/pull/1268','','',''])
    if case=='duplicate_AMR_alias':rows.append(['AMR-108-0050','','',''])
    def call(parts,params,body=None):
        events.append({'mock_gws_parts':parts,'params':params})
        if parts==['spreadsheets','get']:return {'sheets':copy.deepcopy(sheet_state)}
        if parts==['spreadsheets','values','get']:return {'values':copy.deepcopy(rows)}
        raise RuntimeError('Unexpected native tracker write')
    t.call=call
    operative=A.parents[1]/'publication_coordinators/verify_pr1268_merge.py'
    copied=S/('verify_pr1268_merge_copy_'+str(sys.flags.optimize)+'.py')
    copied.write_bytes(operative.read_bytes())
    m=load(copied);m.A=f['audit'];m.P=f['pub'];m.PROGRAM=f['audit'].parents[1];m.REPO=root
    real_run_path=m.runpy.run_path
    def run_path(path):
        if Path(path).name=='update_pr_publication.py':return u.__dict__
        if Path(path).name=='append_tracker.py':return t.__dict__
        return real_run_path(path)
    # Use a private runpy facade, preserving real modules used by the loaded
    # update and tracker functions for their normal package authentication.
    m.runpy=types.SimpleNamespace(run_path=run_path)
    live={'state':'MERGED','headRefOid':head,'headRefName':u.BRANCH,
          'mergeCommit':{'oid':merge},'mergedAt':'2026-10-18T00:00:00Z',
          'body':body,'url':'https://github.com/AlecKriebel/Math/pull/1268'}
    def external(args,**kw):
        events.append({'mock_external':args});return json.dumps(live)
    m.subprocess=types.SimpleNamespace(check_output=external)
    if case=='doi_not_200':
        p['doi_resolution']={'status':'resolved','http_status':201};save(f['pub']/'PUBLICATION_RECEIPT.json',p)
        save(f['pub']/'DOI_INSPECT.json',p)
        # Regenerate the saved reviewed final bytes/identity for this case.
        files,_,_=u.desired_files(f['build'],p,tracker,f['snapshot'])
        wanted=u.expected_identity(p,tracker,files,body)
        for name in ['PR_BRANCH_INTENT.json','PR_BRANCH_RECEIPT.json']:
            old=json.loads((f['pub']/name).read_text());old.update(wanted);save(f['pub']/name,old)
    program=m.PROGRAM;state={'current_pr':1268,'completed_prs':[],'publications':[],'eligible_count':50}
    save(program/'PROGRAM_STATE.json',state)
    try:
        with contextlib.redirect_stdout(io.StringIO()):m.main()
        accepted=True;error=None
    except (RuntimeError,ValueError,FileNotFoundError,KeyError) as exc:
        accepted=False;error=type(exc).__name__+': '+str(exc)
    after=json.loads((program/'PROGRAM_STATE.json').read_text())
    return {'case':case,'optimization':sys.flags.optimize,'accepted':accepted,'error':error,
            'program_advanced_to':after['current_pr'],
            'sheet_metadata_read':any(x.get('mock_gws_parts')==['spreadsheets','get'] for x in events),
            'actual_sheet_state':sheet_state,'row_count':len(rows),
            'operative_program_sha256':hashlib.sha256(operative.read_bytes()).hexdigest(),
            'all_external_and_git_calls_mocked':True,'events':events}

def main():
    source=R/'scratch/program/audits/pr1268_10900050/publication'
    source.mkdir(parents=True,exist_ok=True)
    for name in ['append_tracker.py','build_package.py','check_public_downloads.py',
                 'compile_note.py','prepare_package.py','update_pr_publication.py',
                 'workflow_regression.py','verification/verify.py','zenodo-deposit.json']:
        target=source/name;target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(A/'publication'/name,target)
    coordinators=source.parents[2]/'publication_coordinators'
    coordinators.mkdir(exist_ok=True)
    for name in ['pr1268.py','verify_pr1268_merge.py']:
        shutil.copyfile(A.parents[1]/'publication_coordinators'/name,coordinators/name)
    cases=['baseline','same_title_wrong_gid','missing_gid','duplicate_bare_doi','duplicate_doi_url','duplicate_PR_url','duplicate_AMR_alias','wrong_merge_parent','corrupt_merged_blob','doi_not_200']
    outcomes=[probe(case) for case in cases]
    result={'scope':'Actual operative postmerge source, detached copy; synthetic scratch package/gates/records, all Git and external operations mocked. No release clearance.',
            'optimization':sys.flags.optimize,'cases':outcomes}
    for item in outcomes:
        expected=item['case']=='baseline'
        if item['accepted'] is not expected or item['program_advanced_to']!=(1271 if expected else 1268):raise RuntimeError('Unexpected state advance/rejection '+item['case'])
        if expected and not item['sheet_metadata_read']:raise RuntimeError('Missing live sheet-properties read')
    (R/('POSTMERGE_PROBES_'+str(sys.flags.optimize)+'.json')).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps([{k:x[k] for k in ['case','accepted','error','program_advanced_to','sheet_metadata_read']} for x in outcomes]))

if __name__=='__main__':main()
