"""Replay the complete finite evidence, comparing all output and exit codes."""
import json,subprocess,sys
from pathlib import Path
p=Path(__file__).resolve().parent
data=json.loads((p/'REPLAY_RESULTS.json').read_text())
mutations=['prime_obstruction','fourth_obstruction','inverse','degree_drop','mahler','relative_log','relative_height']
expected=[]
for opt in [[],['-O']]:
 for script in ['verify_exact.py','verify_conversion.py','verify_regressions.py']:expected.append(['python3',*opt,script])
 for mutation in mutations:expected.append(['python3',*opt,'verify_regressions.py','--mutation',mutation])
if [r['command'] for r in data['runs']]!=expected:raise RuntimeError('missing, extra or reordered commands')
recorded_json=(p/'exact_checks.json').read_bytes()
for item in data['runs']:
 command=item['command']
 mode='optimized' if '-O' in command else 'normal'
 if item['mode']!=mode:raise RuntimeError('mode mismatch')
 result=subprocess.run([sys.executable,*command[1:]],cwd=p,capture_output=True,text=True)
 stderr=result.stderr.replace(str(p),'PACKAGE')
 if (result.returncode,result.stdout,stderr)!=(item['returncode'],item['stdout'],item['stderr']):raise RuntimeError('full replay mismatch: '+repr(command))
 is_mutation='--mutation' in command
 if is_mutation and (result.returncode==0 or 'mathematical regression failed:' not in stderr):raise RuntimeError('mutation not detected')
 if not is_mutation and result.returncode!=0:raise RuntimeError('positive test failed')
 if 'verify_exact.py' in command:
  if json.loads(result.stdout)!=json.loads(recorded_json):raise RuntimeError('stdout/recorded JSON mismatch')
  if (p/'exact_checks.json').read_bytes()!=recorded_json:raise RuntimeError('JSON bytes changed')
print(json.dumps({'status':'PASS','complete_command_replays':len(expected),'mathematical_mutations':2*len(mutations),'stdout_stderr_exit_codes_equal':True,'recorded_json_bytes_preserved':True},indent=2))
