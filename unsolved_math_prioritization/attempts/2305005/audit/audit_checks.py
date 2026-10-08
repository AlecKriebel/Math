#!/usr/bin/env python3
"""Independent finite and integrity controls for the frozen 2305005 packet.

No analytic existence theorem is computed. No network access or publication.
"""
import argparse
from fractions import Fraction as Q
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile

PIN = '916ef2162da505bef37aab22de595ccc2c91497908a3b8f28f9c29a81588356a'
ARCHIVE = '8c85e9a8e91e9a0124b62644a7663d7c69b487bb579678ef5772a57e0f1671a1'
RECEIPT = '7e17750906cdf0c3f2c2a6fef621c98cdf3ac756b307e6b7856cc89f8036a15b'
VERIFIER = '487fcef8ed8739fc083835904b3093cd99920c388a3a07e6e48a712a5f7ed870'
INVENTORY = {'CLAIMS.json','FIXTURES.json','MANIFEST.json','README.md','REPORT.md','SOURCES.json','controls.py','verify.py'}
MODES = [[],['-O'],['-OO']]

def check(ok, reason):
    if not ok:
        raise RuntimeError(reason)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def snapshot(root):
    return {p.relative_to(root).as_posix():sha(p.read_bytes()) for p in root.rglob('*') if p.is_file()}

def dump(path, obj):
    path.write_text(json.dumps(obj,indent=2,allow_nan=True)+'\n')

def modify(root, name, action):
    p=root/name
    value=json.loads(p.read_bytes())
    action(value)
    dump(p,value)

def repin(root):
    p=root/'MANIFEST.json'
    m=json.loads(p.read_bytes())
    for e in m['files']:
        b=(root/e['path']).read_bytes()
        e['bytes']=len(b)
        e['sha256']=sha(b)
    dump(p,m)
    return sha(p.read_bytes())

def run(verifier, root, pin, mode, extras=()):
    return subprocess.run([sys.executable,'-B',*mode,str(verifier),'--root',str(root),'--manifest-sha256',pin,*extras],capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})

