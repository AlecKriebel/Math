#!/usr/bin/env python3
"""Read-only package review with one disposable extraction and local-only checks."""
import sys
sys.dont_write_bytecode = True
import datetime
import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import zipfile

REVIEW = Path(__file__).resolve().parent
AUDIT = REVIEW.parent.parent
PREPRINT = AUDIT/'preprint_v1_0'
REPO = AUDIT.parents[2]
commands = []


def need(q, text):
    if not q:
        raise ValueError(text)


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pin(path):
    b = Path(path).read_bytes()
    return {'bytes':len(b),'sha256':sha(b)}


def load(path):
    return json.loads(Path(path).read_text())


def run(argv, cwd, success=True):
    r = subprocess.run(list(map(str,argv)),cwd=cwd,capture_output=True)
    commands.append({'argv':list(map(str,argv)),'cwd':str(cwd),'exit_code':r.returncode,
                     'expected_success':success,'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr)})
    need((r.returncode == 0) == success, 'unexpected command result: '+repr(argv)+' '+r.stderr.decode(errors='replace')[:1500])
    return r.stdout


def main():
    # All eight actual Git object bodies are compared, independent of working checkout.
    original = load(AUDIT/'SUBMITTED_PINS.json')
    git_rows = []
    for row in original['files']:
        b = run(['git','cat-file','blob',original['head_oid']+':'+row['repository_path']],REPO)
        need(b == (AUDIT/row['snapshot_path']).read_bytes(), 'actual Git body mismatch')
        need(sha(b) == row['sha256'] and len(b) == row['bytes'], 'submitted pin mismatch')
        git_rows.append({'path':row['repository_path'],'bytes':len(b),'sha256':sha(b)})
    # Independently verify every preparation input/output and all per-file custody decisions.
    for row in load(PREPRINT/'INPUT_PINS.json')['entries']:
        need(pin(AUDIT/row['path']) == {'bytes':row['bytes'],'sha256':row['sha256']},'preparation input changed')
    output_rows=load(PREPRINT/'OUTPUT_PINS.json')['entries']
    for row in output_rows:
        need(pin(PREPRINT/row['path']) == {'bytes':row['bytes'],'sha256':row['sha256']},'preparation output mismatch '+row['path'])
    copies=exclusions=0
    custody=load(PREPRINT/'kit/provenance/CUSTODY.json')['entries']
    captured={r['path']:r for r in load(PREPRINT/'kit/provenance/INPUT_PINS.json')['entries']}
    need(len(custody)==len(captured)==165,'custody size')
    need({r['original_path'] for r in custody}==set(captured),'custody partition')
    for r in custody:
        before=captured[r['original_path']]
        need(r['bytes']==before['bytes'] and r['sha256']==before['sha256'],'custody original pin')
        if r['decision']=='EXACT_AUTHORED_COPY':
            need((PREPRINT/'kit'/r['copy_path']).read_bytes()==(AUDIT/r['original_path']).read_bytes(),'copy altered')
            copies+=1
        else:
            need(r['decision']=='EXCLUDED' and r['reason'],'exclusion missing reason');exclusions+=1
    metadata=load(PREPRINT/'kit/metadata.json')
    need(load(PREPRINT/'.zenodo.json')==metadata,'bare metadata')
    need(load(PREPRINT/'zenodo-metadata.json')==load(PREPRINT/'kit/zenodo-metadata.json')=={'metadata':metadata},'wrapper metadata')
    native=load(PREPRINT/'zenodo-deposit.json')
    need(native=={'metadata':metadata,'files':[{'path':n,'name':n} for n in ['paper.pdf','pr1097_support_v1_0.zip']]},'native manifest')
    binding=load(PREPRINT/'DEPOSIT_BINDING.json')
    need(binding['metadata']==metadata and binding['kit_manifest_sha256']==pin(PREPRINT/'kit/MANIFEST.json')['sha256'],'binding')
    for r in binding['files']:
        need(pin(PREPRINT/r['name'])=={'bytes':r['bytes'],'sha256':r['sha256']},'asset binding')
    # Independent CLOSED deterministic stored ZIP reconstruction, not builder import.
    source_zip=(PREPRINT/'pr1097_support_v1_0.zip').read_bytes()
    expected=sorted(p.relative_to(PREPRINT/'kit').as_posix() for p in (PREPRINT/'kit').rglob('*') if p.is_file())
    with zipfile.ZipFile(io.BytesIO(source_zip)) as z:
        need(z.namelist()==expected and z.comment==b'' and z.testzip() is None,'ZIP inventory/CRC')
        for info in z.infolist():
            need(z.read(info.filename)==(PREPRINT/'kit'/info.filename).read_bytes(),'ZIP payload mismatch')
            need(info.date_time==(1980,1,1,0,0,0) and info.compress_type==zipfile.ZIP_STORED and
                 info.create_system==3 and info.external_attr==0o100644<<16 and not info.extra and not info.comment,'ZIP header')
    out=io.BytesIO()
    with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_STORED) as z:
        for name in expected:
            i=zipfile.ZipInfo(name,(1980,1,1,0,0,0));i.create_system=3;i.external_attr=0o100644<<16
            z.writestr(i,(PREPRINT/'kit'/name).read_bytes())
    need(out.getvalue()==source_zip,'closed ZIP byte equality')
    scratch=Path(tempfile.mkdtemp(prefix='review1097-package01-',dir='/private/tmp'))
    deletion=[]
    try:
        clean=scratch/'clean';clean.mkdir()
        with zipfile.ZipFile(io.BytesIO(source_zip)) as z:z.extractall(clean)
        clean_before={p.relative_to(clean).as_posix():pin(p) for p in clean.rglob('*') if p.is_file()}
        results=[];pdfs=[]
        # Filesystem is tested for case folding before assuming path aliases exist.
        probe=scratch/'CaseProbe';probe.mkdir()
        case_sensitive=not (scratch/'caseprobe').exists()
        for tag,flags in [('normal',['-B']),('optimized',['-O','-B'])]:
            base=[sys.executable]+flags
            optional=json.loads(run(base+['scripts/verify.py'],clean))
            need(optional['binding']['state']=='ABSENT_OPTIONAL','optional absent binding state')
            check=json.loads(run(base+['scripts/run_checks.py'],clean))
            need(check==load(clean/'EXPECTED_RESULTS.json'),'complete checker JSON mismatch');results.append(check)
            run(base+['scripts/run_checks.py','--inject-failure'],clean,False)
            rebuilt=scratch/(tag+'.zip')
            run(base+['scripts/build_support.py','--out',rebuilt],clean)
            need(rebuilt.read_bytes()==source_zip,'clean ZIP differs')
            pdf_dir=scratch/('pdf-'+tag)
            compile_result=json.loads(run(base+['scripts/rebuild_pdf.py','--out-dir',pdf_dir],clean))
            need(compile_result['matches_distributed_pdf'] and (pdf_dir/'paper.pdf').read_bytes()==(PREPRINT/'paper.pdf').read_bytes(),'actual compiled PDF differs')
            pdfs.append(pin(pdf_dir/'paper.pdf'))
            run(base+['scripts/verify.py','--require-binding'],clean,False)
            run(base+['scripts/verify.py','--binding',scratch/'absent.json'],clean,False)
            run(base+['scripts/verify.py','--binding',PREPRINT/'DEPOSIT_BINDING.json','--require-binding'],clean)
            # Existing regular/hardlinked/symlink leaves, symlink ancestors, protected descendants, traversal and missing parents.
            targets=[AUDIT/'submitted/MATHEMATICAL_REPORT.md',PREPRINT/'paper.pdf',PREPRINT/'zenodo-deposit.json',PREPRINT/'DEPOSIT_BINDING.json',clean/'paper.tex']
            for j,target in enumerate(targets):
                dest=scratch/(tag+'-hardlink-'+str(j));os.link(target,dest);before=pin(target)
                run(base+['scripts/build_support.py','--out',dest],clean,False)
                need(pin(target)==before,'hardlink target changed')
            link=scratch/(tag+'-leaflink');link.symlink_to(PREPRINT/'paper.pdf')
            ancestor=scratch/(tag+'-ancestor');ancestor.symlink_to(scratch,target_is_directory=True)
            for dest in [link,ancestor/'new.zip',clean/'new.zip',AUDIT/'new-review-output.zip',scratch/'..'/'bad.zip',scratch/'missing-parent'/'out.zip']:
                run(base+['scripts/build_support.py','--out',dest],clean,False)
            for dest in [link,ancestor/'new-pdf',clean/'new-pdf',AUDIT/'new-review-pdf',scratch/'..'/'bad-pdf',scratch/'missing-parent'/'new-pdf']:
                run(base+['scripts/rebuild_pdf.py','--out-dir',dest],clean,False)
            occupied=scratch/(tag+'-occupied-pdf');occupied.mkdir()
            for name in ['paper.tex','paper.pdf','paper.log','compile.stdout.txt','compile.stderr.txt']:
                os.link(PREPRINT/'paper.pdf',occupied/name)
            run(base+['scripts/rebuild_pdf.py','--out-dir',occupied],clean,False)
            need(all(pin(occupied/name)==pin(PREPRINT/'paper.pdf') for name in ['paper.tex','paper.pdf','paper.log','compile.stdout.txt','compile.stderr.txt']),'compiler child hardlink changed')
            # A regular bootstrap manifest must be checked before the parser sees its content.
            manifest=clean/'MANIFEST.json';saved=manifest.read_bytes();backup=scratch/(tag+'-manifest.json');backup.write_bytes(saved)
            manifest.unlink();manifest.symlink_to(backup)
            try:
                for script,extra in [('verify.py',[]),('build_support.py',['--out',scratch/(tag+'-bootstrap.zip')]),('rebuild_pdf.py',['--out-dir',scratch/(tag+'-bootstrap-pdf')])]:
                    run(base+['scripts/'+script]+extra,clean,False)
            finally:
                manifest.unlink();manifest.write_bytes(saved)
            # Present optional bindings are not silently ignored; explicit broken symlinks are not 'absent'.
            for bind in [{'bad':'binding'},dict(binding,metadata=dict(metadata,title='WRONG TITLE'))]:
                sibling=scratch/'DEPOSIT_BINDING.json';sibling.write_text(json.dumps(bind))
                run(base+['scripts/verify.py'],clean,False);sibling.unlink()
            sibling=scratch/'DEPOSIT_BINDING.json';sibling.symlink_to(scratch/'missing-bind-target')
            run(base+['scripts/verify.py'],clean,False);sibling.unlink()
            for script in ['verify.py','run_checks.py']:
                run(base+['scripts/'+script,'--output',scratch/(tag+'-unsupported.json')],clean,False)
        need(results[0]==results[1] and pdfs[0]==pdfs[1],'normal/optimized mismatch')
        need({p.relative_to(clean).as_posix():pin(p) for p in clean.rglob('*') if p.is_file()}==clean_before,'clean extraction changed')
        # Read pixels generated from the CURRENT canonical PDF, and bind previously actually-viewed images to them.
        pixels=[]
        for n in range(1,7):
            actual=(AUDIT/'root_reproduction'/('paper_page-'+str(n)+'.png')).read_bytes()
            # The actual 966x1250 root images use a1250-pixel longest-side bound.
            rendered=run(['pdftoppm','-f',n,'-l',n,'-scale-to',1250,'-png','-singlefile',PREPRINT/'paper.pdf'],scratch)
            need(rendered==actual,'actually-viewed PNG differs from current canonical PDF')
            pixels.append({'page_one_based':n,'sha256':sha(actual),'bytes':len(actual),'actually_viewed_by_this_reviewer':True,'independently_rendered_current_pdf_identical':True})
        local=json.loads(run([sys.executable,'-B',REPO/'zenodo_deposit_tool/zenodo.py','check',PREPRINT/'zenodo-deposit.json'],REPO))
        result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS',
                'actual_git_bodies':git_rows,'preparation_outputs_rehashed':len(output_rows),'preparation_inputs_rehashed':165,
                'custody_exact_copies':copies,'individual_exclusions':exclusions,'closed_zip_members':len(expected),
                'pdf':pin(PREPRINT/'paper.pdf'),'zip':pin(PREPRINT/'pr1097_support_v1_0.zip'),
                'ordinary_optimized_complete_JSON_equal_expected':True,'actual_compiler_PDF_byte_identity':pdfs,
                'canonical_pdf_actual_page_views':pixels,'native_local_check':local,'case_sensitive_filesystem':case_sensitive,
                'command_count':len(commands),'expected_nonzero_rejections':sum(not r['expected_success'] for r in commands),
                'candidate_or_original_modified':False,'external_service_actions':False}
        (REVIEW/'PACKAGE_REPRODUCTION.json').write_text(json.dumps(result,indent=2)+'\n')
    finally:
        for p in sorted(scratch.rglob('*')):
            if p.is_file() and not p.is_symlink():deletion.append({'path':str(p.relative_to(scratch)),**pin(p)})
        (REVIEW/'COMMAND_RECEIPTS.json').write_text(json.dumps(commands,indent=2)+'\n')
        (REVIEW/'SCRATCH_CLEANUP.json').write_text(json.dumps({'scratch':str(scratch),'removed_only_own_scratch':True,'files':deletion},indent=2)+'\n')
        shutil.rmtree(scratch)


if __name__=='__main__':
    main()
