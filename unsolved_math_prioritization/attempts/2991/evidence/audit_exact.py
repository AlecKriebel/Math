#!/usr/bin/env python3
"""Independent source-free replay of the immutable KP-4.115 candidate.

Usage: python audit_exact.py /path/to/frozen/public /existing/empty/output
Writes only under the explicitly supplied, empty, external output directory.
Pins and checks remain active under -O and -OO. Smooth topology is not certified.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import itertools
import json
import math
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys

MANIFEST_SHA = 'ed9dc743686e9f58d67f4ec796ab217a3a94dec1635b05f9c4804e4b22bf4cf4'
PROOF_SHA = '90be5ae3ab394227e9b22db5db3c49e1798714f70a7c554eed4fadb539ee820b'

class AuditFailure(RuntimeError):
    pass

def need(condition, message):
    if not condition:
        raise AuditFailure(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def tree_pins(root):
    return {p.name: {'bytes': p.stat().st_size, 'sha256': sha(p.read_bytes()),
                     'mode': format(stat.S_IMODE(p.stat().st_mode), '04o')}
            for p in sorted(root.iterdir()) if p.is_file()}

def verify_tree(root):
    mf = root/'FROZEN_MANIFEST.json'
    need(mf.is_file() and not mf.is_symlink(), 'manifest missing or symlinked')
    need(stat.S_IMODE(mf.stat().st_mode) == 0o444, 'manifest mode must be 0444')
    need(not os.access(mf, os.W_OK), 'manifest writable by actual uid')
    raw = mf.read_bytes()
    need(sha(raw) == MANIFEST_SHA, 'trusted manifest hash mismatch')
    m = json.loads(raw)
    names = {x['name'] for x in m['files']} | {'FROZEN_MANIFEST.json'}
    need({p.name for p in root.iterdir()} == names, 'unexpected or missing candidate file')
    need(stat.S_IMODE(root.stat().st_mode) == 0o555, 'candidate directory mode must be 0555')
    need(not os.access(root, os.W_OK), 'candidate directory writable by actual uid')
    for x in m['files']:
        f = root/x['name']
        need(not f.is_symlink() and f.is_file(), 'candidate member must be an ordinary file')
        data = f.read_bytes()
        need(len(data) == x['bytes'] and sha(data) == x['sha256'], 'member binding mismatch: '+x['name'])
        need(format(stat.S_IMODE(f.stat().st_mode),'04o') == x['mode'], 'member mode mismatch')
        need(not os.access(f, os.W_OK), 'candidate member writable by actual uid')
    need(sha((root/'PART_A_PROOF.md').read_bytes()) == PROOF_SHA, 'proof pin mismatch')
    return tree_pins(root)

def snapshot(root):
    return {p.relative_to(root).as_posix(): (p.stat().st_size, sha(p.read_bytes()),
                    stat.S_IMODE(p.stat().st_mode)) for p in root.rglob('*') if p.is_file()}

def copy_mutable(src, dst):
    shutil.copytree(src, dst)
    dst.chmod(0o755)
    for f in dst.iterdir():
        f.chmod(0o644)
    return dst

def freeze(root):
    for f in root.iterdir():
        if not f.is_symlink():
            f.chmod(0o444)
    root.chmod(0o555)

def exact_det(matrix):
    """Independent rational Gaussian elimination, not Laplace expansion."""
    n=len(matrix)
    a=[[Fraction(v) for v in row] for row in matrix]
    result=Fraction(1)
    for i in range(n):
        pivot=next((r for r in range(i,n) if a[r][i]),None)
        if pivot is None:
            return 0
        if pivot != i:
            a[i],a[pivot]=a[pivot],a[i]
            result=-result
        lead=a[i][i]
        result*=lead
        for r in range(i+1,n):
            factor=a[r][i]/lead
            a[r]=[a[r][c]-factor*a[i][c] for c in range(n)]
    need(result.denominator == 1, 'integer determinant expected')
    return result.numerator

def independent_algebra(checker):
    units=tuple(i for i in range(8) if pow(i,2,8)==1)
    need(units==(1,3,5,7), 'independent unit enumeration failed')
    pair=lambda x:frozenset((x%8,-x%8))
    equations=0
    for xs in itertools.product(units, repeat=3):
        before=Counter(pair(x) for x in xs)
        after=Counter(pair(3*x) for x in xs)
        need(before != after, 'independent multiset obstruction failed')
        for perm in itertools.permutations(range(3)):
            for signs in itertools.product((-1,1),repeat=3):
                need(not all((xs[i]-signs[i]*3*xs[perm[i]])%8==0 for i in range(3)),
                     'signed permutation escaped obstruction')
                equations+=1
    need(equations==3072, 'independent signed permutation count')
    odd_test_count=0
    for modulus in range(2,41):
        us=[x for x in range(modulus) if math.gcd(x,modulus)==1]
        for q in us:
            if q*q%modulus==1 and q not in (1,modulus-1):
                need(all((q*x-x)%modulus and (q*x+x)%modulus for x in us),
                     'fixed unit/sign orbit in general involution argument')
                for xs in itertools.product(us,repeat=3):
                    need(not checker.same_multiset_after_multiplier(xs,modulus,q),
                         'general odd-sector obstruction failed')
                    odd_test_count+=1
    checked=0
    unimodular=0
    for n in (1,2,3):
        upper=[(i,j) for i in range(n) for j in range(i,n)]
        for vals in itertools.product(range(-2,3),repeat=len(upper)):
            s=[[0]*n for _ in range(n)]
            for (i,j),v in zip(upper,vals):
                s[i][j]=s[j][i]=v
            d=exact_det(s)
            need(checker.det(s)==d, 'determinant implementations disagree')
            try:
                got=checker.check_graph(s)
            except checker.VerificationError:
                need(abs(d)!=1, 'checker rejected symmetric unimodular form')
            else:
                need(abs(d)==1 and got=={'rank':n,'determinant':d},
                     'checker accepted nonunimodular form')
                # The symplectic pairing of the graph's ith and jth columns.
                for i in range(n):
                    for j in range(n):
                        pairing=sum(s[k][i]*int(k==j)-int(k==i)*s[k][j] for k in range(n))
                        need(pairing==0, 'independent graph pairing is nonzero')
                unimodular+=1
            checked+=1
    return {'signed_sector_assignments':equations,
            'general_odd_sector_unit_triples':odd_test_count,
            'symmetric_integer_matrices':checked,
            'unimodular_matrices':unimodular}

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('candidate',type=Path)
    parser.add_argument('output',type=Path)
    args=parser.parse_args()
    root=args.candidate.resolve()
    out=args.output.resolve()
    need(os.getuid()==1000 and os.geteuid()==1000, 'this replay requires actual UID/EUID 1000')
    need(out.is_dir() and not any(out.iterdir()), 'output must exist and be empty')
    need(not out.is_relative_to(root), 'output must be outside candidate')
    need(not root.is_relative_to(out), 'candidate must not be inside output')
    before=verify_tree(root)
    initial=snapshot(root)
    # O_WRONLY without writing any bytes tests permissions without altering data.
    try:
        fd=os.open(root/'PART_A_PROOF.md',os.O_WRONLY)
    except PermissionError:
        blocked=True
    else:
        os.close(fd)
        raise AuditFailure('actual write-capable open unexpectedly succeeded')
    run_dir=out/'runs'; run_dir.mkdir()
    records=[]
    env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    def run(label,mode,tree=root,extra=(),expected=0,reason=None):
        cmd=[sys.executable]+mode+[str(tree/'verify_exact.py')]+list(extra)
        proc=subprocess.run(cmd,stdin=subprocess.DEVNULL,capture_output=True,env=env,cwd=out)
        prefix=run_dir/label
        prefix.with_suffix('.stdout').write_bytes(proc.stdout)
        prefix.with_suffix('.stderr').write_bytes(proc.stderr)
        need((proc.returncode==0)==(expected==0),'unexpected checker result: '+label)
        if reason is not None:
            need(reason.encode() in proc.stderr,'wrong rejection reason: '+label)
        records.append({'label':label,'optimization':len(mode[0])-1 if mode else 0,
                        'exit_code':proc.returncode,'stdout_bytes':len(proc.stdout),
                        'stderr_bytes':len(proc.stderr),'expected_success':expected==0})
        return proc
    modes=[('normal',[]),('O',['-O']),('OO',['-OO'])]
    for name,mode in modes:
        p=run(name+'_clean',mode)
        got=json.loads(p.stdout)
        need(got['status']=='pass' and got['uid']==1000 and got['candidate_read_only'], 'baseline environment claim')
        need(got['optimization']==len(mode[0])-1 if mode else got['optimization']==0,'optimization reporting')
        need(got['proof_sha256']==PROOF_SHA and not got['geometric_proof_certified_by_code'],'scope/output pin')
        for fault,reason in [('multiplier','fixed unit/sign class'),('surjectivity','generate C_p'),
                             ('matrix','symmetric'),('expected-count','permutation count mismatch')]:
            run(name+'_fault_'+fault,mode,extra=['--inject-fault',fault],expected=1,reason=reason)
        target=out/(name+'_external.json')
        run(name+'_external',mode,extra=['--output',str(target)])
        need(target.is_file() and json.loads(target.read_text())['status']=='pass','external output missing')
        for label,path,reason in [('inside',root/'new_output.json','outside candidate tree'),
                                  ('existing',target,'overwrite existing'),
                                  ('missing_parent',out/'missing'/'result.json','parent must already exist')]:
            run(name+'_'+label,mode,extra=['--output',str(path)],expected=1,reason=reason)
        link=out/(name+'_inside_symlink')
        link.symlink_to(root/'new_output.json')
        run(name+'_symlink_inside',mode,extra=['--output',str(link)],expected=1,reason='outside candidate tree')
        run(name+'_bad_cli',mode,extra=['--inject-fault','invented'],expected=1,reason='invalid choice')
    mutations=[
        ('unit_enumeration','if math.gcd(x,p)==1]','if math.gcd(x,p)==2]','incorrect unit set'),
        ('sign_class','return min(a % p, (-a) % p)','return max(a % p, (-a) % p)','incorrect unit/sign classes'),
        ('deck_order','p,q=8,3','p,q=7,3','incorrect unit set'),
        ('even_control','same_multiset_after_multiplier([1,3],8,3)','same_multiset_after_multiplier([1,1],8,3)','even-sector counterexample'),
        ('orientation','require(det(real_swap)==1','require(det(real_swap)==-1','R4 orientation'),
        ('congruence','changed==[[2,1],[1,0]]','changed==[[2,1],[1,1]]','congruence computation'),
        ('double_genus','double_g,double_k=2*g+b-1','double_g,double_k=2*g+b','doubling formula'),
        ('double_rank','2*k-2*p_page-b+1','2*k-2*p_page-b+2','doubling formula'),
        ('balanced_relation','genus==b2+3*sector_rank','genus==b2+2*sector_rank','balanced parameter'),
        ('exterior_rank','b2+2*genus','b2+2*genus+1','exterior Euler characteristic'),
    ]
    mutdir=out/'mutations'; mutdir.mkdir()
    source=(root/'verify_exact.py').read_text()
    for label,old,new,reason in mutations:
        need(source.count(old)==1,'mutation not uniquely applicable: '+label)
        mutant=copy_mutable(root,mutdir/label)
        (mutant/'verify_exact.py').write_text(source.replace(old,new))
        freeze(mutant)
        for name,mode in modes:
            run(name+'_semantic_'+label,mode,tree=mutant,expected=1,reason=reason)
    for label,missing in [('proof_tamper',False),('proof_missing',True)]:
        mutant=copy_mutable(root,mutdir/label)
        proof=mutant/'PART_A_PROOF.md'
        if missing:
            proof.unlink()
        else:
            proof.write_bytes(proof.read_bytes()+b'\n')
        freeze(mutant)
        for name,mode in modes:
            run(name+'_'+label,mode,tree=mutant,expected=1,
                reason='FileNotFoundError' if missing else 'proof changed after audit handoff')
    integrity=[]
    for item in sorted(root.iterdir()):
        mutant=copy_mutable(root,mutdir/('integrity_'+item.stem))
        target=mutant/item.name
        target.write_bytes(target.read_bytes()+b'\n')
        freeze(mutant)
        try:
            verify_tree(mutant)
        except AuditFailure as exc:
            integrity.append({'mutation':item.name,'rejected':True,'reason':str(exc)})
        else:
            raise AuditFailure('integrity edit escaped: '+item.name)
    for label in ['extra_member','missing_member','resigned_manifest','symlink_member','writable_manifest','writable_member','writable_directory']:
        mutant=copy_mutable(root,mutdir/label)
        if label=='extra_member':
            (mutant/'extra.txt').write_text('Unexpected authored audit control.\n')
        elif label=='missing_member':
            (mutant/'REPORT.md').unlink()
        elif label=='symlink_member':
            (mutant/'REPORT.md').unlink(); (mutant/'REPORT.md').symlink_to(root/'REPORT.md')
        elif label=='resigned_manifest':
            f=mutant/'REPORT.md'; f.write_bytes(f.read_bytes()+b'\n')
            m=json.loads((mutant/'FROZEN_MANIFEST.json').read_text())
            entry=next(x for x in m['files'] if x['name']=='REPORT.md')
            entry['bytes']=f.stat().st_size; entry['sha256']=sha(f.read_bytes())
            (mutant/'FROZEN_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
        freeze(mutant)
        if label=='writable_manifest':
            (mutant/'FROZEN_MANIFEST.json').chmod(0o644)
        elif label=='writable_member':
            (mutant/'REPORT.md').chmod(0o644)
        elif label=='writable_directory':
            mutant.chmod(0o755)
        try:
            verify_tree(mutant)
        except AuditFailure as exc:
            integrity.append({'mutation':label,'rejected':True,'reason':str(exc)})
        else:
            raise AuditFailure('integrity control escaped: '+label)
    # Explicitly disclose a bounded integrity limitation of the supplied checker:
    # its sole content pin is PART_A_PROOF.md; our envelope binds all nine files.
    report_only=mutdir/'integrity_REPORT'
    coverage=[]
    for name,mode in modes:
        run(name+'_report_only_change_not_bound_by_original',mode,tree=report_only)
        coverage.append({'mode':name,'original_checker_accepts_unpinned_report_change':True,
                         'independent_envelope_rejects_same_change':True})
    sys.dont_write_bytecode=True
    spec=importlib.util.spec_from_file_location('frozen_trisection_checks',root/'verify_exact.py')
    checker=importlib.util.module_from_spec(spec); spec.loader.exec_module(checker)
    algebra=independent_algebra(checker)
    after=verify_tree(root)
    need(initial==snapshot(root) and before==after,'original candidate changed')
    receipt={'status':'pass','uid':os.getuid(),'euid':os.geteuid(),
             'audit_optimization':sys.flags.optimize,'actual_write_capable_open_blocked':blocked,
             'candidate_manifest_sha256':MANIFEST_SHA,'candidate_pins':before,
             'original_candidate_unchanged':True,'checker_runs':records,
             'integrity_controls':integrity,'checker_integrity_scope':coverage,
             'independent_algebra':algebra,'mathematical_scope':
             'Arithmetic and immutable-file verification only; part (a) proof accepted separately, part (b) unresolved.'}
    (out/'AUDIT_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'pass','uid':os.getuid(),'euid':os.geteuid(),
                      'audit_optimization':sys.flags.optimize,'checker_runs':len(records),
                      'integrity_controls':len(integrity),'independent_algebra':algebra,
                      'original_candidate_unchanged':True},indent=2,sort_keys=True))

if __name__=='__main__':
    main()
