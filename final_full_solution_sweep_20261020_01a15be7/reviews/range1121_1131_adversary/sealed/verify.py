#!/usr/bin/env python3
"""Read-only offline custody/interface checks, not a mathematical proof checker.
Run a disposable copy with an independently supplied MANIFEST.json SHA-256.
"""
import argparse, hashlib, io, json, os, re, stat, sys, zipfile
from pathlib import Path, PurePosixPath

CHECKPOINT='74bb4732342eba91cdd65b9cbdc5af71695b36bf'
POSTFREEZE='9b5cbcc8296bbc046ff17efc60d11de5cc15d287'
EFFORT='final_full_solution_sweep_20261020_01a15be7'
POSTPREFIX='draft_pr_actual_claims_1100_1200_20261017/audits/pr1121_30004311/'

def require(ok, why):
    if not ok: raise ValueError(why)

def digest(b): return hashlib.sha256(b).hexdigest()
def git_digest(kind,b): return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def pairs(items):
    out={}
    for k,v in items:
        require(k not in out,'duplicate JSON member')
        out[k]=v
    return out

def loads(b):
    return json.loads(b,object_pairs_hook=pairs,parse_constant=lambda x: (_ for _ in ()).throw(ValueError('nonfinite JSON')))

def valid_path(s):
    require(type(s) is str and bool(s),'empty/nonstring path')
    require('\x00' not in s and '\\' not in s and ':' not in s,'nonportable path')
    p=PurePosixPath(s)
    require(not p.is_absolute() and all(x not in ('','.','..') for x in s.split('/')),'noncanonical path')
    require(str(p)==s,'normalized path differs')
    return s

def pin(b,p):
    require(type(p) is dict and set(p)=={'bytes','sha256'},'bad pin schema')
    require(type(p['bytes']) is int and p['bytes']>=0,'bad pin size')
    require(type(p['sha256']) is str and re.fullmatch('[0-9a-f]{64}',p['sha256']) is not None,'bad pin digest')
    require(p=={'bytes':len(b),'sha256':digest(b)},'pin mismatch')

def inventory(root):
    files=set();dirs=set()
    def visit(d,prefix=''):
        for x in os.scandir(d):
            n=prefix+x.name;valid_path(n);mode=x.stat(follow_symlinks=False).st_mode
            require(not stat.S_ISLNK(mode),'symlink in packet')
            if stat.S_ISDIR(mode): dirs.add(n);visit(x.path,n+'/')
            else: require(stat.S_ISREG(mode),'special file in packet');files.add(n)
    visit(root)
    return files,dirs

def zip_contents(b):
    z=zipfile.ZipFile(io.BytesIO(b));names=z.namelist()
    require(len(names)==len(set(names))==len(set(x.casefold() for x in names)),'duplicate/case-colliding ZIP')
    for x in z.infolist():
        valid_path(x.filename)
        require(not x.is_dir() and not x.flag_bits&1,'directory/encrypted ZIP')
        require(stat.S_IFMT(x.external_attr>>16) in (0,stat.S_IFREG),'special ZIP entry')
    require(z.testzip() is None,'ZIP CRC failure')
    return {n:z.read(n) for n in names}

def tree_hash(items):
    def key(x):return x['path'].encode()+(b'/' if x['type']=='tree' else b'')
    require(len({x['path'] for x in items})==len(items),'duplicate tree path')
    raw=b''
    for x in sorted(items,key=key):
        require('/' not in x['path'],'direct tree contains nested path')
        valid_path(x['path']);mode=x['mode'].lstrip('0')
        require((mode,x['type']) in [('40000','tree'),('100644','blob'),('100755','blob'),('120000','blob'),('160000','commit')],'invalid Git mode')
        require(re.fullmatch('[0-9a-f]{40}',x['sha']) is not None,'bad Git oid')
        raw+=mode.encode()+b' '+x['path'].encode()+b'\0'+bytes.fromhex(x['sha'])
    return git_digest('tree',raw)

