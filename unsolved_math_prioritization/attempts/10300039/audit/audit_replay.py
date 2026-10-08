#!/usr/bin/env python3
"""Independent finite/integrity controls. This is not a geometric proof checker."""
import argparse
from fractions import Fraction as F
import hashlib
import io
import json
import os
from pathlib import Path
import runpy
import shutil
import stat
import subprocess
import sys
import tempfile
import zipfile

PACKET = 'df03afb408c6eb41c56a3a4a94faed0c6a90a08d890d9fd58ce568456de23b7b'
MANIFEST = '4ddc7651c1da6facd2692d5b2cfa1291ad64dbf8765bfb69079372aa9c46684f'
BOOTSTRAP = 'fa007f533eedc28a8d62b0197777c5d6d8cc7c6323a02bf9c3ec0534cf9e1665'

def require(ok, message):
    if not ok:
        raise ValueError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def identity(data):
    return {'bytes': len(data), 'sha256': sha(data)}

def inventory(root):
    result = {}
    for p in sorted(root.rglob('*')):
        require(not p.is_symlink(), 'unexpected symlink')
        if p.is_file():
            result[p.relative_to(root).as_posix()] = identity(p.read_bytes())
        else:
            require(p.is_dir(), 'unexpected filesystem object')
    return result

def check_distribution(root, packet, manifest):
    require(root.is_dir() and not root.is_symlink(), 'regular distribution directory')
    mb = manifest.read_bytes()
    require(len(mb) == 3399 and sha(mb) == MANIFEST, 'external manifest trust pin')
    m = json.loads(mb)
    pb = packet.read_bytes()
    require(len(pb) == 45884 and sha(pb) == PACKET, 'outer packet trust pin')
    require(identity(pb) == m['packet'], 'outer packet metadata')
    require(m['packet_version'] == 2 and m['problem_id'] == 10300039, 'target/version')
    actual = inventory(root)
    require(actual == m['files'] and len(actual) == 21, 'complete expanded inventory')
    expected_dirs={str(parent) for name in actual for parent in Path(name).parents if str(parent)!='.'}
    actual_dirs={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir()}
    require(actual_dirs==expected_dirs,'complete directory inventory')
    require(sha((root/'bootstrap.py').read_bytes()) == BOOTSTRAP, 'bootstrap trust pin')
    with zipfile.ZipFile(io.BytesIO(pb)) as z:
        require(len(z.infolist()) == len(set(z.namelist())) == 21, 'unique outer members')
        require(set(z.namelist()) == set(actual), 'exact outer ZIP inventory')
        for i in z.infolist():
            require(not i.is_dir() and not stat.S_ISLNK(i.external_attr >> 16), 'outer member type')
            require(z.read(i) == (root/i.filename).read_bytes(), 'outer/expanded mismatch')
    return actual

