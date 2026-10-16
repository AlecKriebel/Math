"""Recover the completed exact checkpoint from the retained argv-size failure.

Use literal NUL-delimited pathspec stdin, preserving the original checkpoint.
"""
from pathlib import Path
import hashlib,json,os,stat,subprocess
P=Path(__file__).resolve().parents[1];R=P.parent;A=P/'audits/pr45_9900007'
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
    assert __debug__ and git('branch','--show-current')==b'main\n'and not git('diff','--cached','--name-only')
    cp=P/'checkpoints/CHECKPOINT_20261003_0441.json';record=json.loads(cp.read_bytes())
    assert record['completed_count']==35 and record['main_before']==git('rev-parse','HEAD').decode().strip()
    names=set()
    for z in record['owned_files']:
        p=R/z['path'];assert p.is_file()and not p.is_symlink()
        b=p.read_bytes();assert len(b)==z['bytes']and sha(b)==z['sha256']and stat.S_IMODE(p.stat().st_mode)==z['observed_full_mode']
        names.add(z['path'])
    for p in [cp,Path(__file__),P/'checkpoints/checkpoint_20261003_0441.py',P/'checkpoints/stage_checkpoint_20261003_0441_v2.py']:
        names.add(p.relative_to(R).as_posix())
    for capname in ['root_checkpoint_0441_actual_capture','root_checkpoint_0441_v2_actual_capture']:
        for p in (A/capname).iterdir():
            assert p.is_file() and not p.is_symlink();names.add(p.relative_to(R).as_posix())
    foreign={z['path']for z in record['foreign_dirty_before']};assert not foreign&names
    pathspec=b''.join(n.encode()+b'\0'for n in sorted(names))
    subprocess.run(['git','add','-f','--pathspec-from-file=-','--pathspec-file-nul'],cwd=R,input=pathspec,check=True)
    staged={n for n in git('diff','--cached','--name-only','-z').decode().split('\0')if n}
    assert staged<=names and not staged&foreign
    entries={}
    for row in git('ls-files','--stage','-z').decode().split('\0'):
        if row:
            fields,n=row.split('\t');mode,oid,stage=fields.split()
            if n in staged:assert stage=='0'and mode in{'100644','100755'};entries[n]=(mode,oid)
    assert set(entries)==staged
    ordered=sorted(staged);payload=b''.join((entries[n][1]+'\n').encode()for n in ordered)
    process=subprocess.Popen(['git','cat-file','--batch'],cwd=R,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    data,err=process.communicate(payload);assert process.returncode==0 and err==b''
    offset=0
    for n in ordered:
        end=data.index(b'\n',offset);oid,kind,size=data[offset:end].decode().split();assert oid==entries[n][1]and kind=='blob'
        count=int(size);start=end+1;body=data[start:start+count];assert data[start+count:start+count+1]==b'\n';offset=start+count+1
        assert body==(R/n).read_bytes(),n
    assert offset==len(data)and git('rev-parse','HEAD').decode().strip()==record['main_before']
    print(json.dumps({'status':'PASS_EXACT_COMPLETED_CHECKPOINT_STDIN_STAGE','actual_pid':os.getpid(),'main_before':record['main_before'],
        'owned':len(names),'staged':len(staged),'all_staged_bodies_modes_and_exact_index_scope_verified':True,'foreign_staged':0,
        'completed':35,'completion_percent':35/180*100,'initial_argument_list_failure_preserved':True,'actual_blob_batch_pid':process.pid}))
if __name__=='__main__':main()
