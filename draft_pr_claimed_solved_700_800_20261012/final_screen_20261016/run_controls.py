"""Read-only source verification plus local disposable certificate controls."""
import datetime
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
PACKET = HERE / 'packet'
REPO = '/Users/alec/Documents/Math'
MP = '18a9c5af827deeffbb20b947db499023ac6ca3030662cd62801651757d989c80'
CP = '8cbfc42ea0fb21a9e6e123067bfe664de9895082a13b1e7a1d180e4aeb8256fe'


def need(test, message):
    if not test:
        raise RuntimeError(message)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def mutate_json(path, callback):
    data = json.loads(path.read_bytes())
    callback(data)
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')


def fresh_manifest(p):
    mutate_json(p / 'MANIFEST.json', lambda d: d.update(files={name: sha(p / name) for name in d['files']}))
    return sha(p / 'MANIFEST.json')


def main():
    need(sha(PACKET / 'MANIFEST.json') == MP and sha(PACKET / 'verify_certificate.py') == CP,
         'Original closed packet pin mismatch')
    records = []
    scratch = HERE / 'control-scratch'
    scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='owned-', dir=scratch) as temp:
        base = pathlib.Path(temp)
        hostile = base / 'hostile'
        hostile.mkdir()
        (hostile / 'sitecustomize.py').write_text('raise RuntimeError("HOSTILE_IMPORT_SHOULD_NOT_EXECUTE")\n')
        (hostile / 'json.py').write_text('raise RuntimeError("HOSTILE_IMPORT_SHOULD_NOT_EXECUTE")\n')

        def run(name, transform, should_pass, refresh=False, optimize=False):
            p = base / name
            shutil.copytree(PACKET, p)
            transform(p)
            mp = fresh_manifest(p) if refresh else MP
            command = [sys.executable, '-I', '-S', '-B'] + (['-O'] if optimize else [])
            command += [str(p / 'verify_certificate.py'), str(p), mp, CP, REPO, '--replay-blobs']
            result = subprocess.run(command, cwd=hostile, capture_output=True, text=True)
            passed = result.returncode == 0
            need(passed == should_pass, 'Unexpected control result: ' + name)
            records.append({'name': name, 'expected_pass': should_pass, 'exit_code': result.returncode,
                            'fresh_manifest_used': refresh, 'optimized': optimize,
                            'stdout': result.stdout.strip(), 'stderr_tail': result.stderr[-1600:]})

        run('relocated_hostile_normal', lambda p: None, True)
        run('relocated_hostile_optimized', lambda p: None, True, optimize=True)
        run('missing_file', lambda p: (p / 'REPORT.md').unlink(), False)
        run('extra_file', lambda p: (p / 'EXTRA.txt').write_text('unlisted\n'), False)

        def symlink(p):
            f = p / 'README.md'
            f.unlink()
            f.symlink_to(PACKET / 'README.md')
        run('symlink_entry', symlink, False)

        def bad_coverage(p):
            def alter(d):
                d['rows'] = d['rows'][:-1]
                d['numbers_accounted'] = 100
            mutate_json(p / 'CERTIFICATE.json', alter)
        run('fresh_manifest_missing_number800', bad_coverage, False, refresh=True)

        def forged_status(p):
            def alter(d):
                r = next(r for r in d['rows'] if r['number'] == 799)
                r['own_row'] = r['own_row'].replace('| claimed_solved |', '| unsolved |')
                r['own_row_sha256'] = hashlib.sha256(r['own_row'].encode()).hexdigest()
                r['queue_status'] = 'unsolved'
                r['disposition'] = 'skipped_out_of_scope'
                r['initial_status_unchanged'] = False
                d['open_draft_status_counts'] = {'unsolved': 81, 'already_solved': 9}
                for name in ('current_exact_claimed_solved_numbers', 'eligible_not_yet_processed_numbers'):
                    d[name] = []
            mutate_json(p / 'CERTIFICATE.json', alter)
        run('fresh_manifest_forged_799_status', forged_status, False, refresh=True)

        def bad_expression(p):
            for f in p.glob('queue_oids_*.json'):
                doc = json.loads(f.read_bytes())
                if 'q799:' in doc['query']:
                    doc['query'] = doc['query'].replace('cc45ec9dc93515593c3b2a228def86c3a562e13f:', '0' * 40 + ':')
                    f.write_text(json.dumps(doc, indent=2, sort_keys=True) + '\n')
                    return
            raise RuntimeError('No q799 source query')
        run('fresh_manifest_wrong_799_immutable_expression', bad_expression, False, refresh=True)

    receipt = {'status': 'PASS', 'finished_at': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'manifest_sha256': MP, 'checker_sha256': CP, 'control_count': len(records),
               'positive': sum(r['expected_pass'] for r in records),
               'negative': sum(not r['expected_pass'] for r in records), 'records': records,
               'original_packet_unchanged': sha(PACKET / 'MANIFEST.json') == MP,
               'scope': 'Only owned disposable copies and read-only existing source blob reads; no network or Git writes'}
    need(receipt['original_packet_unchanged'], 'Original packet changed')
    (HERE / 'CONTROL_RESULTS.json').write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: v for k, v in receipt.items() if k != 'records'}))


if __name__ == '__main__':
    main()
