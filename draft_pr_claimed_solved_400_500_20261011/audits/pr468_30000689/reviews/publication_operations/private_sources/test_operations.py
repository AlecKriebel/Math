#!/usr/bin/env python3
"""Offline adversarial operation harness. No real clients, tokens, subprocesses.

Every mutated fixture is private to this review. Candidate source is executed
from its frozen copy with mock boundaries installed before main is invoked.
"""
import base64
import contextlib
import copy
import datetime
import hashlib
import io
import json
import re
import shutil
import sys
import threading
import types
from pathlib import Path
from unittest.mock import patch

OUT = Path(__file__).resolve().parent.parent
REAL_AUDIT = OUT / 'private_sources/frozen_context'
FIXTURES = OUT / 'private_sources/fixtures'
RESULTS = []
ORIGINAL = '8527ccdba064bca52035fc6c8d96caa750ac9c00'
PREFIX = 'unsolved_math_prioritization/attempts/30000689/'
QUEUE = 'unsolved_math_prioritization/QUEUE.md'
PDF = 'missing_faces_and_sphere_skeleta.pdf'
ZIP = 'missing_faces_verification_v1.zip'
DOI = 'https://doi.org/10.5281/zenodo.23310484'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def put(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + '\n')


def load(name):
    path = OUT / 'private_sources' / name
    m = types.ModuleType(name.removesuffix('.py'))
    m.__file__ = str(path)
    exec(compile(path.read_text(), str(path), 'exec'), m.__dict__)
    return m


def fixture(name):
    base = FIXTURES / name
    if base.exists():
        shutil.rmtree(base)
    audit = base / 'repo/program/audits/pr468_30000689'
    audit.mkdir(parents=True)
    shutil.copytree(REAL_AUDIT / 'package', audit / 'package')
    for f in ['PACKAGE_REVIEW_INPUT_4.json', 'PACKAGE_REVIEW_INPUT_3.json',
              'ZENODO_DRAFT_METADATA_RECONCILIATION.json', 'SOURCE_RECEIPT.json', 'BRANCH_INSTALL_PLAN.json']:
        shutil.copy2(REAL_AUDIT / f, audit / f)
    backup = audit / 'references/private_sources/round3_accepted' / ZIP
    backup.parent.mkdir(parents=True)
    shutil.copy2(REAL_AUDIT / 'references/private_sources/round3_accepted' / ZIP, backup)
    reports = []
    for i in [1, 2]:
        r = f'reviews/mock_review_{i}.md'
        data = f'PRIVATE SYNTHETIC FIXTURE: Independent mock complete-package review {i}; PASS.\n'.encode()
        (audit / 'reviews').mkdir(exist_ok=True)
        (audit / r).write_bytes(data)
        reports.append({'path': r, 'sha256': sha(data), 'verdict': 'PASS',
                        'blocking_issue_count': 0, 'required_correction_count': 0})
    put(audit / 'FINAL_ACCEPTANCE_GATE.json', {'verdict': 'ACCEPTED_FOR_PREPRINT_PUBLICATION',
        'pr': 468, 'review_input_manifest': 'PACKAGE_REVIEW_INPUT_4.json', 'complete_package_reviews': reports})
    meta = json.loads((audit / 'package/metadata.json').read_text())
    freeze = json.loads((audit / 'PACKAGE_REVIEW_INPUT_4.json').read_text())
    published = {'state': 'published', 'environment': 'production', 'id': 23310484,
                 'title': meta['title'], 'doi': DOI.removeprefix('https://doi.org/'),
                 'doi_url': DOI, 'record_url': 'https://zenodo.org/records/23310484',
                 'files': [{'name': PDF, 'sha256': freeze['files']['manuscript.pdf']['sha256']},
                           {'name': ZIP, 'sha256': freeze['files'][ZIP]['sha256']}]}
    put(audit / 'ZENODO_PUBLISH_RECEIPT.json', published)
    put(audit / 'TRACKER_APPEND_RECEIPT.json', {'verified': True, 'values': [['mock problem', '', DOI, meta['title']]]})
    plan = json.loads((audit / 'BRANCH_INSTALL_PLAN.json').read_text())
    for e in plan['entries']:
        relative = Path(e['local_program_path']).relative_to('draft_pr_claimed_solved_400_500_20261011')
        e['local_program_path'] = str(Path('program') / relative)
    put(audit / 'BRANCH_INSTALL_PLAN.json', plan)
    return audit


