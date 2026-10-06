#!/usr/bin/env python3
"""Authenticate exact publication bytes before running frozen mathematical checks."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REJECT: invoke with -I -S -B')
import argparse,hashlib,io,json,os,pathlib,stat,subprocess,tempfile,zipfile
PINS = {'AUDIT_SAFE.zip': (52675, 'f0ecba020112e5644a1d871cd1506cc093ae70c39740328af88d5460dc4a5c35'), 'AUDIT_EXTERNAL_MANIFEST.json': (4854, '9eb070a8fe39db9240a749aee4dcb084413216bf6bb92ba4d9f9de4ea5253b50'), 'audit/TAUT_LEAF_GENUS_2999_AUTHOR_SAFE_FREEZE.zip': (15006, 'a1f4ad02d89248ad6a1f0d499951ee0233a58d00083b0ca2d08156d0ac661b03'), 'audit/TAUT_LEAF_GENUS_2999_AUTHOR_EXTERNAL_MANIFEST.json': (2441, '3935a18df9c3d3ea2b75772cfcd89c008637769958052f3e6c960743be0f867e'), 'audit/TAUT_LEAF_GENUS_2999_CORRECTED_SAFE.zip': (15131, '00a3f03d3febfb7dc7df0799c50387f6de7d6c57caeec6b3ebeb5f67c1b2e352'), 'audit/TAUT_LEAF_GENUS_2999_CORRECTED_EXTERNAL_MANIFEST.json': (2192, '829f0d5f4ea9f525a9efaa7bb21afdf4d1db32274ee48c59205bb3c046172d08'), 'audit/CHECKER_SCOPE_HARDENING.patch': (896, '8dbe26341ad93a02984027f99439c83b8c339edbaf48c2325c5e47553a41dbd9'), 'audit/EXACT_ACCEPTANCE.json': (2257, '981579beb5a1c95094601d3d7b0c9677abce8c60581165aaf32891cd127dc001'), 'second_review/INDEPENDENT_MATHEMATICAL_SOURCE_MANIFEST.json': (2923, '85f546fc336d8934fb15a973fdbcb239d84479ba056212ed4742ace4afcd7af1'), 'second_review/CORRECTED_ARCHIVE_MATHEMATICAL_ACCEPTANCE_BRIDGE.json': (1600, 'ade7886b106c2abf95f4cfc797cd52fd0bbddb70a6fc55acb8e9e66bfc5d5969'), 'second_review/INDEPENDENT_MATHEMATICAL_SOURCE_REVIEW.md': (13741, 'd6be9460097a42634b7e4af55a8466cf272565e91c478f9fe137d00e5230e6f6')}
def need(ok,msg):
    if not ok:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(items):
    d={}
    for k,v in items:
        need(k not in d,'duplicate JSON key');d[k]=v
    return d
def decode(b):return json.loads(b,object_pairs_hook=pairs)
def safe_name(n):
    p=pathlib.PurePosixPath(n)
    return bool(n) and not p.is_absolute() and p.as_posix()==n and all(c not in ('','..','.') for c in p.parts) and '\\' not in n and '\x00' not in n
def regular(p):
    need(stat.S_ISREG(p.lstat().st_mode),'not a regular file: '+p.name);return p.read_bytes()
def members(b,manifest):
    expected={e['path']:e for e in manifest['entries']}
    need(len(expected)==len(manifest['entries']),'duplicate manifest member')
    need((len(b),sha(b))==(manifest['zip']['bytes'],manifest['zip']['sha256']),'archive manifest mismatch')
    with zipfile.ZipFile(io.BytesIO(b)) as z:
        infos=z.infolist();names=[i.filename for i in infos]
        need(len(names)==len(set(names)) and set(names)==set(expected),'exact ZIP inventory')
        result={}
        for i in infos:
            need(safe_name(i.filename),'unsafe ZIP path')
            need(not i.is_dir() and not (i.flag_bits&1),'ZIP directory/encryption')
            need(stat.S_IFMT(i.external_attr>>16) in (0,stat.S_IFREG),'ZIP special member')
            b=z.read(i);e=expected[i.filename]
            need((len(b),sha(b))==(e['bytes'],e['sha256']),'ZIP member pin: '+i.filename)
            result[i.filename]=b
        need(z.testzip() is None,'ZIP CRC')
    return result
def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--expected-manifest',required=True)
    for k in ['catalog','problems','reports','source-dir']:ap.add_argument('--'+k)
    args=ap.parse_args();anchor=args.expected_manifest
    need(len(anchor)==64 and all(c in '0123456789abcdef' for c in anchor),'invalid external trust anchor')
    root=pathlib.Path(__file__).absolute().parent
    need(all(not p.is_symlink() for p in [root,*root.parents]),'symlink root ancestry')
    mb=regular(root/'PUBLICATION_MANIFEST.json');need(sha(mb)==anchor,'publication manifest anchor mismatch')
    manifest=decode(mb);need(manifest['schema']=='taut-leaf-publication-v1' and manifest['problem_id']==2999,'manifest identity')
    entries=manifest['files'];names=[e['path'] for e in entries]
    need(len(names)==len(set(names)) and 'PUBLICATION_MANIFEST.json' not in names,'manifest inventory')
    need(all(safe_name(n) for n in names),'unsafe manifest path')
    dirs={str(p) for n in names for p in pathlib.PurePosixPath(n).parents if str(p)!='.'}
    actual=set()
    for p in root.rglob('*'):
        rel=p.relative_to(root).as_posix();mode=p.lstat().st_mode
        if stat.S_ISDIR(mode):need(rel in dirs,'unexpected directory')
        else:need(stat.S_ISREG(mode),'symlink or special file');actual.add(rel)
    need(actual==set(names)|{'PUBLICATION_MANIFEST.json'},'publication file inventory')
    data={}
    for e in entries:
        b=regular(root/e['path']);need(type(e['bytes']) is int and (len(b),sha(b))==(e['bytes'],e['sha256']),'publication member binding: '+e['path']);data[e['path']]=b
    for n,pin in PINS.items():need((len(data[n]),sha(data[n]))==pin,'immutable pin: '+n)
    meta=decode(data['PUBLICATION_METADATA.json'])
    need(meta['rank']==923 and meta['problem_id']==2999 and meta['status']=='unsolved' and meta['turns']=='2/5','publication identity/status')
    need(meta['full_original_resolution'] is False and meta['novelty_claimed'] is False and meta['result_class']=='formulation_counterexample_only','publication claim scope')
    for k,v in {'literal_K3_weak_condition':'refuted','original_Kronheimer_closed_positive_form_question':'unresolved_by_this_work','S2_times_S2_subquestion':'not_resolved','nonzero_homology_variant':'not_refuted','chi_minus_variant':'not_refuted'}.items():need(meta[k]==v,'publication exclusion: '+k)
    ar='audit/TAUT_LEAF_GENUS_2999_'
    packets=[('audit','AUDIT_SAFE.zip','AUDIT_EXTERNAL_MANIFEST.json','taut_leaf_genus_2999_independent_audit/'),('original',ar+'AUTHOR_SAFE_FREEZE.zip',ar+'AUTHOR_EXTERNAL_MANIFEST.json','taut_leaf_genus_2999/'),('corrected',ar+'CORRECTED_SAFE.zip',ar+'CORRECTED_EXTERNAL_MANIFEST.json','taut_leaf_genus_2999/')]
    inventories={}
    for folder,archive,mf,prefix in packets:
        mm=members(data[archive],decode(data[mf]));need(all(n.startswith(prefix) for n in mm),'unexpected ZIP prefix')
        mm={n[len(prefix):]:b for n,b in mm.items()};actual_members={n[len(folder)+1:]:b for n,b in data.items() if n.startswith(folder+'/')}
        need(mm==actual_members,'exact ZIP/extracted membership: '+folder);inventories[folder]=len(mm)
    acceptance=decode(data['audit/EXACT_ACCEPTANCE.json'])
    need(acceptance['decision']=='ACCEPT_FORMULATION_COUNTEREXAMPLE_ONLY_WITH_CHECKER_SCOPE_HARDENING' and acceptance['queue_status']=='unsolved' and acceptance['turns_used']==2 and acceptance['full_original_resolution'] is False,'acceptance scope')
    original={n[9:]:b for n,b in data.items() if n.startswith('original/')};corrected={n[10:]:b for n,b in data.items() if n.startswith('corrected/')}
    need(set(original)==set(corrected),'derivative inventory')
    need([n for n in original if original[n]!=corrected[n]]==['check.py'],'only checker changed')
    report=decode(data['second_review/INDEPENDENT_MATHEMATICAL_SOURCE_MANIFEST.json'])
    need((len(data['second_review/'+report['report']['name']]),sha(data['second_review/'+report['report']['name']]))==(report['report']['bytes'],report['report']['sha256']),'second review report binding')
    corpus={k:getattr(args,k) for k in ['catalog','problems','reports']};supplied=sum(v is not None for v in corpus.values());need(supplied in (0,3),'supply all three corpus files or none')
    corpus={k:str(pathlib.Path(v).absolute()) for k,v in corpus.items()} if supplied else {}
    sources=[]
    if args.source_dir:
        sd=pathlib.Path(args.source_dir).absolute();filenames={'K3':'k3.pdf','K98':'kronheimer.pdf','OS00':'ozsvath_szabo.pdf','S03':'scorpan.pdf','B11':'bowden.pdf'}
        for s in decode(data['audit/SOURCE_VERIFICATION.json'])['sources']:
            b=regular(sd/filenames[s['key']]);need((len(b),sha(b))==(s['pdf_bytes'],s['pdf_sha256']),'source binary pin: '+s['key']);sources.append({'key':s['key'],'bytes':len(b),'sha256':sha(b),'match':True,'fresh_retrieval_this_run':False})
    runs=[]
    with tempfile.TemporaryDirectory(prefix='taut leaf authenticated snapshot ') as td:
        td=pathlib.Path(td);snapshot=td/'packet';snapshot.mkdir();cwd=td/'unrelated cwd';cwd.mkdir()
        for n,b in data.items():p=snapshot/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
        env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
        flags=['-I','-S','-B']+(['-O'] if sys.flags.optimize else [])
        def run(entry,extra):
            r=subprocess.run([os.path.realpath(sys.executable),*flags,str(entry),*extra],cwd=cwd,env=env,capture_output=True,timeout=180)
            need(r.returncode==0 and not r.stderr,'authenticated child failed: '+r.stderr.decode(errors='replace'));return decode(r.stdout)
        for folder in ['original','corrected']:
            extra=['--self-test']+[t for k,v in corpus.items() for t in ['--'+k,v]];result=run(snapshot/folder/'check.py',extra)
            need(result['math']['original_closed_form_problem_solved'] is False and result['self_test']['deliberately_false_checks_rejected']==3,'checker result scope');runs.append({'checker':folder,'result':result})
        result=run(snapshot/'audit/independent_algebra_check.py',[]);need(result['independent_tensor_calculation']=='PASS' and result['contracted_components_checked']==4374,'independent algebra result');runs.append({'checker':'independent_algebra','result':result})
        patchroot=td/'patch replay';(patchroot/'taut_leaf_genus_2999').mkdir(parents=True)
        for n,b in original.items():(patchroot/'taut_leaf_genus_2999'/n).write_bytes(b)
        p=subprocess.run(['patch','--batch','--fuzz=0','-p1','-i',str(snapshot/'audit/CHECKER_SCOPE_HARDENING.patch')],cwd=patchroot,env=env,capture_output=True,timeout=20)
        need(p.returncode==0 and b'fuzz' not in p.stdout.lower() and b'offset' not in p.stdout.lower(),'actual patch failed')
        resulting={p.name:regular(p) for p in (patchroot/'taut_leaf_genus_2999').iterdir()};need(resulting==corrected,'patched bytes differ from accepted derivative')
    print(json.dumps({'result':'pass','problem_id':2999,'status':'unsolved','turns':'2/5','optimized':bool(sys.flags.optimize),'files_verified':len(data)+1,'zip_member_counts':inventories,'authenticated_snapshot':True,'descendants_isolated_no_site_no_bytecode':True,'actual_patch_replayed':True,'only_check_py_changed':True,'sources_rehashed':sources,'full_corpus_replayed':bool(corpus),'runs':runs},sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:print(json.dumps({'result':'fail','error':str(e)},sort_keys=True),file=sys.stderr);sys.exit(1)
