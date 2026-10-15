"""Write only this proposed SOURCE's narrow derivatives; no Git commands."""
import datetime
import difflib
import hashlib
import json
import os
from pathlib import Path

N = Path(__file__).absolute().parent
OLD = N.parent / 'checkpoint_20261003_1530_preparation'
assert N.name == 'checkpoint_20261003_1745_preparation'
PINS = {
    'common.py': '3a5860e2f022cbb5916c29d8f99e2e805ba21582cc0c0454f9b8f2b20d336665',
    'stage_checkpoint.py': '2f3a66919b3bc845becccf0447db4a3b964961b2dd13fd8d45fc4c2a90992e13',
    'commit_checkpoint.py': 'c9b68f71c95fd1d6e30a5697d76dd40448a277ceb4ef49ac876cd5f5e80c2c6f',
    'capture_source.py': '5f0d2da82d767e3b33c507dd91257a365e988483401457f99625577d09e511f0',
}


def sha(body):
    return hashlib.sha256(body).hexdigest()


def main():
    started = datetime.datetime.now(datetime.timezone.utc).isoformat()
    changes = []
    diff = []
    for name in PINS:
        src = OLD / name
        old = src.read_bytes()
        if sha(old) != PINS[name]:
            raise RuntimeError('Prior reviewed helper changed: ' + name)
        text = old.decode()
        if name == 'common.py':
            needle = "checkpoint_20261003_1530_preparation')"
            assert text.count(needle) == 1
            text = text.replace(needle, "checkpoint_20261003_1745_preparation')")
        elif name == 'stage_checkpoint.py':
            needle = "    marker = 'Checkpoint 20261003_1530 SOURCE reviewed by ROOT at ' + args.log_stamp + '; research only; prepared snapshot accepted37/180; PR48 merge/push complete, bookkeeping pending; PR55 already_solved1/5; PR56 unsolved2/5; PR57 claimed_solved1/5, priority pending; no paper or DOI.'\n"
            assert text.count(needle) == 1
            text = text.replace(needle,
                "    suffix = scope['ROOT_log_marker_suffix']\n"
                "    need(isinstance(suffix, str) and suffix and '\\n' not in suffix and '\\r' not in suffix, 'Exact reviewed one-line dated checkpoint context')\n"
                "    marker = 'Checkpoint 20261003_1745 SOURCE reviewed by ROOT at ' + args.log_stamp + '; ' + suffix\n")
        elif name == 'commit_checkpoint.py':
            needle = "        message = b'Checkpoint completed PR55-57 SOURCE findings and recovery evidence\\n\\nAdministrative research custody only. PR48 merge/push completed; bookkeeping pending in the prepared snapshot. Snapshot accepted37/180. No mathematical acceptance, paper, DOI or tracker transition.\\n'\n"
            assert text.count(needle) == 1
            text = text.replace(needle,
                "        message = b'Checkpoint completed PR48 and PR57-60 research evidence\\n\\nAdministrative research custody only. Prepared formal accepted snapshot37/180 (20.5556%). The PR57 preprint package remains unpublished. No native mathematical acceptance, DOI or tracker transition by this checkpoint.\\n'\n")
        elif name == 'capture_source.py':
            text = text.replace("choices=['build_scope.py','verify_source.py','read_source.py']", "choices=['inventory_draft.py','build_scope.py','verify_source.py','read_source.py']")
            text = text.replace('checkpoint_20261003_1530_preparation_readback_actual_capture', 'checkpoint_20261003_1745_preparation_readback_actual_capture')
        body = text.encode()
        dest = N / name
        with dest.open('xb') as f:
            f.write(body)
        changes.append(dict(prior_path=str(src), prior_sha256=sha(old), prior_bytes=len(old),
                            current_path=str(dest), current_sha256=sha(body), current_bytes=len(body),
                            mathematical_or_native_action=False))
        diff.extend(difflib.unified_diff(old.decode().splitlines(True), text.splitlines(True),
                                        fromfile='1530/' + name, tofile='1745/' + name))
    (N / 'HELPER_DERIVATION.diff').write_text(''.join(diff))
    record = dict(schema='checkpoint1745-narrow-SOURCE-helper-derivatives/v1', actual_writer_pid=os.getpid(),
                  started_utc=started, finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                  exact_changes=changes, old_source_modified=False, stage_commit_push_executed=False,
                  native_shared_log_or_real_index_HEAD_mutation=False,
                  mechanism='Only location, dated dedicated-log context, commit prose and SOURCE capture allowlist/name changes; foreign protection and topology/CAS remain identical.')
    body = (json.dumps(record, sort_keys=True, indent=2) + '\n').encode()
    (N / 'HELPER_DERIVATION.json').write_bytes(body)
    print(body.decode(), end='')


if __name__ == '__main__':
    main()
