#!/usr/bin/env python3
"""Externally pinned, fail-closed replay of the jointly accepted SIRSN application.
Run a separately authenticated copy. Mandatory full inputs are never published.
This checks bytes and finite diagnostics, not an infinite-network theorem.
"""
import argparse, hashlib, io, json, os, re, shutil, stat, subprocess, sys, tempfile, zipfile
from pathlib import Path, PurePosixPath
PROBLEM_ID=9700036
PINS={'SIRSN_TREE_9700036_AUTHOR_EXTERNAL_MANIFEST.json': {'bytes': 1124, 'sha256': '8d3de572463b79fb308117515b3710fca0fb1075fdcda4f30ebb57666f066a7a'}, 'SIRSN_TREE_9700036_AUTHOR_SAFE_FREEZE.zip': {'bytes': 10688, 'sha256': '3008e91a1b89b12efe3b3e300e9957585b84d81db715cad3ba340cf38db6be4e'}, 'SIRSN_TREE_9700036_CLARIFIED_EXTERNAL_MANIFEST.json': {'bytes': 1437, 'sha256': '8ca08cc5e379eacfe306569d0bb27d2e1117cd8e3d8a20d8251e009793030210'}, 'SIRSN_TREE_9700036_CLARIFIED_SAFE.zip': {'bytes': 12085, 'sha256': '6b2264154ecdd680c2fd888d1d8c63d0b6bd0a3ba174dcece23b4fed677fe0a1'}, 'SIRSN_TREE_9700036_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json': {'bytes': 3542, 'sha256': '10fad30f5597967416659b0c30fbf06391edc51f310dc65f7e8536c522ecf3de'}, 'SIRSN_TREE_9700036_INDEPENDENT_AUDIT_SAFE.zip': {'bytes': 51564, 'sha256': 'ce002390c4c0e8513f127f5a90792106a6fdb8932d99e87f4634a4bd82d8acca'}, 'SIRSN_TREE_9700036_SECOND_REVIEW_EXTERNAL_MANIFEST.json': {'bytes': 2526, 'sha256': 'f35dcffc66011f363f63a9a7126e060f979f940783fe545b83610f0ffe382259'}, 'SIRSN_TREE_9700036_SECOND_REVIEW_SAFE.zip': {'bytes': 43254, 'sha256': '3d5e6f2db6d33bf74b8024410f1bf08c8d8b9a7ac9f8900f65f097a329a45287'}}

def require(value, message):
    if not value:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def metadata(raw):
    return {'bytes':len(raw), 'sha256':digest(raw)}


def strict_json(raw):
    def unique(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(raw, object_pairs_hook=unique,
                      parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))


def safe_name(name):
    p = PurePosixPath(name)
    require(isinstance(name, str) and name and str(p) == name and
            not p.is_absolute() and not any(x in ('..', '.') for x in p.parts) and
            '\\' not in name and '\x00' not in name, 'unsafe relative name')
    return p


def regular(path):
    path = Path(os.path.abspath(path))
    for part in [path, *path.parents]:
        require(not part.is_symlink(), 'symlink input: ' + str(part))
    require(stat.S_ISREG(path.stat().st_mode), 'not a regular file: ' + str(path))
    return path.read_bytes()


def bound(raw, entry, label):
    require(type(entry['bytes']) is int and entry['bytes'] >= 0 and
            len(raw) == entry['bytes'] and digest(raw) == entry['sha256'],
            'byte binding mismatch: ' + label)


def inventory(root):
    root = Path(os.path.abspath(root))
    for part in [root, *root.parents]:
        require(not part.is_symlink(), 'symlink directory: ' + str(part))
    require(root.is_dir(), 'missing root directory')
    files, dirs = {}, set()
    for p in root.rglob('*'):
        require(not p.is_symlink(), 'symlink member')
        name = p.relative_to(root).as_posix()
        safe_name(name)
        if p.is_dir():
            dirs.add(name)
        else:
            files[name] = regular(p)
    return files, dirs


def compare_tree(root, expected):
    files, dirs = inventory(root)
    allowed_dirs = {q.as_posix() for n in expected for q in PurePosixPath(n).parents if q.as_posix() != '.'}
    require(set(files) == set(expected) and dirs == allowed_dirs, 'extracted inventory mismatch')
    for name, raw in files.items():
        bound(raw, expected[name], name)
        if name.endswith('.json'):
            strict_json(raw)
    return files


