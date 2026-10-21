from pathlib import Path
import subprocess,sys
T=Path("/Users/alec/Documents/Math/draft_pr_claimed_solved_700_800_20261012/audits/pr789_30001478/tmp");V=T/"verification_recipes"
s=(V/"ROOT_RELEASE_REPRODUCTION_V3.py").read_text().replace('root_release_reproduction_v3','root_release_reproduction_v4').replace('"ROOT_PORTABLE_V3_"','"ROOT_PORTABLE_V4_"').replace('V3_OPTIONAL_BODY_CUSTODY','V4_OPTIONAL_BODY_CUSTODY').replace('ROOT_RELEASE_REPRODUCTION_V3.json','ROOT_RELEASE_REPRODUCTION_V4.json')
(V/"ROOT_RELEASE_REPRODUCTION_V4.py").write_text(s)
s=(V/"ROOT_ARCHIVE_PORTABILITY_V3.py").read_text().replace('root_archive_portability_v3','root_archive_portability_v4').replace('ROOT_ARCHIVE_PORTABILITY_V3.json','ROOT_ARCHIVE_PORTABILITY_V4.json').replace('current_v3_optional_body_custody_receipt','current_v4_optional_body_custody_receipt').replace('V3_OPTIONAL_BODY_CUSTODY','V4_OPTIONAL_BODY_CUSTODY')
s=s.replace('the V3 change is bibliography endpoint and optional harness documentation only','the V4 change is canonical Handle metadata and manifest only').replace('Current V3 body custody','Current V4 body custody')
(V/"ROOT_ARCHIVE_PORTABILITY_V4.py").write_text(s)
for n in["ROOT_RELEASE_REPRODUCTION_V4.py","ROOT_ARCHIVE_PORTABILITY_V4.py"]:
 r=subprocess.run([sys.executable,"-I","-B",str(V/n)],capture_output=True,text=True,timeout=300)
 assert r.returncode==0,(r.stdout,r.stderr)
 print(r.stdout.strip())