def math_controls():
    counts = {}
    def ck(name, value):
        require(value, name)
        counts[name] = counts.get(name, 0) + 1
    # Arbitrary centers/radii, both hemisphere sides, and both vertical sides
    # have points below the horosphere. The universal argument is in AUDIT.md.
    for center in [F(-7,3), F(0), F(11,5)]:
        for r in [F(1,100), F(1,2), F(1), F(17,3), F(100)]:
            z = min(F(1,2), r/2)
            ck('hemisphere_inside_below_horosphere', z*z < r*r and 0 < z < 1)
            x = center + 2*r
            ck('hemisphere_outside_below_horosphere', (x-center)**2+z*z > r*r and z < 1)
            for sign in [-1, 1]:
                ck('vertical_side_below_horosphere', sign*((center+sign)-center)>0 and z<1)
    # The triangle inequality implies the Gromov-product estimate used in route 2.
    for d in range(1,21):
        for R in [F(0),F(1,3),F(2),F(21)]:
            for e in [F(0),R/2,R]:
                low=max(F(0),F(d)-e)
                ck('bounded_distance_gromov_product', (F(d)+low-e)/2 >= F(d)-R)
    # Exact integer powers remove all numerical uncertainty around alpha=1/2.
    for den in range(1,13):
        for num in range(1,2*den+1):
            alpha=F(num,den)
            exponent=den-2*num
            a,b=F(2)**exponent,F(2)**(2*exponent)
            ck('holder_strict_threshold', (b<a)==(alpha>F(1,2)))
            ck('holder_boundary_constant', (b==a)==(alpha==F(1,2)))
            ck('holder_subthreshold_growth', (b>a)==(alpha<F(1,2)))
    # Rational Cayley coordinates of upper-halfspace points in the unit ball.
    def ball(x,y,z):
        den=x*x+y*y+(z+1)**2
        return (2*x/den,2*y/den,(x*x+y*y+z*z-1)/den)
    def norm2(v): return sum((a*a for a in v),F(0))
    previous={}
    for n in [2**k for k in range(2,20)]:
        eps=F(1,n)
        cases={
            'vertical_finite_endpoint':(ball(eps,0,eps),(F(0),F(0),F(-1))),
            'vertical_infinite_endpoint':(ball(0,0,F(n)),(F(0),F(0),F(1))),
            'endpoints_collide_at_infinity_low':(ball(F(n),0,eps),(F(0),F(0),F(1))),
            'endpoints_collide_at_infinity_high':(ball(F(n),0,F(n)),(F(0),F(0),F(1))),
            'hemisphere_collapse_finite':(ball(0,0,eps),(F(0),F(0),F(-1))),
        }
        for label,(point,target) in cases.items():
            error=norm2(tuple(x-y for x,y in zip(point,target)))
            ck(label+'_inside_ball',norm2(point)<1)
            if label in previous: ck(label+'_convergence_control',error<previous[label])
            previous[label]=error
    # Unsorted sites approaching zero from both sides test accumulation ordering.
    for length in range(1,31):
        sites=[F((-1)**i,i+1) for i in range(length)]
        weights={s:F(1,2**(i+1)) for i,s in enumerate(sites)}
        points=[]
        for s,w in weights.items():
            for u in [F(0),w/2,w]: points.append((s,u))
        for s,t in zip(sorted(sites),sorted(sites)[1:]): points.append(((s+t)/2,F(0)))
        points.sort()
        images=[t+sum((w for s,w in weights.items() if s<t),F(0))+u for t,u in points]
        ck('summable_weights_exact',sum(weights.values(),F(0))==1-F(1,2**length))
        for a,b in zip(images,images[1:]): ck('ordered_insertions_accumulating_sites',a<b)
    return {'counts':counts,'total':sum(counts.values()),'scope':'finite exact-rational diagnostics, not proofs of the geometric or infinite assertions'}

def independent_external_bindings(a):
    root=a.delivery/'bundle/author'
    expected=json.loads((root/'CORPUS_BINDINGS.json').read_bytes())
    data={}
    corpus_receipt={}
    for name,path in [('problems.json',a.problems),('research_results.json',a.reports)]:
        raw=path.read_bytes(); got=identity(raw)
        require(got=={k:expected['corpora'][name][k] for k in ['bytes','sha256']},'independent corpus identity')
        obj=json.loads(raw);require(len(obj)==expected['corpora'][name]['records'],'independent record count')
        data[name]=obj;corpus_receipt[name]={**got,'records':len(obj)}
    candidates=[x for x in data['problems.json'] if type(x.get('id')) is int and x['id']==10300039]
    require(len(candidates)==1,'independent unique target')
    problem=candidates[0];report=data['research_results.json']['AMR-102-0039']
    hashes={key:sha(json.dumps(value,sort_keys=True).encode()) for value,key in
            [(problem,'problem_record_sha256'),(report,'report_record_sha256'),([problem,report],'record_pair_sha256')]}
    hashes['statement_utf8_sha256']=sha(problem['statement'].encode())
    require(all(value==expected[key] for key,value in hashes.items()),'independent target serialization')
    pdfs={}
    for record in json.loads((root/'SOURCE_METADATA.json').read_bytes())['documents']:
        path=a.sources/record['filename'];got=identity(path.read_bytes())
        require(got=={k:record[k] for k in ['bytes','sha256']},'independent PDF identity')
        extraction=subprocess.run(['pdftotext','-layout',str(path),'-'],capture_output=True,check=True).stdout
        match=extraction==(a.sources/(path.stem+'.txt')).read_bytes()
        require(match,'fresh PDF extraction differs from inspected text')
        pdfs[record['filename']]={**got,'fresh_extraction_matches_inspected_text':True}
    return {'corpora':corpus_receipt,'target_hashes':hashes,'source_pdfs':pdfs,'source_statement_semantics':'independently checked against rendered primary Question 10.1, not a byte-equality assertion'}

