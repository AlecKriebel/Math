#!/usr/bin/env python3
"""Independent reproducible checks. Does not prove the cited existence theorem."""
import argparse
from collections import deque
import hashlib
import itertools
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

AUTHOR_SHA = '15bb36b2d492b2ace008a6b851b31a3893ec0a559ccc3853a2d709f58f3ed96f'
AUTHOR_SIZE = 10114
MANIFEST_SHA = 'd1d79514b2851823f47345677bfa66f53152f1922562b1040f7dd8882028c620'
MEMBERS = {'MANIFEST.json','PUBLIC_METADATA.json','REPORT.md','VERIFICATION.json','audit_checks.py','verify.py'}

def require(ok, message):
    if not ok:
        raise ValueError(message)

def digest(b):
    return hashlib.sha256(b).hexdigest()

def dump(value):
    return json.dumps(value, indent=2, sort_keys=True) + '\n'

def repin(p):
    m = {'schema':'strict-flat-sha256-v1','files':{}}
    for n in sorted(MEMBERS - {'MANIFEST.json'}):
        b=(p/n).read_bytes();m['files'][n]={'bytes':len(b),'sha256':digest(b)}
    b=dump(m).encode();(p/'MANIFEST.json').write_bytes(b)
    return digest(b)

def invoke(verifier, root, pin, optimized):
    cmd=[sys.executable,'-B']+(['-O'] if optimized else [])
    return subprocess.run(cmd+[str(verifier),'--root',str(root),'--manifest-sha256',pin],
                          capture_output=True,text=True,cwd='/tmp',timeout=30)

def dominated(adj, subset):
    return any(all(u in adj[v] for u in subset) for v in range(len(adj)))

def property_p(adj, limit):
    return all(dominated(adj,s) for r in range(min(len(adj),limit)+1)
               for s in itertools.combinations(range(len(adj)),r))

def girth(adj):
    best=None
    for start in range(len(adj)):
        seen={start:0}; queue=deque([start])
        while queue:
            v=queue.popleft()
            for w in adj[v]:
                if w==start:
                    d=seen[v]+1;best=d if best is None else min(best,d)
                elif w not in seen:
                    seen[w]=seen[v]+1;queue.append(w)
    return best

def power(adj, bound, zero=False):
    out=[]
    for v in range(len(adj)):
        reached={v} if zero else set();front={v}
        for _ in range(bound):
            front=set().union(*(adj[w] for w in front)); reached |= front
        out.append(reached)
    return out

