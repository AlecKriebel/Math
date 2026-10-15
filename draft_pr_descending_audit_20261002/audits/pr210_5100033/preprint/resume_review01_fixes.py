"""Resume the one-time review01 authoring after its logged redundant README assertion.

Earlier mutations and immutable review input are preserved; only the unexecuted
suffix is run. This is not a scientific-check failure or an automatic retry.
"""
from pathlib import Path
from datetime import datetime,timezone
import runpy,textwrap,hashlib,json
B=Path(__file__).resolve().parent
p=B/'apply_review01_fixes.py'
ns=runpy.run_path(str(p),run_name='review01_authoring_definitions_only')
ns['now']=datetime.now(timezone.utc).isoformat()
s=p.read_text()
start=s.index("    change(V/'README.md','Even-period products vary in the negative'")
end=s.index("\n\nif __name__=='__main__':")
assert (B/'history/review01_frozen/apply_review01_fixes_initial_failed.py').is_file()
assert not (B/'REVIEW01_RESOLUTION.json').exists(),'Suffix already completed: inspect, do not repeat.'
exec(compile('def resume_unexecuted_suffix():\n'+s[start:end]+'\nresume_unexecuted_suffix()\n',str(p)+'[unexecuted_suffix]','exec'),ns)
