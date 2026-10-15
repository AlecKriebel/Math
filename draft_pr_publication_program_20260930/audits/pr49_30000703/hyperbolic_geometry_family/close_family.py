#!/usr/bin/python3
"""ROOT invokes --close only after this child has exited; --verify is read-only."""
import argparse,datetime,hashlib,json,os,pathlib,stat
root=pathlib.Path(__file__).resolve().parent
manifest=root/'SELF_MANIFEST.json'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def captures():
    rows=[]
    for p in sorted(root.glob('*_capture/CAPTURE.json')):
        c=json.loads(p.read_bytes());folder=p.parent
        pre=json.loads((folder/'PRELAUNCH.json').read_bytes())
        assert c['schema']=='actual_command_completed_v1' and pre['schema']=='actual_command_prelaunch_v1'
        assert c['capture_completed'] is True and c['returncode']==0 and type(c['child_pid']) is int and c['child_pid']>0
        assert c['operator_pid']==pre['operator_pid'] and c['argv']==pre['argv'] and c['cwd']==pre['cwd']
        assert sha(folder/'PRELAUNCH.json')==c['prelaunch']['sha256']
        assert sha(folder/'prelaunch_operator.py')==pre['operator']['sha256']==pre['operator_copy']['sha256']
        assert pre['prelaunch_utc']<=c['started_utc']<=c['completed_utc']
        for n in ['stdout','stderr']:
            q=folder/(n+'.bin');assert sha(q)==c[n]['sha256'] and q.stat().st_size==c[n]['bytes']
        for r in pre['sources']:
            q=pathlib.Path(r['copied']['path']);assert sha(q)==r['copied']['sha256']==r['original']['sha256'] and q.stat().st_size==r['copied']['bytes']==r['original']['bytes']
        rows.append({'path':str(p.relative_to(root)),'child_pid':c['child_pid'],'returncode':c['returncode'],'capture_sha256':sha(p)})
    return rows
def inventory():
    dirs=[];files=[]
    for p in sorted(root.rglob('*')):
        assert not p.is_symlink(),str(p)
        rel=str(p.relative_to(root))
        if p.is_dir():dirs.append({'path':rel,'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')})
        elif p.is_file():
            if p==manifest:continue
            files.append({'path':rel,'bytes':p.stat().st_size,'sha256':sha(p),'mode':format(stat.S_IMODE(p.stat().st_mode),'04o')})
        else:raise AssertionError(str(p))
    return files,dirs
def verify():
    d=json.loads(manifest.read_text())
    assert d['schema']=='pr49-hyperbolic-family-self-only/v1'
    files,dirs=inventory()
    assert files==d['payload_files'] and dirs==d['directories']
    assert all(f['mode']=='0444' for f in files)
    assert stat.S_IMODE(manifest.stat().st_mode)==0o444
    assert len(list(root.rglob('*')))==len(files)+len(dirs)+1
    assert captures()==d['completed_actual_captures']
    return {'verified':True,'payload_files':len(files),'total_files_including_manifest':len(files)+1,'directories':len(dirs),'manifest_sha256':sha(manifest),'root':str(root)}
def main():
    p=argparse.ArgumentParser();p.add_argument('--close',action='store_true');p.add_argument('--verify',action='store_true');a=p.parse_args()
    assert a.close!=a.verify
    if a.close:
        assert not manifest.exists(),'Refuse to replace a closed manifest'
        for q in root.rglob('*'):
            if q.is_file():q.chmod(0o444)
        files,dirs=inventory()
        d={'schema':'pr49-hyperbolic-family-self-only/v1','root':str(root),'closed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_closer_pid':os.getpid(),'closure_authority':'ROOT after child exit; actual invocation captured separately outside this family','payload_files':files,'directories':dirs,'completed_actual_captures':captures(),'manifest_self':{'path':'SELF_MANIFEST.json','mode':'0444','sha256':'Reported by separate closer stdout; omitted here to avoid circular self-hash'},'foreign_primary_bodies_retained':False,'source_scope':'First-party audit prose, scripts, private unchanged submitted helpers, results and actual command receipts only'}
        manifest.write_text(json.dumps(d,indent=2)+'\n');manifest.chmod(0o444)
    result=verify();result['actual_pid']=os.getpid();result['utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();result['action']='close' if a.close else 'verify';print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
