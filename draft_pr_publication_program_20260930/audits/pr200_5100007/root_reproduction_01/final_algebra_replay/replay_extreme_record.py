"""Retest the extreme orbit from the separately serialized175digit resonance."""
from pathlib import Path
import json,runpy
root=Path(__file__).resolve().parent
g=runpy.run_path(str(root/"independent_geometry.py"));mp=g['mp']
row=json.loads((root/'extreme_resonance_record.json').read_text())
g['one_case'](mp.mpf(10),mp.mpf(1),64,31,lam_override=mp.mpf(row['lambda']))
print('PASS extreme175digit serialization replay, explicit exceptions')
