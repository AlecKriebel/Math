from pathlib import Path
import subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");V=T/"verification_recipes"
s=(V/"ROOT_RELEASE_REPRODUCTION_V2.py").read_text().replace('root_release_reproduction_v2','root_release_reproduction_v3').replace('"ROOT_PORTABLE_"','"ROOT_PORTABLE_V3_"').replace('V2_OPTIONAL_BODY_CUSTODY','V3_OPTIONAL_BODY_CUSTODY').replace('ROOT_RELEASE_REPRODUCTION_V2.json','ROOT_RELEASE_REPRODUCTION_V3.json')
(V/"ROOT_RELEASE_REPRODUCTION_V3.py").write_text(s)
s=(V/"ROOT_ARCHIVE_PORTABILITY_V2.py").read_text().replace('root_archive_portability_v2','root_archive_portability_v3').replace('ROOT_ARCHIVE_PORTABILITY_V2.json','ROOT_ARCHIVE_PORTABILITY_V3.json').replace('current_v2_optional_body_custody_receipt','current_v3_optional_body_custody_receipt').replace('V2_OPTIONAL_BODY_CUSTODY','V3_OPTIONAL_BODY_CUSTODY').replace('the V2 change is README only','the V3 change is bibliography endpoint and optional harness documentation only').replace('Current V2 body custody','Current V3 body custody')
(V/"ROOT_ARCHIVE_PORTABILITY_V3.py").write_text(s)
for n in ["ROOT_RELEASE_REPRODUCTION_V3.py","ROOT_ARCHIVE_PORTABILITY_V3.py"]:
 p=subprocess.run([sys.executable,"-I","-B",str(V/n)],capture_output=True,text=True,timeout=300)
 assert p.returncode==0,(p.stdout,p.stderr)
 print(p.stdout.strip())