def graph_controls():
    # Synthetic small fixtures only, never represented as the 100-dominating witness.
    paley=[{(v+d)%7 for d in (1,2,4)} for v in range(7)]
    squared=power(paley,2)
    require(property_p(paley,2) and girth(paley)==3,'Paley fixture mismatch')
    require(property_p(squared,3) and girth(squared)==2,'Power fixture mismatch')
    require(girth(power(paley,2,zero=True))==1,'Zero-walk control failed')
    cycle=[{(v+1)%101} for v in range(101)]
    require(girth(cycle)==101 and not property_p(cycle,2),'Long cycle control failed')
    require(not property_p([],0),'Empty graph must not satisfy the empty-set requirement')
    fork=[{1,2},set(),set()]
    require(dominated(fork,(1,2)) and not any(0 in fork[u] for u in (1,2)), 'Orientation control failed')
    inequalities=[(t, t*99, 9901) for t in range(1,101)]
    require(all(1<=upper<base for _,upper,base in inequalities),'Strict lifting failed')
    require(100*99==9900 and not 100*99<9900,'Off-by-one control failed')
    # The recursive witness reaches m targets by positive walks of lengths <= m-1.
    for m in range(2,101):
        lengths=[1,1]
        for _ in range(3,m+1): lengths=[d+1 for d in lengths]+[1]
        require(len(lengths)==m and min(lengths)>=1 and max(lengths)==m-1,'Recursion depth failed')
    return {'synthetic_graph_fixtures':6,'strict_lifting_inequalities':100,'recursive_subset_sizes':99,
            'scope':'Small implementation controls and arithmetic only; no actual 100-dominating adjacency certificate.'}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--author-archive',type=Path,default=Path(__file__).resolve().parent/'AUTHOR_SAFE_FREEZE.zip')
    args=parser.parse_args()
    raw=args.author_archive.read_bytes()
    require(len(raw)==AUTHOR_SIZE and digest(raw)==AUTHOR_SHA,'Author archive pin mismatch')
    results={'schema':'dominating-digraph-independent-checks-v1','problem_id':30001669,
             'author_archive_sha256':AUTHOR_SHA,'author_manifest_sha256':MANIFEST_SHA,
             'replays':[],'integrity_controls':[],'semantic_controls':[]}
    with tempfile.TemporaryDirectory(prefix='independent-digraph-') as td:
        td=Path(td);author=td/'author';author.mkdir()
        with zipfile.ZipFile(args.author_archive) as z:
            infos=z.infolist()
            require(len(infos)==len(MEMBERS) and {i.filename for i in infos}==MEMBERS,'ZIP inventory mismatch')
            for i in infos:
                require('/' not in i.filename and not i.is_dir(),'Nonflat ZIP entry')
                require(stat.S_ISREG(i.external_attr>>16),'Nonregular ZIP entry')
                (author/i.filename).write_bytes(z.read(i))
        require(digest((author/'MANIFEST.json').read_bytes())==MANIFEST_SHA,'Author manifest pin mismatch')
        trusted=author/'verify.py'
        manifest=json.loads((author/'MANIFEST.json').read_text())
        for name in MEMBERS-{'MANIFEST.json'}:
            b=(author/name).read_bytes()
            require(manifest['files'][name]=={'bytes':len(b),'sha256':digest(b)},'Author payload pin mismatch')
        moved=td/'relocated';shutil.copytree(author,moved)
        for location,p in [('original',author),('relocated',moved)]:
            for opt in (False,True):
                r=invoke(p/'verify.py',p,MANIFEST_SHA,opt)
                require(r.returncode==0,r.stderr)
                results['replays'].append({'location':location,'optimized':opt,'result':json.loads(r.stdout)})
        # Independent mutations use the unmodified pinned verifier and explicit --root.
        labels=['extra_file','extra_directory','symlink_payload','fifo_payload','missing_payload','changed_payload',
                'stale_manifest','hardlink_payload','hardlink_manifest','root_symlink','payload_directory',
                'missing_manifest','unicode_extra_file','changed_verifier']
        for label in labels:
            p=td/label;shutil.copytree(author,p);pin=MANIFEST_SHA
            if label=='extra_file':(p/'unlisted.txt').write_text('test')
            elif label=='extra_directory':(p/'extra').mkdir()
            elif label=='symlink_payload':(p/'REPORT.md').unlink();(p/'REPORT.md').symlink_to(author/'REPORT.md')
            elif label=='fifo_payload':(p/'REPORT.md').unlink();os.mkfifo(p/'REPORT.md')
            elif label=='missing_payload':(p/'REPORT.md').unlink()
            elif label=='changed_payload':(p/'REPORT.md').write_text('changed')
            elif label=='stale_manifest':(p/'MANIFEST.json').write_text('{}\n')
            elif label in ('hardlink_payload','hardlink_manifest'):
                name='REPORT.md' if label=='hardlink_payload' else 'MANIFEST.json'
                target=td/(label+'-target');target.write_bytes((p/name).read_bytes());(p/name).unlink();os.link(target,p/name)
            elif label=='root_symlink':
                link=td/'root-link';link.symlink_to(p,target_is_directory=True);p=link
            elif label=='payload_directory':(p/'REPORT.md').unlink();(p/'REPORT.md').mkdir()
            elif label=='missing_manifest':(p/'MANIFEST.json').unlink()
            elif label=='unicode_extra_file':(p/'REPORT.md\u200b').write_text('test')
            elif label=='changed_verifier':(p/'verify.py').write_text('raise RuntimeError("modified")\n')
            for opt in (False,True):
                r=invoke(trusted,p,pin,opt);require(r.returncode!=0,'Integrity mutation accepted: '+label)
            results['integrity_controls'].append({'name':label,'normal_rejected':True,'optimized_rejected':True})
        changes=[('girth_100',['theorem_specialization','girth_lower_bound'],100),
          ('subset_99',['theorem_specialization','dominated_subset_limit'],99),
          ('reverse_orientation',['theorem_specialization','witness_orientation'],'u_to_v'),
          ('exactly_100',['theorem_specialization','subset_quantifier'],'exactly'),
          ('infinite_only',['theorem_specialization','finite'],False),
          ('tournaments',['theorem_specialization','graph_class'],'tournaments'),
          ('zero_walk',['theorem_specialization','power_minimum_walk_length'],0),
          ('base_9900',['theorem_specialization','base_girth_lower_bound'],9900),
          ('power_100',['theorem_specialization','power_maximum_walk_length'],100),
          ('question_101',['theorem_specialization','cycle_length_upper_bound_question'],101),
          ('girth_float',['theorem_specialization','girth_lower_bound'],101.0),
          ('girth_bool',['theorem_specialization','girth_lower_bound'],True),
          ('wrong_problem',['problem_id'],30001670),
          ('wrong_problem_number',['problem_number'],'OTHER'),
          ('novel_claim',['novel_resolution_claim'],True),
          ('adjacency_claim',['computational_counterexample_claim'],True),
          ('report_present',['full_record_review','report_present'],True),
          ('wrong_record_hash',['full_record_review','sha256'],'0'*64),
          ('wrong_record_size',['full_record_review','bytes'],3625),
          ('wrong_statement_hash',['statement_identity','sha256'],'0'*64),
          ('wrong_theorem',['source_theorem','number'],12),
          ('wrong_page',['source_theorem','printed_page'],82),
          ('wrong_doi',['source_theorem','doi'],'10.0/wrong'),
          ('open_status',['disposition'],'open')]
        for label,keys,value in changes:
            p=td/('semantic-'+label);shutil.copytree(author,p);m=json.loads((p/'PUBLIC_METADATA.json').read_text());node=m
            for key in keys[:-1]:node=node[key]
            node[keys[-1]]=value;(p/'PUBLIC_METADATA.json').write_text(dump(m));pin=repin(p)
            for opt in (False,True):
                r=invoke(trusted,p,pin,opt);require(r.returncode!=0,'Semantic mutation accepted: '+label)
            results['semantic_controls'].append({'name':label,'normal_rejected':True,'optimized_rejected':True,'manifest_recomputed':True})
        for opt in (False,True):
            r=invoke(trusted,author,'0'*64,opt);require(r.returncode!=0,'Wrong external pin accepted')
        results['wrong_external_pin_rejected_both_modes']=True
    results['graph_and_arithmetic_controls']=graph_controls()
    results['status']='pass'
    print(dump(results),end='')

if __name__=='__main__':main()
