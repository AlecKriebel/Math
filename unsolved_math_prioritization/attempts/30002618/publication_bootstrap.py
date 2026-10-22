"""Externally authenticate this file before execution. Standard library only."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.flags.dont_write_bytecode):
    raise SystemExit('REFUSED: Python -I -S -B required')
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import tempfile
import zipfile

PINS = {'ISOCRYSTAL_MONODROMY_30002618_AUTHOR_EXTERNAL_MANIFEST.json': (1327, '7a348b1bc2d5430ec84c790cf1758974227502220f902eea478a93f7cdc681ea'), 'ISOCRYSTAL_MONODROMY_30002618_AUTHOR_SAFE_FREEZE.zip': (11786, '0947c56eb1d4642ac9e92298022a21419aac91a740d1b0ee4ace588260dd2665'), 'ISOCRYSTAL_MONODROMY_30002618_CORRECTED_EXTERNAL_MANIFEST.json': (1291, '9fb9ecf3d28d5961d48490ea17446afb0465bf34fdc97c326e629703ccab0461'), 'ISOCRYSTAL_MONODROMY_30002618_CORRECTED_SAFE.zip': (12287, 'aa53b811b554fbd7655d4d18073c62ac49c65bcdc68dbf898f6e40e2286306d2'), 'ISOCRYSTAL_MONODROMY_30002618_INDEPENDENT_AUDIT_BOOTSTRAP.py': (4031, '7a6d637b0e5b9321d239a2d2f7a0621a8acd0aa60cacf8a3ce64a42fe128bb1c'), 'ISOCRYSTAL_MONODROMY_30002618_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json': (2770, 'd41f4a6db4e4e161182e90f54c189b670a20334a2029e6877decf79fe48132c1'), 'ISOCRYSTAL_MONODROMY_30002618_INDEPENDENT_AUDIT_RECEIPT.json': (7819, '6d89c347d24d2cbf13f0f9f7da5732299809658365e64057c16a402fd370e3c0'), 'ISOCRYSTAL_MONODROMY_30002618_INDEPENDENT_AUDIT_SAFE.zip': (27637, '98d9386a7b67b8dcb8c6de7ff57436dfd20342c9fb9dfb4f1941281d05f155a9')}

def need(ok, why):
    if not ok: raise ValueError(why)

def sha(b): return hashlib.sha256(b).hexdigest()

def unique(pairs):
    d = {}
    for k, v in pairs:
        need(k not in d, 'duplicate JSON key')
        d[k] = v
    return d

def parse(b): return json.loads(b, object_pairs_hook=unique)

def safe_path(p):
    p = Path(os.path.abspath(p))
    for ancestor in [p] + list(p.parents):
        need(not ancestor.is_symlink(), 'symlink path or ancestor')
    return p

def regular(p):
    safe_path(p)
    need(stat.S_ISREG(p.lstat().st_mode), 'nonregular file')
    need(p.stat().st_size < 2000000, 'file size ceiling')
    return p.read_bytes()

def verify(root, manifest_pin):
    root = safe_path(root)
    own = safe_path(__file__)
    need(own == root / 'publication_bootstrap.py', 'wrong operative entrypoint')
    need(stat.S_ISDIR(root.lstat().st_mode), 'non-directory root')
    mb = regular(root / 'PUBLICATION_MANIFEST.json')
    need(re.fullmatch('[0-9a-f]{64}', manifest_pin) is not None and sha(mb) == manifest_pin, 'external manifest pin mismatch')
    manifest = parse(mb)
    need(type(manifest) is dict and set(manifest) == {'schema', 'problem_id', 'files'}, 'manifest schema')
    need(type(manifest['schema']) is int and manifest['schema'] == 1, 'manifest version')
    need(type(manifest['problem_id']) is int and manifest['problem_id'] == 30002618, 'problem identity')
    entries = manifest['files']
    need(type(entries) is dict and entries, 'manifest entries')
    expected_dirs = set()
    for name, item in entries.items():
        path = PurePosixPath(name)
        need(type(name) is str and str(path) == name and not path.is_absolute() and '..' not in path.parts and '\\' not in name, 'unsafe manifest path')
        need(type(item) is dict and set(item) == {'bytes', 'sha256'}, 'entry schema')
        need(type(item['bytes']) is int and 0 <= item['bytes'] < 2000000, 'entry size')
        need(type(item['sha256']) is str and re.fullmatch('[0-9a-f]{64}', item['sha256']) is not None, 'entry digest')
        expected_dirs.update(str(p) for p in path.parents if str(p) != '.')
    files, dirs = set(), set()
    for base, names, fs in os.walk(root, followlinks=False):
        for name in names:
            p = Path(base) / name
            need(not p.is_symlink() and stat.S_ISDIR(p.lstat().st_mode), 'nonregular directory')
            dirs.add(str(p.relative_to(root)))
        for name in fs:
            p = Path(base) / name
            need(not p.is_symlink() and stat.S_ISREG(p.lstat().st_mode), 'nonregular inventory entry')
            files.add(str(p.relative_to(root)))
    need(files == set(entries) | {'PUBLICATION_MANIFEST.json'} and dirs == expected_dirs, 'strict package inventory')
    payload = {}
    for name, item in entries.items():
        b = regular(root / name)
        need(item == {'bytes': len(b), 'sha256': sha(b)}, 'package byte mismatch: ' + name)
        payload[name] = b
    for name, pin in PINS.items():
        b = payload[name]
        need((len(b), sha(b)) == pin, 'immutable input pin: ' + name)
    member_count = 0
    for folder,prefix in [('author','AUTHOR'),('corrected','CORRECTED'),('audit','INDEPENDENT_AUDIT')]:
        stem='ISOCRYSTAL_MONODROMY_30002618_'+prefix
        aname=stem+('_SAFE_FREEZE.zip' if folder=='author' else '_SAFE.zip')
        am=parse(payload[stem+'_EXTERNAL_MANIFEST.json'])
        need(am['archive_bytes']==len(payload[aname]) and am['archive_sha256']==sha(payload[aname]), 'archive manifest binding')
        member_count += check_archive(payload[aname],am['files'])
        with zipfile.ZipFile(io.BytesIO(payload[aname])) as z:
            for name in z.namelist():need(payload[folder+'/'+name]==z.read(name),'extracted member mismatch')
    for name in [p[len('corrected/'):] for p in payload if p.startswith('corrected/')]:
        need(payload['corrected/'+name]==payload['audit/corrected/'+name],'corrected audit copy differs')
    for prefix in ('AUTHOR','CORRECTED'):
        need(payload['ISOCRYSTAL_MONODROMY_30002618_'+prefix+'_EXTERNAL_MANIFEST.json']==payload['audit/'+prefix+'_EXTERNAL_MANIFEST.json'],'audit external manifest duplicate')
    acceptance=parse(payload['audit/ACCEPTANCE_REPORT.json']);status=parse(payload['corrected/STATUS.json']);meta=parse(payload['PUBLICATION_METADATA.json'])
    need(acceptance['verdict']=='ACCEPT_CORRECTED_RIGOROUS_PARTIAL' and acceptance['mathematical_findings']['full_solution'] is False and acceptance['mathematical_findings']['novelty_claimed'] is False,'acceptance scope')
    need(status['status']=='RIGOROUS_PARTIAL_INDEPENDENTLY_AUDITED' and status['approaches_used']==5 and status['approach_limit']==5 and status['full_solution_claimed'] is False and status['novelty_claimed'] is False,'corrected status')
    need(meta['canonical_status']=='unsolved' and meta['turns']=='5/5' and meta['new_proof_attempts_added']==0,'canonical status')
    v=parse(payload['corrected/verification.json']);corpus=parse(payload['audit/CORPUS_VERIFICATION.json']);fresh=parse(payload['PUBLICATION_SOURCE_BINDINGS.json'])
    for field in ('statement_sha256','review_sha256'):
        need(v[field]==corpus[field]==fresh[field],'full source binding')
    need(v['statement_sha256']=='a4bff93318d3db145c78df886926e3de618ed90e5e8bfd6a910de35b133e1dc0' and v['review_sha256']=='5eb4c6f3e31ac0d51d0bea619752f16f9bfd38ecee4c23801b8862107b2fb0ef','statement and record trust pins')
    need(v['corpora']==corpus['corpora'] and len(fresh['corpora'])==3,'corpus metadata')
    for old,new in zip(v['corpora'],fresh['corpora']):
        need(all(new[k]==val for k,val in old.items()) and new['fresh_bytes_and_hash_match'] is True,'fresh corpus bindings')
    sources=parse(payload['corrected/source_metadata.json'])['sources'];audit_sources=parse(payload['audit/SOURCE_RECHECK.json'])['sources'];fresh_sources=fresh['source_PDFs']
    need(len(sources)==len(audit_sources)==len(fresh_sources)==6,'six source records')
    for old,aud,new in zip(sources,audit_sources,fresh_sources):
        need(all(aud[k]==val==new[k] for k,val in old.items()) and new['fresh_retained_pdf_byte_match'] is True,'full source metadata tuple binding')
    return root,payload,{'verified':True,'problem_id':30002618,'package_files':len(files),'archive_members':member_count,'overall':'unsolved','turns':'5/5','correction_required_and_applied':True,'full_source_binding':True}

def check_archive(raw,entries):
    need(type(entries) is list and entries,'archive manifest entries')
    expected={}
    for e in entries:
        need(type(e) is dict and set(e)=={'path','bytes','sha256'},'archive entry schema')
        name=e['path'];path=PurePosixPath(name)
        need(name not in expected and str(path)==name and not path.is_absolute() and '..' not in path.parts and '\\' not in name,'unsafe or duplicate archive path')
        need(type(e['bytes']) is int and 0<=e['bytes']<2000000,'archive entry size')
        expected[name]=e
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        infos=z.infolist();need(len(infos)==len(expected) and {i.filename for i in infos}==set(expected),'strict archive inventory')
        need(z.testzip() is None,'archive CRC')
        for i in infos:
            mode=i.external_attr>>16
            need(i.create_system==3 and stat.S_ISREG(mode) and not mode&0o111 and not i.is_dir() and not i.flag_bits&1,'archive member type or executable')
            need(PurePosixPath(i.filename).suffix in ('.md','.json','.patch'),'archive extension')
            b=z.read(i);s=b.decode('utf-8');need('\0' not in s,'binary text')
            need(len(b)==expected[i.filename]['bytes'] and sha(b)==expected[i.filename]['sha256'],'archive bytes mismatch')
            if i.filename.endswith('.json'):parse(b)
    return len(expected)

def hostile_archives():
    import warnings
    b=b'{}\n';entry=lambda name,body:[{'path':name,'bytes':len(body),'sha256':sha(body)}]
    base=entry('test.json',b)
    cases=[('extra member',[('test.json',b,0o100444),('extra.md',b'extra',0o100444)],base),('missing member',[],base),('duplicate member',[('test.json',b,0o100444)]*2,base),('payload changed',[('test.json',b'[]\n',0o100444)],base),('path traversal',[('../test.json',b,0o100444)],entry('../test.json',b)),('executable mode',[('test.json',b,0o100555)],base),('symbolic link',[('test.json',b,0o120444)],base),('invalid UTF-8',[('test.json',b'\xff',0o100444)],entry('test.json',b'\xff')),('duplicate JSON keys',[('test.json',b'{"x":1,"x":2}',0o100444)],entry('test.json',b'{"x":1,"x":2}')),('invalid JSON',[('test.json',b'{]',0o100444)],entry('test.json',b'{]')),('NUL text',[('test.md',b'x\0y',0o100444)],entry('test.md',b'x\0y'))]
    records=[]
    for name,items,spec in cases:
        out=io.BytesIO()
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            with zipfile.ZipFile(out,'w') as z:
                for path,body,mode in items:
                    i=zipfile.ZipInfo(path);i.create_system=3;i.external_attr=mode<<16;z.writestr(i,body)
        try:check_archive(out.getvalue(),spec)
        except (ValueError,UnicodeDecodeError,zipfile.BadZipFile) as e:records.append({'case':name,'rejected':True,'reason':str(e)})
        else:raise ValueError('hostile archive accepted: '+name)
    return records

def replay(root,payload):
    results={}
    with tempfile.TemporaryDirectory(prefix='isocrystal-publication-') as td:
        work=Path(td);patchroot=work/'patch';patchroot.mkdir()
        for name,b in payload.items():
            if name.startswith('author/'):(patchroot/name.removeprefix('author/')).write_bytes(b)
        patch=work/'CORRECTION.patch';patch.write_bytes(payload['audit/CORRECTION.patch'])
        proc=subprocess.run(['patch','-p1','--batch','--fuzz=0','-i',str(patch)],cwd=patchroot,capture_output=True,timeout=40)
        need(proc.returncode==0 and not proc.stderr,'patch failure')
        expected={name.removeprefix('corrected/'):b for name,b in payload.items() if name.startswith('corrected/')}
        need(set(p.name for p in patchroot.iterdir())==set(expected),'post-patch inventory')
        need(all((patchroot/name).read_bytes()==b for name,b in expected.items()),'six-file patch reproduction')
        results['exact_patch_replay']={'fuzz':0,'file_count':len(expected),'all_six_corrected_files_byte_identical':True,'stdout':proc.stdout.decode()}
        script='publication_diagnostics.py';flags=[sys.executable,'-I','-S','-B']+(['-O'] if sys.flags.optimize else [])
        code='import sys;sys.argv=sys.argv[1:];__file__=sys.argv[0];exec(compile('+repr(payload[script])+',__file__,"exec"))'
        proc=subprocess.run(flags+['-c',code,str(root/script)],cwd=work,capture_output=True,timeout=60)
        need(proc.returncode==0 and not proc.stderr,'diagnostic replay failure: '+proc.stderr.decode());diagnostics=parse(proc.stdout);historical=parse(payload['audit/EXACT_DIAGNOSTICS.json'])
        for key in ('cycle_case_count','abstract_case_count','cycle_cases','abstract_cases'):need(diagnostics[key]==historical[key],'independent exact diagnostic mismatch')
        results['diagnostics']={'cycle_cases':48,'abstract_cases':30,'all_historical_case_records_match':True,'stdout_sha256':sha(proc.stdout),'result':diagnostics}
        results['hostile_archives']=hostile_archives();need(len(results['hostile_archives'])==11,'hostile count')
    return results

def main():
    need(len(sys.argv) in (3,4) and (len(sys.argv)==3 or sys.argv[3]=='--replay'),'usage: publication_bootstrap.py ROOT MANIFEST_SHA256 [--replay]')
    root,payload,result=verify(sys.argv[1],sys.argv[2])
    if len(sys.argv)==4:
        result['replays']=replay(root,payload)
        need(verify(root,sys.argv[2])[1]==payload,'input bytes mutated')
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':
    try:main()
    except (ValueError,OSError,TypeError,KeyError,zipfile.BadZipFile,subprocess.TimeoutExpired) as e:
        print('PUBLICATION VERIFICATION FAILED: '+str(e),file=sys.stderr);sys.exit(1)
