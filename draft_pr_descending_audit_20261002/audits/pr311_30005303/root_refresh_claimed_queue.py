"""After clean whole review, refresh only PR311 using immutable Git objects."""
from root_submission_gate import *
import time

window()
clear = current_clearance()
assert not (A/'queue_repair_receipt.json').exists()
assert not (A/'BRANCH_REFRESH_ATTEMPT.json').exists(), 'Inspect any earlier uncertain mutation before retry.'
cap = Capture('branch_refresh')
assert cap.git('branch','--show-current') == b'main\n'
assert not cap.git('diff','--cached','--raw','-z')
assert cap.run('no_active_merge',['/usr/bin/git','rev-parse','-q','--verify','MERGE_HEAD'],ok=(1,)).returncode == 1
index = Path(cap.git('rev-parse','--git-path','index').decode().strip())
if not index.is_absolute():
    index = R/index
index_before = index.read_bytes()
local = cap.git('rev-parse','HEAD').decode().strip()
dirty_before = dirty_tracked(cap)
pr = json.loads(cap.run('pr_before',['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/311']).stdout)
assert pr['state'] == 'open' and pr['draft'] and pr['head']['sha'] == ORIGINAL_HEAD and pr['head']['ref'] == BRANCH
files = json.loads(cap.run('original_files',['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/311/files?per_page=100']).stdout)
original = load(A/'snapshot_manifest.json')
assert len(files) == len(original['files']) == 30
assert {(f['filename'],f['sha']) for f in files} == {(e['path'],e['git_blob_sha']) for e in original['files']}
window()
cap.git('fetch','origin','main')
base = cap.git('rev-parse','origin/main').decode().strip()
assert base == local
for e in original['files']:
    b = cap.git('show',ORIGINAL_HEAD+':'+e['path'])
    assert len(b) == e['bytes'] and sha(b) == e['sha256']
    assert cap.git('ls-tree',ORIGINAL_HEAD,'--',e['path']).split(b'\t',1)[0].split() == [b'100644',b'blob',e['git_blob_sha'].encode()]
frozen = cap.git('show',ORIGINAL_HEAD+':'+QUEUE).splitlines(keepends=True)
fc = frozen[ownrow(frozen)].split(b'|')
assert [fc[j].strip() for j in (8,9)] == [b'claimed_solved',b'2/5']
raw = cap.git('show',base+':'+QUEUE)
lines = raw.splitlines(keepends=True)
i = ownrow(lines)
before = lines[i]
cells = before.split(b'|')
assert [cells[j].strip() for j in (8,9)] == [b'queued',b'0/5']
for j in (8,9):
    cells[j] = fc[j]
cells[11] = b' '+cells[11].strip()+b' Accepted all-graph binary MTP2 original-edge closure and attractive-approximation theorem; zero supports and literal isolated/empty conventions included. C2/C3 negative witness credited to Gandolfi-Lenarda (published 13 April 2017). Research note and portable verification package cleared by successive new full AI reviews after global provenance/count corrections; bounded priority, extensive AI use, unrefereed. '
assert [j for j,(a,b) in enumerate(zip(before.split(b'|'),cells)) if a != b] == [8,9,11]
lines[i] = b'|'.join(cells)
new = b''.join(lines)
tree = cap.git('show','-s','--format=%T',base).decode().strip()

def replace(t,parts,blob):
    entries = {}
    for item in cap.git('ls-tree','-z',t).split(b'\0'):
        if item:
            meta,name = item.split(b'\t',1)
            entries[name] = tuple(meta.split())
    name = parts[0].encode()
    prior = entries.get(name)
    if len(parts) == 1:
        if prior:
            assert prior[:2] == (b'100644',b'blob')
        entries[name] = (b'100644',b'blob',blob.encode())
    else:
        if prior:
            assert prior[:2] == (b'040000',b'tree')
            child = prior[2].decode()
        else:
            child = cap.git('mktree','-z',input=b'').decode().strip()
        entries[name] = (b'040000',b'tree',replace(child,parts[1:],blob).encode())
    window()
    return cap.git('mktree','-z',input=b''.join(b' '.join(entries[n])+b'\t'+n+b'\0' for n in sorted(entries))).decode().strip()

