from pathlib import Path
from datetime import datetime, timezone
import hashlib, json

root=Path(__file__).resolve().parent
base=root.parent
now=datetime.now(timezone.utc).isoformat()
v=json.loads((root/'VERDICT.json').read_text())
v['completed_utc']=now
(root/'VERDICT.json').write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
s=json.loads((root/'SEARCH_SCOPE.json').read_text())
s['recorded_utc']=now
(root/'SEARCH_SCOPE.json').write_text(json.dumps(s,indent=2,ensure_ascii=False)+'\n')
log="""# García–Wüstholz priority audit log

2026-10-06T03:24:55Z — First captured UTC clock, after initial source reads/searches. Completion estimate: 20% of the assigned audit. Accepted mathematical gate as input and pinned the exact all-positive-real-axis mean/lift/count/parity target. The 2017 final section concerns the same Minkowski null-chain problem, with a number-field hypothesis and no displayed null-period proof. Individual times of earlier reads were not captured.

2026-10-06T03:26:41Z — Public retrieval checkpoint. Completion estimate: 45%. Corrected the preserved report’s approximately2021 ETH-thesis attribution: the matching item is published Wüstholz2021, Acta Arithmetica198(4),329–357. Indexed p331 explicitly motivates with null-geodesics; indexed p357 cites the billiards manuscript in preparation2020. Web full-text fetch returned403; one ordinary unauthenticated default urllib request returned429 and was not retried. Huber–Wüstholz public author preprint fetched200. No bypass occurred.

2026-10-06T03:28:11Z — Source-scope checkpoint. Completion estimate: 75%. Authenticated candidate and supplied-slide hashes. Parsed slide pages77–81 and earlier Humbert pages42–44; visually confirmed final H_{n²}/someN mismatch. Inspected §18.5 of the public author preprint and rendered printedpp168–170. Its general arithmetic period-space theorem does not supply the exact null geometry in the inspected scope. No full2020 manuscript or authentic thesis citation was located.

"""+now+""" — Final bounded audit checkpoint. Completion estimate:100% of assigned audit; historical-priority clearance remains unresolved. Saved REPORT.md, VERDICT.json, SEARCH_SCOPE.json and hash manifest. Exact formula duplication was not verified, but same-system earlier announcement and published null-motivated groundwork bar a blanket first-solution assertion. Next evidence: lawful full2021 paper and publicly released billiards manuscript/null proof, with exact J/differential/period/count mapping. Human-supplied lawful library access could help; no external communication or outreach text was prepared. Original1/5 unchanged; extra central proof-search turns0. Writes were confined to this folder; no Git/native/PR/editor/upload/tracker mutation.
"""
(root/'RESEARCH_LOG.md').write_text(log)
for p in root.rglob('*'):
    if p.is_file() and p.suffix in {'.md','.json','.py','.txt'} and ('private_sources' not in p.relative_to(root).parts or p.suffix=='.json'):
        body=p.read_text()
        bad=sorted(set(ord(c) for c in body if ord(c)<32 and c not in '\n\t'))
        if bad:
            raise RuntimeError(f'Control character in {p}: {bad}')
        if p.suffix=='.json':
            json.loads(body)
pins=[]
for rel in ['ROOT_MATHEMATICAL_GATE_20261006.json','original_source_authentication_20261006/original_attempt/ANALYTIC_CRITERION.md','original_source_authentication_20261006/original_attempt/prior_imported_report.json','primary_sources_20261006/wustholz2017.pdf','primary_sources_20261006/wustholz2017.txt']:
    p=base/rel
    pins.append({'path':'../'+rel,'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
files=[]
for p in sorted(root.rglob('*')):
    if p.is_file() and p.name!='MANIFEST.json':
        files.append({'path':str(p.relative_to(root)),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'private_third_party':p.relative_to(root).parts[0]=='private_sources'})
manifest={'schema':'priority-garcia-wustholz-manifest/v1','created_utc':now,'scope':'own assigned folder; third-party bodies private','input_pins':pins,'files':files,'file_count':len(files),'total_bytes':sum(x['bytes'] for x in files),'control_character_check':'authored files passed; original PDF extraction controls preserved in private text','json_parse_check':'passed','central_proof_search_turns':0}
(root/'MANIFEST.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({'completed_utc':now,'status':v['status'],'queries':s['query_count'],'files':len(files),'bytes':manifest['total_bytes'],'control_characters':'none','json':'all parsed'},indent=2))