def make_writable(root):
    root.chmod(0o755)
    for p in root.rglob('*'):
        if not p.is_symlink(): p.chmod(0o755 if p.is_dir() else 0o644)

def main():
    p=argparse.ArgumentParser()
    for name in ['delivery','packet','manifest','problems','reports','sources']:
        p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args()
    require(os.geteuid()!=0,'unprivileged execution required')
    for key,value in vars(a).items(): setattr(a,key,value.absolute())
    before=check_distribution(a.delivery,a.packet,a.manifest)
    external_bindings=independent_external_bindings(a)
    for path in [a.delivery,*a.delivery.rglob('*')]:
        require(path.stat().st_mode & 0o222 == 0,'actual final distribution must be read-only')
    try:
        with (a.delivery/'audit_write_probe').open('xb'): pass
    except PermissionError:
        pass
    else:
        raise ValueError('actual distribution unexpectedly writable')
    try:
        with (a.delivery/'bootstrap.py').open('r+b'): pass
    except PermissionError:
        pass
    else:
        raise ValueError('actual bootstrap unexpectedly writable')
    trusted=runpy.run_path(str(a.delivery/'bootstrap.py'),run_name='audited_bootstrap')
    parser_checks=[]
    invalid=[{'bytes':True,'sha256':'0'*64},{'bytes':-1,'sha256':'0'*64},
             {'bytes':0,'sha256':'A'*64},{'bytes':0,'sha256':'0'*63},
             {'bytes':0,'sha256':'0'*64,'extra':0},[],None]
    for i,value in enumerate(invalid):
        try: trusted['identity'](b'',value)
        except (ValueError,TypeError): parser_checks.append('identity-schema-'+str(i))
        else: raise ValueError('malformed identity accepted')
    trusted['identity'](b'',identity(b''))
    for label,value in [('duplicate','{"a":1,"a":2}'),('nonfinite','{"a":NaN}'),('syntax','{')]:
        try: json.loads(value,object_pairs_hook=trusted['pairs'],parse_constant=trusted['constant'])
        except ValueError: parser_checks.append(label)
        else: raise ValueError('malformed JSON accepted')
    baseline=[]; rejected=[]; relocated=[]
    with tempfile.TemporaryDirectory(prefix='independent-q10300039-') as td:
        temp=Path(td)
        for mode in ['', '-O', '-OO']:
            flags=['-I','-S','-B']+([mode] if mode else [])
            def invoke(root,*args):
                return subprocess.run([sys.executable,*flags,str(root/'bootstrap.py'),*args],cwd=temp,capture_output=True,timeout=120)
            run=invoke(a.delivery,'--problems',str(a.problems),'--reports',str(a.reports),'--sources',str(a.sources))
            require(run.returncode==0,'full independent binding replay failed')
            baseline.append({'mode':mode or 'normal','returncode':run.returncode,'result':json.loads(run.stdout)})
            dest=temp/('relocated'+str(len(baseline)))
            shutil.copytree(a.delivery,dest)
            try:
                run=invoke(dest)
                require(run.returncode==0,'relocated read-only replay failed')
                relocated.append(mode or 'normal')
            finally: make_writable(dest)
            cases=['missing_archive','missing_manifest','extra_bundle_file','extra_bundle_directory',
                   'author_directory_symlink','bootstrap_bundle_symlink','archive_trailing_bytes',
                   'zip_duplicate_member','manifest_duplicate_key','manifest_wrong_problem',
                   'manifest_nonfinite','manifest_bad_utf8','inner_sentinel','inner_directory',
                   'expanded_edit','outer_extra_file']
            for case in cases:
                dest=temp/((mode or 'normal')+'-'+case)
                shutil.copytree(a.delivery,dest);make_writable(dest)
                b=dest/'bundle'
                if case=='missing_archive': (b/'AUTHOR.zip').unlink()
                elif case=='missing_manifest': (b/'EXTERNAL_MANIFEST.json').unlink()
                elif case=='extra_bundle_file': (b/'extra').write_text('extra')
                elif case=='extra_bundle_directory': (b/'extra').mkdir()
                elif case=='author_directory_symlink':
                    shutil.rmtree(b/'author');(b/'author').symlink_to(a.delivery/'bundle/author',target_is_directory=True)
                elif case=='bootstrap_bundle_symlink':
                    shutil.rmtree(b);b.symlink_to(a.delivery/'bundle',target_is_directory=True)
                elif case=='archive_trailing_bytes':
                    with (b/'AUTHOR.zip').open('ab') as f:f.write(b'x')
                elif case=='zip_duplicate_member':
                    with zipfile.ZipFile(b/'AUTHOR.zip','a') as z:z.writestr('RESULT.md','substitute')
                elif case=='manifest_duplicate_key':(b/'EXTERNAL_MANIFEST.json').write_text('{"files":{},"files":{}}')
                elif case=='manifest_wrong_problem':
                    v=json.loads((b/'EXTERNAL_MANIFEST.json').read_text());v['problem_id']=10300040;(b/'EXTERNAL_MANIFEST.json').write_text(json.dumps(v))
                elif case=='manifest_nonfinite':(b/'EXTERNAL_MANIFEST.json').write_text('{"x":Infinity}')
                elif case=='manifest_bad_utf8':(b/'EXTERNAL_MANIFEST.json').write_bytes(b'{\xff')
                elif case=='inner_sentinel':
                    (b/'author/verify_math.py').write_text('from pathlib import Path\nPath('+repr(str(temp/'UNTRUSTED_RAN'))+').write_text("bad")\n')
                elif case=='inner_directory':
                    (b/'author/verify_math.py').unlink();(b/'author/verify_math.py').mkdir()
                elif case=='expanded_edit':(b/'author/APPROACH_02.md').write_text('Gamma-invariant replacement')
                elif case=='outer_extra_file':
                    (dest/'unlisted.txt').write_text('unlisted')
                    try:check_distribution(dest,a.packet,a.manifest)
                    except ValueError:rejected.append({'mode':mode or 'normal','case':case,'gate':'complete outer manifest'});continue
                    raise ValueError('outer extra file accepted')
                run=invoke(dest)
                require(run.returncode!=0,'damaged distribution accepted: '+case)
                require(not (temp/'UNTRUSTED_RAN').exists(),'unauthenticated sentinel executed')
                rejected.append({'mode':mode or 'normal','case':case,'gate':'pinned bootstrap','returncode':run.returncode})
            bad=temp/'bad.json';bad.write_text('{"a":1,"a":2}')
            for label,args in [('unknown-option',['--not-an-option']),('one-corpus',['--problems',str(a.problems)]),
                               ('malformed-external-corpora',['--problems',str(bad),'--reports',str(bad)]),
                               ('missing-source-pdfs',['--sources',str(temp)])]:
                run=invoke(a.delivery,*args);require(run.returncode!=0,'bad external input accepted')
                rejected.append({'mode':mode or 'normal','case':label,'gate':'bootstrap/inner input','returncode':run.returncode})
        require(check_distribution(a.delivery,a.packet,a.manifest)==before,'final original changed')
    print(json.dumps({'accepted':True,'problem_id':10300039,'audit_date':'2026-10-08','uid':os.geteuid(),
                      'python':sys.version,'audit_optimization':sys.flags.optimize,'outer_files':len(before),'author_packet_sha256':PACKET,
                      'author_manifest_sha256':MANIFEST,'bootstrap_sha256':BOOTSTRAP,
                      'actual_final_readonly_enforced':True,'original_unchanged':True,
                      'full_binding_replays':baseline,'readonly_relocated_replays':relocated,
                      'direct_malformed_guard_controls':parser_checks,'rejected_mutations':rejected,
                      'independent_external_bindings':external_bindings,
                      'rejected_mutation_count':len(rejected),'exact_math_controls':math_controls(),
                      'scope':'proofs reviewed separately; finite controls do not prove Q10.1'},indent=2,sort_keys=True))

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('REJECT: '+str(exc),file=sys.stderr)
        sys.exit(2)
