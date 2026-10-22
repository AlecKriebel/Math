"""Execute byte-identical helpers only in disposable fixtures with all effects mocked.

No actual provider, network, subprocess, Git, index, ref, Queue or SQL operations.
The temporary fixtures live under this audit directory and are removed on exit.
"""
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import patch
from contextlib import redirect_stdout
import base64, copy, gc, hashlib, importlib.util, io, json, os, runpy
import shutil, socket, subprocess, sys, tempfile, urllib.request, zipfile

OUT = Path(__file__).resolve().parent
D = OUT.parent
CASE = D.parent
SOURCE_PUB = CASE / 'publication'
SOURCE_R = CASE / 'preprint'
ROOT = Path('/Users/alec/Documents/Math')
OLD = '2180d64b648b81ac660a792f7823d0b715f9cf12'
TITLE = 'The outer focal-pedal area product in odd elliptic billiards'
PREFIX = 'unsolved_math_prioritization/attempts/5100033/'
QPATH = 'unsolved_math_prioritization/QUEUE.md'
FAMILIES = ['source_domain_adversary_01', 'physical_geometry_adversary_01',
    'meromorphic_divisor_adversary_01', 'priority_author_updates_01',
    'priority_classical_general_01', 'whole_manuscript_adversary_01',
    'whole_manuscript_adversary_02', 'whole_manuscript_adversary_03',
    'release_helpers_adversary_01', 'release_helpers_adversary_02']
RESULTS = []
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
blob_sha = lambda raw: hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
save = lambda p, v: p.write_text(json.dumps(v, indent=2) + '\n')

spec = importlib.util.spec_from_file_location('release_binding', SOURCE_PUB / 'release_binding.py')
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)
sys.modules['release_binding'] = g


def forbidden(*args, **kwargs):
    raise AssertionError('Unmocked external effect attempted')


