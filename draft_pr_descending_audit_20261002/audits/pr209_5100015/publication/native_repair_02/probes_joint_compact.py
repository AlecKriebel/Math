"""Final M03 exact-source matrix using two terminal fixtures plus R03 control.

External state mutations are reversible synthetic provider events. The initial
fixture has an actual simulated merge with an unknown original PATCH response,
then tests initial receipt creation exclusively through read-only recovery.
The accepted fixture retains its original immutable completion throughout.
"""
from pathlib import Path
from datetime import datetime, timezone
import contextlib, copy, io, json, traceback, http.client
import probes_joint_final as H

HERE = Path(__file__).resolve().parent
RESULTS = []


class Fixture(H.Fixture):
    def urlopen(self, url, **kw):
        response = super().urlopen(url, **kw)
        if not getattr(self, 'fail_one_download', False):
            return response
        self.fail_one_download = False
        raw = response.read()
        response.close()
        partial = raw[5:9] + b'\x00\xff'
        self.expected_partial_download = raw[:5] + partial
        class Interrupted:
            first = True
            def __enter__(self): return self
            def __exit__(self, *args): return None
            def read(self, size):
                if self.first:
                    self.first = False
                    return raw[:5]
                raise http.client.IncompleteRead(partial, 100)
        return Interrupted()


def record(label, fn):
    start = datetime.now(timezone.utc).isoformat()
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            result = fn()
        row = dict(label=label, start_utc=start, completed_utc=datetime.now(timezone.utc).isoformat(), PASS=True, result=result)
    except Exception as error:
        row = dict(label=label, start_utc=start, completed_utc=datetime.now(timezone.utc).isoformat(), PASS=False,
            error=repr(error), traceback=traceback.format_exc())
    RESULTS.append(row)
    H.L.b.dump(HERE / 'JOINT_COMPACT_RESULTS.json', RESULTS)
    print(json.dumps(row), flush=True)
    return row


def terminal_fixture(accepted):
    f = Fixture('joint_accepted' if accepted else 'joint_initial')
    f.prepare()
    if accepted:
        f.merge()
    else:
        f.unknown_main = True
        error = H.L.b.reject(f.merge)
        assert error['type'] == 'RuntimeError' and 'unknown' in error['error'].lower(), error
        f.unknown_main = False
    path = f.pub / 'PR_MERGED.json'
    assert path.exists() is accepted and H.main_writes(f) == 1
    f.old_completion = path.read_bytes() if accepted else None
    f.global_intent = (f.pub / 'NATIVE_MERGE_REQUEST.json').read_bytes()
    f.fixed_mutations = len(f.mutations)
    return f


def unchanged(f, accepted):
    path = f.pub / 'PR_MERGED.json'
    assert (path.read_bytes() == f.old_completion) if accepted else not path.exists()
    assert (f.pub / 'NATIVE_MERGE_REQUEST.json').read_bytes() == f.global_intent
    assert len(f.mutations) == f.fixed_mutations and H.main_writes(f) == 1


def drift_case(f, kind, accepted):
    saved = H.snapshot_native(f)
    try:
        f.completion_hook = lambda: H.mutate(f, kind)
        f.completion_hook_fired = False
        error = H.L.b.reject(lambda: f.merge(True))
        assert error['type'] == 'RuntimeError', error
        assert f.completion_hook_fired
        unchanged(f, accepted)
        observation = dict(kind=kind, error=error, actual_pr=copy.deepcopy(f.pr), actual_main=f.main_head,
            actual_result_commit=copy.deepcopy(f.commits[saved['pr']['merge_commit_sha']]),
            existing_receipt=accepted, no_completion_creation_or_rewrite=True,
            mutations=len(f.mutations), main_writes=1)
        H.L.b.dump(f.base / ('DRIFT_' + kind + '.json'), observation)
        return dict(error=error, existing_receipt=accepted, receipt_unchanged_or_absent=True, main_writes=1)
    finally:
        # Restore only controlled provider state. No candidate write or intent
        # reset occurs; every failed transport observation remains on disk.
        H.restore_native(f, saved)
        f.completion_hook = None


