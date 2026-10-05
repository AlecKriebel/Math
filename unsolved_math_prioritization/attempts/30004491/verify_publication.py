#!/usr/bin/env python3
"""Portable fail-closed publication inventory and exact source-free replay."""
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
import zipfile

ROOT=Path(__file__).resolve().parent
FROZEN={'FOLIATION_30004491_AUTHOR_SAFE_FREEZE.zip': {'bytes': 20834, 'sha256': '4f5e1bddcfb9720f76f50cdff5118409d3c764dd24e0701677d01bb54ed98a5b'}, 'FOLIATION_30004491_INDEPENDENT_AUDIT.zip': {'bytes': 19254, 'sha256': '315129f62788a03e17421b6abc175b7160e6e9ca1fa72e17b32d67a6c25fbd37'}, 'author/APPROACHES.md': {'bytes': 5127, 'sha256': '2b57e65f2eada88186b5739a9727d2226c1487edc41c4e32729aa5668bf28503'}, 'author/AUTHOR_MANIFEST.json': {'bytes': 1716, 'sha256': '1398394bb23d7346d694aae514380a80531a23ee94726bc873bb586e387d5b92'}, 'author/BIBLIOGRAPHY.md': {'bytes': 2155, 'sha256': 'bd8f72eda7379e0320e8403ed4773a11708fcb3400b4678e5834a04dce9c09c2'}, 'author/PROOFS.md': {'bytes': 12026, 'sha256': 'c90303d06ae5b773b79e280a471db197e4f1f56a323df23afea00749eb67ee28'}, 'author/README.md': {'bytes': 1775, 'sha256': '7d535bc4d05a3f53c508575c5aa4263976b2c171dd35bbe2c999e0deb08d78ce'}, 'author/RESULT.md': {'bytes': 6920, 'sha256': '2507244b085fb6709c0558e45895bfb9fab009ca57a2f09839d34fd3fcd37aca'}, 'author/SOURCE_VERIFICATION.json': {'bytes': 9057, 'sha256': '2add5eb02a0c967830192fecb2e4e1eb3431f1a5b4f0e829f76e457670b2fa5b'}, 'author/VERIFY_OUTPUT.json': {'bytes': 685, 'sha256': 'db8233000031a9bda90b11ac362289bf0d3846ba451add3a3068942eede7071b'}, 'author/verify.py': {'bytes': 4168, 'sha256': '1f50804feedefac89a39b2a11e60e62041b6558fa9240338f52a7ad7f761938f'}, 'author/verify_manifest.py': {'bytes': 1344, 'sha256': '98346651af1b4a22b6e6a26aace2856d42ccd655199300fd66c265c3d161177d'}, 'independent_audit/AUDIT_MANIFEST.json': {'bytes': 1104, 'sha256': '198c7a6246641bbe4260b6b50e907d8d7bd5887531270e1c2becf04ea9315750'}, 'independent_audit/AUDIT_REPORT.md': {'bytes': 20486, 'sha256': 'df46272c380792a4e8e089d7562648dfe81c2bd244631a46b4b01563fb4d5691'}, 'independent_audit/INDEPENDENT_OUTPUT.json': {'bytes': 5478, 'sha256': '672b45deb45832f317ef29870a7f5d613c91eacdc655399aa020a0d680b1ff73'}, 'independent_audit/SOURCE_AUDIT.json': {'bytes': 8543, 'sha256': '2ad0f00510082f3767e7be23f8032e7d74b1e32fd294347bddf40d07aeabef4a'}, 'independent_audit/independent_verify.py': {'bytes': 11720, 'sha256': 'd0b03ba4cbc7cb827b77059e92daeb8d887e26aaa51b23e6874ba71cc148e906'}, 'independent_audit/verify_audit_manifest.py': {'bytes': 1246, 'sha256': '8e13e0db94acc9acc81d1454ab15b471aa893b13961c31ee8da7facaa84d17a9'}}
SCOPE={'problem_id': 30004491, 'problem_number': 'OWR-1703871-006', 'rank': 752, 'status': 'unsolved', 'turns': '5/5', 'independent_verdict': 'PASS_SCOPED_UNSOLVED', 'mandatory_corrections': [], 'general_conjecture_solved': False, 'novelty_claim': False, 'human_peer_review_claim': False, 'strongest_result': 'Explicit cover-essential singular projective foliation with infinite transverse birational action; closed rational form on a degree-two cover, none downstairs or on a birational model, and no rational first integral after any generically finite cover. This satisfies the original conjecture.', 'remaining_gap': 'No transverse rational infinitesimal symmetry, transversely projective structure, or algebraic integrating factor is constructed for the arbitrary singular dominant-rational target.', 'author_freeze_review_pending_label': 'Historical author-freeze label; current independent assessment is in independent_audit/AUDIT_REPORT.md. Frozen bytes are unchanged.', 'publication_boundary': 'Authored proof/code/audit/results and public verification metadata only; no source PDFs, source text extracts, raw datasets, private sources, or private coordination files.', 'queue_patch': {'path': 'unsolved_math_prioritization/QUEUE.md', 'base_commit': '6144d964777214c6963a915288c18fcf97b42026', 'base_git_blob': '483de6795be8c12bacc3d18e1ef04900eddedf04', 'before': {'bytes': 389371, 'sha256': '6b37d1112c4223ae1c39156a98a745389112a7b129080dcd3a6439c334ebf2c2'}, 'after': {'bytes': 389373, 'sha256': 'adb3a1386b99ee388aeecae30e8f8bbfc20e9cb06839c1a8501c7be1a29b9562'}, 'patch': {'bytes': 1227, 'sha256': '848a897b94f1e6d0e1d17cf88de2211b9f5606be4b3c203aa42da5d6e176bdff'}, 'one_based_line': 763, 'changed_cells': ['Status', 'Turns'], 'old_values': ['queued', '0/5'], 'new_values': ['unsolved', '5/5'], 'all_other_bytes_preserved': True, 'findings_chat_doi_preserved': True, 'embedded_stale_header_preserved': True}}
EXPECTED=['CLARIFICATIONS.md', 'FOLIATION_30004491_AUTHOR_SAFE_FREEZE.zip', 'FOLIATION_30004491_INDEPENDENT_AUDIT.zip', 'PUBLICATION.json', 'PUBLICATION_MANIFEST.json', 'README.md', 'RESEARCH_LOG.md', 'author/APPROACHES.md', 'author/AUTHOR_MANIFEST.json', 'author/BIBLIOGRAPHY.md', 'author/PROOFS.md', 'author/README.md', 'author/RESULT.md', 'author/SOURCE_VERIFICATION.json', 'author/VERIFY_OUTPUT.json', 'author/verify.py', 'author/verify_manifest.py', 'independent_audit/AUDIT_MANIFEST.json', 'independent_audit/AUDIT_REPORT.md', 'independent_audit/INDEPENDENT_OUTPUT.json', 'independent_audit/SOURCE_AUDIT.json', 'independent_audit/independent_verify.py', 'independent_audit/verify_audit_manifest.py', 'verify_publication.py']

