"""Own review-family closure/readback support, never imports production sources."""
from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,math,stat
F=Path(__file__).resolve().parent;R=F.parents[3]
NAME='SELF_MANIFEST.json'
def need(v,m):
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def parse(b):
    def pairs(items):
        d={}
        for k,v in items:need(k not in d,'duplicate JSON');d[k]=v
        return d
    def floating(v):x=float(v);need(math.isfinite(x),'nonfinite JSON');return x
    return json.loads(b,object_pairs_hook=pairs,parse_float=floating,parse_constant=lambda v:(_ for _ in ()).throw(ValueError(v)))
def clock(v):
    t=dt.datetime.fromisoformat(v.replace('Z','+00:00'));need(t.tzinfo is not None and t.utcoffset()==dt.timedelta(0),'UTC');return t
def row(p):
    need(p.is_absolute() and p.is_relative_to(R),'bound regular path')
    for x in [p,*p.parents]:need(not x.is_symlink(),'no symlink ancestor')
    need(stat.S_ISREG(p.lstat().st_mode),'regular full body');b=p.read_bytes()
    return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode))
def topology():
    files={};dirs=set()
    for p in F.rglob('*'):
        need(not p.is_symlink(),'symlink forbidden');n=p.relative_to(F).as_posix()
        if p.is_file():files[n]=row(p)
        else:need(p.is_dir(),'special file forbidden');dirs.add(n)
    expected={q.as_posix() for n in files for q in PurePosixPath(n).parents if q.as_posix()!='.'}
    need(dirs==expected,'no extra empty directory');return files,dirs
def check_external():
    ext=parse((F/'EXTERNAL_BINDINGS.json').read_bytes());need(type(ext['files']) is list,'complete external table');seen=set()
    for z in ext['files']:
        need(set(z)=={'path','bytes','sha256','full_mode'} and type(z['bytes']) is int and type(z['full_mode']) is int,'full typed external row');need(z['path'] not in seen,'unique external binding');seen.add(z['path']);need(row(R/z['path'])==z,'entire external body/fullmode changed')
    root=parse((R/ext['nested_fixed_table']['path']).read_bytes())
    need(len(root['normalized_complete_fixed_bindings'])==ext['nested_fixed_table_count']==3229,'nested fixed count')
    for z in root['normalized_complete_fixed_bindings']:need(row(R/z['path'])==z,'nested whole full body/mode')
    S=F.parent/'acceptance_preparation_family_v2'
    old=parse((S/ext['nested_old_source_table']).read_bytes())
    for z in old['files']:need(row(R/z['path'])==z,'complete old unclosed full body/mode')
    d=parse((S/ext['nested_closed48_history_table']).read_bytes())
    for z in d['closed_history_fixed_bindings']:need(row(R/z['path'])==z,'complete fixed old48 history')
    return len(seen)
def check_captures():
    names={'independent_controls_actual':1,'independent_controls_v2_actual':1,'independent_controls_v3_actual':0,'fixed_source_custody_actual':0}
    out=[]
    for name,code in names.items():
        folder=F/name;cap=parse((folder/'CAPTURE.json').read_bytes());pre=cap['prelaunch']
        need(cap['actual_execution'] is True and cap['completed'] is True and type(cap['pid']) is int and cap['pid']>0 and type(cap['exit_code']) is int and cap['exit_code']==code,'complete actual private child')
        need(pre==parse((folder/'PRELAUNCH.json').read_bytes()) and cap['argv']==pre['argv'] and cap['cwd']==str(F)==pre['cwd'] and cap['stdin_supplied'] is False,'literal own argv/cwd/prelaunch')
        need(clock(pre['created_utc'])<=clock(cap['started_utc'])<=clock(cap['finished_utc'])<=dt.datetime.now(dt.timezone.utc),'actual captured clocks')
        need(sha((folder/'PRELAUNCH_SOURCE.py').read_bytes())==cap['source_sha256']==pre['source_sha256'] and sha((folder/'PRELAUNCH_OPERATOR.py').read_bytes())==cap['operator_sha256']==pre['operator_sha256'],'entire private prelaunch sources')
        need(cap['source_unchanged'] is True and cap['operator_unchanged'] is True,'actual launch source unchanged')
        for key in ['stdout','stderr']:
            z=cap[key];body=(folder/z['path']).read_bytes();need(type(z['bytes']) is int and len(body)==z['bytes'] and sha(body)==z['sha256'],'whole captured stream')
        need((folder/'stderr.bin').read_bytes()==b'' if code==0 else bool((folder/'stderr.bin').read_bytes()),'whole success/failure stderr preserved')
        out.append(dict(name=name,pid=cap['pid'],exit_code=cap['exit_code']))
    return out
