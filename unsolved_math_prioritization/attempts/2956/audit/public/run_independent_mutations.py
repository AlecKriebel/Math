#!/usr/bin/env python3
"""Mutation controls for independent validator, including conditional BF arithmetic."""
import argparse,copy,hashlib,json,os,pathlib,shutil,subprocess,sys,tempfile


def require(ok,message):
    if not ok:raise AssertionError(message)


def main():
    p=argparse.ArgumentParser();p.add_argument('--checker',type=pathlib.Path,required=True);p.add_argument('--candidate',type=pathlib.Path,required=True);p.add_argument('--expected',type=pathlib.Path,required=True);p.add_argument('--output',type=pathlib.Path,required=True);a=p.parse_args()
    require(os.getuid()==1000 and os.geteuid()==1000,'Must run as uid and euid 1000')
    original=json.loads(a.candidate.read_text());cases=[]
    def case(name,change):
        d=copy.deepcopy(original);change(d);cases.append((name,d))
    case('odd_rank_one_claim',lambda d:d['permutation_modules'][1].update(permitted_twist_group_ranks=[0,1,2]))
    case('wrong_triple_generator',lambda d:d['triple_quotient'].update(neck_generators=[1,2,2]))
    case('wrong_A2_group_order',lambda d:d['A_type_reflection_groups'][1].update(generated_matrix_group_order=3))
    case('false_eta4_nonvanishing',lambda d:d['nonequivariant_BF_arithmetic'][1]['neck_cases'][0].update(spin_choice_left='eta^3_nonzero_order_2'))
    case('wrong_twoK3_spin_lift',lambda d:d['nonequivariant_BF_arithmetic'][0]['neck_cases'][0].update(spin_choice_right='zero'))
    case('wrong_connected_sum_Euler',lambda d:d['K3_sums'][2].update(euler_characteristic=72))
    case('truncated_module_coverage',lambda d:d['permutation_modules'].pop())
    case('truncated_root_coverage',lambda d:d['A_type_reflection_groups'].pop())
    base=pathlib.Path(tempfile.mkdtemp(prefix='kp480_independent_ro_'));rows=[]
    try:
      checker=base/'independent_exact.py';checker.write_bytes(a.checker.read_bytes());cached=base/'expected.json';cached.write_bytes(a.expected.read_bytes())
      for name,data in [('baseline',original),*cases]:(base/(name+'.json')).write_text(json.dumps(data))
      for f in base.iterdir():f.chmod(0o444)
      base.chmod(0o555)
      for name,data in [('baseline',original),*cases]:
       for mode,flag in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
        cmd=[sys.executable,'-I','-B',*flag,str(checker),'--candidate',str(base/(name+'.json'))]
        # Baseline independently recomputes every RREF subspace in every optimization mode.
        if name!='baseline':cmd+=['--cached',str(cached)]
        proc=subprocess.run(cmd,cwd=base,capture_output=True,timeout=180)
        if name=='baseline':require(proc.returncode==0,'independent baseline failed');require(proc.stdout==cached.read_bytes(),'independent normal/optimized output changed')
        else:require(proc.returncode!=0 and b'AssertionError' in proc.stderr and b'PermissionError' not in proc.stderr,'Independent semantic mutation escaped')
        rows.append({'case':name,'mode':mode,'uid':os.getuid(),'euid':os.geteuid(),'cwd_mode':oct(base.stat().st_mode&0o777),'returncode':proc.returncode,'stdout_sha256':hashlib.sha256(proc.stdout).hexdigest(),'stderr':proc.stderr.decode()})
      a.output.write_text(json.dumps({'baseline_recomputations':3,'semantic_mutations':len(cases),'semantic_rejections':3*len(cases),'runs':rows},indent=2,sort_keys=True)+'\n')
    finally:
      base.chmod(0o755)
      for f in base.iterdir():f.chmod(0o644)
      shutil.rmtree(base)

if __name__=='__main__':main()
