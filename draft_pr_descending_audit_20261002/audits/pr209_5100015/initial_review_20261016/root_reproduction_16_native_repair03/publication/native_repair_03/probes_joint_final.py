"""Native completion-drift controls against unchanged compiled helper sources.

All publication/GWS/Git providers are in-memory protocols. The root-authorized
joint snapshot pins all six final candidate sources. Synthetic provider/review
authority grants no real release clearance.
"""
from pathlib import Path
from datetime import datetime, timezone
import contextlib, copy, io, json, types, traceback
import legacy_fixture_source as L
from archive_completed_group import archive_completed_group

HERE = Path(__file__).resolve().parent
SNAP = HERE / 'candidate_sources_01'
L.HERE = HERE
L.b.HERE = HERE
L.b.SNAP = SNAP
L.b.RUNS = HERE / 'joint_final_runs'
FREEZE = json.loads((HERE / 'CANDIDATE_INPUTS_01.json').read_text())
L.b.SOURCE = {n: (SNAP / n).read_bytes() for n in L.b.NAMES}
for entry in FREEZE['files']:
    raw=L.b.SOURCE[Path(entry['path']).name]
    assert len(raw)==entry['bytes'] and L.b.sha(raw)==entry['sha256'], 'Frozen source changed'
RESULTS = []


class Fixture(L.Fixture):
    def run(self, args, **kw):
        result = super().run(args, **kw)
        if args[0].endswith('/gws'):
            params=json.loads(args[args.index('--params')+1])
            value=json.loads(result.stdout)
            grid=1114+self.appends
            if args[1:4]==['sheets','spreadsheets','get']:
                value['sheets'][0]['properties'].update(gridProperties=dict(rowCount=grid,columnCount=43),sheetType='GRID')
            elif args[4]=='append':
                value.update(spreadsheetId=self.rb.SHEET,tableRange='\'Math Puzzles\'!A1:D1')
                update=value['updates'];update['updatedColumns']=4
                update['updatedData'].update(range=update['updatedRange'],majorDimension='ROWS')
            else:
                value['majorDimension']='ROWS'
                if params['range']==self.rb.FULL_RANGE:value['range']='\'Math Puzzles\'!A1:D'+str(grid)
            result.stdout=json.dumps(value).encode()
        if isinstance(result.stdout,str):result.stdout=result.stdout.encode()
        if isinstance(result.stderr,str):result.stderr=result.stderr.encode()
        # The mutation is provider state, after an otherwise valid publication
        # inspect. It occurs only inside complete_merge's known long interval.
        if (len(args) > 3 and args[3] == 'inspect' and getattr(self, 'pr', {}).get('merged')
                and getattr(self, 'completion_hook', None) is not None):
            hook = self.completion_hook
            self.completion_hook = None
            self.completion_hook_fired = True
            hook()
        return result

    def urlopen(self,url,**kw):
        name=url.split('/files/')[1].split('?')[0]
        mapping=next(m for m in self.maps if m['name']==name)
        raw=(self.r/mapping['path']).read_bytes()
        self.calls.append(dict(public_url=url,bytes=len(raw),cursor_http_fixture=True))
        return io.BytesIO(raw)

    def native(self, method, path, payload):
        if (method == 'GET' and getattr(self, 'late_unknown_path', None) is not None
                and path.startswith(self.late_unknown_path)):
            self.late_unknown_path = None
            error = TimeoutError('SYNTHETIC unknown final native response')
            error.stdout = b'SYNTHETIC final-read partial\x00\xff'
            error.stderr = b'SYNTHETIC final-read stderr\x00\xfe'
            raise error
        if method == 'GET' and path == 'git/ref/heads/dot/math-5100015' and getattr(self, 'branch_override', None):
            self.native_calls.append(dict(method=method, path=path, payload=payload, synthetic_branch_override=True))
            return {'object': {'sha': self.branch_override}}
        return super().native(method, path, payload)


# Legacy R03 controls use the same NEW binary/grid/cursor fixture adapter.
L.Fixture = Fixture


def setup(label, accepted=False):
    f = Fixture(label)
    f.prepare()
    if accepted:
        f.merge()
        assert (f.pub / 'PR_MERGED.json').exists()
    return f


