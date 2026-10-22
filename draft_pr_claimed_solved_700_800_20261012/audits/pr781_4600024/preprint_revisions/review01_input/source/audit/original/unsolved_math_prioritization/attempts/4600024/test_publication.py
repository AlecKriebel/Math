#!/usr/bin/env python3
"""Exercise actual corrupted copies against the externally pinned publication verifier."""
import argparse,json,os,pathlib,shutil,subprocess,sys,tempfile
ROOT=pathlib.Path(__file__).absolute().parent

def run(root,pin):
    cases=['proof','audit','review','source','results','verdict','archive','missing','extra_file','extra_directory','empty_pycache','populated_pycache','raw_pyc','symlink','fifo','malformed_manifest','changed_manifest','duplicate_manifest_key','mirror_author']
    result=[]
    with tempfile.TemporaryDirectory(prefix='block-code-publication-') as td:
        for opt in (False,True):
            for case in cases:
                dst=pathlib.Path(td)/(case+str(opt));shutil.copytree(root,dst)
                names={'proof':'author/PROOF.md','audit':'audit/AUDIT.md','review':'second_review/REVIEW.md','source':'author/verify_math.py','results':'second_review/RESULTS.json','verdict':'VERDICT.json','archive':'archives/BLOCK_CODE_EXTENSION_4600024_AUTHOR_SAFE_FREEZE.zip','mirror_author':'audit/author/PROOF.md'}
                if case in names:
                    p=dst/names[case];p.write_bytes(p.read_bytes()+b'\nMUTATION\n')
                elif case=='missing':(dst/'README.md').unlink()
                elif case=='extra_file':(dst/'extra.txt').write_text('x')
                elif case=='extra_directory':(dst/'extra').mkdir()
                elif case=='empty_pycache':(dst/'__pycache__').mkdir()
                elif case=='populated_pycache':
                    (dst/'__pycache__').mkdir();(dst/'__pycache__/x.pyc').write_bytes(b'x')
                elif case=='raw_pyc':(dst/'x.pyc').write_bytes(b'x')
                elif case=='symlink':
                    (dst/'README.md').unlink();(dst/'README.md').symlink_to('VERDICT.json')
                elif case=='fifo':os.mkfifo(dst/'pipe')
                elif case=='malformed_manifest':(dst/'PUBLICATION_MANIFEST.json').write_text('[]')
                elif case=='changed_manifest':
                    p=dst/'PUBLICATION_MANIFEST.json';v=json.loads(p.read_text());v['schema']=2;p.write_text(json.dumps(v))
                else:
                    p=dst/'PUBLICATION_MANIFEST.json';p.write_text('{"schema":1,'+p.read_text()[1:])
                cmd=[sys.executable,'-I','-B']+(['-O'] if opt else [])+[str(dst/'verify_publication.py'),'--manifest-sha256',pin,'--inventory-only']
                p=subprocess.run(cmd,cwd='/',capture_output=True,timeout=20)
                if p.returncode==0:raise RuntimeError('mutation accepted: '+case)
                result.append({'case':case,'optimized':opt,'rejected':True})
    return {'status':'PASS','rejected_mutations':len(result),'controls':result,'scope':'Actual corruption copies; no altered mathematical source is executed.'}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--manifest-sha256',required=True);a=p.parse_args()
    print(json.dumps(run(ROOT,a.manifest_sha256),sort_keys=True,indent=2))
