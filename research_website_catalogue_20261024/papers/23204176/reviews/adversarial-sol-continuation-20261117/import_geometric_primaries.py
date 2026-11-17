"""Copy inert classical primary evidence; no mathematical execution."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil
A=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23204176/reviews/adversarial-sol-continuation-20261117')
O=Path('/Users/alec/Documents/Math/openai_followon_k3_moduli_hodge/checks')
names={'seidel-quartic-v4.pdf':'package_review_1/ordinary_hms/seidel-quartic-v4.pdf',
       'abouzaid-faithful.pdf':'package_review_1/ordinary_hms/abouzaid-faithful.pdf',
       'FOOOChartsI1710.01459.pdf':'analytic_falsification/FOOOChartsI1710.01459.pdf',
       'FOOOChartsII1808.06106v2.pdf':'analytic_falsification/FOOOChartsII1808.06106v2.pdf',
       'FOOOGluing1603.07026v2.pdf':'analytic_falsification/FOOOGluing1603.07026v2.pdf',
       'AFOOO2606.12257v1.html':'analytic_falsification/AFOOO2606.12257v1.html'}
rows=[]
for name,relative in names.items():
    src=O/relative;b=src.read_bytes();dest=A/'classical-primary'/name;assert not dest.exists();shutil.copy2(src,dest)
    rows.append({'origin':str(src),'destination':str(dest.relative_to(A)),'bytes':len(b),'SHA256':hashlib.sha256(b).hexdigest(),'inert_primary_evidence_only':True})
(A/'GEOMETRIC_PRIMARY_RECEIPT.json').write_text(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'files':rows,'independent_primary_version_pages_checked':['https://arxiv.org/abs/math/0310414v4','https://ems.press/journals/jems/articles/14813','https://arxiv.org/abs/2606.12257v1'],'no_current_peer_findings_read':True},indent=2)+'\n')
print(json.dumps({'primary_files_copied':len(rows),'project_execution':False}))