def main_writes(f):
    return sum(x['path'] == 'git/refs/heads/main' for x in f.mutations)


def snapshot_native(f):
    return dict(pr=copy.deepcopy(f.pr), main=f.main_head,
        commits=copy.deepcopy(f.commits), branch=getattr(f, 'branch_override', None))


def restore_native(f, saved):
    f.pr = copy.deepcopy(saved['pr'])
    f.main_head = saved['main']
    f.commits = copy.deepcopy(saved['commits'])
    f.branch_override = saved['branch']
    f.late_unknown_path = None


def mutate(f, kind):
    merge = f.pr['merge_commit_sha']
    if kind in {'body', 'combined'}:
        f.pr['body'] = 'STALE FOCAL FIRST PROOF CLAIM DURING LIVE READ'
    elif kind == 'title':
        f.pr['title'] = 'SYNTHETIC stale focal first-proof title'
    elif kind == 'head':
        f.pr['head']['sha'] = L.OLD
    elif kind == 'ref':
        f.branch_override = L.OLD
    elif kind == 'event':
        f.pr['merge_commit_sha'] = L.OLD
    elif kind == 'state':
        f.pr.update(state='open', merged=False)
    elif kind == 'parents':
        f.commits[merge]['parents'] = []
    elif kind == 'tree':
        original = dict(f.filetrees[f.commits[merge]['tree']['sha']])
        original[L.PREFIX + 'SYNTHETIC_UNREVIEWED.txt'] = b'SYNTHETIC corrupt actual result tree'
        f.commits[merge]['tree']['sha'] = f.tree(original)
    if kind in {'main', 'combined'}:
        f.main_head = 'SYNTHETIC-non-descendant-main'
        f.commits[f.main_head] = dict(tree={'sha': f.tree({L.QUEUE: b'SYNTHETIC foreign rewritten main\n'})}, parents=[])


def drift(kind, accepted):
    label = ('accepted_' if accepted else 'initial_') + kind
    f = setup(label, accepted)
    receipt_path = f.pub / 'PR_MERGED.json'
    old = receipt_path.read_bytes() if accepted else None
    # Initial completion enters after the one actual simulated main update.
    # Capture that state in the callback so restoration means read-only
    # reconciliation of the already completed provider merge.
    saved = {}
    def hook():
        saved.update(snapshot_native(f))
        mutate(f, kind)
    f.completion_hook = hook
    first = L.b.reject(lambda: f.merge(accepted))
    assert first['type']=='RuntimeError', first
    assert f.completion_hook_fired and main_writes(f) == 1
    global_path = f.pub / 'NATIVE_MERGE_REQUEST.json'
    global_raw = global_path.read_bytes()
    assert (receipt_path.read_bytes() == old) if accepted else not receipt_path.exists()
    before = len(f.mutations)
    # Both write-capable modes stay forbidden after the durable global intent.
    normal = L.b.reject(f.merge)
    resume = L.b.reject(f.resume)
    pending = L.b.reject(lambda: f.merge(True))
    assert pending['type']=='RuntimeError', pending
    assert len(f.mutations) == before and global_path.read_bytes() == global_raw
    assert (receipt_path.read_bytes() == old) if accepted else not receipt_path.exists()
    restore_native(f, saved)
    f.merge(True)
    assert len(f.mutations) == before and main_writes(f) == 1
    recovered = receipt_path.read_bytes()
    assert (recovered == old) if accepted else json.loads(recovered)['case_completion_percent'] == 100
    f.trace()
    return dict(kind=kind, existing_receipt=accepted, first=first, still_pending=pending,
        normal_refused=normal, resume_refused=resume, receipt_unchanged_during_drift=True,
        recovery_readonly=True, main_writes=1)


