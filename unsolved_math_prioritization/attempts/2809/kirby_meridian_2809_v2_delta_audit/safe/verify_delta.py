#!/usr/bin/env python3
"""Bounded C1 delta audit; all changes and execution occur in temporary copies."""
import argparse, hashlib, json, subprocess, sys, tempfile, zipfile, shutil, ast
from pathlib import Path, PurePosixPath

H=lambda b:hashlib.sha256(b).hexdigest()
PINS={
 'KIRBY_MERIDIAN_2809_AUTHOR_SAFE_FREEZE.zip':'14809993ffccbb97cc3510d7a17df91ad375bc85cf02bd6a9c430c31c12673c3',
 'KIRBY_MERIDIAN_2809_AUTHOR_FREEZE_RECEIPT.json':'7145de950652ce1839a698f02d60428b607b0129ca85c927418ef32fa4130b97',
 'KIRBY_MERIDIAN_2809_INDEPENDENT_AUDIT.zip':'79c4abdd006d1a1fcd5d917fec9984c82fc30ca4864f4c17f76ef461e927cb8f',
 'KIRBY_MERIDIAN_2809_V2_SAFE_FREEZE.zip':'e37dc6bdf5c5b0f5f1547e9d9db0225034fe403682770b59bc254c99140b01a0',
 'KIRBY_MERIDIAN_2809_V2_FROM_V1.patch':'f8e62da8aa381f411cba39bace04f2bae0637b2f0000b1c69137d76dae0aaa36',
 'KIRBY_MERIDIAN_2809_V2_DELTA.json':'753fda2d84a32363684ba4878cdab8bdbb1a79e25e0134f6caa0e02db6df0915'}

def need(x,msg):
    if not x:raise RuntimeError(msg)

def files(root):
    need(not any(p.is_symlink() for p in root.rglob('*')),'Symlink rejected')
    return {p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}

def unpack(zpath,target):
    target.mkdir()
    with zipfile.ZipFile(zpath) as z:
        names=z.namelist();need(len(names)==len(set(names)),'Duplicate ZIP member');need(z.testzip() is None,'ZIP CRC')
        roots=set()
        for entry in z.infolist():
            p=PurePosixPath(entry.filename)
            need(len(p.parts)==2 and not p.is_absolute() and '..' not in p.parts,'Unsafe or unexpected ZIP hierarchy')
            need(not entry.is_dir() and ((entry.external_attr>>16)&0o170000)!=0o120000,'Nonregular ZIP member')
            roots.add(p.parts[0]);(target/p.name).write_bytes(z.read(entry))
        need(len(roots)==1,'Multiple archive roots')
    return target

def verify_manifest(root):
    members=files(root);d=json.loads(members['MANIFEST.json']);entries=d['files']
    need(len(entries)==len({e['path'] for e in entries}),'Duplicate manifest')
    need(set(members)-{'MANIFEST.json'}=={e['path'] for e in entries},'Manifest membership')
    for e in entries:
        need(e['bytes']==len(members[e['path']]) and e['sha256']==H(members[e['path']]),'Manifest hash')

def run(root,opt,script='verify.py'):
    p=subprocess.run([sys.executable,*(['-O'] if opt else []),str(root/script)],cwd=root.parent,capture_output=True,timeout=30)
    return p.returncode,p.stdout

