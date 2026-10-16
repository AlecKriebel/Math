#!/usr/bin/env python3
"""Read-only audit of prepared PR278 objects. Outputs only in this directory."""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
RESUME = ROOT.parent
CASE = RESUME.parent
RECON = RESUME / 'reconciliation'
STORE = RESUME / 'objects.git'
AUTHOR = 'c5252db6ec25ffdbfd2259bfdcf2fb6228e1846e'
BASELINE = '8805848f1bc2cb2ff8d18517225ba6e3aa12013c'
TARGET = b'unsolved_math_prioritization/attempts/30005468'
QUEUE = b'unsolved_math_prioritization/QUEUE.md'

def require(condition, label):
    if not condition:
        raise ValueError(label)

def oid(kind, body):
    return hashlib.sha1(kind.encode() + b' ' + str(len(body)).encode() + b'\0' + body).hexdigest()

def pin(path):
    body = path.read_bytes()
    return dict(path=str(path), bytes=len(body), sha256=hashlib.sha256(body).hexdigest())

class Reader:
    def __init__(self):
        self.cache = {}
        env = {k:v for k,v in os.environ.items() if not k.startswith('GIT_')}
        env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null',
                   GIT_NO_LAZY_FETCH='1', GIT_TERMINAL_PROMPT='0',
                   GIT_OBJECT_DIRECTORY=str(RECON / 'private_objects'),
                   GIT_ALTERNATE_OBJECT_DIRECTORIES=str(STORE / 'objects'))
        self.proc = subprocess.Popen(['git', '--no-replace-objects', '--git-dir', str(STORE),
                                      'cat-file', '--batch'], env=env, stdin=subprocess.PIPE,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def get(self, sha):
        if sha not in self.cache:
            self.proc.stdin.write(sha.encode()+b'\n')
            self.proc.stdin.flush()
            header = self.proc.stdout.readline().split()
            require(len(header)==3 and header[0].decode()==sha, 'Missing object '+sha)
            body = self.proc.stdout.read(int(header[2]))
            require(self.proc.stdout.read(1)==b'\n', 'Bad cat-file framing')
            kind = header[1].decode()
            require(oid(kind,body)==sha, 'Raw SHA mismatch '+sha)
            self.cache[sha]=(kind,body)
        return self.cache[sha]

    def close(self):
        self.proc.stdin.close()
        require(self.proc.wait(timeout=10)==0, 'Object reader failed')

def parse_tree(body):
    result = {}
    pos = 0
    names = []
    while pos < len(body):
        sep = body.index(b' ',pos)
        nul = body.index(b'\0',sep+1)
        mode = body[pos:sep]
        name = body[sep+1:nul]
        rawsha = body[nul+1:nul+21]
        require(mode in (b'40000',b'100644',b'100755',b'120000',b'160000'), 'Noncanonical mode')
        require(name and b'/' not in name and name not in result and len(rawsha)==20, 'Malformed tree')
        result[name]=(mode,rawsha.hex())
        names.append(name)
        pos = nul+21
    require(pos==len(body), 'Tree framing')
    require(names==sorted(names,key=lambda n:n+(b'/' if result[n][0]==b'40000' else b'')), 'Tree order')
    return result

def encode_tree(entries):
    keys = sorted(entries,key=lambda n:n+(b'/' if entries[n][0]==b'40000' else b''))
    return b''.join(entries[n][0]+b' '+n+b'\0'+bytes.fromhex(entries[n][1]) for n in keys)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate',default=str(RECON/'baseline_8805848_v2'))
    args = parser.parse_args()
    directory = Path(args.candidate).resolve()
    require(directory.parent==RECON, 'Candidate outside reconciliation')
    proposed = json.loads((directory/'PROPOSAL.json').read_bytes())
    bound = json.loads((directory/'BOUND_AUTHOR61.json').read_bytes())
    reader = Reader()

    def tree(sha):
        kind,body = reader.get(sha)
        require(kind=='tree', 'Expected tree '+sha)
        entries = parse_tree(body)
        require(encode_tree(entries)==body, 'Noncanonical tree serializer')
        return entries

    def walk(sha,prefix=b''):
        result = {}
        for name,entry in tree(sha).items():
            path = prefix+name
            result[path]=entry
            if entry[0]==b'40000':
                result.update(walk(entry[1],path+b'/'))
        return result

    def root(sha):
        kind,body = reader.get(sha)
        require(kind=='commit', 'Not commit '+sha)
        headers = body.split(b'\n\n',1)[0].splitlines()
        require(headers[0].startswith(b'tree '), 'Missing first tree header')
        return headers[0].split()[1].decode()

    main_root = root(proposed['main'])
    author_root = root(AUTHOR)
    candidate_root = root(proposed['candidate_commit'])
    require(main_root==proposed['before_tree'], 'MAIN root mismatch')
    require(author_root==proposed['accepted_author_tree']=='a4a0630d53562387083fe4481d648e8489b4b1f7', 'Author root mismatch')
    require(candidate_root==proposed['candidate_tree'], 'Candidate root mismatch')
    mains = walk(main_root)
    authors = walk(author_root)
    candidates = walk(candidate_root)
    leaves = lambda paths:{p:e for p,e in paths.items() if e[0]!=b'40000'}
    mainleaves,authorleaves,candidateleaves = map(leaves,(mains,authors,candidates))
    accepted = {p:e for p,e in authorleaves.items() if p.startswith(TARGET+b'/')}
    require(len(accepted)==61 and authors[TARGET]==(b'40000',proposed['target_subtree']), 'All61 census/subtree mismatch')
    manifest = {e['path'].encode():e for e in bound}
    require(len(manifest)==61 and set(manifest)==set(accepted), 'Bound path census mismatch')
    fullbody = []
    for path,(mode,sha) in sorted(accepted.items()):
        kind,body = reader.get(sha)
        entry = manifest[path]
        require(mode==b'100644' and kind=='blob' and entry['mode']=='100644' and entry['type']=='blob', 'Author modes/types')
        require(entry['sha']==sha and entry['bytes']==len(body) and entry['sha256']==hashlib.sha256(body).hexdigest(), 'Logical body mismatch '+path.decode())
        fullbody.append(dict(path=path.decode(),mode=mode.decode(),oid=sha,bytes=len(body),sha256=hashlib.sha256(body).hexdigest()))

    target_in_main = {p:e for p,e in mains.items() if p==TARGET or p.startswith(TARGET+b'/')}
    require(not target_in_main or target_in_main[TARGET]==authors[TARGET], 'Existing target is not absent/exact')
    qmode,qbefore = mainleaves[QUEUE]
    qkind,qbody = reader.get(qbefore)
    require(qkind=='blob' and qmode in (b'100644',b'100755'), 'QUEUE not regular blob')
    kind,accepted_queue = reader.get(authorleaves[QUEUE][1])
    require(kind=='blob', 'Author QUEUE not blob')
    def row(body):
        lines = body.splitlines(keepends=True)
        indexes = [i for i,l in enumerate(lines) if len(l.split(b'|'))>3 and l.split(b'|')[2].strip()==b'30005468 / OWR-12697710-015']
        require(len(indexes)==1,'Exact QUEUE row census')
        return lines,indexes[0]
    oldlines,index = row(qbody)
    alines,ai = row(accepted_queue)
    accepted_row = alines[ai]
    overlay = json.loads((CASE/'ROOT_native04_actual_conflict_consumption_01/ROOT_RECONSTRUCTED_62_OVERLAY.json').read_bytes())
    import base64
    baseline_row = base64.b64decode(overlay['queue_delta']['baseline_base64'])
    require(oldlines[index] in (baseline_row,accepted_row), 'Independent target row overwritten')
    expectedlines = oldlines.copy()
    expectedlines[index] = accepted_row
    expectedqueue = b''.join(expectedlines)
    qnew = oid('blob',expectedqueue)
    require(candidateleaves[QUEUE]==(qmode,qnew), 'QUEUE mode/blob mismatch')
    require(reader.get(qnew)==('blob',expectedqueue), 'Foreign QUEUE bytes changed')
    require(proposed['queue_accepted_row'].encode()==accepted_row, 'Proposal accepted row mismatch')
    require(proposed['queue_before_blob']==qbefore and proposed['queue_after_blob']==qnew, 'Proposal QUEUE ids')

    expected = dict(mainleaves)
    expected.update(accepted)
    expected[QUEUE]=(qmode,qnew)
    require(candidateleaves==expected, 'Whole-tree leaf conservation mismatch')
    changed = sorted(p for p in set(mainleaves)|set(candidateleaves) if mainleaves.get(p)!=candidateleaves.get(p))
    require(set(changed)<=set(accepted)|{QUEUE}, 'Foreign leaf change')
    ancestors = {b'',b'unsolved_math_prioritization',b'unsolved_math_prioritization/attempts'}
    foreign_trees = {p:e for p,e in mains.items() if e[0]==b'40000' and p not in ancestors and not (p==TARGET or p.startswith(TARGET+b'/'))}
    require(all(candidates.get(p)==e for p,e in foreign_trees.items()), 'Whole foreign directory Merkle identity changed')
    for path,entry in authors.items():
        if path==TARGET or path.startswith(TARGET+b'/'):
            require(candidates.get(path)==entry, 'Accepted target inner directory/tree mismatch')

    kind,commitbody = reader.get(proposed['candidate_commit'])
    require(kind=='commit' and commitbody==(directory/'commit.raw').read_bytes(), 'Commit raw mismatch')
    headers = commitbody.split(b'\n\n',1)[0].splitlines()
    parents = [h.split()[1].decode() for h in headers if h.startswith(b'parent ')]
    require(parents==[AUTHOR,proposed['main']]==proposed['ordered_parents'], 'Ordered parent mismatch')
    payload = json.loads((directory/'COMMIT_PAYLOAD.json').read_bytes())
    require(payload['tree']==candidate_root and payload['parents']==parents, 'Commit payload root/parent mismatch')
    for label in ('author','committer'):
        person = payload[label]
        timestamp = int(dt.datetime.strptime(person['date'],'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=dt.timezone.utc).timestamp())
        exact = (label+' '+person['name']+' <'+person['email']+'> '+str(timestamp)+' +0000').encode()
        require(exact in headers, 'Commit identity/time payload mismatch')
    require(commitbody.split(b'\n\n',1)[1]==payload['message'].encode(), 'Commit message payload mismatch')
    tp = json.loads((directory/'TREE_PAYLOAD.json').read_bytes())
    require(tp==dict(base_tree=main_root,tree=[dict(path=TARGET.decode(),mode='040000',type='tree',sha=authors[TARGET][1]),dict(path=QUEUE.decode(),mode=qmode.decode(),type='blob',content=expectedqueue.decode())]), 'Tree payload exactness')
    cas = json.loads((directory/'CAS_PAYLOAD.json').read_bytes())
    ci = cas['variables']['input']
    repository = json.loads((CASE/'ROOT_PR278_author_branch_readback_01/0002_GET_RESPONSE.json').read_bytes())
    require(repository['full_name']=='AlecKriebel/Math' and ci['repositoryId']==repository['node_id'], 'CAS repository')
    require(ci['refUpdates']==[dict(name='refs/heads/dot/math-30005468',beforeOid=AUTHOR,afterOid=proposed['candidate_commit'],force=False)], 'CAS author-only exact-old/nonforce')
    require(proposed['preparation_only'] is True and proposed['execution_authority'] is False and proposed['provider_mutations']==0 and proposed['primary_git_mutations']==0, 'Preparation authority flags')

    package = CASE/'preprint_package_v01'
    packaged = []
    for path,(mode,sha) in sorted(accepted.items()):
        if path.startswith(TARGET+b'/preprint/'):
            rel = path[len(TARGET+b'/preprint/'):].decode()
            released = (package/rel).read_bytes()
            require(reader.get(sha)==('blob',released), 'Frozen published package divergence '+rel)
            packaged.append(rel)
    require(len(packaged)==11, 'Frozen source package census')
    originals = json.loads((CASE/'original_submission_snapshot_01/MANIFEST.json').read_bytes())
    require(len(originals)==18, 'Original submission census')
    preserved_originals = []
    for original in originals:
        path = TARGET+b'/audit/original_submission/'+original['relative_path'].encode()
        mode,sha = accepted[path]
        body = (CASE/'original_submission_snapshot_01/files'/original['relative_path']).read_bytes()
        require(mode.decode()==original['mode'] and sha==original['git_blob'] and reader.get(sha)==('blob',body), 'Original historical body omitted or changed')
        require(len(body)==original['bytes'] and hashlib.sha256(body).hexdigest()==original['sha256'], 'Original manifest integrity')
        preserved_originals.append(original['relative_path'])
    textdir = ROOT/(directory.name+'_accepted_text')
    textdir.mkdir(exist_ok=True)
    for rel in ('RESULT.md','PROOF.md','README.md','HISTORICAL_ERRATUM.md','PUBLICATION_RECEIPT.json'):
        kind,body = reader.get(accepted[TARGET+b'/'+rel.encode()][1])
        require(kind=='blob', 'Review text not blob')
        (textdir/rel).write_bytes(body)
    pins = [pin(directory/name) for name in ('PROPOSAL.json','BOUND_AUTHOR61.json','TREE_PAYLOAD.json','COMMIT_PAYLOAD.json','CAS_PAYLOAD.json','commit.raw')]
    pins += [pin(RECON/'build_reconciliation.py'),pin(RECON/'verify_scope.py'),pin(RESUME/'math_review/MATHEMATICAL_REVIEW.md'),pin(RESUME/'source_priority_review/REPORT.md')]
    pins += [pin(RESUME/name) for name in ('final_pr_body.md','final_pr_metadata.json','ACTION_PLAN.md')]
    pins += [pin(CASE/'original_submission_snapshot_01/MANIFEST.json')]
    report = dict(schema='pr278-second-independent-integration-audit-v1',UTC=dt.datetime.now(dt.timezone.utc).isoformat(),verified=True,
                  main=proposed['main'],author=AUTHOR,candidate_tree=candidate_root,candidate_commit=proposed['candidate_commit'],ordered_parents=parents,
                  main_leaves=len(mainleaves),candidate_leaves=len(candidateleaves),accepted_author_leaves=len(accepted),
                  foreign_main_leaves_preserved=len(set(mainleaves)-set(accepted)-{QUEUE}),
                  unchanged_foreign_directories=len(foreign_trees),foreign_queue_lines_preserved=len(oldlines)-1,
                  target_queue_line=index+1,queue_mode=qmode.decode(),changed_paths=[p.decode() for p in changed],
                  symlinks_preserved=sum(e[0]==b'120000' for p,e in mainleaves.items() if p not in accepted and p!=QUEUE),
                  gitlinks_preserved=sum(e[0]==b'160000' for p,e in mainleaves.items() if p not in accepted and p!=QUEUE),
                  executable_files_preserved=sum(e[0]==b'100755' for p,e in mainleaves.items() if p not in accepted and p!=QUEUE),
                  frozen_source_files_equal=packaged,preserved_all18_original_bodies=preserved_originals,full61=fullbody,input_pins=pins,raw_objects_consumed=len(reader.cache),
                  no_network_or_ref_operations=True,limitations=['Verifies concrete private preparation only, not any future provider operation.','Fresh MAIN and author observations plus renewed conservation are needed for a different prepared tree.','Author expected-old CAS does not atomically freeze MAIN.','OID conservation certifies unchanged foreign contents by Git object identity; missing foreign blob bodies are not reread.'])
    reader.close()
    dest = ROOT/(directory.name+'_INDEPENDENT_RESULT.json')
    dest.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:report[k] for k in ('verified','main','candidate_tree','main_leaves','candidate_leaves','accepted_author_leaves','foreign_main_leaves_preserved','unchanged_foreign_directories','target_queue_line','raw_objects_consumed')},indent=2))

if __name__=='__main__':
    main()
