"""Move only the unexpectedly generated CLI skills into this audit folder."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import subprocess

own = Path(__file__).resolve().parent
repo = own.parents[3]
sources = [repo / 'skills', repo / 'docs/skills.md']
destinations = [own / 'generated_cli/skills', own / 'generated_cli/docs/skills.md']
records = []
for source, dest in zip(sources, destinations):
    assert source.exists() and not dest.exists()
    files = sorted(source.rglob('*')) if source.is_dir() else [source]
    files = [p for p in files if p.is_file()]
    assert files
    tracked = subprocess.run(['git','--no-optional-locks','ls-files','--',str(source.relative_to(repo))],cwd=repo,capture_output=True,check=True)
    assert tracked.stdout == b''
    pins = []
    for path in files:
        st = path.stat()
        assert 1791084708 <= st.st_birthtime <= 1791084711
        assert 1791084708 <= st.st_mtime <= 1791084711
        pins.append({'relative': str(path.relative_to(source)) if source.is_dir() else '.',
                     'bytes': st.st_size, 'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
                     'birthtime':st.st_birthtime,'mtime':st.st_mtime})
    dest.parent.mkdir(parents=True,exist_ok=True)
    os.rename(source,dest)
    for pin in pins:
        p = dest/pin['relative'] if pin['relative'] != '.' else dest
        assert p.stat().st_size == pin['bytes']
        assert hashlib.sha256(p.read_bytes()).hexdigest() == pin['sha256']
    assert not source.exists()
    records.append({'source':str(source),'destination':str(dest),'file_pins':pins})
receipt={'schema':'pr50-gws-generated-path-recovery/v1','utc':dt.datetime.now(dt.timezone.utc).isoformat(),
         'actual_pid':os.getpid(),'trigger_argv':['/Users/alec/.nvm/versions/node/v22.16.0/bin/gws','generate-skills','--help'],
         'observed_behavior':'The CLI ignored --help and generated skills/ and docs/skills.md in the cwd.',
         'all_generated_files_retained':True,'outside_generated_files_untouched':True,
         'git_index_refs_and_external_services_not_mutated':True,'moves':records}
(own/'GENERATED_PATH_RECOVERY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'utc':receipt['utc'],'actual_pid':receipt['actual_pid'],'file_counts':[len(x['file_pins']) for x in records],
                  'all_generated_files_retained':True,'outside_generated_files_untouched':True},indent=2))
