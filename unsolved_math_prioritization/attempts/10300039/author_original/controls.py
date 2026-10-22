#!/usr/bin/env python3
"""Exercise the authenticated bootstrap against final frozen disposable copies."""
import argparse,hashlib,json,os,pathlib,shutil,stat,subprocess,sys,tempfile

def require(x,msg):
    if not x:raise ValueError(msg)
def treehash(root):
    result={}
    for p in sorted(root.rglob('*')):
        if p.is_file():result[p.relative_to(root).as_posix()]={'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
    return result
def writable_copy(src,dst):
    shutil.copytree(src,dst)
    # Only disposable copies receive writable modes; source remains frozen.
    for p in dst.rglob('*'):
        if p.is_dir():p.chmod(0o755)
        elif p.is_file():p.chmod(0o644)
    dst.chmod(0o755)
def freeze(root):
    for p in root.rglob('*'):
        if p.is_file():p.chmod(0o444)
    for p in sorted(root.rglob('*'),key=lambda x:len(x.parts),reverse=True):
        if p.is_dir():p.chmod(0o555)
    root.chmod(0o555)
def thaw(root):
    if root.exists():
        root.chmod(0o755)
        for p in root.rglob('*'):
            if p.is_dir() and not p.is_symlink():p.chmod(0o755)
            elif p.is_file() and not p.is_symlink():p.chmod(0o644)
def main():
    parser=argparse.ArgumentParser();parser.add_argument('--release',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parent);a=parser.parse_args();root=a.release.absolute();bundle=root/'bundle';bootstrap=root/'bootstrap.py'
    require(os.geteuid()!=0,'run unprivileged');require(not bootstrap.stat().st_mode&0o222,'bootstrap must already be frozen')
    require(all(not p.stat().st_mode&0o222 for p in bundle.rglob('*') if p.is_file()),'bundle must already be frozen')
    before=treehash(bundle);accepted=[];rejected=[]
    mutations=['missing_member','changed_member','extra_member','extra_directory','nested_manifest','expanded_symlink','root_symlink','archive_mutation','manifest_mutation','duplicate_json','nan_json','malformed_json','malicious_code','wrong_type']
    with tempfile.TemporaryDirectory(prefix='q10-controls-') as t:
        temp=pathlib.Path(t)
        for mode in [0,1,2]:
            flags=['-I','-S','-B']+(['-'+'O'*mode] if mode else [])
            def invoke(b,*args):return subprocess.run([sys.executable,*flags,str(bootstrap),'--bundle',str(b),*args],stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=temp,timeout=120)
            r=invoke(bundle);require(r.returncode==0,'frozen baseline rejected');accepted.append('frozen-'+str(mode))
            relocated=temp/('relocated-'+str(mode));writable_copy(bundle,relocated);freeze(relocated)
            try:r=invoke(relocated);require(r.returncode==0,'readonly relocation rejected');accepted.append('readonly-relocation-'+str(mode))
            finally:thaw(relocated)
            for case in mutations:
                b=temp/(str(mode)+'-'+case);writable_copy(bundle,b)
                if case=='missing_member':(b/'author/RESULT.md').unlink()
                elif case=='changed_member':(b/'author/RESULT.md').write_text('altered')
                elif case=='extra_member':(b/'author/extra.txt').write_text('extra')
                elif case=='extra_directory':(b/'empty').mkdir()
                elif case=='nested_manifest':(b/'author/MANIFEST.json').write_text('{}')
                elif case=='expanded_symlink':
                    p=b/'author/RESULT.md';p.unlink();p.symlink_to(bundle/'author/RESULT.md')
                elif case=='root_symlink':
                    link=temp/(str(mode)+'-root-link');link.symlink_to(b,target_is_directory=True);b=link
                elif case=='archive_mutation':(b/'AUTHOR.zip').write_bytes((b/'AUTHOR.zip').read_bytes()+b'x')
                elif case=='manifest_mutation':
                    p=b/'EXTERNAL_MANIFEST.json';m=json.loads(p.read_text());m['problem_id']=0;p.write_text(json.dumps(m))
                elif case=='duplicate_json':(b/'EXTERNAL_MANIFEST.json').write_text('{"files":{},"files":{}}')
                elif case=='nan_json':(b/'EXTERNAL_MANIFEST.json').write_text('{"value":NaN}')
                elif case=='malformed_json':(b/'EXTERNAL_MANIFEST.json').write_bytes(b'{\xff')
                elif case=='malicious_code':(b/'author/verify_math.py').write_text('import pathlib\npathlib.Path("UNAUTHENTICATED_EXECUTION").write_text("bad")\n')
                elif case=='wrong_type':(b/'author/RESULT.md').unlink();(b/'author/RESULT.md').mkdir()
                r=invoke(b);require(r.returncode!=0,'accepted damaged case '+case);require(not(temp/'UNAUTHENTICATED_EXECUTION').exists(),'unauthenticated code ran');rejected.append(case+'-'+str(mode))
            for label,args in [('unknown_option',['--unknown']),('incomplete_corpus',['--problems',str(temp/'none')])]:
                r=invoke(bundle,*args);require(r.returncode!=0,label+' accepted');rejected.append(label+'-'+str(mode))
            bad=temp/('bad-corpus-'+str(mode)+'.json');bad.write_text('{"duplicate":0,"duplicate":1}')
            r=invoke(bundle,'--problems',str(bad),'--reports',str(bad));require(r.returncode!=0,'malformed external corpus accepted');rejected.append('malformed-external-corpus-'+str(mode))
        require(treehash(bundle)==before,'frozen source changed')
    print(json.dumps({'uid':os.geteuid(),'frozen_source_unchanged':True,'accepted':accepted,'rejected':rejected,'positive_count':len(accepted),'negative_count':len(rejected),'modes':['normal','-O','-OO'],'meaning':'artifact and finite-control checks, not formal geometric proof'},sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(2)
