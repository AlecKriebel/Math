"""Read-only check of the exact frozen runtime/configuration and target account/PR."""
import sys, os
expected = {'PATH': '/usr/bin:/bin', 'LC_ALL': 'C', 'LANG': 'C', 'TZ': 'UTC'}
if sys.platform == 'darwin':
    expected['__CF_USER_TEXT_ENCODING'] = '0x' + format(os.getuid(), 'X') + ':0x0:0x0'
if not (sys.flags.ignore_environment and sys.flags.no_site and sys.flags.dont_write_bytecode) or dict(os.environ) != expected:
    raise SystemExit('Exact clean Python startup required')
from pathlib import Path
import datetime, hashlib, json

A = Path(__file__).resolve().parent
C = A.parents[2]
D = A / 'native_publication_integration_plan_20261006/corrected_v4'
inputs_path = D / 'EXECUTION_INPUTS_FROZEN_20261006.json'
inputs_bytes = inputs_path.read_bytes()
inputs_sha = '0dd29832e98382f5d73ddbc93b139e23d9f11d8cc2f60d53fe4050ce01b709bf'
if hashlib.sha256(inputs_bytes).hexdigest() != inputs_sha:
    raise SystemExit('Frozen execution inputs changed')
inputs = json.loads(inputs_bytes)
for pin in inputs['program_files']:
    path = C / pin['path']
    body = path.read_bytes()
    if path.parent != D or len(body) != pin['bytes'] or hashlib.sha256(body).hexdigest() != pin['sha256']:
        raise SystemExit('Reviewed program changed')
sys.path.insert(0, str(D))
import v3_guards as g
from bounded_process import BoundedRunner

g.validate_execution_manifest(inputs, inputs_bytes)
effective = inputs['effective']
g.validate_environment_policy(effective['environment_policy'])
g.require(str(Path(sys.executable).resolve()) == effective['runtime']['python_executable'] and sys.version == effective['runtime']['python_version'], 'Python runtime changed')
for role in ['python', 'git', 'gh']:
    path = Path(effective['runtime'][role + '_executable'])
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    g.require({'bytes': path.stat().st_size, 'sha256': h.hexdigest()} == effective['runtime'][role + '_binary'], 'Runtime binary changed: ' + role)
private_before = g.verify_private_runtime_configuration(effective['environment_policy'])
output = A / 'root_native_runtime_read_probe_20261006'
output.mkdir(exist_ok=False)
runner = BoundedRunner(output, C, effective['process_policy'], effective['environment_policy'])
runtime = effective['runtime']
account, _, account_process = runner.run([runtime['gh_executable'], 'api', 'user', '--jq', '.login'], role='gh', stdout_cap=4096)
g.require(account.strip().decode() == 'AlecKriebel', 'Clean-runtime account differs')
pr_bytes, _, pr_process = runner.run([runtime['gh_executable'], 'pr', 'view', '108', '--repo', 'AlecKriebel/Math', '--json', 'number,state,isDraft,headRefOid,headRefName,baseRefName'], role='gh', stdout_cap=4096)
pr = json.loads(pr_bytes)
g.require(pr == {'number': 108, 'state': 'OPEN', 'isDraft': True, 'headRefOid': '3526d46bf143b08e5055ffa7728c6278e9f958ea', 'headRefName': 'dot/math-30003996', 'baseRefName': 'main'}, 'Live target PR changed')
remote, _, remote_process = runner.run([runtime['git_executable'], 'ls-remote', 'https://github.com/AlecKriebel/Math.git', 'refs/heads/main'], role='git', stdout_cap=4096)
g.require(remote.decode().split()[0] == effective['main_parent'], 'Remote main changed')
private_after = g.verify_private_runtime_configuration(effective['environment_policy'])
g.require(private_before == private_after and inputs_path.read_bytes() == inputs_bytes, 'Private configuration/frozen input changed during probe')
receipt = {'schema': 'pr108-root-clean-runtime-read-probe/v1', 'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'actual_operator_PID': os.getpid(), 'actual_receipt': True, 'fixture': False,
           'execution_inputs_sha256': inputs_sha, 'main_parent': effective['main_parent'],
           'private_configuration_validated_metadata_only_in_output': private_after,
           'private_body_contents_logged_or_copied': False, 'expected_account': 'AlecKriebel', 'live_PR': pr,
           'actual_process_PIDs': [account_process['PID'], pr_process['PID'], remote_process['PID']],
           'read_only_service_operations': 3, 'native_prepare_assess_or_export_called': False,
           'thin_config_or_review_gates_created': False, 'new_central_proof_search_turns': 0}
(output / 'ROOT_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({'actual_operator_PID': os.getpid(), 'account': 'AlecKriebel', 'original_PR_head_unchanged': True,
                  'remote_main_matches': True, 'private_configuration_count': len(private_after), 'native_execution': False}))
