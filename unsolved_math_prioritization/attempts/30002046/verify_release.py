#!/usr/bin/env python3
"""Offline immutable-packet replay and actual corruption tests; not a proof assistant."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, json, shutil, subprocess, sys, tempfile
AUTHOR=set('APPROACH_LOG.md EXACT_RESULTS.json MANIFEST.json PROOFS.md README.md SOURCE_VERIFICATION.json STATUS.json VERIFY_LOG.txt verify.py'.split())
AUDIT=set('AUDIT_MANIFEST.json AUDIT_REPORT.md AUTHOR_REPLAY_LOG.txt BINDING.json INDEPENDENT_RESULTS.json INDEPENDENT_RUN_LOG.txt README.md SOURCE_AUDIT.json independent_verify.py'.split())
TOP=set('README.md RELEASE_STATUS.json RELEASE_MANIFEST.json REPLAY_RESULTS.json verify_release.py'.split())
EXPECTED=TOP|{'author/'+s for s in AUTHOR}|{'independent_audit/'+s for s in AUDIT}
PINS={'author/MANIFEST.json':'faf4f5f3d6069420dd4a975a6320e704bdb6f190f64a1626863c5ff1e08bd045','independent_audit/AUDIT_MANIFEST.json':'dde9bcdfc6089c3e48b93fbff102c04ccb234d5f1f9c840b9b19e4b8dbe77802','independent_audit/AUDIT_REPORT.md':'23efa154042224c3d4823b7c51605ab8841dbe7b40aad89fd7b73042e7dc28a4'}
CLARIFICATION='The implemented tests use strict inequalities.'
WIDTH='1/81426020110025487843678548887211712316576276539'
def need(v,message):
    if not v: raise ValueError(message)
def digest(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_bytes())
def check(root,row):
    s=row['path'];p=PurePosixPath(s);need(not p.is_absolute() and '..' not in p.parts and str(p)==s,'unsafe path')
    b=(root/s).read_bytes();need(len(b)==row['bytes'] and digest(b)==row['sha256'],'byte binding: '+s)
def manifest(root,name,inventory):
    rows=read(root/name)['files'];need(len(rows)==len(inventory)-1 and {r['path'] for r in rows}==inventory-{name},'manifest inventory')
    for row in rows:check(root,row)
def verify(root,replay=True):
    files,dirs=set(),set()
    for p in root.rglob('*'):
        need(not p.is_symlink(),'symlink');name=p.relative_to(root).as_posix()
        if p.is_file():files.add(name)
        else:need(p.is_dir(),'special node');dirs.add(name)
    need(files==EXPECTED and dirs=={'author','independent_audit'},'exact inventory')
    manifest(root,'RELEASE_MANIFEST.json',EXPECTED)
    for name,pin in PINS.items():need(digest((root/name).read_bytes())==pin,'immutable pin: '+name)
    manifest(root/'author','MANIFEST.json',AUTHOR);manifest(root/'independent_audit','AUDIT_MANIFEST.json',AUDIT)
    b=read(root/'independent_audit/BINDING.json');need(b['input']['manifest_sha256']==PINS['author/MANIFEST.json'] and b['input']['manifest_bytes']==1493,'audit input pin')
    need({r['path'] for r in b['input']['payload_files']}==AUTHOR-{'MANIFEST.json'} and len(b['input']['payload_files'])==8,'audit bound inventory')
    for row in b['input']['payload_files']:check(root/'author',row)
    s=read(root/'RELEASE_STATUS.json');need(s['problem_id']=='30002046' and s['rank']==713 and s['problem_code']=='OWR-11784-003','identity')
    need(s['queue_status']=='unsolved' and s['turns']=='5/5' and s['substantive_approaches']==5,'disposition')
    need(s['audit_verdict']=='PASS_WITH_SCOPE_LIMITS' and s['controlling_clarification']==CLARIFICATION,'audit gate')
    need(s['domain']=='standard Minkowski question-mark function on [0,1]','domain')
    for key in ['strictness_mathematically_necessary','full_count_solution','uniqueness','transcendence','novelty','global_open_status_certified','one_interval_implies_one_root','finite_controls_replace_proof','exact_aggregator_wording_verified','raw_corpus_content_or_hash_verified','final_GS_journal_pdf_inspected','formal_proof_assistant_certificate']:
        need(s[key] is False,'scope: '+key)
    for key in ['complete_lower_half_root_enclosure','frozen_originals_preserved','independent_audit_completed','primary_OWR_count_question_verified','fresh_primary_pdf_hashes_matched','unrefereed','AI_assisted']:
        need(s[key] is True,'scope: '+key)
    for key,value in [('enclosure_nodes',275),('enclosure_leaves',138),('enclosure_exclusions',137),('enclosure_retained_intervals',1),('selected_root_bisections',160),('reduced_rational_inputs',342090),('rational_scan_max_denominator',1500),('audit_certificate_mutations',6)]:need(s[key]==value,'count: '+key)
    need(s['enclosure_width']==WIDTH,'width')
    g=(root/'README.md').read_text()
    for text in [CLARIFICATION,'not mathematically necessary','One interval is not one root.',WIDTH,'HTTP 403','final Gayfulin–Shulga journal PDF was not inspected','unsolved, 5/5','0% certified','finite evidence only']:need(text in g,'guide: '+text)
    a=read(root/'independent_audit/AUDIT_MANIFEST.json');need(a['verdict']=='PASS_WITH_SCOPE_LIMITS' and a['original_manifest_sha256']==PINS['author/MANIFEST.json'],'audit verdict')
    result=dict(integrity='PASS',release_files=len(EXPECTED),author_files=9,audit_files=9,scope='Audited partial results only; exact count unresolved.',author_replay_optimization=False,independent_replay_optimization=bool(sys.flags.optimize))
    if replay:
        for key,script,args,opt in [('author','author/verify.py',['--check'],False),('independent','independent_audit/independent_verify.py',[str(root/'author'),'--check'],bool(sys.flags.optimize))]:
            cmd=[sys.executable,'-I','-B']+(['-O'] if opt else [])+[str(root/script)]+args
            run=subprocess.run(cmd,capture_output=True,cwd=tempfile.gettempdir())
            need(run.returncode==0 and not run.stderr,key+' replay failed: '+run.stderr.decode(errors='replace'))
            expected=(root/('author/VERIFY_LOG.txt' if key=='author' else 'independent_audit/INDEPENDENT_RUN_LOG.txt')).read_bytes()
            need(run.stdout==expected if key=='author' else expected==run.stdout*2,key+' replay output mismatch')
            result[key+'_replay']=dict(status='PASS',stdout_bytes=len(run.stdout),stdout_sha256=digest(run.stdout))
        verify(root,replay=False)
    return result

def corruptions(root):
    cases=['changed_author','changed_audit','changed_guide','missing','extra_hidden','empty_directory','symlink','unlisted_pdf','manifest_traversal','manifest_omission','manifest_duplicate','coordinated_author','coordinated_audit','wrong_status','wrong_turns','necessary_strictness','one_interval_one_root','full_solution','unique','transcendental','novelty','global_openness','aggregator_verified','raw_verified','journal_inspected','wrong_width','missing_clarification']
    rejected=[]
    for case in cases:
        with tempfile.TemporaryDirectory(prefix='question-mark-corruption-') as td:
            p=Path(td)/'packet';shutil.copytree(root,p);outer=read(p/'RELEASE_MANIFEST.json')
            def rebind(name):
                b=(p/name).read_bytes()
                for row in outer['files']:
                    if row['path']==name:row.update(bytes=len(b),sha256=digest(b));return
                raise ValueError('unlisted mutation')
            if case.startswith('changed_'):
                name={'changed_author':'author/PROOFS.md','changed_audit':'independent_audit/AUDIT_REPORT.md','changed_guide':'README.md'}[case]
                b=bytearray((p/name).read_bytes());b[0]^=1;(p/name).write_bytes(b)
            elif case=='missing':(p/'README.md').unlink()
            elif case=='extra_hidden':(p/'.extra').write_text('synthetic')
            elif case=='empty_directory':(p/'author/empty').mkdir()
            elif case=='symlink':(p/'README.md').unlink();(p/'README.md').symlink_to('author/README.md')
            elif case=='unlisted_pdf':(p/'source.pdf').write_bytes(b'%PDF synthetic')
            elif case.startswith('manifest_'):
                if case=='manifest_traversal':outer['files'][0]['path']='../README.md'
                elif case=='manifest_omission':outer['files'].pop()
                else:outer['files'].append(dict(outer['files'][0]))
            elif case.startswith('coordinated_'):
                folder,name,m=('author','PROOFS.md','MANIFEST.json') if case.endswith('author') else ('independent_audit','AUDIT_REPORT.md','AUDIT_MANIFEST.json')
                (p/folder/name).write_bytes((p/folder/name).read_bytes()+b'\nsynthetic\n');j=read(p/folder/m);data=(p/folder/name).read_bytes()
                for row in j['files']:
                    if row['path']==name:row.update(bytes=len(data),sha256=digest(data))
                (p/folder/m).write_text(json.dumps(j));rebind(folder+'/'+name);rebind(folder+'/'+m)
            elif case=='missing_clarification':(p/'README.md').write_text((p/'README.md').read_text().replace(CLARIFICATION,'Strict inequalities are required.'));rebind('README.md')
            else:
                key,value={'wrong_status':('queue_status','solved'),'wrong_turns':('turns','4/5'),'necessary_strictness':('strictness_mathematically_necessary',True),'one_interval_one_root':('one_interval_implies_one_root',True),'full_solution':('full_count_solution',True),'unique':('uniqueness',True),'transcendental':('transcendence',True),'novelty':('novelty',True),'global_openness':('global_open_status_certified',True),'aggregator_verified':('exact_aggregator_wording_verified',True),'raw_verified':('raw_corpus_content_or_hash_verified',True),'journal_inspected':('final_GS_journal_pdf_inspected',True),'wrong_width':('enclosure_width','1/100')}[case]
                j=read(p/'RELEASE_STATUS.json');j[key]=value;(p/'RELEASE_STATUS.json').write_text(json.dumps(j));rebind('RELEASE_STATUS.json')
            (p/'RELEASE_MANIFEST.json').write_text(json.dumps(outer))
            try:verify(p,replay=False)
            except (ValueError,KeyError,OSError):rejected.append(case)
            else:raise RuntimeError('Accepted actual corruption: '+case)
    return rejected
if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--integrity-only',action='store_true');parser.add_argument('--self-test',action='store_true');args=parser.parse_args()
    root=Path(__file__).resolve().parent;result=verify(root,replay=not args.integrity_only)
    if args.self_test:result['actual_corruptions_rejected']=corruptions(root)
    print(json.dumps(result,indent=2,sort_keys=True))
