#!/usr/bin/env python3
"""Portable frozen-byte and mathematical replay checks. Python 3.10+, offline."""
from pathlib import Path, PurePosixPath
import copy, hashlib, importlib.util, json, re, subprocess, sys, tempfile

AUTHOR = '0a585b480317c19cc8fd53e08a322d87661e1c8076ff1a49d37e62e77dd1549d'
AUDIT = 'da87f9d32c422bd7ad77afbeff12806b6bb75dd1eab512d4c5ece35458b46165'
AUTHOR_FILES = {'MANIFEST.json','PROOF.md','LIMITATIONS.md','run_tests.py','certificate.json','APPROACH_LOG.md','check_certificate.py','TEST_RESULTS.json','README.md','SOURCE_VERIFICATION.json','verify_faces.py'}
AUDIT_FILES = {'mutation-results.json','author-regression.log','AUDIT_BINDING.json','AUDIT_REPORT.md','independent-results.log','SOURCE_AUDIT.json','author-certificate.log','independent-results.json','independent_polytope_check.py','author-enumeration.log'}
ROOT_FILES = {'README.md','RELEASE_ADDENDUM.md','PUBLICATION_PROVENANCE.json','verify_release.py'}
EXPECTED = ROOT_FILES | {'author/'+n for n in AUTHOR_FILES} | {'audit/'+n for n in AUDIT_FILES}

def require(ok, why):
    if not ok: raise ValueError(why)

def sha(b): return hashlib.sha256(b).hexdigest()

def pairs(items):
    result = {}
    for k,v in items:
        require(k not in result, 'duplicate JSON key: '+k)
        result[k] = v
    return result

def readjson(path): return json.loads(path.read_bytes(), object_pairs_hook=pairs)

def inventory(root, entries, expected):
    require(isinstance(entries,list) and entries, 'invalid inventory')
    names = []
    for e in entries:
        require(isinstance(e,dict) and set(e)=={'path','bytes','sha256'},'invalid entry')
        name=e['path'];require(isinstance(name,str) and name and '\\' not in name,'invalid path')
        path=PurePosixPath(name)
        require(not path.is_absolute() and all(x not in ('','.','..') for x in name.split('/')) and path.as_posix()==name,'unsafe path')
        require(name not in names and name in expected,'duplicate or unexpected path')
        names.append(name)
        require(type(e['bytes']) is int and e['bytes']>=0,'invalid size')
        require(isinstance(e['sha256'],str) and re.fullmatch('[0-9a-f]{64}',e['sha256']) is not None,'invalid hash')
        p=root/name;require(p.is_file() and not p.is_symlink(),'missing or symlinked file')
        b=p.read_bytes();require(len(b)==e['bytes'] and sha(b)==e['sha256'],'byte mismatch: '+name)
    require(set(names)==expected,'incomplete inventory')

