#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import hashlib,json,re,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]

def sha(p):
 h=hashlib.sha256();
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()

def load(name):return json.loads((ROOT/'certificates'/name).read_text())
assert sha(ROOT/'baseline'/'SD0_BASELINE_MANUSCRIPT.pdf')=='a6981ccec9bd8c3786d413235d370b393ec754ed762b13974dfdfd30874ec760'
assert json.loads((ROOT/'FINAL_OUTCOME.json').read_text())['outcome']=='Q'
status=(ROOT/'STATUS.md').read_text();assert 'Outcome Q' in status and 'not literally identical' in status
p=load('primary_convention_frontier.json');i=load('independent_frontier.json')
for L in map(str,range(2,10)):
 for k in ('valid_raw_artifact_presentations','tree_child_raw_artifact_presentations','canonical_clean_target_graphs'):
  assert p['path_length_frontier'][L][k]==i['frontier'][L][k]
 pp=sorted((x['raw_artifact_rootings'],x['raw_artifact_tree_child_rootings']) for x in p['cleanup_fibres'][L])
 ii=sorted((x['raw_presentations'],x['tree_child_presentations']) for x in i['frontier'][L]['fibre_profiles'])
 assert pp==ii
assert p['path_length_frontier']['2']['valid_raw_artifact_presentations']==0
assert p['path_length_frontier']['3']['tree_child_raw_artifact_presentations']==0
assert load('cleanup_jc_map.json')['status']=='PROVED'
assert load('independent_cleanup_model.json')['status']=='PROVED'
r=load('independent_rooting_fibres.json')
assert r['strict_target_sd0_rootings']=={'valid':5,'tree_child':5,'strong':True}
assert r['theta_source']['valid']==5 and r['theta_source']['tree_child']==2 and not r['theta_source']['strong']
assert load('independent_convention_review.json')['outcome']=='Q'
assert load('mutation_suite.json')['status']=='ALL MUTATIONS REJECTED'
assert load('root_zipper_structure.json')['structural_statements']['tree_child_zipper_contracts_to_binary_LSA_sd0_rooting']
# Active documentation must not claim literal rooting equivalence or general 2-blob erasure.
active=[ROOT/'STATUS.md',ROOT/'README.md',ROOT/'docs'/'THEOREM_Q_PROOF.md',ROOT/'manuscript'/'convention_closed.tex']
text='\n'.join(x.read_text() for x in active)
assert 'rooting sets do not coincide' in text or 'rooting fibre' in text
assert 'No general 2-sub-blob' in text or 'No arbitrary 2-sub-blob' in text or 'arbitrary 2-sub-blob' in text
assert 'canonical model-preserving quotient' in text or 'canonical cleanup quotient' in text
assert 'literature-standard' in text
# Check compiled PDF and forbidden overstatement in its extracted text.
pdf=ROOT/'manuscript'/'Strong_Tree_Childness_Level2_JC_Convention_Closed.pdf';assert pdf.exists() and pdf.stat().st_size>100000
out=subprocess.check_output(['pdfinfo',str(pdf)],text=True);m=re.search(r'Pages:\s+(\d+)',out);assert m and int(m.group(1))==22
pt=subprocess.check_output(['pdftotext',str(pdf),'-'],text=True)
assert 'Canonical cleanup quotient' in pt
assert 'The conventions are not literally equivalent' in pt
assert 'No general 2-sub-blob is erased' in pt
print('PASS release integrity: Outcome Q')
