from pathlib import Path
import subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");V=T/"verification_recipes"
s=(V/"ROOT_ADMIN_V2_GUARD_REPLAY.py").read_text().replace("8d9d2c001634dffd3cedb9a3ebb513ceed62c0400f68e96d4028e9bfa3dbb5bb","702b8dbf1b6a71a8b721910d57a3bfdd1990e18d8b605eb2a4a0cdcd5445ded1").replace("5d7bccdc118a464da0e149804c4b512c88a9d28cbff2d8b3bc280d963dd4f348","50baca75de83bb4959f52b88762b020a65181428d200dffc4f343db8e026f9de").replace("ROOT_ADMIN_V2_","ROOT_ADMIN_V3_").replace("PASS_V2_ADMIN","PASS_V3_ADMIN")
(V/"ROOT_ADMIN_V3_GUARD_REPLAY.py").write_text(s)
r=subprocess.run([sys.executable,"-I","-B",str(V/"ROOT_ADMIN_V3_GUARD_REPLAY.py")],capture_output=True,text=True,timeout=180)
assert r.returncode==0,(r.stdout,r.stderr)
print(r.stdout.strip())

