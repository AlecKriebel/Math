#!/usr/bin/env python3
"""Externally anchored artifact replay; this is not a topology proof checker."""
import argparse,hashlib,io,json,pathlib,re,shutil,stat,subprocess,sys,tempfile,zipfile
PINS = {'KNOT_SURGERY_2868_INDEPENDENT_AUDIT_RECEIPT.json': [2148, '62665883c7514a05989f204bd2fca3fd04b90bef017ebdb87ce4fa929ca6478a'], 'archives/KNOT_SURGERY_2868_AUTHOR_EXTERNAL_MANIFEST.json': [2207, '886febe0cac1758af13791337f7175a446b9ca0e4c4692909867a4982e0116ef'], 'archives/KNOT_SURGERY_2868_AUTHOR_SAFE_FREEZE.zip': [11525, 'c3b899805315796d6023af73be74d7133f354703447cfe85dc2b5506ccf09b8d'], 'archives/KNOT_SURGERY_2868_EXACT_ACCEPTANCE_EXTERNAL_MANIFEST.json': [610, '571aaa5a4e75e95b0efe73193f10b0c8d06047974ea2a5642cfabc939607cd30'], 'archives/KNOT_SURGERY_2868_EXACT_ACCEPTANCE_SAFE.zip': [1884, 'b0675e386f68300d00daa2ba321dba70ad0734ff36c07ffbc19039c1e772d887'], 'archives/KNOT_SURGERY_2868_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json': [3334, '65f96b198ab1c8d0ef76c3d7316a771c43bc454a16831f89c13fa9158489a25a'], 'archives/KNOT_SURGERY_2868_INDEPENDENT_AUDIT_SAFE.zip': [28981, '869837d38079ed3adc9912fb508ba890ffb331a93d045d80e04d34635a6f6255']}
STEM = 'KNOT_SURGERY_2868_'
TAGS = [('AUTHOR','_SAFE_FREEZE.zip','author',8),('INDEPENDENT_AUDIT','_SAFE.zip','independent_audit',12),('EXACT_ACCEPTANCE','_SAFE.zip','exact_acceptance',2)]
EXTRAS = {'README.md','RESEARCH_LOG.md','PUBLICATION_METADATA.json','PUBLICATION_INPUT_REPLAY.json','PUBLICATION_TEST_RESULTS.json','PUBLICATION_MANIFEST.json','verify_publication.py'}
FALSES = ['full_problem_solved','full_problem_refuted','novelty_claim','formal_proof_certificate','human_peer_review','source_documents_included','dataset_contents_included','private_coordination_included','new_proof_search_performed','new_source_retrieval_or_visual_inspection_claimed']
class Rejected(Exception): pass
def need(ok,why):
    if not ok: raise Rejected(why)
def sha(b): return hashlib.sha256(b).hexdigest()
def enc(x): return (json.dumps(x,sort_keys=True,indent=2)+'\n').encode()
def unique(pairs):
    d={}
    for k,v in pairs:
        need(k not in d,'duplicate JSON key'); d[k]=v
    return d
def parsed(b): return json.loads(b.decode('utf8'),object_pairs_hook=unique,parse_constant=lambda _:(_ for _ in ()).throw(Rejected('nonfinite JSON')))
def safe(n):
    need(type(n) is str and bool(n),'path type'); p=pathlib.PurePosixPath(n)
    need(not p.is_absolute() and '..' not in p.parts and str(p)==n and '\\' not in n,'unsafe path')
def pin(b,size,digest,label):
    need(type(size) is int and size>=0 and type(digest) is str and re.fullmatch('[0-9a-f]{64}',digest) is not None,'malformed pin')
    need((len(b),sha(b))==(size,digest),'pin mismatch '+label)
