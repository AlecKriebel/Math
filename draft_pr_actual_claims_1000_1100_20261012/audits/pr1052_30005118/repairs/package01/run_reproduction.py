#!/usr/bin/env python3
"""Execute the five support commands on wrapped and clean repaired payloads."""
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import stat
import subprocess
import time
import zipfile

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parents[1]
ROOT = AUDIT/'preprint_v1_0'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def utc():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def main():
    scratch = HERE/'private/reproduction'
    require(not scratch.exists(), 'reproduction destination already exists')
    scratch.mkdir(parents=True)
    members = json.loads((ROOT/'SUPPORT_ALLOWLIST.json').read_text())['members']
    shipped = ROOT/'pr1052_support_v1_0.zip'
    runs = []

    def run(surface, cwd, argv):
        start = utc(); mono = time.monotonic()
        proc = subprocess.run(argv, cwd=cwd, capture_output=True, timeout=600)
        item = {'surface': surface, 'argv': argv, 'started_utc': start, 'ended_utc': utc(), 'exit_code': proc.returncode, 'elapsed_seconds': round(time.monotonic()-mono, 3), 'stdout': proc.stdout.decode(), 'stderr': proc.stderr.decode(), 'stdout_sha256': hashlib.sha256(proc.stdout).hexdigest(), 'stderr_sha256': hashlib.sha256(proc.stderr).hexdigest()}
        runs.append(item)
        (HERE/'REPRODUCTION_RECEIPTS.json').write_text(json.dumps({'scope': 'Current repaired package support reproduction and exact metadata-stage controls; no PDF compilation/rendering or new whole/mathematics review.', 'runs': runs}, indent=2)+'\n')
        require(proc.returncode == 0, 'command failed: '+surface+' '+str(argv))
        return proc.stdout

    run('actual_current_candidate', ROOT, ['python3', '-I', '-B', 'verify_support.py', '--archive', 'pr1052_support_v1_0.zip'])
    run('actual_current_candidate_optimized', ROOT, ['python3', '-I', '-B', '-O', 'verify_support.py', '--archive', 'pr1052_support_v1_0.zip'])
    wrapped = scratch/'wrapped'; clean = scratch/'clean'
    for name in members+['zenodo-deposit.json', 'pr1052_support_v1_0.zip', 'pr1052_support_v1_0.zip.sha256']:
        dest = wrapped/name; dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT/name, dest)
    clean.mkdir()
    with zipfile.ZipFile(shipped) as z:
        require(z.namelist() == sorted(members), 'archive not closed over allowlist')
        z.extractall(clean)
    require(not (clean/'zenodo-deposit.json').exists(), 'external descriptor entered clean archive')
    commands = [
        ['python3', '-I', '-B', 'verify_support.py'],
        ['python3', '-I', '-B', 'run_checks.py', '--output', '_runs/fresh.json'],
        ['python3', '-I', '-B', 'test_integrity.py', '--output', '_runs/integrity.json'],
        ['python3', '-I', '-B', 'build_support.py', '--output', '_runs/rebuilt.zip'],
        ['python3', '-I', '-B', 'verify_support.py', '--archive', '_runs/rebuilt.zip']
    ]
    surfaces=[]
    for surface, dest in [('wrapped_exact_payload_copy', wrapped), ('fresh_clean_archive_extraction', clean)]:
        for argv in commands:
            run(surface, dest, argv)
        require((dest/'_runs/rebuilt.zip').read_bytes() == shipped.read_bytes(), surface+' archive bytes changed')
        fresh = json.loads((dest/'_runs/fresh.json').read_text())
        integrity = json.loads((dest/'_runs/integrity.json').read_text())
        (HERE/('FRESH_RUN_'+surface+'.json')).write_text(json.dumps(fresh, indent=2)+'\n')
        (HERE/('INTEGRITY_'+surface+'.json')).write_text(json.dumps(integrity, indent=2)+'\n')
        surfaces.append({'surface': surface, 'all_five_verbatim_readme_commands_exit_zero': True, 'same_zip_bytes': True, 'rebuilt_zip_sha256': sha(dest/'_runs/rebuilt.zip'), 'fresh_checker_runs': len(fresh['runs']), 'integrity_invalid_controls_rejected': integrity['invalid_wrapper_and_path_controls_rejected']})
    controls=[]
    for optimized in [False, True]:
        argv=['python3', '-I', '-B']+(['-O'] if optimized else [])+['negative_controls.py']
        result = json.loads(run('repair_metadata_controls_'+('optimized' if optimized else 'normal'), HERE, argv))
        (HERE/('NEGATIVE_CONTROLS_'+('optimized' if optimized else 'normal')+'.json')).write_text(json.dumps(result, indent=2)+'\n')
        controls.append(result)
    def substance(result):
        return {'all_checks_passed':result['all_checks_passed'], 'accepted':result['accepted_current_metadata_and_strict_two_file_binding_controls'], 'rejections':result['metadata_and_binding_rejections'], 'build_rejections': [{'control':e['control'], 'exit_nonzero':e['exit_code'] != 0, 'archive_not_created':e['archive_not_created']} for e in result['bad_metadata_build_rejections_with_valid_manifest']]}
    require(substance(controls[0]) == substance(controls[1]), 'normal/optimized controls differ substantively')
    # Reconstruct the exact closed archive without importing either shipped builder.
    independent = scratch/'independent.zip'
    with zipfile.ZipFile(independent, 'w', compression=zipfile.ZIP_STORED) as z:
        for name in sorted(members):
            src=clean/name
            require(src.is_file() and not src.is_symlink(), 'not a regular closed payload')
            info=zipfile.ZipInfo(name, date_time=(2026,10,14,0,0,0))
            info.create_system=3
            info.external_attr=(stat.S_IFREG|0o644)<<16
            info.compress_type=zipfile.ZIP_STORED
            z.writestr(info, src.read_bytes())
    require(independent.read_bytes() == shipped.read_bytes(), 'independent closed construction differs')
    summary={'utc':utc(), 'stage':'PENDING_NEW_WHOLE_02', 'publication_ready':False, 'all_issues_resolved':False, 'all_executed_commands_passed':True, 'actual_candidate_strict_wrapped_verification_normal_optimized':True, 'surfaces':surfaces, 'metadata_controls_normal_optimized_substantively_equal':True, 'negative_controls_per_mode':len(controls[0]['metadata_and_binding_rejections'])+len(controls[0]['bad_metadata_build_rejections_with_valid_manifest']), 'independent_closed_archive_bytes_equal':True, 'archive_members':len(members), 'archive_bytes':shipped.stat().st_size, 'archive_sha256':sha(shipped), 'pdf_bytes':(ROOT/'paper.pdf').stat().st_size, 'pdf_sha256':sha(ROOT/'paper.pdf'), 'pdf_compilation_render_or_marker_rerun':False, 'new_math_or_whole_package_review_performed':False}
    (HERE/'REPRODUCTION_SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))


if __name__ == '__main__':
    main()
