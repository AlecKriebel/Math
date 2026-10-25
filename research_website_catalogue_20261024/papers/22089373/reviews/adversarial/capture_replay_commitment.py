#!/usr/bin/env python3
"""Retain the active full replay's own generated commitment before its cleanup."""
from pathlib import Path
import json,time,hashlib
from datetime import datetime,timezone
base=Path(__file__).parent
source=base/'cache/tmp/stc-jc-proof-bundle-nbvq9wib/commitment-0.json'
deadline=time.monotonic()+3600
while time.monotonic()<deadline:
 if source.exists():
  data=source.read_bytes()
  try:json.loads(data)
  except json.JSONDecodeError:time.sleep(.2);continue
  target=base/'full_replay_commitment.json';target.write_bytes(data)
  receipt={'captured_utc':datetime.now(timezone.utc).isoformat(),'source':str(source.resolve()),'target':str(target.resolve()),'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data),'note':'Copied generated evidence bytes only; no replay source, payload or process modified.'}
  base.joinpath('full_replay_capture_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
  print(json.dumps(receipt));break
 if not source.parent.exists():raise SystemExit('Replay directory vanished before commitment capture')
 time.sleep(.5)
else:raise SystemExit('Commitment capture timed out after one hour')