def call(m, apply=True):
    buf = io.StringIO()
    with patch.object(sys, 'argv', ['mock-helper'] + (['--apply'] if apply else [])), contextlib.redirect_stdout(buf):
        try:
            m.main()
            return {'ok': True, 'output': json.loads(buf.getvalue()) if buf.getvalue().strip() else None}
        except Exception as e:
            return {'ok': False, 'exception': type(e).__name__, 'error': str(e)}


def record(name, outcome, assertions, detail=None):
    failed = [k for k, v in assertions.items() if not v]
    RESULTS.append({'case': name, 'outcome': outcome, 'checks': assertions,
                    'all_checks_pass': not failed, 'details': detail})
    if failed:
        raise AssertionError(name + ': ' + ', '.join(failed))


class DepositError(Exception):
    pass


class ArchiveMock:
    def __init__(self, audit, behavior='204', submitted=False):
        self.audit, self.behavior = audit, behavior
        self.calls = []
        manifest = json.loads((audit / 'package/deposit.json').read_text())
        self.metadata = manifest['metadata']
        self.local = []
        for x in manifest['files']:
            path = audit / 'package' / x['path']; data = path.read_bytes()
            self.local.append({'path': path, 'name': x.get('name', path.name), 'size': len(data),
                               'md5': hashlib.md5(data).hexdigest(), 'sha256': sha(data)})
        old = (audit / 'references/private_sources/round3_accepted' / ZIP).read_bytes()
        pdf = next(x for x in self.local if x['name'] == PDF)
        self.deposit = {'id': 23310484, 'submitted': submitted, 'metadata': copy.deepcopy(self.metadata),
            'files': [{'filename': PDF, 'id': 'pdf-preserve', 'filesize': pdf['size'], 'checksum': pdf['md5']},
                      {'filename': ZIP, 'id': '097f2463-43fd-42df-97b0-8cca5b9f51eb',
                       'filesize': len(old), 'checksum': hashlib.md5(old).hexdigest()}]}
        self.base = 'https://mock.invalid'
        self.kit = types.SimpleNamespace(DepositError=DepositError, load_manifest=lambda p: (self.metadata, self.local),
            local_state=lambda p,e: (None, {'id': 23310484}), token_for=lambda e: 'MOCK_TOKEN_NEVER_TRANSMITTED',
            ZenodoClient=lambda e,t: self, validate_record=self.validate, server_files=self.server_files,
            matching_file=self.matching, verify=self.verify)

    def validate(self, d, expected):
        if d['id'] != expected or type(d['submitted']) is not bool:
            raise DepositError('record invalid')

    def server_files(self, d):
        return {x['filename']: x for x in d['files']}

    def matching(self, r, l):
        return str(r.get('checksum', '')).lower().removeprefix('md5:') == l['md5'] and str(r['filesize']) == str(l['size'])

    def verify(self, d, metadata, files):
        assert d['metadata'] == metadata
        remote = self.server_files(d)
        assert set(remote) == {x['name'] for x in files}
        assert all(self.matching(remote[x['name']], x) for x in files)

    def get(self, id):
        self.calls.append(('GET', id))
        if self.behavior == 'delete_then_get_lost' and any(x[0] == 'DELETE' for x in self.calls):
            self.behavior = 'normal'
            raise DepositError('mock readback lost')
        return copy.deepcopy(self.deposit)

    def request(self, method, url):
        self.calls.append((method, url))
        assert method == 'DELETE' and url.endswith('/23310484/files/097f2463-43fd-42df-97b0-8cca5b9f51eb')
        if self.behavior != 'not_reached':
            self.deposit['files'] = [x for x in self.deposit['files'] if x['filename'] != ZIP]
        if self.behavior in {'204', 'delete_then_get_lost', 'not_reached'}:
            raise DepositError('Unexpected or incomplete Zenodo JSON response; operation outcome is unconfirmed' if self.behavior == '204' else 'mock connection lost')
        return {'ok': True}

    def install(self, m):
        m.AUDIT = self.audit; m.MANIFEST = self.audit / 'package/deposit.json'
        m.importlib = types.SimpleNamespace(util=types.SimpleNamespace(
            spec_from_file_location=lambda *args: types.SimpleNamespace(loader=types.SimpleNamespace(exec_module=lambda x: None)),
            module_from_spec=lambda s: self.kit))
        queue = make_queue(claimed=True)
        def check_output(cmd):
            self.calls.append(('mock_gh', cmd[1]))
            return json.dumps({'state': 'OPEN', 'isDraft': True, 'headRefOid': ORIGINAL}).encode() if cmd[1]=='pr' else queue
        m.subprocess = types.SimpleNamespace(check_output=check_output)


