"""Root custody check; --record also captures the three inspected read-only verifiers.

No mathematical/source programme is run, and the default invocation writes nothing.
"""
from pathlib import Path
from hashlib import sha256, md5
import datetime, json, os, subprocess, sys

ROOT = Path(__file__).resolve().parent
PAPER = ROOT.parents[1]
PROGRAMME = PAPER.parents[1]
SOURCES = PAPER / 'sources'
seen = {}

def need(value, message):
    if not value:
        raise RuntimeError(message)

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

def read(path):
    return json.loads(path.read_text())

def check(row, base):
    path = Path(row.get('path', row.get('relative_path')))
    if not path.is_absolute():
        path = base / path
    expected = row.get('sha256', row.get('SHA256'))
    need(path.is_file() and not path.is_symlink(), 'Regular file: ' + str(path))
    need(type(row['bytes']) is int and path.stat().st_size == row['bytes']
         and digest(path) == expected, 'Exact binding: ' + str(path))
    if str(path) in seen:
        need(seen[str(path)] == expected, 'Conflicting binding')
    seen[str(path)] = expected

def table(path, base):
    for row in read(path)['files']:
        check(row, base)

def main():
    pins = {
        SOURCES / 'SOURCE_READY.json': 'ccc7a9bd68b205f78886fbd51a84cfe4f6aa768d154d82f802918889cd9f6828',
        SOURCES / 'SOURCE_READY_MANIFEST.json': '0dc2e9d5ac2c89f033ba18522eba92067c3a5422495af90bae644362eccbef3f',
        SOURCES / 'SOURCE_READY_SEAL.json': 'bd759f183997313109e614402cdd3a40fc155fe3e0148d3e7579a899d779d5bf',
        SOURCES / 'SOURCE_FINAL_MANIFEST.json': '59e5af1b8aaf84ba2edeb23494cee33788043bdb6bcfe1f4b614d2282621c5af',
        SOURCES / 'SOURCE_FINAL_SEAL.json': 'fec38a460a5e9cdf74cce6e7aa22609a9f92cadc034f5745fd5128bd70620a76',
        ROOT / 'INITIAL_SEAL.json': '00e4dd6560f2a7202515503e04d4e6f894b3fc38d34144e2f58775e64fb46add',
        PAPER / 'reviews/scope/FINAL_MANIFEST.json': 'ffeab9a93c18f3eb0d8a676a4d2a265f3976b83f03188c57a5c484142b238f87',
        PAPER / 'reviews/scope/FINAL_SEAL.json': '71e31b434b4a9f461b1fd8ff7166ef64cac530e45a43b772ade5b2b6995fe8ff',
        PAPER / 'reviews/analytic/MANIFEST.json': '6cba77d352d26bbf5a4c9697204901e95007f60234b0b096edd2f17f8db688aa',
        PAPER / 'reviews/analytic/SEAL.json': 'bf1b8f46067e24bb0565d2d3d182a298f0369453591618f81e07e4330012edcb',
        PAPER / 'reviews/adversarial/FINAL_MANIFEST.json': 'ab6d20647ac9075cf8a99d8c8d2fff45eb79228e470210520413546268d2e3ab',
        PAPER / 'reviews/adversarial/FINAL_SEAL.json': '0f359c83ee00704a874efb7fdba88e23d22db32c433170eff7ee60d24c7c7766',
        ROOT / 'rational-check-20261025.json': 'b0f247e05a329b745ff6ca06a5d754c114bb7b6094bc7fa27181a53213cdf910',
        PAPER / 'reviews/scope/cache/primary/morpurgo-web-interface-response.json': '5f5acd0bf35240bd23c51a5983ab77c7302430544fb29899aef4e72627f64f5c',
    }
    for path, expected in pins.items():
        need(digest(path) == expected, 'External root pin: ' + str(path))
    initial = read(ROOT / 'INITIAL_SEAL.json')
    check(initial, PROGRAMME)
    need(initial['prior_inventory_triage_opinion_seen'] is True
         and initial['fourth_blind_family_claim'] is False, 'Honest root exposure')
    table(SOURCES / 'SOURCE_READY_MANIFEST.json', SOURCES)
    table(SOURCES / 'SOURCE_FINAL_MANIFEST.json', SOURCES)
    need(len(read(SOURCES / 'SOURCE_READY_MANIFEST.json')['files']) == 151
         and len(read(SOURCES / 'SOURCE_FINAL_MANIFEST.json')['files']) == 153, 'Exact source envelopes')
    owned = {}
    for lane in ['scope', 'analytic', 'adversarial']:
        folder = PAPER / 'reviews' / lane
        name = 'MANIFEST.json' if lane == 'analytic' else 'FINAL_MANIFEST.json'
        table(folder / name, folder)
        owned[lane] = len(read(folder / name)['files'])
        if lane == 'scope':
            table(folder / 'CACHE_MANIFEST.json', folder)
        if lane == 'analytic':
            table(folder / 'PROTECTED_BINDINGS.json', folder)
        if lane == 'adversarial':
            for group in read(folder / 'INPUT_BINDINGS.json')['groups'].values():
                for row in group:
                    check(row, folder)
    ready = read(SOURCES / 'SOURCE_READY.json')
    record = read(SOURCES / 'record.raw.json')
    assets = ready['all_assets_in_original_order']
    need([item['original_api_file_object'] for item in assets] == record['files'], 'Whole native objects and order')
    need(record['metadata']['version'] == ready['version'] == '1.0.0'
         and record['metadata']['publication_date'] == ready['publication_date'] == '2026-10-13', 'Edition and declared date')
    need(record['created'] == ready['created'] == '2026-10-15T04:00:37.039113+00:00'
         and record['updated'] == ready['updated'], 'Actual timestamps')
    for item in assets:
        body = Path(item['path']).read_bytes()
        native = item['original_api_file_object']
        need(len(body) == item['bytes'] == native['size']
             and sha256(body).hexdigest() == item['sha256'], 'Whole asset size and SHA256')
        need(md5(body).hexdigest() == item['md5']
             and native['checksum'] == 'md5:' + item['md5'], 'Exact native MD5')
    transports = read(SOURCES / 'api-receipts.json')
    need(len(transports) == 5, 'Five actual transports')
    for event in transports:
        need(event['HTTP_status'] == 200 and event['fresh_ordinary_HTTPS'] is True, 'Actual recorded transport')
        check(event['body'], SOURCES)
    aj = Path('/Users/alec/Documents/Math/draft_pr_claimed_solved_800_900_20261012/audits/pr822_30001168/private_sources/Ammann_Jammes_author_20081208.pdf')
    need(digest(aj) == '4449290734e4f634439c93a961623085189c6421ef238e0f5da29ef514a3c717', 'Actual reused AJ author body')
    arithmetic = read(ROOT / 'rational-check-20261025.json')
    need(arithmetic['status'] == 'PASS_EXACT_RATIONAL_FORMULAS'
         and len(arithmetic['all_six_compact_time_rows']) == 6
         and arithmetic['source_code_or_historical_verdict_imported'] is False, 'Actual root exact arithmetic')
    executions = []
    if '--record' in sys.argv:
        out = ROOT / 'custody-recheck-20261025.json'
        need(not out.exists(), 'Receipt already exists')
        python = '/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
        environment = {key: value for key, value in os.environ.items() if key != 'PYTHONOPTIMIZE'}
        for lane, name in [('scope', 'verify_readonly.py'), ('analytic', 'verify_review.py'), ('adversarial', 'verify_review.py')]:
            command = [python, '-B', str(PAPER / 'reviews' / lane / name)]
            run = subprocess.run(command, cwd=PROGRAMME, env=environment, capture_output=True, text=True, timeout=45)
            need(run.returncode == 0, lane + ' read-only verifier: ' + run.stderr)
            data = json.loads(run.stdout)
            need(data['status'] == 'PASS', lane + ' actual result')
            executions.append({'lane': lane, 'command': command, 'exit_code': run.returncode,
                               'stdout': data, 'stderr': run.stderr, 'optimization_environment_removed': True})
    result = {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              'status': 'PASS_ROOT_ORIGINAL_AND_REVIEW_CUSTODY',
              'unique_existing_bindings_rehashed': len(seen), 'lane_owned_payloads': owned,
              'source_ready_bindings': 151, 'source_final_bindings': 153,
              'original_recursive_payloads': 142, 'original_ZIP_containers': 4,
              'recursive_custody_actual_execution': executions,
              'root_complete_exposure_limit_preserved': True,
              'whole_native_objects_dates_order_and_checksums_exact': True,
              'root_arithmetic_receipt_sha256': digest(ROOT / 'rational-check-20261025.json'),
              'helper_sha256': digest(Path(__file__)),
              'source_or_mathematical_programmes_replayed': False,
              'default_invocation_writes': False}
    if '--record' in sys.argv:
        out.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items()
                      if key != 'recursive_custody_actual_execution'}, indent=2))

if __name__ == '__main__':
    main()
