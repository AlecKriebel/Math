#!/usr/bin/env python3
"""Read-only UID-1000 audit. No network, source bodies, publication, or assertions.
Usage: python reproduce_audit.py ORIGINAL_PACKET CORRECTED_PACKET OUTPUT_JSON
Only temporary copies are changed; supplied inputs remain unchanged.
"""
from pathlib import Path
import ast, hashlib, json, os, shutil, stat, subprocess, sys, tempfile

ORIGINAL_PIN='9e290bec9d6ba40ec3a61a1c41b9e70381f75c3ab80db6e2a4ef55f83d3aa751'
CORRECTED_PIN='daaf2d88de9272733ea1d674396ec2236cfe250d4796dc922e841890ff087b69'

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def snapshot(folder):
    return {str(p.relative_to(folder)): {'bytes':p.stat().st_size,'sha256':digest(p.read_bytes()),'mode':stat.S_IMODE(p.stat().st_mode)}
            for p in sorted(folder.rglob('*')) if p.is_file()}

def readonly(folder):
    for p in folder.rglob('*'):
        p.chmod(0o555 if p.is_dir() else 0o444)
    folder.chmod(0o555)
    denied=[]
    for p in [folder/'REPORT.md', folder/'new_write_probe']:
        try:
            fd=os.open(p,os.O_WRONLY|os.O_CREAT,0o600)
        except PermissionError:
            denied.append(True)
        else:
            os.close(fd)
            denied.append(False)
    require(all(denied),'read-only input could be written')
    require(not os.access(folder,os.W_OK),'directory remains writable')
    return {'directory_mode':'0555','file_modes':'0444','existing_write_denied':denied[0], 'new_write_denied':denied[1]}

WRAPPER='import os,sys,json,runpy; print(json.dumps({"audit_runtime":{"uid":os.getuid(),"euid":os.geteuid(),"gid":os.getgid(),"optimize":sys.flags.optimize}}),flush=True); runpy.run_path(sys.argv[1],run_name="__main__")'
MODES=[('normal',[],None),('-O',['-O'],None),('-OO',['-OO'],None),('env-O',[], '1'),('env-OO',[], '2')]

def run(folder, script, mode):
    label, flags, env_opt=mode
    env=dict(os.environ)
    env.pop('PYTHONOPTIMIZE',None)
    env['PYTHONDONTWRITEBYTECODE']='1'
    if env_opt is not None:env['PYTHONOPTIMIZE']=env_opt
    before=snapshot(folder)
    result=subprocess.run([sys.executable,'-B',*flags,'-c',WRAPPER,str(folder/script)],cwd=folder,env=env,text=True,capture_output=True,timeout=120)
    require(before==snapshot(folder),'input changed during test')
    first,*rest=result.stdout.splitlines()
    runtime=json.loads(first)['audit_runtime']
    require(runtime['uid']==1000 and runtime['euid']==1000,'not genuine UID 1000')
    body='\n'.join(rest)
    return {'mode':label,'script':script,'runtime':runtime,'returncode':result.returncode,'stdout_sha256':digest(result.stdout.encode()),'stderr_sha256':digest(result.stderr.encode()),'pass_claimed':'"status": "PASS"' in body,'input_unchanged':True,'last_error_line':result.stderr.strip().splitlines()[-1] if result.stderr.strip() else None,'result':json.loads(body) if result.returncode==0 else None}

def rehash(folder,filename):
    p=folder/'FROZEN_MANIFEST.json'
    m=json.loads(p.read_text())
    for item in m['files']:
        if item['path']==filename:
            data=(folder/filename).read_bytes();item['bytes']=len(data);item['sha256']=digest(data)
    p.write_text(json.dumps(m,indent=2)+'\n')

