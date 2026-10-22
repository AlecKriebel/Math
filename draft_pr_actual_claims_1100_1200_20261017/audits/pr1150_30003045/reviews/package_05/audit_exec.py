#!/usr/bin/env python3
"""Package05 independent offline, rebuild and path/integrity controls.

All mutations are confined to ignored owned copies beside this script.
"""
from pathlib import Path
import datetime, hashlib, json, os, shutil, subprocess, sys, zipfile

R=Path(__file__).absolute().parent
BASE=R/'private/source'
P='draft_pr_actual_claims_1100_1200_20261017/audits/pr1150_30003045'
AUD=BASE/P
INNER=AUD/'pr_repair_candidate'
SOURCE='mixed-kato-counterexample-source-and-verification.zip'
OUTPUTS=['output/'+SOURCE,'output/zenodo-upload-kit.zip','PACKAGE_RECEIPT.json']
FROZEN=R.parent.parent/'publication'
SIX=['main.tex','output/pdf/mixed-kato-counterexample.pdf',*OUTPUTS[:2],'zenodo-metadata.json','zenodo-deposit.json']
def need(ok,msg):
    if not ok: raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(p):
    b=p.read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def save(n,o): (R/n).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
OFF=R/'private/offline';OFF.mkdir(exist_ok=True)
(OFF/'sitecustomize.py').write_text("import sys\ndef no_network(event,args):\n if event.startswith('socket.') and event not in ('socket.__new__',): raise RuntimeError('OFFLINE network denied: '+event)\nsys.addaudithook(no_network)\n")
ENV=dict(os.environ,PYTHONPATH=str(OFF),PYTHONDONTWRITEBYTECODE='1')
def run(path,flags=(),args=()):
    r=subprocess.run([sys.executable,'-B',*flags,str(path),*args],capture_output=True,env=ENV,timeout=180)
    return r,{'exit':r.returncode,'stdout':r.stdout.decode(),'stderr':r.stderr.decode(),'stdout_sha256':sha(r.stdout),'last_error':r.stderr.decode().splitlines()[-1] if r.stderr else ''}
def fresh(n):
    dest=R/'private/cases'/n
    if dest.exists():shutil.rmtree(dest)
    sentinel=dest.parent/(dest.name+'_outside')
    if sentinel.is_dir() and not sentinel.is_symlink():shutil.rmtree(sentinel)
    elif sentinel.exists() or sentinel.is_symlink():sentinel.unlink()
    shutil.copytree(BASE,dest);return dest
def state(p):
    st=p.stat();return {'bytes':len(p.read_bytes()),'sha256':sha(p.read_bytes()),'inode':st.st_ino,'mtime_ns':st.st_mtime_ns}
def states(d,exclude=()):return {n:state(d/n) for n in OUTPUTS if n not in exclude}

