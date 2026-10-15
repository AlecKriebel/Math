#!/usr/bin/env python3
"""Externally pin this script before use. Exact immutable PR938 identity guard.
This is a finite replay/transport guard, not a sandbox or topology verifier.
"""
import argparse, hashlib, json, os, stat, subprocess, sys
from pathlib import Path
PINS = {'AUDIT2_FREEZE_RECEIPT.json': [867, 'cf226445fa2dd3788e5881f0d9fb8d6f7a4636abd674f59fe311daa48bb312d7'], 'BOOTSTRAP.py': [2062, '04e0ebc81c81e72b942552033023e898e1d21139127fb05e40934ba04b128b2e'], 'MUTATION_RESULTS.json': [1231, '585786619f8408a1eaa35ae2e287c5546b75cbcd903ce92d103c092a3270c816'], 'PUBLICATION_ACCEPTANCE.md': [2756, '5494016cdfa53768ee80beec94c57370bea054efb0bef5a3824bd3c2534d4584'], 'PUBLICATION_MANIFEST.json': [8338, '149e6144f0ad90ee12945c29155318100b65c6faee8ba2661d2c09db58b9ae30'], 'README.md': [2856, 'b091d3004cb0b59a452d6014ac4715c6dfdee1633e599e8a46f5861407d7579e'], 'RESEARCH_LOG.md': [844, '28ccd57a65569ea8656fcc490b6a96d514ca8276c525a48dce6036091a7d3888'], 'TEST_MUTATIONS.py': [7667, 'a27c40ac629be4aae54b81c3d3b4b92a4fec60d9df44e1ba748648518916a850'], 'VERIFY_PUBLICATION.py': [12350, '767878142d114ea26f11259196769d78ffc4cbc36d95dc3d25864cd7f8bfad7b'], 'audit1/ACCEPTANCE.json': [1092, '90ae905debbf6db84b1c32e93832d69e1a1fbcb44330d6e4b690f38fa35eaf2f'], 'audit1/AUDIT_MANIFEST.json': [1487, '599456c9e8acb599c226aa7175aede3e72fb50241a83d1937cbc09c1a227f009'], 'audit1/AUTHOR_ADVERSARIAL_REPLAY.json': [761, '4e9b99ca59850559b7bf17610d038d3df272b9159d92caa16c98e28bf33957ac'], 'audit1/AUTHOR_VERIFIER_REPLAY.json': [303, 'd6b0718f41537fef3338342216f27ab880781f8364fe74f9c499ce879810942a'], 'audit1/FULL_AUDIT.md': [15007, '9aeab140dfc350947d47d2b88fe85848bcdfa4f642a0aece7647f3f21653b275'], 'audit1/INDEPENDENT_CHARACTERISTIC_CHECK.json': [1848, 'c3d6da14306cd7331d3ffa04842d39cfb7ca7c6cb6cac5fef095f88dcfac4ad1'], 'audit1/RECOVERY_CONTROLS.json': [3856, 'acc808fafe8f66ba0d528e5a87011a34faeca60eba2a9060774642c705e61bba'], 'audit1/SOURCE_VERIFICATION.json': [4234, '2a13d22eab67d7f1abd18e007cd222d2bc6d994c4660550ad6538d36d61aca17'], 'audit1/recovery_controls.py': [6642, 'e82a5e1c8fa009a52c74b3188e821fc6fd3e406c9915d457d90418d182d90d5d'], 'audit2/ACCEPTANCE.json': [3316, '94b97ad7cec143519637c972bcf73bf2de36006dbe8592517b014280f3865519'], 'audit2/AUDIT_REPORT.md': [11115, '40af681accd2dc21cf3446b824581f14fe22dda21b721045091336c9e9fe1cd7'], 'audit2/AUTHOR_REPLAY.json': [761, '4e9b99ca59850559b7bf17610d038d3df272b9159d92caa16c98e28bf33957ac'], 'audit2/INDEPENDENT_RESULTS.json': [18092, 'ff0734a2f339a58ef0ff4e9d1864f86f1097db73063a5aad37c7dbc223898476'], 'audit2/MANIFEST.json': [2295, '0347538b88fcc15d20816d96bc901b492938492084174749e6e8463905c1ff2a'], 'audit2/PORTABLE_REPLAY.json': [386, '12b3f283a7306bee4ab14a8ec4b422a30277f4d071ef4d905e06f0603b0866f5'], 'audit2/README.md': [1960, 'a2a3886f7511268230e10613bf9a2815b15024f9ef086a09526a95b27b6def69'], 'audit2/RECOVERY_AUTHOR_REPLAY.json': [761, '4e9b99ca59850559b7bf17610d038d3df272b9159d92caa16c98e28bf33957ac'], 'audit2/RECOVERY_CONTROLS.json': [1813, '760b62494cf22ffee9df86f96a344336f636bbe2d2b22f455ab9b8c670843b57'], 'audit2/RECOVERY_INDEPENDENT_RESULTS.json': [18092, 'ff0734a2f339a58ef0ff4e9d1864f86f1097db73063a5aad37c7dbc223898476'], 'audit2/SOURCE_CHECKS.json': [5119, 'f2b29fd0b520a6a9e2990e9fb87c9067e3a8a1a6e6f6df68b404c1fa7cc90464'], 'audit2/independent_check.py': [8832, '8413a45f628425038b1a3937cedc80ac0aecc689eacc4473dc158087002e0703'], 'audit2/recovery_controls.py': [5756, 'c464c472a00deed17af3428225bf808de58f00e484a7b815aa18874336dd175e'], 'audit2/test_second_audit_replay.py': [2830, 'd305be4a50fa6325ada954ea47350e8abeab56201b1b0b5b007dd8617463b3b1'], 'original/ATTEMPT_LEDGER.json': [1182, '9f9e6e1e907f6616ec2d2ce345019649e69b41f5ea27d6fd305707663f62361d'], 'original/MANIFEST.json': [1788, 'd1e1467c6d36b6c62283af2ec50ddff8864020ad8a7c9e0ba9a6704dacb4246a'], 'original/PRIOR_ATTEMPT_GATE.json': [2626, '50ed4109ddf62bf0de0223d04016120485aa11393c48f5e265d0f055583960d1'], 'original/PROOF.md': [13197, '0492e0e0de785be263174e86d69855120b2f5c24b105c6479739cd72d64abe3b'], 'original/README.md': [1935, '5c46e4ecf0500babc8661f8053ab91db9d7da3195f6acbac4472c918996ade23'], 'original/SOURCES.json': [4522, '91338c352ae6fff361c740449fa99e552e69473c2fcfa0de31503ae7c3de32d2'], 'original/SOURCE_AUDIT.md': [5488, '1cf47de23741f57db1250d1a97131f2b6d2369e3f73fbc48eb08a07d7e6d52c6'], 'original/TEST_REPORT.json': [761, '4e9b99ca59850559b7bf17610d038d3df272b9159d92caa16c98e28bf33957ac'], 'original/VERIFY_OUTPUT.json': [303, 'd6b0718f41537fef3338342216f27ab880781f8364fe74f9c499ce879810942a'], 'original/certificate.json': [25068, '66f47cc9a4fe63a50b407808a5a7574ca0fa19ce862b70655aea24124895aa62'], 'original/test_replay.py': [4152, '4632c92442be9a2209ac725aaef86891eb13ede340837b0c14f0a520bd3a626f'], 'original/verify.py': [11845, '816c78ca944e6b8d57b1f1f305f7821ce21bc784cb9cc26f173c96053105f841']}
HEX='149e6144f0ad90ee12945c29155318100b65c6faee8ba2661d2c09db58b9ae30'

