#!/usr/bin/env python3
"""Compare current own bodies/modes with parent's earlier external inventories."""
from pathlib import Path
import hashlib
import json
import stat
R=Path(__file__).resolve().parents[1]
D=R/'evidence/stage_integrity'
D.mkdir(parents=True,exist_ok=True)
results=[]
for name in ['ROOT_PREPRINT01_SOURCE_GATE.json','ROOT_PREPRINT01_FIRST_CANDIDATE_GATE.json']:
    original=(R.parent/name).read_bytes()
    own=D/name
    assert not own.exists(),name+' would overwrite evidence'
    own.write_bytes(original)
    assert (R.parent/name).read_bytes()==original
    gate=json.loads(original)
    rows=[]
    for rec in gate['payloads']:
        rel=Path(rec['path'])
        assert not rel.is_absolute() and '..' not in rel.parts
        path=R/rel
        assert path.is_file() and not path.is_symlink(),str(rel)
        body=path.read_bytes()
        assert stat.S_IMODE(path.stat().st_mode)==rec['mode_decimal'],str(rel)+' mode'
        if str(rel)=='RESEARCH_LOG.md':
            assert len(body)>=rec['bytes'] and hashlib.sha256(body[:rec['bytes']]).hexdigest()==rec['sha256'],'Log prefix changed'
            rows.append(dict(path=str(rel),status='append-only old prefix exact',old_bytes=rec['bytes'],current_bytes=len(body)))
        else:
            assert len(body)==rec['bytes'] and hashlib.sha256(body).hexdigest()==rec['sha256'],str(rel)+' body'
            rows.append(dict(path=str(rel),status='exact body and mode unchanged'))
    for rel,mode in gate['directory_modes'].items():
        assert stat.S_IMODE((R/rel).stat().st_mode)==mode,rel+' directory mode'
    results.append(dict(external_inventory=name,external_inventory_sha256=hashlib.sha256(original).hexdigest(),payloads=len(rows),directory_modes=len(gate['directory_modes']),results=rows))
print(json.dumps(dict(status='PASS_PRIOR_FREEZE_INTEGRITY',source_and_first_candidate_bodies_modes_unchanged=True,research_log_append_only=True,external_inventories_are_historical_pin_evidence_not_mathematical_validation=True,results=results),indent=2))