for e in original['files']:
    if e['path'] != QUEUE:
        assert not cap.git('ls-tree',base,'--',e['path']), 'Attempt already exists; independently reconcile.'
        tree = replace(tree,e['path'].split('/'),e['git_blob_sha'])
window()
queue_blob = cap.git('hash-object','-w','--stdin',input=new).decode().strip()
tree = replace(tree,QUEUE.split('/'),queue_blob)
audit_rel = '../../../draft_pr_descending_audit_20261002/audits/pr311_30005303/'
release = (
    '# Accepted research note: binary MTP2 edge-model closure\n\n'
    'Target: 30005303 / OWR-11695865-001, the two binary factorization questions in Lauritzen\u2019s 2022 contribution. The original author budget remains **2/5**; subsequent work is independent verification, priority comparison and publication preparation. The separate Gaussian coordinate-descent question is outside this target.\n\n'
    'The accepted theorem proves that, for every finite binary graph, globally MTP2 laws with finite nonnegative unary and original-edge factors form a closed set and are exactly the limits of positive attractive Ising laws on those same edges. The proof includes pins, equality blocks, arbitrary zero supports, isolated vertices and empty graphs. A separate corollary handles the source\u2019s literal edge-only convention. This answers source Conjecture 1 affirmatively.\n\n'
    'The negative witness for Conjectures 2 and 3 is already present, up to a graph-preserving coordinate rotation, in Gandolfi\u2013Lenarda, Lemma 5.2, DOI 10.2140/memocs.2016.4.407, published 13 April 2017 in the nominal 2016 issue. The C6 example is a lift of the same construction. Neither is claimed as a new counterexample. The note credits Geiger\u2013Meek\u2013Sturmfels, Lauritzen\u2013Uhler\u2013Zwiernik, Fallat and coauthors, Kahle\u2013Sullivant and the classical graph-cut tools. The general all-support original-edge characterization is presented as an explicitly attributed extension and deduction. The bounded primary-source audit does not certify historical first discovery or worldwide continuing openness.\n\n'
    'Independent mathematical approach families, priority adversaries and successive NEW whole-preprint reviews checked the proofs, boundary cases, references, code, data, metadata, portable archive and page layout. The first whole review found verification-count and build-provenance label defects; these were corrected globally before a new whole review. Historical adverse findings and all original author records are preserved. The 29 original attempt files are byte-identical to submitted head '+ORIGINAL_HEAD+'. Their historical priority-unverified summary is superseded by this current note and the linked audit.\n\n'
    'AI tools were used extensively in solving, drafting and verification. This is an **unrefereed preprint**, without independent external human peer review or proof-assistant certification. Finite verification controls illustrate the unrestricted proofs; they are not an all-graph computational certificate.\n\n'
    'Author: Alec Kriebel, Independent researcher, ORCID https://orcid.org/0009-0001-9320-500X. License: CC BY 4.0.\n\n'
    'Current files:\n\n'
    '- [Research note (PDF)]('+audit_rel+'submission_v02/mtp2-edge-closure-note.pdf)\n'
    '- [Editable LaTeX source]('+audit_rel+'submission_v02/mtp2-edge-closure-note.tex)\n'
    '- [Portable verification package]('+audit_rel+'submission_v02/mtp2-edge-closure-verification.zip)\n'
    '- [Exact deposit metadata]('+audit_rel+'submission_v02/zenodo-deposit.json)\n'
    '- [Publishing clearance]('+audit_rel+'PUBLISHING_CLEARANCE.json)\n'
    '- [Current corrections]('+audit_rel+'CURRENT_CORRECTIONS.json)\n\n'
    'Production deposit, public DOI and exact tracker registration are recorded after successful execution in the audit\u2019s current status and publication receipts.\n\n'
    'Cleared formal artifact fingerprints:\n\n'+''.join('- '+n+': '+str(e['bytes'])+' bytes; SHA256 '+e['sha256']+'\n' for n,e in clear['formal_submission_files'].items())
).encode()
assert not cap.git('ls-tree',base,'--',RELEASE)
window()
release_blob = cap.git('hash-object','-w','--stdin',input=release).decode().strip()
tree = replace(tree,RELEASE.split('/'),release_blob)
expected = {e['path'] for e in original['files']} | {RELEASE}
assert len(expected) == 31 and set(cap.git('diff','--name-only',base,tree).decode().splitlines()) == expected
assert cap.git('show',tree+':'+QUEUE) == new
for e in original['files']:
    if e['path'] != QUEUE:
        b = cap.git('show',tree+':'+e['path'])
        assert len(b) == e['bytes'] and sha(b) == e['sha256']