class Fixture:
    def __init__(self, base):
        self.base = base
        self.R = base / 'preprint'
        self.P = base / 'publication'
        self.D = base / 'initial_review_20261015'
        for p in [self.R, self.P, self.D]: p.mkdir(parents=True)
        for p in SOURCE_PUB.glob('*.py'): shutil.copyfile(p, self.P / p.name)
        for name in ['manuscript.pdf', 'k605a-source-verification.zip', 'metadata.json',
                     'deposit.json', 'PACKAGE_MANIFEST.json', 'SOURCE_MANIFEST.json', 'manuscript.tex']:
            shutil.copyfile(SOURCE_R / name, self.R / name)
        shutil.copytree(SOURCE_R / 'pr_update', self.R / 'pr_update')
        shutil.copyfile(D / 'INTAKE.json', self.D / 'INTAKE.json')
        for family in FAMILIES:
            folder = self.D / family; folder.mkdir()
            (folder / 'SYNTHETIC_REPORT.txt').write_text('Synthetic family seal for control-flow test only.\n')
            p = folder / 'SYNTHETIC_REPORT.txt'
            save(folder / 'AUTHORED_MANIFEST.json', {'synthetic_fixture_only': True, 'files': [
                dict(path=p.name, bytes=p.stat().st_size, sha256=sha(p))]})
        package = json.loads((self.R / 'PACKAGE_MANIFEST.json').read_text())
        metadata = json.loads((self.R / 'metadata.json').read_text())
        self.clear = dict(synthetic_fixture_only=True, release_cleared=True,
            fresh_manuscript_reviews=3, final_frozen_clean_reviews=1,
            unresolved_mandatory_findings=[], unresolved_optional_findings=[],
            original_native_head=OLD, package_manifest_sha256=sha(self.R / 'PACKAGE_MANIFEST.json'),
            deposit_manifest_sha256=sha(self.R / 'deposit.json'),
            publication_metadata_sha256=sha(self.R / 'metadata.json'),
            release_helpers=[dict(path=p.name, bytes=p.stat().st_size, sha256=sha(p))
                            for p in sorted(self.P.glob('*.py'))],
            submission_files=package['submission_files'], source_manifest=package['source_manifest'],
            manuscript_source=package['manuscript_source'], publication_metadata=metadata)
        save(self.R / 'FINAL_CLEARANCE.json', self.clear)
        self.ctx = g.context(self.R)
        self.calls = []; self.downloads = []
        self.ready_count = self.merge_count = self.append_count = self.stage_count = self.publish_count = 0
        self.fail_stage = self.fail_merge = self.fail_download = self.doi_pending = False
        self.before_native_compare = None
        self.compare_override = None
        self.pr = dict(number=210, state='open', draft=True, merged=False, mergeable=True,
            node_id='SYNTHETIC_PR_NODE', html_url='https://github.com/AlecKriebel/Math/pull/210',
            head=dict(sha=OLD, ref='dot/math-5100033', repo=dict(full_name='AlecKriebel/Math')),
            base=dict(ref='main', repo=dict(full_name='AlecKriebel/Math')))
        self.qraw = ('| 5100033 / AMR-050-0033 | source | p | a | b | c | 2020 | claimed_solved | 1/5 | x | old link | old doi |\n'
                     '| other problem | unchanged |\n').encode()
        self.intake = json.loads((self.D / 'INTAKE.json').read_text())
        self.trees = {}; self.blobs = {}
        self.main = 'a' * 40
        self.commits = {self.main: dict(tree=dict(sha=self.make_tree({QPATH: self.qraw})), parents=[])}
        self.native_files = {}; self.sheet = [['Original Problem', 'Solution Chat URL', 'DOI', 'Notes']]
        self.supplementary = []

    def make_tree(self, files):
        directory = {}
        for path, raw in files.items():
            cur = directory; parts = path.split('/')
            for part in parts[:-1]: cur = cur.setdefault(part, {})
            cur[parts[-1]] = raw
        def build(node):
            rows = []
            for name, value in sorted(node.items()):
                if isinstance(value, dict): item = dict(path=name, mode='040000', type='tree', sha=build(value))
                else:
                    b = blob_sha(value); self.blobs[b] = value
                    item = dict(path=name, mode='100644', type='blob', sha=b)
                rows.append(item)
            h = hashlib.sha1(json.dumps(rows, sort_keys=True).encode()).hexdigest()
            self.trees[h] = dict(truncated=False, tree=rows)
            return h
        return build(directory)

    def kit_summary(self, state='published'):
        result = dict(environment='production', files=self.ctx['expected_files'], title=TITLE,
            state=state, id=99900002, metadata_normalizations=[],
            doi='10.5281/zenodo.99900002', doi_url='https://doi.org/10.5281/zenodo.99900002',
            record_url='https://zenodo.org/records/99900002',
            doi_resolution=dict(status='resolved', http_status=200,
                url='https://doi.org/10.5281/zenodo.99900002',
                resolved_url='https://zenodo.org/records/99900002'))
        if self.doi_pending: result['doi_resolution'].update(status='not_resolved', http_status=404)
        return result

    def seed_publication(self):
        v = self.kit_summary()
        z = dict(submitted=True, metadata_and_files_verified=True,
            exact_reviewed_frozen_files_published=True, release_binding=g.binding(self.ctx),
            metadata=self.ctx['metadata'], files=self.ctx['expected_files'],
            additional_public_readback_error=None,
            additional_actual_public_file_downloads=[dict(file=x['name'], bytes=x['size'],
                sha256=x['sha256'], actual_public_download_byte_hash_match=True)
                for x in self.ctx['expected_files']],
            **{k:v[k] for k in ['id','doi','doi_url','record_url','doi_resolution']})
        save(self.P / 'ZENODO_VERIFIED_PUBLICATION.json', z)
        return z

    def urlopen(self, request, *args, **kwargs):
        url = request.full_url; self.downloads.append(url)
        mapping = {x['name']: self.R / x['path'] for x in g.EXPECTED_DEPOSIT_FILES}
        name = url.split('/files/')[1].split('?')[0]
        if name not in mapping: raise AssertionError('Unexpected public download URL')
        raw = b'wrong public data' if self.fail_download else mapping[name].read_bytes()
        class Response:
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self): return raw
        return Response()

    def run(self, argv, *args, **kwargs):
        self.calls.append(list(argv))
        text_mode = kwargs.get('text', False)
        if 'zenodo.py' in ' '.join(argv):
            operation = argv[3]
            if operation == 'stage':
                self.stage_count += 1
                if self.fail_stage: return self.response({}, text_mode, 1)
            if operation == 'publish': self.publish_count += 1
            result = self.kit_summary('ready_to_publish' if operation in ['stage', 'inspect'] and self.publish_count == 0 else 'published')
            if operation == 'check': result = {k:result[k] for k in ['environment', 'files', 'title']}
            return self.response(result, text_mode)
        if argv[0].endswith('/gws'):
            kind = argv[1:5]
            params = json.loads(argv[argv.index('--params') + 1])
            assert params['spreadsheetId'] == '1ZljUv5Q98jNXLoHK8WjwrkzSm3dhHC1-7LElcOU7y20'
            if kind[:3] == ['sheets','spreadsheets','get']:
                result = dict(sheets=[dict(properties=dict(sheetId=1254632077, title='Math Puzzles'))])
            elif kind == ['sheets','spreadsheets','values','get']:
                result = dict(values=self.sheet if params['range'] == "'Math Puzzles'!A:D" else [self.sheet[-1]])
            elif kind == ['sheets','spreadsheets','values','append']:
                self.append_count += 1
                row = json.loads(argv[argv.index('--json') + 1])['values'][0]
                self.sheet.append(row)
                result = dict(updates=dict(updatedRows=1, updatedCells=4,
                    updatedData=dict(values=[row]), updatedRange="'Math Puzzles'!A2:D2"))
            else: raise AssertionError('Unrecognized GWS operation')
            return self.response(result, text_mode)
        if argv[0].endswith('/gh'):
            method = argv[argv.index('--method') + 1] if '--method' in argv else 'GET'
            endpoint = argv[argv.index('--method') + 2] if '--method' in argv else argv[2]
            endpoint = endpoint.removeprefix('repos/AlecKriebel/Math/')
            payload = json.loads(Path(argv[argv.index('--input') + 1]).read_text()) if '--input' in argv else None
            return self.response(self.api(method, endpoint, payload), text_mode)
        raise AssertionError('Unexpected mocked subprocess: ' + repr(argv))

    @staticmethod
    def response(value, text_mode, code=0):
        raw = json.dumps(value)
        return subprocess.CompletedProcess([], code, raw if text_mode else raw.encode(), '' if text_mode else b'')

    def api(self, method, endpoint, payload):
        if endpoint == 'pulls/210' and method == 'GET': return copy.deepcopy(self.pr)
        if endpoint == 'pulls/210' and method == 'PATCH': return copy.deepcopy(self.pr)
        if endpoint == 'git/ref/heads/main': return dict(object=dict(sha=self.main))
        if endpoint == 'git/ref/heads/dot/math-5100033': return dict(object=dict(sha=self.pr['head']['sha']))
        if endpoint.startswith('git/commits/') and method == 'GET': return copy.deepcopy(self.commits[endpoint.split('/')[-1]])
        if endpoint.startswith('git/trees/') and method == 'GET': return copy.deepcopy(self.trees[endpoint.split('/')[-1]])
        if endpoint.startswith('git/blobs/') and method == 'GET':
            raw = self.blobs[endpoint.split('/')[-1]]
            return dict(content=base64.b64encode(raw).decode(), encoding='base64')
        if endpoint.startswith('contents/'):
            path, ref = endpoint.removeprefix('contents/').split('?ref=')
            if ref == OLD: raw = self.qraw; identity = self.intake['Queue_blob']
            elif ref == self.main: raw = self.qraw; identity = blob_sha(raw)
            else: raw = self.native_files[path]; identity = blob_sha(raw)
            return dict(content=base64.b64encode(raw).decode(), encoding='base64', sha=identity)
        if endpoint == 'git/blobs' and method == 'POST':
            raw = base64.b64decode(payload['content']); identity = blob_sha(raw); self.blobs[identity] = raw
            return dict(sha=identity)
        if endpoint == 'git/trees' and method == 'POST':
            assert payload['base_tree'] == self.commits[self.main]['tree']['sha']
            self.native_files = {QPATH:self.qraw}
            for entry in payload['tree']:
                self.native_files[entry['path']] = entry['content'].encode() if 'content' in entry else self.blobs[entry['sha']]
            return dict(sha=self.make_tree(self.native_files))
        if endpoint == 'git/commits' and method == 'POST':
            assert payload['parents'] == [OLD, self.main]
            identity = 'b' * 40
            self.commits[identity] = dict(tree=dict(sha=payload['tree']), parents=[dict(sha=x) for x in payload['parents']])
            return dict(sha=identity)
        if endpoint == 'git/refs/heads/dot/math-5100033' and method == 'PATCH':
            assert payload['force'] is False
            self.pr['head']['sha'] = payload['sha']; return dict(object=dict(sha=payload['sha']))
        if endpoint.startswith('compare/'):
            if self.before_native_compare: self.before_native_compare()
            return self.compare_override or dict(files=[dict(filename=p, status='modified' if p == QPATH else 'added') for p in self.native_files])
        if endpoint == 'graphql' and method == 'POST':
            self.ready_count += 1; self.pr['draft'] = False
            return dict(data=dict(markPullRequestReadyForReview=dict(pullRequest=dict(id='SYNTHETIC_PR_NODE', isDraft=False))))
        if endpoint == 'pulls/210/merge' and method == 'PUT':
            self.merge_count += 1
            assert payload['sha'] == self.pr['head']['sha']
            if self.fail_merge: raise RuntimeError('Synthetic uncertain merge response')
            self.pr.update(merged=True, state='closed', merge_commit_sha='c' * 40)
            return dict(merged=True, sha='c' * 40)
        raise AssertionError('Unexpected mocked native API call: ' + method + ' ' + endpoint)

    def execute(self, name):
        previous = sys.path[:]; sys.path.insert(0, str(self.P))
        # A previous fixture must not leave this action module cached.
        sys.modules.pop('verify_published_readonly', None)
        namespace = None
        with patch.object(subprocess, 'run', self.run), patch.object(subprocess, 'Popen', forbidden), \
             patch.object(urllib.request, 'urlopen', self.urlopen), patch.object(socket, 'create_connection', forbidden), \
             patch.object(socket, 'socket', forbidden), redirect_stdout(io.StringIO()):
            try: namespace = runpy.run_path(str(self.P / name), run_name='__main__')
            finally:
                if namespace and '_RELEASE_LOCK' in namespace: namespace['_RELEASE_LOCK'].close()
                sys.path[:] = previous
                gc.collect()


