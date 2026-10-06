"""Portable deterministic replay. Authenticate this file with the pinned launcher first."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
    raise SystemExit('Use python -I -S -B.')
import hashlib,json,os,pathlib,shutil,subprocess,tempfile,zipfile,runpy

def need(x,msg):
    if not x: raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
need(len(sys.argv)==4,'usage: test_publication.py ROOT MANIFEST_SHA WRAPPER_SHA')
root=pathlib.Path(sys.argv[1]).absolute();mp,wp=sys.argv[2:]
wrapper=root/'verify_publication.py'
need(root==root.resolve() and wrapper==wrapper.resolve() and sha(wrapper.read_bytes())==wp,'external wrapper pin')
cmd=[sys.executable,'-I','-S','-B',str(wrapper),str(root),mp,wp]
subprocess.run(cmd,capture_output=True,text=True,check=True)
specs=runpy.run_path(str(wrapper))['SPECS']
records=[];math_results={};frozen_replay={};auditor_harnesses={}
with tempfile.TemporaryDirectory(prefix='cm publication acceptance ') as td:
    t=pathlib.Path(td);hostile=t/'hostile working directory';hostile.mkdir();marker=t/'UNTRUSTED_EXECUTED'
    payload="__import__('pathlib').Path("+repr(str(marker))+ ").write_text('executed')\n"
    for name in ['fractions.py','hashlib.py','json.py','pathlib.py','stat.py','subprocess.py','itertools.py','sitecustomize.py','usercustomize.py']:(hostile/name).write_text(payload)
    env=dict(os.environ,PYTHONPATH=str(hostile),PYTHONSTARTUP=str(hostile/'sitecustomize.py'))
    def launch(label,args,success=True,cwd=hostile):
        p=subprocess.run(args,cwd=cwd,env=env,capture_output=True,text=True)
        need((p.returncode==0)==success,label+': '+(p.stdout+p.stderr)[-1000:]);need(not marker.exists(),'untrusted code executed')
        records.append({'name':label,'expected':'pass' if success else 'reject','passed':True})
        return p
    def call(r,mode,execute=False,manpin=mp,wrap=wp):
        return [sys.executable,'-I','-S','-B']+(['-O'] if mode else [])+[str(r/'verify_publication.py'),str(r),manpin,wrap]+(['--execute'] if execute else [])
    relocated=t/'relocated whole package with spaces';shutil.copytree(root,relocated)
    for mode in (False,True):
        tag='optimized' if mode else 'normal'
        actual=json.loads(launch(tag+' complete isolated finite replay',call(root,mode,True)).stdout)
        math_results[tag]=actual
        moved=json.loads(launch(tag+' relocated whole-package finite replay',call(relocated,mode,True)).stdout)
        need(actual==moved,'relocation results mismatch')
        cases=[('shadow module',lambda r:(r/'fractions.py').write_text(payload)),
               ('startup module',lambda r:(r/'sitecustomize.py').write_text(payload)),
               ('cache directory',lambda r:(r/'__pycache__').mkdir()),
               ('empty extra directory',lambda r:(r/'extra').mkdir()),
               ('missing file',lambda r:(r/'README.md').unlink()),
               ('changed wrapper',lambda r:(r/'verify_publication.py').write_text(payload)),
               ('changed proof',lambda r:(r/'corrected/PROOF.md').write_text('changed')),
               ('changed audit one entry',lambda r:(r/'audit_one/independent_exact.py').write_text(payload)),
               ('changed audit two entry',lambda r:(r/'audit_two/independent_check.py').write_text(payload)),
               ('changed archive',lambda r:(r/specs[0]['archive']).write_bytes(b'changed')),
               ('changed external manifest',lambda r:(r/'PUBLICATION_MANIFEST.json').write_text('{}')),
               ('member symlink',lambda r:((r/'README.md').unlink(),(r/'README.md').symlink_to(root/'README.md'))),
               ('wrapper symlink',lambda r:((r/'verify_publication.py').unlink(),(r/'verify_publication.py').symlink_to(wrapper))),
               ('directory symlink',lambda r:(shutil.rmtree(r/'author'),(r/'author').symlink_to(root/'author',target_is_directory=True)))]
        for label,change in cases:
            r=t/(tag+' '+label);shutil.copytree(root,r);change(r)
            # Never execute a changed wrapper. Its pin must be rejected by trusted original.
            args=call(r,mode)
            if label in ('changed wrapper','wrapper symlink'):args[args.index(str(r/'verify_publication.py'))]=str(wrapper)
            launch(tag+' reject '+label,args,False)
        linked=t/(tag+' root link');linked.symlink_to(root,target_is_directory=True);launch(tag+' reject root symlink',call(linked,mode),False)
        ancestor=t/(tag+' ancestor');ancestor.symlink_to(root.parent,target_is_directory=True);launch(tag+' reject ancestor symlink',call(ancestor/root.name,mode),False)
        launch(tag+' reject wrong manifest pin',call(root,mode,manpin='0'*64),False)
        launch(tag+' reject wrong wrapper pin',call(root,mode,wrap='0'*64),False)
        # With a newly supplied outer manifest pin, immutable inner input pins still reject changes.
        r=t/(tag+' rehashed inner manifest');shutil.copytree(root,r);target=r/specs[0]['manifest'];target.write_bytes(target.read_bytes()+b'\n')
        m=json.loads((r/'PUBLICATION_MANIFEST.json').read_bytes());m['files'][target.name]={'bytes':target.stat().st_size,'sha256':sha(target.read_bytes())};raw=(json.dumps(m,indent=2,sort_keys=True)+'\n').encode();(r/'PUBLICATION_MANIFEST.json').write_bytes(raw)
        launch(tag+' reject rehashed immutable inner manifest',call(r,mode,manpin=sha(raw)),False)
        for spec in specs:
            packet=root/spec['folder'];boot=root/spec['bootstrap'];manifest=root/spec['manifest']
            def pc(r=packet,m=manifest,extra=()):return [sys.executable,'-I','-S','-B']+(['-O'] if mode else [])+[str(boot),str(r),str(m)]+(['--optimized'] if mode else [])+list(extra)
            out=launch(tag+' '+spec['folder']+' frozen bootstrap clean',pc()).stdout
            frozen_replay[spec['folder']+' '+tag]=json.loads(out)
            need(json.loads(out)==actual['certificates'][spec['folder']],'frozen and operative outputs disagree')
            r=t/(tag+' '+spec['folder']+' relocated packet with spaces');shutil.copytree(packet,r);launch(tag+' '+spec['folder']+' frozen bootstrap relocation',pc(r))
            changes=[('import shadow',lambda r:(r/'fractions.py').write_text(payload)),('startup shadow',lambda r:(r/'sitecustomize.py').write_text(payload)),('cache',lambda r:(r/'__pycache__').mkdir()),('entry changed',lambda r:(r/spec['entrypoint']).write_text(payload)),('report changed',lambda r:next(x for x in r.iterdir() if x.suffix=='.md').write_text('changed')),('entry symlink',lambda r:((r/spec['entrypoint']).unlink(),(r/spec['entrypoint']).symlink_to(packet/spec['entrypoint'])))]
            for label,change in changes:
                r=t/(tag+' '+spec['folder']+' '+label);shutil.copytree(packet,r);change(r);launch(tag+' '+spec['folder']+' frozen reject '+label,pc(r),False)
            link=t/(tag+' '+spec['folder']+' symlink');link.symlink_to(packet,target_is_directory=True);launch(tag+' '+spec['folder']+' frozen reject root symlink',pc(link),False)
            r=t/(tag+' '+spec['folder']+' internal manifest');shutil.copytree(packet,r);shutil.copyfile(manifest,r/'manifest.json');launch(tag+' '+spec['folder']+' frozen reject internal manifest',pc(r,r/'manifest.json'),False)
            mf=t/(tag+' '+spec['folder']+' manifest symlink');mf.symlink_to(manifest);launch(tag+' '+spec['folder']+' frozen reject manifest symlink',pc(m=mf),False)
            mf=t/(tag+' '+spec['folder']+' changed manifest');mf.write_bytes(manifest.read_bytes()+b' ');launch(tag+' '+spec['folder']+' frozen reject manifest mutation',pc(m=mf),False)
            launch(tag+' '+spec['folder']+' frozen reject unrecognized selector',pc(extra=['--arbitrary-entrypoint']),False)
        for fname,stored in [('replay_controls.py','REPLAY_CONTROL_RESULTS.json'),('replay_corrected_controls.py','CORRECTED_REPLAY_CONTROL_RESULTS.json')]:
            args=[sys.executable,'-I','-S','-B']+(['-O'] if mode else [])+[str(root/'audit_one'/fname),str(root)]
            obj=json.loads(launch(tag+' original auditor harness '+fname,args).stdout)
            need(obj==json.loads((root/'audit_one'/stored).read_bytes()),'auditor stored result mismatch')
            auditor_harnesses[fname+' '+tag]={'test_count':obj['test_count'],'all_passed':obj['all_passed'],'stored_result_exact_match':True}
    need(math_results['normal']==math_results['optimized'],'normal and optimized results differ')
    patched=t/'actual zero fuzz reconstructed packet';shutil.copytree(root/'author',patched)
    cp=launch('actual reviewed patch applied with zero fuzz',['patch','--batch','--fuzz=0','-p1','-i',str(root/'audit_two/CONVERSE_SCOPE.patch')],cwd=patched)
    need(cp.stdout.strip()=='patching file PROOF.md','patch output had offsets, fuzz, or other changes')
    names=set(x.name for x in patched.iterdir());need(names==set(x.name for x in (root/'corrected').iterdir()),'patched inventory mismatch')
    need(all((patched/n).read_bytes()==(root/'corrected'/n).read_bytes() for n in names),'patched bytes differ')
    for mode in (False,True):
        spec=specs[1];args=[sys.executable,'-I','-S','-B']+(['-O'] if mode else [])+[str(root/spec['bootstrap']),str(patched),str(root/spec['manifest'])]+(['--optimized'] if mode else [])
        launch(('optimized' if mode else 'normal')+' actual patched directory acceptance',args)
    launch('post-test strict integrity',cmd)
result={'schema':'cm-publication-replay-v1','all_passed':True,'control_count':len(records),'controls':records,'operative_normal_optimized_identical':True,'operative_results':math_results['normal'],'frozen_bootstrap_results':frozen_replay,'auditor_23_case_harnesses':auditor_harnesses,'actual_zero_fuzz_patch_reconstruction':{'exact_five_files':True,'corrected_proof_sha256':'e6955e4c7e5379e103de79ad3e5dc427d36adab8d36409f81647cbc173495a79','normal_optimized_passed':True},'untrusted_marker_absent':True,'post_test_integrity':True,'geometric_theorems_formally_verified':False}
print(json.dumps(result,sort_keys=True,indent=2))
