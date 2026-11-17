"""Authenticate and copy declared primary files as inert evidence only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
A=P/'papers/23204176/reviews/adversarial-sol-continuation-20261117'
N=P/'papers/23204176/sources/archives/01-source-and-verification.zip.extracted'
ORIGIN=Path('/Users/alec/Documents/Math/openai_followon_k3_moduli_hodge/sources')
manifest=json.loads((N/'UPSTREAM_MANIFEST.json').read_text());rows=[]
for row in manifest['files']:
    path=Path(row['path']);assert not path.is_absolute() and '..' not in path.parts
    src=ORIGIN/'pinned'/path;b=src.read_bytes();h=hashlib.sha256(b).hexdigest()
    assert len(b)==row['bytes'] and h==row['sha256'],row['path']
    dest=A/'primary-pinned'/path;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
    assert dest.read_bytes()==b;rows.append(row)
for name in ['bulles_1806.08284v1.pdf','bulles_markman_math0009109.pdf','bulles_arapura_math0102070v5.pdf']:
    src=ORIGIN/'downloads'/name;b=src.read_bytes();dest=A/'classical-primary'/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dest)
    rows.append({'path':str(dest.relative_to(A)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest(),'origin':str(src),'version_claim':'Filename/history claim to check against actual PDF; no theorem adoption from this label'})
(A/'PRIMARY_IMPORT_RECEIPT.json').write_text(json.dumps({'UTC':datetime.now(timezone.utc).isoformat(),'pinned_commit':manifest['pinned_commit'],'pinned_files':len(manifest['files']),'files':rows,'execution_of_imported_material':False},indent=2)+'\n')
print(json.dumps({'pinned_files':len(manifest['files']),'additional_classical_PDFs':3,'all_declared_pins_exact':True}))
