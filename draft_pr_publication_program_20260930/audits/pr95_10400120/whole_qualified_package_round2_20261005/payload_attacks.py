from review_tools import *
import shutil, zipfile
root=A/'attack_payload';root.mkdir()
with zipfile.ZipFile(Q/'publicfiles/pr95_support.zip')as z:z.extractall(root)
baseline={str(p.relative_to(root)):sha(p)for p in root.rglob('*')if p.is_file()}
manifest=root/'PAYLOAD_MANIFEST.json';original_manifest=manifest.read_bytes()
results=[]
def test(case,expected,details=None):
    manifest_hash=sha(manifest)
    for mode,flags in [('normal',[]),('optimized',['-O'])]:
        output=A/('forbidden_output_'+case+'_'+mode)
        if output.exists():raise RuntimeError('unexpected stale output')
        r=run('payload_'+case+'_'+mode,[PY,'-E','-B']+flags+[root/'verification/run_all.py','--output-dir',output],root,[root/'verification/run_all.py',manifest])
        f=A/'processes'/r['label'];err=(f/'stderr.bin').read_text()
        passed=r['exit_code']!=0 and expected in err and (f/'stdout.bin').stat().st_size==0 and not output.exists()
        results.append({'case':case,'mode':mode,'pass':passed,'expected_guard':expected,'actual_exit':r['exit_code'],'output_created':output.exists(),'manifest_sha256':manifest_hash,'details':details})
        if not passed:raise RuntimeError('attack not precisely rejected '+case+' '+mode+' '+err)
def clean():
    current={str(p.relative_to(root)):sha(p)for p in root.rglob('*')if p.is_file()}
    if current!=baseline:raise RuntimeError('fixture restoration failed')
    if any(p.is_symlink()for p in root.rglob('*')):raise RuntimeError('fixture link remains')
test('valid_output_inside','output must be outside supplied package') if False else None
# The critical R1 control changes no declared contents. Move, then link back.
saved=A/'unchanged_recorded_processes';(root/'verification/recorded_processes').rename(saved)
(root/'verification/recorded_processes').symlink_to(saved,target_is_directory=True)
identity=all(sha(root/name)==digest for name,digest in baseline.items())
if not identity:raise RuntimeError('ancestor contents changed')
test('ancestor_symlink','symlinked payload path component: verification/recorded_processes/',{'all_declared_content_hashes_unchanged':True,'ancestor':'verification/recorded_processes','link_target':str(saved)})
(root/'verification/recorded_processes').unlink();saved.rename(root/'verification/recorded_processes');clean()
# A second nested directory component and a leaf exercise both boundaries.
sub=root/'verification/recorded_processes/verify_positive_normal';saved=A/'unchanged_leaf_record_directory';sub.rename(saved);sub.symlink_to(saved,target_is_directory=True)
test('nested_ancestor_symlink','[verify_positive_normal]',{'all_declared_content_hashes_unchanged':all(sha(root/name)==digest for name,digest in baseline.items())})
sub.unlink();saved.rename(sub);clean()
leaf=root/'README.md';saved=A/'unchanged_README.md';leaf.rename(saved);leaf.symlink_to(saved)
test('leaf_symlink','symlinked payload path component: README.md [README.md]')
leaf.unlink();saved.rename(leaf);clean()
old=leaf.read_bytes();leaf.write_bytes(old+b'\nchanged\n');test('changed_bytes','payload hash mismatch: README.md');leaf.write_bytes(old);clean()
leaf.rename(saved);test('missing_member','missing payload: README.md');saved.rename(leaf);clean()
for case,edit,expected in [
    ('duplicate',lambda d:d['files'].append(d['files'][0]),'duplicate payload member'),
    ('unsafe_parent',lambda d:d['files'].append({'file':'../escape','bytes':0,'sha256':'0'*64}),'unsafe payload path'),
    ('absolute',lambda d:d['files'].append({'file':'/tmp/escape','bytes':0,'sha256':'0'*64}),'unsafe payload path'),
    ('wrong_schema',lambda d:d.update(schema='wrong'),'wrong payload schema')]:
    d=json.loads(original_manifest);edit(d);dump(manifest,d);test(case,expected);manifest.write_bytes(original_manifest);clean()
script=root/'verification/independent_checks.py';old=script.read_bytes();script.write_bytes(old+b'\nassert True\n')
d=json.loads(original_manifest)
for e in d['files']:
    if e['file']=='verification/independent_checks.py':e.update(bytes=script.stat().st_size,sha256=sha(script))
dump(manifest,d);test('removable_assert_after_rehash','removable validation assertion: independent_checks.py',{'modified_manifest_is_not_authentication':True})
script.write_bytes(old);manifest.write_bytes(original_manifest);clean()
dump(A/'PAYLOAD_ATTACKS.json',{'UTC':utc(),'all_pass':all(r['pass']for r in results),'controls':results,'critical_R1':'Identical content through linked ancestor precisely rejected before any output creation; no dependency import failure.'})
