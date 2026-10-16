"""Source04 independent transition probes, copied sources and trapped effects only."""
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import patch
from contextlib import redirect_stdout
import base64, copy, gc, hashlib, io, json, os, runpy, shutil, socket, subprocess, sys, tempfile, urllib.request
import regression_workflow_probes as h

OUT=Path(__file__).resolve().parent
g=h.g
RESULTS=[]
Z='ZENODO_VERIFIED_PUBLICATION.json';T='TRACKER_VERIFIED_APPEND.json'
INTENT='RELEASE_BINDING_RECONCILIATION_ATTEMPT.json'
DONE='RELEASE_BINDING_RECONCILIATION.json'
SOURCE=h.D/'reconcile_published_release_readonly.py'
HISTORY=h.D/'history/release_helpers_review03_frozen'
SHEET='1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
load=lambda p:json.loads(p.read_text())

def record(name,**fields):RESULTS.append(dict(test=name,**fields))
def reject(name,fn,f=None):
    try:fn()
    except (RuntimeError,AssertionError,OSError,ValueError,KeyError) as e:
        record(name,expected_rejection=True,passed=True,error=type(e).__name__,reason=str(e),
               **({} if f is None else dict(readonly_calls=len(f.calls),downloads=len(f.downloads))))
        return e
    raise AssertionError(name+': expected refusal but accepted')

