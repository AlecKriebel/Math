#!/usr/bin/env python3
"""Offline integrity and exact finite regressions; not a conjecture certificate."""
import argparse,hashlib,json,os,stat,sys
from pathlib import Path
def deny_network(event,args):
    if event.startswith('socket.'): raise RuntimeError('Network prohibited')
sys.addaudithook(deny_network)
FILES={'SOURCE_METADATA.json', 'SOURCE_GATE.md', 'CHECK_RESULTS_OPTIMIZED.json', 'README.md', 'ROOT_POLYNOMIAL_REGRESSION.json', 'PROVENANCE.json', 'check_reductions.py', 'INDEPENDENT_AUDIT.md', 'CHECK_RESULTS.json', 'FIVE_APPROACHES.md', 'MANIFEST.json', 'verify_package.py', 'ANALYSIS_MANIFEST.json'}
SOURCE_HASHES={'ANALYSIS_MANIFEST.json': {'source_name': 'analysis/ANALYSIS_MANIFEST.json', 'original': {'bytes': 1349, 'sha256': 'b5f72ac87d7b299e401d931ff94f35e2448eb06f67cf7e480ad5dda124cb1eb1'}, 'frozen': {'bytes': 1349, 'sha256': 'b5f72ac87d7b299e401d931ff94f35e2448eb06f67cf7e480ad5dda124cb1eb1'}, 'editorial_changes': []}, 'CHECK_RESULTS.json': {'source_name': 'analysis/CHECK_RESULTS.json', 'original': {'bytes': 459, 'sha256': 'a30a6bce4460b9c4ddc2679b90b8d439f4eb230b95117e8931e01541243d36bb'}, 'frozen': {'bytes': 459, 'sha256': 'a30a6bce4460b9c4ddc2679b90b8d439f4eb230b95117e8931e01541243d36bb'}, 'editorial_changes': []}, 'CHECK_RESULTS_OPTIMIZED.json': {'source_name': 'analysis/CHECK_RESULTS_OPTIMIZED.json', 'original': {'bytes': 459, 'sha256': 'a30a6bce4460b9c4ddc2679b90b8d439f4eb230b95117e8931e01541243d36bb'}, 'frozen': {'bytes': 459, 'sha256': 'a30a6bce4460b9c4ddc2679b90b8d439f4eb230b95117e8931e01541243d36bb'}, 'editorial_changes': []}, 'FIVE_APPROACHES.md': {'source_name': 'analysis/FIVE_APPROACHES.md', 'original': {'bytes': 12461, 'sha256': '0ee0023339a007fbcfc735ad6fa1078cd8f70273a535907c483d14a23fb6c9f6'}, 'frozen': {'bytes': 12461, 'sha256': '0ee0023339a007fbcfc735ad6fa1078cd8f70273a535907c483d14a23fb6c9f6'}, 'editorial_changes': []}, 'INDEPENDENT_AUDIT.md': {'source_name': 'analysis/INDEPENDENT_AUDIT.md', 'original': {'bytes': 13664, 'sha256': '392bcadf08837528760120beae0ee45c7999c81bf1a694b241d33ee7e28eb151'}, 'frozen': {'bytes': 13664, 'sha256': '392bcadf08837528760120beae0ee45c7999c81bf1a694b241d33ee7e28eb151'}, 'editorial_changes': []}, 'ROOT_POLYNOMIAL_REGRESSION.json': {'source_name': 'analysis/ROOT_POLYNOMIAL_REGRESSION.json', 'original': {'bytes': 463, 'sha256': '4a87e380b03348bd79807ecb2b1b5cac002516d70ffadc0ad3cc08f1ea1abaed'}, 'frozen': {'bytes': 463, 'sha256': '4a87e380b03348bd79807ecb2b1b5cac002516d70ffadc0ad3cc08f1ea1abaed'}, 'editorial_changes': []}, 'check_reductions.py': {'source_name': 'analysis/check_reductions.py', 'original': {'bytes': 1609, 'sha256': '72d77a69a30aac05e8fd0476d2b06fd5a8903aad1ac815d384667463a048503c'}, 'frozen': {'bytes': 1609, 'sha256': '72d77a69a30aac05e8fd0476d2b06fd5a8903aad1ac815d384667463a048503c'}, 'editorial_changes': []}, 'SOURCE_GATE.md': {'source_name': 'public/SOURCE_GATE.md', 'original': {'bytes': 3807, 'sha256': '2dc88966cdf6a6cf386bcba9ae10f2179d230cdbdce11cd1f193403d37240edc'}, 'frozen': {'bytes': 3354, 'sha256': 'b3a45e5cdb3949240a494dd4160385a3370c60b6fcbe9a257b17fe49eba36280'}, 'editorial_changes': ['Removed repository searches and private corpus/research-results findings; retained public source and scope metadata.']}, 'SOURCE_METADATA.json': {'source_name': 'public/SOURCE_METADATA.json', 'original': {'bytes': 2503, 'sha256': '9dc07bc8ff54f97e9b2db57367154cc05a3b35767bb78d64f77aff5ce0080c0b'}, 'frozen': {'bytes': 2503, 'sha256': '9dc07bc8ff54f97e9b2db57367154cc05a3b35767bb78d64f77aff5ce0080c0b'}, 'editorial_changes': []}}

