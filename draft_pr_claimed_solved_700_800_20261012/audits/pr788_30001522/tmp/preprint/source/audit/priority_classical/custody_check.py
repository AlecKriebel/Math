"""Read-only PR788 classical-priority custody checker; caller-held external pins required."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,re,stat,sys
HEAD='3412d5a074c3f3a03f75735a9ccf1755e172204a'
INITIAL='a57d2512341ddf0ac3c71ed0f2496381850ec846473aae72bbb8bfed37d36252'
PROVISIONAL='d6915485ba5b3d63f1250285d1683cbac5b9a499811cc225c2ff88a7d455e631'
SELECTED='9fecfb4e59ffae554cdbf2e777005361981237b6236a1a16827a6b70e345927b'
ELIGIBILITY='6411fabd845b616673818ce02c9beb29647056a0f6683ba6731a3cdd68b7e431'
REVIEW='ca5ea39f6f40b6344a17adf507993b7a3aa628f194669943f2b6acb99876e306'
EXCEPTION={'MANIFEST.json':'Only self-hash exception; caller-held external SHA256 required.'}
REQUIRED={'INITIAL_PRIORITY_POSITION.json','PROVISIONAL_FINDING.json','INPUT_BINDINGS.json',
 'SOURCE_LEDGER.json','QUERY_LEDGER.json','REPORT.md','VERDICT.json','RESEARCH_LOG.md',
 'custody_check.py','test_custody.py','CUSTODY_RECIPE.md'}
def need(x,msg):
    if not x:raise ValueError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def validsha(x):return isinstance(x,str) and re.fullmatch('[0-9a-f]{64}',x) is not None
def unique(pairs):
    out={}
    for k,v in pairs:
        need(k not in out,'Duplicate JSON key');out[k]=v
    return out
def badconstant(x):raise ValueError('Nonfinite JSON constant')
def parse(b):return json.loads(b,object_pairs_hook=unique,parse_constant=badconstant)
def safe(n):
    need(isinstance(n,str) and n and '\\' not in n and not PurePosixPath(n).is_absolute()
      and all(p not in ('','.','..') for p in n.split('/')),'Unsafe relative filename')
    return n
def regular(p):
    need(stat.S_ISREG(p.lstat().st_mode),'Nonregular file: '+str(p))
    fd=os.open(p,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
    with os.fdopen(fd,'rb') as f:
        need(stat.S_ISREG(os.fstat(f.fileno()).st_mode),'Nonregular descriptor')
        return f.read()
def relative(root,n):
    safe(n);p=root
    for bit in n.split('/'):
        p=p/bit;need(not p.is_symlink(),'Symlink path component')
    return regular(p)
def tree(root):
    need(root.is_dir() and not root.is_symlink(),'Root must be a directory without symlink')
    files={};dirs=set()
    for p in root.rglob('*'):
        need(not p.is_symlink(),'Tree symlink')
        n=p.relative_to(root).as_posix();safe(n)
        if p.is_dir():dirs.add(n)
        else:files[n]=regular(p)
    expected={p.as_posix() for n in files for p in Path(n).parents if p.as_posix()!='.'}
    need(dirs==expected,'Unlisted empty directory')
    return files
def checkrow(b,r):
    need(isinstance(r,dict) and type(r.get('bytes'))is int and r['bytes']>=0 and validsha(r.get('sha256')),'Invalid byte/hash row')
    need(len(b)==r['bytes'] and sha(b)==r['sha256'],'Byte/hash mismatch')
def main(a):
    need(validsha(a.expected_manifest_sha) and validsha(a.expected_checker_sha),'External pins required')
    w=Path(a.packet).absolute();root=Path(a.input_root).absolute()
    need(Path(__file__).absolute()==w/'custody_check.py','Wrong checker path')
    need(sha(regular(w/'custody_check.py'))==a.expected_checker_sha,'External checker pin')
    files=tree(w);need(all('/' not in n for n in files),'Authored packet must be flat')
    need(sha(files['MANIFEST.json'])==a.expected_manifest_sha,'External manifest pin')
    m=parse(files['MANIFEST.json']);need(m['schema']=='pr788-priority-classical/v1' and m['head']==HEAD,'Wrong target/schema')
    need(m['exceptions']==EXCEPTION,'Widened exception set')
    rows=m['files'];need(isinstance(rows,dict) and REQUIRED<=set(rows),'Missing required authored file')
    need(set(files)==set(rows)|{'MANIFEST.json'} and 'MANIFEST.json'not in rows,'Authored closed inventory')
    for n,r in rows.items():safe(n);checkrow(files[n],r)
    need(sha(files['INITIAL_PRIORITY_POSITION.json'])==INITIAL,'Initial position changed')
    need(sha(files['PROVISIONAL_FINDING.json'])==PROVISIONAL,'Provisional finding changed')
    initial=parse(files['INITIAL_PRIORITY_POSITION.json'])
    need(initial['target']['head']==HEAD and initial['independence']['session_reused']is True,'Wrong initial target/exposure')
    b=parse(files['INPUT_BINDINGS.json']);need(b['head']==HEAD and b['original_count']==48 and b['review_hash']==REVIEW,'Input binding scope')
    need(b['exceptions']==['intake/RESEARCH_LOG.md is ongoing intake process log, not source identity input; no original blob or selected record is excluded.'],'Widened input exception')
    inputs=tree(root);bind=b['files']
    need(len(bind)==51 and set(bind)<=set(inputs) and set(inputs)-set(bind)<={'RESEARCH_LOG.md'},'51-input closure')
    for n,r in bind.items():safe(n);checkrow(inputs[n],r)
    need(sha(inputs['SELECTED_PUBLIC_RECORD.json'])==SELECTED and sha(inputs['ELIGIBILITY_GATE.json'])==ELIGIBILITY,'Frozen selected/eligibility pins')
    selected=parse(inputs['SELECTED_PUBLIC_RECORD.json']);identity=parse(inputs['ROOT_SOURCE_IDENTITY.json'])
    need(sha(json.dumps([selected['problem'],selected['prior_research']],sort_keys=True).encode())==REVIEW,'Complete record/prior canonical hash')
    need(selected['prior_research']=={} and selected['problem']['id']==30001522,'Wrong selected case')
    need(identity['reviewed_head']==HEAD and identity['review_hash']==REVIEW and identity['selected_record_sha256']==SELECTED,'Original source identity')
    need(sha(selected['problem']['statement'].encode())==identity['statement_sha256'],'Statement hash')
    gate=parse(inputs['ELIGIBILITY_GATE.json'])
    need(gate['result']=='ELIGIBLE' and gate['pr']==788 and gate['pr_metadata']['headRefOid']==HEAD,'Eligibility head')
    originals=identity['original_files'];need(len(originals)==48,'Original48 count')
    names=set()
    for r in originals:
        n='original/'+safe(r['path']);need(n not in names,'Duplicate original name');names.add(n)
        checkrow(inputs[n],r)
        blob=hashlib.sha1(b'blob '+str(len(inputs[n])).encode()+b'\0'+inputs[n]).hexdigest()
        need(blob==r['git_blob'] and bind[n].get('git_blob')==blob,'Original Git blob identity')
    need(names=={n for n in inputs if n.startswith('original/')},'Original48 exact closure')
    source=parse(files['SOURCE_LEDGER.json']);entries=source['full_primary_bodies'];external=source['external_scratch_files']
    need(len(entries)==10 and len({e['id']for e in entries})==10 and len(external)==31,'Source artifact scope')
    need(source['third_party_full_bodies_in_packet']is False,'Third-party body redistribution scope')
    need(len(source['unread_gaps'])>=7,'Lost source limitations')
    for e in entries:
        need(e['full_body_access']is True and e['read_scope'] and e['date_version'],'Missing source scope')
        need(external[e['body_file']]=={'bytes':e['body_bytes'],'sha256':e['body_sha256']},'Source body pin/ledger mismatch')
    critical={'yeroshkin':'8ddefbaa3a2704c9bc5797f3f5ed0223c67eb7b4b9dce35edbfe0c01bd1ad65e',
     'kuhn_lloyd_v1':'e4a158cfc203e4ab967e828b9a31b05d1764a0b46ad42b21eb785115be1e2029',
     'kuhn_lloyd_v2':'613faa2cbbed3d9fc52d89808030e2208d85727904ea185b01425717a2c8836f',
     'hanke_owr':'d7659b2af2684adacc83f53de171505bcea3251c42216f9079cdfaf0a6932417'}
    byid={e['id']:e for e in entries}
    for key,pin in critical.items():need(byid[key]['body_sha256']==pin,'Critical primary body pin')
    q=parse(files['QUERY_LEDGER.json'])
    need(q['query_count']==40 and len(q['batches'])==11 and sum(len(r['queries'])for r in q['batches'])==40,'Query ledger scope')
    need([r['batch']for r in q['batches']]==list(range(1,12)),'Query batch order')
    v=parse(files['VERDICT.json'])
    need(v['head']==HEAD and v['status']=='PRIORITY_UNRESOLVED_CLASSICAL_ASSEMBLY' and v['new_substantive_proof_turns']==0,'Verdict target/scope')
    for k in ['full_predecessor_identified','new_ingredient_or_example_certified','firstness_certified',
      'worldwide_current_openness_certified','absence_certified','candidate_mathematical_gate_replaced',
      'current_peer_or_root_priority_outcomes_read','source_mutations','git_mutations','publication','external_individual_contact']:
        need(v.get(k)is False,'Unsupported verdict flag: '+k)
    need(v['explicit_old_components_identified']is True and v['session_reused']is True,'Lost prior evidence/exposure')
    checked=0
    if a.source_root:
        sr=Path(a.source_root).absolute();need(sr.is_dir() and not sr.is_symlink(),'Bad external source root')
        for n,r in external.items():checkrow(relative(sr,n),r);checked+=1
        for e in entries:need(relative(sr,e['body_file']).startswith(b'%PDF'),'Primary body is not PDF')
    return {'status':'PASS','optimization':sys.flags.optimize,'manifest_sha256':a.expected_manifest_sha,
     'checker_sha256':a.expected_checker_sha,'authored_files':len(rows),'bound_source_inputs':51,'original_git_blobs':48,
     'full_primary_pdf_artifacts':10,'external_scratch_files_checked':checked,
     'scope':'Exact byte custody and bounded-report consistency; no proof, novelty or absence certification.'}
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    for n in ['packet','input-root','expected-manifest-sha','expected-checker-sha']:p.add_argument('--'+n,required=True)
    p.add_argument('--source-root')
    try:print(json.dumps(main(p.parse_args()),indent=2,sort_keys=True))
    except Exception as e:print('CUSTODY_FAIL: '+str(e),file=sys.stderr);sys.exit(1)
