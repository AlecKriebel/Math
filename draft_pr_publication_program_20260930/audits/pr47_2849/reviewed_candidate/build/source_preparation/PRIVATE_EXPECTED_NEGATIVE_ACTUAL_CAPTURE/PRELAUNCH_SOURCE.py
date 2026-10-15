"""Intentional private class-substitution failure; no production execution."""
import json
from pathlib import Path
import private_capture_class_controls_v2 as predicates
F=Path(__file__).absolute().parent; A=F.parent
s=json.loads((A/'root_original_actual_reproduction/ROOT_REPRODUCTION_RESULT.json').read_bytes())
c=dict(s['complete_actual_Git_captures'][0]); c['source']=s['complete_actual_helper_captures'][0]['source']; c['source_unchanged']=True
predicates.validate(c,'git',s['complete_actual_Git_captures'][0]['argv'],None,s['actual_operator_pid'])
raise ValueError('Intentional invalid helper substitution was incorrectly accepted')
