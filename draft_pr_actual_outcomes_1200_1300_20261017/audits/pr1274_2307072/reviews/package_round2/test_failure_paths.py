"""New offline edge challenges; no actual credentials, network, or Git."""
from pathlib import Path
import contextlib,copy,datetime,io,json,runpy,shutil,subprocess,types,unittest.mock as mock
R=Path(__file__).resolve().parent; A=R.parents[1]; L=R/'own_local'; L.mkdir(exist_ok=True)
source=(A/'_local/ready_and_merge.py').read_bytes(); original_run_path=runpy.run_path
for name in ['merge_cases','public_cases']:
    if (L/name).exists():shutil.rmtree(L/name)

def need(value,message):
    if not value:raise RuntimeError(message)

def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x)+'\n')
def capture(fn):
    with contextlib.redirect_stdout(io.StringIO()):return fn()

results=[]
for case in ['baseline','already_ready','remote_changed','duplicate_path','path_replaced','body_changed_after_ready','head_changed_after_ready','ready_unconfirmed','lost_ready_response','merge_nonzero','merge_timeout','gate_reject']:
    root=L/'merge_cases'/case; p=root/'publication'; p.mkdir(parents=True,exist_ok=True); script=root/'_local/ready_and_merge.py';script.parent.mkdir();script.write_bytes(source)
    head='a'*40; branch='research/2307072-beurling-annihilator-witnesses'; paths=['problem/'+str(n) for n in range(11)];body='synthetic reviewed body'
    dump(p/'PR_BRANCH_RECEIPT.json',{'commit':head,'branch':branch,'paths':paths});dump(p/'FINAL_REVIEW_GATE.json',{'synthetic_fixture':True});(p/'PR_BODY_FINAL.md').write_text(body)
    live={'url':'https://github.com/AlecKriebel/Math/pull/1274','state':'OPEN','isDraft':case!='already_ready','headRefOid':head,'headRefName':branch,'body':body,'files':[{'path':x} for x in paths]};events=[];reads=0;merges=0
    if case=='duplicate_path':live['files'][-1]=copy.deepcopy(live['files'][0])
    if case=='path_replaced':live['files'][-1]={'path':'foreign/path'}
    def check_output(args,**kw):
        nonlocal_holder=None
        events.append(list(args))
        if args==['git','branch','--show-current']:return 'main\n'
        if args[:2]==['git','ls-remote']:return ('b'*40 if case=='remote_changed' else head)+' refs/heads/'+branch+'\n'
        if args[:3]==['gh','pr','view']:
            return json.dumps(live)
        raise RuntimeError('unmocked check_output '+repr(args))
    def run(args,**kw):
        events.append(list(args))
        if args[:3]==['gh','pr','ready']:
            if case!='ready_unconfirmed':live['isDraft']=False
            if case=='body_changed_after_ready':live['body']='outside body'
            if case=='head_changed_after_ready':live['headRefOid']='c'*40
            if case=='lost_ready_response':raise subprocess.TimeoutExpired(args,60)
            return types.SimpleNamespace(returncode=0,stdout='',stderr='')
        if args[:3]==['gh','pr','merge']:
            need('--match-head-commit' in args and args[-1]==head,'merge lacks exact head')
            if case=='merge_timeout':raise subprocess.TimeoutExpired(args,60)
            return types.SimpleNamespace(returncode=1 if case=='merge_nonzero' else 0,stdout='',stderr='synthetic failure' if case=='merge_nonzero' else '')
        raise RuntimeError('unmocked subprocess '+repr(args))
    def gate(g):
        if case=='gate_reject':raise RuntimeError('synthetic gate refusal')
    def execute():
        with mock.patch('runpy.run_path',return_value={'validate_workflow_gate':gate}),mock.patch('subprocess.check_output',side_effect=check_output),mock.patch('subprocess.run',side_effect=run):
            capture(lambda:exec(compile(source,str(script),'exec'),{'__file__':str(script),'__name__':'__main__'}))
    error=None
    try:execute();ok=True
    except (RuntimeError,FileExistsError,subprocess.TimeoutExpired) as ex:ok=False;error=type(ex).__name__
    expected=case in ['baseline','already_ready'];need(ok==expected,'unexpected result '+case)
    merge_calls=lambda:sum(e[:3]==['gh','pr','merge'] for e in events)
    first_count=merge_calls()
    if first_count:
        try:execute()
        except (RuntimeError,FileExistsError,subprocess.TimeoutExpired):pass
        need(merge_calls()==first_count,'merge repeated after saved intent '+case)
    need(first_count==(1 if case in ['baseline','already_ready','merge_nonzero','merge_timeout'] else 0),'unexpected mutation count '+case)
    results.append({'case':case,'accepted':ok,'error':error,'merge_calls':merge_calls(),'intent_exists':(p/'MERGE_REQUEST_INTENT.json').exists(),'events':events})

