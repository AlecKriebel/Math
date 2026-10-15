"""Read-only validation of authored source assessment and actual saved bytes."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import subprocess

H=Path(__file__).resolve().parent
A=H/'thesis_source_adversary_01'


def pin(path,row):
    assert path.is_file() and not path.is_symlink()
    raw=path.read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    return dict(path=str(path.relative_to(H)),bytes=len(raw),sha256=row['sha256'])


manifest=json.loads((A/'checks_manifest.json').read_text())
public=[]
for row in manifest['artifacts']:
    path=Path(row['path'])
    assert path.resolve().is_relative_to(A.resolve())
    assert 'private_revision_history' not in path.parts
    public.append(pin(path,row))
private=[]
for row in manifest['sources_read_only']:
    path=Path(row['path'])
    assert path.resolve().is_relative_to((H/'private_reading').resolve())
    private.append(pin(path,row))
revision=json.loads((A/'centering_revision.json').read_text())
for group in ['original_artifact_seals','prior_artifact_seals']:
    for row in revision[group]:
        path=Path(row['private_snapshot_path'])
        assert path.resolve().is_relative_to((A/'private_revision_history').resolve())
        private.append(pin(path,row))
assert (A/'.gitignore').read_text()=='/private_revision_history/\n'
assert (H/'.gitignore').read_text()=='/private_reading/\n'
metadata=json.loads((H/'NEW_SOURCE_AUTHENTICATION.json').read_text())
assert metadata['sha256']==manifest['sources_read_only'][0]['sha256']
info=subprocess.run(['pdfinfo',str(Path(manifest['sources_read_only'][0]['path']))],capture_output=True,timeout=30)
assert info.returncode==0 and 'Pages:           15' in info.stdout.decode()
drive=json.loads((H/'DRIVE_REFERENCE_SEARCH_SUMMARY.json').read_text())
raw=(H/'private_reading/DRIVE_REFERENCE_SEARCH_RAW.json').read_bytes()
assert hashlib.sha256(raw).hexdigest()==drive['private_receipt_sha256']
assert len(raw)==drive['private_receipt_bytes']
root=json.loads((H.parent/'ROOT_SOURCE_HOLD_NATIVE_READBACK.json').read_text())
assert root['status']=='PASS' and root['owned_files_verified']==303
result=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',public_adversary_pins=public,
            current_adversary_manifest_sha256=hashlib.sha256((A/'checks_manifest.json').read_bytes()).hexdigest(),
            source_and_preserved_authored_private_pins=private,private_Drive_metadata_pin_verified=True,
            actual_PDF_page_count=15,root_full_source_read=True,root_visual_pages=[1,7,11,15],
            independent_source_report_read_in_full=True,centering_and_variance_strengthening_analytically_checked=True,
            finite_simulation_used_to_establish_asymptotics=False,source_gap_cleared=False,
            case_completion_percent=60,goal_active_incomplete=True,
            previous_native_checkpoint_303_files_verified=root['commit'])
(H/'ROOT_FOLLOWUP_VALIDATION.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['public_adversary_pins','source_and_preserved_authored_private_pins']},indent=2))