def fail(message):
    raise ValueError(message)

def inventory(root):
    if not stat.S_ISDIR(root.lstat().st_mode): fail('root is not a real directory')
    found=set(); bad=[]
    def walk(directory,prefix=''):
        with os.scandir(directory) as it:
            entries=sorted(it,key=lambda e:e.name)
        for entry in entries:
            relative=prefix+entry.name; st=entry.stat(follow_symlinks=False)
            found.add(relative)
            if stat.S_ISDIR(st.st_mode):
                bad.append(relative+': directory prohibited')
                walk(Path(directory)/entry.name,relative+'/')
            elif not stat.S_ISREG(st.st_mode) or st.st_nlink!=1:
                bad.append(relative+': nonregular, symlink, or hardlink prohibited')
    walk(root)
    if bad or found!=FILES: fail('inventory rejected: '+repr({'unsafe':bad,'extra':sorted(found-FILES),'missing':sorted(FILES-found)}))

def read_regular(path):
    # No following symlinks at the final component; recheck type after open.
    fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    try:
        st=os.fstat(fd)
        if not stat.S_ISREG(st.st_mode) or st.st_nlink!=1:fail('unsafe read target')
        with os.fdopen(fd,'rb',closefd=False) as stream:return stream.read()
    finally:os.close(fd)

