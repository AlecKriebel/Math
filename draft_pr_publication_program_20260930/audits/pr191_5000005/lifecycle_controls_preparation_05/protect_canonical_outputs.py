"""Mandatory guard for any future generator; no generator writes are supplied."""
from pathlib import Path
def require_new_outputs(directory,names):
 existing=[n for n in names if (Path(directory)/n).exists()]
 if existing:raise RuntimeError('Refuse overwriting audited canonical outputs: '+', '.join(existing))
