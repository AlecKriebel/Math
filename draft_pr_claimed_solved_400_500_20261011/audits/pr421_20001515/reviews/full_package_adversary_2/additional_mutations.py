"""Reviewer-designed mathematical and manifest falsification controls."""
import pathlib,json,subprocess,shutil,os,hashlib,ast,sys
CASE=pathlib.Path(__file__).resolve().parents[2]
OUT=pathlib.Path(__file__).resolve().parent
PRIVATE=CASE/'private_sources/full_package_adversary_2'
SOURCE=PRIVATE/'extracted_verification'
def need(c,m):
    if not c:raise ValueError(m)
def digest(b):return hashlib.sha256(b).hexdigest()
def main():
    destination=PRIVATE/'reviewer_mutations';destination.mkdir()
    env={**os.environ,'TMPDIR':str(PRIVATE/'tmp')};rows=[]
    cases=[
      ('one attaching edge inverted','verify.py',[("Q_LABELS = {1: 1, 2: 2, 3: 1, 4: 2, 5: 3, 6: 3}","Q_LABELS = {1: 1, 2: 2, 3: 1, 4: 2, 5: -3, 6: 3}")]),
      ('drop repeated A corner','audit/independent_audit.py',[("qlinks = {}","qcorners['A'].pop()\nqlinks = {}")]),
      ('identify opposite interval germs in actual cube','audit/independent_audit.py',[("vertical(qv, 1 if height == 0 else -1)","vertical(qv, 1)")]),
      ('invert top horizontal product boundary incorrectly','audit/independent_audit.py',[("zwords.append([l, vertical(v), inv(lamb(l)), vertical(u, -1)])","zwords.append([l, vertical(v), lamb(l), vertical(u, -1)])")]),
      ('wrong c inverse generator substitution','audit/independent_algebra.py',[("z = prod(inverse(c), inverse(t))","z = prod(c, inverse(t))")]),
      ('coherent different final-b automorphism','audit/independent_algebra.py',[("phi = {'a': 'a', 'b': 'ab', 'c': 'bcb'}","phi = {'a': 'a', 'b': 'ab', 'c': 'bcB'}"),("psi = {'a': 'a', 'b': 'Ab', 'c': 'BacBa'}","psi = {'a': 'a', 'b': 'Ab', 'c': 'BacAb'}")]),
    ]
    for i,(desc,program,replacements) in enumerate(cases):
        for optimized in (False,True):
            fixture=destination/(str(i)+(' O' if optimized else ' normal'));shutil.copytree(SOURCE/'packet',fixture)
            for out in ('checks.json','audit/independent_results.json','audit/independent_algebra_results.json'):(fixture/out).unlink()
            p=fixture/program;s=p.read_text()
            for a,b in replacements:need(s.count(a)==1,'nonunique mutation target');s=s.replace(a,b)
            p.write_text(s)
            ast.parse(s)
            r=subprocess.run([sys.executable,'-I','-S','-B']+(['-O'] if optimized else [])+[str(p)],cwd=PRIVATE,env=env,capture_output=True,text=True,timeout=60)
            tail=r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ''
            need(r.returncode!=0 and not r.stdout and tail.startswith('AssertionError'),'corruption not substantively rejected: '+desc+' '+r.stderr)
            need(not any((fixture/out).exists() for out in ('checks.json','audit/independent_results.json','audit/independent_algebra_results.json')),'corrupt result written')
            rows.append({'control':desc,'program':program,'mode':'-O' if optimized else 'normal','exit_code':r.returncode,'exception_tail':tail,'mutant_sha256':digest(p.read_bytes()),'successful_stdout_absent':True,'fresh_result_absent':True})
    integrity=[]
    for i,desc in enumerate(('unlisted empty directory','duplicate manifest JSON key','unsafe manifest traversal path','symlink member','coordinated script rehash')):
        for opt in (False,True):
            fixture=destination/('integrity'+str(i)+(' O' if opt else ' normal'));shutil.copytree(SOURCE,fixture)
            if i==0:(fixture/'unexpected').mkdir()
            if i==1:
                p=fixture/'MANIFEST.json';s=p.read_text();s=s.replace('"schema_version": 1','"schema_version": 1, "schema_version": 1');p.write_text(s)
            if i==2:
                p=fixture/'MANIFEST.json';m=json.loads(p.read_text());m['files'][0]['path']='../outside';p.write_text(json.dumps(m))
            if i==3:
                p=fixture/'packet/verify.py';p.unlink();p.symlink_to(SOURCE/'packet/verify.py')
            if i==4:
                p=fixture/'packet/verify.py';p.write_bytes(p.read_bytes()+b'\n# reviewer alteration\n')
                m=json.loads((fixture/'MANIFEST.json').read_text());w=json.loads((fixture/'PUBLIC_OUTPUT_WHITELIST.json').read_text())
                for doc in (m,w):
                    rec=next(x for x in doc['files'] if x['path']=='packet/verify.py');rec['bytes']=p.stat().st_size;rec['sha256']=digest(p.read_bytes())
                (fixture/'MANIFEST.json').write_text(json.dumps(m))
                rec=next(x for x in w['files'] if x['path']=='MANIFEST.json');rec['bytes']=(fixture/'MANIFEST.json').stat().st_size;rec['sha256']=digest((fixture/'MANIFEST.json').read_bytes())
                (fixture/'PUBLIC_OUTPUT_WHITELIST.json').write_text(json.dumps(w))
            r=subprocess.run([sys.executable,'-I','-S','-B']+(['-O'] if opt else [])+[str(fixture/'verify_bundle.py')],cwd=PRIVATE,env=env,capture_output=True,text=True,timeout=60)
            need(r.returncode!=0 and not r.stdout and 'VERIFICATION FAILED:' in r.stderr,'manifest corruption accepted')
            expected=['Unlisted/missing bundle directories','Duplicate JSON key','Unsafe or noncanonical manifest path','Symlink excluded','Accepted packet SHA-256 mismatch'][i]
            need(expected in r.stderr,'incidental integrity failure: '+r.stderr)
            integrity.append({'control':desc,'mode':'-O' if opt else 'normal','exit_code':r.returncode,'exact_rejection':r.stderr.strip(),'successful_stdout_absent':True})
    report={'mathematical_controls':rows,'integrity_controls':integrity,'controls_designed_by_current_reviewer':True,'normal_and_optimized':True}
    (OUT/'ADDITIONAL_MUTATION_RESULTS.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'mathematical_rejections':len(rows),'integrity_rejections':len(integrity),'all_substantive':True}))
if __name__=='__main__':main()
