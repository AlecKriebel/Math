"""Authenticate this suite and the verifier externally before running."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('Use python -I -S -B mutation_tests.py PIN PACKET')
from pathlib import Path
import hashlib,json,shutil,subprocess,tempfile

def require(ok,message):
    if not ok:raise RuntimeError(message)
def sha(b):return hashlib.sha256(b).hexdigest()
def snapshot(root):return {p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
def run(script,packet,pin,opt):return subprocess.run([sys.executable,'-I','-S','-B',*(['-O']*opt),str(script),pin,str(packet)],capture_output=True,timeout=600)
def repin(packet):
    p=packet/'PUBLIC_MANIFEST.json';j=json.loads(p.read_bytes())
    for row in j['files']:
        b=(packet/row['path']).read_bytes();row.update(bytes=len(b),sha256=sha(b))
    b=(json.dumps(j,indent=2,sort_keys=True)+'\n').encode();p.write_bytes(b);return sha(b)
require(len(sys.argv)==3,'Expected pin and packet')
pin=sys.argv[1];root=Path(sys.argv[2]).absolute();original=snapshot(root)
results={'problem_id':30002395,'passing_replays':[],'rejected_mutations':[]}
with tempfile.TemporaryDirectory(prefix='dini-corruption-') as td:
    base=Path(td);trusted=base/'trusted_verify.py';trusted.write_bytes(original['verify_publication.py'])
    relocated=base/'relocated';shutil.copytree(root,relocated)
    for name,packet in [('original',root),('relocated',relocated)]:
        for opt in (0,1,2):
            r=run(trusted,packet,pin,opt);require(r.returncode==0,name+' failed: '+r.stderr.decode());j=json.loads(r.stdout)
            require(j['status']=='pass' and j['python_optimization']==opt and all(p['optimization']==opt for p in j['child_runtimes'].values()) and j['frozen_child_assertions_active']==(opt==0) and j['source_pdf_bytes_rechecked'] is False,'Incorrect child replay receipt')
            results['passing_replays'].append({'case':name,'optimization':opt,'status':'pass','child_runtimes':j['child_runtimes']})
    labels=['payload','extra_hidden','missing','empty_directory','payload_symlink','manifest_symlink','directory_symlink','root_symlink','wrong_pin','manifest_byte','verifier_byte','duplicate_inventory','traversal_inventory','absolute_inventory','duplicate_json_key','laundered_author_proof','laundered_author_manifest','laundered_audit_report','laundered_audit_manifest','laundered_corrected_proof','laundered_corrected_manifest','laundered_patch']
    for label in labels:
        packet=base/label;shutil.copytree(root,packet);test_pin=pin
        if label=='payload':(packet/'ACCEPTANCE.md').write_bytes(original['ACCEPTANCE.md']+b'!')
        elif label=='extra_hidden':(packet/'.unlisted').write_bytes(b'x')
        elif label=='missing':(packet/'README.md').unlink()
        elif label=='empty_directory':(packet/'unlisted').mkdir()
        elif label in ('payload_symlink','manifest_symlink'):
            name='README.md' if label=='payload_symlink' else 'PUBLIC_MANIFEST.json';(packet/name).unlink();(packet/name).symlink_to(root/name)
        elif label=='directory_symlink':shutil.rmtree(packet/'public');(packet/'public').symlink_to(root/'public',target_is_directory=True)
        elif label=='root_symlink':
            linked=base/'linked_root';linked.symlink_to(packet,target_is_directory=True);packet=linked
        elif label=='wrong_pin':test_pin='0'*64
        elif label=='manifest_byte':(packet/'PUBLIC_MANIFEST.json').write_bytes(original['PUBLIC_MANIFEST.json']+b' ')
        elif label=='verifier_byte':(packet/'verify_publication.py').write_bytes(b'print("pass")\n')
        elif label=='duplicate_json_key':
            b=original['PUBLIC_MANIFEST.json'].replace(b'{',b'{"problem_id":30002395,',1);(packet/'PUBLIC_MANIFEST.json').write_bytes(b);test_pin=sha(b)
        elif label.startswith('laundered_'):
            name={'laundered_author_proof':'public/PROOF.md','laundered_author_manifest':'public/MANIFEST.json','laundered_audit_report':'independent_audit/AUDIT.md','laundered_audit_manifest':'independent_audit/MANIFEST.json','laundered_corrected_proof':'independent_audit/corrected/PROOF.md','laundered_corrected_manifest':'independent_audit/corrected/MANIFEST.json','laundered_patch':'independent_audit/CORRECTION.patch'}[label]
            (packet/name).write_bytes(original[name]+b' ');test_pin=repin(packet)
        else:
            j=json.loads(original['PUBLIC_MANIFEST.json'])
            if label=='duplicate_inventory':j['files'][-1]=j['files'][0]
            elif label=='traversal_inventory':j['files'][0]['path']='../outside'
            else:j['files'][0]['path']='/tmp/outside'
            b=(json.dumps(j,indent=2)+'\n').encode();(packet/'PUBLIC_MANIFEST.json').write_bytes(b);test_pin=sha(b)
        for opt in (0,1,2):
            r=run(trusted,packet,test_pin,opt);require(r.returncode!=0 and r.stderr.startswith(b'REJECTED: '),'Mutation accepted: '+label)
            results['rejected_mutations'].append({'case':label,'optimization':opt,'status':'rejected','diagnostic':r.stderr.decode().strip()})
require(snapshot(root)==original,'Original packet changed')
results.update(status='pass',original_preserved=True,passing_replay_count=len(results['passing_replays']),rejected_mutation_count=len(results['rejected_mutations']),limits='Trusted verifier, mutation suite, interpreter and OS; not hostile-code sandboxing or theorem proof.')
print(json.dumps(results,indent=2,sort_keys=True))
