"""Pin inputs and seal authored review artifacts; no writes outside this folder."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib
W=Path(__file__).absolute().parent;R=W.parent;D=R.parent/'initial_review_20261015'
now=datetime.now(timezone.utc).isoformat()
local_sources=[
('private_reading/owr_2022_43.pdf','https://doi.org/10.4171/owr/2022/43','Entire contribution, printed 2580-2582; PDF 70-72 rendered and viewed'),
('private_reading/owr_2022_43.txt','https://doi.org/10.4171/owr/2022/43','Complete contribution text read'),
('private_reading/costabel_dauge_nedaiasl.pdf','https://arxiv.org/abs/2302.13159v3','Full primary copy available; direct reading of relevant proof chain through companion text'),
('private_reading/costabel_dauge_nedaiasl.txt','https://arxiv.org/abs/2302.13159v3','Motivation; normalization; 1.6; 2.1-2.4; 3.5 and Proposition 3.15'),
('priority_classical_approximation_01/private_sources/anselone_palmer1968.txt','https://msp.org/pjm/1968/25-3/pjm-v25-n3-p02-p.pdf','Direct reading of compact multiplication, hypotheses and projection/rank theory'),
('priority_classical_approximation_01/private_sources/anselone_treuden1985.txt','https://msp.org/pjm/1985/120-2/pjm-v120-n2-p01-p.pdf','Introduction and relevant 7-9 stable/regular/compact proofs'),
('priority_classical_approximation_01/private_sources/descloux_nassif_rappaz1978.txt','https://www.numdam.org/article/M2AN_1978__12_2_97_0.pdf','P1/P2 and relevant spectral/subspace proofs'),
('priority_classical_approximation_01/private_sources/yurkin2006.txt','https://arxiv.org/abs/0704.0033','Targeted cubic/consistency search and direct Eqs 64-66 assumption discussion'),
('priority_classical_approximation_01/private_sources/yurkin2015_erratum.txt','https://doi.org/10.1364/JOSAA.32.002407','Complete erratum read'),
('priority_author_history_01/private/Conv1D-v2.txt','https://arxiv.org/abs/2303.13693v2','Relevant introductory/model claims and explicit reference 3'),
('priority_author_history_01/private/minicorsi2023.txt','https://events.math.unipd.it/minicorsi/sites/default/files/2021/2023-complete-booklet.pdf','Relevant DDA announcement inspected'),
('priority_counterexample_01/private_evidence/VIE-2018.txt','https://doi.org/10.1103/PhysRevA.97.043824','Full relevant IX discussion, Eqs 69-78, footnote22 and continuity limits'),
('priority_counterexample_01/private_evidence/EM-spectrum-2020.txt','https://arxiv.org/abs/2001.07116','Relevant Theorems3.2,3.7 and proofs/sign/meromorphic conclusions'),
('priority_counterexample_01/private_evidence/Ammari-Millien-2019.txt','https://doi.org/10.1016/j.matpur.2018.12.001','Relevant static decomposition and dynamic perturbation methods; no reliance on suspect compactness/rank-one assertions'),
('priority_counterexample_01/private_evidence/Mie-2017.txt','https://arxiv.org/abs/1702.05883v1','Relevant III, Eqs9-11 and radiation interpretation'),
('root_priority_01/private/zhou2021.txt','https://arxiv.org/abs/0911.4540v5','Relevant2.1 static/HS decomposition and Proposition2.1'),
('priority_author_history_01/private/hal_goepfert_thesis.json','https://theses.hal.science/tel-04884544','Metadata and English abstract only; full thesis not read'),
('final_priority_gate_adversary_01/private/fresh_primary_gap_reads.txt','https://doi.org/10.1137/S1064827598338962','Prior cached primary publisher abstract only; full Rahola not read'),
]
rows=[]
for rel,url,coverage in local_sources:
 p=D/rel;b=p.read_bytes();rows.append({'provenance_path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'url':url,'coverage':coverage})
records=[]
for rel in ['priority_author_history_01/PRIORITY_REPORT.md','priority_classical_approximation_01/REPORT.md','priority_counterexample_01/REPORT.md','final_priority_gate_adversary_01/REPORT.md']:
 p=D/rel;b=p.read_bytes();records.append({'path':str(p),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'role':'Inherited authored evidence, not adopted verdict'})
(W/'SOURCE_PINS.json').write_text(json.dumps({'utc':now,'primary_source_files':rows,'inherited_evidence_reports':records,'fresh_web_reads':[{'url':'https://arxiv.org/abs/2302.13159v3','coverage':'Primary metadata/version record read'},{'url':'https://www.mathunion.org/fileadmin/CDC/Grants/Abel%20Visiting%20Scholar%20Program/2019/khadijeh_nedaiasl_report.pdf','coverage':'Complete two-page primary report text read'},{'url':'https://epubs.siam.org/doi/10.1137/S1064827598338962','coverage':'Fresh fetch timed out; no full text read'},{'url':'https://doi.org/10.4171/owr/2022/43','coverage':'Web resolver failed; complete relevant contribution read in pinned local primary copy'}],'payload_policy':'Only provenance metadata is authored here; no full third-party text, images or raw web outputs are exported. Absolute provenance paths are not runtime dependencies.'},indent=2)+'\n')
# Verify frozen inputs again, independently of earlier extraction.
frozen=json.loads((R/'FROZEN_INPUTS.json').read_text())
for row in frozen['submission_files']:
 b=(R/row['path']).read_bytes();assert len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],row
verdict={'utc':now,'review':'fresh_review_01','mathematical_review':'PASS_NO_BLOCKER_IDENTIFIED','whole_source_lines_read':384,'all_11_rendered_pages_actually_viewed':True,'render_binding_byte_identical':True,'archive_members':136,'payload_hashes_verified':135,'all31_native_objects_verified':True,'portable_programs_all_passed':True,'fresh_independent_controls_passed':True,'minor_documentary_fixes':[{'id':'D1','file':'pr_update/30005244/CANDIDATE.md','lines':[13,235],'also_fix_generator':'prepare_supporting_materials.py','scope':'Replace obsolete active Unreviewed/remaining-review author-stage labels with explicit version-bound historical/current distinction; preserve originals.'},{'id':'D2','file':'prepare_supporting_materials.py','line':104,'scope':'Recorded Python version3.13 is stale; match actual3.14.6/NumPy2.3.4/SymPy1.14.0 or clearly distinguish supported from recorded versions.'}],'priority_certified':False,'source_limits':['Named2022/2023 dynamic manuscript unavailable','Rahola2000 full text unavailable','Goepfert2024 full thesis uninspected','No comprehensive exclusion of every broader classic'],'remaining_parent_work':'Apply minor documentary fixes, rebuild/pin and continue sequential whole-package review and explicit final clearance.','publication_cleared':False,'completion_percent_of_assigned_bounded_review':100,'frozen_inputs_unchanged_at_seal':True}
(W/'REVIEW_VERDICT.json').write_text(json.dumps(verdict,indent=2)+'\n')
p=W/'RESEARCH_LOG.md';s=p.read_text().replace('2026-10-15T08:49:02Z','2026-10-15T08:54:05Z');p.write_text(s+f'- {now} — Primary comparisons and bounded priority evidence assessment complete. No mathematical blocker found. Two minor documentary fixes identified; exact global repairs recorded. Frozen submission bytes rechecked unchanged. Reports and authored-only manifest sealed. Completion estimate 100% of this assigned bounded review; historical first priority and publication clearance remain unestablished.\n')
files=[]
for p in sorted(W.iterdir()):
 if p.is_file() and p.name!='SAFE_AUTHORED_MANIFEST.json':
  b=p.read_bytes();files.append({'path':p.name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
manifest={'utc':now,'scope':'Authored fresh review reports, reconstruction, code, logs and computed receipts only. Excludes private third-party/render/extraction assets and this manifest itself.','safe_authored_files':files,'publication_clearance':False}
(W/'SAFE_AUTHORED_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(json.dumps({'utc':now,'safe_authored_files':len(files),'manifest_sha256':hashlib.sha256((W/'SAFE_AUTHORED_MANIFEST.json').read_bytes()).hexdigest(),'review_verdict':verdict['mathematical_review'],'frozen_inputs_unchanged':True},indent=2))
