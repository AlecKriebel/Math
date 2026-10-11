"""Authenticate the actual frozen first package review before listed repairs."""
from pathlib import Path
from datetime import datetime, timezone
import gzip, hashlib, json, os, stat, sys

A = Path(__file__).resolve().parent
V = A / 'preprint_adversary_01'
F = A / 'preprint_package_v01'

def now(): return datetime.now(timezone.utc).isoformat()
def require(ok, message):
    if not ok: raise RuntimeError(message)
def pin(path):
    p = Path(path)
    require(p.is_file() and not p.is_symlink(), 'Literal regular file required: '+str(p))
    body = p.read_bytes()
    return dict(path=str(p.absolute()), resolved_path=str(p.resolve()), bytes=len(body),
                sha256=hashlib.sha256(body).hexdigest(), mode=stat.S_IMODE(p.stat().st_mode))
def load(path): return json.loads(Path(path).read_bytes())
def check(row, final_mode=None):
    actual = pin(row['path'])
    require(all(actual[k] == row[k] for k in ('bytes','sha256')), 'Whole-body pin differs: '+row['path'])
    if final_mode is not None: require(actual['mode'] == final_mode, 'Final mode differs')
    return actual
def check_executable(row):
    path = Path(row.get('resolved_path', str(Path(row['path']).resolve())))
    require(path == Path(row['path']).resolve(), 'Executable resolution differs')
    actual = pin(path)
    require(all(actual[k] == row[k] for k in ('bytes','sha256')), 'Resolved executable body differs')
    return actual
def time(value):
    d = datetime.fromisoformat(value)
    require(d.tzinfo is not None, 'Timezone missing')
    return d

