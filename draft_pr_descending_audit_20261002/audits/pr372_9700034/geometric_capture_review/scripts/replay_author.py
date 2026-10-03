#!/usr/bin/env python3
"""Read-only frozen-author replays in an ignored private copy; preserve all streams."""
from pathlib import Path
import datetime, hashlib, json, shutil, subprocess, sys

HERE = Path(__file__).resolve().parents[1]
SOURCE = HERE.parent / 'snapshot/problems/9700034_sirsn_maximal_routes'
PRIVATE = HERE / 'private'
COPY = PRIVATE / 'author_copy'
STREAMS = PRIVATE / 'replays'
if COPY.exists():
    raise RuntimeError('Preserve existing author_copy; do not overwrite a replay')
shutil.copytree(SOURCE, COPY)
STREAMS.mkdir(exist_ok=True)
records = []
for name in [f'check_turn_{i}.py' for i in range(1,6)] + ['verify_packet.py']:
    argv = [sys.executable, str(COPY/name)]
    if name == 'verify_packet.py':
        argv += ['--source-dir', str(PRIVATE/'sources')]
    start = datetime.datetime.now(datetime.timezone.utc).isoformat()
    proc = subprocess.run(argv, cwd=COPY, capture_output=True)
    stem = name.removesuffix('.py')
    (STREAMS/f'{stem}.stdout').write_bytes(proc.stdout)
    (STREAMS/f'{stem}.stderr').write_bytes(proc.stderr)
    info = {'program':name, 'program_sha256':hashlib.sha256((COPY/name).read_bytes()).hexdigest(),
            'utc_started':start, 'exit_code':proc.returncode,
            'stdout_bytes':len(proc.stdout), 'stderr_bytes':len(proc.stderr),
            'stdout_sha256':hashlib.sha256(proc.stdout).hexdigest(),
            'stderr_sha256':hashlib.sha256(proc.stderr).hexdigest()}
    if name.startswith('check_turn_') and proc.returncode == 0:
        i = int(stem.rsplit('_',1)[1])
        info['byte_exact_frozen_receipt'] = proc.stdout == (COPY/f'TURN_{i}_CHECKS.json').read_bytes()
        info['parsed_math_stream'] = json.loads(proc.stdout)
    elif proc.returncode == 0:
        info['parsed_math_stream'] = json.loads(proc.stdout)
    records.append(info)
    print(json.dumps(info, sort_keys=True))
    if proc.returncode:
        print(proc.stderr.decode(errors='replace'))
        break
result = {'utc_finished':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'source_copy':str(COPY), 'records':records,
          'all_programs_passed':len(records)==6 and all(x['exit_code']==0 for x in records),
          'old_review_programs_executed':False}
(HERE/'AUTHOR_REPLAY_METADATA.json').write_text(json.dumps(result,indent=2)+'\n')
if not result['all_programs_passed']:
    sys.exit(1)
