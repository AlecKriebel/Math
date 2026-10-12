from pathlib import Path
from datetime import datetime, timezone
import importlib.util, hashlib, json, subprocess
A=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('readonly_api',str(A.parent/'pr156_30005432/prepare_scoped_merge.py'))
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
def save(name,obj):
    p=A/'root_priority'/name;p.write_text(json.dumps(obj,indent=2)+'\n');return p
def main():
    utc=datetime.now(timezone.utc).isoformat()
    raw=subprocess.run(['/opt/homebrew/Cellar/gh/2.85.0/bin/gh','api','repos/AlecKriebel/Math','--method','GET'],capture_output=True,text=True,timeout=60)
    m.require(raw.returncode==0,raw.stderr[:1000])
    repo=json.loads(raw.stdout)
    pr=m.api('pulls/166')
    commit=m.api('commits/efc3f35a72543ad9ae76fd31a860116f1ffd4a32')
    mainref=m.api('git/ref/heads/main')
    m.require(repo.get('private') is False,'Repository current visibility public')
    m.require(pr['head']['sha']=='efc3f35a72543ad9ae76fd31a860116f1ffd4a32','Head changed')
    save('ACTUAL_REPOSITORY_METADATA.json',repo)
    save('ACTUAL_PR_METADATA.json',pr)
    save('ORIGINAL_COMMIT_METADATA.json',commit)
    save('ACTUAL_MAIN_READONLY_SNAPSHOT.json',mainref)
    timeline=dict(UTC=utc,pr=166,original_head=pr['head']['sha'],repository_currently_public=not repo['private'],
     PR_created_utc=pr['created_at'],PR_state=pr['state'],PR_draft=pr['draft'],
     commit_author_timestamp=commit['commit']['author']['date'],commit_committer_timestamp=commit['commit']['committer']['date'],
     actual_MAIN_snapshot=mainref['object']['sha'],
     limits='Git commit timestamps are metadata, not proof of the exact upload time or continuous public visibility. The server-side PR creation timestamp is a stronger disclosure observation; no archival capture or independence certificate is inferred.',
     no_mutations=True)
    p=save('GITHUB_DISCLOSURE_TIMELINE.json',timeline)
    print(json.dumps(timeline,indent=2))
if __name__=='__main__':main()