def archive(raw, manifest):
    bound(raw, manifest['zip'], 'archive')
    entries = manifest['files']
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        infos = z.infolist()
        names = [i.filename for i in infos]
        require(len(names) == len(set(names)) and set(names) == set(entries), 'ZIP member inventory')
        files = {}
        for info in infos:
            safe_name(info.filename)
            kind = stat.S_IFMT(info.external_attr >> 16)
            require(not info.is_dir() and kind in (0, stat.S_IFREG) and not info.flag_bits & 1,
                    'ZIP special node or encrypted member')
            require(info.file_size == entries[info.filename]['bytes'], 'ZIP advertised size mismatch')
            data = z.read(info)
            bound(data, entries[info.filename], 'ZIP member ' + info.filename)
            if info.filename.endswith('.json'):
                strict_json(data)
            files[info.filename] = data
    return files


def unpack(raw, manifest, prefix, members_key, archive_key):
    entries={prefix+n:r for n,r in manifest[members_key].items()}
    result=archive(raw, {'zip':manifest[archive_key], 'files':entries})
    return {n[len(prefix):]:b for n,b in result.items()}


def publication_gate(root, pin):
    require(re.fullmatch('[0-9a-f]{64}',pin) is not None,'external manifest pin format')
    raw=regular(root/'PUBLICATION_MANIFEST.json')
    require(digest(raw)==pin,'external publication manifest pin')
    m=strict_json(raw)
    require(m['problem_id']==PROBLEM_ID and m['rank']==936 and
            m['disposition']=='already_solved' and m['original_search_approaches_used']==0,
            'publication disposition')
    require('PUBLICATION_MANIFEST.json' not in m['files'],'self binding')
    files=compare_tree(root,{**m['files'],'PUBLICATION_MANIFEST.json':metadata(raw)})
    for name,record in PINS.items():bound(files['archives/'+name],record,name)
    specs=[('author','AUTHOR','SAFE_FREEZE.zip','sirsn_tree_9700036/','package_members','zip'),
           ('clarified','CLARIFIED','SAFE.zip','sirsn_tree_9700036/','package_members','zip'),
           ('audit','INDEPENDENT_AUDIT','SAFE.zip','sirsn_tree_9700036_independent_audit/','package_members','zip'),
           ('second_review','SECOND_REVIEW','SAFE.zip','second_review/','members','archive')]
    packages={};manifests={}
    for dest,tag,suffix,prefix,mkey,akey in specs:
        base='archives/SIRSN_TREE_9700036_'+tag+'_'
        manifest=strict_json(files[base+'EXTERNAL_MANIFEST.json'])
        contents=unpack(files[base+suffix],manifest,prefix,mkey,akey)
        require({n[len(dest)+1:]:b for n,b in files.items() if n.startswith(dest+'/')}==contents,'archive/extracted mismatch '+dest)
        packages[dest]=contents;manifests[dest]=manifest
    author,clarified,audit,second=[packages[x] for x in ['author','clarified','audit','second_review']]
    require({n[7:]:b for n,b in audit.items() if n.startswith('author/')}==author,'audit author freeze')
    require({n[9:]:b for n,b in audit.items() if n.startswith('accepted/')}==clarified,'audit clarified target')
    require(audit['SOURCE_PROOF_REPAIR.md']==second['SOURCE_PROOF_REPAIR_V1.md'],'same exact repair accepted twice')
    first=strict_json(audit['ACCEPTANCE.json']);last=strict_json(second['ACCEPTANCE.json'])
    require(first['claim_status']=='ACCEPTED_PRIOR_LITERATURE_RESOLUTION' and
            first['recommended_queue_disposition']=='already_solved' and first['original_search_approaches_used']==0,
            'first acceptance')
    bound(clarified['RESULT.md'],first['application_result'],'first application target')
    bound(audit['SOURCE_PROOF_REPAIR.md'],first['source_proof_repair'],'first repair target')
    bound(audit['CLARIFICATION.patch'],first['clarification_patch'],'exact clarification patch')
    require(last['decision']=='ACCEPT_COMBINED_CLARIFIED_APPLICATION_AND_REPAIR_V1' and
            last['original_author_archive_standalone_accepted'] is False and
            last['human_peer_review'] is False and last['formal_verification'] is False and
            last['novelty_claim'] is False,'second exact acceptance scope')
    bound(second['SECOND_REVIEW.md'],last['report'],'second report')
    bound(clarified['RESULT.md'],last['clarified_result'],'second application')
    for name,record in last['accepted_targets'].items():
        data=second[name] if name.endswith('.md') else files['archives/'+name]
        bound(data,record,'second target '+name)
    for n,b in second.items():
        if n.startswith('inputs/'):require(b==files['archives/'+n[7:]],'second nested freeze '+n)
    bound(audit['MANIFEST.json'],manifests['audit']['audit_manifest'],'inner audit manifest')
    return m,files,packages,manifests


