"""Independent PR888 whole-package checks; outputs authored finite evidence only."""
from pathlib import Path
from fractions import Fraction as F
from math import factorial
from datetime import datetime, timezone
import hashlib
import io
import json
import os
import stat
import struct
import subprocess
import sys
import tempfile
import zipfile
import zlib

HERE = Path(__file__).resolve().parent
A = HERE.parent
C = A / 'candidate'
T = HERE / 'private_tmp'

def require(ok, reason):
    if not ok:
        raise ValueError(reason)

def sha(b):
    return hashlib.sha256(b).hexdigest()

def no_duplicate(items):
    d = {}
    for k,v in items:
        require(k not in d, 'duplicate JSON key')
        d[k] = v
    return d

def js(b):
    return json.loads(b, object_pairs_hook=no_duplicate,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))

def load_index(path, schema):
    d = js(path.read_bytes())
    require(set(d) == {'schema','problem_id','files'}, 'index exact keys')
    require(d['schema'] == schema and d['problem_id'] == '30005079', 'index identity')
    return d['files']

def authenticate():
    pin = A / 'final_package_engineering_01/CANDIDATE_CORE_PINS.json'
    require((len(pin.read_bytes()),sha(pin.read_bytes())) == (32964,'5321e2621183505838c7bc2dd195edf1d87791ab76673dade5b52ff50143c8ea'), 'external core pin')
    rows = js(pin.read_bytes())['files']
    names = [x['path'] for x in rows]
    require(len(names) == len(set(names)) == 179, '179 core files')
    require(len({n.casefold() for n in names}) == len(names), 'casefold distinct')
    actual_files, actual_dirs = set(), set()
    for p in C.rglob('*'):
        n = p.relative_to(C).as_posix()
        require(not p.is_symlink(), 'candidate symlink')
        if p.is_dir(): actual_dirs.add(n)
        else:
            require(stat.S_ISREG(p.stat().st_mode), 'candidate nonregular file')
            actual_files.add(n)
    require(actual_files == set(names), 'closed core file set')
    dirs = {str(p) for n in names for p in Path(n).parents if str(p) != '.'}
    require(actual_dirs == dirs, 'closed core directory set')
    for x in rows:
        require(set(x) == {'path','bytes','sha256'}, 'core row schema')
        b = (C / x['path']).read_bytes()
        require((len(b),sha(b)) == (x['bytes'],x['sha256']), 'core identity '+x['path'])
        if x['path'].endswith('.json'): js(b)
    outer = load_index(C/'CURRENT_PUBLICATION_MANIFEST.json','rank-two-fano-30005079-current-publication-v1')
    require({x['path'] for x in outer} == set(names)-{'CURRENT_PUBLICATION_MANIFEST.json'}, 'outer manifest closure')
    for x in outer:
        b = (C/x['path']).read_bytes()
        require((len(b),sha(b)) == (x['bytes'],x['sha256']), 'outer pin')
    inner = load_index(C/'verification/package_index.json','rank-two-fano-30005079-verification-v1')
    all_inner = {p.relative_to(C/'verification').as_posix():p.read_bytes() for p in (C/'verification').rglob('*') if p.is_file()}
    require(len(all_inner) == 150 and set(all_inner) == {x['path'] for x in inner}|{'package_index.json'}, '150 inner closure')
    for x in inner:
        b = all_inner[x['path']]
        require((len(b),sha(b)) == (x['bytes'],x['sha256']), 'inner pin')
    sm = (A/'SOURCE_MANIFEST.json').read_bytes()
    require((len(sm),sha(sm)) == (5587,'49a72d6bf90d3a74be69ed855c7a9cfc0f3b1d83a4e4e3ce997c0ca7c07d1cbc'), 'external source manifest')
    require(all_inner['root_evidence/SOURCE_MANIFEST.json'] == sm, 'source manifest copy')
    source_rows = js(sm)['files']
    require(len(source_rows) == 21 and sum(x['bytes'] for x in source_rows) == 98055,'source inventory')
    for x in source_rows:
        b = all_inner['source/'+x['path']]
        require((len(b),sha(b)) == (x['bytes'],x['sha256']), 'original source SHA')
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest() == x['git_blob'], 'Git blob identity')
        actual = subprocess.run(['git','cat-file','blob',x['git_blob']],cwd=A,capture_output=True)
        require(actual.returncode == 0 and actual.stdout == b, 'read-only actual Git blob compare')
    raw = (C/'rank-two-fano-verification.zip').read_bytes()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        require(z.namelist() == sorted(all_inner), 'sorted archive names')
        require(len(z.infolist()) == 150 and z.testzip() is None, 'archive CRC')
        require(all(z.read(n) == b for n,b in all_inner.items()), 'every archive member exact')
        require(not z.comment and z.start_dir + struct.unpack_from('<I',raw,len(raw)-10)[0] == len(raw)-22, 'terminal ZIP extent')
    for n in ['portable.py','note.tex','metadata.json','zenodo-deposit.json','README.md']:
        require((C/n).read_bytes() == all_inner[n], 'current copy '+n)
    require((C/'portable.py').read_bytes() == all_inner['publication_tools_01/portable.py'],'engineering tool copy')
    m = js((C/'metadata.json').read_bytes()); d = js((C/'zenodo-deposit.json').read_bytes())
    require(d['metadata'] == m and len(d['files']) == 2, 'two-asset deposit metadata')
    require(m['creators'] == [{'name':'Kriebel, Alec','affiliation':'Independent researcher','orcid':'0009-0001-9320-500X'}], 'sole exact author')
    wheels = A/'publication_tools_01/private_tmp/wheels'
    deps = js(all_inner['dependencies.json'])
    require({p.name for p in wheels.iterdir()} == {x['filename'] for x in deps['wheels']}, 'closed two wheel directory')
    for x in deps['wheels']:
        b=(wheels/x['filename']).read_bytes()
        require((len(b),sha(b)) == (x['bytes'],x['sha256']), 'independent official wheel pin')
    return {'core_files':179,'archive_members':150,'original_source_files':21,
            'original_source_bytes':98055,'actual_git_blobs_compared':21,'closed_trees':True,
            'metadata_copies_and_sole_author':True,'official_wheels_authenticated':2,
            'zip_bytes':len(raw),'zip_sha256':sha(raw)}, all_inner, raw

