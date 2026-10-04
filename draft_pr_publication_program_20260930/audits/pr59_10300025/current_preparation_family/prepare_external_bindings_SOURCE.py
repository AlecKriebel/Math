"""Bind completed external evidence in place. SOURCE, no Git/remote/code replay."""
from pathlib import Path
import json
import hashlib
import stat
import datetime
import os

N=Path(__file__).absolute().parent
A=N.parent
A45=A.parent/'pr45_9900007'


def ref(p):
    s=p.lstat()
    if p.is_symlink() or not stat.S_ISREG(s.st_mode):raise ValueError('Regular external body required')
    b=p.read_bytes();t=p.lstat()
    if (s.st_ino,s.st_mode,s.st_size,s.st_mtime_ns,s.st_ctime_ns)!=(t.st_ino,t.st_mode,t.st_size,t.st_mtime_ns,t.st_ctime_ns):raise ValueError('Changed during read')
    return {'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'full_mode_07777':format(stat.S_IMODE(s.st_mode),'04o')}


def main():
    allfiles={};all_dirs={};families=[]
    spec=[('original_preparation_family','ROOT_MANIFEST.json','e3c0c68005b4ff86b933e9d42fd7d5310b1d927d8800e12516805d5cdaf06150',140,8132,8244),('countable_conjugacy_adversary_family','ROOT_MANIFEST.json','b5182b62259b2bfcb841e0777d524adbbf48df4f9275fa9b0984dc4547a5754e',58,8353,8464),('exhaustion_conjugacy_adversary_family','SELF_MANIFEST.json','9a7055ffa774b03e82d146496e7477a20048cfdfe317c88722865f0626a02ce7',22,8576,8717)]
    for name,mname,sha,count,closer,reader in spec:
        q=A/name;m=ref(q/mname)
        if m['sha256']!=sha:raise ValueError('Exact genuine closed manifest')
        rows=[ref(p) for p in sorted(q.rglob('*')) if p.is_file()]
        if len(rows)!=count or any(z['full_mode_07777']!='0444' for z in rows):raise ValueError('Exact closed family domain and modes')
        md=json.loads((q/mname).read_bytes())
        if 'entries' in md:
            for z in md['entries']:
                actual=ref(q/z['path'])
                if actual['bytes']!=z['bytes'] or actual['sha256']!=z['sha256'] or actual['full_mode_07777']!=z['mode_07777']:raise ValueError('Complete manifest body/mode join')
            if set(md['domain'])|{mname}!={str(Path(z['path']).relative_to(q)) for z in rows}:raise ValueError('Complete closed manifest topology')
        else:
            index=json.loads((q/'INDEX.json').read_bytes())
            if ref(q/'INDEX.json')['sha256']!=md['index_sha256']:raise ValueError('Exhaustion fixed INDEX join')
            for name2,z in index['files'].items():
                actual=ref(q/name2)
                if actual['bytes']!=z['bytes'] or actual['sha256']!=z['sha256'] or int(actual['full_mode_07777'],8)!=z['mode_07777']:raise ValueError('Exhaustion complete body/mode join')
            if set(index['files'])|{'INDEX.json','READY.json',mname}!={str(Path(z['path']).relative_to(q)) for z in rows}:raise ValueError('Exhaustion exact22 topology')
        for z in rows:allfiles[z['path']]=z
        for p in [q]+sorted(p for p in q.rglob('*') if p.is_dir()):
            if p.is_symlink():raise ValueError('No symlink directory')
            all_dirs[str(p)]={'path':str(p),'full_mode_07777':format(stat.S_IMODE(p.stat().st_mode),'04o')}
        families.append({'family':name,'files':count,'genuine_manifest':m,'ROOT_closer_pid':closer,'ROOT_reader_pid':reader,'source_custody_not_new_scientific_credit':True})
    needed={8132,8244,8353,8464,8576,8717};caps={}
    for p in A45.glob('*/CAPTURE.json'):
        c=json.loads(p.read_bytes())
        if c.get('pid') in needed:
            if c['pid'] in caps:raise ValueError('Unique actual ROOT capture')
            caps[c['pid']]=(p,c)
    if set(caps)!=needed:raise ValueError('All six actual ROOT CAPs')
    capture_rows=[]
    for pid in sorted(caps):
        p,c=caps[pid];q=p.parent
        if not c['actual_execution'] or not c['completed'] or c['exit_code']!=0 or not c['operator_unchanged']:raise ValueError('Actual complete successful ROOT child')
        if {v.name for v in q.iterdir()}!={'CAPTURE.json','prelaunch_operator.py','stdout.bin','stderr.bin'}:raise ValueError('Exact CAP4 topology')
        if ref(q/'prelaunch_operator.py')['sha256']!=c['operator_sha256']:raise ValueError('Actual prelaunch whole operator')
        for key in ['stdout','stderr']:
            z=ref(q/(key+'.bin'))
            if z['sha256']!=c[key]['sha256'] or z['bytes']!=c[key]['bytes']:raise ValueError('Complete actual stream')
        for v in sorted(q.iterdir()):z=ref(v);allfiles[z['path']]=z
        all_dirs[str(q)]={'path':str(q),'full_mode_07777':format(stat.S_IMODE(q.stat().st_mode),'04o')}
        capture_rows.append({'pid':pid,'metadata':ref(p),'started_utc':c['started_utc'],'finished_utc':c['finished_utc'],'argv':c['argv'],'cwd':c['cwd'],'completed':True,'exit_code':0})
    science=ref(A/'ROOT_SCIENTIFIC_ADJUDICATION_20261003.json')
    if science['bytes']!=4867 or science['sha256']!='38ba74d0ebbbf7dbdc223d9b09d57d87ff79c3aa0992e5e0f96bb0905da3c779':raise ValueError('Exact ROOT scientific receipt')
    allfiles[science['path']]=science
    out={'schema':'pr59-current-completed-external-bindings/v1','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_SOURCE_binder_pid':os.getpid(),'families':families,'files':[allfiles[k] for k in sorted(allfiles)],'directories':[all_dirs[k] for k in sorted(all_dirs)],'actual_ROOT_CAP4_sets':capture_rows,'ROOT_scientific_adjudication':science,'new_current_ROOT_closure_or_approval_claimed':False,'no_bodies_copied_by_this_binder':True}
    with (N/'EXTERNAL_BINDINGS.json').open('x') as f:f.write(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS_COMPLETED_EXTERNAL_BODY_MODE_TOPOLOGY_AND_CAP_BINDINGS','actual_pid':os.getpid(),'families':len(families),'external_files':len(allfiles),'external_directories':len(all_dirs),'actual_prior_CAP4_sets':len(caps)},indent=2))


if __name__=='__main__':main()
