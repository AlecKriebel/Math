"""Root independently validates all family bindings and replays new controls."""
from pathlib import Path, PurePosixPath
import datetime, hashlib, json, shutil, subprocess
A=Path(__file__).resolve().parent;R=A.parents[2]
PY=R/'draft_pr_descending_audit_20261002/audits/pr378_30004322/sources_effective_review/private_runtime/bin/python'
PRIVATE=A/'tmp/root_family_controls';PRIVATE.mkdir(parents=True,exist_ok=True)
STREAMS=A/'root_family_control_streams';STREAMS.mkdir(exist_ok=True)
checks=[];families=[];replays=[]
def sha(b):return hashlib.sha256(b).hexdigest()
def ck(v,label):
    checks.append({'label':label,'pass':bool(v)});assert v,label
root_original=json.loads((A/'root_original_reproduction_receipt.json').read_bytes())
source_ids={(x['url'],x['bytes'],x['sha256']) for x in root_original['primary_sources']}
defs=[('function_theory_review',15,'independent_function_controls.py','INDEPENDENT_FUNCTION_CONTROLS.json','exact_assertions'),
      ('geometric_hypotheses_review',19,'geometric_controls.py','GEOMETRIC_CONTROLS.json','exact_assertions'),
      ('clean_final_adversary',19,'ADVERSARIAL_CONTROLS.py','ADVERSARIAL_CONTROLS_RESULT.json','assertions')]
for family,count,program,expected_name,count_key in defs:
    D=A/family;mf=json.loads((D/'PUBLIC_MANIFEST.json').read_bytes());seen=set()
    for row in mf['files']:
        rel=PurePosixPath(row['path']);ck(len(rel.parts)==1 and rel.as_posix()==row['path'] and row['path'] not in seen and row['path']!='PUBLIC_MANIFEST.json','literal owned path '+family+'/'+row['path']);seen.add(row['path'])
        f=D/rel;ck(not f.is_symlink() and f.resolve().is_relative_to(D),'owned regular file '+family+'/'+row['path'])
        raw=f.read_bytes();ck(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'immutable public binding '+family+'/'+row['path'])
    ck(len(seen)==count,'exact frozen family public count '+family)
    first=json.loads((D/'SOURCE_FIRST_SEAL.json').read_bytes());math=json.loads((D/'MATHEMATICAL_SEAL.json').read_bytes())
    ck(datetime.datetime.fromisoformat(first['sealed_utc'])<datetime.datetime.fromisoformat(math['sealed_utc'])<datetime.datetime.fromisoformat(root_original['root_math_sealed_utc']),'independent source/math chronology '+family)
    if family=='function_theory_review':
        ck(sha((D/first['file']).read_bytes())==first['sha256'],'function original source seal')
        for name,digest in math['own_files'].items():ck(sha((D/name).read_bytes())==digest,'function original math seal '+name)
        metadata=json.loads((D/'SOURCE_RETRIEVAL_RECEIPT.json').read_bytes())['sources'];metadata=[x for x in metadata if 'name' in x]
        actual_ids={(x['url'],x['bytes'],x['sha256']) for x in metadata};raw_pdfs=list((D/'private').glob('*.pdf'))
    elif family=='geometric_hypotheses_review':
        for name,digest in first['files'].items():ck(sha((D/name).read_bytes())==digest,'geometry original source seal '+name)
        for name,digest in math['files'].items():ck(sha((D/name).read_bytes())==digest,'geometry original math seal '+name)
        metadata=json.loads((D/'PRIMARY_ACCESS_RECEIPTS.json').read_bytes())['sources'];actual_ids={(x['requested_url'],x['bytes'],x['sha256']) for x in metadata};raw_pdfs=list((D/'private_sources').glob('*.pdf'))
    else:
        for name,digest in first['sha256'].items():ck(sha((D/name).read_bytes())==digest,'whole original source seal '+name)
        ck(sha((D/math['verdict_file']).read_bytes())==math['verdict_sha256'],'whole original math seal')
        metadata=json.loads((D/'SOURCE_RETRIEVAL.json').read_bytes());actual_ids={(x['url'],x['bytes'],x['sha256']) for x in metadata};raw_pdfs=list((D/'private/sources').glob('*.pdf'))
    ck(actual_ids==source_ids,'five exact original primary URL/size/hash identities '+family)
    pdfs=[{'path':f.relative_to(A).as_posix(),'bytes':f.stat().st_size,'sha256':sha(f.read_bytes())} for f in raw_pdfs]
    for url,size,digest in sorted(source_ids):ck(sum(x['bytes']==size and x['sha256']==digest for x in pdfs)==1,'independently stored source '+family+' '+url)
    private=PRIVATE/family;private.mkdir(exist_ok=True);copy=private/program;shutil.copyfile(D/program,copy)
    start=datetime.datetime.now(datetime.timezone.utc);result=subprocess.run([str(PY),str(copy)],cwd=private,capture_output=True);end=datetime.datetime.now(datetime.timezone.utc)
    for stream in ['stdout','stderr']:(STREAMS/(family+'.'+stream)).write_bytes(getattr(result,stream))
    ck(result.returncode==0 and not result.stderr,'fresh complete control replay '+family)
    actual=json.loads(result.stdout);old=json.loads((D/expected_name).read_bytes());runtime=[]
    if family=='geometric_hypotheses_review':
        stamp=actual['generated_utc'];ck(start<=datetime.datetime.fromisoformat(stamp)<=end,'actual geometric runtime timestamp')
        ck(json.loads((private/'GEOMETRIC_CONTROLS.json').read_bytes())==actual,'complete geometric disk/stdout equality')
        runtime=[{'field':'generated_utc','old':old['generated_utc'],'new':stamp,'validated_in_actual_run':True}]
        actual_cmp=dict(actual);old_cmp=dict(old);del actual_cmp['generated_utc'];del old_cmp['generated_utc']
    else:actual_cmp=actual;old_cmp=old
    ck(actual_cmp==old_cmp,'every nonruntime control output field '+family)
    replays.append({'family':family,'exit':result.returncode,'stdout_bytes':len(result.stdout),'stdout_sha256':sha(result.stdout),'stderr_bytes':len(result.stderr),'stderr_sha256':sha(result.stderr),'complete_output':actual,'validated_runtime_differences':runtime,'new_controls':actual[count_key]})
    families.append({'family':family,'manifest_sha256':sha((D/'PUBLIC_MANIFEST.json').read_bytes()),'bound_files':count,'all_bindings_pass':True,'primary_pdf_ids':5,'stored_private_pdfs':pdfs,'source_seal_sha256':sha((D/'SOURCE_FIRST_SEAL.json').read_bytes()),'math_seal_sha256':sha((D/'MATHEMATICAL_SEAL.json').read_bytes())})
ck(sum(r['new_controls'] for r in replays)==1262,'all1262 fresh distinct-family auxiliary controls')
out={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','check_count':len(checks),'checks':checks,'families':families,'original_public_bound_files':53,'new_controls_total':1262,'replays':replays,'original_artifacts_mutated':False,'program_sha256':sha(Path(__file__).read_bytes()),'supplemental_picard_source_chronology_clarification_pending':True}
(A/'root_family_control_reproduction.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['status','check_count','original_public_bound_files','new_controls_total']},indent=2))
