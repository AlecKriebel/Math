"""Fresh source05 adversarial controls using source04's fixture protocol only.

Action sources are copied byte-identically from frozen_inputs. All subprocess,
Popen, network/socket entry points are trapped. Nothing invokes an actual CLI.
These control assertions and mutations were authored independently for source05.
"""
from pathlib import Path
from datetime import datetime,timezone
from unittest.mock import patch
from contextlib import redirect_stdout
import base64,copy,gc,hashlib,io,json,os,runpy,shutil,socket,subprocess,sys,tempfile,urllib.request
import regression_workflow_probes as h

O=Path(__file__).resolve().parent;D=O.parent;g=h.g
Z='ZENODO_VERIFIED_PUBLICATION.json';T='TRACKER_VERIFIED_APPEND.json'
ATTEMPT='RELEASE_BINDING_RECONCILIATION_ATTEMPT.json';DONE='RELEASE_BINDING_RECONCILIATION.json'
EVIDENCE=[Z,T,'STAGE_ATTEMPT.json','PUBLISH_ATTEMPT.json','ZENODO_STAGED_VERIFIED.json','ZENODO_TOOL_PUBLICATION_RECEIPT.json','ZENODO_PROVIDER_CONFIRMED_PUBLICATION.json']
HIST=D/'history/release_helpers_review03_frozen'
CAPTURE=D.parent/'publication/private_transport/native_prepare_20261015T142749854176Z'
SHEET='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
sha=lambda raw:hashlib.sha256(raw).hexdigest()
read=lambda p:json.loads(p.read_text())
RESULTS=[]
def record(name,**kw):RESULTS.append(dict(test=name,passed=True,**kw))

def must_reject(name,fn,f=None,precall=False,preintent=True):
    before=0 if f is None else len(f.calls)
    try:fn()
    except (RuntimeError,AssertionError,OSError,ValueError,KeyError,TypeError) as e:
        if f is not None:
            if precall:assert len(f.calls)==before,(name,'unexpected call')
            if preintent:assert not (f.P/ATTEMPT).exists(),name
        record(name,refused=type(e).__name__,reason=str(e),**({} if f is None else dict(trapped_call_count=len(f.calls),public_download_count=len(f.downloads))))
        return e
    raise AssertionError(name+': unexpectedly accepted')