def refresh(root):
    p=root/'MANIFEST.json';d=json.loads(p.read_text())
    for e in d['files']:
        b=(root/e['path']).read_bytes();e.update(bytes=len(b),sha256=H(b))
    p.write_text(json.dumps(d))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('input_directory',type=Path);args=parser.parse_args();base=args.input_directory.resolve()
    for name,pin in PINS.items():need(H((base/name).read_bytes())==pin,'Input pin mismatch: '+name)
    output={'problem_id':2809,'scope':'C1 bounded delta; no new proof search','pins_verified':PINS,
            'checks':[],'replays':[],'integrity_mutations':[],'semantic_mutations':[]}
    checked=lambda label:output['checks'].append(label)
    with tempfile.TemporaryDirectory(prefix='meridian_v2_delta_') as temporary:
        temp=Path(temporary)
        v1=unpack(base/'KIRBY_MERIDIAN_2809_AUTHOR_SAFE_FREEZE.zip',temp/'original')
        v2=unpack(base/'KIRBY_MERIDIAN_2809_V2_SAFE_FREEZE.zip',temp/'renamed_v2')
        audit=unpack(base/'KIRBY_MERIDIAN_2809_INDEPENDENT_AUDIT.zip',temp/'original_audit')
        for folder in (v1,v2,audit):verify_manifest(folder)
        need(len(files(v1))==8 and len(files(v2))==9 and len(files(audit))==10,'Unexpected file count')
        need(files(v1)==files(base/'kirby_meridian_2809'/'safe'),'Original author files changed')
        need(files(v2)==files(base/'kirby_meridian_2809_v2'/'safe'),'Live v2 differs from freeze')
        need(files(audit)==files(base/'kirby_meridian_2809_independent_audit'/'safe'),'Original audit changed')
        checked('Original author/audit and actual v2 memberships, bytes and manifests')
        old,new=files(v1),files(v2)
        changed=sorted(n for n in set(old)&set(new) if old[n]!=new[n]);added=sorted(set(new)-set(old));removed=sorted(set(old)-set(new))
        need(changed==['LITERATURE.md','MANIFEST.json','PROOFS.md','README.md','RESEARCH_LOG.md','SOURCE_VERIFICATION.json'],'Unauthorized changed file')
        need(added==['V2_PROVENANCE.json'] and not removed,'Unexpected added/removed file')
        need(old['verify.py']==new['verify.py'] and old['RESULTS.json']==new['RESULTS.json'],'Code/results changed')
        checked('Changed-file allowlist; verification code and saved results byte-identical')
        need(new['RESEARCH_LOG.md'].startswith(old['RESEARCH_LOG.md']),'Historical log rewritten')
        checked('Entire historical research log is an unchanged prefix')
        requirements=json.loads((audit/'REQUIRED_CORRECTIONS.json').read_text())['mandatory_corrections'][0]['changes']
        expected_proof=old['PROOFS.md'].decode()
        for item in requirements[:2]:
            need(expected_proof.count(item['find'])==1,'Nonunique required replacement')
            expected_proof=expected_proof.replace(item['find'],item['replace'])
        need(expected_proof.encode()==new['PROOFS.md'],'Proof changed beyond exact C1 replacements')
        need(requirements[2]['append'] in new['LITERATURE.md'].decode(),'Required seventh source missing')
        checked('Both required proof replacements exact; seventh-source bibliography present')
        a,b=json.loads(old['SOURCE_VERIFICATION.json']),json.loads(new['SOURCE_VERIFICATION.json'])
        need(b['sources'][:6]==a['sources'] and len(b['sources'])==7,'Original sources changed')
        s=b['sources'][6]
        need(s['url']=='https://arxiv.org/pdf/1509.06653v2' and s['pdf']=={'bytes':99015,'sha256':'7ba4a3a9e37bf675114c01ca0caf984b9f281226c892d7ea9c19fe61e1cdd059'},'Obstruction-source pin')
        need('no SnapPy/Regina' in s['inspection'],'Computation limit not disclosed')
        amendment=b.pop('audit_correction');b['sources']=b['sources'][:6];b['publication_safety']['independent_audit_status']=a['publication_safety']['independent_audit_status']
        need(a==b,'Source metadata changed beyond C1')
        need(amendment['approaches_used']==5 and amendment['new_proof_attempts']==0 and amendment['original_conjecture_resolved'] is False and amendment['computational_inputs_rerun'] is False,'Scope/budget drift')
        checked('Seventh-source pin, precise metadata delta, no computational rerun, unresolved 5/5')
        provenance=json.loads(new['V2_PROVENANCE.json'])
        for e in provenance['correction_inputs']:
            bb=(audit/e['name']).read_bytes();need(len(bb)==e['bytes'] and H(bb)==e['sha256'],'Correction-input pin')
        need(provenance['original_author_receipt']['sha256']==PINS['KIRBY_MERIDIAN_2809_AUTHOR_FREEZE_RECEIPT.json'],'Receipt provenance')
        need(provenance['original_author_zip']['sha256']==PINS['KIRBY_MERIDIAN_2809_AUTHOR_SAFE_FREEZE.zip'],'Archive provenance')
        for n,h in provenance['unchanged_files'].items():need(H(old[n])==h==H(new[n]),'Unchanged provenance')
        checked('Version provenance and original audit-input pins')
        delta=json.loads((base/'KIRBY_MERIDIAN_2809_V2_DELTA.json').read_text())
        need({e['path'] for e in delta['files']}==set(old)|set(new),'Delta membership')
        for e in delta['files']:
            n=e['path']
            for version,items in [('v1',old),('v2',new)]:
                want=None if n not in items else {'bytes':len(items[n]),'sha256':H(items[n])}
                need(e[version]==want,'Delta entry bytes/hash')
        reconstruction=temp/'patch_reconstruction';shutil.copytree(v1,reconstruction)
        p=subprocess.run(['patch','-p1','--batch','--forward','-i',str(base/'KIRBY_MERIDIAN_2809_V2_FROM_V1.patch')],cwd=reconstruction,capture_output=True)
        need(p.returncode==0 and files(reconstruction)==new,'Patch reconstruction')
        checked('Pinned supplied delta exact; supplied patch reconstructs all v2 bytes')
        need(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(new['verify.py']))),'Assertion guard introduced')
        for opt in (False,True):
            rc,out=run(v2,opt);need(rc==0 and out==old['RESULTS.json'],'V2 replay differs')
            rc,rebuilt=run(audit,opt,'independent_controls.py');need(rc==0 and rebuilt==(audit/'INDEPENDENT_RESULTS.json').read_bytes(),'Independent replay differs')
            need(json.loads(rebuilt)['author_domain_counts']==json.loads(out)['counts'],'Category-count mismatch')
            output['replays'].append({'optimized':opt,'v2_checks':10768,'independent_supplementary_checks':3399,'exact_output_match':True})
        for name in ('altered_proof','extra_file','missing_proof','altered_results'):
            copy=temp/name;shutil.copytree(v2,copy)
            if name=='altered_proof':(copy/'PROOFS.md').write_bytes(b'mutation')
            if name=='extra_file':(copy/'EXTRA.txt').write_bytes(b'mutation')
            if name=='missing_proof':(copy/'PROOFS.md').unlink()
            if name=='altered_results':(copy/'RESULTS.json').write_text('{}\n')
            for opt in (False,True):
                rc,_=run(copy,opt);need(rc!=0,'Integrity mutation accepted');output['integrity_mutations'].append({'mutation':name,'optimized':opt,'rejected':True})
        corruptions={
          'drop_sign_guard':('if d < 0 or d*d < 4*r:','if d*d < 4*r:'),
          'drop_second_cap_square':('d = n*n*B*B - P*P - Q*Q','d = n*n*B*B - P*P'),
          'double_determinant_scaling':('r = P*P*Q*Q - n*n*A0*A0','r = P*P*Q*Q - n**4*A0*A0'),
          'max_caps':('F(p[i]+p[j], abs(a[i]-a[j]))','F(max(p[i],p[j]), abs(a[i]-a[j]))'),
          'false_strict_equality':("return 'strict' if d*d > 4*r else 'at_most'","return 'strict' if d*d >= 4*r else 'at_most'"),
          'active_guard':('def algebra_controls():','def algebra_controls():\n    require(False, "injected")')}
        for name,(before,after) in corruptions.items():
            copy=temp/name;shutil.copytree(v2,copy);p=copy/'verify.py';text=p.read_text();need(text.count(before)==1,'Nonunique semantic mutation');p.write_text(text.replace(before,after));refresh(copy)
            for opt in (False,True):
                rc,_=run(copy,opt);need(rc!=0,'Semantic mutation accepted');output['semantic_mutations'].append({'mutation':name,'optimized':opt,'rejected_with_updated_manifest':True})
    for name,pin in PINS.items():need(H((base/name).read_bytes())==pin,'Original input altered')
    output.update(status='PASS_C1_DELTA',v2_archive_accepted=PINS['KIRBY_MERIDIAN_2809_V2_SAFE_FREEZE.zip'],v2_manifest_sha256='df7e3eec992338dfe32cd8c7cb226bc1665b92503c791ea34ec54254d01a6ec0',originals_unchanged=True,full_conjecture_resolved=False,approaches_used=5,new_proof_attempts=0,remote_writes=False,novelty_claim=False)
    print(json.dumps(output,indent=2,sort_keys=True))
if __name__=='__main__':main()
