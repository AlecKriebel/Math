"""Read-only candidate/package audit; owned extraction and JSON outputs only."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib, json, stat, zipfile

O = Path(__file__).resolve().parent
B = O.parent / 'preprint'
F = json.loads((O/'FROZEN_INPUTS.json').read_text())
checks = []
def ck(name, cond):
    assert cond, name
    checks.append(name)
def pin(p):
    raw=p.read_bytes()
    return dict(bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def manifest(p, base):
    obj=json.loads(p.read_text()); paths=[]
    for r in obj['files']:
        rel=PurePosixPath(r['path']); f=base.joinpath(*rel.parts)
        ck('safe_manifest_'+str(p.relative_to(B))+':'+r['path'], not rel.is_absolute() and '..' not in rel.parts and f.resolve().is_relative_to(base.resolve()) and not f.is_symlink())
        ck('manifest_bytes_'+r['path'], pin(f)=={k:r[k] for k in ('bytes','sha256')})
        paths.append(r['path'])
    ck('unique_manifest_'+str(p), len(paths)==len(set(paths)))
    return set(paths)
for r in F['all_candidate_files']:
    ck('frozen_'+r['path'], pin(B/r['path'])=={k:r[k] for k in ('bytes','sha256')})
sm=manifest(B/'SOURCE_MANIFEST.json', B)
vm=manifest(B/'verification/MANIFEST.json', B/'verification')
np=B/'pr_update/5100015'
nm=manifest(np/'MANIFEST.json',np)
cm=manifest(np/'CURRENT_PACKET_MANIFEST.json',np)
ck('native_current_exact_members', cm=={p.relative_to(np).as_posix() for p in np.rglob('*') if p.is_file() and p.name!='CURRENT_PACKET_MANIFEST.json'})
ck('native_top_exact_members', nm=={p.name for p in np.iterdir() if p.is_file() and p.name not in {'MANIFEST.json','CURRENT_PACKET_MANIFEST.json'}})
ck('verification_exact_members', vm=={p.relative_to(B/'verification').as_posix() for p in (B/'verification').rglob('*') if p.is_file() and p.name!='MANIFEST.json'})
pm=json.loads((B/'PACKAGE_MANIFEST.json').read_text())
for r in pm['submission_files']+[pm['source_manifest'],pm['manuscript_source'],pm['metadata']]:
    ck('package_'+r['path'], pin(B/r['path'])=={k:r[k] for k in ('bytes','sha256')})
dep=json.loads((B/'deposit.json').read_text())
ck('deposit_exact_metadata', dep['metadata']==json.loads((B/'metadata.json').read_text()))
ck('deposit_files', {x['path'] for x in dep['files']}=={x['path'] for x in pm['submission_files']})
originals=json.loads((B/'PREPARATION_RECEIPT.json').read_text())['original_pins']
src=O.parent/'initial_review_20261016/submitted/unsolved_math_prioritization/attempts/5100015'
for r in originals:
    for base in [src, B/'verification/original_submission',np/'history/original_submission_20261016']:
        ck('original23_'+str(base)+':'+r['path'],pin(base/r['path'])=={k:r[k] for k in ('bytes','sha256')})
ck('originals_count23',len(originals)==23)
prefix='k303b_outer_center_pedal_product/'
extract=O/'actual_zip_extraction'
ck('new_extraction',not extract.exists())
with zipfile.ZipFile(B/'k303b-source-verification.zip') as z:
    infos=z.infolist();names=[i.filename for i in infos]
    ck('zip_unique211',len(names)==211 and len(names)==len(set(names))==pm['source_archive_entries'])
    ck('zip_crc',z.testzip() is None)
    rels=set()
    for i in infos:
        n=PurePosixPath(i.filename)
        ck('zip_safe_'+i.filename,i.filename.startswith(prefix) and not n.is_absolute() and '..' not in n.parts and '\\' not in i.filename and stat.S_ISREG(i.external_attr>>16) and not (i.flag_bits&1))
        rel=i.filename[len(prefix):];rels.add(rel)
        ck('zip_equal_source_'+rel,z.read(i)==(B/rel).read_bytes())
    ck('zip_exact_manifest_members',rels==sm|{'SOURCE_MANIFEST.json'})
    for i in infos:
        target=extract/i.filename;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(z.read(i))
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',checks=len(checks),zip_members=211,source_files=len(sm),verification_files=len(vm),current_native_files=len(cm),original23_copies_verified=3,extraction=str(extract/prefix))
(O/'BYTE_AUDIT.json').write_text(json.dumps(result,indent=2)+'\n')
with (O/'RESEARCH_LOG.md').open('a') as f:f.write(f"\n- {result['utc']}: Package/source/native/verification manifests, all 211 ZIP member bytes and safety, 23 originals in actual submitted source and both archives verified ({len(checks)} checks). Extracted actual reviewed ZIP into owned folder for offline replay. Case estimate 55%.\n")
print(json.dumps(result,indent=2))
