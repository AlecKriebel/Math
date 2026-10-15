"""Preparation-only actual-process harness; all mutations are disposable.
Run with an output outside the kit. This file is not in the support ZIP.
"""
from pathlib import Path
import sys,os,json,hashlib,subprocess,tempfile,zipfile,shutil,datetime,argparse
KIT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(KIT))
from kit_common import safe_output,sha,require
PYTHON=sys.executable
records=[]
def run(cwd,argv,label,expected=0,env=None):
    before=datetime.datetime.now(datetime.timezone.utc).isoformat()
    p=subprocess.run(argv,cwd=cwd,capture_output=True,text=True,env=env)
    row={'label':label,'utc':before,'cwd':str(cwd),'argv':argv,'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
    records.append(row)
    require((p.returncode==0)==(expected==0),label+' unexpected exit: '+p.stdout+p.stderr)
    return p
def pin_tree(base):
    return {str(p.relative_to(base)):{'bytes':len(p.read_bytes()),'sha256':sha(p.read_bytes())} for p in sorted(base.rglob('*')) if p.is_file()}
def repin(root):
    p=root/'SUPPORT_MANIFEST.json';obj=json.loads(p.read_text())
    for r in obj['files']:
        d=(root/r['path']).read_bytes();r['bytes']=len(d);r['sha256']=sha(d)
    p.write_text(json.dumps(obj,indent=2)+'\n')
def edit(root,name,fn):
    p=root/name;obj=json.loads(p.read_text());fn(obj);p.write_text(json.dumps(obj,indent=2)+'\n');repin(root)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',required=True);args=parser.parse_args()
    output=safe_output(args.output)
    baseline=pin_tree(KIT)
    archive=(KIT/'pr1085_support_v1_0.zip').read_bytes()
    deposit=(KIT/'zenodo-deposit.json').read_bytes()
    binding=(KIT/'UPLOAD_BINDINGS.json').read_bytes()
    with tempfile.TemporaryDirectory(prefix='pr1085-process-',dir='/private/tmp') as temp:
        scratch=Path(temp);root=scratch/'kit'
        def fresh(full=False):
            if root.exists():shutil.rmtree(root)
            root.mkdir()
            with zipfile.ZipFile(KIT/'pr1085_support_v1_0.zip') as z:z.extractall(root)
            if full:
                (root/'pr1085_support_v1_0.zip').write_bytes(archive)
                (root/'zenodo-deposit.json').write_bytes(deposit)
                (root/'UPLOAD_BINDINGS.json').write_bytes(binding)
        for mode in [[],['-O']]:
            prefix=[PYTHON,*mode,'-B'];mode_name='optimized' if mode else 'normal'
            fresh()
            for script in ['verify_package.py','check_math.py']:
                run(root,prefix+[script],mode_name+' clean '+script)
            out=scratch/('rebuilt_'+mode_name+'.zip')
            run(root,prefix+['build_archive.py','--output',str(out)],mode_name+' clean archive')
            require(out.read_bytes()==archive,'clean closed archive exact bytes '+mode_name)
            run(root,prefix+['verify_package.py'],mode_name+' clean verifier after build')
            run(root,prefix+['verify_package.py','--require-deposit'],mode_name+' absent strict descriptor rejection',1)
            for fault in ['normal_sign','lost_jacobian','preprint_theta','fourier_boundary_sign']:
                run(root,prefix+['check_math.py','--mutation',fault],mode_name+' math mutation '+fault,1)
            for key in ['publication_ready','all_actionable_issues_resolved','published','embedded_eigenvalues_excluded',
                        'all_coupling_absence_for_one_fixed_nonzero_graph','general_n_ge_4_nongraph_classification',
                        'human_peer_review','formal_proof_certificate']:
                fresh();edit(root,'STATUS.json',lambda o,k=key:o.__setitem__(k,True))
                run(root,prefix+['verify_package.py'],mode_name+' coherent stage fault '+key,1)
            for key,value in [('new_whole_package_reviews',2),('minimum_new_whole_package_reviews',0),
                              ('novelty','VERIFIED'),('audited_head','0'*40)]:
                fresh();edit(root,'STATUS.json',lambda o,k=key,v=value:o.__setitem__(k,v))
                run(root,prefix+['verify_package.py'],mode_name+' coherent scope fault '+key,1)
            fresh()
            p=root/'.zenodo.json';meta=json.loads(p.read_text());meta['notes']='Published and human refereed.'
            p.write_text(json.dumps(meta)+'\n');(root/'metadata.json').write_text(json.dumps({'metadata':meta})+'\n');repin(root)
            run(root,prefix+['verify_package.py'],mode_name+' coherent all metadata mutation',1)
            fresh();edit(root,'COPY_MAP.json',lambda o:o['files'][0].__setitem__('sha256','0'*64))
            run(root,prefix+['verify_package.py'],mode_name+' coherent historical copy map mutation',1)
            fresh()
            manifest=root/'SUPPORT_MANIFEST.json';saved=scratch/('manifest_'+mode_name+'.json');saved.write_bytes(manifest.read_bytes())
            manifest.unlink();manifest.symlink_to(saved)
            run(root,prefix+['verify_package.py'],mode_name+' self excluded manifest symlink',1)
            fresh()
            allow=root/'PAYLOAD_MEMBERS.txt';saved=scratch/('allow_'+mode_name+'.txt');saved.write_bytes(allow.read_bytes())
            allow.unlink();allow.symlink_to(saved)
            run(root,prefix+['verify_package.py'],mode_name+' bootstrap allowlist symlink',1)
            fresh();p=root/'zenodo-deposit.json';p.symlink_to(scratch/'missing')
            run(root,prefix+['verify_package.py'],mode_name+' dangling descriptor',1)
            fresh();p=root/'STATUS.json';p.write_text('{"pr":1085,"pr":1085}\n');repin(root)
            run(root,prefix+['verify_package.py'],mode_name+' duplicate JSON key',1)
            fresh(full=True)
            run(root,prefix+['verify_package.py','--require-deposit'],mode_name+' complete binding positive')
            for target,fn in [('UPLOAD_BINDINGS.json',lambda o:o['files'][0].__setitem__('bytes',True)),
                              ('UPLOAD_BINDINGS.json',lambda o:o['files'][1].__setitem__('sha256','0'*64)),
                              ('zenodo-deposit.json',lambda o:o['metadata'].__setitem__('version','2.0')),
                              ('zenodo-deposit.json',lambda o:o['files'][0].__setitem__('path','../other.pdf'))]:
                fresh(full=True);p=root/target;o=json.loads(p.read_text());fn(o);p.write_text(json.dumps(o)+'\n')
                run(root,prefix+['verify_package.py','--require-deposit'],mode_name+' external binding fault '+target+str(len(records)),1)
            fresh(full=True)
            p=root/'zenodo-deposit.json';saved=scratch/('deposit_'+mode_name+'.json');saved.write_bytes(p.read_bytes());p.unlink();p.symlink_to(saved)
            run(root,prefix+['verify_package.py','--require-deposit'],mode_name+' ordinary descriptor symlink',1)
            fresh()
            for script,name in [('verify_package.py','paper.tex'),('check_math.py','paper.pdf'),('build_archive.py','.zenodo.json')]:
                target=root/name;before=target.read_bytes()
                run(root,prefix+[script,'--output',str(target)],mode_name+' direct output alias '+script,1)
                require(target.read_bytes()==before,'direct alias untouched')
                alias=scratch/('hard_'+script+'_'+mode_name);os.link(target,alias)
                run(root,prefix+[script,'--output',str(alias)],mode_name+' hardlink output alias '+script,1)
                require(alias.read_bytes()==before and target.read_bytes()==before,'hardlink untouched')
                alias.unlink();alias.symlink_to(target)
                run(root,prefix+[script,'--output',str(alias)],mode_name+' symlink output alias '+script,1)
                require(target.read_bytes()==before,'symlink target untouched');alias.unlink()
            external=scratch/('external_'+mode_name+'.json');external.write_text('{"metadata":{},"files":[]}\n')
            before=external.read_bytes()
            run(root,prefix+['verify_package.py','--deposit',str(external),'--output',str(external)],mode_name+' supplied external descriptor output alias',1)
            require(external.read_bytes()==before,'external descriptor preserved before parse')
            fake=scratch/('fakebin_'+mode_name);fake.mkdir()
            compiler=fake/'tectonic';called=scratch/('COMPILER_CALLED_'+mode_name)
            compiler.write_text('#!/bin/sh\nprintf called > "'+str(called)+'"\nexit 97\n');compiler.chmod(0o755)
            env=dict(os.environ,PATH=str(fake)+os.pathsep+os.environ.get('PATH',''))
            run(root,prefix+['build_pdf.py','--out-dir','.'],mode_name+' canonical PDF directory alias',1,env)
            require(not called.exists(),'compiler not called for canonical alias')
            for name in ['paper.tex','paper.pdf','paper.log','COMPILE_RECEIPT.json']:
                outdir=scratch/('pdfalias_'+mode_name+'_'+name);outdir.mkdir()
                target=root/'paper.tex';before=target.read_bytes();os.link(target,outdir/name)
                run(root,prefix+['build_pdf.py','--out-dir',str(outdir)],mode_name+' PDF child hardlink '+name,1,env)
                require(not called.exists() and target.read_bytes()==before,'PDF child guard before write/compiler')
            # Actual safe compile is a documented command, not the fake compiler.
            fresh()
            outdir=scratch/('pdfsafe_'+mode_name)
            proc=run(root,prefix+['build_pdf.py','--out-dir',str(outdir)],mode_name+' safe PDF rebuild')
            require((outdir/'paper.pdf').read_bytes()==(KIT/'paper.pdf').read_bytes(),'safe PDF exact canonical bytes')
            run(root,prefix+['verify_package.py'],mode_name+' clean payload after safe compile')
        # Complete canonical kit process, with unchanged output routes.
        for mode in [[],['-O']]:
            prefix=[PYTHON,*mode,'-B'];label='canonical optimized' if mode else 'canonical normal'
            run(KIT,prefix+['verify_package.py','--require-deposit'],label+' strict binding')
            run(KIT,prefix+['check_math.py'],label+' mathematics')
        canonical_normal = next(json.loads(r['stdout']) for r in records if r['label']=='canonical normal mathematics')
        canonical_optimized = next(json.loads(r['stdout']) for r in records if r['label']=='canonical optimized mathematics')
        require(canonical_normal==canonical_optimized,'actual canonical normal/optimized finite results equal')
        clean_normal = next(json.loads(r['stdout']) for r in records if r['label']=='normal clean check_math.py')
        clean_optimized = next(json.loads(r['stdout']) for r in records if r['label']=='optimized clean check_math.py')
        require(clean_normal==clean_optimized,'actual clean normal/optimized finite results equal')
        require(pin_tree(KIT)==baseline,'all canonical preparation bytes unchanged by actual processes')
        # Independently reconstruct after the ZIP is CLOSED, without importing builder.
        import io
        names=json.loads((KIT/'SUPPORT_MANIFEST.json').read_text())['files']
        expected=sorted([r['path'] for r in names]+['SUPPORT_MANIFEST.json'])
        stream=io.BytesIO()
        with zipfile.ZipFile(stream,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for name in expected:
                info=zipfile.ZipInfo(name,(2026,10,14,0,0,0));info.create_system=3;info.external_attr=0o100644<<16;info.compress_type=zipfile.ZIP_DEFLATED
                z.writestr(info,(KIT/name).read_bytes(),compresslevel=9)
        require(stream.getvalue()==archive,'independent closed ZIP exact')
        result={'passed':True,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                'command_count':len(records),'expected_rejections':sum(r['returncode']!=0 for r in records),
                'canonical_files_unchanged':len(baseline),'independent_closed_archive_equal':True,
                'normal_and_optimized_finite_results_equal':True,'safe_PDF_rebuild_equal_both_modes':True,
                'PDF_alias_guards_precompiler':True,'commands':records}
        output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(result,indent=2)+'\n')
        print(json.dumps({k:v for k,v in result.items() if k!='commands'},indent=2))
if __name__=='__main__':main()
