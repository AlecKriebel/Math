#!/usr/bin/env python3
"""Read-only portable reproduction of frozen partial results, not a proof certificate."""
import difflib
import hashlib
import json
import os
from pathlib import Path
import subprocess
import shutil
import tempfile
import sys

ROOT=Path(__file__).resolve().parent
PINS={
    'author':'d9e4ec28d3ccab08918a952bc6e448366f451d8abebaca72f292aa9e2a4e8494',
    'audit_original_v1':'3a334e8c87683537cf4c35d29d42d1546b9bada346ed29a9c217d1446690f42a',
    'audit_corrected_v2':'3536f75608094a40b5cfcc38c9f564a0aa5e5320a81754201a2fdb5eb647bb82',
}

def require(value,message):
    if not value:raise RuntimeError(message)

def digest(b):return hashlib.sha256(b).hexdigest()
def obj(p):return json.loads(p.read_text(encoding='utf-8'))

def tree(root,pin=None):
    raw=(root/'MANIFEST.json').read_bytes();h=digest(raw)
    if pin:require(h==pin,'frozen manifest changed: '+root.name)
    require((root/'MANIFEST.sha256').read_text().split()==[h,'MANIFEST.json'],'manifest digest mismatch')
    manifest=json.loads(raw);require(manifest['target_id']=='30002830','wrong target')
    names=[]
    for item in manifest['allowlisted_files']:
        name=item['path'];path=Path(name)
        require(isinstance(name,str) and not path.is_absolute() and '..' not in path.parts and name not in names,'unsafe or duplicate path')
        names.append(name);p=root/name
        require(p.is_file() and not p.is_symlink(),'missing or nonregular file: '+name)
        b=p.read_bytes();require(len(b)==item['bytes'] and digest(b)==item['sha256'],'payload mismatch: '+name)
    paths=list(root.rglob('*'));require(not any(p.is_symlink() for p in paths),'symlink forbidden')
    require({p.relative_to(root).as_posix() for p in paths if p.is_file()}==set(names)|{'MANIFEST.json','MANIFEST.sha256'},'file allowlist mismatch')
    if root==ROOT:require({p.relative_to(root).as_posix() for p in paths if p.is_dir()}==set(PINS),'directory allowlist mismatch')
    else:require(not any(p.is_dir() for p in paths),'unexpected frozen directory')
    return len(names)

