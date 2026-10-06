#!/usr/bin/env python3
"""Static, fail-closed byte/scope verification. Does not execute archived programs."""
from pathlib import Path,PurePosixPath
import difflib,hashlib,io,json,stat,sys,zipfile
PINS={
'archives/CHORD_DENSE_CYCLES_2228_AUTHOR_SAFE_FREEZE.zip':(11900,'970e1d0e9eeee5ff0357c91aabba26f6343955e936167280726a05b0ac68ffdd'),
'archives/CHORD_DENSE_CYCLES_2228_AUTHOR_EXTERNAL_MANIFEST.json':(1869,'5189f13df28414cb1438e75782e332f0d1db2a26d193f5b6135e195fb537ce82'),
'archives/CHORD_DENSE_CYCLES_2228_INDEPENDENT_AUDIT_SAFE.zip':(37619,'3655d8afc3e98e8c6d4c7133db1ce105e3604f2eee79801499886f8be9b2e5c5'),
'archives/CHORD_DENSE_CYCLES_2228_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json':(5673,'521c8019803819e8619ebb560c5b7dda197fc73b65e0dc3b3abcc50961fa3cac')}
EXTRA={'INDEPENDENT_AUDIT_RECEIPT.json','README.md','RESEARCH_LOG.md','PUBLICATION_METADATA.json','PUBLICATION_SOURCE_CHECKS.json','PUBLICATION_MANIFEST.json','PUBLICATION_TEST_RESULTS.json','EXECUTABLE_REPLAY_RESULTS.json','verify_publication.py','replay_checks.py'}
def need(x,m):
    if not x:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def identity(b):return len(b),sha(b)
def safe(n):
    p=PurePosixPath(n);return bool(n) and not p.is_absolute() and '..' not in p.parts and '.' not in n.split('/') and '\\' not in n and n==p.as_posix()
def zip_check(raw,rows,prefix,mode):
    names=[x['path'] for x in rows];need(len(names)==len(set(names)),'duplicate manifest member')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        actual=z.namelist();need(len(actual)==len(set(actual)) and set(actual)==set(names),'ZIP exact member set')
        out={}
        for row in rows:
            n=row['path'];need(safe(n) and n.startswith(prefix),'unsafe ZIP member');info=z.getinfo(n);need(stat.S_ISREG(info.external_attr>>16) and info.external_attr>>16==mode,'ZIP regular member mode');b=z.read(n);need(identity(b)==(row['bytes'],row['sha256']),'ZIP member pin');out[n[len(prefix):]]=b
        need(z.testzip() is None,'ZIP CRC')
        return out