def need(x,m):
    if not x:raise ValueError(m)

def authenticate(root,readonly=False):
    root=Path(os.path.abspath(root))
    for p in [root,*root.parents]:
        need(stat.S_ISDIR(p.lstat().st_mode),'symlink/non-directory root or ancestor: '+str(p))
    fm,dm=(0o444,0o555)if readonly else(0o644,0o755)
    need(stat.S_IMODE(root.lstat().st_mode)==dm,'root permissions')
    actual={}; dirs=set()
    for base,sub,files in os.walk(root,followlinks=False):
        for name in sub+files:
            p=Path(base)/name;st=p.lstat();rel=p.relative_to(root).as_posix()
            if stat.S_ISDIR(st.st_mode):
                need(stat.S_IMODE(st.st_mode)==dm,'directory mode '+rel);dirs.add(rel)
            else:
                need(stat.S_ISREG(st.st_mode),'nonregular file '+rel)
                need(stat.S_IMODE(st.st_mode)==fm,'file mode '+rel)
                need(rel in PINS,'extra file '+rel)
                fd=os.open(p,os.O_RDONLY|getattr(os,'O_NOFOLLOW',0))
                try:
                    fst=os.fstat(fd);need((st.st_dev,st.st_ino,st.st_mode)==(fst.st_dev,fst.st_ino,fst.st_mode),'file changed before read')
                    with os.fdopen(fd,'rb',closefd=False)as f:data=f.read(PINS[rel][0]+1)
                finally:os.close(fd)
                need((len(data),hashlib.sha256(data).hexdigest())==tuple(PINS[rel]),'immutable Git mismatch '+rel)
                actual[rel]=True
    need(set(actual)==set(PINS),'missing file')
    need(dirs=={'original','audit1','audit2'},'extra/missing directory')
    return root

def main():
    p=argparse.ArgumentParser();p.add_argument('--packet',required=True);p.add_argument('--readonly',action='store_true');p.add_argument('--check-only',action='store_true');p.add_argument('--python',default=sys.executable);p.add_argument('--script',default='BOOTSTRAP.py');p.add_argument('--mode',choices=['normal','O','OO','env2'],default='normal');p.add_argument('extra',nargs=argparse.REMAINDER);a=p.parse_args()
    root=authenticate(a.packet,a.readonly)
    if a.check_only:
        print(json.dumps({'status':'PASS_IMMUTABLE_GIT_IDENTITY','files':44,'closed_directories':3,'ancestor_symlinks_rejected':True}));return 0
    need(a.script in PINS and a.script.endswith('.py'),'unlisted entrypoint')
    flags={'normal':[],'O':['-O'],'OO':['-OO'],'env2':[]}[a.mode]
    env={k:v for k,v in os.environ.items()if not k.startswith('PYTHON')};env['PYTHONDONTWRITEBYTECODE']='1'
    if a.mode=='env2':env['PYTHONOPTIMIZE']='2'
    # env2 deliberately omits -I so inherited optimization reaches this worker.
    startup=[]if a.mode=='env2'else['-I']
    extra=a.extra[1:]if a.extra[:1]==['--']else a.extra
    cmd=[a.python,*startup,'-B',*flags,str(root/a.script),*extra]
    cp=subprocess.run(cmd,env=env,capture_output=True,timeout=1500)
    sys.stdout.buffer.write(cp.stdout);sys.stderr.buffer.write(cp.stderr)
    authenticate(root,a.readonly)
    return cp.returncode
if __name__=='__main__':
    try:sys.exit(main())
    except (ValueError,OSError,subprocess.SubprocessError)as e:print('GUARD_REJECT: '+str(e),file=sys.stderr);sys.exit(1)
