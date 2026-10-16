#!/usr/bin/env python3
"""Reproduce optimization and mutation controls using genuine non-root readonly trees."""
import argparse, ast, hashlib, json, os, pathlib, shutil, subprocess, sys, tempfile, time


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--original', type=pathlib.Path, required=True)
    p.add_argument('--corrected', type=pathlib.Path, required=True)
    p.add_argument('--expected', type=pathlib.Path, required=True)
    p.add_argument('--output', type=pathlib.Path, required=True)
    args=p.parse_args()
    require(os.getuid()==1000 and os.geteuid()==1000, 'Real uid and effective uid must both equal 1000')
    orig=args.original.read_text(); fixed=args.corrected.read_text(); expected=args.expected.read_bytes()
    mutations=[
      ('odd_rank_one_allowed', 'expected=sorted({0,n-1} if n%2 else {0,1,n-1})', 'expected=sorted({0,1,n-1})'),
      ('scalar_diagonal_condition_removed', ' and v.bit_count()%2==0]', ']'),
      ('wrong_triple_diagonal', 'delta=7', 'delta=3'),
      ('reflection_generator_dropped', '        refl.append(s)', '        if i != 0:\n            refl.append(s)'),
      ('coxeter_product_omitted', '        coxeter = matmul(coxeter,s)', '        coxeter = coxeter'),
    ]
    base=pathlib.Path(tempfile.mkdtemp(prefix='kp480_readonly_'))
    records=[]; before={}; probes=[]
    try:
      for label,source in [('original',orig),('corrected',fixed)]:
        variants=[('baseline',source)]
        for name,old,new in mutations:
          require(source.count(old)==1, name+' replacement not unique')
          variants.append((name,source.replace(old,new)))
        for name,body in variants:
          folder=base/(label+'_'+name); folder.mkdir()
          f=folder/'verify_exact.py'; f.write_text(body); (folder/'sentinel').write_text('readonly probe\n')
          for q in folder.iterdir():q.chmod(0o444)
          folder.chmod(0o555)
          before[str(f)]=hashlib.sha256(f.read_bytes()).hexdigest()
          for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
            started=time.monotonic()
            proc=subprocess.run([sys.executable,'-I','-B',*flags,str(f)],cwd=folder,capture_output=True,timeout=180)
            row={'implementation':label,'case':name,'mode':mode,'uid':os.getuid(),'euid':os.geteuid(),'cwd_permissions':oct(folder.stat().st_mode&0o777),'script_permissions':oct(f.stat().st_mode&0o777),'returncode':proc.returncode,'stdout_bytes':len(proc.stdout),'stdout_sha256':hashlib.sha256(proc.stdout).hexdigest(),'stderr':proc.stderr.decode(),'baseline_bytes_match':proc.stdout==expected}
            if proc.returncode==0:
              data=json.loads(proc.stdout);row['reported_all_assertions_passed']=data.get('all_assertions_passed')
            if name=='baseline':require(proc.returncode==0 and proc.stdout==expected,label+' baseline failed '+mode)
            elif label=='corrected' or mode=='normal':
              require(proc.returncode!=0 and b'AssertionError' in proc.stderr,label+' mutation failed to reject '+name+' '+mode)
              require(b'PermissionError' not in proc.stderr,'Permission failure is not semantic rejection')
            else:
              require(proc.returncode==0 and row['reported_all_assertions_passed'] is True,'Expected frozen false-PASS control absent')
            records.append(row)
            print(label,name,mode,proc.returncode,flush=True)
          probe_code='''import json,os,pathlib
r={'uid':os.getuid(),'euid':os.geteuid(),'groups':os.getgroups(),'directory_write_denied':False,'file_write_denied':False}
try:pathlib.Path('write_probe').write_text('forbidden')
except PermissionError:r['directory_write_denied']=True
try:open('sentinel','a').write('forbidden')
except PermissionError:r['file_write_denied']=True
print(json.dumps(r))
'''
          probe=subprocess.run([sys.executable,'-I','-B','-c',probe_code],cwd=folder,capture_output=True,check=True)
          info=json.loads(probe.stdout);require(info['directory_write_denied'] and info['file_write_denied'],'Readonly probe failed')
          probes.append({'tree':label+'_'+name,**info})
      unchanged=all(hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()==v for p,v in before.items())
      require(unchanged,'Readonly source changed')
      require(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse(fixed))),'Corrected source has removable assert')
      out={'python':sys.version,'uid':os.getuid(),'euid':os.geteuid(),'baseline_runs':6,'semantic_mutations':len(mutations),'corrected_mutation_rejections':15,'original_normal_rejections':5,'original_optimized_false_passes':10,'all_readonly_scripts_unchanged':unchanged,'corrected_ast_assert_nodes':0,'permission_probes':probes,'runs':records,'scope':'Algebraic runtime checks only. No gauge invariant or smooth isotopy is computed.'}
      args.output.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    finally:
      for folder in base.iterdir():
        if folder.is_dir():
          folder.chmod(0o755)
          for f in folder.iterdir():f.chmod(0o644)
      shutil.rmtree(base)

if __name__=='__main__':main()
