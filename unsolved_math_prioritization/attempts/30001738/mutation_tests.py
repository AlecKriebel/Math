"""Use only after this script and the verifier were independently authenticated."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('Use python -I -S -B mutation_tests.py PIN PACKET')
from pathlib import Path
import hashlib,json,shutil,subprocess,tempfile

def require(ok,message):
    if not ok:raise RuntimeError(message)
def digest(b):return hashlib.sha256(b).hexdigest()
def snapshot(root):return {p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
def run(script,packet,pin,optimization):
    return subprocess.run([sys.executable,'-I','-S','-B',*(['-O']*optimization),str(script),pin,str(packet)],capture_output=True,timeout=180)
def repin(packet):
    p=packet/'PUBLIC_MANIFEST.json';j=json.loads(p.read_bytes())
    for row in j['files']:
        f=packet/row['path']
        if f.is_file():
            b=f.read_bytes();row.update(bytes=len(b),sha256=digest(b))
    raw=(json.dumps(j,indent=2,sort_keys=True)+'\n').encode();p.write_bytes(raw);return digest(raw)
require(len(sys.argv)==3,'Expected pin and packet')
pin=sys.argv[1];root=Path(sys.argv[2]).absolute();original=snapshot(root)
results={'problem_id':30001738,'passing_replays':[],'rejected_mutations':[]}
with tempfile.TemporaryDirectory(prefix='unitary-mutations-') as td:
    base=Path(td);trusted=base/'trusted_verify.py';trusted.write_bytes(original['verify_publication.py'])
    relocated=base/'relocated';shutil.copytree(root,relocated)
    for name,packet in [('original',root),('relocated',relocated)]:
        for opt in (0,1,2):
            r=run(trusted,packet,pin,opt);require(r.returncode==0,name+' failed: '+r.stderr.decode())
            j=json.loads(r.stdout);require(j['status']=='pass' and j['python_optimization']==opt and j['author_checks']==3044 and j['audit_integrity_rejections']==22 and j['audit_semantic_rejections']==16,'Invalid replay receipt')
            results['passing_replays'].append({'case':name,'optimization':opt,'status':'pass'})
    labels=['payload','extra_hidden','missing','empty_directory','payload_symlink','manifest_symlink','root_symlink','wrong_pin','manifest_byte','archive_byte','verifier_byte','duplicate_inventory','traversal_inventory','absolute_inventory','duplicate_json_key','laundered_frozen_report','laundered_frozen_manifest']
    for label in labels:
        packet=base/label;shutil.copytree(root,packet);test_pin=pin
        if label=='payload':(packet/'ACCEPTANCE.md').write_bytes(original['ACCEPTANCE.md']+b'!')
        elif label=='extra_hidden':(packet/'.unlisted').write_bytes(b'x')
        elif label=='missing':(packet/'README.md').unlink()
        elif label=='empty_directory':(packet/'extra').mkdir()
        elif label in ('payload_symlink','manifest_symlink'):
            name='README.md' if label=='payload_symlink' else 'PUBLIC_MANIFEST.json';(packet/name).unlink();(packet/name).symlink_to(root/name)
        elif label=='root_symlink':
            linked=base/'linked_root';linked.symlink_to(packet,target_is_directory=True);packet=linked
        elif label=='wrong_pin':test_pin='0'*64
        elif label=='manifest_byte':(packet/'PUBLIC_MANIFEST.json').write_bytes(original['PUBLIC_MANIFEST.json']+b' ')
        elif label=='archive_byte':(packet/'AUDIT_PACKET.zip').write_bytes(original['AUDIT_PACKET.zip']+b'!')
        elif label=='verifier_byte':(packet/'verify_publication.py').write_bytes(b'print("pass")\n')
        elif label=='duplicate_json_key':
            b=original['PUBLIC_MANIFEST.json'];b=b.replace(b'{',b'{"problem_id":30001738,',1);(packet/'PUBLIC_MANIFEST.json').write_bytes(b);test_pin=digest(b)
        elif label.startswith('laundered_'):
            name='author/REPORT.md' if label.endswith('report') else 'author/MANIFEST.json';(packet/name).write_bytes(original[name]+b' ');test_pin=repin(packet)
        else:
            j=json.loads(original['PUBLIC_MANIFEST.json'])
            if label=='duplicate_inventory':j['files'][-1]=j['files'][0]
            elif label=='traversal_inventory':j['files'][0]['path']='../outside'
            else:j['files'][0]['path']='/tmp/outside'
            b=(json.dumps(j,indent=2)+'\n').encode();(packet/'PUBLIC_MANIFEST.json').write_bytes(b);test_pin=digest(b)
        for opt in (0,1,2):
            r=run(trusted,packet,test_pin,opt)
            require(r.returncode!=0 and r.stderr.startswith(b'REJECTED: '),'Mutation accepted: '+label)
            results['rejected_mutations'].append({'case':label,'optimization':opt,'status':'rejected','diagnostic':r.stderr.decode().strip()})
require(snapshot(root)==original,'Original changed')
results.update(status='pass',original_preserved=True,passing_replay_count=6,rejected_mutation_count=51,limits='Trusted interpreter and OS; not a hostile-code sandbox or theorem proof.')
print(json.dumps(results,indent=2,sort_keys=True))