def expect(name, action, exception=None):
    try: action()
    except Exception as exc:
        if exception is None or not isinstance(exc, exception): raise
        RESULTS.append(dict(test=name, passed=True, refused=type(exc).__name__, reason=str(exc)))
    else:
        assert exception is None, name + ': expected rejection'
        RESULTS.append(dict(test=name, passed=True))


def with_fixture(name, action):
    with tempfile.TemporaryDirectory(prefix='fixture-', dir=OUT) as tmp:
        fixture = Fixture(Path(tmp)); action(fixture)
    gc.collect()


def run_probes():
    def publication_success(f):
        f.execute('publish_preprint.py')
        z = g.publication(f.R,f.P,f.ctx)
        assert f.stage_count == f.publish_count == 1 and len(f.downloads) == 2
        assert z['metadata'] == f.ctx['metadata']
        expect('normal publication, exact public SHA pair and DOI/version', lambda: None)
        before = len(f.calls)
        expect('verified publication refuses action reentry', lambda:f.execute('publish_preprint.py'), AssertionError)
        assert len(f.calls) == before
    with_fixture('publication_success', publication_success)

    def stage_failure(f):
        f.fail_stage=True
        expect('uncertain stage creates a durable exclusive intent',lambda:f.execute('publish_preprint.py'),RuntimeError)
        assert (f.P/'STAGE_ATTEMPT.json').exists() and f.stage_count==1
        before=len(f.calls)
        expect('uncertain stage action reentry refuses before CLI',lambda:f.execute('publish_preprint.py'),AssertionError)
        assert len(f.calls)==before
    with_fixture('stage_failure',stage_failure)

    for mode in ['DOI_pending','bad_public_SHA']:
        def pending(f,mode=mode):
            f.doi_pending=mode=='DOI_pending';f.fail_download=mode=='bad_public_SHA'
            expect(mode+' retains provider fact and refuses promotion',lambda:f.execute('publish_preprint.py'),RuntimeError)
            assert (f.P/'ZENODO_PROVIDER_CONFIRMED_PUBLICATION.json').exists()
            assert (f.P/'PUBLICATION_VERIFICATION_PENDING.json').exists()
            assert not (f.P/'ZENODO_VERIFIED_PUBLICATION.json').exists()
            assert f.publish_count==f.stage_count==1
            f.doi_pending=f.fail_download=False
            f.execute('verify_published_readonly.py')
            g.publication(f.R,f.P,f.ctx)
            assert f.publish_count==f.stage_count==1
            expect(mode+' recovers exclusively through inspect/downloads',lambda:None)
        with_fixture(mode,pending)

    def tracker_success(f):
        f.seed_publication();f.execute('append_verified_tracker.py')
        g.tracker(f.R,f.P,f.ctx);assert f.append_count==1
        expect('normal exact four-cell tracker append',lambda:None)
        (f.P/'TRACKER_VERIFIED_APPEND.json').unlink()
        f.execute('append_verified_tracker.py');assert f.append_count==1
        assert json.loads((f.P/'TRACKER_VERIFIED_APPEND.json').read_text())['append_count']==0
        expect('tracker existing exact attempted row reconciles without reappend',lambda:None)
    with_fixture('tracker_success',tracker_success)

    def tracker_conflict(f):
        f.seed_publication();f.sheet.append(['https://arxiv.org/abs/2004.12497v11','','https://doi.org/10.5281/zenodo.99900001','5100033 / AMR-050-0033'])
        expect('append-time conflicting problem with different DOI refuses',lambda:f.execute('append_verified_tracker.py'),RuntimeError)
        assert f.append_count==0
    with_fixture('tracker_conflict',tracker_conflict)

    def stale_append(f):
        f.seed_publication();f.execute('append_verified_tracker.py');(f.P/'TRACKER_VERIFIED_APPEND.json').unlink()
        p=f.P/'private_transport/tracker/APPEND_ATTEMPT.json';a=json.loads(p.read_text());a['release_binding']['clearance_sha256']='0'*64;save(p,a)
        expect('exact tracker row with stale attempt release refuses',lambda:f.execute('append_verified_tracker.py'),RuntimeError)
        assert f.append_count==1
    with_fixture('stale_append',stale_append)

    def prepare(f):
        f.seed_publication();f.execute('append_verified_tracker.py');f.execute('integrate_reviewed_pr.py')
        p=json.loads((f.P/'PR_PREPARED.json').read_text())
        assert p['parents']==[OLD,f.main] and p['prepared_head']==f.pr['head']['sha']
        assert len(p['included_owned_pins'])<300
        return p

    def native_success(f):
        p=prepare(f)
        assert f.native_files[QPATH].decode().splitlines()[1]==f.qraw.decode().splitlines()[1]
        assert 'claimed_solved' in p['target_queue_row'] and '1/5' in p['target_queue_row'] and '2020' in p['target_queue_row']
        expect('native integration succeeds with two parents, reviewed seals and foreign queue preserved',lambda:None)
        f.execute('verify_and_merge.py');assert f.ready_count==f.merge_count==1
        m=json.loads((f.P/'PR_MERGED.json').read_text());assert m['program_counts']==[44,21,21,0]
        expect('native expected-head full tree/body verification, ready and merged/closed readback',lambda:None)
    with_fixture('native_success',native_success)

    for field in ['tree','main_parent','publication_receipt_sha256','release_binding']:
        def stale_prepared(f,field=field):
            p=prepare(f)
            p[field] = {'clearance_sha256':'0'*64} if field=='release_binding' else '0'*40
            save(f.P/'PR_PREPARED.json',p)
            expect('native prepared '+field+' mismatch refuses before ready/merge',lambda:f.execute('verify_and_merge.py'),RuntimeError)
            assert f.ready_count==f.merge_count==0
        with_fixture('stale_prepared_'+field,stale_prepared)

    def prior_ready(f):
        prepare(f);save(f.P/'NATIVE_READY_ATTEMPT.json',dict(synthetic_fixture_only=True))
        expect('uncertain ready intent with draft still true refuses second POST',lambda:f.execute('verify_and_merge.py'),FileExistsError)
        assert f.ready_count==f.merge_count==0
        f.pr['draft']=False
        f.execute('verify_and_merge.py');assert f.ready_count==0 and f.merge_count==1
        expect('confirmed ready state permits merge without repeating prior ready POST',lambda:None)
    with_fixture('prior_ready',prior_ready)

    def uncertain_merge(f):
        prepare(f);f.fail_merge=True
        expect('uncertain merge leaves exclusive request before one PUT',lambda:f.execute('verify_and_merge.py'),RuntimeError)
        assert f.merge_count==1 and (f.P/'NATIVE_MERGE_REQUEST.json').exists()
        before=len(f.calls)
        expect('prior merge request refuses action reentry before CLI',lambda:f.execute('verify_and_merge.py'),RuntimeError)
        assert f.merge_count==1 and len(f.calls)==before
    with_fixture('uncertain_merge',uncertain_merge)

    def wrong_branch(f):
        f.pr['head']['ref']='another-branch'
        expect('publication wrong branch refuses before stage',lambda:f.execute('publish_preprint.py'),RuntimeError)
        assert f.stage_count==0
    with_fixture('wrong_branch',wrong_branch)

    def ready_clearance_change(f):
        prepare(f)
        def invalidate():
            bad=copy.deepcopy(f.clear);bad['release_cleared']=False;save(f.R/'FINAL_CLEARANCE.json',bad)
        f.before_native_compare=invalidate
        expect('clearance invalidated during native reads stops merge',lambda:f.execute('verify_and_merge.py'),RuntimeError)
        assert f.merge_count==0
        RESULTS.append(dict(test='ready transition after clearance invalidation',
            passed=False, defect_reproduced=True, ready_POST_count=f.ready_count,
            merge_PUT_count=f.merge_count, invalid_clearance_at_ready=True,
            reason='No unchanged/publication/tracker revalidation immediately precedes ready POST'))
        assert f.ready_count==1
    with_fixture('ready_clearance_change',ready_clearance_change)

    # Observe exactly which descriptor(s) exclusive_json flushes; no crash is simulated.
    with tempfile.TemporaryDirectory(prefix='fsync-fixture-',dir=OUT) as tmp:
        path=Path(tmp)/'intent.json';syncs=[];real_fsync=os.fsync
        def record(fd):
            syncs.append(dict(fd=fd,is_directory=os.path.isdir('/dev/fd/'+str(fd))))
            return real_fsync(fd)
        with patch.object(os,'fsync',record):g.exclusive_json(path,{'synthetic_fixture_only':True})
        RESULTS.append(dict(test='intent persistence descriptor trace',passed=True,
            fsync_calls=syncs,parent_directory_fsynced=any(x['is_directory'] for x in syncs),
            scope='Trace only; no crash or filesystem durability guarantee asserted by this computation'))


if __name__=='__main__':
    run_probes()
    result=dict(utc=datetime.now(timezone.utc).isoformat(),synthetic_fixture_only=True,
        network_or_provider_calls=0,actual_subprocesses_executed=0,
        untrapped_helper_top_levels_imported=0,tests=RESULTS,
        passing_test_count=sum(r['passed'] for r in RESULTS),
        reproduced_defects=[r for r in RESULTS if r.get('defect_reproduced')],
        completion_percent=75)
    save(OUT/'MOCKED_WORKFLOW_RESULTS.json',result)
    print(json.dumps(result,indent=2))
