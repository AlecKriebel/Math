#!/usr/bin/env python3
"""Publication wrapper regressions using only synthetic mutations of safe files."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


def need(ok, message):
    if not ok: raise ValueError(message)

def sha(b): return hashlib.sha256(b).hexdigest()

def dump(v): return json.dumps(v,indent=2,sort_keys=True)+'\n'

def repin(root):
    files={p.relative_to(root).as_posix():{'bytes':len(p.read_bytes()),'sha256':sha(p.read_bytes())}
           for p in sorted(root.rglob('*')) if p.is_file() and p.name != 'PUBLICATION_MANIFEST.json'}
    raw=dump({'schema':'dominating-digraph-strict-publication-v1','files':files}).encode()
    (root/'PUBLICATION_MANIFEST.json').write_bytes(raw)
    return sha(raw)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--manifest-sha256',required=True)
    args=parser.parse_args()
    root=Path(__file__).absolute().parent
    need(sha((root/'PUBLICATION_MANIFEST.json').read_bytes())==args.manifest_sha256,'external pin')
    trusted=root/'verify_publication.py'
    result={'schema':'dominating-digraph-publication-tests-v1','replays':[],'integrity_controls':[],'semantic_controls':[]}
    def invoke(target,pin,opt,full=False):
        return subprocess.run([sys.executable,'-I','-B',*(['-O'] if opt else []),str(trusted),'--root',str(target),'--manifest-sha256',pin,*(['--full'] if full else [])],cwd='/tmp',capture_output=True,text=True,timeout=240)
    with tempfile.TemporaryDirectory(prefix='digraph-publication-') as td:
        td=Path(td);moved=td/'relocated';shutil.copytree(root,moved)
        baseline=None
        for location,target in [('original',root),('relocated',moved)]:
            for opt in (False,True):
                p=invoke(target,args.manifest_sha256,opt,True)
                need(p.returncode==0 and not p.stderr,p.stderr)
                out=json.loads(p.stdout)
                if baseline is None: baseline=out
                need(out==baseline,'replay mode/location disagreement')
                result['replays'].append({'location':location,'optimized':opt,'result':out})
        labels=['extra_file','extra_directory','symlink_file','symlink_directory','fifo','hardlink_file','hardlink_manifest','root_symlink','missing_payload','corrupt_payload','missing_manifest','stale_manifest','duplicate_manifest_key','unsafe_manifest_path','wrong_pin','changed_archive','changed_verifier']
        for label in labels:
            target=td/label;shutil.copytree(root,target);pin=args.manifest_sha256
            if label=='extra_file': (target/'extra.txt').write_text('synthetic')
            elif label=='extra_directory': (target/'__pycache__').mkdir()
            elif label=='symlink_file': (target/'README.md').unlink();(target/'README.md').symlink_to(root/'README.md')
            elif label=='symlink_directory': (target/'unexpected').symlink_to(root/'author',target_is_directory=True)
            elif label=='fifo': (target/'README.md').unlink();os.mkfifo(target/'README.md')
            elif label in ('hardlink_file','hardlink_manifest'):
                name='README.md' if label=='hardlink_file' else 'PUBLICATION_MANIFEST.json'
                path=td/(label+'-alias');path.write_bytes((target/name).read_bytes());(target/name).unlink();os.link(path,target/name)
            elif label=='root_symlink':
                link=td/'root-link';link.symlink_to(target,target_is_directory=True);target=link
            elif label=='missing_payload': (target/'README.md').unlink()
            elif label=='corrupt_payload': (target/'README.md').write_text('synthetic change')
            elif label=='missing_manifest': (target/'PUBLICATION_MANIFEST.json').unlink()
            elif label=='stale_manifest': (target/'PUBLICATION_MANIFEST.json').write_text('{}\n')
            elif label=='duplicate_manifest_key':
                mp=target/'PUBLICATION_MANIFEST.json';b=mp.read_bytes();b=b.replace(b'{',b'{"schema":"duplicate",',1);mp.write_bytes(b);pin=sha(b)
            elif label=='unsafe_manifest_path':
                mp=target/'PUBLICATION_MANIFEST.json';m=json.loads(mp.read_bytes());m['files']['../escape']={'bytes':0,'sha256':sha(b'')};mp.write_text(dump(m));pin=sha(mp.read_bytes())
            elif label=='wrong_pin': pin='0'*64
            elif label=='changed_archive':
                z=target/'archives/DOMINATING_DIGRAPH_30001669_AUTHOR_SAFE_FREEZE.zip';z.write_bytes(z.read_bytes()+b'changed');pin=repin(target)
            elif label=='changed_verifier': (target/'verify_publication.py').write_text('raise SystemExit(0)\n')
            for opt in (False,True):
                p=invoke(target,pin,opt);need(p.returncode!=0,'mutation accepted: '+label)
            result['integrity_controls'].append({'name':label,'normal_rejected':True,'optimized_rejected':True})
        changes=[('novel_claim',['novel_resolution_claim'],True),('adjacency_claim',['computed_adjacency_certificate_claim'],True),('human_peer_review',['human_peer_review_of_this_packet_claim'],True),('formal_proof',['formal_proof_claim'],True),('open_classification',['classification'],'queued'),('positive_answer',['answer'],'positive'),('wrong_turns',['turns'],'2/5'),('wrong_approaches',['approaches_used'],2),('wrong_credit',['credit'],'Anonymous'),('wrong_year',['prior_result_year'],2026),('girth_100',['specialization','k'],100),('reverse_orientation',['specialization','witness_orientation'],'target to witness'),('zero_walk',['specialization','positive_walk_lengths'],[0,99]),('base_9900',['specialization','base_girth'],9900),('exact_size_only',['specialization','subset_sizes'],'exactly 100'),('unbounded_queue_edit',['queue_edit','changed_cells'],['Status','Turns','Findings','Impact'])]
        for label,keys,value in changes:
            target=td/('semantic-'+label);shutil.copytree(root,target)
            mp=target/'PUBLICATION_METADATA.json';m=json.loads(mp.read_bytes());node=m
            for key in keys[:-1]:node=node[key]
            node[keys[-1]]=value;mp.write_text(dump(m));pin=repin(target)
            for opt in (False,True):
                p=invoke(target,pin,opt);need(p.returncode!=0,'semantic mutation accepted: '+label)
            result['semantic_controls'].append({'name':label,'normal_rejected':True,'optimized_rejected':True,'manifest_recomputed':True})
    result['status']='pass'
    result['scope']='Frozen public files, arithmetic, selected semantic controls and synthetic graph fixtures only; not a formal theorem proof.'
    print(dump(result),end='')

if __name__=='__main__':main()