m=original_run_path(str(A/'publication/check_public_downloads.py'));t=original_run_path(str(A/'publication/append_tracker.py'))
base=L/'public_cases';base.mkdir(exist_ok=True);(base/'reviews/workflow_tooling').mkdir(parents=True); metadata=json.loads((A/'publication/zenodo-deposit.json').read_text())['metadata'];build=json.loads((A/'publication/BUILD_RECEIPT.json').read_text())
pub={'id':123,'environment':'production','state':'published','title':metadata['title'],'metadata_normalizations':[],'doi':'10.5281/zenodo.123','doi_url':'https://doi.org/10.5281/zenodo.123','record_url':'https://zenodo.org/records/123'}
actual=copy.deepcopy(metadata); actual['resource_type']={'type':actual.pop('upload_type'),'subtype':actual.pop('publication_type')};actual['license']={'id':actual['license']};actual['doi']=pub['doi']
record={'id':123,'doi':pub['doi'],'metadata':actual,'files':[{'key':build[k]['path'],'links':{'self':'https://fixture.invalid/'+build[k]['path']}} for k in ['pdf','verification_zip']]}
public_results=[]
for case in ['baseline','boolean_record_id','wrong_nested_doi','duplicate_file','extra_file','missing_file','modified_pdf_same_length','truncated_zip','creator_extra_field','html_description_escaped']:
    root=base/case;root.mkdir();dump(root/'FINAL_REVIEW_GATE.json',{'synthetic_fixture':True});dump(root/'PUBLICATION_RECEIPT.json',pub);dump(root/'BUILD_RECEIPT.json',build);dump(root/'zenodo-deposit.json',{'metadata':metadata});observed=copy.deepcopy(record);calls=[]
    if case=='boolean_record_id':observed['id']=True
    if case=='wrong_nested_doi':observed['metadata']['doi']='10.5281/zenodo.124'
    if case=='duplicate_file':observed['files'].append(copy.deepcopy(observed['files'][0]))
    if case=='extra_file':observed['files'].append({'key':'foreign','links':{'self':'https://fixture.invalid/foreign'}})
    if case=='missing_file':observed['files'].pop()
    if case=='creator_extra_field':observed['metadata']['creators'][0]['extra']='server addition in supplied list'
    if case=='html_description_escaped':observed['metadata']['description']=observed['metadata']['description'].replace('<p>','&lt;p&gt;')
    def fetch(url,limit):
        calls.append(url)
        if url=='https://zenodo.org/api/records/123':return json.dumps(observed).encode()
        name=url.rsplit('/',1)[-1];data=(A/'publication'/name).read_bytes()
        if case=='modified_pdf_same_length' and name.endswith('.pdf'):data=b'X'+data[1:]
        if case=='truncated_zip' and name.endswith('.zip'):data=data[:-1]
        return data
    ns=original_run_path(str(A/'publication/check_public_downloads.py'));ns['main'].__globals__['ROOT']=root;ns['main'].__globals__['fetch']=fetch
    ns['main'].__globals__['runpy']=types.SimpleNamespace(run_path=lambda path:{'validate_workflow_gate':lambda gate:None} if Path(path).name=='update_pr_publication.py' else t)
    try:capture(ns['main']);ok=True
    except (RuntimeError,KeyError):ok=False
    need(ok==(case=='baseline'),'public check unexpectedly accepted '+case);public_results.append({'case':case,'accepted':ok,'fetches':calls})
# Boundary-preserving alias recognition is tested in each of the four cells.
alias_results=[]
for text,wanted in [('AMR\t022\n7072',True),('(AMR_00022-0007072)',True),('AMR-022-7072x',False),('AMR-022-7072-variant',True),('xAMR0227072',False),('AMR-022-70720',False)]:
    for col in range(4):
        row=['']*4;row[col]=text;got=t['row_has_problem_identity'](row);need(got==wanted,'alias edge '+text);alias_results.append({'identity':text,'column':col,'recognized':got})
result={'at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'ready_and_merge':results,'public_downloads':public_results,'alias_boundaries':alias_results,'all_operations_mocked':True,'scratch_only':True,'status':'PASS'}
(R/'FAILURE_PATH_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print({'status':'PASS','merge_cases':len(results),'public_cases':len(public_results),'alias_cases':len(alias_results)})