def validate(files,check_manifest=True):
    for name,pin in PINS.items():need(name in files and identity(files[name])==pin,'fixed external pin: '+name)
    am=json.loads(files['archives/CHORD_DENSE_CYCLES_2228_AUTHOR_EXTERNAL_MANIFEST.json']);bm=json.loads(files['archives/CHORD_DENSE_CYCLES_2228_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json'])
    za='archives/CHORD_DENSE_CYCLES_2228_AUTHOR_SAFE_FREEZE.zip';zb='archives/CHORD_DENSE_CYCLES_2228_INDEPENDENT_AUDIT_SAFE.zip'
    for m,z in [(am,za),(bm,zb)]:need((m['archive']['bytes'],m['archive']['sha256'])==PINS[z],'manifest archive binding')
    author=zip_check(files[za],[dict(x,path='chord_dense_cycles_2228/'+x['path']) for x in am['files']],'chord_dense_cycles_2228/',0o100644)
    audit=zip_check(files[zb],bm['files'],'chord_dense_cycles_2228_independent_audit/',0o100444)
    need(len(author)==8 and len(audit)==21,'frozen member counts');expected=set(PINS)|EXTRA
    for leaf,members in [('original_author',author),('independent_audit',audit)]:
        for name,b in members.items():path=leaf+'/'+name;need(files.get(path)==b,'loose member differs: '+path);expected.add(path)
    need(set(files)==expected,'exact publication inventory')
    for n,b in files.items():
        need(safe(n),'unsafe public path')
        if not n.endswith('.zip'):
            text=b.decode('utf-8');need(all(x not in text for x in ['/'+'work'+'space/','/'+'home/'+'agent/','codex:'+ '/'+'/threads/','private_'+'sources/','agent_'+'notes/']),'local or private path')
    internal=json.loads(audit['MANIFEST.json']);rows=internal['files'];need(len(rows)==20 and len({x['path'] for x in rows})==20 and {x['path'] for x in rows}==set(audit)-{'MANIFEST.json'},'audit internal inventory')
    for row in rows:need(identity(audit[row['path']])==(row['bytes'],row['sha256']),'audit internal pin')
    need(sha(audit['MANIFEST.json'])==bm['internal_manifest_sha256']=='205501b7ebfe2f7449fb18d5832e330c122f567a936142affcdb81a93b738855','internal manifest binding')
    need(audit['author_external_manifest.json']==files['archives/CHORD_DENSE_CYCLES_2228_AUTHOR_EXTERNAL_MANIFEST.json'],'same author manifest')
    for n,b in author.items():need(audit['author_original/'+n]==b,'historical author preservation')
    receipt=json.loads(files['INDEPENDENT_AUDIT_RECEIPT.json']);need(receipt['problem_id']==2228 and receipt['problem_number']=='EP-642' and receipt['status']=='partial_stalled' and receipt['approaches_used']==3,'receipt scope')
    need(identity(audit['acceptance_report.json'])==(2710,'5938fef56d81def5ea6c05704e047dbfbc00119c980bab13b81219a1c19e0ba8'),'exact acceptance pin')
    need(receipt['acceptance_report_sha256']==sha(audit['acceptance_report.json']) and receipt['audit_report_sha256']==sha(audit['audit_report.md']),'receipt report binding')
    acceptance=json.loads(audit['acceptance_report.json']);need(acceptance['decision']=='accept_elementary_partial_results_and_hardened_validation' and acceptance['status']=='partial_stalled' and acceptance['approaches_used']==3 and acceptance['approach_cap']==5,'accepted disposition')
    for k in ['full_solution_accepted','asymptotic_improvement_accepted','novelty_accepted','original_optimized_validation_accepted','mathematical_correction_required','cited_papers_complete_proofs_accepted','missing_historical_sources_certified']:need(acceptance[k] is False,'acceptance exclusion')
    need(acceptance['corrected_normal_and_optimized_validation_accepted'] is True and acceptance['validation_correction_required'] is True,'hardening accepted')
    patch=''.join(difflib.unified_diff(author['validation.py'].decode().splitlines(True),audit['corrected/validation.py'].decode().splitlines(True),fromfile='author_original/validation.py',tofile='corrected/validation.py')).encode()
    need(patch==audit['validation_hardening.patch'],'actual patch differs from exact derivative diff')
    need(audit['corrected/validation_results.json']==author['validation_results.json'],'unchanged finite result bytes')
    for row in acceptance['accepted_derivative_files']:need(identity(audit[row['path']])==(row['bytes'],row['sha256']),'exact accepted derivative')
    meta=json.loads(files['PUBLICATION_METADATA.json']);need(meta['problem_id']==2228 and meta['problem_number']=='EP-642' and meta['rank']==900 and meta['queue_status']=='partial' and meta['research_status']=='partial_stalled','publication identity/disposition');need(type(meta['approaches_used'])is int and meta['approaches_used']==3 and meta['approach_cap']==5,'approach budget')
    for k in ['full_solution_accepted','asymptotic_improvement_accepted','novelty_accepted','original_optimized_validation_accepted','mathematical_correction_required','exhaustive_best_known_claim','forum_exponent_seven_certified','historical_original_sources_certified','entire_cited_paper_proofs_certified','formal_verification_claimed','human_peer_review_claimed']:need(meta[k] is False,'publication overclaim: '+k)
    need(meta['corrected_normal_and_optimized_validation_accepted'] is True and meta['validation_correction_required'] is True and meta['historical_freeze_fields_preserved'] is True,'publication hardening/preservation')
    need(meta['acceptance_sha256']==sha(audit['acceptance_report.json']) and meta['audit_report_sha256']==sha(audit['audit_report.md']) and meta['patch_sha256']==sha(patch),'exact report and patch binding')
    need(meta['strongest_verified_bound']=='O(n(log n)^8)','literature bound')
    q=meta['queue'];need(q['changed_cells']==['Status','Turns'] and q['status']=='partial' and q['turns']=='3/5' and q['findings_preserved'] is True and q['unrelated_bytes_preserved'] is True,'queue allowed scope')
    replay=json.loads(files['EXECUTABLE_REPLAY_RESULTS.json']);need(replay['normal_optimized_equal'] is True and replay['corpus']['status']=='PASS' and replay['public_pdf_identity']['status']=='PASS','full replay receipt');need(replay['semantic_mutation_rejections']==10 and replay['integrity_mutation_rejections']==16 and replay['finite_checks_prove_infinite_target'] is False and replay['original_optimized_checks_active'] is False,'active validation boundaries')
    need(replay['runs']['independent_relocated_normal']['all_labeled_graphs_orders_0_through_5']==1100,'oracle finite scope');need(replay['runs']['mutations_relocated_normal']['patch_reconstructs_exact_derivative'] is True,'actual patch replay')
    if check_manifest:
        m=json.loads(files['PUBLICATION_MANIFEST.json']);rows=m['files'];need(m['schema']=='public-file-manifest-v1' and len(rows)==len(files)-1 and len({x['path'] for x in rows})==len(rows) and {x['path'] for x in rows}==set(files)-{'PUBLICATION_MANIFEST.json'},'publication manifest exact inventory')
        for row in rows:need(identity(files[row['path']])==(row['bytes'],row['sha256']),'publication manifest pin')
    return {'status':'PASS','files_checked':len(files),'author_archive_members':8,'audit_archive_members':21,'archive_and_loose_bytes_equal':True,'exact_acceptance_bound':True,'exact_patch_diff_verified':True,'archive_code_executed_by_this_program':False,'finite_checks_prove_infinite_target':False}

