"""Run only with -O or -OO; refusal must precede any source/dependency read."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent;S=ROOT/'source'
body=(S/'bootstrap17.py').read_bytes()
if hashlib.sha256(body).hexdigest()!='5a60e8743ab5dd72e113a75f9af370974a0895bdabd8e68321d58701c947ae94':raise RuntimeError('Bootstrap pin')
ns={'__file__':str(S/'bootstrap17.py'),'__name__':'inert_preload_probe'}
exec(compile(body,str(S/'bootstrap17.py'),'exec',dont_inherit=True,optimize=0),ns)
reads=[]
def deny(self):
    reads.append(str(self));raise RuntimeError('Project read before optimized rejection')
original=Path.read_bytes;Path.read_bytes=deny
try:
    try:ns['load_verified'](S,'623a85eca963527260367dd192bb0373f6a81972179633fa6f219c72a6237803','5a60e8743ab5dd72e113a75f9af370974a0895bdabd8e68321d58701c947ae94')
    except RuntimeError as error:
        if str(error)!='Optimized execution unsupported':raise
    else:raise RuntimeError('Optimized source accepted')
finally:Path.read_bytes=original
if reads or sys.flags.optimize not in {1,2}:raise RuntimeError('Invalid preload test')
out={'optimize':sys.flags.optimize,'status':'PASS_REJECTED_PRELOAD','project_read_attempts':reads,'actual_requests':0,'actual_service_or_Git_mutations':0,'action_matrix_claimed':False}
(ROOT/'private'/('PRELOAD_'+str(sys.flags.optimize)+'.json')).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
