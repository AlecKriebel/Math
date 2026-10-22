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
        self.bindings = json.loads((LIVE / 'WHOLE_PACKAGE_REVIEW_INPUTS.normalization_repair.json').read_text())
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


NORM=[{'field':'description','kind':'plain_text_html_entities'}]
RECEIPTS=['ZENODO_PUBLICATION_RECEIPT.json','ZENODO_POST_PUBLICATION_INSPECTION.json']
def norm(f,value=NORM):
 for n in RECEIPTS:f.mutate_json(n,lambda x:x.update(metadata_normalizations=copy.deepcopy(value)))
def isolated_description(f,description):
 files,raw,accepted,review=f.h.accepted_inputs(f.a/'publication')
 d=json.loads(files['zenodo-deposit.json']);d['metadata']['description']=description
 files['zenodo-deposit.json']=jbytes(d);f.h.accepted_inputs=lambda p:(files,raw,accepted,review)
 f.h.archive_binding=lambda *a:({}, {'isolated_normalization_test_only':True})
 return f

def root_diagnostic(f,merge=False):
 p=f.a/'root_check_integration.py';shutil.copy2(LIVE/'root_check_integration.py',p)
 d=load(p,'fresh_exact_root_readonly_diagnostic')
 live=copy.deepcopy(f.live)
 if merge:
  r=json.loads((f.a/'INTEGRATION_PUSHED_RECEIPT.json').read_bytes());env=dict(os.environ,GIT_OBJECT_DIRECTORY=r['object_directory'],GIT_ALTERNATE_OBJECT_DIRECTORIES=str(f.repo/'.git/objects'))
  oid=real_subprocess.check_output(['git','commit-tree',r['tree'],'-p',f.base,'-p',r['integration_commit']],cwd=f.repo,env=env,input=b'FAKE root diagnostic merge fixture\n').decode().strip()
  live.update(state='MERGED',isDraft=False,mergedAt=NOW.isoformat(),mergeCommit={'oid':oid})
 def run(command,**kw):
  if command[0]=='gh':
   need(command[:4]==['gh','pr','view','681'],'diagnostic wrong PR')
   return types.SimpleNamespace(stdout=json.dumps(live),returncode=0)
  need(command[0]=='git'and Path(kw['cwd'])==f.repo,'diagnostic escaped fixture')
  need(command[1]in {'ls-tree','rev-parse','rev-list','show','diff','ls-remote','fetch'},'diagnostic nonread Git')
  if command[1]=='fetch':
   need('--no-write-fetch-head'in command and '--refmap='in command,'unsafe diagnostic fetch');return types.SimpleNamespace(stdout=b'',returncode=0)
  if command[1]=='ls-remote':return types.SimpleNamespace(stdout=(f.remote_head+'\trefs/heads/'+f.h.BRANCH+'\n').encode(),returncode=0)
  return real_subprocess.run(command,**kw)
 d.subprocess=types.SimpleNamespace(run=run);argv=sys.argv;sys.argv=['root_check_integration.py']+(['--merge']if merge else[])
 try:
  with contextlib.redirect_stdout(io.StringIO())as out:d.main()
 finally:sys.argv=argv
 return json.loads(out.getvalue())

