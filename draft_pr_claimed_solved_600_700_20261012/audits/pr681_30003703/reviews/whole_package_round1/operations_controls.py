#!/usr/bin/env python3
"""Adversarial runtime controls: exact helper source, FAKE receipts/transports only.

Every fixture is below this review's ignored tmp. No real gh/gws/network/push
dispatch is possible through the adapters. Local Git writes use a toy repo.
"""
import contextlib
import copy
import datetime as dt
import hashlib
import io
import importlib._bootstrap_external
import json
import os
from pathlib import Path
import shutil
import subprocess as real_subprocess
import sys
import types

R = Path(__file__).absolute().parent
LIVE = R.parent.parent
T = R / 'tmp' / ('operations-optimized' if sys.flags.optimize else 'operations-normal')
DOI = '10.5281/zenodo.999999991'
RESULTS = []
DISPATCHES = []
NOW = dt.datetime.now(dt.timezone.utc)


def need(x, label):
    if not x:
        raise RuntimeError(label)


def jbytes(x):
    return (json.dumps(x, indent=2, sort_keys=True) + '\n').encode()


def write(path, x):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(jbytes(x))


def digest(b):
    return hashlib.sha256(b).hexdigest()


def check(name, fun):
    fun()
    RESULTS.append({'name': name, 'outcome': 'PASS'})


def reject(name, fun, text=None):
    try:
        fun()
    except (ValueError, OSError, real_subprocess.CalledProcessError) as exc:
        if text:
            need(text in str(exc), name + ': unexpected error ' + str(exc))
        RESULTS.append({'name': name, 'outcome': 'REJECTED', 'error': str(exc)})
        return
    raise RuntimeError(name + ': ACCEPTED hostile fixture')


def load(path, name):
    m = types.ModuleType(name)
    m.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), 'exec'), m.__dict__)
    return m


