#!/usr/bin/env python3
"""Check frozen-packet verifier rejects three isolated temporary mutations."""
import json,pathlib,shutil,subprocess,sys,tempfile
p=pathlib.Path(sys.argv[1]).resolve() if len(sys.argv)>1 else pathlib.Path(__file__).resolve().parent.parent/'submission'
results={}
for mutation in ['changed_content','extra_file','extra_directory']:
    with tempfile.TemporaryDirectory(prefix='rank650-audit-') as td:
        copy=pathlib.Path(td)/'packet'; shutil.copytree(p,copy)
        if mutation=='changed_content':
            with (copy/'README.md').open('ab') as f:f.write(b'\nAUDIT TEMPORARY MUTATION\n')
        elif mutation=='extra_file':(copy/'unexpected.txt').write_text('audit test')
        else:(copy/'unexpected').mkdir()
        run=subprocess.run([sys.executable,str(copy/'verify_manifest.py')],capture_output=True,text=True)
        assert run.returncode!=0,(mutation,'mutation not detected')
        results[mutation]='rejected as expected'
print(json.dumps({'author_manifest_negative_controls':results,'original_files_modified':False},indent=2,sort_keys=True))
