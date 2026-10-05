#!/usr/bin/env python3
"""Strict read-only publication inventory and frozen exact replay. Standard library only."""
import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

BASE=Path(__file__).resolve().parent
FROZEN={'author':'6dc7b5dc2209ed8ef3285b4b7da123df2285d328236b907fd7bad4ff17098c9e',
        'audit':'5e3be31007fb2221ed44c57d41bb17d8026f447ea186d6b3d007ed73d077b397'}
def require(ok,message):
    if not ok:raise RuntimeError(message)
def digest(b):return hashlib.sha256(b).hexdigest()
def main():
    paths=list(BASE.rglob('*'))
    require(not any(p.is_symlink() for p in paths),'symlink forbidden')
    require(all(p.is_file() or p.is_dir() for p in paths),'nonregular member')
    raw=(BASE/'MANIFEST.json').read_bytes();m=json.loads(raw)
    require((BASE/'MANIFEST.sha256').read_text()==digest(raw)+'  MANIFEST.json\n','manifest binding')
    require(set(m)=={'schema_version','problem_id','files'} and m['schema_version']==1 and m['problem_id']=='30003070','manifest identity')
    names=[]
    for e in m['files']:
        require(set(e)=={'path','bytes','sha256'},'manifest entry fields')
        name=e['path'];p=PurePosixPath(name)
        require(isinstance(name,str) and re.fullmatch(r'[A-Za-z0-9_./-]+',name) and not p.is_absolute() and '..' not in p.parts and str(p)==name,'unsafe manifest path')
        require(name not in {'MANIFEST.json','MANIFEST.sha256'},'recursive manifest member')
        require(type(e['bytes']) is int and e['bytes']>=0 and re.fullmatch('[0-9a-f]{64}',e['sha256']),'entry metadata')
        names.append(name)
    require(len(names)==len(set(names)),'duplicate manifest path')
    require({p.relative_to(BASE).as_posix() for p in paths if p.is_file()}==set(names)|{'MANIFEST.json','MANIFEST.sha256'},'file inventory mismatch')
    require({p.relative_to(BASE).as_posix() for p in paths if p.is_dir()}=={'author','audit'},'directory inventory mismatch')
    for e in m['files']:
        b=(BASE/e['path']).read_bytes()
        require(len(b)==e['bytes'] and digest(b)==e['sha256'],'payload mismatch: '+e['path'])
    for folder,pinned in FROZEN.items():
        raw=(BASE/folder/'MANIFEST.json').read_bytes()
        require(digest(raw)==pinned,'frozen manifest changed: '+folder)
        frozen=json.loads(raw)
        for e in frozen['files']:
            b=(BASE/folder/e['name']).read_bytes()
            require(len(b)==e['bytes'] and digest(b)==e['sha256'],'frozen payload changed')
    s=json.loads((BASE/'release_status.json').read_text())
    require(s['schema_version']==1 and s['problem_id']=='30003070' and s['rank']==729 and s['status']=='unsolved' and s['turns']=='5/5','publication disposition')
    require(s['independent_audit']=='scoped PASS' and s['scope_clarifications']=='PUBLICATION_SCOPE.md','audit scope')
    require(s['frozen_author_manifest_sha256']==FROZEN['author'] and s['frozen_audit_manifest_sha256']==FROZEN['audit'],'status freeze binding')
    for key in ['full_solution','full_counterexample','verified_full_prior_resolution','novelty_claim','global_current_openness_claim','cube_embedding_constructs_root_sequence','raw_statement_inspected','prior_ai_report_inspected','raw_retrieval_retried']:
        require(s[key] is False,'scope overclaim: '+key)
    q=s['queue_change']
    require(q['changed_rows']==1 and q['changed_cells']==['Status','Turns'] and q['after_status']=='unsolved' and q['after_turns']=='5/5','queue scope')
    require(q['all_other_bytes_unchanged'] is True and q['findings_chat_doi_unchanged'] is True and q['embedded_stale_header_preserved'] is True,'queue preservation')
    for p in BASE.rglob('*.py'):
        require(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(p.read_text()))),'optimization-sensitive assertion: '+p.name)
    flags=['-B']+(['-OO'] if sys.flags.optimize>1 else ['-O'] if sys.flags.optimize else [])
    def run(script):
        r=subprocess.run([sys.executable,*flags,str(BASE/script)],cwd='/tmp',capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
        require(r.returncode==0 and not r.stderr,'replay failed '+script+': '+r.stderr.decode(errors='replace'))
        return json.loads(r.stdout)
    a=run('author/verify_release.py');n=run('author/verify_negative_controls.py');v=run('audit/verify_audit.py')
    require(a['status']=='PASS' and a['math_checks']==32332 and a['source_pdfs_verified']==0,'author replay scope')
    require(n['status']=='PASS' and n['negative_controls_rejected']==13,'author negative controls')
    require(v['status']=='PASS' and v['independent_math_checks']==68132 and v['optional_author_and_source_replay'] is False,'audit portable replay scope')
    print(json.dumps({'status':'PASS','problem_id':'30003070','disposition':'unsolved, 5/5','publication_files':len(names)+2,'publication_manifest_sha256':digest((BASE/'MANIFEST.json').read_bytes()),'frozen_trees_unchanged':True,'author_math_checks':32332,'independent_math_checks':68132,'author_negative_controls_rejected':13,'source_pdfs_required':False,'network_required':False,'writes_performed':False},sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('FAIL: '+str(exc),file=sys.stderr)
        raise SystemExit(1)
