"""Capture complete future readonly replay return or infrastructure failure."""
from pathlib import Path
import datetime, hashlib, json, os, sys, traceback
D=Path(__file__).resolve().parent
if sys.flags.optimize or not(sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):raise RuntimeError('Use -I -S -B optimize0')
p=D/'INDEPENDENT_COLD02.py';raw=p.read_bytes()
if hashlib.sha256(raw).hexdigest()!='8881549a6b8b742cc7233179a36ffd03f3110ddd837fbf9bd197c2f716c4976c':raise RuntimeError('Independent decoder changed')
if os.statvfs(D).f_bavail*os.statvfs(D).f_frsize<165*1024*1024:raise RuntimeError('Do not expand new world before165MiB measured reserve')
n={'__file__':str(p),'__name__':'controlled_independent_cold'}
exec(compile(raw,str(p),'exec',dont_inherit=True,optimize=0),n)
try:
    v=n['check'](D)
except BaseException as error:
    details={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'traceback':traceback.format_exc(),'partial_complete_cases_not_full_PASS':None,'actual_effects':0}
    tb=error.__traceback__
    while tb:
        if tb.tb_frame.f_code.co_name=='check'and type(tb.tb_frame.f_locals.get('out'))is dict:details['partial_complete_cases_not_full_PASS']=tb.tb_frame.f_locals['out']
        tb=tb.tb_next
    i=1
    while(D/'private'/('CONTROLLED_COLD_FAILURE_'+str(i)+'.json')).exists():i+=1
    with(D/'private'/('CONTROLLED_COLD_FAILURE_'+str(i)+'.json')).open('x')as f:f.write(json.dumps(details,ensure_ascii=True,indent=2)+'\n')
    raise
with(D/'private/OWN17_INDEPENDENT_COLD.json').open('x')as f:f.write(json.dumps(v,ensure_ascii=True,indent=2)+'\n');f.flush();os.fsync(f.fileno())
print(json.dumps({k:x for k,x in v.items()if k!='semantic_original_checks'},sort_keys=True))
