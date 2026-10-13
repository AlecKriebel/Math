#!/usr/bin/env python3
"""Pin this family's final evidence; verify frozen input bytes read-only."""
import hashlib
import json
from datetime import datetime,timezone
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    intake=json.loads((ROOT/'INTAKE.json').read_text())
    checked=[]
    for item in intake['files']:
        p=Path(item['local_path'])
        actual=digest(p)
        checked.append({'repository_path':item['repository_path'],'git_blob_oid':item['git_blob_oid'],
                        'sha256':actual,'matches_intake':actual==item['sha256'],
                        'byte_count':p.stat().st_size})
    artifacts={}
    for p in sorted(HERE.iterdir()):
        if p.is_file() and p.name!='MANIFEST.json':
            artifacts[p.name]={'sha256':digest(p),'byte_count':p.stat().st_size}
    out={'created_utc':datetime.now(timezone.utc).isoformat(),'family':'direct_geometry_adversary',
         'audit_completion_estimate_percent':100,'PR':259,'authentic_head':intake['original_inventory_and_current_head'],
         'intake_sha256':digest(ROOT/'INTAKE.json'),'frozen_submitted_body_count':len(checked),
         'all_frozen_submitted_hashes_match':all(x['matches_intake'] for x in checked),
         'frozen_submitted_bodies':checked,'artifacts':artifacts,
         'public_selection':sorted(artifacts),
         'public_selection_exclusions':'No external PDFs/full text; no caches; manifest omits its own recursive hash.',
         'no_Git_actions':True,'no_provider_writes':True,'no_external_individual_contact':True,
         'result':'No scoped theorem defect found; exact even-list odd-repeat extension counterexample; no priority verdict.'}
    (HERE/'MANIFEST.json').write_text(json.dumps(out,indent=2)+'\n')
    print('Pinned',len(artifacts),'family files; all',len(checked),'frozen submitted bodies match:',out['all_frozen_submitted_hashes_match'])


if __name__=='__main__':
    main()
