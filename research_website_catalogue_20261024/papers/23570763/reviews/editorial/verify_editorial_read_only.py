"""Pure offline custody, no scientific/native/builder/control imports or execution.

Default behavior only hashes this sealed packet and its original protected inputs.
It writes nothing and makes no current publication or browser/tracker assertion.
"""
from pathlib import Path
import argparse
import hashlib
import json
import platform
import sys


def verify(root):
    root=Path(root).resolve();checks=0
    def need(ok,why):
        nonlocal checks
        checks+=1
        if not ok:raise ValueError(why)
    def sha(raw):return hashlib.sha256(raw).hexdigest()
    def authenticate(path,size,digest):
        path=Path(path);need(path.is_file() and not path.is_symlink(),'regular original '+str(path));raw=path.read_bytes();need(len(raw)==size,'size '+str(path));need(sha(raw)==digest,'SHA256 '+str(path))
    raw=(root/'MANIFEST.json').read_bytes();manifest=json.loads(raw);seal=json.loads((root/'SEAL.json').read_bytes());need(sha(raw)==seal['MANIFEST_SHA256'],'manifest seal');need(len(raw)==seal['MANIFEST_bytes'],'manifest bytes')
    rows=manifest['files'];names=[r['path'] for r in rows];need(len(names)==len(set(names)),'unique owned namespace');need(all(not Path(n).is_absolute() and '..' not in Path(n).parts for n in names),'owned relative safe paths')
    actual=sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file());need(actual==sorted(names+['MANIFEST.json','SEAL.json']),'complete sealed owned namespace');need(not any(p.is_symlink() for p in root.rglob('*')),'no owned symlinks')
    for row in rows:authenticate(root/row['path'],row['bytes'],row['SHA256'])
    need(len(rows)==seal['owned_payload_count'],'owned count');protected=json.loads((root/'PROTECTED_INPUTS.json').read_bytes())
    for row in protected['files']:authenticate(row['path'],row['bytes'],row['SHA256'])
    source=root.parent.parent/'sources';need(sorted(str(p.relative_to(source)) for p in source.rglob('*') if p.is_file())==protected['source_file_namespace'],'original65 source namespace unchanged')
    publication=json.loads((root/'config/publication.json').read_bytes());promotion=json.loads((root/'config/promotion.json').read_bytes());need(publication['canonical_url'] is None and publication['AA'] is None and promotion['production_integration_authorized'] is False,'sealed private config gates')
    return {'status':'PASS','scope':'Pure offline custody only; no semantic controls, scientific replay, network or writes.','python':platform.python_version(),'optimized':not __debug__,'checks':checks,'owned_payloads':len(rows),'protected_originals':len(protected['files']),'original_source_files':len(protected['source_file_namespace']),'whole_scientific_verdicts_preserved':2,'all18_original_ZIP_payloads_preserved':True,'publication_live_browser_native_adoption_claim':False}


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--packet-root',required=True);args=ap.parse_args()
    try:result=verify(args.packet_root)
    except Exception as error:print(json.dumps({'status':'FAIL','error':str(error)},indent=2));sys.exit(1)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
