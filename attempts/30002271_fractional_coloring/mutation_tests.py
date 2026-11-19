#!/usr/bin/env python3
"""Offline rejection tests. All changes occur in writable temporary copies."""
import json, shutil, subprocess, sys, tempfile, os
from pathlib import Path
ROOT=Path(__file__).parent

def run():
    import validate
    validate.validate(ROOT)
    results=[]
    def case(name, change, command):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'copy';shutil.copytree(ROOT,root)
            for p in root.iterdir(): p.chmod(0o644)
            root.chmod(0o755)
            change(root)
            out=subprocess.run([sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+[command],cwd=root,capture_output=True,text=True,timeout=30)
            rejected=out.returncode!=0
            if not rejected: raise ValueError('mutation accepted: '+name)
            results.append({'name':name,'rejected':True,'returncode':out.returncode,'stdout':out.stdout,'stderr':out.stderr.replace(str(root),'<disposable>')})
    def alter(a,b):
        def change(root):
            p=root/'check_exact.py';s=p.read_text()
            if s.count(a)!=1: raise ValueError('mutation anchor count')
            p.write_text(s.replace(a,b))
        return change
    for name,a,b in [
        ('wrong_average','F(3*k,4)+1','F(3*k,3)+1'),
        ('strict_k4','(k>=5)','(k>=4)'),
        ('invalid_primal','(i+1)%k','i%k'),
        ('overweight_dual','int(v<k)','2*int(v<k)'),
        ('k1_wrong_chi','chi=max(k,2)','chi=k'),
        ('missing_pendant_edges','edge(i,k+i*k+j)','edge((i+1)%k,k+i*k+j)')]:
        # Last mutation merely relabels leaves, so instead remove one edge to alter construction.
        if name=='missing_pendant_edges': b='edge(i,k+i*k+j) if j else None'
        case(name,alter(a,b),'check_exact.py')
    def manifest(field,value):
        def change(root):
            p=root/'MANIFEST.json';m=json.loads(p.read_text())
            if field=='bytes':m['files'][0]['bytes']=value
            elif field=='duplicate':m['files'].append(m['files'][0])
            else:m[field]=value
            p.write_text(json.dumps(m))
        return change
    for name,field,value in [('bool_size','bytes',True),('float_size','bytes',5914.0),('negative_size','bytes',-1),('bool_schema','schema_version',True),('float_id','problem_id',30002271.0),('duplicate','duplicate',None)]:case(name,manifest(field,value),'validate.py')
    case('payload_tamper',lambda p:(p/'AUDIT.md').write_text('altered'),'validate.py')
    case('extra_file',lambda p:(p/'extra').write_text('unexpected'),'validate.py')
    case('missing_file',lambda p:(p/'AUDIT.md').unlink(),'validate.py')
    case('extra_directory',lambda p:(p/'extra').mkdir(),'validate.py')
    def symlink(p,name):
        (p/name).unlink();(p/name).symlink_to('absent-target')
    case('manifest_symlink',lambda p:symlink(p,'MANIFEST.json'),'validate.py')
    case('payload_symlink',lambda p:symlink(p,'AUDIT.md'),'validate.py')
    case('fifo',lambda p:os.mkfifo(p/'fifo'),'validate.py')
    case('hardlink',lambda p:os.link(p/'AUDIT.md',p/'alias'),'validate.py')
    # Simulate socket lstat mode rather than opening or binding an actual socket.
    with tempfile.TemporaryDirectory() as d:
        shutil.copytree(ROOT,Path(d)/'copy');p=Path(d)/'copy'
        program="import validate,stat;from pathlib import Path;from types import SimpleNamespace;orig=Path.lstat;Path.lstat=lambda self: SimpleNamespace(st_mode=stat.S_IFSOCK,st_nlink=1,st_size=0) if self.name=='AUDIT.md' else orig(self);validate.validate(Path('.'))"
        out=subprocess.run([sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+['-c',program],cwd=p,text=True,capture_output=True)
        if out.returncode==0:raise ValueError('socket mode accepted')
        results.append({'name':'simulated_socket_mode','rejected':True,'returncode':out.returncode,'stdout':out.stdout,'stderr':out.stderr.replace(str(p),'<disposable>')})
    return {'passed':True,'tests':len(results),'actual_sockets_created':False,'writable_disposable_copies_only':True,'results':results}
if __name__=='__main__':print(json.dumps(run(),indent=2))
