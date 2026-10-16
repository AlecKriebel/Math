#!/usr/bin/env python3
"""Review-02 clean extraction and fresh mutation tests, entirely disposable."""
from pathlib import Path
import datetime, hashlib, io, json, os, shutil, subprocess, sys, tempfile, zipfile

HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent.parent
KIT=AUDIT/'preprint_v1_0'
PY=sys.executable
records=[]
def h(b): return hashlib.sha256(b).hexdigest()
def demand(ok,msg):
    if not ok: raise RuntimeError(msg)
def run(argv,cwd,expect=0,label=''):
    p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True)
    row={'label':label,'argv':[str(x) for x in argv],'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    records.append(row)
    (HERE/'COMMAND_RECEIPTS.json').write_text(json.dumps(records,indent=2)+'\n')
    demand((p.returncode==0)==(expect==0),label+' unexpected exit '+str(p.returncode))
    return p
def files(root):
    return {str(p.relative_to(root)):h(p.read_bytes()) for p in root.rglob('*') if p.is_file() and not p.is_symlink()}

def main():
    scratch=HERE/'scratch';scratch.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='review02-',dir=scratch) as work:
        base=Path(work); clean=base/'clean';clean.mkdir()
        archive=(KIT/'pr1085_support_v1_0.zip').read_bytes()
        with zipfile.ZipFile(io.BytesIO(archive)) as z:
            names=z.namelist();demand(len(names)==91 and names==sorted(set(names)),'exact archive membership')
            demand(z.testzip() is None,'CRC')
            for i in z.infolist():
                demand(not Path(i.filename).is_absolute() and '..' not in Path(i.filename).parts,'safe archive name')
                demand(i.date_time==(2026,10,14,0,0,0) and i.create_system==3 and i.external_attr==0o100644<<16 and i.extra==b'' and i.comment==b'' and i.flag_bits==0 and i.compress_type==zipfile.ZIP_DEFLATED,'headers')
                demand(z.read(i.filename)==(KIT/i.filename).read_bytes(),'member equals current')
            z.extractall(clean)
        # Independently reconstruct only AFTER closing the writer.
        out=io.BytesIO()
        with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for name in names:
                info=zipfile.ZipInfo(name,(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED
                z.writestr(info,(clean/name).read_bytes(),compresslevel=9)
        demand(out.getvalue()==archive,'independent CLOSED ZIP reproduction')
        baseline=files(clean)
        for optimized in [False,True]:
            mode='optimized' if optimized else 'normal';prefix=[PY]+(['-O'] if optimized else [])+['-B']
            p=run(prefix+['verify_package.py'],clean,label=mode+' README default verification')
            demand(json.loads(p.stdout)['external_deposit_binding_verified'] is False,'absent descriptor not verified')
            p=run(prefix+['check_math.py'],clean,label=mode+' README math')
            q=base/(mode+'-archive.zip');run(prefix+['build_archive.py','--output',str(q)],clean,label=mode+' README archive rebuild')
            demand(q.read_bytes()==archive,'builder exact byte reproduction')
            run(prefix+['verify_package.py'],clean,label=mode+' README repeat verification')
            # Strict actual binding requires both external descriptors and exact canonical attachments.
            for name in ['zenodo-deposit.json','UPLOAD_BINDINGS.json','pr1085_support_v1_0.zip']:
                shutil.copyfile(KIT/name,clean/name)
            p=run(prefix+['verify_package.py','--require-deposit'],clean,label=mode+' present strict native binding')
            demand(json.loads(p.stdout)['external_deposit_binding_verified'] is True,'present binding')
            external=base/'external-descriptor.json';external.write_bytes((KIT/'zenodo-deposit.json').read_bytes())
            for name in ['zenodo-deposit.json','UPLOAD_BINDINGS.json','pr1085_support_v1_0.zip']:(clean/name).unlink()
            run(prefix+['verify_package.py','--require-deposit'],clean,1,mode+' missing required descriptor')
            for mutation in ['normal_sign','lost_jacobian','preprint_theta','fourier_boundary_sign']:
                run(prefix+['check_math.py','--mutation',mutation],clean,1,mode+' shipped semantic fault '+mutation)
            # Default self-excluded bootstrap inputs must reject symlinks before parsing.
            for name in ['SUPPORT_MANIFEST.json','PAYLOAD_MEMBERS.txt']:
                path=clean/name; original=path.read_bytes(); target=base/(name+'.target');target.write_bytes(original);path.unlink();path.symlink_to(target)
                run(prefix+['verify_package.py'],clean,1,mode+' bootstrap identical symlink '+name)
                run(prefix+['build_archive.py','--output',str(base/'bad.zip')],clean,1,mode+' builder bootstrap symlink '+name)
                path.unlink();path.write_bytes(original)
            path=clean/'SUPPORT_MANIFEST.json'; original=path.read_bytes();path.write_bytes(original.replace(b'{',b'{"schema":1,',1))
            run(prefix+['verify_package.py'],clean,1,mode+' duplicate JSON key')
            path.write_bytes(original)
            # A real protected pre-authoring source in the extracted audit layout.
            old=base/'submitted/MATHEMATICAL_REPORT.md';old.parent.mkdir(exist_ok=True);old.write_bytes((clean/'evidence/submitted/MATHEMATICAL_REPORT.md').read_bytes())
            for protected in [clean/'paper.tex',clean/'SUPPORT_MANIFEST.json',old,external]:
                before=protected.read_bytes(); alias=base/'alias';os.link(protected,alias)
                if protected==external:
                    run(prefix+['verify_package.py','--deposit',str(external),'--output',str(alias)],clean,1,mode+' external descriptor hardlink guard')
                else:
                    run(prefix+['build_archive.py','--output',str(alias)],clean,1,mode+' archive hardlink guard '+protected.name)
                    run(prefix+['check_math.py','--output',str(alias)],clean,1,mode+' checker hardlink guard '+protected.name)
                    run(prefix+['verify_package.py','--output',str(alias)],clean,1,mode+' verifier hardlink guard '+protected.name)
                demand(protected.read_bytes()==before,'prewrite hardlink preservation');alias.unlink()
            for script,flag in [('build_archive.py','--output'),('check_math.py','--output'),('verify_package.py','--output')]:
                link=base/'symbolic-output';link.symlink_to(clean/'paper.tex');before=(clean/'paper.tex').read_bytes()
                run(prefix+[script,flag,str(link)],clean,1,mode+' output symlink '+script)
                demand((clean/'paper.tex').read_bytes()==before,'symlink preservation');link.unlink()
                ancestor=base/'linked-parent';ancestor.symlink_to(base,target_is_directory=True)
                run(prefix+[script,flag,str(ancestor/'new.json')],clean,1,mode+' output ancestor symlink '+script);ancestor.unlink()
            # Guard every compiler child filename. The command must fail before finding/starting the engine.
            for name in ['paper.tex','paper.pdf','paper.log','COMPILE_RECEIPT.json']:
                outdir=base/'hostile-pdf';outdir.mkdir(exist_ok=True);target=clean/'paper.tex';before=target.read_bytes();os.link(target,outdir/name)
                run(prefix+['build_pdf.py','--out-dir',str(outdir)],clean,1,mode+' compiler protected hardlink child '+name)
                demand(target.read_bytes()==before and sorted(p.name for p in outdir.iterdir())==[name],'compiler prewrite preservation');(outdir/name).unlink();outdir.rmdir()
            outdir=base/('pdf-'+mode)
            run(prefix+['build_pdf.py','--out-dir',str(outdir)],clean,label=mode+' REAL clean Tectonic compilation')
            demand((outdir/'paper.pdf').read_bytes()==(KIT/'paper.pdf').read_bytes(),'Tectonic exact canonical PDF')
            demand(files(clean)==baseline,'entire clean kit preserved after mode')
        # New independent diagnostics and seven meaningful faults, both interpreter modes.
        independent=[]
        for opt in [False,True]:
            prefix=[PY]+(['-O'] if opt else [])+['-B',str(HERE/'check_independent_forms.py')]
            p=run(prefix,HERE,label='independent exact math '+str(opt));independent.append(json.loads(p.stdout))
            for fault in ['Fourier_trace_sign','mass_exponent','normal_sign','area_lost','old_theta','Hardy_m2','flat_sign']:
                run(prefix+['--fault',fault],HERE,1,'independent semantic fault '+fault+' optimized='+str(opt))
        demand(independent[0]==independent[1],'new independent full JSON normal/O equality')
        (HERE/'NEW_MATH_RESULT.json').write_text(json.dumps(independent[0],indent=2,sort_keys=True)+'\n')
        result={'passed':True,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'commands':len(records),'expected_failures':sum(x['exit']!=0 for x in records),'zip_members':len(names),'zip_bytes':len(archive),'zip_sha256':h(archive),'independent_closed_zip_equal':True,'clean_kit_preserved':True,'normal_optimized_exact_math_equal':True,'real_pdf_rebuilds':2,'exact_current_pdf_equal':True,'own_disposable_scratch_removed_on_exit':True}
        (HERE/'REPRODUCTION_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps(result,indent=2))
if __name__=='__main__':main()
