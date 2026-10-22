#!/usr/bin/env python3
"""Audit-package integrity and bounded finite replay; no formal topology claims."""
import hashlib,json,pathlib,subprocess,sys
sys.dont_write_bytecode=True
FILES={'README.md','AUDIT_REPORT.md','IDENTITY_AUDIT.json','SOURCE_AUDIT.json','REPOSITORY_AUDIT.json','corrections/BIBLIOGRAPHY_ADDENDUM.md','code/audit_checks.py','code/check_identity.py','results/finite_controls.json','results/author_replay.json','verify.py'}
def require(ok,text):
    if not ok:raise ValueError(text)
def unique(pairs):
    out={}
    for k,v in pairs:require(k not in out,'duplicate JSON key: '+k);out[k]=v
    return out
def read(path):return json.loads(path.read_text(),object_pairs_hook=unique)
def main():
    require(len(sys.argv)==1,'no arguments accepted');root=pathlib.Path(__file__).resolve().parent;entries=list(root.rglob('*'))
    require(not any(p.is_symlink() for p in entries),'symlink forbidden')
    require({p.relative_to(root).as_posix() for p in entries if p.is_file()}==FILES|{'MANIFEST.json'},'unexpected or missing file')
    m=read(root/'MANIFEST.json');require(set(m)=={'schema_version','files'} and type(m['schema_version']) is int and m['schema_version']==1,'manifest schema mismatch')
    require(isinstance(m['files'],dict) and set(m['files'])==FILES,'manifest file set mismatch')
    for name,meta in m['files'].items():
        require(isinstance(meta,dict) and set(meta)=={'sha256','bytes'},'manifest entry schema mismatch');b=(root/name).read_bytes()
        require(type(meta['bytes']) is int and meta['bytes']==len(b),'size mismatch: '+name)
        require(meta['sha256']==hashlib.sha256(b).hexdigest(),'digest mismatch: '+name)
    expected=read(root/'results/finite_controls.json')
    for mode in [[],['-O']]:
        p=subprocess.run([sys.executable,*mode,'-B',str(root/'code/audit_checks.py')],cwd=root,capture_output=True,text=True);require(p.returncode==0,'finite replay failed: '+p.stderr);require(json.loads(p.stdout,object_pairs_hook=unique)==expected,'finite replay mismatch')
    require(expected['all_pass'] is True and expected['exhaustive_labeled_graphs_vertices_0_through_5']==1100,'finite scope mismatch')
    r=read(root/'results/author_replay.json');require(r['all_pass'] is True and r['relocated_normal_and_optimized_pass'] is True,'author replay failure')
    require(r['author_archive_sha256']=='a7085468b08f93b8422c2764799a0712b806e2772292cbafe5514b38851fb5b9' and r['author_archive_bytes']==14171,'author anchor mismatch')
    require(r['author_manifest_sha256']=='a06410f384f30791a067a97d639b0ec73eaf7df75334fcc4dd0cb896987b9b61','author manifest anchor mismatch')
    cases=r['normal_and_optimized_cases'];require(len(cases)==30,'author replay case count mismatch')
    names={'clean','missing_proof','changed_proof','extra_file','symlink','duplicate_manifest_key','wrong_size','traversal_entry','no_square_removed','flag_removed','pl_strengthened','wrong_identity','false_recorded_result','broken_mathematical_control','forged_all_pass'}
    require({(x['case'],x['optimized']) for x in cases}=={(n,o) for n in names for o in [False,True]},'author replay case set mismatch')
    for x in cases:require(x['expected_outcome_observed'] is True and (x['exit_code']==0)==(x['case']=='clean'),'author mutation outcome mismatch')
    require(r['independent_finite_controls']==expected,'independent controls mismatch')
    identity=read(root/'IDENTITY_AUDIT.json');require(identity['identity_pass'] is True and identity['target_id']==6200014 and identity['catalog_rank']==808,'identity mismatch')
    require(identity['review_sha256']=='1ec3eb8a33545c474dae36d4b1ed4c07552f04d21401776d3e67d4c14c057dd6','review digest mismatch')
    print(json.dumps({'audit_integrity_pass':True,'verified_files':len(FILES),'finite_controls_normal_and_optimized_pass':True,'author_recorded_clean_passes':2,'author_recorded_mutation_rejections':28,'exhaustive_graphs':1100,'author_archive_reexecuted_by_this_command':False,'topological_theorems_formally_verified':False},sort_keys=True,indent=2))
if __name__=='__main__':
    try:main()
    except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