def main():
    require(not sys.flags.optimize, 'Optimization forbidden')
    manifest_path = V/'OUTPUT_MANIFEST.json'
    seal_path = V/'CLOSURE_SEAL.json'
    require(pin(manifest_path)['sha256'] == 'c907c417937cbdf1d5b908b790cfdbec6a172a706244330dd84296a0b6eb20b7', 'External manifest anchor differs')
    require(pin(seal_path)['sha256'] == '6c1e8e667d532ccc4232fe327341cd31999f3b3746b54582ba669900e38e9e51', 'External seal anchor differs')
    manifest = load(manifest_path); seal = load(seal_path)
    require(manifest['file_count'] == 153 and seal['literal_total_file_count_including_manifest_and_seal'] == 155, 'Closure size differs')
    expected = {row['relative_path'] for row in manifest['files']} | {'OUTPUT_MANIFEST.json','CLOSURE_SEAL.json'}
    actual_files = sorted(p for p in V.rglob('*') if p.is_file())
    require({str(p.relative_to(V)) for p in actual_files} == expected, 'Literal closure file set differs')
    all_pins = [check(row, 0o444) for row in manifest['files']]
    all_pins += [pin(manifest_path), pin(seal_path)]
    require(all(p['mode'] == 0o444 for p in all_pins), 'Frozen file permission differs')
    directories = [V]+sorted(p for p in V.rglob('*') if p.is_dir())
    require({str(p) for p in directories} == {x['path'] for x in manifest['directories']}, 'Directory inventory differs')
    require(all(not p.is_symlink() and stat.S_IMODE(p.stat().st_mode) == 0o555 for p in directories), 'Frozen directory differs')
    check(seal['manifest'], 0o444)
    require(seal['publication_clearance'] is False and not seal['mandatory_unresolved_issues'], 'Seal verdict differs')

    first = load(F/'FIRST_CANDIDATE_MANIFEST.json')
    require(pin(F/'FIRST_CANDIDATE_MANIFEST.json')['sha256'] == '522fc23022c2975a0d43b66796bc2fa58d95eb4a59b892b835ea034ef78f5a73', 'First candidate anchor differs')
    candidate = [check(row, 0o444) for row in first['files']]
    require(len(candidate) == 23, 'Candidate scope differs')
    receipts = sorted((V/'processes').glob('*/execution.json')) + sorted((V/'portable_replay').glob('*/execution.json'))
    require(len(receipts) == 14, 'Actual native receipt count differs')
    native = []; full_sources = []; stream_checks = []
    for path in receipts:
        result = load(path); request = load(path.parent/'request.json')
        require(all(result[k] == value for k,value in request.items()), 'Prelaunch request/result mismatch')
        outer = path.parent.parent.name == 'processes'
        pid = result['actual_Popen_PID'] if outer else result['actual_child_PID']
        require(isinstance(pid,int) and pid > 0, 'Actual child PID missing')
        start = result['UTC_started'] if outer else result['started_UTC']
        end = result['UTC_completed'] if outer else result['completed_UTC']
        require(time(start) <= time(end), 'Execution timestamp order differs')
        if outer: require(time(result['UTC_prelaunch']) <= time(start), 'Prelaunch order differs')
        failed = outer and path.parent.name == 'authenticate'
        require(result['exit_code'] == (1 if failed else 0), 'Unexpected actual exit status')
        require(Path(result['argv'][0]).is_absolute() and Path(result['cwd']).is_dir(), 'Execution identity incomplete')
        for name in ('stdout','stderr'):
            stream = result[name]; stored = check(stream['stored'],0o444)
            body = gzip.decompress(Path(stored['path']).read_bytes())
            require(len(body) == stream['logical_bytes'] and hashlib.sha256(body).hexdigest() == stream['logical_sha256'], 'Complete stream differs')
            stream_checks.append(dict(receipt=str(path), stream=name, actual_stored_pin=stored,
                                      logical_bytes=len(body), logical_sha256=hashlib.sha256(body).hexdigest()))
        if outer:
            for item in result['sources']:
                actual = check(item['immutable_full_copy'],0o444)
                require(all(actual[k] == item['input'][k] for k in ('bytes','sha256')), 'Actual retained prelaunch source differs')
                full_sources.append(dict(receipt=str(path), historical_input=item['input'], actual_immutable_copy=actual))
            check_executable(result['executable'])
        else:
            source = check(result['source'],0o444); original = check(result['original_source'],0o444)
            require(source['sha256'] == original['sha256'], 'Portable child source differs from ZIP')
            check(result['runner_source'],0o444); check_executable(result['runtime']['executable'])
            require(result['runtime']['optimization'] == 0 and result['runtime']['sympy'] == '1.14.0', 'Runtime control differs')
            full_sources.append(dict(receipt=str(path), actual_executed_source=source, actual_ZIP_source=original))
        native.append(dict(receipt=pin(path), actual_PID=pid, argv=result['argv'], cwd=result['cwd'],
                           started_UTC=start, completed_UTC=end, exit_code=result['exit_code']))
    require(sum(x['exit_code'] != 0 for x in native) == 1, 'Historical failure count differs')
    replay = load(V/'portable_replay/REPLAY_RECEIPT.json')
    require(replay['status'] == 'PASS_ALL_EIGHT_FINITE_CONTROL_SUITES' and len(replay['native_executions']) == 8, 'Actual portable reproduction failed')
    for row in replay['native_executions']:
        require(row['native_execution'] == load(V/'portable_replay'/row['label']/'execution.json'), 'Portable summary is not the actual child receipt')
    verdict = load(V/'VERDICT.json')
    require(not verdict['mandatory_unresolved_issues'] and verdict['publication_clearance'] is False, 'Actual reviewer verdict differs')
    evidence = load(V/'EVIDENCE_CROSSCHECK.json')
    require(evidence['case_count'] == 8 and evidence['leaf_counts'] == {'float':19,'exact_nonfloat':4077}
            and not evidence['floating_differences'], 'Scientific output comparison differs')
    physical = sum(p.stat().st_blocks*512 for p in actual_files+directories)
    require(physical < 20_000_000, 'Namespace capacity exceeded')
    output = dict(UTC=now(), status='PASS_FIRST_WHOLE_PACKAGE_REVIEW_FOR_LISTED_GLOBAL_REPAIRS',
                  actual_ROOT_recorder_PID=os.getpid(), argv=sys.argv, cwd=str(Path.cwd()),
                  recorder_source=pin(__file__), resolved_interpreter=pin(sys.executable),
                  ROOT_accepts_mathematics=True, publication_clearance=False,
                  reviewer_manifest=pin(manifest_path), reviewer_seal=pin(seal_path),
                  exact_frozen_namespace_files=all_pins, directory_count=len(directories), physical_bytes=physical,
                  unchanged_literal_first_candidate=candidate, actual_native_executions=native,
                  actual_full_prelaunch_sources=full_sources, complete_stream_checks=stream_checks,
                  actual_scientific_outputs=dict(control_suites=8,exact_nonfloat_leaves=4077,floating_leaves=19,observed_floating_differences=[]),
                  original_problem_and_scope='Almost-sure recovery of a smooth reversible diffusion tensor and unknown stationary density from one stationary trajectory observed at a fixed positive lag, with known ellipticity/density bounds and smooth bounded connected domain.',
                  ROOT_read_and_adjudication='ROOT fully read REPORT, DERIVATION, READ_LEDGER and VERDICT before closure; rederived the mathematical and classical arguments, then authenticated their frozen bodies. No mandatory mathematical or package issue remains in this first candidate. All four nonmandatory clarifications will be applied before a fresh second reviewer. Source-byte authentication is not a claim to have read every unrelated page in retained primary sources.',
                  global_repairs=['C1 replace the unbundled CRITERIA pointer with the bundled alternative conclusion','C2 fully credit Hansen2008 in both supplementary application and source editions','C3 explicitly define the sample kernel at boundary states by a Borel zero extension; stationary boundary events have probability zero','C4 explicitly restrict the conventional Holder exponent to below one; no change to the strict Sobolev assumption or conclusion'],
                  qualification='Historical launch modes are retained in native receipts; final 0444 modes are separately authenticated. Popen PIDs are actual launcher observations; launcher PIDs/clock origin are self-reports, not independent OS/upstream certification. The genuine failed first flat-ZIP checker and capacity interruption remain retained. No Git/index, PR, Zenodo, tracker or lease mutation.',
                  completion_estimate_percent=dict(mathematics=100,bounded_priority=100,publication_workflow=50))
    with (A/'ROOT_FIRST_PREPRINT_REVIEW_ADJUDICATION.json').open('x') as stream:
        stream.write(json.dumps(output,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(dict(status=output['status'],actual_PID=os.getpid(),files=len(all_pins),
                          actual_native_records=len(native),physical_bytes=physical,publication_clearance=False)))

if __name__ == '__main__': main()
