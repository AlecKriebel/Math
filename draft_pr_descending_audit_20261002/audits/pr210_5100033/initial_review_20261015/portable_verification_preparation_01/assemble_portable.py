from pathlib import Path
import hashlib,json,shutil
from datetime import datetime,timezone
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent
DEST=SOURCE.parent/'preprint/verification'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def copy(src,dst):
    dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
intake=json.loads((SOURCE/'INTAKE.json').read_text())
original=[]
for rec in intake['original_source_files']:
    src=SOURCE/'submitted'/rec['native_path']
    assert src.stat().st_size==rec['bytes'] and sha(src)==rec['sha256']
    rel=Path(rec['native_path']).relative_to('unsolved_math_prioritization/attempts/5100033')
    copy(src,DEST/'original_submission'/rel)
    original.append({**rec,'portable_path':str(Path('original_submission')/rel)})
families=[]
for name in ['source_domain_adversary_01','physical_geometry_adversary_01','meromorphic_divisor_adversary_01','priority_author_updates_01','priority_classical_general_01']:
    source=SOURCE/name;manifest=source/'AUTHORED_MANIFEST.json';data=json.loads(manifest.read_text());rows=data.get('authored_files',data.get('files'))
    assert isinstance(rows,list)
    for rec in rows:
        rel=Path(rec['path']);assert not rel.is_absolute() and '..' not in rel.parts
        src=source/rel;assert src.stat().st_size==rec['bytes'] and sha(src)==rec['sha256'],str(src)
        copy(src,DEST/'audits'/name/rel)
    copy(manifest,DEST/'audits'/name/'AUTHORED_MANIFEST.json')
    families.append({'family':name,'authored_file_count':len(rows),'manifest_sha256':sha(manifest),'manifest_path':str(Path('audits')/name/'AUTHORED_MANIFEST.json')})
receipts=['INTAKE.json','ORIGINAL_NATIVE_PR_CLAIMS.json','ROOT_AUTHOR_REPLAY_ACCEPTANCE.json','ROOT_MATHEMATICAL_SOURCE_ACCEPTANCE.json','ROOT_PRIORITY_ACCEPTANCE.json','ROOT_SOURCE_FAMILY_REPLAY.json','ROOT_PHYSICAL_GEOMETRY_FAMILY_REPLAY.json','ROOT_MEROMORPHIC_FAMILY_REPLAY.json','ROOT_PRIORITY_AUTHOR_FAMILY_REPLAY.json','ROOT_PRIORITY_CLASSICAL_FAMILY_REPLAY.json','ROOT_SOURCE_READING_PROVENANCE.json','ROOT_V1_TABLE_VISUAL_PROVENANCE.json','ROOT_NATIVE_CHANGED_PATH_AUDIT.json','UPSTREAM_PROVENANCE_RECEIPT.json','ROOT_INITIAL_RECONSTRUCTION.md','ROOT_DIVISOR_RECONSTRUCTION.md','ROOT_SOURCE_AND_EXACT_GEOMETRY_AUDIT.md','ROOT_PRIORITY_INITIAL_MAP.md','ROOT_CLASSICAL_BRIDGE_RECONSTRUCTION.md','ROOT_PRIORITY_PROGRESS_LEDGER.json','PRESENTATION_REPAIR_LEDGER.json','ROOT_POLARITY_SIGN_CORRECTION.json']
for name in receipts:copy(SOURCE/name,DEST/'audit_receipts'/name)
for name in ['root_exact_geometry_controls.py','ROOT_EXACT_GEOMETRY_CONTROLS.json','root_priority_projective_control.py','ROOT_PRIORITY_PROJECTIVE_CONTROL.json']:
    copy(SOURCE/name,DEST/'scope_controls'/name)
for src in (SOURCE/'history/polarity_sign_intermediate_20261015').iterdir():
    assert src.is_file();copy(src,DEST/'forensic_history/polarity_sign_intermediate_20261015'/src.name)
provenance={'schema':'PR210-portable-provenance-v1','assembled_utc':datetime.now(timezone.utc).isoformat(),'source_head':intake['head'],'problem_id':'5100033','PR':210,'original_files':original,'original_count':len(original),'families':families,'all_original_and_family_payload_hashes_checked':True,'primary_payloads_redistributed':False,'notes':['Absolute private paths in authored provenance receipts are historical locators only; no private payload is present.','The five family manifests bind their original authored payloads; the portable MANIFEST binds the relocated package.','The preserved V1 manifest has one documented superseded SOURCES.md hash; current MANIFEST and all INTAKE hashes match.']}
(DEST/'PROVENANCE.json').write_text(json.dumps(provenance,indent=2)+'\n')
print(json.dumps({'original_files':len(original),'families':families,'root_receipts':len(receipts),'package_files_before_harness':sum(p.is_file() for p in DEST.rglob('*'))},indent=2))
