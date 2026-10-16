"""Seal the first stage without classifying downloaded sources as our authorship."""
import datetime, hashlib, json, pathlib
ROOT=pathlib.Path(__file__).resolve().parent
source=(ROOT/'fetch_primary.py').read_text()
v1=source.replace("if len(sys.argv)>1:\n    sources=json.loads((ROOT/sys.argv[1]).read_text())\n",'').replace("(ROOT/(sys.argv[2] if len(sys.argv)>2 else 'primary_fetch_inventory.json')).write_text", "(ROOT/'primary_fetch_inventory.json').write_text")
archive=ROOT/'control_sources'
archive.mkdir(exist_ok=True)
(archive/'fetch_primary_initial.py').write_text(v1)
assert hashlib.sha256(v1.encode()).hexdigest()=='93c4357b8c91cfd68488f17937174e819ca5e431bec4af73fde3b76b037d3ed3'
(archive/'fetch_primary_round2_and3.py').write_text(source)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
(ROOT/'research_log.md').write_text(f'''# Literal geometry family research log

2026-10-02T22:05:41Z: Started literal source-only stage. Scientific completion
estimate: 0%; audit-stage estimate: 0%. Root instructions and pinned source read.

2026-10-02T22:07:28Z: Actual current Bloom source captured; raw dated triage and
unexpected candidate-adjacent search snippet exposure disclosed. Scientific
estimate: 2%; audit-stage estimate: 15%. Full original proofs unavailable so far.

2026-10-02T22:12:18Z: Exact controls completed with preserved PID/time/streams.
Checked exact line-family maximum, elementary pair-center square-root defect,
g(2),g(3),g(4). Scientific estimate: 5%; audit-stage estimate: 30%. No asymptotic
solution. Original paper limits and accidental exposure documented.

{now}: Initial first-party scope/geometry seal. Scientific estimate: 5%;
audit-stage estimate: 35%. Ready for immutable original candidate snapshot.
No original attempts or audit turns added; no canonical index or Git edits.
''')
def entry(path):
 data=path.read_bytes()
 return {'path':str(path.relative_to(ROOT)),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
files=sorted(p for p in ROOT.rglob('*') if p.is_file() and p.name!='initial_seal.json')
first=[entry(p) for p in files if 'foreign_primary' not in p.relative_to(ROOT).parts]
foreign=[entry(p) for p in files if 'foreign_primary' in p.relative_to(ROOT).parts]
seal={'sealed_utc':now,'scientific_completion_percent':5,'audit_completion_percent':35,
      'scope':'literal source and primary-access limits plus checkable independent geometry before candidate snapshot',
      'independence_limit':'unrequested candidate-adjacent search snippets exposed; circles not asserted exposure-independent',
      'substantive_attempt_increment':0,'original_audit_turn_increment':0,
      'first_party_closed_files':first,'foreign_primary_excluded_files':foreign,
      'self_exclusion':'initial_seal.json does not hash itself; this file is the seal record'}
(ROOT/'initial_seal.json').write_text(json.dumps(seal,indent=2)+'\n')
print(json.dumps({'sealed_utc':now,'first_party_count':len(first),'foreign_count':len(foreign),
 'seal_sha256':hashlib.sha256((ROOT/'initial_seal.json').read_bytes()).hexdigest()},indent=2))
