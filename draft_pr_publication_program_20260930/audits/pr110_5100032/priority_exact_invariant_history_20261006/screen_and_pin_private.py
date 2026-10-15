#!/usr/bin/env python3
"""Produce metadata only; never copy private source bodies to the public payload."""
from pathlib import Path
import hashlib, json, os, re, datetime
W=Path(__file__).resolve().parent
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
patterns={"literal_603":r"(?:k\s*[_{}]?\s*)?603", "antipedal":r"anti[ -]?pedal", "distance_sum_alias":r"sum.{0,40}distances|distances.{0,40}sum", "circumradius_alias":r"circumradi(?:us|i)"}
rows=[]
for base in (W/'private_sources',W/'private_review_materials'):
    for p in sorted(base.rglob('*')):
        if not p.is_file(): continue
        b=p.read_bytes()
        row={'path':str(p.relative_to(W)), 'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()}
        if p.suffix in ('.txt','.tex','.bib','.md'):
            body=b.decode('utf-8','replace')
            row['line_count']=len(body.splitlines())
            row['screen_counts']={k:len(re.findall(v,body,re.I)) for k,v in patterns.items()}
        rows.append(row)
out={'schema':'private-source-metadata-only/v1','UTC':utc,'actual_operator_PID':os.getpid(), 'scope':'Every locally downloaded private source and extraction. Search counts are discovery screens, never a proof of semantic absence. No private bodies are copied.', 'rows':rows}
(W/'PRIVATE_SOURCE_PINS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'UTC':utc,'actual_operator_PID':os.getpid(),'private_files':len(rows),'metadata_output':'PRIVATE_SOURCE_PINS.json'}))
