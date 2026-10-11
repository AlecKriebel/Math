"""Extract literal newly-added science from captured diff; authenticate Git blob IDs."""
from pathlib import Path
import datetime
import hashlib
import json
import re

F = Path(__file__).resolve().parent
HEAD = '8006dd5f134ad0a2fa930e7278d3cb17945f4201'
PREFIX = 'unsolved_math_prioritization/attempts/30000166/'


def load(name):
    return json.loads((F/'captures'/name/'STDOUT.bin').read_bytes())


def git_blob(b):
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()


meta, compare = load('pr_metadata'), load('pr_compare')
assert meta['headRefOid'] == compare['head_sha'] == HEAD
assert meta['headRefName'] == 'dot/math-30000166'
assert compare['base_sha'] == compare['merge_base_sha'] == meta['baseRefOid']
directory, review = load('science_directory_quoted'), load('review_directory')
api_files = [q for q in directory if q['type']=='file'] + review
assert len(api_files)==15 and all(q['type']=='file' for q in api_files)
expected = {q['path']: q for q in api_files}
assert len(expected)==15
assert set(expected)=={q['filename'] for q in compare['files'] if q['filename'].startswith(PREFIX)}
assert len(compare['files'])==16
diff_path = F/'captures'/'pr_full_diff'/'STDOUT.bin'
diff = diff_path.read_bytes()
sections = re.split(br'(?m)(?=^diff --git )',diff)
extracted = {}
for section in sections:
    if not section: continue
    lines = section.splitlines(keepends=True)
    m = re.fullmatch(br'diff --git a/(\S+) b/(\S+)\n', lines[0])
    assert m and m.group(1)==m.group(2)
    path = m.group(1).decode()
    if not path.startswith(PREFIX): continue
    mode = next(x.split()[-1].decode() for x in lines if x.startswith(b'new file mode '))
    assert mode in ('100644','100755')
    assert any(x.startswith(b'--- /dev/null') for x in lines)
    h = next(i for i,x in enumerate(lines) if x.startswith(b'@@ '))
    body=[]
    for line in lines[h+1:]:
        if line.startswith(b'+'): body.append(line[1:])
        elif line.startswith(b'\\ No newline at end of file'):
            assert body and body[-1].endswith(b'\n');body[-1]=body[-1][:-1]
        else: raise AssertionError(('unexpected added-file hunk',path,line[:40]))
    b=b''.join(body)
    q=expected[path]
    assert len(b)==q['size'] and git_blob(b)==q['sha']
    assert path not in extracted
    extracted[path]=(b,mode)
assert set(extracted)==set(expected)
out=F/'source_snapshot';out.mkdir()
rows=[]
for path,(b,mode) in sorted(extracted.items()):
    relative=path[len(PREFIX):]
    target=out/relative;target.parent.mkdir(parents=True,exist_ok=True)
    with target.open('xb') as t:t.write(b)
    target.chmod(0o755 if mode=='100755' else 0o644)
    rows.append({'repository_path':path,'snapshot_relative_path':relative,
                 'git_mode':mode,'bytes':len(b),'git_blob_sha1':git_blob(b),
                 'sha256':hashlib.sha256(b).hexdigest()})
receipt={'schema':'pr51-original-literal-snapshot/v1',
         'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'original_head':HEAD,'original_head_tree':load('original_commit_metadata')['tree']['sha'],
         'base':compare['base_sha'],'merge_base':compare['merge_base_sha'],
         'branch':meta['headRefName'],'science_prefix':PREFIX,
         'capture_diff':{'path':str(diff_path),'bytes':len(diff),'sha256':hashlib.sha256(diff).hexdigest()},
         'changed_paths_count':len(compare['files']),'science_files_count':len(rows),
         'science_bytes':sum(q['bytes'] for q in rows),'files':rows,
         'archive_mode_semantics':'Git modes retained in metadata; later read-only audit storage does not claim original filesystem modes.'}
(F/'SNAPSHOT_IDENTITY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