def need(test,message):
    if not test: raise RuntimeError(message)

def pin(data):
    return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def unique_object(pairs):
    result={}
    for key,value in pairs:
        need(key not in result,'duplicate JSON key: '+key)
        result[key]=value
    return result

def read_json(path):
    return json.loads(path.read_text(),object_pairs_hook=unique_object)

def run(path,*args):
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    return subprocess.check_output([sys.executable,'-B',*(['-O'] if sys.flags.optimize else []),str(path),*map(str,args)],env=env)

def inventory():
    expected=set(EXPECTED)
    actual=set();directories=set()
    for p in ROOT.rglob('*'):
        rel=p.relative_to(ROOT).as_posix()
        need(not p.is_symlink(),'symlink: '+rel)
        if p.is_file(): actual.add(rel)
        elif p.is_dir(): directories.add(rel)
        else: need(False,'special entry: '+rel)
    need(actual==expected,'file allowlist mismatch')
    wanted_dirs={q.as_posix() for p in expected for q in PurePosixPath(p).parents if q.as_posix()!='.'}
    need(directories==wanted_dirs,'directory allowlist mismatch')
    manifest=read_json(ROOT/'PUBLICATION_MANIFEST.json')
    need(set(manifest)=={'problem_id','files'} and manifest['problem_id']==30004491,'manifest metadata')
    need(set(manifest['files'])==expected-{'PUBLICATION_MANIFEST.json'},'manifest allowlist')
    for name,meta in manifest['files'].items():
        path=PurePosixPath(name)
        need(not path.is_absolute() and '..' not in path.parts,'unsafe manifest name')
        need(pin((ROOT/name).read_bytes())==meta,'manifest mismatch: '+name)
    for name,meta in FROZEN.items():
        need(pin((ROOT/name).read_bytes())==meta,'frozen pin mismatch: '+name)
    need(read_json(ROOT/'PUBLICATION.json')==SCOPE,'scope metadata mismatch')
    for archive,folder in [('FOLIATION_30004491_AUTHOR_SAFE_FREEZE.zip','author'),('FOLIATION_30004491_INDEPENDENT_AUDIT.zip','independent_audit')]:
        with zipfile.ZipFile(ROOT/archive) as z:
            infos=z.infolist();names=[i.filename for i in infos]
            wanted={p.name for p in (ROOT/folder).iterdir()}
            need(len(names)==len(set(names)) and set(names)==wanted,'archive membership: '+archive)
            for item in infos:
                need(not item.is_dir() and not stat.S_ISLNK(item.external_attr>>16),'unsafe archive member')
                need(z.read(item)==(ROOT/folder/item.filename).read_bytes(),'archive content mismatch')
    return {'status':'PASS_PUBLICATION_INVENTORY','problem_id':30004491,'packet_files':len(expected),'frozen_files_and_archives':len(FROZEN),'archives':2}