def finite_checks():
    counts={'independent_coefficient_identities':0,'independent_bloch_scalars':0,'independent_lacunary_bounds':0,'independent_parabola_identities':0,'infimal_envelope_properties':0,'independent_lattice_upper':0,'independent_lattice_lower':0}
    for n in range(1,257):
        convolution=sum((Q(4,j*(n-j)) for j in range(1,n,2) if (n-j)%2),Q())
        harmonic=Q() if n%2 else Q(4,n//2)*sum((Q(1,2*j-1) for j in range(1,n//2+1)),Q())
        check(convolution==harmonic,'coefficient identity')
        counts['independent_coefficient_identities']+=1
    for n in range(1,257):
        t=1-Q(1,2*n)
        check(t**(n-1)>=Q(1,2) and n*(1-t*t)>=Q(3,4),'Bloch scalar')
        counts['independent_bloch_scalars']+=1
        check(8**n>=8*n and Q(4**n-4,3)<Q(4**n,3),'lacunary integer bounds')
        counts['independent_lacunary_bounds']+=2
    check(Q(1,2)-Q(1,3)-Q(1,63)==Q(19,126)>0,'Rouche margin')
    for a2 in [Q(1,4),Q(1),Q(3,2),Q(5)]:
        for j in range(17):
            r=a2+Q(j,3)
            for k in range(17):
                t2=Q(k,5)
                check((r+a2-t2)**2+4*a2*t2==(t2-r+a2)**2+4*a2*r,'parabola identity')
                counts['independent_parabola_identities']+=1
    # Continuous nondecreasing piecewise-affine H with slopes both above and
    # below one. Its infimal envelope need only be minimized at r or a knot.
    knots=[(Q(0),Q(16)),(Q(1),Q(18)),(Q(4),Q(18)),(Q(5),Q(30)),(Q(20),Q(31)),(Q(100),Q(64))]
    def H(x):
        for (l,u),(r,v) in zip(knots,knots[1:]):
            if l<=x<=r:
                return u+(x-l)*(v-u)/(r-l)
        return Q(64)+(x-100)/64
    def h(x):
        check(x>=0,'envelope argument')
        return min([H(x)]+[y+x-t for t,y in knots if t<=x])/4
    def floor(x):
        return x.numerator//x.denominator
    def ceil(x):
        return -floor(-x)
    directions=[(1,0,1),(-1,0,1),(0,1,1),(0,-1,1),(3,4,5),(-3,-4,5),(5,-12,13),(-12,5,13)]
    for j in range(601):
        r=Q(j,3);hr=h(r)
        check(4<=hr<=H(r)/4,'envelope bounds')
        check(hr>=min(16+r/2,H(r/2))/4,'envelope lower minorant')
        for delta in [Q(1,7),Q(5,4),Q(17,3)]:
            hs=h(r+delta)
            check(hr<=hs<=hr+delta/4,'envelope monotonicity/Lipschitz')
            counts['infimal_envelope_properties']+=1
        counts['infimal_envelope_properties']+=2
        for dx,dy,d in directions:
            x=r*Q(dx,d);y=r*Q(dy,d)
            m=floor(x+Q(1,2));hm=h(abs(Q(m)))
            n=max(ceil(hm),floor(abs(y)+Q(1,2)))
            if y<0:n=-n
            check(abs(n)>=hm and abs(m-x)+abs(n-y)<=hr+Q(13,8),'independent lattice upper')
            counts['independent_lattice_upper']+=1
        # Outside this finite horizontal window the lower bound follows from
        # the horizontal distance alone; inside, nearest vertical punctures suffice.
        for m in range(floor(r-hr/2)-1,ceil(r+hr/2)+2):
            n=ceil(h(abs(Q(m))))
            check((m-r)**2+n*n >= (hr/2)**2,'independent lattice lower')
            counts['independent_lattice_lower']+=1
    return counts

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--author-root',type=Path,required=True)
    ap.add_argument('--archive',type=Path,required=True)
    ap.add_argument('--receipt',type=Path,required=True)
    a=ap.parse_args()
    root=a.author_root.absolute();verifier=root/'verify.py'
    before=snapshot(root)
    check(set(before)==INVENTORY,'fixed eight-file inventory')
    check(sha((root/'MANIFEST.json').read_bytes())==PIN,'external manifest pin')
    check(sha(verifier.read_bytes())==VERIFIER,'verifier bootstrap pin')
    check(a.archive.stat().st_size==20951 and sha(a.archive.read_bytes())==ARCHIVE,'external archive pin')
    check(a.receipt.stat().st_size==3516 and sha(a.receipt.read_bytes())==RECEIPT,'external receipt pin')
    with zipfile.ZipFile(a.archive) as z:
        check(len(z.infolist())==8 and set(z.namelist())==INVENTORY,'archive names')
        for info in z.infolist():
            check(not info.is_dir() and (info.external_attr>>16)&0o170000==0o100000,'regular archive member')
            check(z.read(info.filename)==(root/info.filename).read_bytes(),'archive/member binding')
    outputs=[]
    for mode in MODES:
        r=run(verifier,root,PIN,mode)
        check(r.returncode==0,'baseline rejected')
        outputs.append(r.stdout)
    check(len(set(outputs))==1,'baseline optimization difference')
    tests=[]
    def add(label,name,fn):tests.append((label,name,fn))
    add('boolean_manifest_schema','MANIFEST.json',lambda x:x.__setitem__('schema',True))
    add('float_manifest_schema','MANIFEST.json',lambda x:x.__setitem__('schema',1.0))
    add('boolean_manifest_problem','MANIFEST.json',lambda x:x.__setitem__('problem_id',True))
    add('float_manifest_problem','MANIFEST.json',lambda x:x.__setitem__('problem_id',2305005.0))
    add('null_manifest_files','MANIFEST.json',lambda x:x.__setitem__('files',None))
    add('boolean_payload_size','MANIFEST.json',lambda x:x['files'][0].__setitem__('bytes',True))
    add('float_payload_size','MANIFEST.json',lambda x:x['files'][0].__setitem__('bytes',1909.0))
    add('uppercase_payload_digest','MANIFEST.json',lambda x:x['files'][0].__setitem__('sha256',x['files'][0]['sha256'].upper()))
    add('backslash_payload_path','MANIFEST.json',lambda x:x['files'][0].__setitem__('path','x\\CLAIMS.json'))
    add('dot_payload_path','MANIFEST.json',lambda x:x['files'][0].__setitem__('path','./CLAIMS.json'))
    add('empty_path_component','MANIFEST.json',lambda x:x['files'][0].__setitem__('path','x//CLAIMS.json'))
    add('boolean_fixture_schema','FIXTURES.json',lambda x:x.__setitem__('schema',True))
    add('boolean_fixture_problem','FIXTURES.json',lambda x:x.__setitem__('problem_id',True))
    add('finite_float_coefficient','FIXTURES.json',lambda x:x['log_square_coefficients'][0].__setitem__('numerator',0.0))
    add('boolean_denominator','FIXTURES.json',lambda x:x['log_square_coefficients'][0].__setitem__('denominator',True))
    add('zero_denominator','FIXTURES.json',lambda x:x['log_square_coefficients'][0].__setitem__('denominator',0))
    add('negative_infinity','FIXTURES.json',lambda x:x['log_square_coefficients'][0].__setitem__('numerator',-float('inf')))
    add('nan_nested','FIXTURES.json',lambda x:x['geometry']['directions'][0].__setitem__(0,float('nan')))
    add('boolean_geometry_denominator','FIXTURES.json',lambda x:x['geometry'].__setitem__('radius_denominator',True))
    add('boolean_direction','FIXTURES.json',lambda x:x['geometry']['directions'][0].__setitem__(0,True))
    add('zero_direction_denominator','FIXTURES.json',lambda x:x['geometry']['directions'][0].__setitem__(2,0))
    add('boolean_route_count','CLAIMS.json',lambda x:x.__setitem__('mathematical_routes',True))
    add('false_flag_as_integer','CLAIMS.json',lambda x:x.__setitem__('full_solution_claimed',0))
    add('unresolved_status_overclaim','CLAIMS.json',lambda x:x.__setitem__('literal_limit_status','solved'))
    add('source_false_flag_as_integer','SOURCES.json',lambda x:x['scholarly_sources'][1].__setitem__('original_full_theorem_inspected',0))
    add('source_finite_float','SOURCES.json',lambda x:x['dataset_pins'][0].__setitem__('bytes',68931837.0))
    labels=[];rejections=0
    with tempfile.TemporaryDirectory(prefix='slow-audit-') as td:
        temp=Path(td)
        for i,(label,name,fn) in enumerate(tests):
            c=temp/str(i);shutil.copytree(root,c)
            modify(c,name,fn)
            pin=sha((c/'MANIFEST.json').read_bytes()) if name=='MANIFEST.json' else repin(c)
            for mode in MODES:
                r=run(verifier,c,pin,mode)
                check(r.returncode!=0 and 'REJECT:' in r.stderr,'mutation accepted: '+label)
                rejections+=1
            labels.append(label)
        for label,pin in [('wrong_external_pin','0'*64),('uppercase_external_pin',PIN.upper()),('short_external_pin',PIN[:-1])]:
            for mode in MODES:
                r=run(verifier,root,pin,mode)
                check(r.returncode!=0 and 'REJECT:' in r.stderr,'pin mutation accepted')
                rejections+=1
            labels.append(label)
        raw_tests=[('overflow_float','FIXTURES.json',b'"numerator": 0',b'"numerator": 1e999'),('duplicate_fixture_key','FIXTURES.json',b'"schema": 1',b'"schema": 1, "schema": 1')]
        for label,name,old,new in raw_tests:
            c=temp/label;shutil.copytree(root,c);p=c/name
            b=p.read_bytes();check(old in b,'mutation pattern absent');p.write_bytes(b.replace(old,new,1));pin=repin(c)
            for mode in MODES:
                r=run(verifier,c,pin,mode)
                check(r.returncode!=0 and 'REJECT:' in r.stderr,'raw mutation accepted')
                rejections+=1
            labels.append(label)
        # Explicit path-object cases, including symlinked roots and manifest.
        for label in ['root_symlink','manifest_symlink','nested_extra_payload']:
            c=temp/label;shutil.copytree(root,c);target=c
            if label=='root_symlink':
                target=temp/'root-link';target.symlink_to(c,target_is_directory=True)
            elif label=='manifest_symlink':
                p=c/'MANIFEST.json';p.unlink();p.symlink_to(root/'MANIFEST.json')
            else:
                (c/'.extra').mkdir();(c/'.extra'/'data').write_bytes(b'extra')
            for mode in MODES:
                r=run(verifier,target,PIN,mode)
                check(r.returncode!=0 and 'REJECT:' in r.stderr,'path mutation accepted')
                rejections+=1
            labels.append(label)
        bogus=temp/'wrong-input';bogus.write_bytes(b'{}')
        for label,flag in [('wrong_problem_source','--problems'),('wrong_research_source','--research'),('wrong_pdf_source','--pdf')]:
            for mode in MODES:
                r=run(verifier,root,PIN,mode,[flag,str(bogus)])
                check(r.returncode!=0 and 'REJECT:' in r.stderr,'wrong source accepted')
                rejections+=1
            labels.append(label)
        ro=temp/'genuine-readonly';shutil.copytree(root,ro)
        ro_before=snapshot(ro)
        for p in ro.iterdir():p.chmod(0o444)
        ro.chmod(0o555)
        check(hasattr(os,'geteuid') and os.geteuid()!=0,'read-only control requires nonroot POSIX')
        denied=[]
        try:
            for p in [ro/'NEW_FILE',ro/'REPORT.md']:
                try:
                    with p.open('ab') as f:f.write(b'x')
                except PermissionError:denied.append(p.name)
                else:raise RuntimeError('read-only write succeeded')
            for mode in MODES:
                r=run(verifier,ro,PIN,mode)
                check(r.returncode==0 and r.stdout==outputs[0],'read-only/relocation mismatch')
            check(snapshot(ro)==ro_before,'read-only snapshot changed')
        finally:
            ro.chmod(0o755)
            for p in ro.iterdir():p.chmod(0o644)
    check(snapshot(root)==before,'original packet changed')
    result={'schema':1,'problem_id':2305005,'original_packet_unchanged':True,'archive_member_count':8,'bootstrap_verifier_pin_checked':True,'baseline_modes':['normal','-O','-OO'],'baseline_outputs_identical':True,'author_finite_check_count':sum(json.loads(outputs[0])['exact_finite_checks'].values()),'independent_finite_checks':finite_checks(),'additional_negative_cases':len(labels),'additional_negative_rejections':rejections,'additional_negative_labels':labels,'read_only_uid':os.geteuid(),'read_only_modes':['normal','-O','-OO'],'read_only_write_probes_denied':denied,'read_only_inventory_unchanged':True,'relocated_output_identical':True,'analytic_existence_proof_computed':False}
    print(json.dumps(result,sort_keys=True,separators=(',',':')))

if __name__=='__main__':
    try:main()
    except (RuntimeError,OSError,ValueError,KeyError,TypeError) as e:
        print('AUDIT FAILURE: '+str(e),file=sys.stderr)
        sys.exit(1)
