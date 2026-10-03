from pathlib import Path
import hashlib,json,subprocess
A=Path(__file__).resolve().parent;R=A.parents[2];K='unsolved_math_prioritization/attempts/30004386/';Q='unsolved_math_prioritization/QUEUE.md'
def main():
    assert __debug__
    p=json.loads((A/'integration_preflight.json').read_bytes());o=json.loads((A/'integration_check.json').read_bytes())
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==p['main_before']
    assert subprocess.check_output(['git','rev-parse','MERGE_HEAD'],cwd=R).decode().strip()=='86be0f85c7a37a5cad8d24abd16a32d8d1f27e62'
    rows=o['canonical_overlay_files'];assert len(rows)==355
    for z in rows:
        b=(R/K/z['path']).read_bytes();assert len(b)==z['bytes']and hashlib.sha256(b).hexdigest()==z['sha256']
    b=(R/Q).read_bytes();assert hashlib.sha256(b).hexdigest()==o['whole_queue_after_sha256']
    assert set(subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R).decode().splitlines())=={K+z['path']for z in json.loads((A/'snapshot_manifest.json').read_bytes())['files']}|{Q}
    subprocess.run(['git','add','--',Q]+[K+z['path']for z in rows],cwd=R,check=True)
    assert set(subprocess.check_output(['git','diff','--cached','--name-only'],cwd=R).decode().splitlines())=={K+z['path']for z in rows}|{Q}
    assert not subprocess.check_output(['git','diff','--name-only','--diff-filter=U'],cwd=R)
    print('PASS: exact355 reviewed canonical members and one queue; no unrelated staged member.')
if __name__=='__main__':main()