def main():
    # Start each independent execution from the original authenticated ZIP.
    with zipfile.ZipFile(FROZEN/'output'/SOURCE) as z:
        info=z.infolist();names=[i.filename for i in info]
        need(len(names)==len(set(names)),'duplicate ZIP names')
        for i in info:
            q=Path(i.filename)
            need(not q.is_absolute() and '..' not in q.parts and not i.is_dir() and ((i.external_attr>>16)&0o170000) in (0,0o100000),'unsafe ZIP member')
        if BASE.exists():shutil.rmtree(BASE)
        BASE.mkdir(parents=True)
        for i in info:
            p=BASE/i.filename;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(i))
    manifest=json.loads((BASE/'SOURCE_MANIFEST.json').read_text())
    actual={str(p.relative_to(BASE)) for p in BASE.rglob('*') if p.is_file()}
    need(actual==set(manifest)|{'SOURCE_MANIFEST.json'},'source manifest inventory')
    for n,w in manifest.items():need(pin(BASE/n)==w,'source manifest '+n)
    allowed=json.loads((BASE/'verification/AUDIT_MEMBERS.json').read_text())
    for n,w in allowed.items():need(pin(AUD/n)==w,'audit manifest '+n)
    meta=json.loads((BASE/'zenodo-metadata.json').read_text());dep=json.loads((BASE/'zenodo-deposit.json').read_text())
    need(meta==dep['metadata'],'metadata object equality')
    kit=R/'private/kit';portable=json.loads((kit/'zenodo-deposit.json').read_text())
    need(portable['metadata']==meta,'portable metadata')
    need(portable['files']==[{'path':'mixed-kato-counterexample.pdf'},{'path':SOURCE}],'portable paths')
    for a,b in [(BASE/'output/pdf/mixed-kato-counterexample.pdf',kit/'mixed-kato-counterexample.pdf'),(FROZEN/'output'/SOURCE,kit/SOURCE),(BASE/'zenodo-metadata.json',kit/'zenodo-metadata.json'),(BASE/'README.md',kit/'README.md')]:need(a.read_bytes()==b.read_bytes(),'kit member equality '+str(a))
    save('MANIFEST_CHECKS.json',{'status':'PASS','source_members':len(actual),'manifest_entries':len(manifest),'authored_audit_members':len(allowed),'kit_members':len(list(kit.iterdir())),'all_member_pins_match':True,'portable_metadata_and_payloads_equal':True})

    runs=[]
    for flags in [(),('-O',)]:
        r,rec=run(BASE/'verification/verify_all.py',flags);need(r.returncode==0 and r.stdout==(BASE/'verification/REPLAY_RECEIPT.json').read_bytes() and not r.stderr,'outer full replay')
        save('REPLAY_'+('OPTIMIZED' if flags else 'NORMAL')+'.json',json.loads(r.stdout));runs.append({'kind':'outer','flags':flags,**rec})
    exact=[];wrong=[]
    diagnostics={'differentiate_square':'wrong d(beta squared)=d beta','wrong_h_frobenius':'wrong beta exponent in h squared','wrong_s_power':'wrong s^-2 in xi','omit_exact_correction':'wrong equality of differential representatives','gamma_kills_dz':'wrong independent gamma kills dz','a_belongs_R':'wrong a belongs R','wrong_quotient_derivative':'wrong quotient obstruction numerator','slot_z_preserves_dz':'wrong square-root slot preserves dz','invalid_exponent_one_base_dlog':'wrong base-field dlog(1+uz) with du term omitted'}
    for flags in [(),('-O',)]:
        for prog,baseline in [('verify_symbols.py','symbols_expected.json'),('diagnose_norm.py','norm_expected.json')]:
            r,rec=run(INNER/prog,flags);need(r.returncode==0 and not r.stderr and r.stdout==(INNER/baseline).read_bytes(),'direct complete output '+prog);exact.append({'program':prog,'flags':flags,**rec})
        for mode,expected in diagnostics.items():
            r,rec=run(INNER/'verify_symbols.py',flags,('--wrong',mode));need(r.returncode==1 and rec['last_error']=='ValueError: CHECK FAILED: '+expected and not r.stdout,'direct computed failure '+mode);wrong.append({'mode':mode,'flags':flags,**rec})
    save('DIRECT_MATH_EXECUTIONS.json',{'complete_positive_outputs':exact,'actual_computed_wrong_result_failures':wrong,'wrong_result_failures':len(wrong),'network_policy':'Inherited sitecustomize audit hook denies socket operations; programs independently inspected for stdlib-only/no-network imports.'})
    r,rec=run(INNER/'verify_all.py');need(r.returncode==0 and not r.stderr,'inner runner');runs.append({'kind':'inner',**rec})
    save('OFFLINE_REPLAY.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'runs':runs,'status':'PASS'})
    r,rec=run(BASE/'build_package.py');need(r.returncode==0 and not r.stderr,'private rebuild')
    rebuild={n:{'rebuilt':pin(BASE/n),'frozen':pin(FROZEN/n),'equal':(BASE/n).read_bytes()==(FROZEN/n).read_bytes()} for n in SIX}
    need(all(v['equal'] for v in rebuild.values()),'six byte-exact rebuild')
    need((BASE/'PACKAGE_RECEIPT.json').read_bytes()==(FROZEN/'PACKAGE_RECEIPT.json').read_bytes(),'receipt rebuild')
    save('PRIVATE_REBUILD.json',{'status':'PASS','files':rebuild,'receipt_equal':True,'process':rec,'pinned_pdf_not_tex_recompile':True})
    print('Replay, all-member validation and byte-exact rebuild passed',flush=True)

    controls=[]
    for flags in [(),('-O',)]:
      for tool in ['verifier','builder']:
       for mode in ['corrupt_proof','missing_member','flat_extra_file','flat_extra_directory','flat_directory_symlink','leaf_symlink','ancestor_symlink','unsafe_allowlist','metadata_disagreement']:
        if mode=='metadata_disagreement' and tool=='verifier':continue
        d=fresh(tool+'_'+mode+('_O' if flags else ''));a=d/P;inner=a/'pr_repair_candidate'
        if mode=='corrupt_proof':(a/'FINAL_PROOF.md').write_bytes((a/'FINAL_PROOF.md').read_bytes()+b'corruption\n')
        elif mode=='missing_member':(inner/'README.md').unlink()
        elif mode=='flat_extra_file':(inner/'extra').write_bytes(b'extra')
        elif mode=='flat_extra_directory':(inner/'extra').mkdir()
        elif mode=='flat_directory_symlink':(inner/'extra').symlink_to(d/'output',target_is_directory=True)
        elif mode=='leaf_symlink':
            p=inner/'README.md';target=d/'same_payload';target.write_bytes(p.read_bytes());p.unlink();p.symlink_to(target)
        elif mode=='ancestor_symlink':
            p=a/'reviews';target=d/'same_payload_reviews';p.rename(target);p.symlink_to(target,target_is_directory=True)
        elif mode=='unsafe_allowlist':
            p=d/'verification/AUDIT_MEMBERS.json';v=json.loads(p.read_text());v['../outside']=next(iter(v.values()));p.write_text(json.dumps(v))
        elif mode=='metadata_disagreement':
            p=d/'zenodo-metadata.json';v=json.loads(p.read_text());v['title']='Deliberately mismatched';p.write_text(json.dumps(v))
        before=states(d);r,rec=run(d/('verification/verify_all.py' if tool=='verifier' else 'build_package.py'),flags);after=states(d)
        need(r.returncode!=0 and 'ValueError:' in rec['stderr'] and before==after,'integrity rejection/preservation '+tool+mode)
        controls.append({'tool':tool,'mode':mode,'flags':flags,'before':before,'after':after,**rec})
      print('Integrity controls passed '+str(flags),flush=True)
    save('INTEGRITY_CONTROLS.json',{'status':'PASS','count':len(controls),'controls':controls,'separate_from_18_mathematical_failures':True})

    path=[]
    for flags in [(),('-O',)]:
      for index,n in enumerate(OUTPUTS):
       for mode in ['symlink','directory','fifo']:
        d=fresh('out_'+str(index)+'_'+mode+('_O' if flags else ''));p=d/n;p.unlink();outside=d.parent/(d.name+'_outside');outside.write_bytes(b'DISTINCT OUTSIDE SENTINEL '+mode.encode());sentinel=state(outside)
        if mode=='symlink':p.symlink_to(outside)
        elif mode=='directory':p.mkdir()
        else:os.mkfifo(p)
        before=states(d,(n,));r,rec=run(d/'build_package.py',flags);after=states(d,(n,));sentinel_after=state(outside)
        need(r.returncode!=0 and 'ValueError:' in rec['stderr'] and before==after and sentinel==sentinel_after,'output rejection '+n+mode)
        path.append({'output':n,'mode':mode,'flags':flags,'other_before':before,'other_after':after,'outside_before':sentinel,'outside_after':sentinel_after,**rec})
      for mode in ['ancestor_regular','ancestor_symlink']:
        d=fresh(mode+('_O' if flags else ''));p=d/'output';target=d.parent/(d.name+'_outside');p.rename(target)
        if mode=='ancestor_regular':p.write_bytes(b'not a directory')
        else:p.symlink_to(target,target_is_directory=True)
        before={n:state((target/Path(n).relative_to('output')) if n.startswith('output/') else d/n) for n in OUTPUTS}
        r,rec=run(d/'build_package.py',flags)
        after={n:state((target/Path(n).relative_to('output')) if n.startswith('output/') else d/n) for n in OUTPUTS}
        need(r.returncode!=0 and 'ValueError:' in rec['stderr'] and before==after,'output ancestor rejection '+mode)
        path.append({'mode':mode,'flags':flags,'before':before,'after':after,**rec})
      for index,n in enumerate(OUTPUTS):
        d=fresh('hardlink_'+str(index)+('_O' if flags else ''));p=d/n;outside=d.parent/(d.name+'_outside');outside.write_bytes(b'DISTINCT BYTES HARDLINK CONTROL '+n.encode());p.unlink();os.link(outside,p);before=state(outside);shared=state(p)
        need(shared['inode']==before['inode'] and shared['sha256']!=pin(BASE/n)['sha256'],'meaningful original hardlink')
        r,rec=run(d/'build_package.py',flags);after=state(outside);new=state(p)
        need(r.returncode==0 and not r.stderr and before==after and new['inode']!=before['inode'] and (d/n).read_bytes()==(BASE/n).read_bytes(),'atomic hardlink preservation '+n)
        path.append({'output':n,'mode':'distinct_byte_hardlink_success','flags':flags,'outside_before':before,'outside_after':after,'old_output':shared,'new_output':new,**rec})
      print('Output controls passed '+str(flags),flush=True)
    save('OUTPUT_PATH_CONTROLS.json',{'status':'PASS','count':len(path),'controls':path,'static_contract_only':True,'separate_from_18_mathematical_failures':True})
    print('ALL PACKAGE05 EXECUTION CHECKS PASSED',flush=True)

if __name__=='__main__':main()