def rec(data):return {'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}

def require(value,message):
    if not value: fail(message)

def exact_checks():
    import sympy as s
    import itertools
    x=s.symbols('x')
    f=x**5+x**4-4*x**3-3*x**2+3*x+1
    P=x**2-2
    Q=-x**4-x**3+3*x**2+2*x-1
    identities={
        'Q(P)-X':s.expand(Q.subs(x,P)-x+(x**3-x**2-2*x+1)*f),
        'P(Q)-X':s.expand(P.subs(x,Q)-x-(x**3+x**2-2*x-1)*f),
        'f(P)':s.expand(f.subs(x,P)-(x**5-x**4-4*x**3+3*x**2+3*x-1)*f)}
    require(all(v==0 for v in identities.values()),'quintic inverse or same-polynomial identity failed')
    fm=s.Poly(f,x,modulus=2)
    require(all(int(fm.eval(i))%2!=0 for i in (0,1)), 'quintic has mod-2 root')
    require(s.rem(fm,s.Poly(x**2+x+1,x,modulus=2)).as_expr()==1,'quintic quadratic remainder failed')
    ps=[x,x**2,x**3,x**4,-x**4+4*x**3+3*x**2-3*x-1]
    U=s.Matrix([[p.coeff(x,j) for p in ps] for j in range(5)])
    require(U.det()==-1,'lattice-unit determinant failed')
    residues=[s.rem(ps[i]*ps[0]**(i-1)-ps[1]**i,f,x) for i in range(2,5)]
    require(all(v==0 for v in residues),'lattice-unit congruences failed')
    require(s.cancel(ps[1]/ps[0])==x,'lattice-unit recovered root failed')
    require(5>2+1 and 5<=2*4,'degree window failed')
    powers=[s.rem(P**i,f,x) for i in range(5)]
    V=s.Matrix([[p.coeff(x,j) for p in powers] for j in range(5)])
    require(V.det()==1,'conjugate generator basis determinant failed')
    A6=[p for p in itertools.permutations(range(1,7)) if sum(p[i]>p[j] for i in range(6) for j in range(i+1,6))%2==0]
    require(len(A6)==360 and len({p[:4] for p in A6})==360,'A6 4-transitivity count failed')
    require(not any(p[:5]==(1,3,2,4,5) for p in A6),'forbidden A6 transport found')
    return {'quintic_identities':{k:str(v) for k,v in identities.items()},'mod2_roots':False,'mod2_quadratic_remainder':1,'lattice_unit_det':int(U.det()),'lattice_unit_residues':[str(v) for v in residues],'recovered_root':'x','conjugate_basis_det':int(V.det()),'A6_order':len(A6),'A6_ordered_four_image_count':360,'forbidden_transport_count':0}

def validate(root,receipt_path):
    inventory(root)
    require(not receipt_path.resolve().is_relative_to(root.resolve()),'receipt must be external')
    receipt=json.loads(read_regular(receipt_path))
    manifest_bytes=read_regular(root/'MANIFEST.json')
    require(rec(manifest_bytes)==receipt['manifest'],'external manifest anchor mismatch')
    require(rec(read_regular(root/'verify_package.py'))==receipt['validator'],'external validator anchor mismatch')
    manifest=json.loads(manifest_bytes)
    require(set(manifest)=={'row','problem_id','status','turns','files'},'manifest schema mismatch')
    require((manifest['row'],manifest['problem_id'],manifest['status'],manifest['turns'])==(1889,30005097,'UNRESOLVED',5),'target or status mismatch')
    require(set(manifest['files'])==FILES-{'MANIFEST.json'},'manifest inventory mismatch')
    for name,wanted in manifest['files'].items():
        require(rec(read_regular(root/name))==wanted,'content mismatch: '+name)
    provenance=json.loads(read_regular(root/'PROVENANCE.json'))
    require(provenance['source_artifacts']==SOURCE_HASHES,'source provenance mismatch')
    for name,wanted in SOURCE_HASHES.items():
        require(rec(read_regular(root/name))==wanted['frozen'],'frozen source mismatch: '+name)
    require((receipt['row'],receipt['problem_id'],receipt['status'],receipt['turns'])==(1889,30005097,'UNRESOLVED',5),'receipt target mismatch')
    require(receipt['source_artifacts']==SOURCE_HASHES,'receipt provenance mismatch')
    regress=json.loads(read_regular(root/'ROOT_POLYNOMIAL_REGRESSION.json'))
    require(regress['f']=='x**5 + x**4 - 4*x**3 - 3*x**2 + 3*x + 1' and regress['P']=='x**2 - 2' and regress['Q']=='-x**4 - x**3 + 3*x**2 + 2*x - 1','regression polynomial mismatch')
    results=exact_checks()
    print(json.dumps({'status':'PASS','row':1889,'problem_id':30005097,'disposition':'UNRESOLVED','turns':5,'exact_checks':results,'boundary':'Integrity and finite regressions only, no general solution or novelty'},indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--receipt',required=True,type=Path);a=p.parse_args()
    try:validate(Path(__file__).absolute().parent,a.receipt)
    except (OSError,ValueError,KeyError,TypeError,RecursionError,RuntimeError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