def verify(inventory_only=False):
    result=inventory()
    if inventory_only:return result
    author=ROOT/'author';audit=ROOT/'independent_audit'
    need(json.loads(run(author/'verify_manifest.py'))=={'status':'PASS_EXACT_MANIFEST','files':9},'author manifest replay')
    need(run(author/'verify.py')==(author/'VERIFY_OUTPUT.json').read_bytes(),'author output replay')
    need(json.loads(run(audit/'verify_audit_manifest.py'))=={'status':'PASS_AUDIT_MANIFEST','files':6},'audit manifest replay')
    expected=read_json(audit/'INDEPENDENT_OUTPUT.json')
    need(set(expected)=={'author_runs','dataset_pins','freeze','general_conjecture_solved','independent_symbolic','mutations','source_pins','status'},'historical output fields')
    del expected['source_pins'];del expected['dataset_pins']
    replay=run(audit/'independent_verify.py','--author',author,'--archive',ROOT/'FOLIATION_30004491_AUTHOR_SAFE_FREEZE.zip')
    expected_bytes=(json.dumps(expected,sort_keys=True,indent=2)+'\n').encode()
    need(replay==expected_bytes,'source-free independent replay not byte-exact')
    need(expected['independent_symbolic']['total_checks']==34,'independent controls')
    need(len(expected['mutations'])==14 and all(x['rejected'] for x in expected['mutations']),'negative controls')
    need(all(x['controls']==3588 for x in expected['author_runs']),'author control count')
    inventory()
    result.update({'status':'PASS_SCOPED_PUBLICATION','disposition':'unsolved','turns':'5/5','author_controls_per_mode':3588,'independent_exact_controls':34,'author_corruptions_rejected':14,'source_free_replay_byte_exact':True,'general_conjecture_solved':False,'source_and_dataset_retrieval_in_this_replay':False})
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--inventory-only',action='store_true')
    args=parser.parse_args()
    print(json.dumps(verify(args.inventory_only),indent=2,sort_keys=True))
