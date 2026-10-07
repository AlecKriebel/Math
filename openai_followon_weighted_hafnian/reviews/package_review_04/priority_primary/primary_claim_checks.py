#!/usr/bin/env python3
"""Audit exact inspected source/PDF text and candidate identities, not mathematical novelty."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib,json,re,subprocess
R=Path(__file__).resolve().parent
P=R/'primary_reading'
def txt(name):
 f=P/(name+'.txt')
 if not f.exists(): subprocess.run(['pdftotext','-layout',str(P/(name+'.pdf')),str(f)],check=True)
 return f.read_text()
def src(name,file): return (P/(name+'_source')/file).read_text(encoding='latin1')
def has(t,s): return s in ' '.join(t.split())
checks={
 'mcq_pdf_sec7_2_and_lemmas25_27': all(has(txt('mcquillan-v1'),x) for x in ['7.2 Approximate counting','Lemma 25.','Lemma 27.','specified in binary','A simple graph G']),
 'mcq_tex_binary_rational_scope': has(src('mcquillan-v1','main.tex'),'fugacities and edge-weights are given as ratios of non-negative integers specified in binary'),
 'mcq_tex_computable_scale_and_simple_output': all(x in src('mcquillan-v1','main.tex') for x in ['C=\\prod_{e\\in E^{G_3}}q_e','subdivide','simple graph']),
 'cai_pdf_thm1_2_prop5': all(has(txt('cai-liu1904-v1'),x) for x in ['Theorem 1.2.','[McQ13, Proposition 5]','allowing nonnegative edge-weights does not add more computational']),
 'cai_tex_prop5_scope_agrees': has(src('cai-liu1904-v1','intro.tex'),'allowing nonnegative edge-weights does not add more computational power'),
 'cai_tex_internal_reference_prop5': '[Proposition 5]{DBLP:journals/corr/abs-1301-2880}' in src('cai-liu1904-v1','intro.tex'),
 'barvinok_v5_pdf_thm2_1_not2_2': has(txt('barvinok-v5'),'Theorem 2.1 For any 0 <') and has(txt('barvinok-v5'),'Theorem 2.2 Let us fix'),
 'barvinok_v5_internal_label_th2_2_is_arbitrary': '\\begin{thm}\\label{th2.2}' in src('barvinok-v5','barvinok.tex'),
 'yi_pdf_thm1_1a': has(txt('yi-v1'),'Theorem 1.1 (Main result for matchings). Fix') and '(a)' in txt('yi-v1'),
 'yi_tex_rational_matrix_and_fixed_margin': all(has(src('yi-v1','unified_frontmatter.tex'),x) for x in ['Fix $0<\\gamma<1/2$ and $0<\\theta\\le1$','Let $A$ be a rational symmetric $n$ by $n$ matrix']),
 'jvv_pdf_thm6_3_self_reducible': has(txt('jvv1986'),'Theorem 6.3. Let R be a self-reducible p-relation.'),
 'dhw2010_pdf_fig3_log_weight': 'Fig. 3.' in txt('dhw2010') and 'log a' in txt('dhw2010'),
 'dell_expanded_v1_pdf_fig3_log_weight': 'Figure 3:' in txt('dell2014-v1') and 'log a' in txt('dell2014-v1'),
}
C=R.parent/'extracted'
M=R.parent.parent/'candidate_v4'
paths=[C/'main.tex',C/'research/PRIORITY_AUDIT.md',C/'research/priority_sources/SOURCE_STATEMENTS.md',M/'zenodo-deposit.json',M/'paper.pdf',M/'source-and-verification.zip']
identity={str(f):{'sha256':hashlib.sha256(f.read_bytes()).hexdigest(),'bytes':f.stat().st_size} for f in paths}
report={'checked_utc':datetime.now(timezone.utc).isoformat(),'checks':checks,'all_checks_pass':all(checks.values()),'candidate_identity':identity,'meaning':'Finite statement/identity checks; neither proof certification nor absence-of-prior-publication certificate.'}
(R/'SOURCE_STATEMENT_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
for k,v in checks.items(): print(k, 'PASS' if v else 'FAIL')