def foreign_descendant(accepted=False, unknown=False):
    f = setup(('accepted_' if accepted else 'initial_') + ('foreign_unknown' if unknown else 'foreign'), accepted)
    path = f.pub / 'PR_MERGED.json'
    old = path.read_bytes() if accepted else None
    def hook():
        f.advance({'foreign/late-descendant.txt': b'SYNTHETIC legitimate late foreign work'})
        if unknown:
            f.late_unknown_path = 'compare/'
    f.completion_hook = hook
    if unknown:
        first = L.b.reject(lambda: f.merge(accepted))
        assert first['type']=='RuntimeError', first
        assert (path.read_bytes() == old) if accepted else not path.exists()
        before = len(f.mutations)
        f.merge(True)
        assert len(f.mutations) == before
    else:
        first = None
        f.merge(accepted)
    assert f.completion_hook_fired and main_writes(f) == 1
    assert f.filetrees[f.commits[f.main_head]['tree']['sha']]['foreign/late-descendant.txt'] == b'SYNTHETIC legitimate late foreign work'
    if accepted:
        assert path.read_bytes() == old
    f.trace()
    return dict(existing_receipt=accepted, unknown_final_ancestry=unknown, first=first,
        legitimate_foreign_descendant_accepted=True, old_receipt_unchanged=accepted, main_writes=1)


def unknown_final(path_kind, accepted):
    f = setup(('accepted_' if accepted else 'initial_') + 'unknown_' + path_kind, accepted)
    path = f.pub / 'PR_MERGED.json'
    old = path.read_bytes() if accepted else None
    def hook():
        f.late_unknown_path = 'pulls/209' if path_kind == 'pr' else 'git/ref/heads/main'
    f.completion_hook = hook
    first = L.b.reject(lambda: f.merge(accepted))
    assert first['type']=='RuntimeError', first
    assert f.completion_hook_fired and main_writes(f) == 1
    assert (path.read_bytes() == old) if accepted else not path.exists()
    before = len(f.mutations)
    L.b.reject(f.merge)
    L.b.reject(f.resume)
    f.merge(True)
    assert len(f.mutations) == before and main_writes(f) == 1
    if accepted:
        assert path.read_bytes() == old
    outputs = list((f.pub / 'private_transport').rglob('*-partial-stdout.bin'))
    assert any(p.read_bytes() == b'SYNTHETIC final-read partial\x00\xff' for p in outputs)
    f.trace()
    return dict(existing_receipt=accepted, first=first, partial_response_retained=True,
        recovered_readonly=True, main_writes=1)


def check(label, fn):
    start = datetime.now(timezone.utc).isoformat()
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            result = fn()
        row = dict(label=label, start_utc=start, completed_utc=datetime.now(timezone.utc).isoformat(), PASS=True, result=result)
    except Exception as error:
        row = dict(label=label, start_utc=start, completed_utc=datetime.now(timezone.utc).isoformat(), PASS=False,
            error=repr(error), traceback=traceback.format_exc())
    RESULTS.append(row)
    L.b.dump(HERE / 'JOINT_FINAL_RESULTS.json', RESULTS)
    print(json.dumps(row), flush=True)
    receipt = archive_completed_group(HERE, L.b.RUNS, 'joint_final_' + label)
    if receipt:
        print(json.dumps(dict(fixture_archive=receipt)), flush=True)


if __name__ == '__main__':
    for accepted in [False, True]:
        prefix = 'accepted_' if accepted else 'initial_'
        for kind in ['title', 'body', 'head', 'ref', 'main', 'event', 'tree', 'parents', 'state', 'combined']:
            check(prefix + kind, lambda kind=kind, accepted=accepted: drift(kind, accepted))
        check(prefix + 'foreign_descendant', lambda accepted=accepted: foreign_descendant(accepted))
        check(prefix + 'foreign_unknown', lambda accepted=accepted: foreign_descendant(accepted, True))
        for kind in ['pr', 'main']:
            check(prefix + 'unknown_' + kind, lambda kind=kind, accepted=accepted: unknown_final(kind, accepted))
    check('R03_repeated_safe_advances_preserved', L.safe_advance_recovery)
    summary = dict(groups=len(RESULTS), all_pass=all(x['PASS'] for x in RESULTS),
        case_completion_percent=65, release_authority=False, final_all_six_freeze=True,
        utc=datetime.now(timezone.utc).isoformat())
    L.b.dump(HERE / 'JOINT_FINAL_SUMMARY.json', summary)
    print(json.dumps(summary), flush=True)
    raise SystemExit(0 if summary['all_pass'] else 1)