def input_gate(a, packages):
    source=strict_json(packages['clarified']['SOURCE_MANIFEST.json']);corpora={};out={'corpora':{},'pdfs':{}}
    for key,path in [('catalog',a.catalog),('problems',a.problems),('research_results',a.reports)]:
        raw=regular(path);bound(raw,source['corpora'][key],'complete '+key)
        corpus=strict_json(raw);corpora[key]=corpus;out['corpora'][key]={**metadata(raw),'records':len(corpus)}
    records=[p for p in corpora['problems'] if str(p.get('id'))=='9700036']
    catalogs=[p for p in corpora['catalog'] if str(p.get('id'))=='9700036']
    require(len(records)==len(catalogs)==1,'unique exact ID')
    p,c=records[0],catalogs[0]
    require(p['problem_number']==c['problem_number']=='AMR-096-0036' and c['rank']==936,'exact rank/number')
    require(p['problem_number'] in corpora['research_results'],'complete report present')
    pair=json.dumps([p,corpora['research_results'].get(p['problem_number'],{})],sort_keys=True).encode()
    bound(pair,source['canonical_pair'],'canonical full array')
    require(digest(pair)==c['review_hash'],'catalog review hash')
    require(regular(a.sources_dir/'canonical_pair.private.json')==pair,'saved canonical bytes')
    require(strict_json(regular(a.sources_dir/'catalog_record.private.json'))==c,'saved catalog record')
    variants={'wrapper':{'problem':p,'report':corpora['research_results'][p['problem_number']]},'projection':[{'id':p['id']},corpora['research_results'][p['problem_number']]],'missing_report':[p,{}],'reversed':[corpora['research_results'][p['problem_number']],p]}
    out['canonical_shape_controls']={k:digest(json.dumps(v,sort_keys=True).encode())!=digest(pair) for k,v in variants.items()}
    require(all(out['canonical_shape_controls'].values()),'canonical negative controls')
    out['canonical_pair']={**metadata(pair),'matches_catalog_review_hash':True,'exact_saved_bytes_match':True}
    for s in source['sources']:
        if s.get('local_pdf'):
            record=s['local_pdf'];raw=regular(a.sources_dir/record['filename']);bound(raw,record,'PDF '+record['filename'])
            require(raw.startswith(b'%PDF'),'PDF format')
            out['pdfs'][record['filename']]=metadata(raw)
    require(len(out['pdfs'])==4,'four PDF coverage')
    return out


def write_tree(root,files):
    root.mkdir()
    for name,raw in files.items():
        p=root/safe_name(name);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)


def run(cmd,cwd,success,label):
    r=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=180)
    require((r.returncode==0)==success,'unexpected result '+label+': '+r.stderr)
    return {'test':label,'expected':'pass' if success else 'reject','returncode':r.returncode,
            'stdout':r.stdout.strip(),'stderr':r.stderr.strip().replace(str(cwd),'RELOCATED')}


