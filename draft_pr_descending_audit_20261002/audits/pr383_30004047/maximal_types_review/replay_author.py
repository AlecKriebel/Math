#!/usr/bin/env python3
"""Private B copy replay after reading code; save full streams, compare all bytes."""
import pathlib,subprocess,hashlib,json,time,os
HERE=pathlib.Path(__file__).resolve().parent
SRC=HERE.parent/'snapshot/unsolved_math_prioritization/attempts/30004047'
PRIVATE=HERE/'private_B_replay'
PRIVATE.mkdir(exist_ok=True)
rows=[]
for turn in (3,4,5):
 name=f'check_turn_{turn}.py'
 data=(SRC/name).read_bytes()
 (PRIVATE/name).write_bytes(data)
 assert (PRIVATE/name).read_bytes()==data
 start=time.time()
 proc=subprocess.run(['python3','-B',name],cwd=PRIVATE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 (PRIVATE/f'turn_{turn}.stdout').write_bytes(proc.stdout)
 (PRIVATE/f'turn_{turn}.stderr').write_bytes(proc.stderr)
 expected=(SRC/f'TURN_{turn}_CHECKS.json').read_bytes()
 assert proc.returncode==0 and not proc.stderr
 assert proc.stdout==expected,(turn,proc.stdout,expected)
 rows.append({'turn':turn,'exit_code':proc.returncode,'checker_sha256':hashlib.sha256(data).hexdigest(),'stdout_sha256':hashlib.sha256(proc.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(proc.stderr).hexdigest(),'full_stdout_byte_equal_frozen_checks':True,'elapsed_seconds':round(time.time()-start,3),'parsed_stdout':json.loads(proc.stdout)})
 result={'status':'PASS','read_before_replay':True,'private_B_copy':True,'full_stdout_compared':True,'turns':rows}
(HERE/'AUTHOR_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
