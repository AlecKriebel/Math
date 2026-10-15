"""SOURCE ONLY: ROOT may execute after reading the complete report and sources.
The hash arguments bind reviewed bytes; they do not prove human approval.
Writes only this family's exclusive closure manifest and its permission modes.
"""
import argparse, datetime as dt, json, os, stat
from custody_checks import F, MANIFEST, SCHEMA, sha, files_and_dirs, verify_results
def main():
    p = argparse.ArgumentParser()
    p.add_argument('--report-sha256', required=True)
    p.add_argument('--verdict-sha256', required=True)
    a = p.parse_args()
    assert not (F/MANIFEST).exists()
    assert sha((F/'REPORT.md').read_bytes()) == a.report_sha256
    assert sha((F/'VERDICT.json').read_bytes()) == a.verdict_sha256
    verify_results()
    files, dirs = files_and_dirs()
    required = {'REPORT.md','VERDICT.json','VIRTUAL_PROOF.md','PRIMARY_READ_LEDGER.json',
                'EARLY_INDEPENDENCE.json','RESEARCH_LOG.md','CONTROL_RESULT.json',
                'SELECTED_INPUT_BINDINGS.json','capture_actual_command.py',
                'virtual_lift_controls.py','verify_selected_inputs.py',
                'custody_checks.py','close_for_ROOT.py','verify_closed_readonly.py','READY.json'}
    assert required <= {p.relative_to(F).as_posix() for p in files}
    rows = []
    for path in files:
        b = path.read_bytes()
        rows.append(dict(path=path.relative_to(F).as_posix(), bytes=len(b), sha256=sha(b), full_mode=0o444))
    result = dict(schema=SCHEMA, root=str(F), created_utc=dt.datetime.now(dt.timezone.utc).isoformat(),
                  actual_closer_pid=os.getpid(), files_count=len(rows), files=rows,
                  self_excluded=MANIFEST, directory_full_mode=0o555,
                  directories=[p.relative_to(F).as_posix() for p in dirs],
                  report_sha256=a.report_sha256, verdict_sha256=a.verdict_sha256,
                  scope='Self-only custody closure; no ROOT acceptance or mathematical truth certified.',
                  ROOT_acceptance_certified=False)
    for path in files: os.chmod(path, 0o444)
    with (F/MANIFEST).open('xb') as h:
        h.write((json.dumps(result, indent=2, sort_keys=True)+'\n').encode()); h.flush(); os.fsync(h.fileno())
    os.chmod(F/MANIFEST, 0o444)
    for path in sorted(dirs, key=lambda x: len(x.parts), reverse=True): os.chmod(path, 0o555)
    print(json.dumps(dict(schema=SCHEMA, actual_pid=os.getpid(), files_count=len(rows),
                         manifest_sha256=sha((F/MANIFEST).read_bytes()),
                         ROOT_acceptance_certified=False), sort_keys=True))
if __name__ == '__main__': main()
