#!/usr/bin/env python3
"""Mathematical and inventory negative controls; disposable writable copies only."""
import ast, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
from unittest.mock import patch
sys.dont_write_bytecode=True
from validate import validate, require
ROOT=Path(__file__).resolve().parent

def fixture(destination):
    shutil.copytree(ROOT,destination)
    destination.chmod(0o700)
    for p in destination.iterdir():p.chmod(0o600)
    return destination

def main():
    validate(ROOT)
    results=[]
    with tempfile.TemporaryDirectory(prefix='theta-controls-') as t:
        tmp=Path(t)
        edits=[('profile_shift','profile_test.py','row[(j-s)%N]','row[j%N]','PROFILES.json'),
               ('profile_rank','profile_test.py','return a[:k],piv','return a[:max(0,k-1)],piv','PROFILES.json'),
               ('irreducibility_polynomial','independent_check.py','F = [2, 0, 1, 0, 0, 0, 0, 1]','F = [0, 0, 1, 0, 0, 0, 0, 1]','INDEPENDENT_CHECK.json')]
        for name,program,old,new,expected in edits:
            root=fixture(tmp/name);p=root/program;s=p.read_text()
            require(s.count(old)==1,'unique mutation target '+name)
            changed=s.replace(old,new);ast.parse(changed);p.write_text(changed)
            for mode in ([],['-O']):
                proc=subprocess.run([sys.executable,*mode,str(p)],capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
                require(proc.returncode!=0 or proc.stdout!=(ROOT/expected).read_bytes(),'undetected '+name)
                results.append({'name':name,'optimized':bool(mode),'rejected':True,'exit_code':proc.returncode,'stderr':proc.stderr.decode().replace(str(tmp), '<disposable>')})
        for name,old,new in [('field_reduction','t[j-5]+=2*c','t[j-5]+=0*c'),('rank_enumeration','hist[rk(c)]++','hist[7]++')]:
            root=fixture(tmp/name);p=root/'finite_test.cpp';s=p.read_text();require(s.count(old)==1,'unique C++ target');p.write_text(s.replace(old,new))
            for mode in ([],['-DNDEBUG']):
                binary=tmp/(name+('optimized' if mode else 'normal'))
                proc=subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra','-pedantic',*mode,str(p),'-o',str(binary)],capture_output=True)
                require(proc.returncode==0,'mutant must compile')
                proc=subprocess.run([str(binary)],capture_output=True,cwd=tmp)
                require(proc.returncode!=0 or proc.stdout!=(ROOT/'FINITE_TEST.json').read_bytes(),'undetected C++ mutation')
                results.append({'name':name,'ndebug':bool(mode),'rejected':True,'exit_code':proc.returncode,'stdout':proc.stdout.decode(),'stderr':proc.stderr.decode().replace(str(tmp), '<disposable>')})
        for name in ['boolean_histogram','float_dimension','wrong_rank_count','missing_generator','wrong_code_name']:
            root=fixture(tmp/name)
            p=root/('PROFILES.json' if name in ('float_dimension','missing_generator') else 'FINITE_TEST.json');v=json.loads(p.read_text())
            if name=='boolean_histogram':v['codes'][0]['projective_rank_histogram'][0]=False
            elif name=='float_dimension':v['monomial_013']['1']['sums'][0]=3.0
            elif name=='wrong_rank_count':v['codes'][0]['projective_rank_histogram'][5]+=1;v['codes'][0]['projective_rank_histogram'][6]-=1
            elif name=='missing_generator':del v['twisted_eta1']['2']
            else:v['codes'][1]['name']='monomial_013'
            p.write_text(json.dumps(v))
            for mode in ([],['-O']):
                proc=subprocess.run([sys.executable,*mode,str(root/'exact_checks.py')],capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
                require(proc.returncode!=0,'undetected schema or mathematics mutation '+name)
                results.append({'name':name,'optimized':bool(mode),'rejected':True,'exit_code':proc.returncode})
        root=fixture(tmp/'production_rank_pivot');p=root/'finite_test.cpp';s=p.read_text();require(s.count('++r;break;')==1,'rank pivot target');p.write_text(s.replace('++r;break;','r+=0;break;'))
        proc=subprocess.run([sys.executable,str(root/'rank_checks.py')],capture_output=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        require(proc.returncode!=0,'undetected production rank mutation')
        results.append({'name':'production_rank_pivot','rejected':True,'exit_code':proc.returncode})
        # Require zero reads for bad inventory, including a poisoned manifest.
        for name in ['payload_symlink','manifest_symlink','directory','fifo','hardlink','manifest_hardlink']:
            root=fixture(tmp/name)
            if name=='payload_symlink':
                (root/'AUDIT.md').unlink();(root/'AUDIT.md').symlink_to(tmp/'missing')
            elif name=='manifest_symlink':
                (root/'MANIFEST.json').unlink();(root/'MANIFEST.json').symlink_to(tmp/'missing')
            elif name=='directory':(root/'unexpected').mkdir()
            elif name=='fifo':os.mkfifo(root/'unexpected')
            elif name=='hardlink':os.link(root/'AUDIT.md',root/'unexpected')
            else:os.link(root/'MANIFEST.json',root/'unexpected')
            with patch.object(Path,'read_text',side_effect=RuntimeError('premature content read')),patch.object(Path,'read_bytes',side_effect=RuntimeError('premature content read')):
                try:validate(root)
                except ValueError:results.append({'name':name,'rejected':True,'content_reads':0})
                else:raise ValueError('accepted bad inventory '+name)
        for name in ['boolean_byte_count','boolean_schema','float_problem_id','duplicate_json_key','hash_change','unexpected_regular']:
            root=fixture(tmp/name);p=root/'MANIFEST.json';m=json.loads(p.read_text())
            if name=='boolean_byte_count':m['files'][0]['bytes']=True
            elif name=='boolean_schema':m['schema_version']=True
            elif name=='float_problem_id':m['problem_id']=30004105.0
            elif name=='hash_change':(root/'AUDIT.md').write_bytes(b'changed')
            elif name=='unexpected_regular':(root/'unexpected').write_bytes(b'x')
            if name=='duplicate_json_key':p.write_text('{"schema_version":1,'+p.read_text()[1:])
            else:p.write_text(json.dumps(m))
            try:validate(root)
            except ValueError:results.append({'name':name,'rejected':True})
            else:raise ValueError('accepted malformed fixture '+name)
    print(json.dumps({'status':'PASS','all_controls':len(results),'results':results,'actual_sockets_created':False,'fixtures':'writable disposable copies'},indent=2))
if __name__=='__main__':main()
