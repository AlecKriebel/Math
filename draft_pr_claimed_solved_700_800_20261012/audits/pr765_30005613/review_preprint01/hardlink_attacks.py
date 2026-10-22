"""Reproduce two regular-output hardlink attacks on disposable input copies."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile


def main():
    root = Path(__file__).resolve().parent
    package = root.parent/'preprint'
    scratch = root/'tmp/hardlink_attacks'
    scratch.mkdir(parents=True, exist_ok=False)
    rows = []
    try:
        for name, relative in [('regular_output_hardlink','zenodo-metadata.json'),
                               ('receipt_hardlink','PACKAGE_INVENTORY.json')]:
            work = scratch/name
            source, out = work/'input', work/'out'
            with zipfile.ZipFile(package/'source-and-verification.zip') as z:
                for n in z.namelist():
                    if Path(n).is_absolute() or '..' in Path(n).parts:
                        raise ValueError('Unsafe ZIP path')
                z.extractall(source)
            out.mkdir()
            before = (source/'paper.tex').read_bytes()
            os.link(source/'paper.tex',out/relative)
            cmd = [sys.executable,'-O','-B',str(source/'build_package.py'),
                   '--output-dir',str(out),'--pdf',str(package/'output/pdf/paper.pdf')]
            run = subprocess.run(cmd,cwd='/',capture_output=True,text=True,timeout=60)
            after = (source/'paper.tex').read_bytes()
            rows.append({'case':name,'command':cmd,'initial_same_inode':True,
                         'target':relative,'returncode':run.returncode,
                         'input_paper_tex_unchanged':before==after,
                         'before_sha256':hashlib.sha256(before).hexdigest(),
                         'after_sha256':hashlib.sha256(after).hexdigest(),
                         'after_bytes':len(after),'stderr':run.stderr})
            shutil.rmtree(work)
    finally:
        shutil.rmtree(scratch)
    result = {'utc':datetime.now(timezone.utc).isoformat(),
              'status':'PASS_REJECTION_AND_PRESERVATION' if all(x['returncode'] != 0 and x['input_paper_tex_unchanged'] for x in rows) else 'FAIL_HARDLINK_CLOSED_INPUT_PRESERVATION',
              'cases':rows,'scope':'Own disposable copies only; frozen input untouched.'}
    (root/'OUTPUT_HARDLINK_ATTACK.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
