import json,os,pathlib,sys
sys.dont_write_bytecode=True
sys.path.insert(0,sys.argv[1])
from safe_output import write_new,Journal
base=pathlib.Path(sys.argv[2]); kind=sys.argv[3]; method=sys.argv[4]
victim=base/"victim"; leaf=base/"leaf"
write_new(victim,b"UNCHANGED")
j=Journal(leaf)
if method=="journal_update": j.save({"before":True}); leaf.unlink()
if kind=="symlink": leaf.symlink_to(victim)
else: os.link(victim,leaf)
rejected=False
try:
 if method=="first_write": write_new(leaf,b"NEW")
 else: j.save({"after":True})
except FileExistsError: rejected=True
if victim.read_bytes()!=b"UNCHANGED": raise RuntimeError("Victim changed")
if method=="journal_update":
 if rejected or json.loads(leaf.read_text())!={"after":True}: raise RuntimeError("Atomic replacement failed")
elif not rejected: raise RuntimeError("First creation followed alias")
print(json.dumps({"status":"PASS","victim_unchanged":True, "method":method,"link_type":kind}))