def own_math():
    ap=[(-1,0,[4,4,1]),(0,2,[4,-4,1])]; bp=[(-1,1,[2,1])]
    def moment(ps,k):
        return sum((F(c)*(F(hi**(k+i+1)-lo**(k+i+1),k+i+1))
                    for lo,hi,co in ps for i,c in enumerate(co)), F())
    require([moment(ap,0),moment(bp,0),moment(ap,1),moment(bp,1)] == [5,4,F(5,12),F(2,3)], 'independent exact moments')
    def transformed(ps,shift,power):
        terms={}
        for lo,hi,co in ps:
            polynomial=[0]+co
            for derivative in range(len(polynomial)):
                for endpoint,sign in [(hi,-1),(lo,1)]:
                    value=sum((F(c)*endpoint**i for i,c in enumerate(polynomial)),F())
                    key=(shift-endpoint,power-derivative-1)
                    terms[key]=terms.get(key,F())+sign*value
                polynomial=[(i+1)*polynomial[i+1] for i in range(len(polynomial)-1)]
        return {k:v for k,v in terms.items() if v}
    require(transformed(ap,2,4)=={(3,3):-1,(3,2):-1,(3,1):2,(3,0):6,(2,1):-16,(0,1):-4,(0,0):-6},'independent A identity by derivative recurrence')
    require(transformed(bp,1,3)=={(2,2):-1,(2,0):2,(0,2):-3,(0,1):-4,(0,0):-2},'independent B identity by derivative recurrence')
    signs=[]
    for n,ps,r,l1,lo,hi in [('a',ap,2,F(9,4),F('0.27379184'),F('0.27379185')),
                              ('b',bp,1,F(2),F('0.52761951'),F('0.52761953'))]:
        for t,want in [(lo,1),(hi,-1)]:
            mid=sum(((-t)**k*moment(ps,k+1)/factorial(k) for k in range(37)),F())
            err=3*l1*(r*t)**37/factorial(37)
            require(r*t<1 and (mid-err>0 if want==1 else mid+err<0),'independent rational bracket')
            signs.append({'root':n,'parameter':str(t),'sign':want,'rational_taylor_order':36})
    # The universal resultant argument is checked analytically in the report,
    # independently of the finite rational arithmetic evidence here.
    normals=[(1,0),(0,1),(-1,1),(0,-1)]
    require([x[0]*y[1]-x[1]*y[0] for x,y in zip(normals,normals[1:]+normals[:1])] == [1]*4,'fan determinants')
    return {'exact_masses':['5','4'],'exact_first_moments':['5/12','2/3'],
            'both_exponential_identities_by_polynomial_derivative_recurrence':True,
            'rational_taylor_brackets':signs,'fan_determinants':[1,1,1,1],
            'universal_irrationality':'Analytically checked separately; not inferred from finite controls.'}