class Fixture(h.Fixture):
    def __init__(self,base):
        super().__init__(base)
        self.H=self.D/'history/release_helpers_review03_frozen';shutil.copytree(HIST,self.H)
        for n in EVIDENCE:shutil.copyfile(self.H/n,self.P/n)
        self.script=self.D/'reconcile_published_release_readonly.py';shutil.copyfile(O/'frozen_inputs'/self.script.name,self.script)
        self.clear=read(O/'frozen_inputs/RENEWED_CLEARANCE_CANDIDATE.json')
        self.clear.update(release_cleared=True,synthetic_fixture_only=True,candidate_only=False,supporting_source05_pending=False)
        self.refresh_clear()
        self.z=read(self.H/Z);self.t=read(self.H/T)
        self.provider=dict(environment='production',state='published',files=copy.deepcopy(self.ctx['expected_files']),**{k:copy.deepcopy(self.z[k]) for k in ['id','doi','doi_url','record_url','doi_resolution']})
        self.props={'sheets':[{'properties':{'sheetId':1254632077,'title':'Math Puzzles'}}]}
        self.cells=[copy.deepcopy(self.t['values'])];self.hook=None;self.download_hook=None;self.command_error_at=None
        self.archive_before={p.name:p.read_bytes() for p in self.H.iterdir() if p.is_file()}
        self.evidence_before={n:(self.P/n).read_bytes() for n in EVIDENCE}
        # Use byte-for-byte captured native rows, retaining an independent foreign sentinel.
        oq=read(CAPTURE/'002-stdout.json');mq=read(CAPTURE/'008-stdout.json')
        original=next(x for x in base64.b64decode(oq['content']).decode().splitlines() if '5100033 / AMR-050-0033' in x)
        actual=next(x for x in base64.b64decode(mq['content']).decode().splitlines() if '5100033 / AMR-050-0033' in x)
        self.qraw=(original+'\n| foreign sentinel | remains exact |\n').encode()
        self.main_qraw=(actual+'\n| foreign sentinel | remains exact |\n').encode()
        self.commits[self.main]['tree']['sha']=self.make_tree({h.QPATH:self.main_qraw,'foreign/preserved.txt':b'foreign main bytes\n'})
        self.captured_original_row=original;self.captured_main_row=actual
    def refresh_clear(self):
        h.save(self.R/'FINAL_CLEARANCE.json',self.clear);self.ctx=g.context(self.R)
    def run(self,argv,*args,**kw):
        self.calls.append(list(argv))
        if self.hook:self.hook(argv)
        if self.command_error_at==len(self.calls):raise subprocess.TimeoutExpired(argv,180)
        if argv[0].endswith('/gh'):
            if argv[1:]==['api','repos/AlecKriebel/Math/pulls/210']:value=copy.deepcopy(self.pr)
            else:
                assert argv[1:]==['api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+h.OLD],argv
                value={'sha':self.intake['Queue_blob'],'content':base64.b64encode(self.qraw).decode()}
        elif argv[0].endswith('/gws'):
            p=json.loads(argv[argv.index('--params')+1]);assert p['spreadsheetId']==SHEET
            if argv[1:4]==['sheets','spreadsheets','get']:
                assert p=={'spreadsheetId':SHEET};value=self.props
            else:
                assert argv[1:5]==['sheets','spreadsheets','values','get'],argv
                assert p==dict(spreadsheetId=SHEET,range=self.t['updated_range']);value={'values':self.cells}
        else:
            assert argv[1:]==['-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','inspect',str(self.R/'deposit.json'),'--check-doi'],argv
            value=self.provider
        return h.Fixture.response(value,True)
    def urlopen(self,request,*args,**kw):
        exact={self.provider['record_url']+'/files/'+x['name']+'?download=1' for x in self.ctx['expected_files']}
        assert request.full_url in exact
        if self.download_hook:self.download_hook(request)
        return super().urlopen(request,*args,**kw)
    def reconcile(self):
        handles=[];real=g.acquire;previous=sys.path[:]
        def capture(pub):handle=real(pub);handles.append(handle);return handle
        with patch.object(subprocess,'run',self.run),patch.object(subprocess,'Popen',h.forbidden),patch.object(urllib.request,'urlopen',self.urlopen),patch.object(socket,'socket',h.forbidden),patch.object(socket,'create_connection',h.forbidden),patch.object(g,'acquire',capture),redirect_stdout(io.StringIO()):
            try:runpy.run_path(str(self.script),run_name='__main__')
            finally:
                for handle in handles:handle.close()
                sys.path[:]=previous;gc.collect()
    def archive_exact(self):return all((self.H/n).read_bytes()==raw for n,raw in self.archive_before.items())
    def evidence_exact(self):return all((self.P/n).read_bytes()==raw for n,raw in self.evidence_before.items())
    def rehash_archive(self,refresh_authority=False,refresh_evidence_pins=False):
        m=read(self.H/'ARCHIVE_MANIFEST.json')
        for row in m['files']:
            p=self.H/row['path'];row.update(bytes=p.stat().st_size,sha256=sha(p.read_bytes()))
        h.save(self.H/'ARCHIVE_MANIFEST.json',m)
        if refresh_authority:
            p=self.H/'ARCHIVE_MANIFEST.json';self.clear['initial_publication_tracker_state']['archive_manifest']=dict(path=p.name,bytes=p.stat().st_size,sha256=sha(p.read_bytes()))
        if refresh_evidence_pins:
            byname={r['path']:r for r in m['files']}
            for k,n in [('publication_receipt',Z),('tracker_receipt',T),('stage_intent','STAGE_ATTEMPT.json'),('publish_intent','PUBLISH_ATTEMPT.json')]:self.clear['initial_publication_tracker_state'][k]=byname[n]
        if refresh_authority or refresh_evidence_pins:self.refresh_clear()
    def native(self):
        # Dispatch only this separately authorized synthetic phase to full native mock.
        old=self.run;self.run=h.Fixture.run.__get__(self)
        try:self.execute('integrate_reviewed_pr.py')
        finally:self.run=old

def each(fn):
    with tempfile.TemporaryDirectory(prefix='source05-',dir=O) as tmp:fn(Fixture(Path(tmp)))

def clean_transition(f):
    f.reconcile();z=g.publication(f.R,f.P,f.ctx);t=g.tracker(f.R,f.P,f.ctx,z)
    assert len(f.calls)==5 and len(f.downloads)==2 and z['id']==23398175 and t['updated_range']=="'Math Puzzles'!A113:D113"
    assert f.archive_exact() and all((f.P/n).read_bytes()==f.evidence_before[n] for n in EVIDENCE if n not in [Z,T])
    assert z['initial_publication_receipt_sha256']==sha(f.evidence_before[Z]) and t['initial_tracker_receipt_sha256']==sha(f.evidence_before[T])
    assert z['additional_stage_or_publish_calls']==0 and t['additional_append_or_update_calls']==0
    assert read(f.P/DONE)['prior_evidence_preserved'] and read(f.P/ATTEMPT)['record_id']==23398175
    record('fresh SAME-pair/read-only transition and preserved original evidence',readonly_inspections=5,downloads=2,retained_archive_payloads=len(f.archive_before))
    must_reject('normal reconciliation reentry blocks before any call',f.reconcile,f,precall=True,preintent=False)
    f.native();p=read(f.P/'PR_PREPARED.json')
    assert p['parents']==[h.OLD,f.main] and f.pr['head']['sha']==p['prepared_head']
    assert f.native_files[h.QPATH].decode().splitlines()[1]=='| foreign sentinel | remains exact |'
    assert all(len(f.captured_main_row.split('|')[i])==2 for i in [10,11,12])
    assert (f.P/'native_current_source/PROOF.md').read_bytes()==(f.R/'pr_update/5100033/PROOF.md').read_bytes()
    assert {r['path'] for r in p['included_owned_pins']} >= {h.PREFIX+'PROOF.md'}
    record('actual captured MAIN two-space placeholder completes native prepare after receipt rebinding',two_parent_nonforce=True,foreign_queue_preserved=True,science_unchanged=True)
    # Fixture tree constructor reconstructs only mocked files; explicitly inspect posted base_tree to cover foreign MAIN preservation.
    tree_req=next(read(Path(c[c.index('--input')+1])) for c in f.calls if '--method' in c and c[c.index('--method')+1]=='POST' and c[c.index('--method')+2].endswith('/git/trees'))
    assert tree_req['base_tree']==f.commits[f.main]['tree']['sha']
    record('native tree request uses entire current MAIN as base, including foreign subtree',base_tree=f.commits[f.main]['tree']['sha'])
    old=f.run;f.run=h.Fixture.run.__get__(f)
    try:f.execute('verify_and_merge.py')
    finally:f.run=old
    assert f.ready_count==f.merge_count==1 and read(f.P/'PR_MERGED.json')['merged']
    record('complete renewal/reconciliation/actual-placeholder/native-readback/ready/merge transition',mocked_ready_count=1,mocked_merge_count=1)

def authorization_checks():
    def candidate(f):
        shutil.copyfile(O/'frozen_inputs/RENEWED_CLEARANCE_CANDIDATE.json',f.R/'FINAL_CLEARANCE.json')
        must_reject('exact candidate is false and cannot authorize any read-only reconciliation',f.reconcile,f,precall=True)
    each(candidate)
    def old(f):
        shutil.copyfile(f.H/'FINAL_CLEARANCE.json',f.R/'FINAL_CLEARANCE.json')
        must_reject('actual retained old clearance rejects repaired native helper',f.reconcile,f,precall=True)
    each(old)
    for key in ['prior_published_clearance_sha256','supplemental_readonly_reconciliation']:
        def one(f,key=key):
            if key=='supplemental_readonly_reconciliation':f.clear[key]['sha256']='0'*64
            else:f.clear[key]='0'*64
            f.refresh_clear();must_reject('wrong '+key+' rejects before provider',f.reconcile,f,precall=True)
        each(one)
    for key in ['archive_manifest','publication_receipt','tracker_receipt','stage_intent','publish_intent']:
        def one(f,key=key):
            f.clear['initial_publication_tracker_state'][key]['sha256']='0'*64;f.refresh_clear()
            must_reject('explicit original authority pin '+key+' refuses mismatch',f.reconcile,f,precall=True)
        each(one)
    for n in ['NATIVE_PREPARE_ATTEMPT.json','PR_PREPARED.json','native_current_source']:
        def one(f,n=n):
            if n=='native_current_source':(f.P/n).mkdir()
            else:h.save(f.P/n,{})
            must_reject('preexisting '+n+' blocks reconciliation',f.reconcile,f,precall=True)
        each(one)

def original_identity_attacks():
    def alternate(f,kind):
        if kind=='record':
            z=read(f.H/Z);z.update(id=23398176,doi='10.5281/zenodo.23398176',doi_url='https://doi.org/10.5281/zenodo.23398176',record_url='https://zenodo.org/records/23398176');z['doi_resolution'].update(url=z['doi_url'],resolved_url=z['record_url'])
            h.save(f.H/Z,z);shutil.copyfile(f.H/Z,f.P/Z)
            t=read(f.H/T);t['doi_url']=z['doi_url'];t['values'][2]=z['doi_url'];t['publication_receipt_sha256']=sha((f.H/Z).read_bytes())
        else:t=read(f.H/T);t['updated_range']="'Other tab'!A7:D7"
        h.save(f.H/T,t);shutil.copyfile(f.H/T,f.P/T)
        f.rehash_archive()
        must_reject('source04 coherent '+kind+' substitution blocked by pinned archive',f.reconcile,f,precall=True)
    for kind in ['record','range']:each(lambda f,kind=kind:alternate(f,kind))
    def explicit(f,kind):
        # Independently exercise exact record/destination authority after allowing a rehashed archive in a synthetic clearance.
        if kind=='record':
            z=read(f.H/Z);z.update(id=23398176,doi='10.5281/zenodo.23398176',doi_url='https://doi.org/10.5281/zenodo.23398176',record_url='https://zenodo.org/records/23398176');z['doi_resolution'].update(url=z['doi_url'],resolved_url=z['record_url']);h.save(f.H/Z,z);shutil.copyfile(f.H/Z,f.P/Z)
        else:
            t=read(f.H/T);t['updated_range']="'Other tab'!A7:D7";h.save(f.H/T,t);shutil.copyfile(f.H/T,f.P/T)
        f.rehash_archive(True,True)
        e=must_reject('explicit original '+kind+' identity still rejects coherent alternate evidence',f.reconcile,f,precall=True)
        assert ('Historical record differs' if kind=='record' else 'Historical tracker cells differ') in str(e)
    for kind in ['record','range']:each(lambda f,kind=kind:explicit(f,kind))
    for label,change in [('duplicate path',lambda m:m['files'].append(copy.deepcopy(m['files'][0]))),('missing member',lambda m:m['files'].pop()),('extra member',lambda m:m['files'].append(dict(path='extra.json',bytes=0,sha256=sha(b'')))),('parent path',lambda m:m['files'][0].update(path='../elsewhere')),('bool size',lambda m:m['files'][0].update(bytes=True))]:
        def one(f,label=label,change=change):
            m=read(f.H/'ARCHIVE_MANIFEST.json');change(m);h.save(f.H/'ARCHIVE_MANIFEST.json',m)
            p=f.H/'ARCHIVE_MANIFEST.json';f.clear['initial_publication_tracker_state']['archive_manifest']=dict(path=p.name,bytes=p.stat().st_size,sha256=sha(p.read_bytes()));f.refresh_clear()
            must_reject('historical archive schema '+label+' rejected under pinned mutated manifest',f.reconcile,f,precall=True)
        each(one)
    def symlink(f):
        p=f.H/'release_binding.py';raw=p.read_bytes();p.unlink();(f.H/'alias.py').write_bytes(raw);p.symlink_to('alias.py')
        must_reject('same-byte historical symlink refused',f.reconcile,f,precall=True)
    each(symlink)

def evidence_checks():
    for n in EVIDENCE:
        def early(f,n=n):
            p=f.P/n;p.write_bytes(p.read_bytes()+b'\n')
            must_reject('current original '+n+' drift before reads',f.reconcile,f,precall=True)
        each(early)
    archive_names=[p.name for p in HIST.iterdir() if p.is_file()]
    for loc,n in [('archive',n) for n in archive_names]+[('current',n) for n in EVIDENCE]:
        def late(f,loc=loc,n=n):
            p=(f.H if loc=='archive' else f.P)/n;initial=p.read_bytes();fired=False
            def hook(argv):
                nonlocal fired
                if not fired:fired=True;p.write_bytes(initial+b'\n')
            f.hook=hook
            must_reject('late accepted '+loc+' evidence drift '+n+' refuses before local intent',f.reconcile,f)
            assert fired and p.read_bytes()==initial+b'\n'
            assert all((f.P/k).read_bytes()==v for k,v in f.evidence_before.items() if not (loc=='current' and k==n))
            assert not (f.P/DONE).exists()
        each(late)
    # Exercise the second guard after exclusive intent, not only the pre-intent guard.
    def during_intent(f):
        real=g.exclusive_json
        def intent(p,v):
            result=real(p,v)
            if Path(p)==f.P/ATTEMPT:(f.H/Z).write_bytes((f.H/Z).read_bytes()+b'\n')
            return result
        with patch.object(g,'exclusive_json',intent):must_reject('evidence changes while local intent flushes; second guard blocks replacements',f.reconcile,f,preintent=False)
        assert (f.P/ATTEMPT).exists() and f.evidence_exact()
        must_reject('post-intent evidence failure rerun stops before calls',f.reconcile,f,precall=True,preintent=False)
    each(during_intent)

def provider_controls():
    variants=[('sandbox',lambda f:f.provider.update(environment='sandbox')),('unpublished',lambda f:f.provider.update(state='draft')),('wrong ID',lambda f:f.provider.update(id=23398176)),('wrong file order',lambda f:f.provider['files'].reverse()),('extra file',lambda f:f.provider['files'].append(copy.deepcopy(f.provider['files'][0]))),('wrong file SHA',lambda f:f.provider['files'][0].update(sha256='0'*64)),('wrong DOI URL',lambda f:f.provider.update(doi_url='https://doi.org/10.5281/zenodo.23398176')),('DOI HTTP failure',lambda f:f.provider['doi_resolution'].update(http_status=404)),('DOI wrong origin',lambda f:f.provider['doi_resolution'].update(resolved_url='https://example.com/records/23398175')),('wrong tab title',lambda f:f.props['sheets'][0]['properties'].update(title='Other tab')),('duplicate tab identity',lambda f:f.props['sheets'].append(copy.deepcopy(f.props['sheets'][0]))),('fourth cell drift',lambda f:f.cells[0].__setitem__(3,'other notes')),('blank DOI cell',lambda f:f.cells[0].__setitem__(2,'')),('extra tracker row',lambda f:f.cells.append(copy.deepcopy(f.cells[0]))),('public bytes differ',lambda f:setattr(f,'fail_download',True))]
    for name,change in variants:
        def one(f,name=name,change=change):
            change(f);must_reject('read-only provider mismatch '+name,f.reconcile,f)
            assert f.archive_exact() and f.evidence_exact()
        each(one)
    for i in range(1,6):
        def timeout(f,i=i):
            f.command_error_at=i
            try:f.reconcile()
            except subprocess.TimeoutExpired:pass
            else:raise AssertionError('timeout swallowed')
            assert f.archive_exact() and f.evidence_exact() and not (f.P/ATTEMPT).exists()
            record('read-only command timeout '+str(i)+' preserves evidence and has no local intent',trapped_calls=len(f.calls))
        each(timeout)
    def url_failure(f):
        def fail(req):raise OSError('synthetic public transport failure')
        f.download_hook=fail;must_reject('public download transport failure preserves original evidence',f.reconcile,f)
        assert f.archive_exact() and f.evidence_exact()
    each(url_failure)

def replacement_faults():
    for target in [Z,T]:
        for kind in ['replace','filefsync','dirsync']:
            def one(f,target=target,kind=kind):
                real_replace=os.replace;real_fsync=os.fsync;real_dir=g.sync_directory;replaced=[];fired=False
                def replacement(a,b):
                    nonlocal fired
                    if kind=='replace' and Path(b)==f.P/target:fired=True;raise OSError('synthetic replace failure '+target)
                    result=real_replace(a,b);replaced.append(Path(b).name);return result
                def fsync(fd):
                    nonlocal fired
                    tmp=f.P/(target+'.reconciliation-tmp')
                    if kind=='filefsync' and tmp.exists():
                        # This path exists only when its own replacement stream is flushing.
                        fired=True;raise OSError('synthetic replacement file fsync failure '+target)
                    return real_fsync(fd)
                def directory(p):
                    nonlocal fired
                    if kind=='dirsync' and Path(p)==f.P and replaced and replaced[-1]==target:fired=True;raise OSError('synthetic replacement directory fsync failure '+target)
                    return real_dir(p)
                with patch.object(os,'replace',replacement),patch.object(os,'fsync',fsync),patch.object(g,'sync_directory',directory):must_reject('local '+target+' '+kind+' fault propagates with sticky intent',f.reconcile,f,preintent=False)
                assert fired and (f.P/ATTEMPT).exists() and not (f.P/DONE).exists() and f.archive_exact()
                assert all((f.P/n).read_bytes()==v for n,v in f.evidence_before.items() if n not in [Z,T])
                must_reject('local '+target+' '+kind+' fault retry refuses before provider',f.reconcile,f,precall=True,preintent=False)
                # Prior to second path replace, pair is incomplete and every native entry is blocked.
                if target==Z or kind in ['replace','filefsync']:
                    before=len(f.calls);must_reject('incomplete '+target+' '+kind+' pair blocks integration',f.native,f,precall=True,preintent=False);assert len(f.calls)==before
                else:
                    # Both values are freshly validated even if last sync failed; record the exact limit without claiming crash durability.
                    g.tracker(f.R,f.P,f.ctx);record('second directory-sync fault leaves two freshly verified readable receipts; no automatic reconciliation retry',crash_durability_not_simulated=True)
            each(one)
    def done_failure(f):
        real=g.exclusive_json
        def fail(p,v):
            if Path(p)==f.P/DONE:raise OSError('synthetic final summary failure')
            return real(p,v)
        with patch.object(g,'exclusive_json',fail):must_reject('final summary failure propagates after both receipts complete',f.reconcile,f,preintent=False)
        g.tracker(f.R,f.P,f.ctx);assert f.archive_exact() and (f.P/ATTEMPT).exists()
        must_reject('final summary failure retry blocked before calls',f.reconcile,f,precall=True,preintent=False)
    each(done_failure)

def additional_local_gates():
    def lock_contention(f):
        held=g.acquire(f.P)
        try:must_reject('shared release lock contention prevents reconciler calls',f.reconcile,f,precall=True)
        finally:held.close()
    each(lock_contention)
    def optimized(f):
        def execute():
            with patch.object(subprocess,'run',h.forbidden),patch.object(subprocess,'Popen',h.forbidden),patch.object(urllib.request,'urlopen',h.forbidden),patch.object(socket,'socket',h.forbidden):
                exec(compile(f.script.read_bytes(),str(f.script),'exec',optimize=1),{'__file__':str(f.script),'__name__':'__main__'})
        must_reject('optimized supplemental reconciler refuses before imports or effects',execute,f,precall=True)
    each(optimized)
    for mode in ['file','directory']:
        def fault(f,mode=mode):
            real=g.sync_directory;real_fsync=os.fsync;fired=False;target=f.P/ATTEMPT
            def directory(p):
                nonlocal fired
                if mode=='directory' and Path(p)==f.P and target.exists():fired=True;raise OSError('synthetic reconciliation intent directory-sync failure')
                return real(p)
            def fsync(fd):
                nonlocal fired
                if mode=='file' and target.exists():fired=True;raise OSError('synthetic reconciliation intent file-sync failure')
                return real_fsync(fd)
            with patch.object(g,'sync_directory',directory),patch.object(os,'fsync',fsync):must_reject('reconciliation intent '+mode+' sync fault blocks both replacements',f.reconcile,f,preintent=False)
            assert fired and target.exists() and f.archive_exact() and f.evidence_exact()
            must_reject('reconciliation intent '+mode+' sync fault retry blocked before calls',f.reconcile,f,precall=True,preintent=False)
        each(fault)
    for what in ['self','helper','clearance','metadata','PDF']:
        def drift(f,what=what):
            target={'self':f.script,'helper':f.P/'integrate_reviewed_pr.py','clearance':f.R/'FINAL_CLEARANCE.json','metadata':f.R/'metadata.json','PDF':f.R/'manuscript.pdf'}[what];fired=False
            def hook(argv):
                nonlocal fired
                if not fired:fired=True;target.write_bytes(target.read_bytes()+b'\n')
            f.hook=hook;must_reject('late accepted '+what+' byte drift blocks local receipt intent',f.reconcile,f)
            assert fired and f.archive_exact() and f.evidence_exact()
        each(drift)

def queue_boundaries():
    # Each test runs the entire copied integrator through the guard with genuine current receipt bindings.
    for i in range(1,13):
        def one(f,i=i):
            f.reconcile();lines=f.main_qraw.decode().splitlines();fields=lines[0].split('|');fields[i]+=' changed';lines[0]='|'.join(fields);f.main_qraw=('\n'.join(lines)+'\n').encode()
            before=len(f.calls);must_reject('actual queued MAIN column '+str(i)+' near miss rejected',f.native,f,preintent=False)
            assert not (f.P/'native_current_source').exists() and not (f.P/'NATIVE_PREPARE_ATTEMPT.json').exists()
            assert not any('--method' in a and a[a.index('--method')+1]!='GET' for a in f.calls[before:])
        each(one)
    for i in [10,11,12]:
        def one(f,i=i):
            f.reconcile();cols=f.captured_main_row.split('|');cols[i]=' ';f.main_qraw=('|'.join(cols)+'\n').encode()
            must_reject('actual queued MAIN one-space empty cell '+str(i)+' rejected',f.native,f,preintent=False)
            assert not (f.P/'native_current_source').exists()
        each(one)
    for status in ['Queued','already_solved','blocked','working','unsolved']:
        def one(f,status=status):
            f.reconcile();cols=f.captured_main_row.split('|');cols[8]=' '+status+' ';f.main_qraw=('|'.join(cols)+'\n').encode()
            must_reject('queued MAIN status '+status+' is not exact untouched placeholder',f.native,f,preintent=False)
            assert not (f.P/'native_current_source').exists()
        each(one)
    def claimed(f):
        f.reconcile();f.main_qraw=f.qraw;f.native();assert (f.P/'PR_PREPARED.json').exists()
        record('previously supported claimed_solved MAIN route remains valid')
    each(claimed)
    def subtree(f):
        f.reconcile();f.commits[f.main]['tree']['sha']=f.make_tree({h.QPATH:f.main_qraw,h.PREFIX+'PROOF.md':b'other science'})
        before=len(f.calls);must_reject('fresh MAIN scientific subtree refuses any integration overwrite',f.native,f,preintent=False)
        assert not (f.P/'native_current_source').exists() and not any('--method' in a and a[a.index('--method')+1]!='GET' for a in f.calls[before:])
    each(subtree)
    for family in ['release_helpers_adversary_04','release_helpers_adversary_05']:
        def one(f,family=family):
            f.reconcile();(f.D/family/'AUTHORED_MANIFEST.json').unlink();before=len(f.calls)
            must_reject('required '+family+' seal missing refuses native object/ref action',f.native,f,preintent=False)
            assert not any('--method' in a and a[a.index('--method')+1]!='GET' for a in f.calls[before:])
        each(one)

if __name__=='__main__':
    each(clean_transition);authorization_checks();original_identity_attacks();evidence_checks();provider_controls();replacement_faults();additional_local_gates();queue_boundaries()
    value=dict(utc=datetime.now(timezone.utc).isoformat(),source_review='05',independently_authored_controls=True,fixture_protocol_reused=True,test_count=len(RESULTS),all_tests_passed=all(x['passed'] for x in RESULTS),tests=RESULTS,real_provider_network_CLI_Git_index_ref_QUEUE_SQL_calls=0,mandatory_findings=[],optional_findings=[],hardware_crash_simulated=False)
    h.save(O/'INDEPENDENT_SOURCE05_RESULTS.json',value);print(json.dumps({k:v for k,v in value.items() if k!='tests'},indent=2))
