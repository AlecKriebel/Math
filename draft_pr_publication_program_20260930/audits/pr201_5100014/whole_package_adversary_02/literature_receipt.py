from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
A=Path(__file__).resolve().parent.parent
sources=[
 ('priority_exact_history_01/private_sources/ferudun_zenodo_v10_arxiv_source_main.tex','https://doi.org/10.5281/zenodo.23087221','Theorem 1; local pole/reversal proof sections 3–5; radial/six-period proposition section 6; repeated triangle section 7'),
 ('priority_exact_history_01/private_sources/ferudun_zenodo_v11_arxiv_source_main.tex','https://doi.org/10.5281/zenodo.23088516','Full v1.0/v1.1 source diff read: overlapping arbitrary-point theorem retained; adjacent centered extension added'),
 ('priority_general_theorems_01/private_sources/chavez_journal0200154.pdf','https://doi.org/10.1007/s40598-020-00154-8','Journal flag framework section 2 printed p98; area product theorem 6 section 5 printed p104; cached extraction read'),
 ('primary_source_private/reznik_garcia_koiller_2004.12497v11.pdf','https://arxiv.org/abs/2004.12497v11','Page6, section3.4 Table4: k303,a, N=2mod4, all M; literal least period absent'),
 ('priority_classical_pedals_01/primary_private/steiner1838_offprint_ocr.txt','https://doi.org/10.3931/e-rara-3816','OCR sections XV–XVI, printed pp19–21, fixed-polygon pedal circle-level/radial quadratic; OCR caveat, modern formula independently derived')]
rows=[]
for rel,url,read in sources:
 b=(A/rel).read_bytes();rows.append({'source_relative_to_A':rel,'url':url,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'reading':read})
print(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'cached_primary_texts_only_no_favorable_reports_used_as_mathematical_evidence':True,'fresh_primary_API_checks':'primary_records.json','sources':rows,'web_access':'arXiv current abs page accessible. DOI opens for Zenodo and journal failed in web tool; cached primary sources read and fresh public Zenodo/DataCite APIs succeeded. No new fulltext download required.','coverage_limits':'Focused decisive primary comparison, not exhaustive history. No priority, novelty, independence, human refereeing or proof-assistant certification.'},indent=2))