def make_queue(claimed=True, other='KEEP UNRELATED ROW EXACTLY', status=None):
    header='| Rank | ID / code | Problem | EV | Impact (/10) | Difficulty | Proposed | Status | Turns | Chat | Findings | DOI |\n'
    selected=json.loads((REAL_AUDIT / 'SOURCE_RECEIPT.json').read_text())['selected_queue_row']
    if not claimed:
        selected=selected.replace('| claimed_solved |', '| queued |')
    if status:
        selected=selected.replace('| claimed_solved |', '| '+status+' |').replace('| queued |','| '+status+' |')
    return ('# Private queue mock\n'+header+'|---|---|---|---|---|---|---|---|---|---|---|---|\n'+selected+'\n'+
        '| 499 | 39999999 / MOCK | '+other+' | 0 | 1 | 1 | 2000 | queued | 0/5 | | unaffected | |\n').encode()


def archive_cases():
    for name, behavior in [('archive_delete204', '204'), ('archive_lost_response', 'normal')]:
        a=fixture(name); m=load('replace_pr468_draft_archive.py'); f=ArchiveMock(a, behavior); f.install(m)
        if name=='archive_lost_response':
            # Simulate a successful deletion with a lost network response.
            old_request=f.request
            def lost(method,url):
                old_request(method,url); raise DepositError('mock DELETE response lost')
            f.request=lost
        r=call(m); receipt=json.loads((a/'ZENODO_ARCHIVE_REPLACE_RECEIPT.json').read_text())
        record(name,r, {'succeeds':r['ok'], 'one_delete':sum(x[0]=='DELETE' for x in f.calls)==1,
              'pdf_preserved': [x['filename'] for x in f.deposit['files']]==[PDF],
              'receipt_verified': receipt['state']=='superseded_zip_absent_verified'})
    a=fixture('archive_resume_get_lost');m=load('replace_pr468_draft_archive.py');f=ArchiveMock(a,'delete_then_get_lost');f.install(m)
    first=call(m);second=call(m)
    record('archive_resume_get_lost',{'first':first,'second':second}, {'first_fails':not first['ok'],'resume_succeeds':second['ok'],'no_repeat_delete':sum(x[0]=='DELETE' for x in f.calls)==1})
    a=fixture('archive_request_not_reached');m=load('replace_pr468_draft_archive.py');f=ArchiveMock(a,'not_reached');f.install(m)
    first=call(m);second=call(m)
    record('archive_request_not_reached',{'first':first,'second':second},{'both_fail_closed':not first['ok'] and not second['ok'],'one_attempt_only':sum(x[0]=='DELETE' for x in f.calls)==1})
    for name, mutate in [
       ('archive_hold_gate',lambda a,f: shutil.copy2(REAL_AUDIT/'FINAL_ACCEPTANCE_GATE.json',a/'FINAL_ACCEPTANCE_GATE.json')),
       ('archive_hash_drift',lambda a,f: (a/'package/metadata.json').write_text('PRIVATE MUTATION')),
       ('archive_published_record',lambda a,f: f.deposit.update(submitted=True)),
       ('archive_unknown_zip',lambda a,f: f.deposit['files'][1].update(checksum='0'*32)),
       ('archive_changed_pdf',lambda a,f: f.deposit['files'][0].update(checksum='0'*32)),
       ('archive_wrong_draft_id',lambda a,f: setattr(f.kit,'local_state',lambda p,e:(None,{'id':23310485}))),
       ('archive_unsafe_file_id',lambda a,f: f.deposit['files'][1].update(id='../../other-file')),
       ('archive_extra_remote_file',lambda a,f: f.deposit['files'].append({'filename':'unrelated-file.pdf'})),
       ('archive_metadata_drift',lambda a,f: f.deposit['metadata'].update(title='PRIVATE WRONG TITLE')),
       ('archive_nonclaimed_source',lambda a,f: setattr(f,'nonclaimed',True)),
    ]:
        a=fixture(name);m=load('replace_pr468_draft_archive.py');f=ArchiveMock(a);f.install(m);mutate(a,f)
        if name=='archive_nonclaimed_source':
            prior=m.subprocess.check_output
            m.subprocess.check_output=lambda cmd: make_queue(False) if cmd[1]=='api' else prior(cmd)
        r=call(m)
        record(name,r,{'rejected':not r['ok'],'no_delete':not any(x[0]=='DELETE' for x in f.calls)})
    a=fixture('archive_already_replaced');m=load('replace_pr468_draft_archive.py');f=ArchiveMock(a);f.install(m)
    accepted=next(x for x in f.local if x['name']==ZIP);f.deposit['files'][1].update(filesize=accepted['size'],checksum=accepted['md5'])
    r=call(m)
    record('archive_already_replaced',r,{'succeeds':r['ok'],'no_delete':not any(x[0]=='DELETE' for x in f.calls),'idempotent_state':r.get('output',{}).get('state')=='accepted_archive_already_present'})
    a=fixture('archive_required_review_issue');m=load('replace_pr468_draft_archive.py');f=ArchiveMock(a);f.install(m)
    gate=json.loads((a/'FINAL_ACCEPTANCE_GATE.json').read_text());gate['complete_package_reviews'][1]['required_correction_count']=1;put(a/'FINAL_ACCEPTANCE_GATE.json',gate)
    r=call(m);record('archive_required_review_issue',r,{'rejects_required_issue':not r['ok'],'no_delete':not any(x[0]=='DELETE' for x in f.calls)})
    for name,mutate in [
      ('archive_stale_round3_gate',lambda g:g.update(review_input_manifest='PACKAGE_REVIEW_INPUT_3.json')),
      ('archive_report_hash_drift',lambda g:g['complete_package_reviews'][0].update(sha256='0'*64)),
    ]:
        a=fixture(name);m=load('replace_pr468_draft_archive.py');f=ArchiveMock(a);f.install(m)
        gate=json.loads((a/'FINAL_ACCEPTANCE_GATE.json').read_text());mutate(gate);put(a/'FINAL_ACCEPTANCE_GATE.json',gate)
        r=call(m);record(name,r,{'rejects':not r['ok'],'no_delete':not any(x[0]=='DELETE' for x in f.calls)})