def historical_evidence():
    envelopes=[]
    for m in sorted((C/'verification').glob('*/SAFE*MANIFEST.json')):
        rows=js(m.read_bytes())['files']; names={r['path'] for r in rows}
        require(len(names)==len(rows),'safe envelope unique paths')
        for r in rows:
            b=(m.parent/r['path']).read_bytes()
            require((len(b),sha(b))==(r['bytes'],r['sha256']),'safe envelope payload pin')
        actual={p.relative_to(m.parent).as_posix() for p in m.parent.rglob('*') if p.is_file()}
        require(actual==names|{m.name},'safe envelope exact closed copied payload')
        envelopes.append({'family':m.parent.name,'payload_files':len(rows),'manifest_sha256':sha(m.read_bytes())})
    ledger=js((C/'verification/priority_classical_01/SOURCE_LEDGER.json').read_bytes())
    primary=[]
    for r in ledger['bodies']:
        p=A/'priority_classical_01'/r['path']; b=p.read_bytes()
        require((len(b),sha(b))==(r['bytes'],r['sha256']),'classical primary body pin')
        primary.append({'family':'classical','id':r['id'],'bytes':len(b),'sha256':sha(b),'url':r['url']})
    ledger=js((C/'verification/priority_recent_01/EXTERNAL_SOURCE_PINS.json').read_bytes())
    for r in ledger['primary_pdf_bodies']:
        p=A/'priority_recent_01'/r['private_path']; b=p.read_bytes()
        require((len(b),sha(b))==(r['bytes'],r['sha256']),'recent primary body pin')
        primary.append({'family':'recent','bytes':len(b),'sha256':sha(b),'url':r['url']})
    original=js((A/'SOURCE_MANIFEST.json').read_bytes())['files']
    changed=[]
    for r in original:
        if (C/r['path']).read_bytes() != (C/'verification/source'/r['path']).read_bytes(): changed.append(r['path'])
    require(set(changed)=={'README.md','RESEARCH_LOG.md','PUBLICATION.md','LITERATURE_AND_SCOPE.md'},'exact four historical outer assembly changes')
    return {'closed_historical_safe_envelopes':envelopes,'primary_body_pin_observations':primary,
            'all_listed_primary_bytes_authenticated':True,
            'body_read_scope':'Relevant theorem bodies for proof inputs and direct Li-Li predecessor passages; not every page of all priority works.',
            'exact_changed_outer_original_roles':sorted(changed),'all21_source_copies_unchanged':True}