def rowpin(b,row,label): pin(b,row['bytes'],row['sha256'],label)
def inspect_zip(raw,ext,count):
    need(ext['problem_id']==2868 and ext['schema_version']==1,'archive identity'); rowpin(raw,ext['archive'],'archive')
    rows=ext['members']; need(type(rows) is dict and len(rows)==count,'archive manifest count')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names=z.namelist(); need(len(names)==len(set(names))==count and set(names)==set(rows),'ZIP inventory')
        need(z.testzip() is None,'ZIP CRC'); out={}
        for n in names:
            safe(n); need('/' not in n,'flat ZIP required'); i=z.getinfo(n); mode=(i.external_attr>>16)&0xffff
            need(stat.S_ISREG(mode) and not i.is_dir() and not (i.flag_bits&1) and i.file_size<200000,'ZIP member type/size')
            b=z.read(i); rowpin(b,rows[n],n); out[n]=b
    if 'internal_manifest' in ext: rowpin(out['MANIFEST.json'],ext['internal_manifest'],'internal manifest')
    return out

def validate(files,expected):
    for n in files: safe(n)
    need(type(expected) is str and re.fullmatch('[0-9a-f]{64}',expected) is not None,'expected manifest pin required')
    need(sha(files['PUBLICATION_MANIFEST.json'])==expected,'publication manifest external anchor')
    manifest=parsed(files['PUBLICATION_MANIFEST.json']); need(manifest['problem_id']==2868 and manifest['schema_version']==1,'publication manifest identity')
    need(set(manifest['files'])==set(files)-{'PUBLICATION_MANIFEST.json'},'publication manifest inventory')
    for n,row in manifest['files'].items(): rowpin(files[n],row,n)
    for n,(size,digest) in PINS.items(): pin(files[n],size,digest,n)
    expected_names=set(PINS)|EXTRAS; packets={}
    for tag,suffix,leaf,count in TAGS:
        ext=parsed(files['archives/'+STEM+tag+'_EXTERNAL_MANIFEST.json']); pack=inspect_zip(files['archives/'+STEM+tag+suffix],ext,count); packets[tag]=pack
        for n,b in pack.items():
            expected_names.add(leaf+'/'+n); need(files[leaf+'/'+n]==b,'extracted byte mismatch '+leaf+'/'+n)
    need(set(files)==expected_names,'exact public inventory')
    for n,b in files.items():
        if n.endswith('.json'): parsed(b)
    author=packets['AUTHOR']; audit=packets['INDEPENDENT_AUDIT']; exact=packets['EXACT_ACCEPTANCE']
    for suffix in ['AUTHOR_SAFE_FREEZE.zip','AUTHOR_EXTERNAL_MANIFEST.json']:
        need(audit[STEM+suffix]==files['archives/'+STEM+suffix],'nested original preserved')
    status=parsed(author['STATUS.json']); need(status['status']=='stalled_partial' and status['turns_used']==3 and status['turn_limit']==5,'author status')
    need(status['audit_status']=='pending independent audit' and status['publication_status']=='not published at author freeze','historical fields preserved')
    need(all(status[k] is False for k in ['full_problem_solved','full_problem_refuted','novelty_claim']),'author limits')
    a=parsed(exact['ACCEPTANCE.json']); historic=parsed(audit['ACCEPTANCE.json'])
    need(all(k in a and a[k]==v for k,v in historic.items()),'exact acceptance preserves prior acceptance')
    need(a['verdict']=='ACCEPT_UNCHANGED_STALLED_PARTIAL' and a['problem_id']==2868 and a['rank']==915 and a['problem_number']=='KP-3.70' and a['turns_used']==3 and a['turn_limit']==5,'exact acceptance identity')
    need(a['mathematical_status']=='stalled_partial' and a['correction_required'] is False and a['original_preserved'] is True and a['accepted_author_member_count']==8,'unchanged acceptance')
    for k in FALSES[:8]: need(a[k] is False,'acceptance claim '+k)
    for key,suffix in [('original_archive','AUTHOR_SAFE_FREEZE.zip'),('original_external_manifest','AUTHOR_EXTERNAL_MANIFEST.json'),('independent_audit_archive','INDEPENDENT_AUDIT_SAFE.zip'),('independent_audit_external_manifest','INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json')]:
        row=a[key]; need(row['filename']==STEM+suffix,'acceptance filename'); rowpin(files['archives/'+STEM+suffix],row,key)
    rowpin(audit['MANIFEST.json'],a['independent_audit_internal_manifest'],'audit internal acceptance')
    need(a['verification_summary']=={'author_controls_per_replay':7,'four_identical_full_replays':True,'independent_controls_per_replay':11,'outer_audit_controls_rejected':6},'verification counts')
    receipt=parsed(files[STEM+'INDEPENDENT_AUDIT_RECEIPT.json'])
    for key,suffix in [('original_author_archive','AUTHOR_SAFE_FREEZE.zip'),('original_author_external_manifest','AUTHOR_EXTERNAL_MANIFEST.json'),('independent_audit','INDEPENDENT_AUDIT_SAFE.zip'),('independent_audit_external_manifest','INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json'),('exact_acceptance','EXACT_ACCEPTANCE_SAFE.zip'),('exact_acceptance_external_manifest','EXACT_ACCEPTANCE_EXTERNAL_MANIFEST.json')]: rowpin(files['archives/'+STEM+suffix],receipt[key],key)
    rowpin(audit['MANIFEST.json'],receipt['audit_internal_manifest'],'receipt audit manifest')
    meta=parsed(files['PUBLICATION_METADATA.json']); need(meta['problem_id']==2868 and meta['rank']==915 and meta['problem_number']=='KP-3.70' and meta['status']=='unsolved' and meta['mathematical_status']=='stalled_partial' and type(meta['turns_used']) is int and meta['turns_used']==3 and meta['turn_limit']==5,'publication status')
    need(meta['verdict']=='ACCEPT_UNCHANGED_STALLED_PARTIAL' and meta['no_correction_required'] is True and meta['historical_freeze_fields_preserved'] is True,'publication acceptance')
    for k in FALSES: need(meta[k] is False,'publication claim '+k)
    q=meta['queue']; need(q['changed_cells']==['Status','Turns'] and q['status']=='unsolved' and q['turns']=='3/5' and q['findings_preserved'] is True and q['unrelated_bytes_preserved'] is True,'queue policy')
    inputs=parsed(files['PUBLICATION_INPUT_REPLAY.json']); recorded=parsed(files['PUBLICATION_TEST_RESULTS.json'])
    iv=parsed(audit['INPUT_VERIFICATION.json']); sv=parsed(audit['SOURCE_VERIFICATION.json'])
    need(inputs['problem_id']==2868 and inputs['rank']==915 and inputs['current_full_corpus_rehash']=='PASS_FULL_CORPUS_AND_COMPLETE_PAIR' and inputs['current_source_pdf_rehash']=='PASS_THREE_PINNED_SOURCE_PDFS' and inputs['source_or_corpus_contents_included'] is False,'publication input report status')
    need(inputs['full_corpus_pins']==iv['inputs'] and inputs['statement_sha256']==iv['statement_sha256'] and inputs['complete_pair_sha256']==iv['record_report_pair_sha256'] and inputs['complete_pair_serialization']==iv['pair_serialization'],'publication input bindings')
    need(inputs['source_pdf_pins']==[{'id':r['id'],'title':r['title'],'url':r['public_url'],'bytes':r['bytes'],'sha256':r['sha256']} for r in sv['sources']],'publication source bindings')
    need(recorded['result']=='PASS_PUBLICATION_INTEGRITY_ONLY' and recorded['problem_id']==2868 and recorded['public_files']==len(files) and recorded['archive_members']=={k:len(v) for k,v in packets.items()} and recorded['normal_optimized_relocated_equal'] is True and recorded['modes']==['normal','optimized','relocated_normal','relocated_optimized'],'publication test report status')
    need(recorded['mathematical_proof_certified'] is False and recorded['author_controls_per_mode']==7 and recorded['independent_controls_per_mode']==11 and recorded['outer_audit_controls_previously_rejected']==6,'publication test limits')
    need(recorded['current_corpus_rehash']==inputs['current_full_corpus_rehash'] and recorded['current_source_pdf_rehash']==inputs['current_source_pdf_rehash'],'publication test input status')
    controls=recorded['wrapper_controls'];need(controls['count']==len(controls['rejected']) and len(set(controls['rejected']))==controls['count'] and 'explicit fail-closed guard' in controls['rejected'],'publication controls inventory')
    need(len(recorded['cli_negative_controls'])==8 and all(x['result']=='REJECTED' and x['exit_code']!=0 for x in recorded['cli_negative_controls']),'publication CLI controls')
    need(recorded['queue_check']=={'result':'PASS','changed_cells':['Status','Turns'],'findings_and_every_other_byte_preserved':True},'publication queue check')
    return packets

