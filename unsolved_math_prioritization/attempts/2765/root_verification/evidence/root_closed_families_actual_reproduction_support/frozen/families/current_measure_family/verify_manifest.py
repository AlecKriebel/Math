#!/usr/bin/env python3
"""Check complete authored inventory, source pins, and optional ignored-cache inventory."""
from pathlib import Path
import hashlib,json,sys
ROOT=Path(__file__).resolve().parent
MANIFEST=ROOT/'artifact_manifest.json'
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def inventory(cache=False):
    rows=[]
    for path in sorted(ROOT.rglob('*')):
        if path.is_symlink():raise AssertionError('symlink not allowed: '+str(path))
        if not path.is_file() or path==MANIFEST:continue
        rel=path.relative_to(ROOT)
        is_cache=rel.parts[0]=='tmp'
        if is_cache!=cache:continue
        rows.append({'path':rel.as_posix(),'size':path.stat().st_size,'sha256':digest(path)})
    return rows
if len(sys.argv)>1 and sys.argv[1]=='--generate':
    from datetime import datetime,timezone
    packet={'schema':1,'time_utc':datetime.now(timezone.utc).isoformat(),'scope':'Every regular authored/copied/derived file recursively, except the self manifest. Ignored tmp is external-source/cache material inventoried separately and not publication content. No path allowlist.','frozen_head':'980719c79e13ffbc3f5cfbf149c325ea2fb51df0','frozen_base':'c6975ca76f9f667f1250ba403d0e6da2aafe14d0','snapshot_manifest_sha256':'2c58f3aa5f73920fa62c7103648deee899db3a12f3f48c940576f99eff74dfe2','authored_files':inventory(),'ignored_cache_files':inventory(True)}
    MANIFEST.write_text(json.dumps(packet,indent=2)+'\n')
    print(json.dumps({'generated':True,'authored_count':len(packet['authored_files']),'ignored_cache_count':len(packet['ignored_cache_files']),'manifest_sha256':digest(MANIFEST)},indent=2))
else:
    packet=json.loads(MANIFEST.read_text())
    assert packet['authored_files']==inventory(),'missing/extra/altered authored files'
    if (ROOT/'tmp').exists():assert packet['ignored_cache_files']==inventory(True),'missing/extra/altered ignored cache files'
    assert packet['frozen_head']=='980719c79e13ffbc3f5cfbf149c325ea2fb51df0'
    assert packet['frozen_base']=='c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
    assert digest(ROOT.parent/'snapshot_manifest.json')==packet['snapshot_manifest_sha256']
    assert digest(ROOT/'source_record_literal.json')=='0d6179bc1f850670535220113fb63b3f87e3cccc4223b94c6c2c3e211c2d421e'
    seal=json.loads((ROOT/'proof_seal.json').read_text())
    assert digest(ROOT/'independent_proofs.md')==seal['independent_proof_sha256']
    print(json.dumps({'status':'PASS','authored_count':len(packet['authored_files']),'ignored_cache_count':len(packet['ignored_cache_files']),'manifest_sha256':digest(MANIFEST),'self_excluded_only':MANIFEST.name,'no_authored_allowlist':True,'source_pins_match':True},indent=2))
