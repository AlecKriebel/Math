#!/usr/bin/env python3
"""Read-only canonical install selection and text/code inventory audit."""
from pathlib import Path, PurePosixPath
import ast
import hashlib
import json
import re
import zipfile

OUT=Path(__file__).resolve().parent
AUDIT=OUT.parent.parent
REPO=AUDIT.parents[2]
PKG=AUDIT/'package'
count=0

def need(ok,label):
    global count
    count+=1
    if not ok:raise RuntimeError(label)

def object_pairs(pairs):
    out={}
    for k,v in pairs:
        need(k not in out,'duplicate JSON key')
        out[k]=v
    return out

def parse(data):return json.loads(data,object_pairs_hook=object_pairs)

def digest(data):return hashlib.sha256(data).hexdigest()

def safe(name):
    p=PurePosixPath(name)
    need(type(name)is str and p.as_posix()==name and not p.is_absolute() and '..' not in p.parts,'path alias/escape')
    need(not set(p.parts)&{'private_sources','private_cases','mutation_fixtures','.venv','venv','__pycache__','.secrets','.zenodo-state'},'forbidden path')

def run():
    manifest=parse((PKG/'SHA256SUMS.json').read_bytes())
    freeze=parse((AUDIT/'PACKAGE_REVIEW_INPUT_2.json').read_bytes())
    plan=parse((AUDIT/'BRANCH_INSTALL_PLAN.json').read_bytes())
    expected=set(manifest['files'])|{'SHA256SUMS.json'}|set(freeze['files'])
    entries=plan['entries']
    prefix='unsolved_math_prioritization/attempts/30004807/preprint_20261012/'
    need(plan['positive_selection_only']is True,'positive install flag')
    need(len(entries)==185 and len({x['repository_destination'] for x in entries})==185,'install count/uniqueness')
    seen=set()
    for item in entries:
        local=item['local_program_path'];dest=item['repository_destination']
        safe(local);safe(dest)
        file=REPO/local
        need(file.is_file() and not file.is_symlink() and file.resolve().is_relative_to(PKG),'install local containment')
        relative=file.relative_to(PKG).as_posix()
        need(dest==prefix+relative,'install exact destination')
        need(relative not in seen,'install duplicate source');seen.add(relative)
        data=file.read_bytes()
        need(type(item['bytes'])is int and len(data)==item['bytes'] and digest(data)==item['sha256'],'install hash/size')
    need(seen==expected,'install union matches frozen archive and outputs')
    json_count=0;python_count=0;unique_python={};imports=set();secret_hits=[]
    patterns=[r'ghp_[A-Za-z0-9]{30,}',r'github_pat_[A-Za-z0-9_]{30,}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----',r'ya29\.[A-Za-z0-9_-]{25,}']
    with zipfile.ZipFile(PKG/'regular_zas_bianchi_verification_v1.zip') as z:
        for item in z.infolist():
            data=z.read(item.filename);text=data.decode('utf-8')
            need(not item.flag_bits&1,'encrypted archive entry')
            if item.filename.endswith('.json'):
                parse(text);json_count+=1
            if item.filename.endswith('.py'):
                tree=ast.parse(text);python_count+=1;unique_python[digest(data)]=item.filename
                for node in ast.walk(tree):
                    if isinstance(node,ast.Import):imports.update(x.name.split('.')[0] for x in node.names)
                    if isinstance(node,ast.ImportFrom) and node.module:imports.add(node.module.split('.')[0])
            if any(re.search(p,text) for p in patterns):secret_hits.append(item.filename)
    need(not secret_hits,'high specificity credential signature')
    need(not imports&{'requests','httpx','urllib','socket','google','keyring'},'unexpected network/credential Python import')
    return {'verdict':'PASS','explicit_check_count':count,'install_entries':len(entries),'exact_install_union':True,'text_archive_entries':181,'json_entries_duplicate_keys_checked':json_count,'python_entries_AST_parsed':python_count,'unique_python_sources':len(unique_python),'python_import_roots':sorted(imports),'high_specificity_credential_pattern_hits':secret_hits,'credential_scan_is_not_universal_oracle':True,'no_external_calls':True}

if __name__=='__main__':print(json.dumps(run(),indent=2,sort_keys=True))