class Fixture:
    count = 0

    def __init__(self):
        Fixture.count += 1
        self.root = T / f'f{Fixture.count:03d}'
        self.repo = self.root / 'toyrepo'
        self.a = self.repo / 'program/audits/pr681_30003703'
        self.a.mkdir(parents=True)
        for n in ['prepare_integration.py', 'record_tracker.py', 'SCOPE_AND_SNAPSHOT.json',
                  'MATH_SOURCE_GATE_ACCEPTANCE.json', 'PRIORITY_GATE_ACCEPTANCE.json']:
            shutil.copy2(LIVE / n, self.a / n)
        shutil.copytree(LIVE / 'publication', self.a / 'publication')
        shutil.copytree(LIVE / 'native', self.a / 'native')
        self.h = load(self.a / 'prepare_integration.py', 'exact_integration_fixture')
        self.tr = load(self.a / 'record_tracker.py', 'exact_tracker_fixture')
        self.live = {'number': 681, 'state': 'OPEN', 'isDraft': True, 'baseRefName': 'main',
                     'headRefName': self.h.BRANCH, 'headRefOid': self.h.ORIGINAL,
                     'headRepositoryOwner': {'login': 'AlecKriebel'}, 'isCrossRepository': False}
        self.remote_head = self.h.ORIGINAL
        self.base = None
        self.append_mode = 'ok'
        self.push_mode = 'ok'
        self.append_count = self.push_count = 0
        self.values = [self.tr.HEADERS.copy()]
        self.target_override = None
        self.bad_headers = self.bad_gid = False
        self.calls = []
        self.bindings = json.loads((LIVE / 'WHOLE_PACKAGE_REVIEW_INPUTS.json').read_text())
        self.helpers = self.h.helper_pins()
        self.fake_acceptance()
        self.fake_receipts()
        self.adapter = types.SimpleNamespace(check_output=self.check_output, run=self.run, PIPE=real_subprocess.PIPE)
        self.h.subprocess = self.adapter
        self.tr.subprocess = self.adapter
        self.tr._dependency.subprocess = self.adapter

    def fake_acceptance(self):
        previous = None
        rounds = []
        for i in [1, 2]:
            start = (NOW - dt.timedelta(hours=2, minutes=10 - 2*i)).isoformat()
            end = (NOW - dt.timedelta(hours=2, minutes=9 - 2*i)).isoformat()
            reviewer = f'FAKE-FIXTURE-REVIEWER-{i}'
            report = {'schema': 'pr681-whole-package-review-verdict-v1', 'verdict': 'PASS',
                      'reviewer_id': reviewer, 'pr':681, 'problem_id':'30003703',
                      'original_head':self.h.ORIGINAL, 'started_utc':start, 'completed_utc':end,
                      'previous_report_sha256':previous, 'publication_files':self.bindings['publication_files'],
                      'helper_sha256':self.helpers, 'gate_bindings':self.bindings['gate_bindings'],
                      'mandatory_findings':0, 'optional_findings':0, 'findings':[],
                      'findings_waived':False, 'human_peer_review':False, 'AI_tools_used_extensively':True,
                      'FAKE_FIXTURE_NOT_REAL_REVIEW':True}
            path = f'reviews/fake{i}/VERDICT.json'; write(self.a / path, report)
            previous = digest((self.a/path).read_bytes())
            rounds.append({'reviewer_id':reviewer,'report_path':path,'report_sha256':previous,
                           'mandatory_findings':0,'optional_findings':0})
        accepted = {'schema':'pr681-accepted-publication-inputs-v1','pr':681,'problem_id':'30003703',
                    'original_head':self.h.ORIGINAL,'ready_for_publication':True,
                    'final_live_gate_required_before_writes':True,
                    'created_utc':(NOW-dt.timedelta(hours=1, minutes=40)).isoformat(),
                    'files':self.bindings['publication_files'],'helper_sha256':self.helpers,
                    'gate_bindings':self.bindings['gate_bindings'],'whole_package_review_rounds':rounds,
                    'FAKE_FIXTURE_NOT_REAL_ACCEPTANCE':True}
        write(self.a/'ACCEPTED_PUBLICATION_INPUTS.json',accepted)
        final = {'schema':'pr681-publication-final-acceptance-v1','status':'PASS','pr':681,
                 'problem_id':'30003703','original_head':self.h.ORIGINAL,
                 'created_utc':(NOW-dt.timedelta(hours=1,minutes=30)).isoformat(),
                 'accepted_input_gate_sha256':digest((self.a/'ACCEPTED_PUBLICATION_INPUTS.json').read_bytes()),
                 'claim_scope':self.h.EXPECTED_SCOPE,'FAKE_FIXTURE_NOT_REAL_ACCEPTANCE':True}
        write(self.a/'PUBLICATION_FINAL_ACCEPTANCE.json', final)

    def fake_receipts(self):
        for i,n in enumerate(['ZENODO_PUBLICATION_RECEIPT.json','ZENODO_POST_PUBLICATION_INSPECTION.json']):
            receipt = {'environment':'production','state':'published','receipt_saved':True,
                       'title':self.h.TITLE,'id':999999991,'doi':DOI,'doi_url':'https://doi.org/'+DOI,
                       'record_url':'https://zenodo.org/records/999999991',
                       'verified_utc':(NOW-dt.timedelta(hours=1,minutes=20-i)).isoformat(),
                       'doi_resolution':{'status':'resolved','http_status':200,'url':'https://doi.org/'+DOI,
                                         'resolved_url':'https://zenodo.org/records/999999991'},
                       'files':[{'name':n,'size':p['bytes'],'sha256':p['sha256']}
                                for n,p in self.bindings['publication_files'].items() if n in self.h.UPLOAD_NAMES],
                       'metadata_normalizations':[], 'FAKE_FIXTURE_NOT_REAL_PUBLICATION':True,
                       'fake_observer':i}
            write(self.a/n, receipt)

    def mutate_json(self, path, f):
        p=self.a/path; x=json.loads(p.read_bytes()); f(x); write(p,x)

    def inputs(self):
        return self.h.publication_inputs(self.a/'publication', DOI,
                    self.a/'ZENODO_PUBLICATION_RECEIPT.json', self.a/'ZENODO_POST_PUBLICATION_INSPECTION.json')

    def ready(self):
        p=self.inputs()
        return {'publication_validation':p['validation'],'doi':DOI,'row':self.tr.wanted_row(DOI),'applied':False}

    def repin_report(self, number, mutation):
        path=f'reviews/fake{number}/VERDICT.json'; self.mutate_json(path,mutation)
        self.mutate_json('ACCEPTED_PUBLICATION_INPUTS.json',lambda x:x['whole_package_review_rounds'][number-1].update(
            report_sha256=digest((self.a/path).read_bytes())))
        self.mutate_json('PUBLICATION_FINAL_ACCEPTANCE.json',lambda x:x.update(
            accepted_input_gate_sha256=digest((self.a/'ACCEPTED_PUBLICATION_INPUTS.json').read_bytes())))

    def final_gate(self, kind, validation=None, **extra):
        if validation is None: validation=self.inputs()['validation']
        gate = {'schema':f'pr681-final-{kind}-gate-v1','status':'PASS','pr':681,'problem_id':'30003703',
                'original_head':self.h.ORIGINAL,'doi':DOI,'created_utc':NOW.isoformat(),
                **{k:validation[k] for k in ['accepted_input_gate_sha256','publication_receipt_sha256',
                                            'inspection_receipt_sha256','helper_sha256']},
                'live_pr':{k:self.live[k] for k in ['number','state','isDraft','baseRefName','headRefName','headRefOid']}}
        if kind=='tracker':gate.update(tracker_append_allowed=True,spreadsheet_id=self.tr.ID,
                                     sheet_id=self.tr.GID,sheet_title=self.tr.TAB)
        else:gate.update(integration_allowed=True, main_base=self.base)
        gate.update(extra); write(self.a/f'FINAL_{kind.upper()}_GATE.json',gate)
        return gate

    def check_output(self, command, **kw):
        if command[0]=='gh':
            need(command[:4]==['gh','pr','view','681'],'unexpected gh dispatch')
            self.calls.append(['MOCK_GH_READ',*command[1:]])
            return jbytes(self.live)
        need(command[0]=='git','nonallowlisted subprocess check_output blocked')
        need(Path(kw['cwd'])==self.repo,'Git escaped toy fixture')
        args=command[1:]
        while args and args[0]=='-c':args=args[2:]
        op=args[0]
        self.calls.append(['GIT',op])
        if op=='ls-remote':
            need(args[-2] in {'https://github.com/AlecKriebel/Math.git','https://github.com/AlecKriebel/Math'},
                 'unexpected remote URL')
            ref=args[-1]; oid=self.base if ref=='refs/heads/main' else self.remote_head
            return (oid+'\t'+ref+'\n').encode()
        if op=='fetch':
            need(kw['env'].get('GIT_OBJECT_DIRECTORY','').startswith(str(self.a/'tmp')),
                 'fetch lacks isolated objects')
            need('--no-write-fetch-head' in args and '--refmap=' in args,'unsafe fetch options')
            DISPATCHES.append({'kind':'MOCK_FETCH_NO_NETWORK','fixture':str(self.root),'args':args})
            return b''
        if op=='push':
            need(kw['env'].get('GIT_OBJECT_DIRECTORY','').startswith(str(self.a/'tmp')),
                 'push lacks isolated objects')
            intent=self.a/'INTEGRATION_PUSH_INTENT.json'
            need(intent.is_file(),'push dispatched without durable intent')
            need('--force' not in args and not any(x.startswith('+') for x in args),'force push')
            self.push_count+=1; DISPATCHES.append({'kind':'MOCK_PUSH_NO_NETWORK','fixture':str(self.root),
                    'intent_sha256':digest(intent.read_bytes()),'args':args})
            if self.push_mode=='lost':raise real_subprocess.CalledProcessError(1,command,stderr=b'FAKE lost response')
            self.remote_head=args[-1].split(':')[0];self.live['headRefOid']=self.remote_head
            return b'FAKE push accepted\n'
        need(op not in {'clone','pull','checkout','reset','update-ref'},'dangerous source Git op')
        return real_subprocess.check_output(command,**kw)

    def run(self, command, **kw):
        if command[0]=='gws':
            need(command[1]=='sheets','non-Sheets gws blocked')
            params=json.loads(command[command.index('--params')+1]); method=command[command.index('--params')-1]
            need(params['spreadsheetId']==self.tr.ID,'wrong tracker target')
            self.calls.append(['MOCK_GWS',method,params.get('range')])
            if method=='append':
                need((self.a/'TRACKER_UNCONFIRMED.json').is_file(),'append without durable intent')
                self.append_count+=1
                body=json.loads(command[command.index('--json')+1]);row=body['values'][0]
                need(params['valueInputOption']=='RAW' and params['insertDataOption']=='INSERT_ROWS', 'unsafe append')
                DISPATCHES.append({'kind':'MOCK_GWS_APPEND_NO_NETWORK','fixture':str(self.root),'body':body})
                if self.append_mode!='lost_no_write':self.values.append(copy.deepcopy(row))
                if self.append_mode in {'lost','lost_no_write'}:
                    raise real_subprocess.CalledProcessError(1,command,stderr='FAKE ambiguous response')
                n=len(self.values);out={'spreadsheetId':self.tr.ID,'updates':{
                    'updatedRange':f"'Math Puzzles'!A{n}:D{n}",'updatedRows':1,'updatedColumns':4,
                    'updatedCells':4,'updatedData':{'values':[row]}}}
                if self.append_mode=='bad_response':out['updates']['updatedCells']=3
                if self.append_mode=='duplicate_after':self.values.append(copy.deepcopy(row))
            elif 'values' not in command:
                out={'sheets':[{'properties':{'sheetId': self.tr.GID + int(self.bad_gid),'title':self.tr.TAB}}]}
            elif params['range'].endswith('A1:D1'):
                out={'values':[['wrong']] if self.bad_headers else [self.tr.HEADERS]}
            elif params['range'].endswith('A:D'):out={'values':copy.deepcopy(self.values)}
            else:
                n=int(params['range'].split('!A')[1].split(':')[0]);out={'values':self.target_override or [self.values[n-1]]}
            return types.SimpleNamespace(returncode=0,stdout=json.dumps(out),stderr='')
        need(Path(command[0]).absolute()==Path(sys.executable).absolute(),'non-Python subprocess blocked')
        script=Path(next(x for x in command if x.endswith('.py')))
        need(script.is_relative_to(self.a/'tmp'),'replay script escaped fixture')
        return real_subprocess.run(command,**kw)

    def init_git(self):
        def g(*args,input=None):
            return real_subprocess.check_output(['git',*args],cwd=self.repo,input=input,stderr=real_subprocess.PIPE)
        g('init','-q','-b','main');g('config','user.name','FAKE fixture reviewer');g('config','user.email','fixture.invalid@example.invalid')
        g('remote','add','origin','https://github.com/AlecKriebel/Math.git')
        # Existing real objects are immutable read-only alternates; every new object is toy-local.
        objects=real_subprocess.check_output(['git','rev-parse','--git-path','objects'],cwd=LIVE.parents[2]).decode().strip()
        objects=Path(objects) if Path(objects).is_absolute() else LIVE.parents[2]/objects
        p=self.repo/'.git/objects/info/alternates';p.parent.mkdir(parents=True,exist_ok=True);p.write_text(str(objects)+'\n')
        snapshot=json.loads((self.a/'SCOPE_AND_SNAPSHOT.json').read_bytes())
        cells=snapshot['queue_row'].split('|');cells[8]=' queued ';cells[9]=' 0/5 ';cells[11]=' '
        self.queue=b'outside-before\r\n'+('|'.join(cells)+'\r\n').encode()+b'outside-after unchanged bytes\n'
        blob=g('hash-object','-w','--stdin',input=self.queue).strip()
        qtree=g('mktree',input=b'100644 blob '+blob+b'\tQUEUE.md\n').strip()
        sentinel=g('hash-object','-w','--stdin',input=b'untouched sentinel\x00\xff\n').strip()
        link=g('hash-object','-w','--stdin',input=b'sentinel').strip()
        tree=g('mktree',input=b'040000 tree '+qtree+b'\tunsolved_math_prioritization\n100755 blob '+sentinel+b'\tsentinel\n120000 blob '+link+b'\tlink\n').strip()
        self.base=g('commit-tree',tree,input=b'FAKE toy main fixture\n').decode().strip()
        g('update-ref','refs/heads/main',self.base)
        # Empty index is intentionally created only in toy repository.
        g('read-tree',tree)
        self.git_initial=self.git_snapshot()

    def git_snapshot(self):
        return {p.relative_to(self.repo/'.git').as_posix():digest(p.read_bytes())
                for p in (self.repo/'.git').rglob('*') if p.is_file()}

    def integration(self,push=False):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            argv=sys.argv;sys.argv=['prepare_integration.py','--doi',DOI]+(['--push'] if push else [])
            try:self.h.main()
            finally:sys.argv=argv
        return json.loads(out.getvalue())

    def tracker_main(self,apply=False):
        with contextlib.redirect_stdout(io.StringIO()) as out:
            argv=sys.argv;sys.argv=['record_tracker.py','--doi',DOI]+(['--apply'] if apply else [])
            try:self.tr.main()
            finally:sys.argv=argv
        return json.loads(out.getvalue())


