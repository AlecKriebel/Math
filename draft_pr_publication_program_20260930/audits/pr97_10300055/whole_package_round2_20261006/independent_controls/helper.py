import sys,os,json,pathlib
sys.path.insert(0,sys.argv[1])
from safe_output import write_new,Journal,fresh_output
b=pathlib.Path(sys.argv[2]); kind=sys.argv[3]; action=sys.argv[4]
victim=b/"victim"; victim.write_bytes(b"UNCHANGED")
leaf=b/"leaf";j=Journal(leaf)
if action=="update":j.save({"old":1});leaf.unlink()
if kind=="symlink":leaf.symlink_to(victim)
elif kind=="hardlink":os.link(victim,leaf)
else:leaf.write_bytes(b"EXISTING")
blocked=False
try:
 if action=="bytes":write_new(leaf,b"CORRUPTED")
 else:j.save({"new":2})
except FileExistsError:blocked=True
if victim.read_bytes()!=b"UNCHANGED":raise RuntimeError("Victim changed")
if action=="update":
 if blocked or leaf.is_symlink() or json.loads(leaf.read_text())!={"new":2}:raise RuntimeError("Bad replacement")
elif not blocked:raise RuntimeError("Initial alias write accepted")
if list(b.glob(".journal-*")):raise RuntimeError("Temporary residue")
print(json.dumps({"PASS":True,"victim_unchanged":True,"action":action,"kind":kind}))
