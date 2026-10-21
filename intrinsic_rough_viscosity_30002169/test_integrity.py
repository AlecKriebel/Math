"""Isolated integrity corruption checks; not theorem verification."""
import json,pathlib,shutil,subprocess,sys,tempfile
ROOT=pathlib.Path(__file__).resolve().parent

def run(root,opt):
    return subprocess.run([sys.executable,'-B']+(['-O'] if opt else [])+[str(root/'verify_manifest.py')],capture_output=True,text=True).returncode

def mutate(root,case):
    target=root/'RESEARCH.md'
    mpath=root/'MANIFEST.json'
    if case=='changed_bytes':target.write_bytes(target.read_bytes()+b'\nTAMPER\n')
    elif case=='same_size_changed_bytes':
        b=target.read_bytes();target.write_bytes(bytes([b[0]^1])+b[1:])
    elif case=='missing_file':target.unlink()
    elif case=='extra_file':(root/'unexpected.txt').write_text('extra')
    elif case=='symlink':(root/'unexpected_link').symlink_to('RESEARCH.md')
    else:
        m=json.loads(mpath.read_text())
        if case=='duplicate_path':m['files'].append(m['files'][0])
        elif case=='traversal_path':m['files'][0]['path']='../outside'
        elif case=='wrong_total':m['total_bytes_excluding_manifest']+=1
        else:raise RuntimeError('Unknown test')
        mpath.write_text(json.dumps(m))

def main():
    results=[]
    for opt in (False,True):
        if run(ROOT,opt)!=0:raise RuntimeError('Clean package rejected')
        for case in ('changed_bytes','same_size_changed_bytes','missing_file','extra_file','symlink','duplicate_path','traversal_path','wrong_total'):
            with tempfile.TemporaryDirectory(prefix='rough_integrity_') as tmp:
                copy=pathlib.Path(tmp)/'package';shutil.copytree(ROOT,copy)
                mutate(copy,case)
                if run(copy,opt)==0:raise RuntimeError('Corruption accepted: '+case)
                results.append({'mode':'optimized' if opt else 'normal','case':case,'result':'REJECTED'})
    print(json.dumps({'status':'PASS','clean_modes':2,'negative_controls':results},indent=2))
if __name__=='__main__':main()
