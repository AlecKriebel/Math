"""Independent packet tests. Standard library only; never modifies the input packet.
Usage: python -I -S -B replay_audit.py AUTHOR_DIRECTORY AUTHOR_ZIP
"""
import sys
if not (sys.flags.isolated and sys.flags.no_site):
    raise SystemExit('Use python -I -S -B replay_audit.py AUTHOR_DIRECTORY AUTHOR_ZIP')
from pathlib import Path
from hashlib import sha256
import json, shutil, subprocess, tempfile, zipfile
MANIFEST_PIN='56c934a8949d90e0558849578e1421826b9e66520c0a9899a8745eebe7223ef2'
VERIFIER_PIN='ac53854fdf7f99f902da3461929d03dec1c31c2891afa9df96bfc56efe9153fb'
ARCHIVE_PIN='02a24cc8994a462d65de1471ba73a7d2cca63b51e3f562278db9866d9012ee58'
def require(ok,msg):
    if not ok: raise RuntimeError(msg)
def digest(b): return sha256(b).hexdigest()
def run(verifier,packet,pin=MANIFEST_PIN,optimized=False):
    cmd=[sys.executable,'-I','-S','-B']+(['-O'] if optimized else [])
    p=subprocess.run(cmd+[str(verifier),pin,str(packet)],capture_output=True,text=True)
    return {'returncode':p.returncode,'stdout':p.stdout,'stderr':p.stderr}
if len(sys.argv)!=3: raise SystemExit(__doc__)
root=Path(sys.argv[1]).resolve(); archive=Path(sys.argv[2]).resolve()
original={p.name:p.read_bytes() for p in root.iterdir() if p.is_file() and not p.is_symlink()}
require(digest(original['MANIFEST.json'])==MANIFEST_PIN,'manifest pin')
require(digest(original['verify.py'])==VERIFIER_PIN,'verifier pin')
require(digest(archive.read_bytes())==ARCHIVE_PIN,'archive pin')
manifest=json.loads(original['MANIFEST.json'])
require(set(original)=={r['path'] for r in manifest['files']}|{'MANIFEST.json'},'inventory')
for r in manifest['files']:
    require(len(original[r['path']])==r['bytes'] and digest(original[r['path']])==r['sha256'],'payload')
with zipfile.ZipFile(archive) as z:
    require(len(z.namelist())==len(set(z.namelist())),'duplicate archive entries')
    require(set(z.namelist())==set(original),'archive names')
    require(z.testzip() is None,'archive CRC')
    for name in z.namelist(): require(z.read(name)==original[name],'archive payload')
results={'schema':'independent-galois-multiplicity-audit-v1','problem_id':30001738,
         'author_manifest_sha256':MANIFEST_PIN,'author_verifier_sha256':VERIFIER_PIN,
         'author_archive_sha256':ARCHIVE_PIN,'archive_bytes':archive.stat().st_size,
         'packet_files':len(original),'replays':[],'integrity_mutations':[],'semantic_mutations':[]}
