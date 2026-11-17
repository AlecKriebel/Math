"""Apply one exact private-runtime ignore rule and verify its actual effect once."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat
import subprocess

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
M = P.parent
W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
RUN = P / 'verification/gram-thompson-d4-runtime-sol-20261117'
TEMP = Path('/Users/alec/.codex/tmp/gram-thompson-d4-root-ignore-prerequisite-20261117')
OUT = P / 'verification/root-gram-thompson-d4-runtime-ignore-prerequisite-20261117.json'
line = '/verification/gram-thompson-d4-runtime-sol-20261117/'

def pin(path):
    raw = path.read_bytes()
    return {'path': str(path), 'bytes': len(raw),
            'SHA256': hashlib.sha256(raw).hexdigest(),
            'mode': format(stat.S_IMODE(path.lstat().st_mode), '04o')}

assert not os.path.lexists(RUN) and not os.path.lexists(TEMP) and not OUT.exists()
ignore = P / '.gitignore'
before = ignore.read_bytes()
assert len(before) == 5846
assert hashlib.sha256(before).hexdigest() == '256b1359b16a7f339a93be38430e696ee93a48db784c984d08bb8d736059c1e6'
assert stat.S_IMODE(ignore.stat().st_mode) == 0o644 and before.endswith(b'\n')
assert line not in before.decode().splitlines()
protected = [root/'.git'/leaf for root in (M,W) for leaf in ('HEAD','index','config')]
protected.append(M/'.gitignore')
protected_before = [pin(path) for path in protected]
os.mkdir(TEMP, 0o700)
os.chmod(TEMP, 0o700)
with ignore.open('ab') as stream:
    stream.write(('\n'+line+'\n').encode())
    stream.flush()
    os.fsync(stream.fileno())
assert ignore.read_bytes() == before + ('\n'+line+'\n').encode()
assert stat.S_IMODE(ignore.stat().st_mode) == 0o644
argv = ['/usr/bin/git','--no-optional-locks','-C',str(M),'-c','core.hooksPath=/dev/null',
        '-c','core.fsmonitor=false','-c','core.untrackedCache=false',
        'check-ignore','--no-index','-v','--',str(RUN)+'/']
env = {key:value for key,value in os.environ.items() if not key.startswith('GIT_')}
env['GIT_OPTIONAL_LOCKS'] = '0'
started = datetime.now(timezone.utc).isoformat()
with (TEMP/'stdout.bin').open('xb') as out, (TEMP/'stderr.bin').open('xb') as err:
    os.chmod(TEMP/'stdout.bin', 0o600)
    os.chmod(TEMP/'stderr.bin', 0o600)
    try:
        result = subprocess.run(argv, cwd=M, env=env, stdout=out, stderr=err)
    finally:
        out.flush()
        err.flush()
        os.fsync(out.fileno())
        os.fsync(err.fileno())
record = {'started_UTC':started, 'finished_UTC':datetime.now(timezone.utc).isoformat(),
          'argv':argv, 'exit':result.returncode,
          'stdout':pin(TEMP/'stdout.bin'), 'stderr':pin(TEMP/'stderr.bin')}
with (TEMP/'COMMAND.json').open('x') as stream:
    json.dump(record, stream, indent=2)
    stream.write('\n')
    os.chmod(TEMP/'COMMAND.json', 0o600)
    stream.flush()
    os.fsync(stream.fileno())
assert result.returncode == 0 and (TEMP/'stderr.bin').read_bytes() == b''
source_line, target = (TEMP/'stdout.bin').read_text().rstrip('\n').split('\t')
source, number, pattern = source_line.rsplit(':',2)
assert source == str(ignore.relative_to(M)) and number.isdecimal() and pattern == line
assert target == str(RUN)+'/'
assert [pin(path) for path in protected] == protected_before
assert not os.path.lexists(RUN)
obj = {'UTC':datetime.now(timezone.utc).isoformat(),
       'status':'EXACT_RUNTIME_IGNORE_APPLIED_AND_EFFECTIVE_RUN_ABSENT',
       'root_applied_exact_line':True, 'root_verified_effective_ignore':True,
       'runtime_root':str(RUN), 'runtime_absent':True, 'exact_last_meaningful_line':line,
       'P_ignore':pin(ignore), 'before_ignore_bytes':len(before),
       'before_ignore_SHA256':hashlib.sha256(before).hexdigest(),
       'private_readonly_Git_evidence':pin(TEMP/'COMMAND.json'),
       'all_native_M_W_HEAD_index_config_and_Mroot_ignore_unchanged':True,
       'production_helper_invocations':0, 'future_action_authority':False}
with OUT.open('x') as stream:
    json.dump(obj, stream, indent=2)
    stream.write('\n')
    stream.flush()
    os.fsync(stream.fileno())
print(json.dumps({'status':obj['status'], 'prerequisite':pin(OUT),
                  'ignore':pin(ignore), 'runtime_absent':True}))
