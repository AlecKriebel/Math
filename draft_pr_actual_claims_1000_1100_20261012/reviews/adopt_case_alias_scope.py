from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile,os,datetime
P=Path(__file__).resolve().parents[1];R=P/'reviews/case_alias_scope_20261016'
def load(p):return json.loads(p.read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def require(v,m):
    if not v:raise RuntimeError(m)
def check(p,r):
    b=p.read_bytes();require(len(b)==r['bytes'] and sha(b)==r['sha256'],str(p))
s=load(R/'SEAL.json')
for name in ['report','output_pins','canonical_input_pins']:r=s[name];check(R/r['path'],r)
outputs=load(R/'OUTPUT_PINS.json')['files']
for r in outputs:check(R/r['path'],r)
packages=load(R/'CANONICAL_INPUT_PINS.json')['packages'];count=0
for obj in packages:
    for r in obj['files']:check(P/r['path'],r);count+=1
commands=[]
configs=[(1064,'audits/pr1064_30001073/preprint_v1_0/support.zip','build_archive.py','--output'),(1071,'audits/pr1071_30002170/NEWpreprint_v1_0/PR1071_preprint_v1_0_support.zip','scripts/build_archive.py','--out'),(1085,'audits/pr1085_20000488/preprint_v1_0/pr1085_support_v1_0.zip','build_archive.py','--output')]
for pr,arc,script,option in configs:
    original=(P/arc).read_bytes()
    with tempfile.TemporaryDirectory(prefix='root-case-'+str(pr)+'-',dir='/private/tmp') as td:
        td=Path(td);clean=td/'clean'
        with zipfile.ZipFile(P/arc) as z:z.extractall(clean)
        alias=td/'CLEAN';require(alias.exists() and os.path.samefile(clean,alias),'samefile case alias absent')
        before={str(p.relative_to(clean)):sha(p.read_bytes()) for p in clean.rglob('*') if p.is_file()}
        for optimized in [False,True]:
            prefix=['python3','-B']+(['-O'] if optimized else [])+[str(clean/script),option]
            for target,expect in [(alias/('case-'+str(optimized)+'.zip'),True),(clean/('direct-'+str(optimized)+'.zip'),False)]:
                p=subprocess.run(prefix+[str(target)],cwd=clean,capture_output=True)
                require((p.returncode==0)==expect,'case/control outcome differs: '+str(pr)+p.stderr.decode(errors='replace'))
                if expect:
                    actual=clean/target.name;require(actual.read_bytes()==original,'case alias generated archive differs');actual.unlink()
                commands.append({'pr':pr,'optimized':optimized,'argv':prefix+[str(target)],'exit_code':p.returncode,'expected_acceptance_defect':expect,'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr),'samefile_parent':True})
        require(before=={str(p.relative_to(clean)):sha(p.read_bytes()) for p in clean.rglob('*') if p.is_file()},'disposable inputs changed')
for obj in packages:
    for r in obj['files']:check(P/r['path'],r)
record={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'ROOT_ADOPT_THREE_NEW_UNPUBLISHED_SUPPORT_P3_FINDINGS_PENDING_BOUNDED_REPAIRS_AND_NEW_COMPLETE_WHOLE_REVIEWS','full_scope_REPORT_read':True,'canonical_files_independently_rehashed':count,'review_outputs_rehashed':len(outputs),'original16_receipts_restored':'Actual original command_000..015 files included in output pins and full exact restoration chronology read; no temporary masquerading artifacts accepted.','root_actual_reproduction':commands,'affected_prs':[1064,1071,1085],'no_finding_for_this_issue_only':[1033,1034,1037,1041,1047,1052],'other_active_actual_affected':[1080,1097],'unrelated_new_lexical_contract_finding':1094,'mathematical_acceptance_unchanged':True,'existing_input_overwrite_observed':False,'required_repairs':'Physical existing-output-ancestor identity checks preserving per-package intended mutable destinations and existing direct/symlink/hardlink guards; new complete full reviews required after bounded repair.','supersession':'Former1064/1071 rootready seals remain captured history; current program supporthold supersedes readiness. 1085 terminal admin is not rootcleared.','published_records_not_inspected_or_changed':True,'publication_ready_for_affected':False,'services_held_after_pr':1032,'scope_output_pins_sha256':s['output_pins']['sha256'],'scope_seal_sha256':sha((R/'SEAL.json').read_bytes())}
(P/'ROOT_CASE_ALIAS_SCOPE_REVIEW.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({'status':'PASS_ADOPT_THREE_P3','canonical_files':count,'outputs':len(outputs),'root_commands':len(commands),'affected':[1064,1071,1085]}))