def unknown_case(f, kind, accepted):
    saved = H.snapshot_native(f)
    try:
        def hook():
            if kind == 'download':
                f.fail_one_download = True
            else:
                if kind == 'ancestry':
                    f.advance({'foreign/unknown-final-ancestry.txt': b'SYNTHETIC valid foreign descendant'})
                f.late_unknown_path = {'pr': 'pulls/209', 'ref': 'git/ref/heads/dot/math-5100015',
                    'commit': 'git/commits/' + f.pr['merge_commit_sha'], 'main': 'git/ref/heads/main',
                    'ancestry': 'compare/'}[kind]
        f.completion_hook = hook
        f.completion_hook_fired = False
        error = H.L.b.reject(lambda: f.merge(True))
        expected_type = 'IncompleteRead' if kind == 'download' else 'RuntimeError'
        assert error['type'] == expected_type, error
        assert f.completion_hook_fired
        unchanged(f, accepted)
        if kind == 'download':
            candidates = list((f.pub / 'private_transport').rglob('k303b-outer-center-pedal-areas.pdf'))
            assert any(p.read_bytes() == f.expected_partial_download for p in candidates)
        else:
            assert 'unknown' in error['error'].lower()
            outputs = list((f.pub / 'private_transport').rglob('*-partial-stdout.bin'))
            assert any(p.read_bytes() == b'SYNTHETIC final-read partial\x00\xff' for p in outputs)
        return dict(kind=kind, error=error, existing_receipt=accepted, failure_bytes_preserved=True,
            no_completion_creation_or_rewrite=True, main_writes=1)
    finally:
        H.restore_native(f, saved)
        f.completion_hook = None
        f.fail_one_download = False


def write_modes_stay_forbidden(f, accepted):
    normal = H.L.b.reject(f.merge)
    resume = H.L.b.reject(f.resume)
    assert normal['type'] == resume['type'] == 'RuntimeError'
    assert 'already created' in resume['error']
    unchanged(f, accepted)
    return dict(normal=normal, resume=resume, no_second_main_write=True)


def valid_foreign_recovery(f, accepted):
    def hook():
        f.advance({'foreign/final-descendant.txt': b'SYNTHETIC successful foreign work preserved'})
    f.completion_hook = hook
    f.completion_hook_fired = False
    f.merge(True)
    assert f.completion_hook_fired and len(f.mutations) == f.fixed_mutations and H.main_writes(f) == 1
    path = f.pub / 'PR_MERGED.json'
    if accepted:
        assert path.read_bytes() == f.old_completion
    else:
        receipt = json.loads(path.read_bytes())
        assert receipt['case_completion_percent'] == 100 and receipt['program_counts'] == [45,22,22,0]
    files = f.filetrees[f.commits[f.main_head]['tree']['sha']]
    assert files['foreign/final-descendant.txt'] == b'SYNTHETIC successful foreign work preserved'
    f.trace()
    return dict(existing_receipt=accepted, recovered_readonly=True, legitimate_foreign_descendant_preserved=True,
        global_intent_unchanged=(f.pub / 'NATIVE_MERGE_REQUEST.json').read_bytes() == f.global_intent,
        main_writes=1, counts_increment_once=True)


if __name__ == '__main__':
    for accepted in [False, True]:
        prefix = 'accepted_' if accepted else 'initial_'
        with contextlib.redirect_stdout(io.StringIO()):
            f = terminal_fixture(accepted)
        for kind in ['title', 'body', 'head', 'ref', 'main', 'event', 'tree', 'parents', 'state', 'combined']:
            record(prefix + kind, lambda kind=kind: drift_case(f, kind, accepted))
        for kind in ['download', 'pr', 'ref', 'commit', 'main', 'ancestry']:
            record(prefix + 'unknown_' + kind, lambda kind=kind: unknown_case(f, kind, accepted))
        record(prefix + 'write_modes_refused', lambda: write_modes_stay_forbidden(f, accepted))
        record(prefix + 'valid_foreign_recovery', lambda: valid_foreign_recovery(f, accepted))
        f.trace()
        receipt = H.archive_completed_group(HERE, H.L.b.RUNS, 'joint_compact_' + prefix.rstrip('_'))
        print(json.dumps(dict(fixture_archive=receipt)), flush=True)
    record('R03_two_safe_advances_exactly_one_main_write', H.L.safe_advance_recovery)
    receipt = H.archive_completed_group(HERE, H.L.b.RUNS, 'joint_compact_R03')
    print(json.dumps(dict(fixture_archive=receipt)), flush=True)
    summary = dict(utc=datetime.now(timezone.utc).isoformat(), groups=len(RESULTS), all_pass=all(x['PASS'] for x in RESULTS),
        root_freeze_utc=H.FREEZE['root_freeze_utc'], final_all_six_freeze=True,
        case_completion_percent=65, no_release_authority=True)
    H.L.b.dump(HERE / 'JOINT_COMPACT_SUMMARY.json', summary)
    print(json.dumps(summary), flush=True)
    raise SystemExit(0 if summary['all_pass'] else 1)
