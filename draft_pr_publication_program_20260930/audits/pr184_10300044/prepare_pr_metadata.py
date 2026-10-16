"""Prepare concrete accurate PR metadata after verified publication and tracking."""
from pathlib import Path
import importlib.util,json
A=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('m',A/'prepare_final_scoped_merge.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
g,z,tr=m.gates();pr=m.api('pulls/184')
m.require(pr['head']['sha']==m.HEAD and pr['state']=='open' and not pr['merged'],'Original source PR changed')
body=f'''The literal volume-only bound in Calegari's arXiv:math/0209081v1 Question 10.6 fails: one fixed closed oriented hyperbolic three-manifold supports smooth cooriented taut foliations with ordinary Godbillon-Vey numbers Na, a>0, for every finite positive integer N. The same embedded positive closed circle meets every leaf. Compact leaves are permitted; the distinct minimal-foliation question is not resolved here.

This is a credited consequence of classical Mather-Thurston/Tsuboi compact-support suspension theory, interval-bundle replacement documented by Gabai, and Thurston hyperbolization. Historical priority remains unresolved after a bounded primary-body audit with explicit unread-source and version gaps. No historical firstness, guaranteed novelty or present-day open-status certificate is claimed.

Published research note and verification package: {z['doi_url']}. The exact reviewed PDF, standalone LaTeX source and supplemental ZIP were verified with the repository's Zenodo kit. Tracker row {tr['range']} was independently read back.

Three successive fresh whole-package reviews were completed. Review02 found a wrong expansion of the authors of an unread 1981 Annals paper; v2 globally corrects this to Mizutani-Morita-Tsuboi, DOI10.2307/2006995, while retaining its unread-body qualification. The final fresh review found no required repairs. The proof, PDF and executable controls were unchanged by that bibliographic repair.

Current exact local controls use explicit failures that remain active under optimization. They reproduce 2,660 polynomial and 1,640 symbolic checks, supplemented by an independent implementation of 58 rational Taylor-jet checks and a 343-point sampling counterexample. Deliberately incorrect variants fail in both modes. These controls supplement the global proof and do not certify holonomy realization, hyperbolization or all-leaf tautness numerically. The original imported universal lower-bound claim is superseded by the correct zero-GV fiber-foliation diagnostic. Original submission and review history remain preserved, including the frozen proof.

AI tools were used extensively in development, drafting, source checking, reproduction and adversarial review. The preprint is unrefereed and has not undergone conventional human peer review.
'''
request={'repository_full_name':'AlecKriebel/Math','pr_number':184,'title':'10300044: unbounded taut Godbillon-Vey numbers (credited consequence)','body':body}
(A/'PR_METADATA_REQUEST.json').write_text(json.dumps(request,indent=2)+'\n');print(json.dumps({'status':'CONCRETE_PR_METADATA_PREPARED','DOI':z['doi'],'original_head':m.HEAD}))
