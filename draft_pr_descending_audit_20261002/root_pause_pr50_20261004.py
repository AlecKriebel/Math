#!/usr/bin/env python3
"""One-shot native shared-window acknowledgement; no Git/index mutation."""
from pathlib import Path
import datetime, hashlib, json, os, stat, subprocess, sys
ROOT = Path('/Users/alec/Documents/Math')
P = ROOT / 'draft_pr_descending_audit_20261002'
OUT = P / 'private_shared_pause_20261004T0408'
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pin(p):
    b = p.read_bytes()
    return {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b), 'mode': stat.S_IMODE(p.stat().st_mode)}
if OUT.exists(): raise RuntimeError('One-shot capture already exists')
OUT.mkdir()
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONHASHSEED='0')
def run(label, args):
    pre = {'utc': now(), 'argv': args, 'cwd': str(ROOT), 'program': pin(Path(__file__)), 'environment_overrides': {'PYTHONDONTWRITEBYTECODE':'1', 'PYTHONHASHSEED':'0'}}
    (OUT / (label + '.preexecution.json')).write_text(json.dumps(pre, indent=2)+'\n')
    proc = subprocess.run(args, cwd=ROOT, env=env, capture_output=True)
    (OUT / (label + '.stdout')).write_bytes(proc.stdout)
    (OUT / (label + '.stderr')).write_bytes(proc.stderr)
    rec = dict(pre, completed_utc=now(), exit_status=proc.returncode, stdout_bytes=len(proc.stdout), stdout_sha256=hashlib.sha256(proc.stdout).hexdigest(), stderr_bytes=len(proc.stderr), stderr_sha256=hashlib.sha256(proc.stderr).hexdigest())
    (OUT / (label + '.json')).write_text(json.dumps(rec, indent=2)+'\n')
    if proc.returncode: raise RuntimeError(label + ' native failure')
    return proc.stdout
branch = run('branch', ['git','branch','--show-current']).decode().strip()
head = run('head', ['git','rev-parse','HEAD']).decode().strip()
remote = run('remote', ['git','ls-remote','origin','refs/heads/main']).decode().split()[0]
staged = run('staged', ['git','diff','--cached','--raw','-z'])
index = run('index', ['git','ls-files','--stage','-z'])
dirty = run('dirty_tracked', ['git','status','--porcelain=v1','-z','--untracked-files=no'])
assert branch == 'main' and head == remote and not staged
dirty_pins = {}
for record in dirty.decode().split('\0'):
    if record:
        path = ROOT / record[3:]
        if path.is_file(): dirty_pins[record[3:]] = pin(path)
receipt = {'utc':now(), 'status':'SHARED_PR50_EXACT_HEAD_MERGE_WINDOW_PAUSED', 'branch':branch, 'local_main':head, 'remote_main':remote, 'all_staged_path_count':0, 'entire_index_sha256':hashlib.sha256(index).hexdigest(), 'dirty_tracked_body_mode_pins_before_status_acknowledgement':dirty_pins, 'python':sys.version, 'python_executable':sys.executable, 'no_git_or_index_writes':True, 'program':pin(Path(__file__))}
(OUT / 'PAUSE_ACKNOWLEDGEMENT.json').write_text(json.dumps(receipt, indent=2)+'\n')
status_path = P / 'SHARED_GIT_WINDOW_STATUS.json'
status = json.loads(status_path.read_text())
status.update({'utc':now(), 'shared_git_writes_paused':True, 'reason':'Incoming ascending review requests PR50 exact-head merge, native queue acceptance and final scoped checkpoint; independent native main/remote and whole empty-index verification passed.', 'paused_for':'PR50 exact-head merge, native acceptance mirror and final scoped checkpoint', 'resume_on':'Explicit ascending completion/release followed by independent exact-head native readback', 'local_main_at_pause':head, 'remote_main_at_pause':remote, 'all_staged_path_count':0, 'owned_staged_paths':[], 'entire_index_sha256_at_pause':hashlib.sha256(index).hexdigest(), 'native_pause_capture_directory':str(OUT), 'outbound_message_sent':False, 'descending_git_checkpoint_preparing':False, 'descending_mathematical_readonly_review_continues':True, 'dirty_tracked_bodies_modes_frozen_after_acknowledgement':True})
status_path.write_text(json.dumps(status, indent=2)+'\n')
with (P / 'RESEARCH_LOG.md').open('a') as f:
    f.write('\n### '+now()+' — PR50 exclusive shared Git window acknowledged\n\nNative main and remote both '+head+'; entire index empty with SHA-256 '+hashlib.sha256(index).hexdigest()+'. Shared Git/index/queue/history writers paused and dirty tracked bodies/modes held stable after this acknowledgement. PR344 read-only proof adjudication and own untracked evidence continue. PR344 mathematical verification remains 65% provisional; publication workflow 16%. No outbound chat message sent.\n')
print(json.dumps({'status':receipt['status'], 'main':head, 'index_sha256':receipt['entire_index_sha256'], 'capture':str(OUT)}, indent=2))
