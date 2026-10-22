#!/usr/bin/env python3
"""Engineering tests on deleted synthetic document fixtures; no publication assembly.
Optional full-input replay uses verified read-only hardlinks, never corpus copies.
"""
import argparse, hashlib, io, json, os, runpy, stat, subprocess, sys, tempfile, zipfile
from datetime import datetime, timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
TOOLS=AUDIT/'preprint'
def sha(raw):return hashlib.sha256(raw).hexdigest()
def require(ok,why):
    if not ok:raise ValueError(why)
def encoded(obj):return (json.dumps(obj,indent=2,sort_keys=True)+'\n').encode()
def index_for(blobs,outer=False):
    return encoded({'schema':'city-ode-current-publication-v1' if outer else 'city-ode-verification-v1','problem_id':'9700026',
                    'files':[{'path':name,'bytes':len(raw),'sha256':sha(raw)} for name,raw in sorted(blobs.items())]})
def materialize(root,blobs):
    root.mkdir()
    for name,raw in blobs.items():
        p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw);p.chmod(0o644)
def process(script,args,optimized=False,mask=-1):
    p=subprocess.run([sys.executable,'-I','-S','-B',*(['-O'] if optimized else []),str(script),*map(str,args)],cwd=HERE,capture_output=True,timeout=800,umask=mask)
    return {'returncode':p.returncode,'stderr':p.stderr.decode(),'stdout_bytes':len(p.stdout),'stdout_sha256':sha(p.stdout),'result':json.loads(p.stdout)}
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--provenance',action='store_true');args=ap.parse_args()
    v=runpy.run_path(str(TOOLS/'verify_package.py'),run_name='known_good')
    c=runpy.run_path(str(TOOLS/'check_originals.py'),run_name='known_good')
    o=runpy.run_path(str(AUDIT/'local_tools/pr880_verify_current_publication.py'),run_name='known_good')
    probes=[];executions=[]
    def attempt(label,call,reject=True,model='resealed synthetic helper fixture'):
        try:call()
        except Exception as e:r={'rejected':True,'exception':type(e).__name__,'reason':str(e)}
        else:r={'rejected':False}
        r.update(label=label,expected_rejection=reject,passed=r['rejected']==reject,trust_model=model);probes.append(r)
        require(r['passed'],'unexpected probe result: '+label)
    with tempfile.TemporaryDirectory(prefix='.engineering_fixture_',dir=HERE) as td:
        work=Path(td)
        blobs={'source/'+p.relative_to(AUDIT/'source').as_posix():p.read_bytes() for p in (AUDIT/'source').rglob('*') if p.is_file()}
        blobs['root_evidence/SOURCE_MANIFEST.json']=(AUDIT/'SOURCE_MANIFEST.json').read_bytes()
        for name in ('check_originals.py','verify_package.py','build_verification.py'):blobs[name]=(TOOLS/name).read_bytes()
        blobs.update({'note.tex':b'SYNTHETIC TEST NOTE\n','note.pdf':b'SYNTHETIC TEST PDF\n','README.md':b'SYNTHETIC TEST README\n','metadata.json':b'{}\n','CURRENT_PRIORITY.md':b'SYNTHETIC TEST PRIORITY\n'})
        index=index_for(blobs);portable={**blobs,'package_index.json':index};root=work/'portable';materialize(root,portable)
        for opt in (False,True):
            for extra in (['--verify-only'],[]):
                r=process(TOOLS/'check_originals.py',['--root',root,*extra],opt)
                require(r['returncode']==0 and r['result']['source_replay']=='NOT_RUN','checker baseline');executions.append({'kind':'checker_verify_only' if extra else 'checker_replay','optimized':opt,**r})
            r=process(TOOLS/'verify_package.py',[sha(index),'--root',root,'--full'],opt)
            require(r['returncode']==0 and r['result']['full_replay']['status']=='PASS','portable baseline');executions.append({'kind':'portable_full','optimized':opt,**r})
        for opt in (False,True):
            r=process(TOOLS/"verify_package.py",[sha(index),"--root",root,"--full"],opt,0o077)
            require(r["returncode"]==0,"restrictive umask relocation failed: "+str(r));executions.append({"kind":"portable_full_umask_077","optimized":opt,**r})
        for name in sorted(blobs):
            p=root/name;raw=p.read_bytes();p.write_bytes(raw+b'\n')
            attempt('fixed_index_payload:'+name,lambda:v['package_inputs'](root,sha(index)),model='unchanged external index pin');p.write_bytes(raw)
        for name,mutate,clean in [
            ('extra_file',lambda:(root/'extra').write_bytes(b'x'),lambda:(root/'extra').unlink()),
            ('extra_empty_directory',lambda:(root/'extra').mkdir(),lambda:(root/'extra').rmdir()),
            ('extra_fifo',lambda:os.mkfifo(root/'extra'),lambda:(root/'extra').unlink()),
            ('extra_symlink',lambda:(root/'extra').symlink_to('README.md'),lambda:(root/'extra').unlink())]:
            mutate();attempt('closed_tree_'+name,lambda:v['package_inputs'](root,sha(index)),model='unchanged external index pin');clean()
        for kind in ('symlink','fifo'):
            p=root/'README.md';raw=p.read_bytes();p.unlink()
            p.symlink_to(root/'note.tex') if kind=='symlink' else os.mkfifo(p)
            attempt('listed_'+kind+'_before_open',lambda:v['package_inputs'](root,sha(index)),model='unchanged external index pin');p.unlink();p.write_bytes(raw)
        p=root/'source/README.md';p.chmod(0o755);attempt('original_executable_mode',lambda:c['original_inputs'](root),model='fixed source manifest and mode rule');p.chmod(0o644)
        variants=[('duplicate_key',index.replace(b'{',b'{"problem_id":"WRONG",',1))]
        variants += [(label,index.replace(b'{',('{"probe":'+value+',').encode(),1)) for label,value in [('nan','NaN'),('infinity','Infinity'),('overflow','1e999')]]
        for label,change in [('boolean_bytes',lambda d:d['files'][0].update(bytes=True)),('float_bytes',lambda d:d['files'][0].update(bytes=1.0)),
                             ('negative_bytes',lambda d:d['files'][0].update(bytes=-1)),('wrong_pid_type',lambda d:d.update(problem_id=9700026)),
                             ('extra_schema_key',lambda d:d.update(extra=1)),('duplicate_path',lambda d:d['files'].append(d['files'][0])),
                             ('file_directory_collision',lambda d:d['files'].append({'path':d['files'][0]['path']+'/x','bytes':0,'sha256':sha(b'')}))]:
            d=json.loads(index);change(d);variants.append((label,encoded(d)))
        for name in ('../x','/x','./x','a\\x','C:x','a//x','a/../x','x\x01'):
            d=json.loads(index);d['files'][0]['path']=name;variants.append(('unsafe_path_'+repr(name),encoded(d)))
        for label,raw in variants:
            (root/'package_index.json').write_bytes(raw);attempt('resealed_index_'+label,lambda raw=raw:v['package_inputs'](root,sha(raw)))
        (root/'package_index.json').write_bytes(index)
        marker=work/'MUST_NOT_EXIST';p=root/'check_originals.py';raw=p.read_bytes()
        p.write_bytes(('from pathlib import Path\nPath('+repr(str(marker))+').write_text("executed")\n').encode()+raw)
        r=process(TOOLS/'verify_package.py',[sha(index),'--root',root,'--full']);require(r['returncode']!=0 and not marker.exists(),'checker startup marker ran')
        probes.append({'label':'fixed_index_checker_startup_marker','passed':True,'rejected':True,'marker_exists':False,'trust_model':'trusted verifier startup and unchanged external index pin'});p.write_bytes(raw)
        p=root/'verify_package.py';raw=p.read_bytes();p.write_bytes(b'raise SystemExit("MUTATED STARTUP")\n'+raw)
        attempt('external_verifier_startup_pin',lambda:v['authenticate'](v['read_regular'](p),{'bytes':len(raw),'sha256':sha(raw)},'startup'),model='external pre-execution startup gate; mutated bytes never execute');p.write_bytes(raw)
        for label,raw in [('duplicate',b'{"a":1,"a":2}'),('nan',b'{"a":NaN}'),('overflow',b'{"a":1e999}')]:attempt('strict_json_'+label,lambda raw=raw:c['strict_json'](raw))
        def zip_fixture(names,mode,delta):
            bio=io.BytesIO()
            with zipfile.ZipFile(bio,'w') as z:
                for name in names:
                    i=zipfile.ZipInfo(name);i.create_system=3;i.external_attr=mode<<16;z.writestr(i,b'x')
            raw=bio.getvalue()
            if delta:
                pos=raw.index(b'PK\x01\x02')+24;raw=raw[:pos]+(1+delta).to_bytes(4,'little')+raw[pos+4:]
            return raw,[{'path':name,'bytes':1,'sha256':sha(b'x')} for name in set(names)]
        for label,names,mode,delta in [('regular',['x'],0o100644,0),('duplicate',['x','x'],0o100644,0),('symlink',['x'],0o120777,0),
                                     ('fifo',['x'],0o010644,0),('directory',['x/'],0o040755,0),('executable',['x'],0o100755,0),
                                     ('declared_size',['x'],0o100644,1),('huge_declared_size',['x'],0o100644,100000000),('absolute',['/x'],0o100644,0),
                                     ('traversal',['../x'],0o100644,0),('backslash',['a\\x'],0o100644,0),('drive',['C:x'],0o100644,0)]:
            raw,rows=zip_fixture(names,mode,delta);attempt('zip_'+label,lambda raw=raw,rows=rows:c['zip_payloads'](raw,rows,label),label!='regular')
        archives=[]
        for opt in (False,True):
            out=work/('built_opt' if opt else 'built_normal');r=process(TOOLS/'build_verification.py',[root,sha(index),sha(blobs['verify_package.py']),out],opt)
            require(r['returncode']==0,'fixture builder failed: '+str(r));archives.append((out/'verification.zip').read_bytes());executions.append({'kind':'builder_fixture','optimized':opt,**r})
        require(archives[0]==archives[1],'deterministic ZIP differs');attempt('deterministic_zip_metadata_and_copies',lambda:o['archive_copies'](archives[0],portable),False)
        time_mutant=archives[0][:10]+(1).to_bytes(2,'little')+archives[0][12:]
        for label,raw in [('trailer',archives[0]+b'SYNTHETIC TRAILER'),('prefix',b'SYNTHETIC PREFIX'+archives[0]),('local_header_time',time_mutant)]:
            attempt('outer_zip_representation_'+label,lambda raw=raw:o['archive_copies'](raw,portable),model='resealed synthetic ZIP representation; no fixed external pin bypass')
        for label,out in [('inside',root/'bad_output'),('collision',root),('nonempty',work/'built_normal')]:
            r=process(TOOLS/'build_verification.py',[root,sha(index),sha(blobs['verify_package.py']),out]);require(r['returncode']!=0,'bad output accepted')
            probes.append({'label':'builder_output_'+label,'passed':True,'rejected':True,'reason':r['result']['reason'],'trust_model':'valid pinned synthetic assembly'})
        r=process(TOOLS/'build_verification.py',[root,sha(index),'0'*64,work/'bad_verifier_out']);require(r['returncode']!=0 and not (work/'bad_verifier_out').exists(),'bad verifier pin accepted')
        probes.append({'label':'builder_wrong_external_verifier_pin','passed':True,'rejected':True,'trust_model':'external verifier pin'})
        preprint={'note.tex':blobs['note.tex'],'output/pdf/note.pdf':blobs['note.pdf'],'README.md':blobs['README.md'],'metadata.json':blobs['metadata.json'],
                  'CURRENT_PRIORITY.md':blobs['CURRENT_PRIORITY.md'],**{n:blobs[n] for n in ('check_originals.py','verify_package.py','build_verification.py')},
                  'package_index.json':index,'verification.zip':archives[0],'zenodo-deposit.json':encoded({'metadata':{},'files':o['DEPOSIT_FILES']})}
        outer={n[7:]:raw for n,raw in blobs.items() if n.startswith('source/') and n[7:] not in ('README.md','PUBLICATION_MANIFEST.json')}
        outer.update({'README.md':b'SYNTHETIC ROOT\n','RESEARCH_LOG.md':b'SYNTHETIC LOG\n','CURRENT_PUBLICATION.json':encoded({'zenodo_metadata':{}}),
                      'verify_current_publication.py':(AUDIT/'local_tools/pr880_verify_current_publication.py').read_bytes()})
        outer.update({o['PREPRINT']+n:raw for n,raw in preprint.items()});outer.update({o['PORTABLE']+n:raw for n,raw in portable.items()})
        outer_index=index_for(outer,True);outer['PUBLICATION_MANIFEST.json']=outer_index;outer_root=work/'outer';materialize(outer_root,outer)
        for opt in (False,True):
            r=process(AUDIT/'local_tools/pr880_verify_current_publication.py',[sha(outer_index),'--root',outer_root,'--full'],opt)
            require(r['returncode']==0,'outer baseline failed: '+str(r));executions.append({'kind':'outer_full_fixture','optimized':opt,**r})
        assembler=AUDIT/'local_tools/pr880_assemble.py'
        for kind,input_root,input_blobs,index_name,document in [('portable',root,portable,'package_index.json','metadata.json'),('outer',outer_root,outer,'PUBLICATION_MANIFEST.json',o['PREPRINT']+'metadata.json')]:
            spec={'schema':'city-ode-explicit-assembly-v1','kind':kind,'files':[{'source':n,'path':n,'bytes':len(raw),'sha256':sha(raw)} for n,raw in sorted(input_blobs.items()) if n!=index_name]}
            spec_path=work/(kind+'_spec.json');spec_raw=encoded(spec);spec_path.write_bytes(spec_raw);out=work/(kind+'_assembled_fixture')
            r=process(assembler,[input_root,spec_path,sha(spec_raw),out]);require(r['returncode']==0 and r['result']['status']=='ASSEMBLED_REQUIRES_INDEPENDENT_VERIFICATION','valid explicit assembler control failed')
            executions.append({'kind':kind+'_explicit_assembler_fixture','optimized':False,**r})
            require((out/index_name).read_bytes()==input_blobs[index_name],'assembler index mismatch')
            for spelling in (index_name,index_name+'/x'):
                changed=json.loads(spec_raw);next(row for row in changed['files'] if row['path']==document)['path']=spelling
                raw=encoded(changed);spec_path.write_bytes(raw);bad_out=work/(kind+'_rejected_'+str(len(probes)))
                r=process(assembler,[input_root,spec_path,sha(raw),bad_out]);require(r['returncode']!=0 and r['result']['reason']=='generated index file/directory collision' and not bad_out.exists(),'assembler generated-index collision materialized output')
                probes.append({'label':'assembler_'+kind+'_generated_index_'+('descendant' if '/' in spelling else 'exact'),'passed':True,'rejected':True,'output_materialized':False,'reason':r['result']['reason'],'trust_model':'externally pinned explicit synthetic assembly spec'})
        altered=dict(outer);altered[o['PREPRINT']+'note.tex']=b'different';attempt('outer_preprint_portable_mismatch',lambda:o['portable_inputs'](altered))
        altered=dict(outer);altered['author/PROOF.md']=b'different';attempt('outer_preserved_original_mismatch',lambda:o['original_copies'](altered,portable))
        altered=dict(portable);altered['source/README.md']=b'different';attempt('outer_archival_original_mismatch',lambda:o['original_copies'](outer,altered))
        altered=dict(portable);altered['note.tex']=b'different';attempt('outer_zip_portable_mismatch',lambda:o['archive_copies'](archives[0],altered))
        provenance={'status':'NOT_RUN','reason':'No complete inputs requested.'}
        if args.provenance:
            repo=next(p for p in AUDIT.parents if (p/'unsolved_math_prioritization/catalog.json').is_file())
            source_args=['--catalog',repo/'unsolved_math_prioritization/catalog.json','--problems',repo/'unsolved_math_prioritization/cache/problems.json',
                         '--reports',repo/'unsolved_math_prioritization/cache/research_results.json','--pdf-dir',AUDIT/'private_sources','--pdf-2012',AUDIT/'private_sources/1209.5120v1.pdf']
            r=process(TOOLS/'check_originals.py',['--root',root,*source_args]);require(r['returncode']==0 and r['result']['source_replay']=='PASS','complete replay failed: '+str(r))
            provenance={'status':'PASS','fixture_method':r['result']['source_fixture_method'],'receipt':r}
        for name,script,arguments in [('checker_partial_source',TOOLS/'check_originals.py',['--root',root,'--catalog',root/'note.tex']),
                                      ('checker_mapping_only',TOOLS/'check_originals.py',['--root',root,'--pdf-2012',root/'note.pdf']),
                                      ('verifier_mapping_only',TOOLS/'verify_package.py',[sha(index),'--root',root,'--pdf-2012',root/'note.pdf'])]:
            r=process(script,arguments);require(r['returncode']!=0,'bad source CLI accepted');probes.append({'label':name,'passed':True,'rejected':True,'reason':r['result']['reason'],'trust_model':'CLI validation'})
        archive_receipt={'bytes':len(archives[0]),'sha256':sha(archives[0]),'members':len(portable),'normal_optimized_identical':True,'fixture_only':True}
    result={'status':'PASS','timestamp_utc':datetime.now(timezone.utc).isoformat(),'completion_estimate_percent':95,
            'scope':'Tool engineering on deleted synthetic document fixtures; no mathematical or priority certification.',
            'harness_sha256':sha(Path(__file__).read_bytes()),'tool_pins':{**{n:sha((TOOLS/n).read_bytes()) for n in ('check_originals.py','verify_package.py','build_verification.py')}, **{n:sha((AUDIT/n).read_bytes()) for n in ('local_tools/pr880_verify_current_publication.py','local_tools/pr880_assemble.py')}},
            'probes':probes,'probe_count':len(probes),'all_probes_passed':all(r['passed'] for r in probes),'executions':executions,
            'top_level_positive_process_count':len(executions),'deterministic_zip_fixture':archive_receipt,'external_inputs':provenance,
            'disposable_fixtures_removed':True,'corpus_bytes_copied':0,'final_assembly_created':False}
    target=HERE/('GUARD_RESULTS_WITH_PROVENANCE.json' if args.provenance else 'GUARD_RESULTS_SOURCE_FREE.json');target.write_bytes(encoded(result))
    print(json.dumps({'status':'PASS','probes':len(probes),'positive_processes':len(executions),'external_inputs':provenance['status'],'output':target.name},indent=2))
if __name__=='__main__':main()
