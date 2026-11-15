#!/usr/bin/env python3
"""Read-only execution of a byte-identical isolated native arithmetic program.
The known Path.write_text receipt sink is captured in memory, never executed.
"""
from pathlib import Path
from unittest.mock import patch
from contextlib import redirect_stdout
from io import StringIO
import runpy,json,sys,hashlib
sys.dont_write_bytecode=True
if len(sys.argv)!=2 or sys.argv[1] not in ['degree_two','wheel','symbolic']:raise RuntimeError('select one bound arithmetic program')
name=sys.argv[1];target=Path(__file__).resolve().parent/'cache/replay-native'/(name+'.py');writes=[];out=StringIO()
def capture(path,data,*args,**kwargs):
 writes.append(str(path));return len(data)
with patch.object(Path,'write_text',capture),redirect_stdout(out):runpy.run_path(str(target),run_name='__main__')
if len(writes)!=(1 if name=='degree_two' else 0):raise RuntimeError('unexpected native receipt sink')
print(json.dumps({'program':name,'program_SHA256':hashlib.sha256(target.read_bytes()).hexdigest(),'captured_write_paths':writes,'filesystem_writes':0,'output':json.loads(out.getvalue())},indent=2,sort_keys=True))