def recursive_tree(v):
    require(v.get('truncated') is False,'truncated Git tree')
    entries=v['tree'];index={x['path']:x for x in entries}
    require(len(index)==len(entries),'duplicate recursive tree')
    groups={'':[]}
    for x in entries:
        valid_path(x['path']);parent,_,leaf=x['path'].rpartition('/')
        groups.setdefault(parent,[]).append({**x,'path':leaf})
        if x['type']=='tree':groups.setdefault(x['path'],[])
    for path,items in groups.items():
        expected=v['sha'] if not path else index[path]['sha']
        require(tree_hash(items)==expected,'recursive Git tree mismatch')
    return index

def verify(root,external):
    require(re.fullmatch('[0-9a-f]{64}',external) is not None,'external SHA-256 required')
    mb=(root/'MANIFEST.json').read_bytes();require(digest(mb)==external,'external manifest anchor mismatch')
    m=loads(mb);require(m['checkpoint']==CHECKPOINT,'wrong checkpoint')
    public=m['public'];private=loads((root/'INPUT_MANIFEST.json').read_bytes())['files']
    require(set(public)=={'REPORT.md','CHECKS.json','verify.py','RESEARCH_LOG.md','.gitignore','INPUT_MANIFEST.json'},'public packet schema')
    require(all(x.startswith('private/') for x in private),'private inventory escapes private')
    require(set(public).isdisjoint(private),'inventories overlap')
    expected=set(public)|set(private)|{'MANIFEST.json'}
    for x,p in (public|private).items():valid_path(x);pin((root/x).read_bytes(),p)
    actual,dirs=inventory(root);expected_dirs={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'}
    require(actual==expected and dirs==expected_dirs,'packet not closed')
    def read(n):return (root/'private'/n).read_bytes()
    def j(n):return loads(read(n))
    raw=read('checkpoint_commit.raw');require(git_digest('commit',raw)==CHECKPOINT,'checkpoint object mismatch')
    rt=j('remote_root_tree.json');require(raw.splitlines()[0]==('tree '+rt['sha']).encode(),'checkpoint tree differs')
    require(tree_hash(rt['tree'])==rt['sha'] and rt.get('truncated') is False,'root tree mismatch')
    et=j('remote_effort_tree.json');require(next(x['sha'] for x in rt['tree'] if x['path']==EFFORT)==et['sha'],'effort not in checkpoint')
    idx=recursive_tree(et);frozen=j('FROZEN_PINS.json');require(len(frozen)==46,'frozen file count')
    for x in frozen:
        b=read('frozen/'+valid_path(x['path']));pin(b,{k:x[k] for k in ('bytes','sha256')})
        require(git_digest('blob',b)==x['git_oid']==idx[x['path']]['sha'],'frozen Git blob mismatch')
    journal=[loads(x) for x in read('frozen/dispositions.jsonl').splitlines()]
    require([x['pr'] for x in journal]==list(range(9,1132)),'journal prefix incomplete/duplicate/unordered')
    state=j('frozen/STATE.json');require((state['next_pr'],state['last_completely_processed_pr'],state['completed_pr_count'])==(1132,1131,1123),'checkpoint cursor')
    inv=j('frozen/rest_inventory.json');refresh=j('frozen/INVENTORY_REFRESH_20261021T2232.json')
    require(inv['highest_pr']==1446 and inv['in_scope_pr_count']==1438 and inv['numeric_gaps']==[],'inventory bound')
    require(refresh['changed_existing']==refresh['new_prs']==refresh['removed_prs']==[] and refresh['reconciliation_is_final'] is False,'refresh status')
    require(digest(read('frozen/rest_inventory.json'))==refresh['after_sha256'],'inventory refresh pin')
    cases=j('IDENTITY_RESULTS.json');require([x['pr'] for x in cases['cases']]==list(range(1121,1132)) and cases['total_files']==88,'case census')
    by_pr={x['number']:x for x in inv['pull_requests']};total=0
    for c in cases['cases']:
        n=c['pr'];pre=f'original/{n}/';v=by_pr[n];live=j(pre+'LIVE.json');last=j(f'final_live/pr{n}.json');cache=j(pre+'CACHE.json');blobs=j(pre+'BLOBS.json')
        require(c['head']==v['headRefOid']==live['head']['sha']==last['head']['sha']==cache['inventory_head_sha'],'head differs')
        require(c['base']==v['baseRefOid']==live['base']['sha']==last['base']['sha']==cache['inventory_base_sha'],'base differs')
        require(v['body']==live['body']==last['body'] and digest(v['body'].encode())==c['body_sha256'],'PR body differs')
        require((live['state'],live['merged'],live['draft'])==(last['state'],last['merged'],last['draft'])==(c['state'],c['merged'],c['draft']),'live flags changed')
        paths=[x['path'] for x in blobs];require(len(paths)==len(set(paths))==c['paths'],'blob census')
        require(set(paths)==set(cache['changed_paths'])=={x['filename'] for x in cache['files']},'incomplete actual file list')
        require(not any(PurePosixPath(x).name=='QUEUE.md' for x in paths),'unexpected QUEUE status')
        cm={x['filename']:x['sha'] for x in cache['files']}
        for f in blobs:
            b=read(pre+valid_path(f['path']));pin(b,{k:f[k] for k in ('bytes','sha256')})
            require(git_digest('blob',b)==f['git_oid']==cm[f['path']] and bool(cm[f['path']]),'actual/cache Git blob mismatch')
        total+=len(blobs)
    require(total==88,'total head blob count')
    for name in ['sheet.json','final_live/sheet.json']:
        s=j(name)['values'];require(len(s)>=180,'missing ledger rows')
        def rows(term):return [i for i,x in enumerate(s,1) if term.lower() in ' '.join(x).lower()]
        for term in ['23441906','30004311','OWR-17294-011','/pull/1121']:require(rows(term)==[158],'1121 ledger duplicate/missing')
        require(s[157][2]=='https://doi.org/10.5281/zenodo.23441906','1121 ledger DOI')
        for term in ['30005461','OWR-12697710-007','/pull/1129','motzkin','mixed odd']:require(rows(term)==[],'1129 new ledger lead; reassess')
    require(j('sheet.json')['values'][157]==j('final_live/sheet.json')['values'][157],'1121 row changed')
    leads=j('final_live/SHEET_SEMANTIC_LEADS.json')['leads']
    for term in ['30005455','OWR-12697708-008','/pull/1131','warm','whisker']:require(leads[term]==[],'1131 new duplicate lead')
    require([x['row'] for x in leads['reinforc']]==[114] and [x['row'] for x in leads['forest']]==[138],'recheck related semantic leads')
    source=j('sources/WARM_SOURCE_CORRECTION.json');pin(read('sources/owr1131.pdf'),{k:source[k] for k in ('bytes','sha256')})
    require(source['url']=='https://ems.press/content/serial-article-files/47008' and source['sha256']=='320d7e903924249d1f57536cdf67491b3b5f89de8401c9a7c07800b09ee750c7','wrong original WARM source')
    reopen=j('final_live/PR1131_SCOPE_REOPENING.json')
    require(reopen['pr']==1131 and reopen['head']==by_pr[1131]['headRefOid'] and reopen['not_publication_ready'] is True,'reopening scope')
    require(reopen['historical_disposition_sha256']==digest(read('frozen/PR1131_DISPOSITION.json')),'wrong historical decision corrected')
    require(any(x['pr']==1131 and x['evidence']=='PR1131_SCOPE_REOPENING.json' and x['not_publication_ready'] is True for x in j('final_live/STATE.json')['reopened_candidates']),'1131 not kept active')
    for x in j('sources/FETCH_RECEIPTS.json'):
        require(x['status']==200,'source retrieval status');pin(read('sources/'+valid_path(x['file'])),{k:x[k] for k in ('bytes','sha256')})
    record=j('pub1121/record.json');final=j('final_live/record.json')
    require(record['id']==final['id']==23441906 and record['doi']==final['doi']=='10.5281/zenodo.23441906','wrong record')
    for v in [record,final]:require(v['state']=='done' and v['submitted'] is True and len(v['files'])==2,'unpublished/incomplete record')
    for f in record['files']:
        b=read('pub1121/'+valid_path(f['key']));require(f['size']==len(b) and f['checksum']=='md5:'+hashlib.md5(b).hexdigest(),'provider file checksum')
        g=next(x for x in final['files'] if x['key']==f['key']);require((g['size'],g['checksum'])==(f['size'],f['checksum']),'final provider file changed')
        receipt=next(x for x in j('final_live/RECEIPT.json')['files'] if x['name']==f['key']);pin(b,{k:receipt[k] for k in ('bytes','sha256')})
    for name in ['pub1121/DOI.json','final_live/DOI.json']:require(j(name)=={'status':200,'final_url':'https://zenodo.org/records/23441906'},'DOI resolution differs')
    archive=zip_contents(read('pub1121/simple-brace-counterexample-source-and-verification.zip'));require(len(archive)==79,'source ZIP count')
    am=loads(archive['SOURCE_MANIFEST.json']);require(len(am)==78 and set(archive)==set(am)|{'SOURCE_MANIFEST.json'},'source ZIP not closed')
    for n,p in am.items():valid_path(n);pin(archive[n],p)
    for n in ['main.tex','README.md','PROVENANCE.json','zenodo-metadata.json']:require(read('pub1121/'+n)==archive[n],'operative extract differs')
    require(archive['output/pdf/simple-brace-counterexample.pdf']==read('pub1121/simple-brace-counterexample.pdf'),'embedded PDF differs')
    for f in j('original/1121/BLOBS.json'):
        require(archive['audit/inputs/'+PurePosixPath(f['path']).name]==read('original/1121/'+f['path']),'original head copy absent/different')
    meta=loads(archive['zenodo-metadata.json']);require(len(meta)==12,'native metadata count')
    for provider in [record['metadata'],final['metadata']]:
        for k,v in meta.items():
            a=provider['resource_type']['type'] if k=='upload_type' else provider['resource_type']['subtype'] if k=='publication_type' else provider['license']['id'] if k=='license' else provider[k]
            require(a==v,'provider native metadata differs '+k)
    raw=read('postfreeze_commit.raw');require(git_digest('commit',raw)==POSTFREEZE,'postfreeze commit mismatch')
    chain=j('postfreeze_tree_chain.json');oid=raw.splitlines()[0].decode().split()[1]
    for v,path in zip(chain[:3],['draft_pr_actual_claims_1100_1200_20261017','audits','pr1121_30004311']):
        require(v['sha']==oid==tree_hash(v['tree']) and v.get('truncated') is False,'historical path tree mismatch')
        oid=next(x['sha'] for x in v['tree'] if x['path']==path)
    require(chain[3]['sha']==oid,'postfreeze subtree mismatch');pi=recursive_tree(chain[3]);pp=j('POSTFREEZE_PINS.json');require(len(pp)==10,'postfreeze pin count')
    for x in pp:
        b=read(valid_path(x['local']));pin(b,{k:x[k] for k in ('bytes','sha256')})
        require(x['path'].startswith(POSTPREFIX),'unexpected postfreeze path');rel=x['path'][len(POSTPREFIX):]
        require(git_digest('blob',b)==x['git_oid']==pi[rel]['sha'],'postfreeze actual blob mismatch')
    prefix='pub1121/postfreeze/';kit=zip_contents(read(prefix+'publication/output/zenodo-upload-kit.zip'))
    require(set(kit)=={'README.md','simple-brace-counterexample.pdf','simple-brace-counterexample-source-and-verification.zip','zenodo-metadata.json','zenodo-deposit.json'},'kit not exact five-file set')
    for n in set(kit)-{'zenodo-deposit.json'}:require(kit[n]==read('pub1121/'+n),'kit payload differs')
    portable=loads(kit['zenodo-deposit.json']);native=j(prefix+'publication/zenodo-deposit.json')
    require(portable['metadata']==native['metadata']==meta,'kit/native metadata differs')
    require(portable['files']==[{'path':n} for n in ['simple-brace-counterexample.pdf','simple-brace-counterexample-source-and-verification.zip']],'portable kit paths')
    operative={
      'main.tex':read('pub1121/main.tex'),
      'output/pdf/simple-brace-counterexample.pdf':read('pub1121/simple-brace-counterexample.pdf'),
      'output/simple-brace-counterexample-source-and-verification.zip':read('pub1121/simple-brace-counterexample-source-and-verification.zip'),
      'output/zenodo-upload-kit.zip':read(prefix+'publication/output/zenodo-upload-kit.zip'),
      'zenodo-metadata.json':read('pub1121/zenodo-metadata.json'),
      'zenodo-deposit.json':read(prefix+'publication/zenodo-deposit.json')}
    gate=j(prefix+'ACCEPTANCE_GATE.json');require(gate['head_sha']==by_pr[1121]['headRefOid'] and gate['published'] is False and gate['package_reviews_clean']==2,'historical gate scope')
    for k,review in enumerate(gate['package_reviews'],1):
        require(review['round']==k and review['status']=='PASS' and review['new_independent_agent'] is True and review['same_first_freeze'] is True and review['required_repairs']==[],'not two fresh clean reviews')
        folder=prefix+f'reviews/package_{k:02}/';report=read(folder+'REPORT.md');manifest=read(folder+'ARTIFACT_MANIFEST.json')
        require(digest(report)==review['report_sha256'] and digest(manifest)==review['manifest_sha256'],'review gate binding')
        rm=loads(manifest)
        authored=rm.get('authored_files',rm.get('authored_public_artifacts'))
        require(type(authored) is dict,'review authored-file inventory missing')
        for name in (['REPORT.md','OPERATIVE_PINS_AND_INVENTORY.json'] if k==1 else ['REPORT.md','OPERATIVE_PINS.json','FINAL_OPERATIVE_RECHECK.json']):
            pin(read(folder+name),authored[name])
        rp=rm.get('operative_pins',rm.get('six_operative_pins'))
        if rp is None: rp=rm.get('operative_release_pins')
        require(type(rp) is dict and set(rp)==set(operative),'review operative pin set')
        for n,b in operative.items():pin(b,rp[n])
    checks=loads((root/'CHECKS.json').read_bytes())
    require(checks['counts']=={'partial':6,'credited_prior':2,'prior_full_consequence':1,'published_covered':1,'provisional_reopened':1},'false classification census')
    require(checks['whole_sweep_complete'] is False and checks['actionable_finding']['pr']==1131 and checks['actionable_finding']['status']=='eligibility_correction_fulfilled_by_explicit_reopening_full_audit_pending','missing material objection')
    return {'verdict':'BOUNDED_REVIEW_WITH_1131_REOPENING','checkpoint':CHECKPOINT,'files':len(expected),'private_files':len(private),'prs':11,'actual_head_blobs':total,'prefix_records':len(journal),'read_only_offline':True,'boundary':'Custody and exact interfaces only; written report states mathematical judgment, source limits and pending1131audit. No whole-sweep or publication-readiness certification.'}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--manifest-sha256',required=True);args=ap.parse_args()
    try: print(json.dumps(verify(Path(__file__).resolve().parent,args.manifest_sha256),sort_keys=True))
    except (ValueError,KeyError,TypeError,StopIteration,OSError,zipfile.BadZipFile) as e:
        print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
