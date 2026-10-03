#!/usr/bin/env python3
"""Portable runner; the original independent checker remains byte-identical."""
import json
from pathlib import Path
import independent_controls as c
c.PUB=Path(__file__).resolve().parent.parent
print(json.dumps({'integrity':c.integrity(),'homology':c.homology_controls(),'nonretraction':c.no_retraction(),
 'exterior_square':c.exterior_controls(),'attraction_gaps':c.core_and_gaps(),'periodic':c.periodic_controls()},indent=2))
