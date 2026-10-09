#!/usr/bin/env python3
"""Fresh isolated finite diagnostics, not a universal topological proof."""
import json,math,os,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
REASONS={'unsigned_symmetrization':'symmetrization is not a chain map','omit_denominator':'symmetrization is not a chain map','skip_symmetrization':'same-index pairing requires each face operator to vanish','same_orientation_pair':'paired face orientations agree','wrong_face_index':'pairing changed omitted index','colour_identification':'face gluing identifies different colours','drop_face_pair':'face coverage is not exactly once','duplicate_face_pair':'face coverage is not exactly once','denominator_mismatch':'normalized tetrahedron count mismatch','wrong_cover_ratio':'Gaifullin tile identity mismatch','drop_torsion_multiplier':'rational equality did not clear integral torsion','false_count_exception_guard':'Diagnostic failed: len(copies)==120'}
def need(ok,message):
 if not ok:raise ValueError(message)
def same(a,b):
 if type(a) is not type(b):return False
 if type(b) is dict:return set(a)==set(b) and all(same(a[k],v) for k,v in b.items())
 if type(b) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def unique(pairs):
 result={}
 for k,v in pairs:need(k not in result,'duplicate JSON key');result[k]=v
 return result
def nonfinite(token):raise ValueError('nonfinite JSON')
def number(token):
 x=float(token);need(math.isfinite(x),'nonfinite float');return x
def parse(raw):return json.loads(raw,object_pairs_hook=unique,parse_constant=nonfinite,parse_float=number)
def identities():
 return [('current/check_coloured_cycles.py',None),('current/check_audit.py',None)]+[('check_author_case.py' if m=='false_count_exception_guard' else 'current/check_audit.py',m) for m in sorted(REASONS)]
def positive(index,mode):
 if index==0:return {'status':'PASS','test':'symmetrized boundary of an abstract4-simplex','original_tetrahedra':5,'original_l1':'5','symmetrized_l1':'5','denominator':24,'paired_tetrahedra':120,'face_pairs':240,'individual_face_operators_zero':[True]*4,'all_vertex_identifications_color_preserving':True,'normalized_tetrahedron_count':'5','barycentric_loss_removed':24,'scope':'Formal finite face/sign/denominator check; no Gaifullin topology or all-space theorem is certified computationally.'}
 return {'status':'PASS','optimization':mode,'mutation':'none','exact_chain_cases':80,'primary_pairing':{'tetrahedra':120,'face_pairs':240,'denominator':24,'normalized_l1':'5','dual_component_sizes':[120]},'disconnected_pairing':{'tetrahedra':240,'face_pairs':480,'denominator':24,'normalized_l1':'10','dual_component_sizes':[120,120]},'frozen_files_checked':None,'scope':'Finite algebra, orientation, colour, pairing, count and integrity checks only; not universal topological certification.'}
def wanted(index,mutation,mode):
 if mutation is None:return positive(index,mode)
 out=dict(status='FAIL',optimization=mode,error=REASONS[mutation])
 if mutation=='false_count_exception_guard':out['mutation']=mutation
 return out
def main():
 need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000');need(sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode,'-I -S -B required');need(len(sys.argv)==1,'no optional or skip arguments')
 contract=parse((HERE/'FINITE_CONTRACT.json').read_bytes())
 need(type(contract) is dict and set(contract)=={'schema','problem_id','modes','role'} and type(contract['schema']) is int and contract['schema']==1 and type(contract['problem_id']) is int and contract['problem_id']==30001812,'contract schema')
 need(type(contract['modes']) is dict and set(contract['modes'])=={'0','1','2'},'all optimization modes')
 expected=contract['modes'][str(sys.flags.optimize)]
 need(type(expected) is list and len(expected)==14,'exact nonempty suite size');need([(r['program'],r['mutation']) for r in expected]==identities(),'exact identities and order')
 mode=[] if sys.flags.optimize==0 else ['-'+'O'*sys.flags.optimize];rows=[]
 for index,row in enumerate(expected):
  need(type(row) is dict and set(row)=={'program','mutation','expected_exit','stdout','stderr'},'case schema')
  script,mutation=row['program'],row['mutation'];code=1 if mutation else 0
  need(type(row['expected_exit']) is int and row['expected_exit']==code,'case exit schema');need(type(row['stdout']) is str and row['stdout'] and type(row['stderr']) is str and row['stderr']=='','raw reference fields')
  args=[script]+((['--mutation',mutation] if script.endswith('check_audit.py') else [mutation]) if mutation else [])
  p=subprocess.run([sys.executable,'-I','-S','-B',*mode,*args],cwd=HERE,env=dict(PATH=os.defpath,HOME='/tmp',TMPDIR='/tmp',LC_ALL='C'),capture_output=True,timeout=300)
  need(type(p.returncode) is int and p.returncode==code,'exact intended exit');need(p.stdout==row['stdout'].encode() and p.stderr==row['stderr'].encode(),'entire raw output differs '+script+' '+str(mutation))
  parsed=parse(p.stdout);need(same(parsed,parse(row['stdout'])),'recursive exact output types');need(same(parsed,wanted(index,mutation,sys.flags.optimize)),'exact identities counts and rejection reason')
  category='positive_checker' if mutation is None else 'exception_guard' if mutation=='false_count_exception_guard' else 'algorithm_input_mutant'
  reason='positive finite diagnostics accepted' if mutation is None else REASONS[mutation]
  rows.append(dict(script=script,mutation=mutation,category=category,exit_code=p.returncode,expected_exit=code,rejected=mutation is not None,reason=reason,stdout=p.stdout.decode(),stderr=p.stderr.decode(),complete_output_comparison=True,recursive_exact_type_comparison=True,normalization='NONE'))
 need(len(rows)==14 and sum(r['rejected'] is False for r in rows)==2 and sum(r['rejected'] is True for r in rows)==12,'exact totals')
 print(json.dumps(dict(status='passed',problem_id=30001812,uid=os.getuid(),euid=os.geteuid(),python_optimize=sys.flags.optimize,positive_checker_runs=2,expected_mutant_rejections=12,rejection_categories={'algorithm_input_mutants':11,'exception_guard':1},cases=rows,mathematics='Finite diagnostics on a bounded subset only; universal topology and the comparison/reduction proofs are audited in writing. Eleven algorithm/input mutations and one separate actual false-count exception guard per mode. Repeated hostile and integrity replays add no mathematical coverage.'),sort_keys=True))
if __name__=='__main__':
 try:main()
 except (ValueError,OSError,TypeError,KeyError,subprocess.TimeoutExpired) as error:
  print('REJECT: finite-interface replay failed: '+str(error),file=sys.stderr);sys.exit(1)