class ReconcileFixture(h.Fixture):
    def __init__(self,base):
        super().__init__(base)
        self.H=self.D/'history/release_helpers_review03_frozen'
        shutil.copytree(HISTORY,self.H)
        self.script=self.D/SOURCE.name;shutil.copyfile(SOURCE,self.script)
        for n in [Z,T,'STAGE_ATTEMPT.json','PUBLISH_ATTEMPT.json']:
            shutil.copyfile(self.H/n,self.P/n)
        self.clear.update(prior_published_clearance_sha256=sha(self.H/'FINAL_CLEARANCE.json'),
          supplemental_readonly_reconciliation=dict(path=self.script.name,bytes=self.script.stat().st_size,sha256=sha(self.script)))
        h.save(self.R/'FINAL_CLEARANCE.json',self.clear);self.ctx=g.context(self.R)
        self.oz=load(self.H/Z);self.ot=load(self.H/T)
        self.provider=self.provider_from(self.oz)
        self.props=dict(sheets=[dict(properties=dict(sheetId=1254632077,title='Math Puzzles'))])
        self.cells=[self.ot['values']]
        self.on_call=None;self.exitcode=0
        self.initial={str(p.relative_to(base)):p.read_bytes() for p in self.H.iterdir() if p.is_file()}
        self.initial_intents={n:(self.P/n).read_bytes() for n in ['STAGE_ATTEMPT.json','PUBLISH_ATTEMPT.json']}
        self.allow_alternate_record=False
    def provider_from(self,z):
        return dict(environment='production',state='published',files=self.ctx['expected_files'],
          **{k:copy.deepcopy(z[k]) for k in ['id','doi','doi_url','record_url','doi_resolution']})
    def run(self,argv,*args,**kw):
        self.calls.append(list(argv))
        if self.on_call:self.on_call(argv)
        if argv[0].endswith('/gh'):
            assert argv[1:] in [['api','repos/AlecKriebel/Math/pulls/210'],
              ['api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+h.OLD]],argv
            v=copy.deepcopy(self.pr) if argv[-1].endswith('/210') else dict(sha=self.intake['Queue_blob'],content=base64.b64encode(self.qraw).decode())
        elif argv[0].endswith('/gws'):
            params=json.loads(argv[argv.index('--params')+1]);assert params['spreadsheetId']==SHEET
            if argv[1:4]==['sheets','spreadsheets','get']:v=self.props
            else:
                assert argv[1:5]==['sheets','spreadsheets','values','get'],argv
                assert params['range']==self.ot['updated_range'],params
                v=dict(values=self.cells)
        else:
            assert argv[1:4]==['-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','inspect'],argv
            assert argv[-1]=='--check-doi' and argv[-2]==str(self.R/'deposit.json'),argv
            v=self.provider
        return h.Fixture.response(v,True,self.exitcode)
    def urlopen(self,request,*args,**kwargs):
        url=request.full_url
        exact={self.provider['record_url']+'/files/'+x['name']+'?download=1' for x in self.ctx['expected_files']}
        assert url in exact,url
        return super().urlopen(request,*args,**kwargs)
    def execute_reconcile(self):
        previous=sys.path[:];sys.path.insert(0,str(self.P));handles=[];real=g.acquire
        def lock(pub):
            f=real(pub);handles.append(f);return f
        with patch.object(subprocess,'run',self.run),patch.object(subprocess,'Popen',h.forbidden),\
          patch.object(urllib.request,'urlopen',self.urlopen),patch.object(socket,'socket',h.forbidden),\
          patch.object(socket,'create_connection',h.forbidden),patch.object(g,'acquire',lock),redirect_stdout(io.StringIO()):
            try:runpy.run_path(str(self.script),run_name='__main__')
            finally:
                for f in handles:f.close()
                sys.path[:]=previous;gc.collect()
    def archive_unchanged(self):
        return all((self.base/p).read_bytes()==raw for p,raw in self.initial.items())
    def refresh_archive_manifest(self):
        m=load(self.H/'ARCHIVE_MANIFEST.json')
        for row in m['files']:
            p=self.H/row['path'];row.update(bytes=p.stat().st_size,sha256=sha(p))
        h.save(self.H/'ARCHIVE_MANIFEST.json',m)
    def replace_history_receipts(self,z=None,t=None):
        if z is not None:
            h.save(self.H/Z,z);shutil.copyfile(self.H/Z,self.P/Z);self.oz=z
        if t is not None:
            h.save(self.H/T,t);shutil.copyfile(self.H/T,self.P/T);self.ot=t;self.cells=[t['values']]
        self.refresh_archive_manifest()

def fixture(fn):
    with tempfile.TemporaryDirectory(prefix='independent04-',dir=OUT) as d:fn(ReconcileFixture(Path(d)))

def normal(f):
    f.execute_reconcile();z=g.publication(f.R,f.P,f.ctx);t=g.tracker(f.R,f.P,f.ctx,z)
    assert z['id']==23398175 and t['updated_range']=="'Math Puzzles'!A113:D113"
    assert len(f.calls)==5 and len(f.downloads)==2 and f.archive_unchanged()
    assert all((f.P/n).read_bytes()==raw for n,raw in f.initial_intents.items())
    assert (f.P/INTENT).exists() and (f.P/DONE).exists()
    record('normal exact old-to-new binding with fresh SAME deposit and four cells',passed=True,readonly_calls=5,downloads=2,archive_unchanged=True,original_intents_unchanged=True)
    calls=len(f.calls);reject('reconciliation reentry stops before provider calls',f.execute_reconcile,f);assert len(f.calls)==calls
    f.run=h.Fixture.run.__get__(f)
    f.execute('integrate_reviewed_pr.py')
    assert (f.P/'PR_PREPARED.json').exists()
    record('reconciled receipts permit queued MAIN integration in trapped fixture',passed=True)

def local_guards():
    changes={
      'stale old-clearance authority':lambda f:f.clear.update(prior_published_clearance_sha256='0'*64),
      'stale supplemental self pin':lambda f:f.clear['supplemental_readonly_reconciliation'].update(sha256='0'*64),
      'changed current helper':lambda f:(f.P/'integrate_reviewed_pr.py').write_text('tamper'),
      'changed archive receipt without manifest repair':lambda f:(f.H/Z).write_text('{}'),
      'changed current publication receipt':lambda f:(f.P/Z).write_text('{}'),
      'changed current tracker receipt':lambda f:(f.P/T).write_text('{}'),
      'existing native source':lambda f:(f.P/'native_current_source').mkdir(),
      'existing native ref intent':lambda f:h.save(f.P/'NATIVE_PREPARE_ATTEMPT.json',{}),
    }
    for name,change in changes.items():
        def test(f,name=name,change=change):
            change(f)
            if name in ['stale old-clearance authority','stale supplemental self pin']:h.save(f.R/'FINAL_CLEARANCE.json',f.clear)
            reject(name,f.execute_reconcile,f);assert not f.calls and not (f.P/INTENT).exists()
        fixture(test)
    def old_clear(f):
        shutil.copyfile(f.H/'FINAL_CLEARANCE.json',f.R/'FINAL_CLEARANCE.json')
        reject('genuine old-style clearance refuses changed integrator pin',f.execute_reconcile,f);assert not f.calls
    fixture(old_clear)

def provider_guards():
    variants={
      'wrong deposit identity':lambda f:f.provider.update(id=23398176),
      'sandbox environment':lambda f:f.provider.update(environment='sandbox'),
      'unpublished state':lambda f:f.provider.update(state='draft'),
      'missing provider file':lambda f:f.provider['files'].pop(),
      'wrong DOI version':lambda f:f.provider.update(doi='10.5281/zenodo.23398176'),
      'DOI resolved elsewhere':lambda f:f.provider['doi_resolution'].update(resolved_url='https://zenodo.org/records/23398176'),
      'wrong tracker tab title':lambda f:f.props['sheets'][0]['properties'].update(title='Other'),
      'changed existing fourth cell':lambda f:f.cells[0].__setitem__(3,'wrong notes'),
      'wrong public SHA':lambda f:setattr(f,'fail_download',True),
    }
    for name,change in variants.items():
        def test(f,name=name,change=change):
            change(f);reject(name,f.execute_reconcile,f)
            assert not (f.P/INTENT).exists() and f.archive_unchanged()
        fixture(test)

def coherent_tampering():
    def record_change(f):
        z=copy.deepcopy(f.oz);z.update(id=23398176,doi='10.5281/zenodo.23398176',doi_url='https://doi.org/10.5281/zenodo.23398176',record_url='https://zenodo.org/records/23398176')
        z['doi_resolution'].update(url=z['doi_url'],resolved_url=z['record_url'])
        t=copy.deepcopy(f.ot);t['doi_url']=z['doi_url'];t['values'][2]=z['doi_url']
        f.replace_history_receipts(z=z);t['publication_receipt_sha256']=sha(f.H/Z);f.replace_history_receipts(t=t)
        f.provider=f.provider_from(z);f.execute_reconcile();g.tracker(f.R,f.P,f.ctx)
        record('coherently rewritten archive/current receipts and unpinned manifest select OTHER deposit',passed=False,defect_reproduced=True,accepted_record_id=load(f.P/Z)['id'],expected_record_id=23398175,readonly_calls=len(f.calls))
    fixture(record_change)
    def range_change(f):
        t=copy.deepcopy(f.ot);t['updated_range']="'Other tab'!A7:D7";f.replace_history_receipts(t=t)
        f.execute_reconcile();g.tracker(f.R,f.P,f.ctx)
        record('coherently rewritten unpinned archived range selects OTHER tab/cells',passed=False,defect_reproduced=True,accepted_range=load(f.P/T)['updated_range'],expected_range="'Math Puzzles'!A113:D113")
    fixture(range_change)
    def late_archive(f):
        fired=False
        def mutate(argv):
            nonlocal fired
            if not fired:
                fired=True;z=load(f.H/Z);z['late_unverified_archive_change']=True;h.save(f.H/Z,z)
        f.on_call=mutate;f.execute_reconcile();z=g.publication(f.R,f.P,f.ctx)
        assert z['initial_publication_receipt_sha256']==sha(f.H/Z)
        assert 'late_unverified_archive_change' not in z
        record('archive changes after initial check yet new receipt provenance hashes changed bytes',passed=False,defect_reproduced=True,archive_unchanged=f.archive_unchanged(),new_receipt_points_to_unaccepted_archive=True)
    fixture(late_archive)
    def late_current(f):
        before=(f.P/Z).read_bytes();fired=False
        def mutate(argv):
            nonlocal fired
            if not fired:
                fired=True;z=load(f.P/Z);z['late_current_evidence_change']=True;h.save(f.P/Z,z)
        f.on_call=mutate;f.execute_reconcile();z=g.publication(f.R,f.P,f.ctx)
        assert 'late_current_evidence_change' not in z and f.archive_unchanged()
        record('current publication receipt changes mid-flight and is silently overwritten',passed=False,defect_reproduced=True,changed_current_evidence_preserved=False,original_archive_still_present=True)
    fixture(late_current)
    def changed_intent(f):
        (f.P/'PUBLISH_ATTEMPT.json').write_text('{"wrong_initial_intent":true}\n')
        f.execute_reconcile();g.tracker(f.R,f.P,f.ctx)
        record('initial current publish intent differs from pinned archive yet transition accepts',passed=False,defect_reproduced=True,intent_vs_archive_match=False)
    fixture(changed_intent)

def failure_controls():
    for dest in [Z,T]:
        def test(f,dest=dest):
            real=os.replace;fired=False
            def fail(a,b):
                nonlocal fired
                if Path(b)==f.P/dest:fired=True;raise OSError('synthetic receipt replace failure '+dest)
                return real(a,b)
            with patch.object(os,'replace',fail):reject(dest+' replacement interruption',f.execute_reconcile,f)
            assert fired and (f.P/INTENT).exists() and f.archive_unchanged() and not (f.P/DONE).exists()
            calls=len(f.calls);reject(dest+' interruption rerun stops before calls',f.execute_reconcile,f);assert len(f.calls)==calls
            calls=len(f.calls);reject(dest+' interruption blocks native integration',lambda:f.execute('integrate_reviewed_pr.py'),f);assert len(f.calls)==calls
        fixture(test)
    def final_write(f):
        real=g.exclusive_json
        def fail(p,data):
            if Path(p)==f.P/DONE:raise OSError('synthetic final reconciliation receipt write failure')
            return real(p,data)
        with patch.object(g,'exclusive_json',fail):reject('final audit receipt write failure propagates',f.execute_reconcile,f)
        assert (f.P/INTENT).exists() and not (f.P/DONE).exists() and f.archive_unchanged()
        g.tracker(f.R,f.P,f.ctx)
        record('final audit write fault leaves fully fresh valid pair and sticky intent',passed=True,verified_pair_complete=True,automatic_reconciliation_retry_blocked=True)
    fixture(final_write)

def queued_guards():
    # Source-derived placeholder controls above are deliberately distinct from
    # this exact saved live MAIN row. A successful synthetic row is no substitute.
    with tempfile.TemporaryDirectory(prefix='actualqueued04-',dir=OUT) as d:
        f=h.Fixture(Path(d));f.seed_publication();f.execute('append_verified_tracker.py')
        captured=h.SOURCE_PUB/'private_transport/native_prepare_20261015T142749854176Z/008-stdout.json'
        payload=load(captured);actual=base64.b64decode(payload['content']).decode()
        row=next(x for x in actual.splitlines() if '5100033 / AMR-050-0033' in x)
        source_row=f.main_qraw.decode().splitlines()[0]
        assert row!=source_row and all(row.split('|')[i]=='  ' for i in [10,11,12])
        f.main_qraw=(row+'\n| other problem | unchanged |\n').encode()
        before=len(f.calls)
        reject('actual retained MAIN queued row still refuses current repaired source',lambda:f.execute('integrate_reviewed_pr.py'),f)
        assert not (f.P/'native_current_source').exists() and not (f.P/'NATIVE_PREPARE_ATTEMPT.json').exists()
        assert not any('--method' in c and c[c.index('--method')+1] in ['POST','PATCH','PUT'] for c in f.calls[before:])
        record('actual MAIN whitespace regression',passed=False,defect_reproduced=True,origin='independently confirmed root-reported finding',actual_empty_cell_lengths=[len(row.split('|')[i]) for i in [10,11,12]],reconstructed_empty_cell_lengths=[len(source_row.split('|')[i]) for i in [10,11,12]],copy_or_native_mutations=0)
    # Each changed MAIN column starts from the exact observed placeholder.
    for index in range(1,13):
        def test(f,index=index):
            f.seed_publication();f.execute('append_verified_tracker.py')
            lines=f.main_qraw.decode().splitlines();cols=lines[0].split('|');cols[index]+=' altered';lines[0]='|'.join(cols);f.main_qraw=('\n'.join(lines)+'\n').encode()
            before=len(f.calls);reject('MAIN queued near miss column '+str(index),lambda:f.execute('integrate_reviewed_pr.py'),f)
            assert not (f.P/'native_current_source').exists() and not (f.P/'NATIVE_PREPARE_ATTEMPT.json').exists()
            assert not any('--method' in c and c[c.index('--method')+1] in ['POST','PATCH','PUT'] for c in f.calls[before:])
        with tempfile.TemporaryDirectory(prefix='queued04-',dir=OUT) as d:test(h.Fixture(Path(d)))
    def claimed(f):
        f.seed_publication();f.execute('append_verified_tracker.py');f.main_qraw=f.qraw;f.execute('integrate_reviewed_pr.py')
        record('prior claimed_solved MAIN route retained',passed=True)
    with tempfile.TemporaryDirectory(prefix='claimed04-',dir=OUT) as d:claimed(h.Fixture(Path(d)))

if __name__=='__main__':
    fixture(normal);local_guards();provider_guards();coherent_tampering();failure_controls();queued_guards()
    value=dict(utc=datetime.now(timezone.utc).isoformat(),review='source04',synthetic_fixture_only=True,
      actual_provider_network_subprocess_Git_writes=0,independently_authored=True,
      tests=RESULTS,test_count=len(RESULTS),defect_count=sum(bool(x.get('defect_reproduced')) for x in RESULTS),
      actual_helpers_executed=False,completion_percent=85)
    h.save(OUT/'INDEPENDENT_RECONCILIATION_RESULTS.json',value)
    print(json.dumps({k:v for k,v in value.items() if k!='tests'},indent=2))