for n,e in clear['formal_submission_files'].items():
    p = str((O/n).relative_to(R))
    assert cap.git('show',tree+':'+p) == (O/n).read_bytes() == cap.git('show',base+':'+p)
current_clearance()
assert cap.git('rev-parse','HEAD').decode().strip() == local and index.read_bytes() == index_before and dirty_tracked(cap) == dirty_before
remote = json.loads(cap.run('main_before_push',['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/git/ref/heads/main']).stdout)
assert remote['object']['sha'] == base
window()
commit = cap.git('commit-tree',tree,'-p',ORIGINAL_HEAD,'-p',base,
    input=b'Refresh PR311 on current main; preserve original packet and qualify reviewed MTP2 note\n').decode().strip()
(A/'BRANCH_REFRESH_ATTEMPT.json').write_text(json.dumps({'utc':utc(),'original_head':ORIGINAL_HEAD,'base':base,'commit':commit,'tree':tree,'capture_directory':str(cap.directory)},indent=2)+'\n')
window()
cap.git('push','origin',commit+':refs/heads/'+BRANCH)
assert cap.git('rev-parse','HEAD').decode().strip() == local and index.read_bytes() == index_before and dirty_tracked(cap) == dirty_before
for j in range(6):
    after = json.loads(cap.run('pr_after_'+str(j),['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/pulls/311']).stdout)
    if after['head']['sha'] == commit:
        break
    time.sleep(.5)
assert after['state'] == 'open' and after['head']['sha'] == commit and after['head']['ref'] == BRANCH
S = A/'repaired_snapshot'
assert not S.exists()
repaired = []
for p in sorted(expected):
    b = cap.git('show',commit+':'+p)
    f = S/p
    f.parent.mkdir(parents=True,exist_ok=True)
    f.write_bytes(b)
    f.chmod(0o644)
    meta = cap.git('ls-tree',commit,'--',p).split(b'\t',1)[0].split()
    assert meta[:2] == [b'100644',b'blob']
    repaired.append({'path':p,'bytes':len(b),'sha256':sha(b),'git_blob_sha':meta[2].decode(),'mode':'100644'})
(A/'repaired_snapshot_manifest.json').write_text(json.dumps({'pr':311,'head':commit,'base':base,'original_frozen_head':ORIGINAL_HEAD,'utc':utc(),'files':repaired},indent=2)+'\n')
receipt = {'utc':utc(),'status':'PASS_CLAIMED_SOLVED_QUEUE_REFRESH','pr':311,'original_head':ORIGINAL_HEAD,
           'repaired_head':commit,'base':base,'tree':tree,'parents':[ORIGINAL_HEAD,base],
           'original29_unchanged':True,'formal5_preexisting_exact':True,
           'old_row':before.decode(),'new_row':lines[i].decode(),'queue_only_pipe_cells':[8,9,11],
           'all_other_queue_bytes_preserved':True,'native_state_history_unchanged':True,
           'original_two_turn_ledgers_preserved_without_extra_search':True,
           'main_checkout_entire_index_dirty_bodies_modes_unchanged':True,
           'nonforce_branch_push':True,'capture_directory':str(cap.directory),'workflow_percent':80}
(A/'queue_repair_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
