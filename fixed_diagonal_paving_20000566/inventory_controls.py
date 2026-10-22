"""Negative tests on disposable copies; never modify the verified package."""
import sys
sys.dont_write_bytecode=True
import json,shutil,tempfile
from pathlib import Path
from verify import verify
ROOT=Path(__file__).parent

def main():
    verify(ROOT)
    outcomes=[]
    for label in ['extra_file','nested_manifest','symlink_file','symlink_directory','unsafe_parent','unsafe_absolute','unsafe_backslash','duplicate_entry','missing_file','changed_bytes','empty_unlisted_directory','listed_nested_manifest','symlink_manifest']:
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)/'package';shutil.copytree(ROOT,root)
            mp=root/'MANIFEST.json';m=json.loads(mp.read_text())
            if label=='symlink_manifest':
                external=Path(td)/'external.json';external.write_bytes(mp.read_bytes());mp.unlink();mp.symlink_to(external)
            elif label=='listed_nested_manifest':
                m['files'].append({'path':'nested/MANIFEST.json','bytes':2,'sha256':'0'*64});mp.write_text(json.dumps(m))
            elif label=='extra_file':(root/'EXTRA.txt').write_text('unexpected')
            elif label=='nested_manifest':
                (root/'nested').mkdir();(root/'nested/MANIFEST.json').write_text('{}')
            elif label=='symlink_file':(root/'link.txt').symlink_to(root/'README.md')
            elif label=='symlink_directory':(root/'linked').symlink_to(root/'outputs',target_is_directory=True)
            elif label.startswith('unsafe_'):
                m['files'][0]['path']={'unsafe_parent':'../outside','unsafe_absolute':'/outside','unsafe_backslash':'dir\\outside'}[label];mp.write_text(json.dumps(m))
            elif label=='duplicate_entry':m['files'].append(m['files'][0]);mp.write_text(json.dumps(m))
            elif label=='missing_file':(root/m['files'][0]['path']).unlink()
            elif label=='changed_bytes':(root/'README.md').write_text('tampered')
            elif label=='empty_unlisted_directory':(root/'unlisted').mkdir()
            try:verify(root)
            except RuntimeError as exc:
                expected={'extra_file':'unlisted EXTRA.txt','nested_manifest':'nested manifest','symlink_file':'symlink link.txt','symlink_directory':'symlink linked','unsafe_parent':'unsafe path','unsafe_absolute':'unsafe path','unsafe_backslash':'unsafe path','duplicate_entry':'duplicate entry','missing_file':'missing inventory member','changed_bytes':'content mismatch README.md','empty_unlisted_directory':'unexpected or missing directory','listed_nested_manifest':'nested or self manifest','symlink_manifest':'manifest type'}[label]
                if str(exc)!=expected:raise RuntimeError('wrong failure for '+label+': '+str(exc))
                outcomes.append({'attack':label,'detected':True,'reason':str(exc)})
            else:raise RuntimeError('inventory attack accepted: '+label)
    return {'status':'PASS','optimized':bool(sys.flags.optimize),'attacks':outcomes}
if __name__=='__main__':print(json.dumps(main(),indent=2))