def main():
 import html
 if T.exists():
  need(T.parent==R/'tmp'and T.name.startswith('operations-'),'unsafe scratch cleanup');shutil.rmtree(T)
 T.mkdir(parents=True,exist_ok=True)
 f=Fixture();baseline=f.inputs();description=json.loads(baseline['files']['zenodo-deposit.json'])['metadata']['description']
 check('full_gate_empty_normalization_positive',lambda:need(baseline['validation']['metadata_normalizations']==[] and baseline['validation']['remote_description_representation_sha256']==digest(description.encode()),'raw hash'))
 norm(f);v=f.inputs()['validation']
 check('full_gate_exact_entity_normalization_positive',lambda:need(v['metadata_normalizations']==NORM and v['remote_description_representation_sha256']==digest(html.escape(description,quote=False).encode()),'escaped hash'))
 norm(f,[{'kind':'plain_text_html_entities','field':'description'}]);check('normalization_object_key_order_positive',f.inputs)
 invalid=[None,False,{},'plain_text_html_entities',[{}],[{'field':'description'}],[{'kind':'plain_text_html_entities'}],[{'field':'title','kind':'plain_text_html_entities'}],[{'field':'Description','kind':'plain_text_html_entities'}],[{'field':'description','kind':'unknown'}],[{'field':'description','kind':'paragraph_apostrophes_u2019_to_ascii'}],[{'field':'creators','kind':'omitted_creator_affiliation_to_null'}],NORM+NORM,[dict(NORM[0],extra=True)],[[],*NORM],[*NORM,{}],[{},*NORM],[None],[True],['description']]
 for i,value in enumerate(invalid):norm(f,value);reject(f'normalization_invalid_type_field_kind_order_cardinality_{i:02d}',f.inputs)
 for i,values in enumerate([(NORM,[]),([],NORM)]):
  for n,value in zip(RECEIPTS,values):f.mutate_json(n,lambda x:x.update(metadata_normalizations=copy.deepcopy(value)))
  reject('two_receipt_normalization_mismatch_'+str(i),f.inputs)
 for i,desc in enumerate([description+' <p>text</p>',description+' <!-- comment -->',description+' <!DOCTYPE html>',description+' <?x?>',description+' &amp;',description+' &#62;',description+' &gt',description.replace('>','greater than')]):
  q=Fixture();norm(q);isolated_description(q,desc);reject('ineligible_HTML_entity_or_no_actual_change_'+str(i),q.inputs)
 for i,desc in enumerate([description+' 3 < 5',description+' & prose',description+" 'quoted' \"text\""]):
  q=Fixture();norm(q);isolated_description(q,desc);out=q.inputs()
  check('eligible_plain_text_exact_escape_'+str(i),lambda:need(out['validation']['remote_description_representation_sha256']==digest(html.escape(desc,quote=False).encode()),'alternate escaped hash'))
 q=Fixture();isolated_description(q,description.replace('>',' greater than '));check('no_change_empty_normalization_positive',q.inputs)
 f=Fixture();norm(f);v=f.inputs()['validation']
 for rel in v['source_bindings']:
  p=f.a/rel;old=p.read_bytes();p.write_bytes(old+b'\n');reject('captured_source_recheck_'+rel,lambda:f.h.recheck_sources(v));p.write_bytes(old)
 check('all_captured_sources_restored',lambda:f.h.recheck_sources(v))
 for name,path,mutation in [
  ('stale_review_hash','ACCEPTED_PUBLICATION_INPUTS.json',lambda x:x['whole_package_review_rounds'][0].update(report_sha256='0'*64)),
  ('duplicate_reviewer','ACCEPTED_PUBLICATION_INPUTS.json',lambda x:x['whole_package_review_rounds'][1].update(reviewer_id=x['whole_package_review_rounds'][0]['reviewer_id'])),
  ('missing_second_review','ACCEPTED_PUBLICATION_INPUTS.json',lambda x:x.update(whole_package_review_rounds=x['whole_package_review_rounds'][:1])),
  ('expanded_scope','PUBLICATION_FINAL_ACCEPTANCE.json',lambda x:x['claim_scope'].update(degree5_rank3_claim=True)),
  ('future_acceptance','ACCEPTED_PUBLICATION_INPUTS.json',lambda x:x.update(created_utc=(NOW+dt.timedelta(days=1)).isoformat())),
  ('wrong_title',RECEIPTS[0],lambda x:x.update(title='wrong')),('wrong_id',RECEIPTS[0],lambda x:x.update(id=999)),
  ('wrong_file_hash',RECEIPTS[0],lambda x:x['files'][0].update(sha256='0'*64)),
  ('wrong_resolver',RECEIPTS[0],lambda x:x['doi_resolution'].update(resolved_url='https://zenodo.org/records/1')),
  ('future_publication',RECEIPTS[0],lambda x:x.update(verified_utc=(NOW+dt.timedelta(days=1)).isoformat())),
  ('nonUTC_publication',RECEIPTS[0],lambda x:x.update(verified_utc='2026-10-14T23:00:00-07:00')),
  ('inspection_predates_publication',RECEIPTS[1],lambda x:x.update(verified_utc=(NOW-dt.timedelta(days=1)).isoformat()))]:
  old=(f.a/path).read_bytes();f.mutate_json(path,mutation);reject(name,f.inputs);(f.a/path).write_bytes(old)
 for name,mutation in [('expired',lambda x:x.update(created_utc=(NOW-dt.timedelta(minutes=16)).isoformat())),('future',lambda x:x.update(created_utc=(NOW+dt.timedelta(minutes=1)).isoformat())),('wrong_sheet',lambda x:x.update(sheet_id=42)),('extra_live_identity',lambda x:x['live_pr'].update(extra=True))]:
  f.final_gate('tracker',v);f.mutate_json('FINAL_TRACKER_GATE.json',mutation);reject('live_gate_'+name,lambda:f.h.validate_live_write_gate('tracker',DOI,v))
 for name,mutation in [('wrong_predecessor',lambda x:x.update(previous_report_sha256='0'*64)),('overlap',lambda x:x.update(started_utc=(NOW-dt.timedelta(days=1)).isoformat())),('waived',lambda x:x.update(findings_waived=True)),('human_review',lambda x:x.update(human_peer_review=True)),('wrong_helpers',lambda x:x['helper_sha256'].update(record_tracker='0'*64)),('wrong_target',lambda x:x.update(problem_id='other'))]:
  q=Fixture();q.repin_report(2,mutation);reject('review_'+name,q.inputs)
 for use_norm in [False,True]:
  f=Fixture()
  if use_norm:norm(f)
  dry=f.tracker_main(False);check('tracker_full_dry_'+str(use_norm),lambda:need(f.append_count==0 and not dry['applied'] and dry['row'][1]=='','dry tracker'))
  f.final_gate('tracker');done=f.tracker_main(True)
  check('tracker_full_apply_'+str(use_norm),lambda:need(f.append_count==1 and done['applied'] and done['publication_validation']['metadata_normalizations']==(NORM if use_norm else []),'tracker normalized path'))
  f.tracker_main(True);check('tracker_existing_no_duplicate_'+str(use_norm),lambda:need(f.append_count==1,'duplicate'))
 for mode in ['lost','lost_no_write','bad_response','duplicate_after']:
  f=Fixture();norm(f);ready=f.ready();f.final_gate('tracker',ready['publication_validation']);f.append_mode=mode
  reject('tracker_ambiguous_'+mode,lambda:f.tr.append_once(ready));need(f.append_count==1 and(f.a/'TRACKER_UNCONFIRMED.json').is_file(),'missing durable intent')
  if mode in ['lost','bad_response']:f.tr.append_once(ready);check('tracker_reconcile_'+mode,lambda:need(f.append_count==1,'repeated write'))
  else:reject('tracker_sticky_no_retry_'+mode,lambda:f.tr.append_once(ready));need(f.append_count==1,'blind retry')
 f=Fixture();norm(f);ready=f.ready();f.final_gate('tracker',ready['publication_validation'],created_utc=(NOW-dt.timedelta(minutes=16)).isoformat());reject('tracker_stale_gate_no_append',lambda:f.tr.append_once(ready));need(f.append_count==0,'stale append')
 f=Fixture();norm(f);f.init_git();dry=f.integration(False)
 check('integration_full_dry_normalized_current_helpers',lambda:need(not f.push_count and f.git_snapshot()==f.git_initial and dry['proposed_tree_replay']['accepted_archive']['selftest']['total_rejections']==60,'dry integration'))
 row=dry['queue_patch']['after_row'].encode().split(b'|');need(row[9].strip()==b'1/5','helper turns changed')
 old=(LIVE/'root_check_integration.py.before_turns_repair').read_bytes();current=(LIVE/'root_check_integration.py').read_bytes()
 check('F1_old_diagnostic_mismatch_reproduced',lambda:need(b"ac[9].strip()==b'5/5'"in old and row[9].strip()!=b'5/5','missing mismatch'))
 check('F1_exact_single_literal_repair',lambda:need(current==old.replace(b"ac[9].strip()==b'5/5'",b"ac[9].strip()==b'1/5'"),'nonminimal diagnostic repair'))
 f=Fixture();norm(f);f.init_git();f.final_gate('integration');pushed=f.integration(True)
 check('integration_mock_push_durable_intent_and_readback',lambda:need(f.push_count==1 and pushed['pushed']and f.git_snapshot()==f.git_initial and pushed['remote_branch_head_verified'],'guarded push'))
 out=root_diagnostic(f);check('F1_repaired_exact_root_diagnostic_full_fixture',lambda:need(out['status']=='PASS' and out['all_23_native_bytes_blobs_modes_exact']and out['accepted_target_queue_changed_cells']==['Status','Turns','Findings'],'root diagnostic'))
 out=root_diagnostic(f,True);check('repaired_exact_root_merge_readonly_diagnostic_full_fixture',lambda:need(out['status']=='PASS'and out['isolated_fetch_for_actual_merge_only']and out['whole_actual_tree_equals_accepted'],'merge diagnostic'))
 reject('successful_push_cannot_repeat',lambda:f.integration(True),'push was already dispatched')
 f=Fixture();norm(f);f.init_git();f.final_gate('integration');f.push_mode='lost';reject('ambiguous_push_sticky',lambda:f.integration(True));reject('ambiguous_push_no_repeat',lambda:f.integration(True),'push was already dispatched');need(f.push_count==1,'blind retry')
 f=Fixture();norm(f);f.init_git();f.final_gate('integration',created_utc=(NOW-dt.timedelta(minutes=16)).isoformat());reject('integration_stale_no_push',lambda:f.integration(True));need(f.push_count==0,'stale push')
 f=Fixture();f.init_git();f.live['headRefOid']='0'*40;reject('original_head_checked_first',lambda:f.integration(False),'unreviewed PR head')
 f=Fixture();p=f.a/f'__pycache__/prepare_integration.{sys.implementation.cache_tag}.pyc';p.parent.mkdir();src=f.a/'prepare_integration.py';st=src.stat()
 p.write_bytes(importlib._bootstrap_external._code_to_timestamp_pyc(compile("raise RuntimeError('HOSTILE STALE PYC')",str(src),'exec'),int(st.st_mtime),st.st_size))
 check('current_tracker_ignores_stale_pyc',lambda:load(f.a/'record_tracker.py','exact_current_stale_pyc_control'))
 print(json.dumps({'schema':'pr681-round3-current-operational-controls-v1','status':'PASS','mode':'optimized'if sys.flags.optimize else'normal','control_count':len(RESULTS),'controls':RESULTS,'mock_dispatches':DISPATCHES,'fake_fixtures_only':True,'real_network_cloud_tracker_GitHub_writes':0,'executed_helper_sha256':json.loads((LIVE/'WHOLE_PACKAGE_REVIEW_INPUTS.normalization_repair.json').read_text())['helper_sha256'],'root_diagnostic_sha256':digest((LIVE/'root_check_integration.py').read_bytes()),'resolved_finding_F1':'historical 5/5 mismatch corrected to reviewed original 1/5; exact diagnostic tested'},indent=2,sort_keys=True))

if __name__=='__main__':main()