def execute(a,files,packages,manifests,work):
    roots={}
    for name,contents in packages.items():
        roots[name]=work/('relocated '+name);write_tree(roots[name],contents)
    inputs=work/'external inputs';inputs.mkdir()
    options=['--catalog',str(a.catalog),'--problems',str(a.problems),'--reports',str(a.reports),'--sources-dir',str(a.sources_dir)]
    results=[]
    for opt in [False,True]:
        py=[sys.executable,'-I','-B']+(['-O'] if opt else [])
        cmd=py+[str(roots['audit']/'verify_audit.py'),'--manifest-sha',manifests['audit']['audit_manifest']['sha256'],
                '--author-zip',str(a.publication_root/'archives/SIRSN_TREE_9700036_AUTHOR_SAFE_FREEZE.zip'),
                '--clarified-zip',str(a.publication_root/'archives/SIRSN_TREE_9700036_CLARIFIED_SAFE.zip')]+options
        r=run(cmd,work,True,'first audit full relocated '+str(opt));v=strict_json(r['stdout'])
        require(v['status']=='PASS' and v['audit_files_bound']==19,'first audit bound count')
        for variant in ['author','accepted']:
            require(v['outcomes'][variant]['complete_corpora_checked'] is True and v['outcomes'][variant]['pdfs_checked']==4,'first replay full inputs')
        results.append(r)
        r=run(py+[str(roots['second_review']/'verify_second_review.py')],work,True,'second review relocated '+str(opt))
        require(strict_json(r['stdout'])['input_pins_verified']==5,'second replay target count');results.append(r)
        for flavor in ['author','clarified']:
            root=roots[flavor];cmd=py+[str(root/'verify.py')]
            for name in ['RESULT.md','verify.py','SOURCE_MANIFEST.json','CERTIFICATE.json']:
                p=root/name;old=p.read_bytes()
                if name=='CERTIFICATE.json':
                    bad=strict_json(old);bad['problem_id']=0;p.write_text(json.dumps(bad))
                else:p.write_bytes(old+b'\n')
                try:results.append(run(cmd,work,False,flavor+' mutated '+name+' '+str(opt)))
                finally:p.write_bytes(old)
            for kind in ['extra_file','extra_directory','symlink']:
                p=root/('unexpected' if kind!='symlink' else 'README.md');old=None
                if kind=='extra_file':p.write_text('tamper')
                elif kind=='extra_directory':p.mkdir()
                else:old=p.read_bytes();p.unlink();p.symlink_to(a.publication_root/flavor/'README.md')
                try:results.append(run(cmd,work,False,flavor+' '+kind+' '+str(opt)))
                finally:
                    if kind=='extra_directory':p.rmdir()
                    else:p.unlink()
                    if old is not None:p.write_bytes(old)
            results.append(run(cmd,work,True,flavor+' restored '+str(opt)))
        repair=roots['audit']/'SOURCE_PROOF_REPAIR.md';old=repair.read_bytes();repair.write_bytes(old+b'\n')
        try:results.append(run(py+[str(roots['audit']/'verify_audit.py'),'--manifest-sha',manifests['audit']['audit_manifest']['sha256']],work,False,'first repair tamper '+str(opt)))
        finally:repair.write_bytes(old)
        repair=roots['second_review']/'SOURCE_PROOF_REPAIR_V1.md';old=repair.read_bytes();repair.write_bytes(old+b'\n')
        try:results.append(run(py+[str(roots['second_review']/'verify_second_review.py')],work,False,'second repair tamper '+str(opt)))
        finally:repair.write_bytes(old)
    patched=work/'exact patch replay';write_tree(patched,packages['author'])
    patch=run(['patch','-p1','--batch','--forward','--fuzz=0','-i',str(roots['audit']/'CLARIFICATION.patch')],patched,True,'exact clarified derivative')
    require('offset' not in patch['stdout'].lower() and 'fuzz' not in patch['stdout'].lower(),'nonexact patch')
    actual=compare_tree(patched,{n:metadata(b) for n,b in packages['clarified'].items()})
    require(actual==packages['clarified'],'patch differs from exact accepted five files')
    return {'runs':results,'exact_patch_replay':patch,'accepted_files':{n:metadata(b) for n,b in actual.items()},
            'passes':sum(r['expected']=='pass' for r in results),'negative_controls':sum(r['expected']=='reject' for r in results)}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for name in ['publication-root','catalog','problems','reports','sources-dir']:
        parser.add_argument('--'+name,type=Path,required=True)
    parser.add_argument('--manifest-sha256',required=True);parser.add_argument('--receipt',type=Path)
    a=parser.parse_args()
    for name in ['publication_root','catalog','problems','reports','sources_dir']:setattr(a,name,getattr(a,name).absolute())
    manifest,files,packages,manifests=publication_gate(a.publication_root,a.manifest_sha256)
    # No package code has run before all public bytes and all seven external inputs pass.
    validation=input_gate(a,packages)
    with tempfile.TemporaryDirectory(prefix='sirsn-tree-publication-') as td:
        execution=execute(a,files,packages,manifests,Path(td))
    receipt={'status':'PASS','problem_id':9700036,'rank':936,'disposition':'already_solved','original_search_approaches_used':0,
             'publication_manifest_sha256':a.manifest_sha256,'publication_files_bound':len(manifest['files']),
             'full_corpus_source_validation':validation,'execution':execution,
             'scope':'Externally anchored integrity and finite diagnostics. The combined mathematical argument is independently AI-reviewed, not human peer reviewed or formally verified. No new theorem attribution.'}
    if a.receipt:
        require(a.publication_root not in a.receipt.absolute().parents,'receipt outside publication root')
        a.receipt.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps(receipt,sort_keys=True))


if __name__=='__main__':
    try:main()
    except (OSError,ValueError,KeyError,TypeError,zipfile.BadZipFile,subprocess.SubprocessError) as exc:
        print('FAIL: '+str(exc),file=sys.stderr);sys.exit(1)