def finite_controls(inner, raw):
    tool=C/'portable.py'; namespace={'__name__':'independent_review_import','__file__':str(tool)}
    exec(compile(tool.read_bytes(),str(tool),'exec',optimize=0),namespace)
    records=[]
    def bad(label,fn):
        try: fn()
        except (ValueError,OSError,KeyError,TypeError,zipfile.BadZipFile,struct.error,zlib.error) as e:
            records.append({'control':label,'rejected':True,'exception':type(e).__name__})
        else: raise ValueError('negative control accepted '+label)
    for label,b in [('duplicate_keys',b'{"x":1,"x":2}'),('nan',b'{"x":NaN}'),('float_overflow',b'{"x":1e999}')]:
        bad(label,lambda b=b:namespace['strict_json'](b))
    for label,n in [('traversal','../x'),('absolute','/x'),('empty_component','a//b'),('dot_component','a/./b'),('backslash','a\\b')]:
        bad(label,lambda n=n:namespace['safe_name'](n))
    good={'path':'x','bytes':1,'sha256':'a'*64}
    for label,v in [('boolean_size',True),('negative_size',-1),('oversize',namespace['MAX_FILE']+1)]:
        bad(label,lambda v=v:namespace['pin_row']({**good,'bytes':v}))
    bad('unknown_index_key',lambda:namespace['typed_index'](b'{"schema":"x","problem_id":"30005079","files":[],"extra":1}','x'))
    bad('case_alias',lambda:namespace['rows_map']([good,{**good,'path':'X'}]))
    bad('directory_alias',lambda:namespace['rows_map']([{**good,'path':'a/x'},{**good,'path':'A/y'}]))
    bad('file_directory_collision',lambda:namespace['rows_map']([good,{**good,'path':'x/y'}]))
    bad('zip_prefix',lambda:namespace['zip_payloads'](b'JUNK'+raw,inner,True))
    bad('zip_suffix',lambda:namespace['zip_payloads'](raw+b'JUNK',inner,True))
    damaged=bytearray(raw); damaged[30+len(sorted(inner)[0])+3]^=1
    bad('raw_compressed_corruption',lambda:namespace['zip_payloads'](bytes(damaged),inner,True))
    # Change one raw local name while keeping the indexed central name.
    damaged=bytearray(raw); damaged[30]^=1
    bad('local_central_name_mismatch',lambda:namespace['zip_payloads'](bytes(damaged),inner,True))
    # A coherent ZIP can hide unused bytes after a DEFLATE stream. Repair every
    # offset/size after inserting one byte; ordinary ZipFile still reads it.
    first_size=struct.unpack_from('<I',raw,18)[0]
    nlen,xlen=struct.unpack_from('<HH',raw,26)
    insertion=30+nlen+xlen+first_size
    expanded=bytearray(raw[:insertion]+b'\0'+raw[insertion:])
    struct.pack_into('<I',expanded,18,first_size+1)
    central=struct.unpack_from('<I',raw,len(raw)-6)[0]+1
    struct.pack_into('<I',expanded,len(expanded)-6,central)
    for index in range(len(inner)):
        require(expanded[central:central+4]==b'PK\x01\x02','independent raw ZIP central traversal')
        nn,xx,cc=struct.unpack_from('<HHH',expanded,central+28)
        if index==0:
            struct.pack_into('<I',expanded,central+20,first_size+1)
        else:
            old=struct.unpack_from('<I',expanded,central+42)[0]
            struct.pack_into('<I',expanded,central+42,old+1)
        central+=46+nn+xx+cc
    expanded=bytes(expanded)
    with zipfile.ZipFile(io.BytesIO(expanded)) as permissive:
        require(all(permissive.read(n)==b for n,b in inner.items()),'ordinary reader accepts raw suffix fixture')
    bad('coherent_deflate_unused_suffix_ordinary_reader_accepts',lambda:namespace['zip_payloads'](expanded,inner,True))
    fixture=T/'controls'; fixture.mkdir(exist_ok=True)
    indexed=fixture/'indexed'; indexed.mkdir(exist_ok=True)
    (indexed/'x').write_bytes(b'x')
    bad('inside_indexed_output',lambda:namespace['output_preflight'](indexed,{'x':b'x'},indexed/'rank-two-fano-verification.zip'))
    existing=fixture/'rank-two-fano-verification.zip'; existing.write_bytes(b'x')
    bad('existing_output',lambda:namespace['output_preflight'](indexed,{'x':b'x'},existing))
    link=fixture/'linked'
    if not link.is_symlink(): link.symlink_to(indexed,target_is_directory=True)
    bad('symlink_output_traversal',lambda:namespace['output_preflight'](indexed,{'x':b'x'},link/'rank-two-fano-verification.zip'))
    extra=indexed/'extra'; extra.write_bytes(b'x')
    bad('closed_tree_extra',lambda:namespace['closed_tree'](indexed,{'x'}))
    # Original parser rejects a genuinely broken context independently of hash gates.
    root={"__name__":"independent_root_import","__file__":str(C/'verification/source/verify_publication.py')}
    exec(compile(inner['source/verify_publication.py'],'original verify_publication.py','exec',optimize=0),root)
    try: root['apply_unified'](b'wrong\n',b'--- a\n+++ b\n@@ -1 +1 @@\n-old\n+new\n')
    except RuntimeError: records.append({'control':'original_patch_context','rejected':True,'exception':'RuntimeError'})
    else: raise ValueError('damaged original patch accepted')
    return records

if __name__ == '__main__':
    auth,inner,raw=authenticate()
    result={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS',
            'authentication':auth,'independent_math':own_math(),
            'historical_evidence':historical_evidence(),
            'complementary_negative_controls':finite_controls(inner,raw),
            'scope':'Independent closure, identities, finite controls and exact rational checks; no formal proof or publication approval.'}
    (HERE/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'status':'PASS','core':179,'archive':150,'git_blobs':21,'negative_controls':len(result['complementary_negative_controls'])}))
