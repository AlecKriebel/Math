#!/usr/bin/env python3
"""Compile the independent C++ implementation and hash its complete action stream."""
from pathlib import Path
import subprocess,tempfile,hashlib,json
p=Path(__file__).resolve().parent
with tempfile.TemporaryDirectory() as d:
 exe=Path(d)/'check'
 subprocess.run(['g++','-O3','-std=c++17',str(p/'check_turn_4.cpp'),'-o',str(exe)],check=True)
 process=subprocess.Popen([str(exe),'--stream'],stdout=subprocess.PIPE)
 sha=hashlib.sha256();states=0;result=None
 for line in process.stdout:
  if line.startswith(b'S|'):sha.update(line);states+=1
  else:result=json.loads(line)
 assert process.wait()==0 and result is not None
 expected=json.loads((p/'TURN_4_CHECKS.json').read_text())
 assert states==expected['coaccessible_states']
 for key,value in result.items():assert expected[key]==value
 assert sha.hexdigest()==expected['canonical_action_stream_sha256']
 print(json.dumps({'status':'PASS','stream_states':states,'canonical_action_stream_sha256':sha.hexdigest(),'Cplusplus_counts':result,'all_actions_compared_exactly_before_hashing':True,'scope':'A second exact implementation, not a replacement for the completeness proof or independent mathematical review.'},indent=2,sort_keys=True))