class TrackerMock:
    def __init__(self,behavior='normal'):
        self.rows=[['Original Problem','Solution Chat URL','DOI','Notes']]
        self.behavior=behavior;self.calls=[];self.expected=None
    def cli(self,action,params,body=None):
        self.calls.append((action,params.get('range')))
        if action=='get':
            ran=params['range']
            if ran.endswith('A1:D1'):return {'values':[self.rows[0]]}
            if ran.endswith('A:D'):return {'values':copy.deepcopy(self.rows)}
            row=int(re.search(r'A(\d+):',ran).group(1));return {'values':[copy.deepcopy(self.rows[row-1])]}
        assert action=='append';self.expected=copy.deepcopy(body['values'][0])
        if self.behavior=='not_reached':raise RuntimeError('mock response lost before append')
        if self.behavior=='same_doi_race':self.rows.append(copy.deepcopy(self.expected))
        self.rows.append(copy.deepcopy(self.expected));row=len(self.rows)
        if self.behavior=='lost':raise RuntimeError('mock successful append response lost')
        return {'updates':{'updatedRows':1,'updatedColumns':4,'updatedRange':f"'Math Puzzles'!A{row}:D{row}"}}
    def install(self,m,a):m.ROOT=a;m.cli=self.cli


def tracker_cases():
    for name,behavior in [('tracker_normal','normal'),('tracker_lost_response','lost'),('tracker_not_reached','not_reached')]:
        a=fixture(name);m=load('register_pr468_tracker.py');f=TrackerMock(behavior);f.install(m,a)
        first=call(m);second=call(m)
        expected_ok=behavior!='not_reached'
        canonical=json.loads((a/'package/metadata.json').read_text())
        fields_ok=(not expected_ok or (f.expected[1]=='' and f.expected[2]==DOI
            and '30000689 / OWR-1455-008' in f.expected[0]
            and 'https://ems.press/content/serial-article-files/46090 (p.238, Conjecture4)' in f.expected[0]
            and canonical['title'] in f.expected[3] and 'Alec Kriebel' in f.expected[3]
            and 'version1.0, 12October2026' in f.expected[3]
            and 'https://github.com/AlecKriebel/Math/pull/468' in f.expected[3]
            and 'Extensive AI use; unrefereed' in f.expected[3]
            and 'no independent human peer review or first-priority claim' in f.expected[3]))
        record(name,{'first':first,'second':second},{'expected_outcome':first['ok']==expected_ok and second['ok']==expected_ok,
              'one_append_only':sum(x[0]=='append' for x in f.calls)==1,
              'doi_count':len(m.matches(DOI,f.rows))==(1 if expected_ok else 0),'canonical_registration_fields':fields_ok},
              {'row_fields':f.expected if expected_ok else None})
    a=fixture('tracker_existing_mismatch');m=load('register_pr468_tracker.py');f=TrackerMock();f.rows.append(['wrong','','10.5281/zenodo.23310484','different']);f.install(m,a)
    r=call(m);record('tracker_existing_mismatch',r,{'rejects_different_fields':not r['ok'],'does_not_append':not any(x[0]=='append' for x in f.calls)})
    a=fixture('tracker_unpublished');m=load('register_pr468_tracker.py');f=TrackerMock();f.install(m,a)
    p=json.loads((a/'ZENODO_PUBLISH_RECEIPT.json').read_text());p['state']='ready_to_publish';put(a/'ZENODO_PUBLISH_RECEIPT.json',p)
    r=call(m);record('tracker_unpublished',r,{'rejects_unpublished':not r['ok'],'no_cloud_call':not f.calls})
    a=fixture('tracker_title_drift');m=load('register_pr468_tracker.py');f=TrackerMock();f.install(m,a)
    p=json.loads((a/'ZENODO_PUBLISH_RECEIPT.json').read_text());p['title']='PRIVATE WRONG TITLE';put(a/'ZENODO_PUBLISH_RECEIPT.json',p)
    r=call(m);record('tracker_title_drift',r,{'rejects_title_drift':not r['ok'],'no_cloud_call':not f.calls})
    a=fixture('tracker_duplicate_existing');m=load('register_pr468_tracker.py');f=TrackerMock();f.install(m,a)
    f.rows.extend([['mock','',DOI,'mock'],['mock','','10.5281/zenodo.23310484','mock']])
    r=call(m);record('tracker_duplicate_existing',r,{'rejects_existing_duplicates':not r['ok'],'does_not_append':not any(x[0]=='append' for x in f.calls)})
    a=fixture('tracker_concurrent_same_doi');m=load('register_pr468_tracker.py');f=TrackerMock('same_doi_race');f.install(m,a)
    r=call(m);record('tracker_concurrent_same_doi',r,{'witness_returns_success':r['ok'],'witness_duplicate_count_two':len(m.matches(DOI,f.rows))==2},
       {'mechanism':'another runner appends same canonical DOI between duplicate read and this append; returned-row readback alone misses duplicate'})