def main():
    root=Path(sys.argv[1] if len(sys.argv)>1 else '.').resolve();paths=list(root.rglob('*'));need(not any(p.is_symlink() for p in paths),'symlink in publication');files={p.relative_to(root).as_posix():p.read_bytes() for p in paths if p.is_file()};result=validate(files);rejections=[]
    def reject(label,alter,manifest=False):
        f=dict(files);alter(f)
        try:validate(f,manifest)
        except (ValueError,KeyError,UnicodeDecodeError,zipfile.BadZipFile,json.JSONDecodeError):rejections.append(label);return
        raise ValueError('negative control accepted: '+label)
    for n in PINS:reject('changed external pin '+n,lambda f,n=n:f.__setitem__(n,f[n]+b'x'))
    for n in ['original_author/proof_note.md','original_author/validation.py','independent_audit/acceptance_report.json','independent_audit/audit_report.md','independent_audit/validation_hardening.patch','independent_audit/corrected/validation.py','independent_audit/corrected/validation_results.json']:reject('changed loose member '+n,lambda f,n=n:f.__setitem__(n,f[n]+b'x'))
    reject('missing member',lambda f:f.pop('original_author/proof_note.md'));reject('extra member',lambda f:f.__setitem__('extra.txt',b'x'));reject('path traversal',lambda f:f.__setitem__('../escape',b'x'))
    for key,value in [('queue_status','verified_solved'),('approaches_used',4),('full_solution_accepted',True),('original_optimized_validation_accepted',True),('novelty_accepted',True),('asymptotic_improvement_accepted',True),('exhaustive_best_known_claim',True),('forum_exponent_seven_certified',True),('validation_correction_required',False),('formal_verification_claimed',True)]:
        def alter(f,k=key,v=value):m=json.loads(f['PUBLICATION_METADATA.json']);m[k]=v;f['PUBLICATION_METADATA.json']=json.dumps(m).encode()
        reject('bad claim '+key,alter)
    def queue_attack(f):m=json.loads(f['PUBLICATION_METADATA.json']);m['queue']['findings_preserved']=False;f['PUBLICATION_METADATA.json']=json.dumps(m).encode()
    reject('changed Findings scope',queue_attack)
    reject('stale wrapper manifest',lambda f:f.__setitem__('README.md',f['README.md']+b'x'),True)
    def manifest_attack(f):m=json.loads(f['PUBLICATION_MANIFEST.json']);m['files'].pop();f['PUBLICATION_MANIFEST.json']=json.dumps(m).encode()
    reject('missing publication manifest entry',manifest_attack,True)
    # Exercise archive structure rejection independently of the outer digest.
    for label,names in [('duplicate',['x/a','x/a']),('traversal',['x/../a']),('absolute',['/x/a']),('backslash',['x/a\\b'])]:
        raw=io.BytesIO()
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            with zipfile.ZipFile(raw,'w') as z:
                for n in names:
                    info=zipfile.ZipInfo(n);info.external_attr=0o100644<<16;z.writestr(info,b'x')
        rows=[{'path':n,'bytes':1,'sha256':sha(b'x')} for n in names]
        try:zip_check(raw.getvalue(),rows,'x/',0o100644)
        except ValueError:rejections.append('hostile ZIP '+label)
        else:raise ValueError('hostile ZIP accepted')
    result['negative_controls_rejected']=rejections;result['negative_control_count']=len(rejections);print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
