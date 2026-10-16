"""Local synthetic release fixtures only; actual helper actions are never allowed."""
from pathlib import Path
from datetime import datetime,timezone
import copy,gc,hashlib,importlib.util,json,runpy,shutil,subprocess,sys,tempfile,urllib.request
D=Path(__file__).resolve().parent;PUB=D.parent/'publication'
spec=importlib.util.spec_from_file_location('release_binding',PUB/'release_binding.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g);sys.modules['release_binding']=g
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
save=lambda p,v:p.write_text(json.dumps(v,indent=2)+'\n')
rows=[];blocked=[]
def reject(name,action):
    try:action()
    except (RuntimeError,FileExistsError,KeyError,FileNotFoundError) as e:rows.append({'test':name,'rejected':True,'exception':type(e).__name__,'reason':str(e)})
    else:raise AssertionError('Accepted invalid release fixture: '+name)
with tempfile.TemporaryDirectory(prefix='pr210-root-release-tests-') as tmp:
    C=Path(tmp);R=C/'preprint';P=C/'publication';R.mkdir();P.mkdir()
    for p in PUB.glob('*.py'):shutil.copyfile(p,P/p.name)
    for n,raw in [('manuscript.pdf',b'SYNTHETIC-PDF-FIXTURE'),('k605a-source-verification.zip',b'SYNTHETIC-ZIP-FIXTURE'),('SOURCE_MANIFEST.json',b'{}\n'),('manuscript.tex',b'SYNTHETIC TEX\n')]: (R/n).write_bytes(raw)
    metadata={'title':'The outer focal-pedal area product in odd elliptic billiards','fixture_only':True};save(R/'metadata.json',metadata)
    pin=lambda n:{'path':n,'bytes':(R/n).stat().st_size,'sha256':sha(R/n)}
    package={'submission_files':[pin('manuscript.pdf'),pin('k605a-source-verification.zip')],'source_manifest':pin('SOURCE_MANIFEST.json'),'manuscript_source':pin('manuscript.tex'),'metadata':pin('metadata.json')};save(R/'PACKAGE_MANIFEST.json',package)
    deposit={'metadata':metadata,'files':copy.deepcopy(g.EXPECTED_DEPOSIT_FILES)};save(R/'deposit.json',deposit)
    helperpins=[{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(P.glob('*.py'))]
    clear=dict(release_cleared=True,fresh_manuscript_reviews=3,final_frozen_clean_reviews=1,unresolved_mandatory_findings=[],unresolved_optional_findings=[],original_native_head=g.ORIGINAL_HEAD,package_manifest_sha256=sha(R/'PACKAGE_MANIFEST.json'),deposit_manifest_sha256=sha(R/'deposit.json'),publication_metadata_sha256=sha(R/'metadata.json'),release_helpers=helperpins,submission_files=package['submission_files'],source_manifest=package['source_manifest'],manuscript_source=package['manuscript_source'],publication_metadata=metadata)
    save(R/'FINAL_CLEARANCE.json',clear);ctx=g.context(R);rows.append({'test':'synthetic fully bound baseline','passed':True})
    def mutate_clear(name,transform):
        d=copy.deepcopy(clear);transform(d);save(R/'FINAL_CLEARANCE.json',d);reject(name,lambda:g.context(R));save(R/'FINAL_CLEARANCE.json',clear)
    mutate_clear('false release clearance',lambda d:d.update(release_cleared=False))
    mutate_clear('fewer than two fresh manuscript reviews',lambda d:d.update(fresh_manuscript_reviews=1))
    mutate_clear('no clean frozen review',lambda d:d.update(final_frozen_clean_reviews=0))
    mutate_clear('unresolved optional finding',lambda d:d.update(unresolved_optional_findings=['fixture']))
    mutate_clear('wrong original PR head',lambda d:d.update(original_native_head='0'*40))
    bad=copy.deepcopy(deposit);bad['files'][0]['path']='other.pdf';save(R/'deposit.json',bad)
    d=copy.deepcopy(clear);d['deposit_manifest_sha256']=sha(R/'deposit.json');save(R/'FINAL_CLEARANCE.json',d)
    reject('alternate upload path even with separately repinned manifest',lambda:g.context(R));save(R/'deposit.json',deposit);save(R/'FINAL_CLEARANCE.json',clear)
    raw=(R/'manuscript.pdf').read_bytes();(R/'manuscript.pdf').write_bytes(raw+b'change');reject('changed cleared PDF bytes',lambda:g.context(R));(R/'manuscript.pdf').write_bytes(raw)
    z=dict(submitted=True,metadata_and_files_verified=True,exact_reviewed_frozen_files_published=True,release_binding=g.binding(ctx),metadata=metadata,files=ctx['expected_files'],additional_public_readback_error=None,additional_actual_public_file_downloads=[dict(file=x['name'],bytes=x['size'],sha256=x['sha256'],actual_public_download_byte_hash_match=True) for x in ctx['expected_files']],id=99900002,doi='10.5281/zenodo.99900002',doi_url='https://doi.org/10.5281/zenodo.99900002',record_url='https://zenodo.org/records/99900002',doi_resolution={'status':'resolved','http_status':200,'url':'https://doi.org/10.5281/zenodo.99900002','resolved_url':'https://zenodo.org/records/99900002'})
    save(P/'ZENODO_VERIFIED_PUBLICATION.json',z);assert g.publication(R,P,ctx)==z
    def mutate_z(name,transform):
        d=copy.deepcopy(z);transform(d);save(P/'ZENODO_VERIFIED_PUBLICATION.json',d);reject(name,lambda:g.publication(R,P,ctx));save(P/'ZENODO_VERIFIED_PUBLICATION.json',z)
    mutate_z('stale clearance in publication receipt',lambda d:d['release_binding'].update(clearance_sha256='0'*64))
    mutate_z('stale publication PDF set',lambda d:d['files'][0].update(sha256='0'*64))
    mutate_z('stale publication metadata',lambda d:d['metadata'].update(title='other'))
    mutate_z('missing actual public file readback',lambda d:d['additional_actual_public_file_downloads'].pop())
    mutate_z('failed public SHA readback',lambda d:d['additional_actual_public_file_downloads'][0].update(actual_public_download_byte_hash_match=False))
    mutate_z('unresolved DOI',lambda d:d['doi_resolution'].update(status='not_resolved',http_status=404))
    mutate_z('DOI resolves to different record',lambda d:d['doi_resolution'].update(resolved_url='https://zenodo.org/records/99900001'))
    t=dict(verified=True,exact_all_four_cells_readback=True,release_binding=g.binding(ctx),publication_receipt_sha256=sha(P/'ZENODO_VERIFIED_PUBLICATION.json'),doi_url=z['doi_url'],spreadsheet_id='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20',sheet_id=1254632077,values=['https://arxiv.org/abs/2004.12497v11','',z['doi_url'],metadata['title']+' AMR-050-0033 /5100033'])
    save(P/'TRACKER_VERIFIED_APPEND.json',t);assert g.tracker(R,P,ctx,z)==t
    bad=copy.deepcopy(t);bad['publication_receipt_sha256']='0'*64;save(P/'TRACKER_VERIFIED_APPEND.json',bad);reject('stale cross-stage tracker receipt',lambda:g.tracker(R,P,ctx,z));save(P/'TRACKER_VERIFIED_APPEND.json',t)
    intent=P/'fixture-intent.json';g.exclusive_json(intent,{'one':1});before=intent.read_bytes();reject('second exclusive intent creation',lambda:g.exclusive_json(intent,{'one':2}));assert intent.read_bytes()==before
    lock=g.acquire(P);reject('second whole-run lock acquisition',lambda:g.acquire(P));lock.close()
    pr={'number':210,'state':'open','draft':True,'head':{'sha':g.ORIGINAL_HEAD,'ref':'dot/math-5100033','repo':{'full_name':'AlecKriebel/Math'}},'base':{'ref':'main','repo':{'full_name':'AlecKriebel/Math'}}}
    g.pr_identity(pr,g.ORIGINAL_HEAD,True)
    bad=copy.deepcopy(pr);bad['head']['ref']='different';reject('wrong PR head branch',lambda:g.pr_identity(bad,g.ORIGINAL_HEAD,True))
    bad=copy.deepcopy(pr);bad['head']['repo']['full_name']='other/Math';reject('wrong PR head repository',lambda:g.pr_identity(bad,g.ORIGINAL_HEAD,True))
    # Actual helper entry under -O must stop before import of action code or any fixture mutation.
    for p in sorted(P.glob('*.py')):
        completed=subprocess.run([sys.executable,'-O','-B',str(p)],capture_output=True,text=True)
        assert completed.returncode!=0 and ('optimized Python' in completed.stderr),p
        rows.append({'test':p.name+' optimized entry refused','passed':True})
    # Actual normal-mode top-levels see an existing FALSE clearance; all subprocess/network calls trapped.
    clear_false=copy.deepcopy(clear);clear_false['release_cleared']=False;save(R/'FINAL_CLEARANCE.json',clear_false)
    (P/'ZENODO_VERIFIED_PUBLICATION.json').unlink();(P/'TRACKER_VERIFIED_APPEND.json').unlink()
    original_run=subprocess.run;original_urlopen=urllib.request.urlopen
    def forbidden(*args,**kwargs):blocked.append('forbidden action attempted');raise AssertionError('A provider/CLI call was attempted in false-clearance fixture')
    subprocess.run=forbidden;urllib.request.urlopen=forbidden
    try:
        for name in ['publish_preprint.py','append_verified_tracker.py','integrate_reviewed_pr.py','verify_and_merge.py','verify_published_readonly.py']:
            if name=='verify_and_merge.py':save(P/'PR_PREPARED.json',{'prepared_head':'fixture-only'})
            reject(name+' false clearance blocks normal entry',lambda name=name:runpy.run_path(str(P/name),run_name='__main__'));gc.collect()
            if (P/'PR_PREPARED.json').exists():(P/'PR_PREPARED.json').unlink()
    finally:subprocess.run=original_run;urllib.request.urlopen=original_urlopen
    assert not blocked
result=dict(utc=datetime.now(timezone.utc).isoformat(),synthetic_fixture_only=True,network_or_provider_calls=0,actual_helpers_executed_only_with_optimized_refusal_or_false_clearance=True,all_tests_passed=True,test_count=len(rows),tests=rows,current_helpers=[{'path':p.name,'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(PUB.glob('*.py'))])
save(D/'ROOT_RELEASE_BINDING_TEST_RESULTS.json',result);print(json.dumps(result,indent=2))