class GitMock:
    def __init__(self,a,behavior='normal'):
        self.audit=a;self.behavior=behavior;self.calls=[];self.lock=threading.Lock();self.branch='existing-pr468'
        self.refs={'main':'main-latest',self.branch:ORIGINAL};self.parents={ORIGINAL:[],'main-latest':[],'racing-head':[ORIGINAL]}
        receipt=json.loads((a/'SOURCE_RECEIPT.json').read_text())
        source={e['path']:(REAL_AUDIT/'source_snapshot'/e['path']).read_bytes() for e in receipt['files']}
        source[QUEUE]=make_queue()
        self.trees={'original-tree':source,'main-tree':{QUEUE:make_queue(False,other='LATEST MAIN UNRELATED ROW'),
                     'unrelated/current-main.txt':b'latest unrelated main bytes\n'}}
        self.commit_trees={ORIGINAL:'original-tree','main-latest':'main-tree'};self.blobs={}
        self.original_files=[{'filename':p} for p in source]
    def api(self,endpoint,payload=None,method=None,raw=False):
        with self.lock:self.calls.append((endpoint,method,payload))
        if endpoint=='pulls/468':return {'state':'open','draft':True,'head':{'sha':self.refs[self.branch],'ref':self.branch,'repo':{'full_name':'AlecKriebel/Math'}}}
        if endpoint.startswith('pulls/468/files'):return self.original_files
        if endpoint.startswith('contents/'):
            path,head=endpoint.removeprefix('contents/').rsplit('?ref=',1)
            return self.trees[self.commit_trees[head]][path]
        if endpoint.startswith('git/ref/heads/'):return {'object':{'sha':self.refs[endpoint.removeprefix('git/ref/heads/')]}}
        if endpoint.startswith('git/commits/'):
            head=endpoint.removeprefix('git/commits/');return {'tree':{'sha':self.commit_trees[head]}}
        if endpoint=='git/blobs':
            data=base64.b64decode(payload['content']);blob=sha(data)
            with self.lock:self.blobs[blob]=data
            return {'sha':blob}
        if endpoint=='git/trees':
            tree=copy.deepcopy(self.trees[payload['base_tree']]);tree.update({x['path']:self.blobs[x['sha']] for x in payload['tree']});self.trees['installed-tree']=tree;return {'sha':'installed-tree'}
        if endpoint=='git/commits':
            self.parents['installed-commit']=payload['parents'];self.commit_trees['installed-commit']=payload['tree'];return {'sha':'installed-commit'}
        if endpoint.startswith('compare/'):
            pair=endpoint.removeprefix('compare/');old,new=pair.split('...');a=self.trees[self.commit_trees[old]];b=self.trees[self.commit_trees[new]]
            return {'files':[{'filename':p} for p in sorted(set(a)|set(b)) if a.get(p)!=b.get(p)]}
        if endpoint.startswith('git/refs/heads/'):
            assert method=='PATCH' and payload['force'] is False
            if self.behavior=='race':self.refs[self.branch]='racing-head'
            target=payload['sha'];current=self.refs[self.branch]
            if current not in self.parents[target]:raise RuntimeError('mock non-fast-forward rejected')
            self.refs[self.branch]=target
            if self.behavior=='lost':raise RuntimeError('mock successful ref update response lost')
            return {'object':{'sha':target}}
        raise AssertionError('Unmocked endpoint '+endpoint)
    def install(self,m):m.AUDIT=self.audit;m.REPOSITORY=self.audit.parents[2];m.api=self.api


