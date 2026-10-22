#!/usr/bin/env python3
"""Fail-closed integrity controls; mutations occur only in disposable copies."""
import copy,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
CASES=['changed_bytes','same_size_changed_bytes','missing_file','extra_file','extra_directory','symlink_file','unsafe_manifest_path','absolute_manifest_path','duplicate_manifest_path','manifest_self_entry','wrong_byte_count','wrong_hash','noncanonical_manifest','duplicate_json_key','wrong_external_pin','nonregular_object','rebased_original_anchor','rebased_acceptance_status','rebased_missing_binding']
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def canonical(obj):return (json.dumps(obj,indent=2,sort_keys=True)+'\n').encode()
def ident(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def run(root,flags=(),expected=None):
 args=[sys.executable,'-I','-B',*flags,str(root/'verify_package.py')]
 if expected is not None:args+=['--manifest-sha256',expected]
 return subprocess.run(args,cwd=root,capture_output=True,timeout=30)
def rebase_manifest(work,m):
 for row in m['files']:row.update(ident((work/row['path']).read_bytes()))
 (work/'MANIFEST.json').write_bytes(canonical(m))
def main():
 require(run(ROOT).returncode==0,'Original package failed integrity')
 records=[]
 with tempfile.TemporaryDirectory(prefix='handlebody-tamper-') as temp:
  for name in CASES:
   work=Path(temp)/name;shutil.copytree(ROOT,work)
   for p in work.rglob('*'):
    if p.is_file():p.chmod(0o644)
   readme=work/'README.md';manifest=work/'MANIFEST.json';m=json.loads(manifest.read_bytes());reason=None
   if name=='changed_bytes':readme.write_bytes(readme.read_bytes()+b'changed\n');reason='Wrong byte count: README.md'
   elif name=='same_size_changed_bytes':readme.write_bytes(b'!'+readme.read_bytes()[1:]);reason='Wrong hash: README.md'
   elif name=='missing_file':readme.unlink();reason='Missing file or symlink: README.md'
   elif name=='extra_file':(work/'unexpected.json').write_text('{}');reason='Unexpected or unlisted payload files'
   elif name=='extra_directory':(work/'unexpected').mkdir();reason='Unexpected or missing payload directory'
   elif name=='symlink_file':(work/'unexpected').symlink_to('README.md');reason='Symlink in public payload'
   elif name=='nonregular_object':os.mkfifo(work/'unexpected_fifo');reason='Nonregular object in public payload'
   elif name in ['unsafe_manifest_path','absolute_manifest_path']:
    m['files'][0]['path']='../outside' if name=='unsafe_manifest_path' else '/outside';manifest.write_bytes(canonical(m));reason='Unsafe or self-referential path'
   elif name=='duplicate_manifest_path':m['files'].append(copy.deepcopy(m['files'][0]));manifest.write_bytes(canonical(m));reason='Unsorted or duplicate manifest paths'
   elif name=='manifest_self_entry':m['files'][0]['path']='MANIFEST.json';manifest.write_bytes(canonical(m));reason='Unsafe or self-referential path'
   elif name=='wrong_byte_count':m['files'][0]['bytes']+=1;manifest.write_bytes(canonical(m));reason='Wrong byte count:'
   elif name=='wrong_hash':m['files'][0]['sha256']='0'*64;manifest.write_bytes(canonical(m));reason='Wrong hash:'
   elif name=='noncanonical_manifest':manifest.write_text(json.dumps(m));reason='Noncanonical manifest encoding'
   elif name=='duplicate_json_key':manifest.write_bytes(b'{"schema":"discarded",'+manifest.read_bytes()[1:]);reason='Duplicate JSON key: schema'
   elif name=='wrong_external_pin':reason='External manifest pin mismatch'
   elif name=='rebased_original_anchor':
    p=work/'ORIGINAL_IDENTITIES.json';obj=json.loads(p.read_bytes())
    row=next(r for r in obj['files'] if r['path']=='pass1_genus_two/GENUS_TWO_GENERATORS.md');row['original_sha256']='0'*64
    p.write_bytes(canonical(obj));rebase_manifest(work,m);reason='Original acceptance anchor differs: pass1_genus_two/GENUS_TWO_GENERATORS.md'
   elif name=='rebased_acceptance_status':
    rel='pass1_audit/RESULT.json';p=work/rel;obj=json.loads(p.read_bytes());obj['status']='FAIL';p.write_bytes(canonical(obj));pin=ident(p.read_bytes())
    p=work/'ORIGINAL_IDENTITIES.json';obj=json.loads(p.read_bytes());row=next(r for r in obj['files'] if r['path']==rel);row['public_bytes']=pin['bytes'];row['public_sha256']=pin['sha256'];p.write_bytes(canonical(obj))
    p=work/'AUDIT_BINDINGS.json';obj=json.loads(p.read_bytes())
    for b in obj['bindings']:
     if b['path']==rel:b['public_copy']=pin
    p.write_bytes(canonical(obj));rebase_manifest(work,m);reason='Final acceptance absent'
   elif name=='rebased_missing_binding':
    p=work/'AUDIT_BINDINGS.json';obj=json.loads(p.read_bytes());obj['bindings']=[b for b in obj['bindings'] if b['path']!='ROOT_EXACT_CHECKS.json'];p.write_bytes(canonical(obj));rebase_manifest(work,m);reason='Original binding coverage differs'
   require(reason is not None,'Unimplemented control')
   for mode,flags in [('normal',[]),('optimized',['-O']),('double_optimized',['-OO'])]:
    cp=run(work,flags,expected='0'*64 if name=='wrong_external_pin' else None)
    require(cp.returncode!=0 and reason.encode() in cp.stderr,'Control accepted or wrong rejection: '+name+' '+mode+' '+cp.stderr.decode())
   records.append({'case':name,'expected_rejection':reason,'rejected_in_all_three_modes':True})
 require(run(ROOT).returncode==0,'Original package changed')
 print(json.dumps({'status':'PASS','case_count':len(records),'verification_invocations':3*len(records),'modes':['normal','optimized','double_optimized'],'original_package_intact':True,'controls':records},indent=2,sort_keys=True))
if __name__=='__main__':main()
