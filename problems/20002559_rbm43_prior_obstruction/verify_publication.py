#!/usr/bin/env python3
"""Strict package integrity; separate portable and external-input replay levels."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
MANIFEST = 'PUBLICATION_MANIFEST.json'
INNER_PINS = {'author':'a0200ecddcdc503e9e8f8e1f06960050eb7049a6061f659a48a3f0b782ff28d9',
              'audit':'ffd2d970178c3597ed81ac6870eebbad202cdd8fe38ee20998eacdc7a13b6b69'}
SOURCE_PINS = {'appendix.md':(3785,'7e4ac6e492f2e1278f82b4c91dddd15de8f7e014beb3c2d62a63a6f3fe04e3f0'),
               'certificate.json':(20691,'451797a35b04ef35c603b872cc965fc6adebaf43da49dc4b1ac3a6e32b34f1e7')}

def need(ok,why):
    if not ok: raise ValueError(why)

def sha(b): return hashlib.sha256(b).hexdigest()
def blob(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def pairs(items):
    out={}
    for k,v in items:
        need(k not in out,'duplicate JSON key')
        out[k]=v
    return out

def read_json(raw): return json.loads(raw,object_pairs_hook=pairs)

def check_queue(root,queue):
    need(queue.is_file() and not queue.is_symlink(),'queue regular file')
    q=read_json((root/'QUEUE_PATCH.json').read_bytes());raw=queue.read_bytes()
    need((len(raw),sha(raw),blob(raw))==(q['updated_bytes'],q['updated_sha256'],q['updated_blob']),'updated queue identity')
    lines=raw.splitlines(keepends=True)
    rows=[i for i,line in enumerate(lines) if b'| 20002559 /' in line]
    need(rows==[q['line_number']-1],'queue target uniqueness')
    i=rows[0];cells=lines[i].split(b'|');old=cells[:]
    need(cells[1].strip()==b'763','rank')
    for index,key in [(8,'Status'),(9,'Turns'),(11,'Findings')]:
        need(cells[index].decode()==q['new_values'][key],'new queue value '+key)
        old[index]=q['old_values'][key].encode()
    need(cells[8]==b' already_solved ' and cells[9]==b' 1/5 ','queue disposition')
    need(q['changed_indices']==[8,9,11] and q['changed_cells']==['Status','Turns','Findings'],'queue metadata')
    need([k for k in range(len(cells)) if cells[k]!=old[k]]==[8,9,11],'three cells only')
    lines[i]=b'|'.join(old);base=b''.join(lines)
    need((len(base),sha(base),blob(base))==(q['base_bytes'],q['base_sha256'],q['base_blob']),'exact old queue restoration')
    return {'changed_cells':['Status','Turns','Findings'],'all_other_bytes_preserved':True,'chat_doi_and_stale_header_preserved':True}

def verify(root,pin,queue=None):
    need(root.is_dir() and not root.is_symlink(),'package directory')
    mpath=root/MANIFEST
    need(mpath.is_file() and not mpath.is_symlink(),'manifest regular file')
    raw=mpath.read_bytes()
    need(re.fullmatch('[0-9a-f]{64}',pin) and sha(raw)==pin,'external manifest pin')
    m=read_json(raw)
    need(m['schema']=='rbm43-prior-obstruction-publication-v1' and m['problem_id']==20002559,'manifest schema')
    entries={}
    for row in m['files']:
        name=row['path'];p=PurePosixPath(name)
        need(re.fullmatch('[A-Za-z0-9_./-]+',name) and not p.is_absolute() and str(p)==name and '..' not in p.parts and name not in ('.',MANIFEST) and name not in entries,'manifest path')
        need(type(row['bytes']) is int and row['bytes']>=0 and re.fullmatch('[0-9a-f]{64}',row['sha256']),'manifest value')
        entries[name]=row
    actual=set();dirs=set()
    for p in root.rglob('*'):
        need(not p.is_symlink(),'package symlink')
        name=p.relative_to(root).as_posix()
        if p.is_dir(): dirs.add(name);continue
        need(stat.S_ISREG(p.stat().st_mode),'nonregular file');actual.add(name)
    need(actual==set(entries)|{MANIFEST},'complete inventory')
    need(dirs=={str(p) for name in entries for p in PurePosixPath(name).parents if str(p)!='.'},'directory inventory')
    for name,row in entries.items():
        b=(root/name).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['sha256'],'payload identity '+name)
    for folder,expected in INNER_PINS.items():
        b=(root/folder/'MANIFEST.json').read_bytes();need(sha(b)==expected,'inner manifest pin')
        inner=read_json(b);names=[r['path'] for r in inner['files']]
        need(len(names)==len(set(names)) and {p.name for p in (root/folder).iterdir()}==set(names)|{'MANIFEST.json'},'inner inventory')
        for row in inner['files']:
            need('/' not in row['path'],'inner path')
            b=(root/folder/row['path']).read_bytes();need((len(b),sha(b))==(row['bytes'],row['sha256']),'inner file')
    s=read_json((root/'PUBLICATION_STATUS.json').read_bytes())
    need(s['status']=='already_solved' and s['turns_used']==1 and s['turn_limit']==5,'disposition')
    need(s['selectors_covered']==16777216 and s['hidden_units_universality_bounds']==[4,6],'scope')
    for k in ['exact_hidden_units_threshold_claimed','journal_acceptance_claimed','human_specialist_review_claimed','formal_verification_claimed','novelty_claimed','source_contents_bundled','source_free_portable_check_proves_full_result','zenodo_landing_independently_verified']:
        need(s[k] is False,'scope nonclaim '+k)
    need(s['missing_external_input_status']=='NOT_RUN','missing source status')
    a=read_json((root/'audit/VERDICT.json').read_bytes())
    need(a['verdict']=='PASS' and a['recommended_disposition']=='already_solved' and not a['required_revisions'],'audit gate')
    return {'integrity':'PASS','package_files':len(actual),'queue':check_queue(root,queue) if queue else 'NOT_RUN: no queue supplied'}

def run(root,script,*args):
    flags=['-I','-B']+(['-O'] if sys.flags.optimize else [])
    with tempfile.TemporaryDirectory(prefix='rbm replay working directory ') as cwd:
        p=subprocess.run([sys.executable,*flags,str(root.resolve()/script),*map(str,args)],cwd=cwd,capture_output=True,text=True,timeout=900,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
    need(p.returncode==0,script+' failed: '+p.stderr)
    return read_json(p.stdout)

def portable(root):
    spec=importlib.util.spec_from_file_location('rbm_author',root/'author/verify_reconstruction.py')
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    positive=module.exact_controls()
    chart=run(root,'author/verify_prior_local_chart.py')
    need(chart==read_json((root/'author/prior_local_chart_receipt.json').read_bytes()),'local chart saved receipt')
    return {'status':'PASS_LIMITED_PORTABLE_CHECKS','exact_positive_target':positive,'local_chart':chart,'full_certificate_replay':'NOT_RUN: external source inputs required'}

def source_check(sources):
    if sources is None or not sources.is_dir(): return ['appendix.md','certificate.json']
    missing=[name for name in SOURCE_PINS if not (sources/name).is_file()]
    if missing: return missing
    for name,(size,pin) in SOURCE_PINS.items():
        f=sources/name;need(not f.is_symlink(),'external source symlink')
        b=f.read_bytes();need((len(b),sha(b))==(size,pin),'external source hash/size '+name)
    return []

def full(root,sources):
    missing=source_check(sources)
    if missing: return {'status':'NOT_RUN','reason':'Required external source input missing','missing':missing}
    sources=sources.resolve(); optimized=bool(sys.flags.optimize)
    specs=[('author/verify_reconstruction.py',[sources/'certificate.json',sources/'appendix.md'],'author/reconstruction_optimized_receipt.json' if optimized else 'author/reconstruction_receipt.json'),
           ('author/test_reconstruction.py',[sources/'certificate.json',sources/'appendix.md'],'author/adversarial_optimized_receipt.json' if optimized else 'author/adversarial_receipt.json'),
           ('audit/audit_certificate.py',[sources/'appendix.md',sources/'certificate.json'],'audit/fresh_audit_optimized_receipt.json' if optimized else 'audit/fresh_audit_receipt.json')]
    outputs={}
    for script,args,saved in specs:
        result=run(root,script,*args);need(result==read_json((root/saved).read_bytes()),'fresh replay/saved receipt mismatch '+script)
        outputs[script]=result
    audit=outputs['audit/audit_certificate.py']
    need(audit['full_shannon_cover']['covered']==audit['full_matrix_cover']['covered']==16777216,'full selector counts')
    return {'status':'PASS_FULL_EXTERNAL_CERTIFICATE_REPLAY','selectors':16777216,'author_negative_controls':len(outputs['author/test_reconstruction.py']['rejected_cases']),'audit_controls':len(audit['controls']),'source_pins_verified':True,'all_saved_receipts_matched':True,'auxiliary_and_complete_corpus_replays':'NOT_RUN: use separate audit README commands'}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('expected_manifest');p.add_argument('--queue',type=Path);p.add_argument('--full',action='store_true');p.add_argument('--sources',type=Path)
    a=p.parse_args();result=verify(a.root,a.expected_manifest,a.queue);result['portable']=portable(a.root)
    if a.full: result['full']=full(a.root,a.sources)
    verify(a.root,a.expected_manifest,a.queue)
    print(json.dumps(result,sort_keys=True,indent=2))
    if a.full and result['full']['status']=='NOT_RUN': return 2
    return 0

if __name__=='__main__':
    raise SystemExit(main())