def integration_cases():
    for name,behavior in [('integration_normal','normal'),('integration_ref_response_lost','lost'),('integration_head_race','race')]:
        a=fixture(name);m=load('integrate_pr468_publication.py');f=GitMock(a,behavior);f.install(m);r=call(m)
        tree=f.trees['installed-tree'];base=f.trees['main-tree'];installed_queue=tree[QUEUE];lines_before=base[QUEUE].splitlines();lines_after=installed_queue.splitlines()
        checks={'expected_result':r['ok']==(behavior!='race'),'unrelated_main_file_preserved':tree['unrelated/current-main.txt']==base['unrelated/current-main.txt'],
          'one_queue_line_changed':sum(x!=y for x,y in zip(lines_before,lines_after))==1 and len(lines_before)==len(lines_after),
          'latest_other_row_preserved':lines_before[-1]==lines_after[-1],'two_parents':[ORIGINAL,'main-latest']==f.parents['installed-commit'],
          'one_nonforce_update':sum(x[0].startswith('git/refs/heads/') and x[2]['force'] is False for x in f.calls)==1,
          'race_preserves_changed_ref':f.refs[f.branch]==('racing-head' if behavior=='race' else 'installed-commit')}
        record(name,r,checks,{'remote_tree_changed_paths':len([p for p in tree if tree.get(p)!=base.get(p)])})
    for name,mutation in [
      ('integration_hold_gate',lambda a,f: shutil.copy2(REAL_AUDIT/'FINAL_ACCEPTANCE_GATE.json',a/'FINAL_ACCEPTANCE_GATE.json')),
      ('integration_nonclaimed_source',lambda a,f: f.trees['original-tree'].update({QUEUE:make_queue(False)})),
      ('integration_hash_drift',lambda a,f:(a/'package/manuscript.tex').write_text('PRIVATE MUTATION')),
      ('integration_unrelated_original_scope',lambda a,f:f.original_files.append({'filename':'unrelated/author-change.txt'})),
      ('integration_source_hash_drift',lambda a,f:f.trees['original-tree'].update({PREFIX+'EXPLANATORY_ADDENDUM.md':b'PRIVATE MUTATION'})),
      ('integration_main_disposition_changed',lambda a,f:f.trees['main-tree'].update({QUEUE:make_queue(status='refuted')})),
    ]:
        a=fixture(name);m=load('integrate_pr468_publication.py');f=GitMock(a);f.install(m);mutation(a,f);r=call(m)
        record(name,r,{'rejects':not r['ok'],'no_remote_mutation':not any(x[2] is not None for x in f.calls)})
    for name,mutate in [
      ('integration_published_file_hash_drift',lambda p:p['files'][0].update(sha256='0'*64)),
      ('integration_published_title_drift',lambda p:p.update(title='PRIVATE WRONG TITLE')),
    ]:
        a=fixture(name);m=load('integrate_pr468_publication.py');f=GitMock(a);f.install(m)
        pub=json.loads((a/'ZENODO_PUBLISH_RECEIPT.json').read_text());mutate(pub);put(a/'ZENODO_PUBLISH_RECEIPT.json',pub)
        r=call(m);record(name,r,{'rejects':not r['ok'],'no_remote_mutation':not any(x[2] is not None for x in f.calls)})
    for name,mutate in [
      ('integration_stale_round3_freeze',lambda g:g.update(review_input_manifest='PACKAGE_REVIEW_INPUT_3.json')),
      ('integration_report_hash_drift',lambda g:g['complete_package_reviews'][0].update(sha256='0'*64)),
    ]:
        a=fixture(name);m=load('integrate_pr468_publication.py');f=GitMock(a);f.install(m)
        gate=json.loads((a/'FINAL_ACCEPTANCE_GATE.json').read_text());mutate(gate);put(a/'FINAL_ACCEPTANCE_GATE.json',gate)
        r=call(m);record(name,r,{'rejects':not r['ok'],'no_remote_mutation':not any(x[2] is not None for x in f.calls)})
    a=fixture('integration_required_review_issue');m=load('integrate_pr468_publication.py');f=GitMock(a);f.install(m)
    gate=json.loads((a/'FINAL_ACCEPTANCE_GATE.json').read_text());gate['complete_package_reviews'][1]['required_correction_count']=1;put(a/'FINAL_ACCEPTANCE_GATE.json',gate)
    r=call(m);record('integration_required_review_issue',r,{'witness_proceeds_with_required_issue':r['ok'],'witness_branch_updated':f.refs[f.branch]=='installed-commit'})


def main():
    sys.dont_write_bytecode=True
    archive_cases();tracker_cases();integration_cases()
    put(OUT/'MOCK_TEST_RESULTS.json',{'generated_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'service_boundary':'Entirely in memory; never contacts remote service, invokes subprocess, loads credentials/state, or touches shared Git index.',
        'case_count':len(RESULTS),'results':RESULTS})
    print(json.dumps({'case_count':len(RESULTS),'all_harness_assertions_pass':all(x['all_checks_pass'] for x in RESULTS),
        'witness_cases':[x['case'] for x in RESULTS if 'witness_' in ' '.join(x['checks'])]},indent=2))


if __name__=='__main__':main()
