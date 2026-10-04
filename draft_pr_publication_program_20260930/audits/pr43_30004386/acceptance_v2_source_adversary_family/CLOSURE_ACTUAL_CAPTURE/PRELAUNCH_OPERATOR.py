"""Capture a new owned closure check, then seal only after its real exit."""
from pathlib import Path,PurePosixPath
import datetime as dt,hashlib,json,os,stat,subprocess,sys
D=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def utc():return dt.datetime.now(dt.timezone.utc).isoformat()
def main():
    assert __debug__ and os.environ.get('PYTHONOPTIMIZE','') in ('','0')
    dest=D/'CLOSURE_ACTUAL_CAPTURE';dest.mkdir()
    source=D/'validate_before_closure.py';raw=source.read_bytes();op=Path(__file__).read_bytes()
    (dest/'PRELAUNCH_SOURCE.py').write_bytes(raw);(dest/'PRELAUNCH_OPERATOR.py').write_bytes(op)
    argv=['/usr/bin/python3','-B',str(source)]
    rec={'schema':'PR43_V2_SOURCE_ADVERSARY_ACTUAL_OWN_CAPTURE_v1','argv':argv,'cwd':str(D),'actual_parent_pid':os.getpid(),'started_utc':utc(),'prelaunch_source_sha256':sha(raw),'prelaunch_operator_sha256':sha(op),'proposed_foreign_helpers_imported_compiled_executed':False}
    p=subprocess.Popen(argv,cwd=D,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=p.communicate()
    rec.update(actual_child_pid=p.pid,actual_execution=True,completed_after_child_exit=True,exit_code=p.returncode,finished_utc=utc(),source_unchanged=source.read_bytes()==raw)
    for channel,data in [('stdout',out),('stderr',err)]:
        with (dest/(channel+'.bin')).open('xb') as stream:stream.write(data);stream.flush();os.fsync(stream.fileno())
        rec[channel]={'path':channel+'.bin','bytes':len(data),'sha256':sha(data)}
    with (dest/'CAPTURE.json').open('x') as stream:json.dump(rec,stream,indent=2);stream.write('\n');stream.flush();os.fsync(stream.fileno())
    if p.returncode!=0 or not rec['source_unchanged']:
        print(json.dumps(rec,indent=2));return 1
    names=[];dirs=[]
    for file in D.rglob('*'):
        assert not file.is_symlink() and (file.is_file() or file.is_dir())
        name=file.relative_to(D).as_posix()
        assert file.name!='SELF_MANIFEST.json'
        if file.is_file():names.append(name);file.chmod(0o444)
        else:dirs.append(name)
    names.sort();dirs.sort()
    expected={p.as_posix() for n in names for p in PurePosixPath(n).parents if p.as_posix()!='.'}
    assert set(dirs)==expected
    rows=[]
    for name in names:
        data=(D/name).read_bytes();assert stat.S_IMODE((D/name).stat().st_mode)==0o444
        rows.append({'path':name,'bytes':len(data),'sha256':sha(data),'mode':'0444','classification':'This family authored material, private fixture or actual captured project-query evidence','novelty_claim':False})
    inputs=json.loads((D/'CLOSURE_CONTROL_RESULT.json').read_bytes())['external_individually_excluded_inputs']
    obj={'schema':'PR43_NEW_DIFFERENT_V2_ACCEPTANCE_SOURCE_ADVERSARY_SELF_ONLY_CLOSURE_v1','created_utc':utc(),'actual_closure_parent_pid':os.getpid(),'actual_closure_child_pid':p.pid,'files_count':len(rows),'files':rows,'self_excluded':['SELF_MANIFEST.json'],'mode':'0444','directories':dirs,'preparation_manifest_sha256':'11f39e9d890bc1a65efb4fe64bd8bd1612774c746c42c3cafa9883629fe58e91','external_individually_excluded_inputs':inputs,'external_copied_members':[],'review_completion_percent':100,'new_discovery_percent':0,'future_ROOT_or_PR42_approval_certified':False}
    path=D/'SELF_MANIFEST.json'
    with path.open('x') as stream:json.dump(obj,stream,indent=2);stream.write('\n');stream.flush();os.fsync(stream.fileno())
    path.chmod(0o444)
    assert {f.relative_to(D).as_posix() for f in D.rglob('*') if f.is_file()}==set(names)|{'SELF_MANIFEST.json'}
    for row in rows:
        data=(D/row['path']).read_bytes();assert len(data)==row['bytes'] and sha(data)==row['sha256'] and stat.S_IMODE((D/row['path']).stat().st_mode)==0o444
    print(json.dumps({'status':'CLOSED_SOURCE_ONLY','actual_closure_parent_pid':os.getpid(),'actual_closure_child_pid':p.pid,'manifest_bytes':path.stat().st_size,'manifest_sha256':sha(path.read_bytes()),'owned_members':len(rows),'external_individual_inputs':len(inputs),'all_files_literal0444':True},indent=2))
    return 0
if __name__=='__main__':sys.exit(main())
