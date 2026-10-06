"""Record actual offline fixture and syntax checks; never run the real preparer."""
from pathlib import Path
import ast, datetime, hashlib, json, os, subprocess, sys
D = Path(__file__).resolve().parent
records = []
def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(data):
    return hashlib.sha256(data).hexdigest()
def main():
    outdir = D / ('offline_fixture_receipts_' + datetime.datetime.now(datetime.timezone.utc).strftime('%H%M%S'))
    outdir.mkdir(exist_ok=False)
    for name in ['OFFLINE_FIXTURE_PROCESS_JOURNAL.json', 'OFFLINE_FIXTURE_RESULTS.json']:
        if (D / name).exists():
            (outdir / ('PREVIOUS_' + name)).write_bytes((D / name).read_bytes())
    for label, options in [('normal', []), ('optimized', ['-O'])]:
        argv = [sys.executable, '-E', '-B', *options, '-m', 'unittest', '-v', 'test_review_bundle']
        start = now()
        process = subprocess.Popen(argv, cwd=D, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = process.communicate()
        (outdir / (label + '.stdout.bin')).write_bytes(out)
        (outdir / (label + '.stderr.bin')).write_bytes(err)
        records.append({'label': label, 'argv': argv, 'cwd': str(D), 'PID': process.pid,
                        'UTC_start': start, 'UTC_end': now(), 'exit_code': process.returncode,
                        'stdout_bytes': len(out), 'stdout_sha256': sha(out), 'stderr_bytes': len(err),
                        'stderr_sha256': sha(err), 'fixture_only': True,
                        'stdout_file': outdir.name + '/' + label + '.stdout.bin',
                        'stderr_file': outdir.name + '/' + label + '.stderr.bin',
                        'native_assess_executed': False, 'real_prepare_executed': False})
        (D / 'OFFLINE_FIXTURE_PROCESS_JOURNAL.json').write_text(json.dumps({'actual_operator_PID': os.getpid(), 'records': records}, indent=2) + '\n')
        (outdir / 'PROCESS_JOURNAL.json').write_bytes((D / 'OFFLINE_FIXTURE_PROCESS_JOURNAL.json').read_bytes())
        if process.returncode:
            raise RuntimeError(err.decode())
    syntax = []
    for name in ['collect_context.py', 'prepare_review_bundle.py', 'test_review_bundle.py', 'run_offline_checks.py', 'seal_artifacts.py']:
        data = (D / name).read_bytes()
        compile(ast.parse(data, filename=name), name, 'exec')
        syntax.append({'path': name, 'bytes': len(data), 'sha256': sha(data), 'AST_compile_passed': True})
    result = {'schema': 'pr108-native-plan-offline-fixtures/v1', 'UTC': now(), 'actual_operator_PID': os.getpid(),
              'fixture_tests_per_mode': 13, 'normal_and_optimized_passed': True, 'syntax_pins': syntax,
              'real_native_integration_executed': False, 'real_native_assess_executed': False,
              'publication_executed': False, 'fixtures_are_not_real_runtime_evidence': True}
    (D / 'OFFLINE_FIXTURE_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
    (outdir / 'RESULTS.json').write_bytes((D / 'OFFLINE_FIXTURE_RESULTS.json').read_bytes())
    print(json.dumps(result))
if __name__ == '__main__':
    main()
