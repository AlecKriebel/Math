#!/usr/bin/env python3
"""Reproduce frozen controls and safely challenge packet integrity.

Run with the packet's numpy/scipy/sympy versions plus mpmath. Original bytes are
never written: each replay/mutation uses disposable copies. No sources fetched.
The independent mathematical checker is imported only from this review folder.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import sys
import tempfile
import time


def require(ok,message):
    if not ok: raise RuntimeError(message)


def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def hashbytes(data):
    return hashlib.sha256(data).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packet',type=Path)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--mutations-only',action='store_true')
    args=parser.parse_args()
    own=module(Path(__file__).with_name('independent_checker.py'),'pr906_independent')
    packet=args.packet or own.default_packet()
    before=own.authenticate(packet)
    original=module(packet/'verify_publication.py','pr906_frozen_validator')
    anchor=own.PUBLIC_PIN
    result={'status':'PASS','problem_id':30006419,'turns':'2/5','authentication':before,'replays':[],'mutations':[], 'child_guard_challenges':[], 'trust_boundary_observations':[]}
    with tempfile.TemporaryDirectory(prefix='pr906-adversary-',dir='/tmp') as tmp:
        temp=Path(tmp)
        r=temp/'packet'
        shutil.copytree(packet,r)
        if not args.mutations_only:
            modes=[('normal',['-I','-B'],{}),('O',['-I','-B','-O'],{}),('OO',['-I','-B','-OO'],{}),('PYTHONOPTIMIZE_2',['-B'],{'PYTHONOPTIMIZE':'2'})]
            for name,flags,updates in modes:
                env=dict(os.environ)
                env.pop('PYTHONOPTIMIZE',None)
                env['PYTHONDONTWRITEBYTECODE']='1'
                env.update(updates)
                entry={'mode':name,'flags':flags,'environment_updates':updates,'commands':[]}
                def run(relative,params,expected):
                    start=time.monotonic()
                    process=subprocess.run([sys.executable,*flags,str(r/relative),*map(str,params)],cwd=temp,env=env,capture_output=True,timeout=240)
                    require(process.returncode==0,'Frozen replay failed '+name+'/'+relative+': '+process.stderr.decode(errors='replace'))
                    parsed=json.loads(process.stdout)
                    for key,value in expected.items():
                        require(parsed.get(key)==value,'Frozen replay outcome '+name+'/'+relative+'/'+key)
                    entry['commands'].append({'script':relative,'returncode':process.returncode,'seconds':round(time.monotonic()-start,3),'stdout_sha256':hashbytes(process.stdout),'result':parsed})
                    return process.stdout
                run('verify_publication.py',['--expected-manifest',anchor],{'status':'PASS','author_exact_controls':257,'audit_b_executed_mixed_checks':673,'source_identity_checks_omitted':2})
                run('mutation_tests.py',['--expected-manifest',anchor],{'status':'PASS','rejected_mutations':67})
                author=run('author/checks.py',[],{'status':'PASS','total':257})
                require(author==(packet/'author/CHECK_RESULTS.json').read_bytes(),'Standalone author output not byte identical')
                adapter_output=temp/('adapter_'+name+'.json')
                run('source_free_audit_b.py',['--manuscript',r/'author','--output',adapter_output],{'status':'PASS','checks':673,'failed':0})
                adapter=json.loads(adapter_output.read_bytes())
                require(len(adapter['results'])==673 and all(x['passed'] is True for x in adapter['results']),'Direct source-free result count')
                require(not any(x['name'].startswith('independently_retrieved_') for x in adapter['results']),'Source-free falsely reports source inputs')
                entry['direct_adapter_output_sha256']=hashbytes(adapter_output.read_bytes())
                entry['direct_adapter_metadata']=adapter['source_free_replay']
                entry['wrapper_child_optimization_note']='Parent optimize 2 is converted by historical wrapper to -O for children; direct author/adapter executions here do run optimize 2.' if name in ('OO','PYTHONOPTIMIZE_2') else 'Wrapper child optimize level agrees with parent.'
                own.authenticate(r)
                result['replays'].append(entry)
            # Deliberately failing disposable mutants are NOT authentic packet
            # executions. They test that failure guards actually survive -O,
            # -OO and environment optimization, unlike an assert.
            guard_sources={
                'author_explicit_math_guard':(r/'author/checks.py').read_text().replace("check(integ(grad2(f)) ==", "check(False and integ(grad2(f)) ==",1),
                'audit_a_explicit_math_guard':(r/'audit_a/independent_controls.py').read_text().replace("if not all((0 <= a", "if True or not all((0 <= a",1),
            }
            btree=ast.parse((r/'audit_b/independent_checks.py').read_bytes())
            for node in list(btree.body):
                if isinstance(node,ast.For) and isinstance(node.iter,ast.Call) and isinstance(node.iter.func,ast.Attribute) and isinstance(node.iter.func.value,ast.Name) and node.iter.func.value.id=='source_expected':
                    btree.body.remove(node)
            bsource=ast.unparse(btree).replace("require('sampled_a_bounds', all", "require('sampled_a_bounds', False and all",1)
            require("False and all" in bsource,'Missing direct Audit B failing math guard')
            guard_sources['audit_b_source_free_explicit_math_guard']=bsource
            for guard_name,source in guard_sources.items():
                bad_script=temp/(guard_name+'.py');bad_script.write_text(source)
                for name,flags,updates in modes:
                    env=dict(os.environ);env.pop('PYTHONOPTIMIZE',None);env['PYTHONDONTWRITEBYTECODE']='1';env.update(updates)
                    params=['--manuscript',str(r/'author'),'--output',str(temp/'unused.json')] if guard_name.startswith('audit_b') else []
                    process=subprocess.run([sys.executable,*flags,str(bad_script),*params],cwd=temp,env=env,capture_output=True,timeout=60)
                    expected_error='RuntimeError' in process.stderr.decode(errors='replace')
                    require(process.returncode!=0 and expected_error,'Explicit child failure guard disappeared: '+guard_name+'/'+name)
                    result['child_guard_challenges'].append({'case':guard_name,'mode':name,'returncode':process.returncode,'explicit_RuntimeError_observed':True,'stderr_sha256':hashbytes(process.stderr),'scope':'Disposable deliberately failing mutant; tests guard execution, not authenticated packet replay.'})
        def reject(label,validator=original.validate,pin=anchor):
            try: validator(r,pin)
            except (RuntimeError,OSError,ValueError,KeyError,TypeError) as e:
                result['mutations'].append({'name':label,'rejected':True,'exception':type(e).__name__,'reason':str(e)})
            else: raise RuntimeError('Mutation accepted: '+label)
        # The original 67 controls already cover every regular file. Extend them
        # with all nonregular file types and nested directory symlinks.
        for filename in ['PUBLIC_MANIFEST.json','author/PROOF.md','extra_fifo']:
            p=r/filename
            old=p.read_bytes() if p.exists() else None
            if p.exists(): p.unlink()
            os.mkfifo(p)
            reject('FIFO '+filename)
            p.unlink()
            if old is not None: p.write_bytes(old)
        for filename in ['author/PROOF.md','extra_socket']:
            p=r/filename
            old=p.read_bytes() if p.exists() else None
            if p.exists(): p.unlink()
            sock=socket.socket(socket.AF_UNIX)
            try:
                sock.bind(str(p)); reject('Unix socket '+filename)
            finally:
                sock.close(); p.unlink()
                if old is not None: p.write_bytes(old)
        for dirname in ['audit_a','author']:
            p=r/dirname; preserved=temp/('saved_'+dirname)
            p.rename(preserved);p.symlink_to(preserved,target_is_directory=True)
            reject('listed directory symlink '+dirname)
            p.unlink();preserved.rename(p)
        proof=r/'author/PROOF.md'
        proof_bytes=proof.read_bytes()
        public=r/'PUBLIC_MANIFEST.json'
        public_bytes=public.read_bytes()
        def signed_record(name,data):
            changed=json.loads(public_bytes)
            changed['files'][name]={'bytes':len(data),'sha256':hashbytes(data)}
            raw=(json.dumps(changed,indent=2)+'\n').encode()
            public.write_bytes(raw)
            return hashbytes(raw)
        # Semantic corruptions are rejected as byte mutations; the independent
        # checker separately diagnoses coefficient/degree/shift changes.
        for label,old,new in [('narrow cutoff',b'16t^2-1',b'64t^2-1'),('wide cutoff',b'16t^2-1',b'4t^2-1'),
                              ('shift upper bound',b'\\in(0,1/2)',b'\\in(0,1/4)'),('leading degree',b't^3/3',b't^5/5')]:
            require(old in proof_bytes,'Missing intended proof mutant '+label)
            altered=proof_bytes.replace(old,new,1)
            proof.write_bytes(altered)
            reject('semantic byte mutation '+label)
            new_anchor=signed_record('author/PROOF.md',altered)
            reject('resigned proof blocked by independent freeze '+label,pin=new_anchor)
            proof.write_bytes(proof_bytes);public.write_bytes(public_bytes)
        extra=r/'EXTERNAL_SOURCE_PAYLOAD.txt'
        extra.write_bytes(b'DISPOSABLE SYNTHETIC PAYLOAD, NO SOURCE CONTENT\n')
        reject('unlisted extra synthetic source-like payload')
        fresh_anchor=signed_record(extra.name,extra.read_bytes())
        reject('resigned extra payload using authentic external anchor')
        # This is an expected trust boundary: a caller who trusts a changed
        # public anchor has explicitly trusted a changed publication envelope.
        observed=original.validate(r,fresh_anchor)
        require(extra.name in observed['files'],'Expected external trust boundary changed')
        result['trust_boundary_observations'].append({'case':'extra root payload with freshly supplied outer anchor','historical_validator':'ACCEPTS','meaning':'Expected external-anchor trust boundary, not authenticity under the live PR pin. Original pinned nested freezes stay intact. Independent checker hard-codes the live PR anchor and rejects this replacement.'})
        try: own.authenticate(r)
        except RuntimeError as e:
            result['mutations'].append({'name':'independent hard pin rejects caller-resigned extra payload','rejected':True,'reason':str(e)})
        else: raise RuntimeError('Independent anchor boundary failed')
        extra.unlink();public.write_bytes(public_bytes)
        link=temp/'packet_root_symlink'
        link.symlink_to(r,target_is_directory=True)
        original.validate(link,anchor)
        result['trust_boundary_observations'].append({'case':'symlinked packet root','historical_validator':'ACCEPTS after Path.resolve','meaning':'All internal packet symlinks are rejected. Root symlink canonicalization is a wording/tooling boundary, not changed frozen bytes. Independent checker rejects root symlinks.'})
        try: own.authenticate(link)
        except RuntimeError as e:
            result['mutations'].append({'name':'independent root symlink guard','rejected':True,'reason':str(e)})
        else: raise RuntimeError('Independent root guard failed')
        # Explicit record comparator accepts bool as a float. Authentication of
        # frozen producers prevents substituting such records in an authentic
        # packet, but this helper is not a strict numeric type checker.
        original.equivalent(True,1.0)
        result['trust_boundary_observations'].append({'case':'equivalent(True,1.0)','historical_comparator':'ACCEPTS','meaning':'Numeric tolerance helper uses isinstance(bool,int); not a strict numeric type guarantee. Authenticated exact producers and independent guards remain necessary.'})
        original.validate(r,anchor);own.authenticate(r)
    after=own.authenticate(packet)
    require(before==after,'Original packet changed')
    result['extended_rejected_mutations']=len(result['mutations'])
    result['original_authenticated_before_and_after']=True
    result['scope']='Frozen finite controls reproduced; expanded nonregular/inventory/pin adversary. Tooling boundaries are separated from mathematical truth. Original author 2/5 count retained.'
    args.output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':result['status'],'modes':len(result['replays']),'extended_rejected_mutations':len(result['mutations']),'trust_boundary_observations':len(result['trust_boundary_observations']),'original_unchanged':True},indent=2))


if __name__=='__main__':main()