with tempfile.TemporaryDirectory(prefix='galois-audit-') as td:
    base=Path(td); verifier=base/'trusted_verify.py';verifier.write_bytes(original['verify.py'])
    relocated=base/'packet';shutil.copytree(root,relocated)
    for label,packet,opt in [('original',root,False),('optimized',root,True),('relocated',relocated,False)]:
        r=run(verifier,packet,optimized=opt)
        require(r['returncode']==0,label+' replay')
        receipt=json.loads(r['stdout'])
        require(receipt['controls']['checks']==3044 and receipt['controls']['synthetic_multiset_patterns']==494,'receipt counters')
        results['replays'].append({'case':label,'status':'pass','receipt':receipt})
    def fresh(name):
        dest=base/name;shutil.copytree(root,dest);return dest
    def repin(packet):
        j=json.loads((packet/'MANIFEST.json').read_bytes())
        for row in j['files']:
            p=packet/row['path']
            if p.is_file():
                b=p.read_bytes();row.update(bytes=len(b),sha256=digest(b))
        raw=(json.dumps(j,sort_keys=True,indent=2)+'\n').encode();(packet/'MANIFEST.json').write_bytes(raw)
        return digest(raw)
    for label in ['payload','extra_hidden','missing','directory','payload_symlink','manifest_symlink','wrong_pin','manifest_byte','receipt_semantics','duplicate_inventory','traversal_inventory']:
        packet=fresh('integrity_'+label);pin=MANIFEST_PIN
        if label=='payload': (packet/'REPORT.md').write_bytes(original['REPORT.md']+b'!')
        elif label=='extra_hidden': (packet/'.extra').write_bytes(b'x')
        elif label=='missing': (packet/'README.md').unlink()
        elif label=='directory': (packet/'extra').mkdir()
        elif label=='payload_symlink':
            (packet/'REPORT.md').unlink();(packet/'REPORT.md').symlink_to(root/'REPORT.md')
        elif label=='manifest_symlink':
            (packet/'MANIFEST.json').unlink();(packet/'MANIFEST.json').symlink_to(root/'MANIFEST.json')
        elif label=='wrong_pin': pin='0'*64
        elif label=='manifest_byte': (packet/'MANIFEST.json').write_bytes(original['MANIFEST.json']+b' ')
        elif label=='receipt_semantics':
            j=json.loads(original['CONTROL_RECEIPT.json']);j['checks']+=1
            (packet/'CONTROL_RECEIPT.json').write_text(json.dumps(j));pin=repin(packet)
        else:
            j=json.loads(original['MANIFEST.json'])
            if label=='duplicate_inventory': j['files'].append(j['files'][0])
            else: j['files'][0]['path']='../CONTROL_RECEIPT.json'
            raw=json.dumps(j).encode();(packet/'MANIFEST.json').write_bytes(raw);pin=digest(raw)
        for opt in (False,True):
            r=run(verifier,packet,pin,optimized=opt)
            require(r['returncode']!=0,'accepted integrity mutation '+label)
            results['integrity_mutations'].append({'case':label,'optimized':opt,'status':'rejected','diagnostic':(r['stderr'] or r['stdout']).strip().splitlines()[-1]})
    mutations={
      'distinct_fixed_factors':('fixed = sum(TAU[x] == x for x in labels)','fixed = sum(TAU[x] == x for x in set(labels))'),
      'all_factors_fixed':('fixed = sum(TAU[x] == x for x in labels)','fixed = len(labels)'),
      'remove_stability_gate':('degree = (1 << fixed) if stable else 0','degree = (1 << fixed)'),
      'swap_orbit_multiplicities':('per_orbit = ((degree + 1)//2, degree//2)','per_orbit = (degree//2, (degree + 1)//2)'),
      'residue_ring_not_field':('x[0]*y[0]-x[1]*y[1]','x[0]*y[0]+x[1]*y[1]'),
      'fiber_quartic_sign':('p[d-2]+=4*c','p[d-2]-=4*c'),
      'twist_coefficient_conjugation':('3*log[x]%8','7*log[x]%8'),
      'delete_scope_guard':('if scope != SCOPE:','if False:')}
    src=original['controls.py'].decode()
    for label,(old,new) in mutations.items():
        require(src.count(old)==1,'mutation target not unique '+label)
        packet=fresh('semantic_'+label);(packet/'controls.py').write_text(src.replace(old,new));pin=repin(packet)
        for opt in (False,True):
            r=run(verifier,packet,pin,optimized=opt)
            require(r['returncode']!=0,'accepted semantic mutation '+label)
            results['semantic_mutations'].append({'case':label,'optimized':opt,'status':'rejected','diagnostic':(r['stderr'] or r['stdout']).strip().splitlines()[-1]})
require({p.name:p.read_bytes() for p in root.iterdir()}==original,'original packet changed')
results.update(status='pass',original_preserved=True,limits='Trusted interpreter and OS; diagnostics do not prove infinite-dimensional multiplicities or the cited analytic theorem.')
print(json.dumps(results,indent=2,sort_keys=True))