def load_files(root):
    need(root.is_dir() and not root.is_symlink(),'invalid root'); paths=list(root.rglob('*'))
    need(all(not p.is_symlink() and (p.is_dir() or p.is_file()) for p in paths),'nonregular filesystem member')
    return {p.relative_to(root).as_posix():p.read_bytes() for p in paths if p.is_file()}
def queue_check(base,new,meta):
    q=meta['queue']; need(sha(base)==q['base_sha256'] and sha(new)==q['new_sha256'],'queue external pins')
    old=base.splitlines(keepends=True); now=new.splitlines(keepends=True); need(len(old)==len(now),'queue line count')
    idx=[i for i,(x,y) in enumerate(zip(old,now)) if x!=y]
    need(len(idx)==1 and old[idx[0]].startswith(b'| 915 | 2868 / KP-3.70 |'),'only target row')
    x=old[idx[0]].split(b'|'); y=now[idx[0]].split(b'|'); need(len(x)==len(y) and [i for i,(a,b) in enumerate(zip(x,y)) if a!=b]==[8,9],'only Status and Turns')
    need(x[8:10]==[b' queued ',b' 0/5 '] and y[8:10]==[b' unsolved ',b' 3/5 '],'queue transition')
    return {'result':'PASS','changed_cells':['Status','Turns'],'findings_and_every_other_byte_preserved':True}
