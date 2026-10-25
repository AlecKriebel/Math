#!/usr/bin/env python3
"""Post-seal controls, explicitly separated from pre-helper independence evidence."""
from pathlib import Path
import ast,copy,json,subprocess,sys,hashlib,datetime
import sympy as S
O=Path(__file__).resolve().parent;B=O.parents[2];P=B/'sources/published-source/deep-derived-pure-braids-source-verification-v1.0'
# Reuse own sealed function definitions without executing or rewriting its evidence outputs.
ns={'S':S}
tree=ast.parse((O/'independent_controls.py').read_text())
for node in tree.body:
 if isinstance(node,ast.FunctionDef) and node.name in ['goeritz','variation','characteristic_inertia']:
  exec(compile(ast.Module(body=[node],type_ignores=[]),'own sealed function','exec'),ns)
A=[2,-1];Bb=[1,-2];G=ns['goeritz'](A,Bb);wrong=G.copy();start=0;n=G.rows
for j,b in enumerate(Bb):
 cur=1 if b>0 else -1;prev=1 if Bb[j-1]>0 else -1
 for k in range(abs(b)):
  i=(start+k)%n;q=(i+1)%n
  wrong[i,q]+=prev-cur;wrong[q,i]+=prev-cur
 start+=abs(b)
gi=ns['characteristic_inertia'](G)[0];wi=ns['characteristic_inertia'](wrong)[0]
assert gi!=wi
# Replay independently mutated certificate inputs in our dedicated scratch, never sources.
cert=json.loads((P/'original_packet/original/certificate.json').read_text());fixtures={}
fixtures['reversed_claimed_signature']=copy.deepcopy(cert);fixtures['reversed_claimed_signature']['signature']=2
fixtures['overstated_depth']=copy.deepcopy(cert);fixtures['overstated_depth']['derived_level']=4
fixtures['one_letter_reversal']=copy.deepcopy(cert);fixtures['one_letter_reversal']['word'][0]*=-1
fixtures['diagonal_perturbation']=copy.deepcopy(cert);fixtures['diagonal_perturbation']['goeritz'][0][0]+=2
work=B/'reviews/adversarial/replay-work/negative-fixtures';work.mkdir(parents=True,exist_ok=True)
results=[]
for name,c in fixtures.items():
 f=work/(name+'.json');f.write_text(json.dumps(c))
 cmd=[sys.executable,'-I','-B',str(P/'original_packet/original/verify.py'),str(f)]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
 assert p.returncode!=0 and p.stderr.startswith('REJECT:')
 results.append({'name':name,'returncode':p.returncode,'stderr':p.stderr.strip(),'fixture_sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'mutation':{'field':name,'fixture_is_private_copy':True}})
r={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'after_helper_inspection':True,'mixed_parity_index_fixture':{'A':A,'B':Bb,'geometric_matrix':[[int(x) for x in G.row(i)] for i in range(n)],'geometric_inertia':gi,'printed_previous_index_matrix':[[int(x) for x in wrong.row(i)] for i in range(n)],'previous_index_inertia':wi},'negative_certificate_controls':results,'scope':'Checks corruption detection, not universal group/topology proofs. Historical expectation text is not evidence.'}
(O/'post-helper-controls.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r,indent=2))