def main():
    if T.exists():
        need(T.parent == R / 'tmp' and T.name.startswith('operations-'), 'unsafe scratch cleanup')
        shutil.rmtree(T)
    T.mkdir(parents=True,exist_ok=True)
    f=Fixture();check('accepted_exact_gate_chain_scope_receipts_archive_and_native23',f.inputs)
    baseline=f.inputs(); v=baseline['validation']
    f.final_gate('tracker',v);check('fresh_final_tracker_gate',lambda:f.h.validate_live_write_gate('tracker',DOI,v))
    for name,path,mutation in [
        ('stale_review_hash','ACCEPTED_PUBLICATION_INPUTS.json',lambda x:x['whole_package_review_rounds'][0].update(report_sha256='0'*64)),
        ('same_reviewer','ACCEPTED_PUBLICATION_INPUTS.json',lambda x:x['whole_package_review_rounds'][1].update(reviewer_id=x['whole_package_review_rounds'][0]['reviewer_id'])),
        ('missing_second_review','ACCEPTED_PUBLICATION_INPUTS.json',lambda x:x.update(whole_package_review_rounds=x['whole_package_review_rounds'][:1])),
        ('expanded_scope','PUBLICATION_FINAL_ACCEPTANCE.json',lambda x:x['claim_scope'].update(degree5_rank3_claim=True)),
        ('future_acceptance','ACCEPTED_PUBLICATION_INPUTS.json',lambda x:x.update(created_utc=(NOW+dt.timedelta(days=1)).isoformat())),
        ('wrong_title','ZENODO_PUBLICATION_RECEIPT.json',lambda x:x.update(title='wrong')),
        ('wrong_doi_id','ZENODO_PUBLICATION_RECEIPT.json',lambda x:x.update(id=999)),
        ('metadata_normalization','ZENODO_PUBLICATION_RECEIPT.json',lambda x:x.update(metadata_normalizations=[{'field':'description'}])),
        ('wrong_remote_file_sha','ZENODO_PUBLICATION_RECEIPT.json',lambda x:x['files'][0].update(sha256='0'*64)),
        ('wrong_resolved_record','ZENODO_PUBLICATION_RECEIPT.json',lambda x:x['doi_resolution'].update(resolved_url='https://zenodo.org/records/1')),
        ('future_public_receipt','ZENODO_PUBLICATION_RECEIPT.json',lambda x:x.update(verified_utc=(NOW+dt.timedelta(days=1)).isoformat())),
        ('nonUTC_public_receipt','ZENODO_PUBLICATION_RECEIPT.json',lambda x:x.update(verified_utc='2026-10-14T23:00:00-07:00')),
        ('inspection_predates_confirmation','ZENODO_POST_PUBLICATION_INSPECTION.json',lambda x:x.update(verified_utc=(NOW-dt.timedelta(days=1)).isoformat())),
    ]:
        old=(f.a/path).read_bytes();f.mutate_json(path,mutation);reject(name,f.inputs);(f.a/path).write_bytes(old)
    for name,mutation in [('expired_gate',lambda x:x.update(created_utc=(NOW-dt.timedelta(minutes=16)).isoformat())),
                         ('future_gate',lambda x:x.update(created_utc=(NOW+dt.timedelta(minutes=1)).isoformat())),
                         ('wrong_sheet',lambda x:x.update(sheet_id=42)),
                         ('extra_live_identity',lambda x:x['live_pr'].update(extra=True))]:
        f.final_gate('tracker',v);f.mutate_json('FINAL_TRACKER_GATE.json',mutation)
        reject(name,lambda:f.h.validate_live_write_gate('tracker',DOI,v))
    for relative in ['publication/satoh_filtration_counterexamples.tex','prepare_integration.py',
                     'MATH_SOURCE_GATE_ACCEPTANCE.json','reviews/fake1/VERDICT.json',
                     'ZENODO_PUBLICATION_RECEIPT.json','native/'+f.h.PREFIX+'release/PROOF.md']:
        p=f.a/relative;old=p.read_bytes();p.write_bytes(old+b'\n');reject('source_recheck_'+relative,lambda:f.h.recheck_sources(v));p.write_bytes(old)
    for name,number,mutation in [
        ('review_chain_wrong_previous',2,lambda x:x.update(previous_report_sha256='0'*64)),
        ('review_overlap',2,lambda x:x.update(started_utc=(NOW-dt.timedelta(days=1)).isoformat())),
        ('review_findings_waived',2,lambda x:x.update(findings_waived=True)),
        ('review_claims_human_review',2,lambda x:x.update(human_peer_review=True)),
        ('review_wrong_helper_pins',2,lambda x:x['helper_sha256'].update(record_tracker='0'*64)),
        ('review_wrong_target',2,lambda x:x.update(problem_id='other')),
    ]:
        q=Fixture();q.repin_report(number,mutation);reject(name,q.inputs)
    q=Fixture();p=q.a/'ZENODO_POST_PUBLICATION_INSPECTION.json';p.write_bytes((q.a/'ZENODO_PUBLICATION_RECEIPT.json').read_bytes())
    reject('identical_publication_and_inspection_receipt_bytes',q.inputs)
    q=Fixture();p=q.a/'SCOPE_AND_SNAPSHOT.json';p.write_bytes(p.read_bytes()+b'\n');reject('immutable_snapshot_change',q.inputs)
    q=Fixture();p=q.a/'native'/q.h.PREFIX/'unexpected.txt';p.write_bytes(b'extra');reject('native_inventory_extra_file',q.inputs)
    q=Fixture();p=q.a/'publication/requirements.txt';p.unlink();p.symlink_to(LIVE/'publication/requirements.txt')
    reject('publication_symlink',q.inputs)
    q=Fixture();q.init_git();snapshot=json.loads((q.a/'SCOPE_AND_SNAPSHOT.json').read_bytes())
    reject('queue_duplicate_target',lambda:q.h.patch_queue(q.queue+snapshot['queue_row'].encode()+b'\n',DOI,snapshot['queue_row']))
    bad=q.queue.replace(b' queued ',b' claimed_solved ')
    reject('queue_remote_status_already_changed',lambda:q.h.patch_queue(bad,DOI,snapshot['queue_row']))
    bad=q.queue.replace(b'| 710 |',b'| 711 |')
    reject('queue_selected_identity_changed',lambda:q.h.patch_queue(bad,DOI,snapshot['queue_row']))
    # Exact source loader must ignore arbitrary existing cached bytecode.
    pyc=f.a/f'__pycache__/prepare_integration.{sys.implementation.cache_tag}.pyc';pyc.parent.mkdir()
    source=f.a/'prepare_integration.py';s=source.stat()
    stale=compile("raise RuntimeError('HOSTILE STALE PYC EXECUTED')",str(source),'exec')
    pyc.write_bytes(importlib._bootstrap_external._code_to_timestamp_pyc(stale,int(s.st_mtime),s.st_size))
    check('tracker_ignores_stale_pyc',lambda:load(f.a/'record_tracker.py','fresh_stale_pyc_tracker'))
    # Real kit check is read-only; stage and publish are never invoked.
    kit=load(LIVE.parents[2]/'zenodo_deposit_tool/zenodo.py','exact_zenodo_readonly_kit')
    result=kit.run(types.SimpleNamespace(command='check',manifest=f.a/'publication/zenodo-deposit.json',sandbox=False))
    check('exact_zenodo_kit_manifest_compatible',lambda:need(len(result['files'])==2 and result['environment']=='production','kit mismatch'))
    # Tracker cases use exact call()/append_once()/readback, with all gws intercepted.
    f=Fixture();dry=f.tracker_main(False)
    check('tracker_full_main_dry_preparation_never_appends',lambda:need(f.append_count==0 and dry['row'][1]=='' and not dry['applied'] and (f.a/'TRACKER_ROW_READY.json').is_file(),'tracker dry main failed'))
    f.final_gate('tracker');applied=f.tracker_main(True)
    check('tracker_full_main_apply_confirmed_receipt',lambda:need(f.append_count==1 and applied['applied'] and (f.a/'TRACKER_RECEIPT.json').is_file(),'tracker apply main failed'))
    f=Fixture();ready=f.ready();f.final_gate('tracker',ready['publication_validation'])
    receipt=f.tr.append_once(ready)
    check('tracker_exact_RAW_append_durable_intent_and_unique_readback',lambda:need(f.append_count==1 and receipt['read_back']==[ready['row']],'append failed'))
    f.tr.append_once(ready);check('tracker_second_call_readonly_reconciliation',lambda:need(f.append_count==1,'duplicate append'))
    f.values.append(ready['row']);reject('tracker_duplicate_global_DOI',lambda:f.tr.append_once(ready))
    f=Fixture();ready=f.ready();row=ready['row'].copy();row[3]='wrong';f.values.append(row)
    reject('tracker_existing_DOI_wrong_notes',lambda:f.tr.append_once(ready))
    for mode in ['lost','lost_no_write','bad_response','duplicate_after']:
        f=Fixture();ready=f.ready();f.final_gate('tracker',ready['publication_validation']);f.append_mode=mode
        reject('tracker_'+mode,lambda:f.tr.append_once(ready))
        need((f.a/'TRACKER_UNCONFIRMED.json').is_file(),'lost sticky intent')
        if mode in ['lost','bad_response']:
            f.tr.append_once(ready);need(f.append_count==1,'append retried after accepted write')
            RESULTS.append({'name':'tracker_'+mode+'_read_only_recovery','outcome':'PASS'})
        else:
            reject('tracker_'+mode+'_sticky_no_retry',lambda:f.tr.append_once(ready));need(f.append_count==1,'unexpected retry')
    for field in ['bad_headers','bad_gid']:
        f=Fixture();setattr(f,field,True);reject('tracker_'+field,f.tr.inspect)
    f=Fixture();ready=f.ready();f.final_gate('tracker',ready['publication_validation']);f.target_override=[['wrong']]
    reject('tracker_target_readback_mismatch',lambda:f.tr.append_once(ready));need(f.append_count==1,'readback case not dispatched')
    f=Fixture();ready=f.ready();f.final_gate('tracker',ready['publication_validation'],created_utc=(NOW-dt.timedelta(minutes=16)).isoformat())
    reject('tracker_stale_gate_no_dispatch',lambda:f.tr.append_once(ready));need(f.append_count==0,'expired gate dispatched')
    # Isolated full main, real replay/tree/commit object construction, mocked remote.
    f=Fixture();f.init_git();receipt=f.integration(False)
    check('integration_full_dry_run_no_shared_Git_change',lambda:need(f.git_snapshot()==f.git_initial and not f.push_count,'toy shared Git changed'))
    object_dir=receipt['object_directory'];env=dict(os.environ,GIT_OBJECT_DIRECTORY=object_dir,
                                                 GIT_ALTERNATE_OBJECT_DIRECTORIES=str(f.repo/'.git/objects'))
    sent=real_subprocess.check_output(['git','ls-tree',receipt['tree'],'--','sentinel','link'],cwd=f.repo,env=env)
    orig=real_subprocess.check_output(['git','ls-tree',f.base,'--','sentinel','link'],cwd=f.repo)
    check('integration_unrelated_executable_symlink_bytes_and_modes_preserved',lambda:need(sent==orig,'sentinel drift'))
    patch=receipt['queue_patch'];check('integration_exact_queue_three_cells_unrelated_bytes',lambda:need(patch['changed_cells']==['Status','Turns','Findings'] and patch['all_unselected_bytes_unchanged'],'queue drift'))
    prepared=json.loads((f.a/'INTEGRATION_PREPARED_RECEIPT.json').read_bytes())
    check('integration_publication_confirmed_time_distinct_from_preparation',lambda:need(
        prepared['publication_validation']['publication_confirmed_utc']!=prepared['integration_prepared_utc'], 'invented publication time'))
    f=Fixture();f.init_git();f.final_gate('integration');receipt=f.integration(True)
    check('integration_guarded_mock_push_durable_intent_and_readback',lambda:need(f.push_count==1 and receipt['pushed'] and f.git_snapshot()==f.git_initial,'push incorrect'))
    reject('integration_successful_dispatch_cannot_repeat',lambda:f.integration(True),'push was already dispatched')
    f=Fixture();f.init_git();f.final_gate('integration');f.push_mode='lost'
    reject('integration_ambiguous_push_sticky_intent',lambda:f.integration(True));need(f.push_count==1,'lost push no dispatch')
    reject('integration_ambiguous_push_cannot_repeat',lambda:f.integration(True),'push was already dispatched');need(f.push_count==1,'repeated ambiguous push')
    f=Fixture();f.init_git();f.live['headRefOid']='0'*40
    reject('integration_original_head_required_before_reading_payload',lambda:f.integration(False),'unreviewed PR head')
    f=Fixture();f.init_git();f.final_gate('integration',created_utc=(NOW-dt.timedelta(minutes=16)).isoformat())
    reject('integration_stale_gate_no_push',lambda:f.integration(True));need(f.push_count==0,'stale gate pushed')
    summary={'schema':'pr681-independent-operations-controls-v1','status':'PASS',
             'mode':'optimized' if sys.flags.optimize else 'normal','fake_fixtures_only':True,
             'real_network_cloud_github_tracker_writes':0,'controls':RESULTS,'count':len(RESULTS),
             'mock_dispatches':DISPATCHES,'fixture_root':str(T),
             'executed_helper_sha256':json.loads((LIVE/'WHOLE_PACKAGE_REVIEW_INPUTS.json').read_text())['helper_sha256']}
    print(json.dumps(summary,indent=2,sort_keys=True))


if __name__=='__main__':main()