def mutate(folder,kind):
    p=folder/'FROZEN_MANIFEST.json'
    if kind=='extra_file':(folder/'UNLISTED.txt').write_text('audit control\n')
    elif kind=='report_same_size':
        p=folder/'REPORT.md';s=p.read_text();require('unresolved' in s,'mutation target');p.write_text(s.replace('unresolved','not solved',1))
    elif kind=='report_truncated':
        p=folder/'REPORT.md';p.write_bytes(p.read_bytes()[:-9])
    elif kind=='manifest_bytes':
        m=json.loads(p.read_text());m['files'][0]['bytes']+=1;p.write_text(json.dumps(m))
    elif kind=='manifest_hash':
        m=json.loads(p.read_text());m['files'][0]['sha256']='0'*64;p.write_text(json.dumps(m))
    elif kind=='saved_wrong_count_rehashed':
        p=folder/'CHECK_RESULTS.json';m=json.loads(p.read_text());m['checks']['horizontal_cover_arithmetic']+=1;p.write_text(json.dumps(m));rehash(folder,p.name)
    elif kind=='saved_wrong_bool_rehashed':
        p=folder/'CHECK_RESULTS.json';m=json.loads(p.read_text());m['does_not_prove_original_problem']=False;p.write_text(json.dumps(m));rehash(folder,p.name)
    elif kind=='saved_integer_true_rehashed':
        p=folder/'CHECK_RESULTS.json';m=json.loads(p.read_text());m['does_not_prove_original_problem']=1;p.write_text(json.dumps(m));rehash(folder,p.name)
    elif kind=='saved_nan_rehashed':
        p=folder/'CHECK_RESULTS.json';m=json.loads(p.read_text());m['checks']['horizontal_cover_arithmetic']=float('nan');p.write_text(json.dumps(m));rehash(folder,p.name)
    elif kind=='bad_math_reeb_rehashed':
        p=folder/'check_math.py';s=p.read_text();a='zx,zy=Q(py,f*f),Q(-px,f*f)';require(a in s,'Reeb mutation target');p.write_text(s.replace(a,'zx,zy=Q(py,f*f),Q(px,f*f)'));rehash(folder,p.name)
    elif kind=='bad_math_d3_rehashed':
        p=folder/'check_math.py';s=p.read_text();a='c_square=-(1-2*g)**2';require(a in s,'Chern mutation target');p.write_text(s.replace(a,'c_square=(1-2*g)**2'));rehash(folder,p.name)
    else:raise RuntimeError(kind)


def main():
    require(len(sys.argv)==4,'usage: ORIGINAL CORRECTED OUTPUT_JSON')
    original,corrected,output=map(lambda s:Path(s).resolve(),sys.argv[1:])
    require(os.getuid()==1000 and os.geteuid()==1000,'run as UID 1000')
    source_snapshots={str(p):snapshot(p) for p in [original,corrected]}
    for p,pin in [(original,ORIGINAL_PIN),(corrected,CORRECTED_PIN)]:require(digest((p/'FROZEN_MANIFEST.json').read_bytes())==pin,'packet pin mismatch')
    rows=[]
    checks=['extra_file','report_same_size','report_truncated','manifest_bytes','manifest_hash','saved_wrong_count_rehashed','saved_wrong_bool_rehashed','saved_integer_true_rehashed','saved_nan_rehashed','bad_math_reeb_rehashed','bad_math_d3_rehashed']
    with tempfile.TemporaryDirectory(prefix='contact-support-audit-') as temp:
        temp=Path(temp)
        for name,source in [('original',original),('corrected',corrected)]:
            folder=temp/(name+'_baseline');shutil.copytree(source,folder);ro=readonly(folder)
            for mode in MODES:
                for script in ['check_math.py','verify_packet.py']:
                    r=run(folder,script,mode);r.update(packet=name,test='baseline',readonly=ro);rows.append(r)
                    require(r['returncode']==0 and r['pass_claimed'],'baseline failed')
            for kind in checks:
                folder=temp/(name+'_'+kind);shutil.copytree(source,folder);mutate(folder,kind);ro=readonly(folder)
                scripts=['verify_packet.py']+(['check_math.py'] if kind.startswith('bad_math') else [])
                for mode in MODES:
                    for script in scripts:
                        r=run(folder,script,mode);r.update(packet=name,test=kind,readonly=ro);rows.append(r)
                        # Exact-type equality is deliberately characterized, not silently repaired.
                        if name=='corrected' and kind!='saved_integer_true_rehashed':require(r['returncode']!=0 and not r['pass_claimed'],'corrected verifier accepted invalid control')
        # TemporaryDirectory needs writable directories to remove its own controls.
        for p in temp.rglob('*'):
            if p.is_dir():p.chmod(0o755)
        for p in temp.iterdir():
            if p.is_dir():p.chmod(0o755)
    for p in [original,corrected]:require(snapshot(p)==source_snapshots[str(p)],'supplied packet changed')
    result={'status':'PASS','meaning':'Audit completed; original optimized vulnerabilities are recorded, not accepted as robust verification.','uid':os.getuid(),'python_version':sys.version,'original_manifest_sha256':ORIGINAL_PIN,'corrected_manifest_sha256':CORRECTED_PIN,'total_runs':len(rows),'rows':rows,'input_packets_unchanged':True,'strict_json_schema_claimed':False,'exact_type_limitation':'Self-rehashed true-to-1 substitution compares equal under Python JSON-object equality; external frozen manifest pin still rejects altered bytes. This minimal optimization fix does not claim exact-type schema validation.'}
    output.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','runs':len(rows),'output':str(output),'original_false_passes':sum(r['packet']=='original' and r['test']!='baseline' and r['returncode']==0 for r in rows),'corrected_accepted_type_equivalence':sum(r['packet']=='corrected' and r['test']=='saved_integer_true_rehashed' and r['returncode']==0 for r in rows)},indent=2))

if __name__=='__main__':main()
