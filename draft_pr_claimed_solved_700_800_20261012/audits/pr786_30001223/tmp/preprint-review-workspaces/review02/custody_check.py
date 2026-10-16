"""Independent read-only review02 custody checker with mandatory external pins."""
from pathlib import Path, PurePosixPath
import argparse, hashlib, io, json, os, re, stat, sys, zipfile
HEAD='34f21454986a28ca49f24999be3a0fd1b42755f8'
INPUT_PIN='c562c7328d8fda283f46d83d30de8de28a9476f1a4d2946688fba992199bb599'
SOURCE_PIN='32d7a891fa5ad3ff49269865e122f5ed3327da4fe83b3344738d958130bcf38b'
INITIAL_PIN='5c5a8ff02497b9bba38908507f88d309ce1553764878037034b5307e931d66bb'
REQUIRED={'INITIAL_WHOLE_POSITION.json','INPUT_BINDINGS.json','SOURCE_CUSTODY.json',
 'SOURCE_AND_VISUAL_RECEIPTS.json','MATH_RECONSTRUCTION.md','REPORT.md','VERDICT.json',
 'REPLAY_312_NORMAL.json','REPLAY_312_OPTIMIZED.json','REPLAY_SYSTEM_CORE.json',
 'CUSTODY_SYSTEM_OPTIMIZED.json','BUILD_312_NORMAL.json','BUILD_312_OPTIMIZED.json',
 'SOFTWARE_GUARD_RESULTS.json','software_guards.py','RESEARCH_LOG.md','custody_check.py'}
def need(condition,message):
    if not condition: raise ValueError(message)
def sha(raw): return hashlib.sha256(raw).hexdigest()
def hashvalid(v): return isinstance(v,str) and re.fullmatch('[0-9a-f]{64}',v) is not None
def unique(pairs):
    d={}
    for key,value in pairs:
        need(key not in d,'Duplicate JSON key');d[key]=value
    return d
def reject(v): raise ValueError('Nonfinite JSON constant')
def parse(raw): return json.loads(raw,object_pairs_hook=unique,parse_constant=reject)
def regular(path):
    need(stat.S_ISREG(path.lstat().st_mode),'Nonregular input: '+str(path))
    fd=os.open(path,os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW)
    with os.fdopen(fd,'rb') as f:
        need(stat.S_ISREG(os.fstat(f.fileno()).st_mode),'Nonregular opened file')
        return f.read()
def safe(name):
    need(isinstance(name,str) and bool(name) and '\\' not in name
         and not PurePosixPath(name).is_absolute()
         and all(x not in ('','.','..') for x in name.split('/')),'Unsafe relative name')
    return name
def relative_regular(root,name):
    safe(name);parts=PurePosixPath(name).parts;path=root
    for part in parts:
        path=path/part
        need(not path.is_symlink(),'Symlink path component')
    return regular(path)
def checkrow(raw,row):
    need(isinstance(row,dict) and type(row.get('bytes')) is int and row['bytes']>=0
         and hashvalid(row.get('sha256')),'Invalid file record')
    need(len(raw)==row['bytes'] and sha(raw)==row['sha256'],'File byte/hash mismatch')
def identity(raw): return {'bytes':len(raw),'sha256':sha(raw)}
def zipfiles(raw):
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        rows=z.infolist();names=[r.filename for r in rows]
        need(len(names)==len(set(names)),'Repeated ZIP member')
        need(sum(r.file_size for r in rows)<3000000,'Unexpected ZIP expansion')
        out={}
        for row in rows:
            safe(row.filename)
            need(not row.is_dir() and stat.S_IFMT(row.external_attr>>16) in (0,stat.S_IFREG),
                 'Nonregular ZIP member')
            out[row.filename]=z.read(row)
        return out
def root_files(root):
    need(root.is_dir() and not root.is_symlink(),'Root must be a regular directory')
    out={};dirs=set()
    for path in root.rglob('*'):
        need(not path.is_symlink(),'Tree symlink')
        name=path.relative_to(root).as_posix();safe(name)
        if path.is_dir(): dirs.add(name)
        else: out[name]=regular(path)
    expect={q.as_posix() for n in out for q in Path(n).parents if q.as_posix()!='.'}
    need(dirs==expect,'Unlisted empty directory')
    return out