def replay(packets,full_inputs=None,source_dir=None):
    audit=packets['INDEPENDENT_AUDIT']; manifest=sha(audit['MANIFEST.json'])
    with tempfile.TemporaryDirectory(prefix='knot-surgery-replay-') as t:
        base=pathlib.Path(t); root=base/'nested/packet'; root.mkdir(parents=True); cwd=base/'unrelated';cwd.mkdir()
        for n,b in audit.items(): (root/n).write_bytes(b)
        cmd=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+[str(root/'verify_audit.py'),'--expected-manifest-sha256',manifest]
        if full_inputs: cmd+=['--full-inputs']+[str(pathlib.Path(p).absolute()) for p in full_inputs]
        if source_dir: cmd+=['--source-dir',str(pathlib.Path(source_dir).absolute())]
        p=subprocess.run(cmd,cwd=cwd,capture_output=True,text=True,timeout=120)
        need(p.returncode==0,'audit replay: '+p.stderr); result=parsed(p.stdout.encode())
        need(result['audit_packet']=='PASS_EXTERNALLY_PINNED_AUDIT' and result['normal_optimized_relocated_equal'] is True and len(result['runs'])==4 and result['mathematical_proof_certified'] is False,'audit replay contract')
        need(len(result['independent_negative_controls'])==11 and all(x['result']=='REJECTED' for x in result['independent_negative_controls']),'eleven independent controls')
        need(load_files(root)==audit,'audit replay mutated bytes'); return result

def reanchor(f):
    m=parsed(f['PUBLICATION_MANIFEST.json']);m['files']={n:{'bytes':len(b),'sha256':sha(b)} for n,b in sorted(f.items()) if n!='PUBLICATION_MANIFEST.json'}
    f['PUBLICATION_MANIFEST.json']=enc(m);return sha(f['PUBLICATION_MANIFEST.json'])
