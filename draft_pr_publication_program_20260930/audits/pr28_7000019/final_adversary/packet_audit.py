#!/usr/bin/env python3
"""Fresh read-only packet gate; isolated copies are the only executed old code."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, shutil, sqlite3, subprocess, sys, os, urllib.request

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
REPO = next(p for p in HERE.parents if (p / '.git').exists())
CANDIDATE = AUDIT / 'reviewed_candidate'
HEAD = '90a81313f3f65a7914fb6d5a9950fa087ea7467e'
BASE = 'c6975ca76f9f667f1250ba403d0e6da2aafe14d0'
PREFIX = 'unsolved_math_prioritization/attempts/7000019/'
PYTHON = '/usr/bin/python3'
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
def sha(b): return hashlib.sha256(b).hexdigest()
def read_json(path): return json.loads(path.read_text())
def command(*args):
    return subprocess.check_output(args, cwd=REPO, env=ENV)
def entries(m): return m.get('files', m.get('artifacts'))
def check_manifest(root, manifest):
    out=[]
    for item in entries(manifest):
        p=root/item['path']; b=p.read_bytes()
        assert len(b)==item['bytes'] and sha(b)==item['sha256'], str(p)
        content=b.decode('utf8')
        if p.suffix=='.json': json.loads(content)
        out.append({'path':item['path'],'bytes':len(b),'sha256':sha(b)})
    return out

def main():
    assert command('git','branch','--show-current').decode().strip()=='main'
    assert sha((CANDIDATE/'MANIFEST.json').read_bytes())=='db23b0e890792a03b5f144348f23b5c6014898ce56ba19948e4740c603da1024'
    candidate=check_manifest(CANDIDATE,read_json(CANDIDATE/'MANIFEST.json'))
    actual=sorted(str(p.relative_to(CANDIDATE)) for p in CANDIDATE.rglob('*') if p.is_file() and p.name!='MANIFEST.json')
    assert actual==sorted(x['path'] for x in candidate) and len(candidate)==28
    deps=check_manifest(AUDIT,read_json(CANDIDATE/'CURRENT_PROOF_DEPENDENCIES.json'))
    assert len(deps)==50 and len({x['path'] for x in deps})==50
    family=[]
    for mf in ['convex_family/MANIFEST.json','potential_family/FIRST_PARTY_MANIFEST.json','primary_scope_family/FIRST_PARTY_MANIFEST.json']:
        root=(AUDIT/mf).parent; m=read_json(AUDIT/mf)
        listed=check_manifest(root,m)
        roster=sorted(str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and not any(z in p.relative_to(root).parts for z in ['tmp','.tmp','__pycache__']) and p.name!=Path(mf).name and p.suffix!='.pyc')
        assert roster==sorted(x['path'] for x in listed)
        family.append({'manifest':mf,'sha256':sha((AUDIT/mf).read_bytes()),'members':len(listed)})
    assert sum(x['members'] for x in family)==43
    snap=read_json(AUDIT/'snapshot_manifest.json'); originals=[]
    for item in snap['files']:
        b=(AUDIT/'source_snapshot'/item['path']).read_bytes()
        assert b==command('git','show',HEAD+':'+PREFIX+item['path'])
        assert len(b)==item['bytes'] and sha(b)==item['sha256']
        blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        assert blob==item['git_blob_sha1']
        originals.append({'path':item['path'],'sha256':sha(b),'git_blob_sha1':blob})
    assert len(originals)==17
    diff=command('git','diff','--no-ext-diff','--name-only',BASE,HEAD).decode().splitlines()
    assert diff==snap['changed_paths'] and len(diff)==18
    rows={}
    for label,ref in [('base',BASE),('original_head',HEAD)]:
        rows[label]=next(x for x in command('git','show',ref+':unsolved_math_prioritization/QUEUE.md').decode().splitlines() if '| 7000019 / AMR-069-0019 |' in x)
    assert '| queued | 0/5 |' in rows['base'] and '| unsolved | 2/5 |' in rows['original_head']
    rows['current_main']=next(x for x in (REPO/'unsolved_math_prioritization/QUEUE.md').read_text().splitlines() if '| 7000019 / AMR-069-0019 |' in x)
    archives={}
    for n in ['PROOF.md','README.md','SOURCE_AUDIT.md','attempt.json','pr_body.md']:
        assert (CANDIDATE/('ORIGINAL_'+n)).read_bytes()==(AUDIT/'source_snapshot'/n).read_bytes()
        archives[n]=sha((CANDIDATE/('ORIGINAL_'+n)).read_bytes())
    original_math=(AUDIT/'source_snapshot/PROOF.md').read_bytes().split(b'## 2. Averaging a centered strip',1)[1]
    candidate_math=(CANDIDATE/'PROOF.md').read_bytes().split(b'## 2. Averaging a centered strip',1)[1]
    assert candidate_math==original_math
    for item in originals:
        if item['path'] not in archives:
            assert (CANDIDATE/item['path']).read_bytes()==(AUDIT/'source_snapshot'/item['path']).read_bytes()
    history=[]
    for commit in command('git','log','--format=%H',HEAD,'--',PREFIX+'PROOF.md').decode().splitlines():
        history.append({'commit':commit,'proof_sha256':sha(command('git','show',commit+':'+PREFIX+'PROOF.md'))})
    assert all(x['proof_sha256']!='acd8d7f8d98d7500cb2c09cb724bdceb187993634b76579aff4febf7715015d7' for x in history)

    cache=REPO/'unsolved_math_prioritization/cache'
    manifest=read_json(REPO/'unsolved_math_prioritization/manifest.json'); raw=[]
    for name,item in manifest['files'].items():
        b=(cache/name).read_bytes(); assert len(b)==item['bytes'] and sha(b)==item['sha256']
        raw.append({'file':name,'bytes':len(b),'sha256':sha(b)})
    problems=read_json(cache/'problems.json'); matches=[x for x in problems if str(x['id'])=='7000019']
    assert len(matches)==1 and matches[0]==read_json(CANDIDATE/'source_record.json')
    code=matches[0]['problem_number']; multiplicity=sum(x['problem_number']==code for x in problems)
    assert code=='AMR-069-0019' and multiplicity==1
    reports=read_json(cache/'research_results.json'); assert reports[code]==read_json(CANDIDATE/'prior_report.json')
    db=sqlite3.connect((cache/'catalog.sqlite').as_uri()+'?mode=ro&immutable=1',uri=True)
    row=db.execute('select payload,report from records where key=?',('7000019',)).fetchone()
    revision=list(db.execute('select revision from metadata'));db.close()
    assert json.loads(row[0])==matches[0] and json.loads(row[1])==reports[code]
    assert revision==[(manifest['revision'],)]
    upstream_url='https://huggingface.co/api/datasets/ulamai/UnsolvedMath/tree/'+manifest['revision']+'?recursive=true&expand=false'
    upstream_bytes=urllib.request.urlopen(upstream_url,timeout=30).read()
    (HERE/'foreign/upstream_tree.json').write_bytes(upstream_bytes)
    upstream=json.loads(upstream_bytes)
    for item in raw:
        u=next(x for x in upstream if x['path']==item['file'])
        assert u['size']==item['bytes'] and u['lfs']['oid']==item['sha256']
    administrative={}
    for n in ['state.json','assessments.json']:
        administrative[n]=read_json(REPO/'unsolved_math_prioritization'/n).get('7000019')
    for n in ['history.jsonl','assessment_history.jsonl','update_history.jsonl']:
        administrative[n]=[json.loads(x) for x in (REPO/'unsolved_math_prioritization'/n).read_text().splitlines() if x.strip() and str(json.loads(x).get('id'))=='7000019']
    administrative['catalog_target']=next(x for x in read_json(REPO/'unsolved_math_prioritization/catalog.json') if x['id']=='7000019')
    related=(REPO/'unsolved_math_prioritization/review_v2/related_target_groups.json').read_text()
    administrative['related_groups_exact_ID_present']='7000019' in related
    administrative['related_groups_exact_code_present']=code in related

    replays=HERE/'replays'; replays.mkdir(exist_ok=True)
    isolated=replays/'original'; shutil.copytree(AUDIT/'source_snapshot',isolated,dirs_exist_ok=True)
    legacy=[]
    for name,expected in [('verify.py','verification.json'),('review/submitted_verify.py','review/verification.json'),('review/independent_checks.py','review/independent_results.json')]:
        script=isolated/name;b=script.read_bytes()
        r=subprocess.run([PYTHON,str(script)],cwd=script.parent,capture_output=True,env=ENV,check=True)
        output=script.with_name('independent_results.json').read_bytes() if name.endswith('independent_checks.py') else r.stdout
        assert output==(AUDIT/'source_snapshot'/expected).read_bytes() and script.read_bytes()==b
        d=json.loads(output); legacy.append({'script':name,'script_sha256':sha(b),'output_sha256':sha(output),'assertions':d.get('total_assertions',d.get('passed')),'byte_exact':True})
    new_runs=[]
    for family_name,script_name,receipt_name,exclude in [('convex_family','geometric_controls.py','GEOMETRIC_RECEIPT.json',[]),('potential_family','new_controls.py','new_control_receipts.json',['utc']),('primary_scope_family','controls.py','CONTROLS_RESULT.json',[])]:
        root=replays/family_name; root.mkdir(exist_ok=True)
        for p in (AUDIT/family_name).iterdir():
            if p.is_file(): shutil.copyfile(p,root/p.name)
        if family_name=='primary_scope_family':
            shutil.copytree(AUDIT/'source_snapshot',root/'.tmp/original_snapshot'/PREFIX,dirs_exist_ok=True)
            sources=root/'.tmp/sources';sources.mkdir(parents=True,exist_ok=True)
            for src,dest in [('ghomi_2004.pdf','ghomi2004.pdf'),('kim_kim_2012.pdf','kimkim2012.pdf')]:
                shutil.copyfile(HERE/'foreign'/src,sources/dest)
                subprocess.run(['pdftotext','-layout',str(sources/dest),str((sources/dest).with_suffix('.txt'))],check=True)
        b=(root/script_name).read_bytes()
        subprocess.run([PYTHON,str(root/script_name)],cwd=REPO,env=ENV,capture_output=True,check=True)
        d=read_json(root/receipt_name);old=read_json(AUDIT/family_name/receipt_name)
        for field in exclude:d.pop(field);old.pop(field)
        assert d==old and (root/script_name).read_bytes()==b
        new_runs.append({'family':family_name,'script_sha256':sha(b),'mathematical_fields_equal':True,'excluded_fields':exclude,'output_sha256':sha((root/receipt_name).read_bytes())})
    mutants=[]
    for name,text in [('deleted_proof',None),('empty_proof',''),('invented_solution','Every convex body is a sphere. QED.')]:
        root=replays/'own_proof_mutants'/name;root.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(AUDIT/'source_snapshot/verify.py',root/'verify.py')
        if text is not None:(root/'PROOF.md').write_text(text)
        r=subprocess.run([PYTHON,str(root/'verify.py')],cwd=root,env=ENV,capture_output=True,check=True)
        assert r.stdout==(AUDIT/'source_snapshot/verification.json').read_bytes()
        mutants.append({'name':name,'old_verifier_passes':1056,'byte_exact_output':True,'scope':'Proof blindness, not an analytic counterexample.'})
    # Final exact-content checks detect mutations during replay.
    assert candidate==check_manifest(CANDIDATE,read_json(CANDIDATE/'MANIFEST.json'))
    assert deps==check_manifest(AUDIT,read_json(CANDIDATE/'CURRENT_PROOF_DEPENDENCIES.json'))
    assert command('git','check-ignore',str(HERE/'foreign/reichel_1996.pdf')).strip()
    assert command('git','check-ignore',str(replays/'original/verify.py')).strip()
    result={'utc':datetime.now(timezone.utc).isoformat(),'original_head':HEAD,'candidate_manifest_sha256':sha((CANDIDATE/'MANIFEST.json').read_bytes()),'candidate_files':candidate,'proof_dependencies':deps,'family_manifests':family,'original17':originals,'changed18':diff,'queue_rows':rows,'archives_exact':archives,'sections2onward_bytes_equal':True,'sections2onward_sha256':sha(original_math),'proof_history':history,'old_preheader_recovered':False,'raw_datasets':raw,'upstream_tree_sha256':sha(upstream_bytes),'unique_prior_join_code':code,'code_multiplicity':multiplicity,'readonly_SQLite_exact':True,'administrative_snapshot':administrative,'original_replays':legacy,'family_replays':new_runs,'own_proof_mutants':mutants,'closed_inputs_unchanged_at_end':True,'new_substantive_attempts':0,'future_candidate_or_canonical_bytes_certified':False}
    output=HERE/'PACKET_RECEIPT.json' if '--record' in sys.argv else HERE/'tmp/PACKET_LAST_REPLAY.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'candidate_files':len(candidate),'dependencies':len(deps),'original17_exact':True,'changed18_exact':True,'family_members':43,'original_replays':[x['assertions'] for x in legacy],'family_replays_equal':True,'source_prior_SQLite_upstream_exact':True,'closed_inputs_unchanged':True}))

if __name__=='__main__':main()
