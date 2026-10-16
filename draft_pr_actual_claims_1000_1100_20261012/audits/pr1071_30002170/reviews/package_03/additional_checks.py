"""Additional actual entry-point, metadata semantic, and Git-body checks."""
import sys
sys.dont_write_bytecode=True
import json,os,subprocess,hashlib,shutil,datetime
from pathlib import Path
from review_checks import run,require,sha,pin,save,WORK,KIT,AUDIT,HERE
clean=WORK/'CleanPackage';archive=KIT/'PR1071_preprint_v1_0_support.zip'
childnames=['normal/original_finite_checks.py','normal/FINITE_CHECKS.json','normal/stdout.txt','normal/stderr.txt','optimized/original_finite_checks.py','optimized/FINITE_CHECKS.json','optimized/stdout.txt','optimized/stderr.txt','CHECK_RECEIPT.json','paper.tex','paper.pdf','paper.log','compile.stdout.txt','compile.stderr.txt']
reuse=WORK/'reused-with-child-aliases';reuse.mkdir()
canary=WORK/'child-canary';canary.write_text('never replace')
for i,name in enumerate(childnames):
    p=reuse/name;p.parent.mkdir(parents=True,exist_ok=True)
    if i%3==0:p.symlink_to(canary)
    elif i%3==1:os.link(canary,p)
    else:p.symlink_to(WORK/'absent-child-target')
before=sha(canary)
compiler=WORK/'compiler-sentinel.py';sentinel=WORK/'COMPILER_WAS_RUN'
records=[]
for flags,label in [([], 'normal'),(['-O'],'optimized')]:
    for script in ['build_archive.py','check.py','build_pdf.py']:
        args=[sys.executable,*flags,clean/'scripts'/script,'--out',reuse]
        if script=='build_pdf.py':args+=['--tectonic',compiler]
        r=run('child-file-aliases-reused-output-'+script+'-'+label,args,False)
        require(not sentinel.exists() and sha(canary)==before,'Child alias canary changed')
    run('default-temporary-checker-'+label,[sys.executable,*flags,clean/'scripts/check.py'])
    # Coherent outer manifest mutations must still trip semantic status guards.
    status=clean/'CASE_ALIAS_REPAIR_STATUS.json';statusbytes=status.read_bytes()
    mp=clean/'PACKAGE_MANIFEST.json';mb=mp.read_bytes()
    for key,new in [('publication_ready',True),('issues_resolved',True),('published',True),('new_complete_whole_review_completed',True),('new_complete_whole_review_required',2),('services_held_after_pr',1071),('root_repair_adoption_required',False),('root_terminal_adoption_required',False),('fresh_whole_package_reviews_completed',3),('minimum_fresh_reviews_required',1)]:
        obj=json.loads(statusbytes);obj[key]=new;status.write_text(json.dumps(obj,indent=2)+'\n')
        manifest=json.loads(mb)
        row=next(x for x in manifest['members'] if x['path']=='CASE_ALIAS_REPAIR_STATUS.json');row['bytes']=status.stat().st_size;row['sha256']=sha(status)
        mp.write_text(json.dumps(manifest,indent=2)+'\n')
        run('coherent-current-status-fault-'+key+'-'+label,[sys.executable,*flags,clean/'scripts/verify_package.py'],False)
        status.write_bytes(statusbytes);mp.write_bytes(mb)
        records.append({'mode':label,'fault':key,'rejected_with_coherent_manifest':True})
    # Malformed bootstrap symlink must fail before opening an output ZIP.
    malformed=WORK/'not-json';mp.unlink();mp.symlink_to(malformed)
    target=WORK/('bootstrap-no-archive-'+label+'.zip')
    run('bootstrap-link-before-archive-write-'+label,[sys.executable,*flags,clean/'scripts/build_archive.py','--out',target],False,contains='Symlink member/ancestor')
    require(not target.exists(),'Bootstrap failure wrote archive')
    mp.unlink();mp.write_bytes(mb)
    run('native-local-check-'+label,[sys.executable,*flags,'-B','/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py','check',AUDIT/'publication/zenodo-deposit.json'])
run('optimized-actual-pdf-compile',[sys.executable,'-O',clean/'scripts/build_pdf.py','--out',WORK/'pdf-rebuild-optimized'])
require((WORK/'pdf-rebuild-optimized/paper.pdf').read_bytes()==(KIT/'paper.pdf').read_bytes(),'optimized compile differs')
run('post-extra-controls-clean-verification',[sys.executable,clean/'scripts/verify_package.py'])
# Read-only exact Git object retrieval; no index, branch, commit, or remote action.
head='fc37aa5169a0fe6adae0a254c9ee6c1531a2911f';repo=Path('/Users/alec/Documents/Math');gitrows=[]
for row in json.loads((AUDIT/'SUBMITTED_PINS.json').read_text())['files']:
    args=['git','show',head+':'+row['repository_path']]
    r=subprocess.run(args,cwd=repo,capture_output=True)
    require(r.returncode==0,'Actual Git body unavailable '+row['repository_path'])
    body=(AUDIT/row['snapshot_path']).read_bytes()
    require(r.stdout==body and len(body)==row['bytes'] and hashlib.sha256(body).hexdigest()==row['sha256'],'Actual original Git bytes differ')
    gitrows.append({**row,'actual_git_object_command':args,'returncode':r.returncode,'same_bytes':True})
save('ACTUAL_GIT_NINE.json',{'head':head,'read_only':True,'rows':gitrows})
# review_checks.run has a separate module ledger for this phase, retained here;
# restore the first phase ledger, then combine to avoid losing actual evidence.
from review_checks import RECEIPTS
save('ADDITIONAL_COMMAND_RECEIPTS.json',RECEIPTS)
save('ADDITIONAL_CHECKS.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command_count':len(RECEIPTS),'child_aliases':childnames,'child_canary_unchanged':True,'semantic_status_faults':records,'optimized_pdf_byte_equal':True,'actual_git_nine':True,'clean_members_after_controls':[pin(clean/x['path']) for x in json.loads((clean/'PACKAGE_MANIFEST.json').read_text())['members']]})
print(json.dumps({'additional_commands':len(RECEIPTS),'status':'PASS','actual_git_nine':True}))