def negatives(files):
    rejected=[]; trusted=sha(files['PUBLICATION_MANIFEST.json'])
    def reject(label,alter,anchor=True,explicit=None):
        f=dict(files);alter(f);expected=explicit if explicit is not None else (reanchor(f) if anchor else trusted)
        try: validate(f,expected)
        except (Rejected,KeyError,ValueError,TypeError,zipfile.BadZipFile): rejected.append(label);return
        raise Rejected('negative control accepted: '+label)
    for n in PINS: reject('changed externally frozen '+n,lambda f,n=n:f.__setitem__(n,f[n]+b'x'))
    for n in ['author/REPORT.md','independent_audit/AUDIT_REPORT.md','exact_acceptance/ACCEPTANCE.json']:
        reject('changed extracted '+n,lambda f,n=n:f.__setitem__(n,f[n]+b'x'))
    reject('missing extracted member',lambda f:f.pop('author/README.md'))
    reject('extra public member',lambda f:f.__setitem__('extra.md',b'extra'))
    reject('unsafe public path',lambda f:f.__setitem__('../extra.md',b'extra'))
    for k,v in [('status','solved'),('turns_used',4),('turns_used',True),('historical_freeze_fields_preserved',False),('no_correction_required',False)]+[(k,True) for k in FALSES]:
        def alter(f,k=k,v=v): m=parsed(f['PUBLICATION_METADATA.json']);m[k]=v;f['PUBLICATION_METADATA.json']=enc(m)
        reject('rehashed invalid claim '+k+'='+str(v),alter)
    reject('duplicate JSON key',lambda f:f.__setitem__('PUBLICATION_METADATA.json',f['PUBLICATION_METADATA.json'].replace(b'"rank": 915',b'"rank": 915, "rank": 915')))
    reject('nonfinite JSON',lambda f:f.__setitem__('PUBLICATION_METADATA.json',f['PUBLICATION_METADATA.json'].replace(b'"rank": 915',b'"rank": NaN')))
    for filename in ['PUBLICATION_INPUT_REPLAY.json','PUBLICATION_TEST_RESULTS.json']:
        reject('pending evidence '+filename,lambda f,n=filename:f.__setitem__(n,enc({'status':'PENDING'})))
    def false_pdf(f):
        j=parsed(f['PUBLICATION_INPUT_REPLAY.json']);j['source_pdf_pins'][0]['sha256']='0'*64;f['PUBLICATION_INPUT_REPLAY.json']=enc(j)
    reject('rehashed false source evidence',false_pdf)
    reject('stale publication manifest',lambda f:f.__setitem__('README.md',f['README.md']+b'x'),anchor=False)
    reject('wrong external publication pin',lambda f:None,explicit='0'*64)
    reject('corrupt publication manifest',lambda f:f.__setitem__('PUBLICATION_MANIFEST.json',b'{}'),anchor=False)
    try: need(False,'explicit fail-closed guard')
    except Rejected: rejected.append('explicit fail-closed guard')
    else: raise Rejected('disabled guard')
    with tempfile.TemporaryDirectory() as t:
        p=pathlib.Path(t);(p/'link').symlink_to(__file__)
        try:load_files(p)
        except Rejected:rejected.append('filesystem symlink')
        else:raise Rejected('symlink accepted')
    return {'count':len(rejected),'rejected':rejected}
def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--directory',type=pathlib.Path,default=pathlib.Path(__file__).absolute().parent);p.add_argument('--expected-manifest-sha256',required=True);p.add_argument('--full-inputs',nargs=3);p.add_argument('--source-dir');p.add_argument('--base-queue');p.add_argument('--queue');p.add_argument('--self-test',action='store_true');a=p.parse_args()
    need(bool(a.base_queue)==bool(a.queue),'both queue paths required');need(bool(a.full_inputs)==bool(a.source_dir),'all corpus and PDF input paths required')
    f=load_files(a.directory);packets=validate(f,a.expected_manifest_sha256)
    result={'result':'PASS_PUBLICATION_INTEGRITY_ONLY','public_files':len(f),'archive_members':{k:len(v) for k,v in packets.items()},'mathematical_proof_certified':False,'audit_replay':replay(packets,a.full_inputs,a.source_dir),'queue_check':'NOT_REQUESTED','wrapper_controls':'NOT_REQUESTED'}
    if a.base_queue:result['queue_check']=queue_check(pathlib.Path(a.base_queue).read_bytes(),pathlib.Path(a.queue).read_bytes(),parsed(f['PUBLICATION_METADATA.json']))
    if a.self_test:result['wrapper_controls']=negatives(f)
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':
    try: main()
    except (Rejected,OSError,ValueError,KeyError,TypeError,zipfile.BadZipFile,subprocess.SubprocessError) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