def frozen(root, filename, digest, key, expected):
    p=root/filename;require(sha(p.read_bytes())==digest,'frozen binding changed')
    z=readjson(p)
    inventory(root,[dict(path=n,**v) for n,v in z[key].items()],expected-{filename})
    return z

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def run(root):
    root=root.resolve()
    for p in root.rglob('*'): require(not p.is_symlink(),'symlink in packet')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    require(actual==EXPECTED|{'MANIFEST.json'},'missing or extra release file')
    m=readjson(root/'MANIFEST.json')
    require(m['schema']=='gelfand-zetlin-release-v1' and m['problem_id']==30001132,'wrong identity')
    require(m['disposition']=='already_solved' and m['turns']=='1/5','wrong disposition')
    require(m['author_manifest_sha256']==AUTHOR and m['audit_binding_sha256']==AUDIT,'wrong manifest binding')
    inventory(root,m['files'],EXPECTED)
    frozen(root/'author','MANIFEST.json',AUTHOR,'files',AUTHOR_FILES)
    a=frozen(root/'audit','AUDIT_BINDING.json',AUDIT,'audit_files',AUDIT_FILES)
    require(a['frozen_author_manifest']['sha256']==AUTHOR and a['verdict']=='PASS' and not a['material_findings'],'audit changed')
    p=readjson(root/'PUBLICATION_PROVENANCE.json')
    require(p['current_disposition']=='already_solved' and p['turns']=='1/5' and not p['novelty_claim'],'provenance changed')
    require(p['frozen_binding']=={'author_manifest_sha256':AUTHOR,'audit_binding_sha256':AUDIT},'provenance binding mismatch')
    require(set(p['queue']['changed_fields'])=={'Status','Turns','Findings'},'queue scope mismatch')
    def call(args): return subprocess.run([sys.executable,'-B']+list(map(str,args)),check=True,capture_output=True)
    regress=call([root/'author/run_tests.py'])
    require(b'Ran 6 tests' in regress.stderr and b'OK' in regress.stderr,'regression summary mismatch')
    cert=call([root/'author/check_certificate.py',root/'author/certificate.json'])
    require(cert.stdout==(root/'audit/author-certificate.log').read_bytes(),'certificate replay mismatch')
    with tempfile.TemporaryDirectory() as tmp:
        dest=Path(tmp)
        enum=call([root/'author/verify_faces.py','--output',dest/'enumeration.json'])
        require(enum.stdout==(root/'audit/author-enumeration.log').read_bytes(),'enumeration replay mismatch')
        independent=call([root/'audit/independent_polytope_check.py',root/'author/certificate.json','--output',dest/'independent.json'])
        require((dest/'independent.json').read_bytes()==(root/'audit/independent-results.json').read_bytes(),'independent result byte mismatch')
        require(independent.stdout==(root/'audit/independent-results.log').read_bytes(),'independent log mismatch')
        data=readjson(dest/'enumeration.json'); ind=readjson(dest/'independent.json')
        for case in ind['cases']:
            n=case['n']
            author=data[str(n)] if isinstance(data,dict) and str(n) in data else next(x for x in data if x['n']==n)
            require(author['nonrepresentable']==[list(map(int,x)) for x in case['nonrepresentable']],'class classification mismatch')
            expected={''.join(map(str,rec['w'])):[''.join(map(str,b)) for b in rec['admissible_borels']] for rec in author['records']}
            require(expected==case['admissible_borels_by_class'],'class/Borel decision mismatch')
    checker=module(root/'audit/independent_polytope_check.py','independent_release_check')
    source=readjson(root/'author/certificate.json'); mutations={}
    z=copy.deepcopy(source);z.pop();mutations['missing_borel']=z
    z=copy.deepcopy(source);z[-1]=copy.deepcopy(z[0]);mutations['duplicated_borel']=z
    z=copy.deepcopy(source);z[0]['sigma']=[1,2,3,4];mutations['wrong_composition']=z
    z=copy.deepcopy(source);z[0]['predecessor']=[2,4,1,3];z[0]['sigma_predecessor']=[2,4,1,3];mutations['not_a_cover']=z
    z=copy.deepcopy(source);z[0]['equality']=[[1,0],[0,0]];mutations['wrong_face_equation']=z
    z=copy.deepcopy(source);z[0]['top_labels_at_predecessor']=[1,1];mutations['wrong_coordinate_labels']=z
    rejected={}
    for name,z in mutations.items():
        try: checker.run((1,2,3,4),z)
        except (AssertionError,ValueError,StopIteration): rejected[name]='rejected'
        else: raise ValueError('invalid certificate accepted: '+name)
    require(rejected==readjson(root/'audit/mutation-results.json'),'mutation replay differs')
    return {'status':'PASS','problem_id':30001132,'disposition':'already_solved','turns':'1/5','release_files':len(actual),'manifested_payloads':len(EXPECTED),'frozen_author_files':len(AUTHOR_FILES),'frozen_audit_files':len(AUDIT_FILES),'author_regressions':6,'author_enumeration':'PASS_BYTE_IDENTICAL','author_certificate':'PASS_BYTE_IDENTICAL','independent_H_polytope_replay':'PASS_BYTE_IDENTICAL','independent_certificate_instances':72,'invalid_certificate_variants_rejected':len(rejected),'manifest_sha256':sha((root/'MANIFEST.json').read_bytes())}

if __name__=='__main__':
    sys.dont_write_bytecode=True
    try: print(json.dumps(run(Path(__file__).parent),indent=2))
    except (ValueError,KeyError,TypeError,OSError,subprocess.CalledProcessError) as e:
        print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