def run(args):
    result=subprocess.run([sys.executable,'-B',*args],cwd=ROOT,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
    require(result.returncode==0,'replay failed: '+result.stderr)
    require(not result.stderr,'unexpected replay stderr')
    return json.loads(result.stdout)

def main():
    count=tree(ROOT)
    for folder,pin in PINS.items():tree(ROOT/folder,pin)
    old=ROOT/'audit_original_v1';new=ROOT/'audit_corrected_v2'
    correction=obj(new/'METADATA_CORRECTION.json')
    require(correction['original_audit_manifest_sha256']==PINS['audit_original_v1'],'original audit correction binding')
    require(correction['mathematical_statements_changed'] is False and correction['verification_code_changed'] is False and correction['exact_check_results_changed'] is False,'non-attribution correction')
    changed={x['path'] for x in correction['changed_payloads']}
    require(changed=={'AUDIT.md','README.md','replay_results.json'},'correction payload set')
    diff=''
    for item in correction['changed_payloads']:
        name=item['path'];a=(old/name).read_bytes();b=(new/name).read_bytes()
        require(digest(a)==item['original_sha256'] and digest(b)==item['corrected_sha256'],'correction content binding')
        t=a.decode()
        for replacement in item['replacements']:
            require(t.count(replacement['old'])==1,'ambiguous replacement')
            t=t.replace(replacement['old'],replacement['new'])
        require(t.encode()==b,'non-attribution byte delta')
        diff+=''.join(difflib.unified_diff(a.decode().splitlines(keepends=True),b.decode().splitlines(keepends=True),fromfile='original/'+name,tofile='corrected/'+name))
    require(diff==(new/'METADATA_CORRECTION.diff').read_text(),'exact correction diff mismatch')
    unchanged={i['path'] for i in correction['unchanged_payloads']}
    require(unchanged==set(obj(old/'MANIFEST.json')['allowlisted_files'][i]['path'] for i in range(len(obj(old/'MANIFEST.json')['allowlisted_files'])))-changed,'unchanged correction set')
    for item in correction['unchanged_payloads']:
        name=item['path'];require((old/name).read_bytes()==(new/name).read_bytes(),'unrecorded payload revision')
        require(digest((new/name).read_bytes())==item['sha256'],'unchanged payload binding')
    status=obj(ROOT/'release_status.json')
    require(status['status']=='unsolved' and status['turns']=='5/5' and status['retained_routes']==5,'disposition')
    require(status['authoritative_audit']=='audit_corrected_v2','audit authority')
    require(status['correction_type']=='attribution_only_no_mathematical_change','correction scope')
    require(status['audit_attribution']=='AI mathematical audit; not human review or peer review.','audit attribution')
    require(status['historical_original_audit_preserved'] is True,'original history preservation')
    require(status['rational_cover_degree']==3 and status['rational_quotient_degrees']==[2,24],'finite-map directions')
    require(status['relative_obstructions_only'] is True and status['monomial_obstruction_scope']=='unimodular_monomial_projections_of_degree_one','obstruction scope')
    for key in ['cyclic_descent_resolved','total_space_rationality_resolved','total_space_nonrationality_resolved','geometric_dependencies_computer_formalized','novelty_claim','global_current_openness_claim','live_target_contents_verified','full_imported_records_inspected','raw_corpus_hashes_recomputed']:
        require(status[key] is False,'invalid claim: '+key)
    require(status['neighbor_30002829']==dict(pr=697,row_changed=False,budget_changed=False,coverage='partial_method_specific_overlap'),'neighbor scope')
    args=[str(new/'replay_audit.py'),'--author-safe',str(ROOT/'author')]
    normal=run(args);optimized=run(['-O',*args]);require(normal==optimized,'normal and optimized replay differ')
    require(normal['integrity_passed'] and normal['symbolic_replay_passed'],'symbolic replay incomplete')
    author=obj(ROOT/'author/verification_results.json');independent=obj(new/'independent_results.json')
    require((author['check_count'],author['negative_control_count'])==(73,11),'author check counts')
    require((independent['check_count'],independent['negative_control_count'])==(120,10),'independent check counts')
    # The frozen mutation runner preserves copy permissions. Supply a writable
    # temporary author copy so even a read-only release can run its controls.
    with tempfile.TemporaryDirectory(prefix='ueno-release-controls-') as tmp:
        author_copy=Path(tmp)/'author';shutil.copytree(ROOT/'author',author_copy)
        author_copy.chmod(0o755)
        for p in author_copy.rglob('*'):p.chmod(0o755 if p.is_dir() else 0o644)
        tree(author_copy,PINS['author'])
        controls=run(['-O',str(new/'run_negative_controls.py'),'--author-safe',str(author_copy)])
    require(controls==obj(new/'negative_controls.json') and controls['all_rejected'] and controls['control_count']==14,'corruption-control replay mismatch')
    print(json.dumps(dict(status='passed',target_id='30002830',release_manifest_sha256=digest((ROOT/'MANIFEST.json').read_bytes()),release_payload_count=count,author_checks=73,author_negative_controls=11,independent_checks=120,independent_negative_controls=10,corruption_controls_rejected=14,normal_optimized_results_equal=True,original_audit_preserved=True,corrected_v2_controls=True,attribution_only_delta_verified=True,writes_to_release=False,scope='Five retained partial routes; rationality and nonrationality of total space unresolved.'),indent=2))

if __name__=='__main__':main()
