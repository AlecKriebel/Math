"""Capture one requested ordinary checkpoint-helper invocation, without modifying it."""
import datetime, hashlib, json, os
from pathlib import Path
import subprocess, sys, time

P = Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
OWN = P/'verification/checkpoint-native140-correctedstage-rieszcopy-20261117'
HELPER = P/'scripts/checkpoint_subtree.py'
assert sys.argv[1:] in (['dry-run'],['push'])
mode = sys.argv[1]
name = 'DRY_RUN' if mode == 'dry-run' else 'PUSH'
before = HELPER.read_bytes()
pin = dict(bytes=len(before),SHA256=hashlib.sha256(before).hexdigest(),lines=len(before.splitlines()))
guard = json.loads((OWN/'GUARDS_BEFORE.json').read_bytes())
assert pin['SHA256'] == guard['helper']['SHA256'] and pin['lines'] == 94
active = []
excludes = []
for dirname in ['hafnian-retract-stage-corrected-audit-sol-20261117','hafnian-retract-stage-audit-continuation-sol-20261117','hafnian-retract-production-prepare-sol-20261117','hafnian-retract-production-audit-sol-20261117',OWN.name]:
    relative = 'verification/'+dirname
    path = P/relative
    exists = os.path.lexists(path)
    regular = path.is_dir() and not path.is_symlink() if exists else False
    active.append(dict(path=relative,exists=exists,regular_directory=regular))
    if exists:
        assert regular
        excludes.append(relative)
assert 'verification/'+OWN.name in excludes
argv = [sys.executable,'-B',str(HELPER)]
if mode == 'dry-run':
    argv.append('--dry-run')
else:
    adoption = json.loads((OWN/'DRY_REVIEW.json').read_bytes())
    assert adoption['status'] == 'APPROVED_FOR_ORDINARY_SCOPED_PUSH' and adoption['expected_parent'] == '386463ab847f283920e746a48f52079ac8b3d735'
    argv.append('Checkpoint native tracker 140, corrected private stage, Riesz page review and partial K3 progress')
argv += ['--exclude-path='+p for p in excludes]
env = dict(os.environ,PATH='/usr/bin:/bin:/usr/sbin:/sbin',GIT_OPTIONAL_LOCKS='0',GIT_CONFIG_COUNT='2',GIT_CONFIG_KEY_0='core.hooksPath',GIT_CONFIG_VALUE_0='/dev/null',GIT_CONFIG_KEY_1='core.fsmonitor',GIT_CONFIG_VALUE_1='false')
for key in ('GIT_DIR','GIT_WORK_TREE','GIT_INDEX_FILE','GIT_COMMON_DIR','GIT_OBJECT_DIRECTORY','GIT_ALTERNATE_OBJECT_DIRECTORIES'):
    env.pop(key,None)
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
tick = time.monotonic()
with (OWN/(name+'.stdout')).open('xb') as out,(OWN/(name+'.stderr')).open('xb') as err:
    completed = subprocess.run(argv,cwd=P,env=env,stdout=out,stderr=err,check=False,timeout=300)
receipt = dict(schema='one-scoped-checkpoint-helper-invocation-v1',mode=mode,argv=argv,cwd=str(P),started_UTC=start,finished_UTC=datetime.datetime.now(datetime.timezone.utc).isoformat(),elapsed_seconds=time.monotonic()-tick,exit_code=completed.returncode,stdout_bytes=(OWN/(name+'.stdout')).stat().st_size,stderr_bytes=(OWN/(name+'.stderr')).stat().st_size,helper=pin,helper_unchanged=HELPER.read_bytes()==before,helper_full_source_personally_read=True,active_exclusions_discovered_immediately_before_invocation=active,excluded_actual_directories=excludes,internal_isolated_index=True,external_GIT_DIR_override=False,native_protected_boundary='HEAD/index/config/local branch heads; remote-tracking refs/FETCH_HEAD/object additions allowed by root clarification',ordinary_nonforce_push_only=mode=='push')
with (OWN/(name+'.invocation.json')).open('x') as stream:
    json.dump(receipt,stream,indent=2)
    stream.write('\n')
if completed.returncode == 0:
    source = P/'verification'/('checkpoint-subtree-dry-run-20261025.json' if mode=='dry-run' else 'PUSH_RECEIPT.json')
    with (OWN/(name+'.receipt.json')).open('xb') as stream:
        stream.write(source.read_bytes())
print(json.dumps(receipt))
raise SystemExit(completed.returncode)