def main(a):
    need(hashvalid(a.expected_manifest_sha) and hashvalid(a.expected_checker_sha),'External pins required')
    packet=Path(a.packet).absolute();inputs=Path(a.input_root).absolute()
    need(Path(__file__).absolute()==packet/'custody_check.py','Wrong executed checker path')
    need(sha(regular(packet/'custody_check.py'))==a.expected_checker_sha,'External checker pin')
    files=root_files(packet)
    need(all('/' not in n for n in files),'Review packet must be flat')
    mraw=files['MANIFEST.json'];need(sha(mraw)==a.expected_manifest_sha,'External review manifest pin')
    m=parse(mraw);need(m['schema']=='pr786-whole-review02/v1' and m['head']==HEAD,'Wrong review target')
    need(m['exceptions']=={'MANIFEST.json':'Only self-hash exception; caller-held external SHA256 required.'},
         'Widened exception list')
    rows=m['files'];need(isinstance(rows,dict) and REQUIRED<=set(rows),'Missing review file')
    need(set(files)==set(rows)|{'MANIFEST.json'} and 'MANIFEST.json' not in rows,'Review closure')
    for name,row in rows.items(): safe(name);checkrow(files[name],row)
    need(sha(files['INITIAL_WHOLE_POSITION.json'])==INITIAL_PIN,'Initial independent position changed')
    initial=parse(files['INITIAL_WHOLE_POSITION.json'])
    need(initial['target']['head']==HEAD and initial['initial_issues']==[],'Wrong initial position')
    bindings=parse(files['INPUT_BINDINGS.json'])['files']
    actual=root_files(inputs);need(len(bindings)==9 and set(actual)==set(bindings),'Complete9-input closure')
    for name,row in bindings.items():checkrow(actual[name],row)
    need(sha(actual['REVIEW_INPUTS.json'])==INPUT_PIN,'Externally fixed F2 inventory changed')
    intake=parse(actual['REVIEW_INPUTS.json'])
    need(intake['reviewed_head']==HEAD and intake['source_manifest_sha256']==SOURCE_PIN,'Wrong F2 target')
    nineset={r['path'] for r in intake['files']}
    need(len(nineset)==8 and nineset==set(actual)-{'REVIEW_INPUTS.json'},'F2 listed8+inventory closure')
    for row in intake['files']:checkrow(actual[row['path']],{'bytes':row['size'],'sha256':row['sha256']})
    source=zipfiles(actual['source-and-verification.zip']);need(len(source)==213,'Source213 members')
    need(sha(source['MANIFEST.json'])==SOURCE_PIN,'External source manifest pin')
    sm=parse(source['MANIFEST.json']);need(sm['schema']=='pr786-closed-source/v1','Source manifest schema')
    sr={r['path']:{k:r[k] for k in ('bytes','sha256')} for r in sm['files']}
    need(len(sr)==212 and len(sr)==len(sm['files']) and set(source)==set(sr)|{'MANIFEST.json'},'Source closed inventory')
    for name,row in sr.items():safe(name);checkrow(source[name],row)
    custody=parse(files['SOURCE_CUSTODY.json'])
    need(custody['source_members']==sr and custody['closed_source_files']==213,'Independent source ledger mismatch')
    ident=parse(source['audit/intake/ROOT_SOURCE_IDENTITY.json'])
    need(ident['reviewed_head']==HEAD and ident['original_file_count']==41,'Original target/count')
    originals={}
    for row in ident['original_files']:
        name='audit/intake/original/'+safe(row['path'])
        need(name not in originals,'Duplicate original')
        data=source[name];checkrow(data,row)
        need(hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['git_blob'],'Original Git blob')
        originals[name]=row
    need(len(originals)==41 and {n for n in source if n.startswith('audit/intake/original/')}==set(originals),
         'Original41 closure')
    ledger_originals={r['path']:{k:r[k] for k in ('bytes','sha256','git_blob')} for r in custody['original_files']}
    need(len(ledger_originals)==41 and len(custody['original_files'])==41
         and ledger_originals=={name:{k:r[k] for k in ('bytes','sha256','git_blob')} for name,r in originals.items()},
         'Independent41-blob ledger mismatch')
    selected=parse(source['audit/intake/SELECTED_PUBLIC_RECORD.json'])
    need(sha(json.dumps([selected['problem'],selected['prior_research']],sort_keys=True).encode())==ident['review_hash'],
         'Full selected record/prior binding')
    need(sha(source['audit/intake/SELECTED_PUBLIC_RECORD.json'])==ident['selected_record_sha256'],'Selected source hash')
    need(source['paper.tex']==actual['paper.tex'],'Source/F2 TeX mismatch')
    pb=parse(source['PREPRINT_BINDINGS.json']);checkrow(actual['paper.tex'],pb['paper.tex']);checkrow(actual['output/pdf/paper.pdf'],pb['paper.pdf'])
    release=parse(actual['RELEASE_INVENTORY.json']);package=parse(actual['PACKAGE_INVENTORY.json'])
    need(release['source_manifest_sha256']==SOURCE_PIN and package['source_manifest_sha256']==SOURCE_PIN,
         'Release/source pin')
    outputrows={r['path']:{k:r[k] for k in ('bytes','sha256')} for r in release['files']}
    need(len(outputrows)==6 and set(outputrows)<=set(actual),'All6 release outputs')
    need(outputrows=={r['path']:{k:r[k] for k in ('bytes','sha256')} for r in package['files']},'Package/release inventory disagreement')
    for name,row in outputrows.items():checkrow(actual[name],row)
    metadata=parse(actual['zenodo-metadata.json'])['metadata'];deposit=parse(actual['zenodo-deposit.json'])
    need(deposit['metadata']==metadata and metadata['publication_type']=='preprint' and metadata['version']=='1.0',
         'Deposit/metadata mismatch')
    kit=zipfiles(actual['zenodo-upload-kit.zip'])
    need(set(kit)=={'README.md','paper.pdf','source-and-verification.zip','zenodo-deposit.json','zenodo-metadata.json'},
         'Upload kit5 closure')
    for name,original in [('paper.pdf','output/pdf/paper.pdf'),('source-and-verification.zip','source-and-verification.zip'),
                          ('zenodo-metadata.json','zenodo-metadata.json')]:
        need(kit[name]==actual[original],'Kit/output bytes differ')
    flat=parse(kit['zenodo-deposit.json']);need(flat['metadata']==metadata and flat['files']==[{'path':'paper.pdf'},{'path':'source-and-verification.zip'}],
         'Flat deposit differs')
    for n,count in [('REPLAY_312_NORMAL.json',24),('REPLAY_312_OPTIMIZED.json',24),('REPLAY_SYSTEM_CORE.json',20),('CUSTODY_SYSTEM_OPTIMIZED.json',0)]:
        run=parse(files[n]);need(run['exitcode']==0 and run['stdout']['result']=='PASS' and len(run['stdout']['replay_runs'])==count,
             'Reproduction receipt failure')
    for n in ['BUILD_312_NORMAL.json','BUILD_312_OPTIMIZED.json']:
        run=parse(files[n]);need(run['status']=='PASS' and run['release_inventory_byte_equal'] is True,'Builder receipt')
        need({r['path']:{k:r[k] for k in ('bytes','sha256')} for r in run['outputs']}==outputrows and all(r['exact']is True for r in run['outputs']),
             '6-output rebuild receipt')
    guards=parse(files['SOFTWARE_GUARD_RESULTS.json'])
    need(guards['status']=='PASS' and guards['positive_cases']==2 and guards['negative_cases']==52,'Guard coverage')
    v=parse(files['VERDICT.json'])
    need(v['head']==HEAD and v['issues']==[] and v['result']=='PASS_REVIEWED_F2_ZERO_ACTIONABLE_ISSUES','Wrong final verdict')
    need(all(type(x)is int and x==0 for x in v['issue_counts'].values()),'Issue-count mismatch')
    for flag in ['firstness_certified','novelty_certified','current_worldwide_openness_certified','formal_proof_certified',
                 'external_human_peer_review_claimed','source_mutations','old_priority_packet_mutations','git_mutations',
                 'publication_or_merge','external_contacts','whole_review01_findings_read']:
        need(v.get(flag)is False,'Unsupported outcome flag: '+flag)
    need(v['initial_position_unchanged']is True and v['priority_status']=='UNRESOLVED','Independence/priority scope')
    primary_checked=0;visual_checked=0
    evidence=parse(files['SOURCE_AND_VISUAL_RECEIPTS.json'])
    need(evidence['paper_pdf_pages']==4 and len(evidence['sources'])==4 and len(evidence['visuals'])==5,'Source/visual scope')
    original_primary={r['name']:r for r in parse(source['audit/root-receipts/ROOT_PRIMARY_SOURCE_RECEIPTS.json'])['sources']}
    cp=next(r for r in parse(source['audit/root-receipts/ROOT_PRIORITY_SOURCE_RETRIEVALS.json']) if r['key']=='cox_parker_2005')
    el=parse(source['audit/root-receipts/ROOT_PRIORITY_ERDMANN_LAW.json'])
    pins={'M':original_primary['owr2009'],'DD':original_primary['dd2005'],'CP':cp,'EL':el}
    need({r['id'] for r in evidence['sources']}==set(pins),'4-primary identity set')
    for row in evidence['sources']:
        need(identity(b'')!=row and row['sha256']==pins[row['id']]['sha256']
             and row['bytes']==pins[row['id']]['bytes'],'Primary source pin differs from authenticated source record')
    if a.primary_root:
        root=Path(a.primary_root).absolute()
        for row in evidence['sources']:
            checkrow(relative_regular(root,row['relative_to_primary_root']),row);primary_checked+=1
    if a.visual_root:
        root=Path(a.visual_root).absolute()
        for row in evidence['visuals']:
            checkrow(relative_regular(root,row['file']),row);visual_checked+=1
    return {'status':'PASS','review_manifest_sha256':a.expected_manifest_sha,'checker_sha256':a.expected_checker_sha,
       'optimization':sys.flags.optimize,'authored_files':len(rows),'input_files':9,'source_members':213,'original_git_blobs':41,
       'release_outputs':6,'external_primary_bodies_checked':primary_checked,'viewed_renders_checked':visual_checked,
       'scope':'Byte custody and receipt consistency, not a formal mathematical or novelty certificate.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['packet','input-root','expected-manifest-sha','expected-checker-sha']:p.add_argument('--'+n,required=True)
    p.add_argument('--primary-root');p.add_argument('--visual-root')
    try:print(json.dumps(main(p.parse_args()),indent=2,sort_keys=True))
    except Exception as e:
        print('CUSTODY_FAIL: '+str(e),file=sys.stderr);sys.exit(1)
