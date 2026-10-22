#!/usr/bin/env python3
"""Read-only independent range checks; no project imports or service calls."""
import datetime, hashlib, io, json, subprocess, zipfile
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
SWEEP = HERE.parents[1]
REPO = SWEEP.parent

def need(ok, label):
    if not ok: raise RuntimeError(label)

def read(p): return json.loads(Path(p).read_text())
def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def pin(b): return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def git(*args): return subprocess.check_output(['git',*args],cwd=REPO)

def publication(n, record, ledger_row, archived_head_prefix):
    raw = SWEEP / f'raw/pr{n}'
    provider = read(raw / f'zenodo_{record}.json')
    checks = read(SWEEP / f'PR{n}_PUBLICATION_VERIFICATION.json')
    payloads = {}
    for f in checks['files']:
        b = (raw / ('payload_'+f['sha256']+'.bin')).read_bytes()
        need(pin(b)=={'bytes':f['size'],'sha256':f['sha256']},'payload SHA/size')
        need('md5:'+hashlib.md5(b).hexdigest()==f['checksum'],'payload MD5')
        native = next(v for v in provider['files'] if v['key']==f['name'])
        need((native['size'],native['checksum'])==(len(b),f['checksum']),'native file identity')
        payloads[f['name']] = b
    need(provider['doi']==f'10.5281/zenodo.{record}' and provider['state']=='done' and provider['submitted'] is True,'published DOI')
    ledger = read(HERE/'LIVE_GWS_READ.json')['response']['values']
    doi = 'https://doi.org/'+provider['doi']
    need(ledger[ledger_row-1][2]==doi and sum(r[2]==doi for r in ledger[1:])==1,'live unique DOI')
    z = zipfile.ZipFile(io.BytesIO(next(b for k,b in payloads.items() if k.endswith('.zip'))))
    names = z.namelist()
    need(len(names)==len(set(names)) and z.testzip() is None,'zip uniqueness/CRC')
    mn = 'source-archive-manifest.json' if n==1156 else 'SOURCE_MANIFEST.json'
    m = json.loads(z.read(mn)); m = m['files'] if n==1156 else m
    need(set(names)==set(m)|{mn},'archive closure')
    for path, expected in m.items(): need(pin(z.read(path))==expected,'archive manifest '+path)
    if archived_head_prefix:
        e = read(SWEEP/f'eligibility/pr{n}.json')
        for path in e['changed_paths']:
            need(z.read(archived_head_prefix+PurePosixPath(path).name)==git('show',e['inventory_head_sha']+':'+path),'archived exact head')
    return {'pr':n,'record':record,'ledger_row':ledger_row,'files':len(payloads),'closed_members':len(names)}

def main():
    if (HERE/'INPUT_PINS.json').exists():
        for f in read(HERE/'INPUT_PINS.json')['files']:
            need(pin((REPO/f['path']).read_bytes())=={k:f[k] for k in ['bytes','sha256']},'external input pin '+f['path'])
    if (HERE/'MANIFEST.json').exists():
        m = read(HERE/'MANIFEST.json')['files']
        actual = {str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file() and p.name!='MANIFEST.json'}
        need(actual==set(m),'authored closed manifest membership')
        for path,expected in m.items(): need(pin((HERE/path).read_bytes())==expected,'authored manifest '+path)
    need(git('branch','--show-current').decode().strip()=='main','branch')
    scope = read(HERE/'IMMUTABLE_SCOPE_CHECK.json')['fresh_git_checks']
    need([r['pr'] for r in scope]==list(range(1151,1161)),'complete sequential range')
    inventory = {p['number']:p for p in read(SWEEP/'rest_inventory.json')['pull_requests']}
    times = []
    count = 0
    for r in scope:
        n = r['pr']; d = read(SWEEP/f'PR{n}_DISPOSITION.json'); e = read(SWEEP/f'eligibility/pr{n}.json')
        need(digest(SWEEP/f'PR{n}_DISPOSITION.json')==r['disposition_sha256'],'disposition changed')
        need((d['inventory_head_sha'],d['inventory_base_sha'])==(r['head'],r['base']),'head/base')
        original = inventory[n]
        need((original['headRefOid'],original['baseRefOid'])==(r['head'],r['base']),'inventory head/base')
        need(hashlib.sha256((original['body'] or '').encode()).hexdigest()==d['inventory_body_sha256'],'inventory PR body')
        times.append(d['processed_at'])
        paths = git('diff','--name-only',r['base']+'...'+r['head']).decode().splitlines()
        need(set(paths)=={f['path'] for f in r['files']}==set(e['changed_paths']),'complete paths')
        need(not any('QUEUE' in PurePosixPath(x).name for x in paths),'QUEUE changed')
        for f in r['files']:
            b = git('show',r['head']+':'+f['path'])
            need(pin(b)=={k:f[k] for k in ['bytes','sha256']},'Git bytes')
            oid = hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
            need(oid==f['blob']==next(v['sha'] for v in e['files'] if v['filename']==f['path']),'Git object/cache')
            count += 1
    need(times==sorted(times),'sequential disposition timestamps')
    pubs = [publication(1151,23444606,167,'draft_pr_actual_claims_1100_1200_20261017/audits/pr1151_30003321/pr_repair_candidate/'),publication(1155,23444839,169,'draft_pr_actual_claims_1100_1200_20261017/audits/pr1155_30000214/inputs/'),publication(1156,23350364,182,'')]
    a = SWEEP/'audits/pr1156_30003650'; ac = read(a/'ROOT_EXACT_INSTANCE_V2_ACCEPTANCE.json'); plan = read(a/'LEDGER_RECONCILIATION_PLAN.json')
    need(digest(a/'reconcile_exact_instance_v2.py')==ac['helper_sha256'],'v2 helper pin')
    need(digest(a/'LEDGER_RECONCILIATION_PLAN.json')==ac['plan_sha256'],'v2 plan pin')
    for p in ac['review_pins']: need(digest(a/p['path'])==p['sha256'],'accepted review pin '+p['path'])
    receipt = read(a/'LEDGER_PUBLICATION_VERIFICATION.json'); raw = SWEEP/receipt['raw_receipts']
    before = read(raw/'before.json')['values']; after = read(raw/'after.json')['values']
    need(len(before)==181 and read(raw/'immediate_before_append.json')['values']==before,'preappend ledger')
    need(after==before+[plan['proposed_row']] and len(after)==182,'exact append')
    need(read(HERE/'LIVE_GWS_READ.json')['response']['values']==after,'fresh full live ledger')
    u = read(a/'LEDGER_RECONCILIATION_RESPONSE.json')['updates']
    need(u['updatedRange']=="'Math Puzzles'!A182:D182" and u['updatedData']['values']==[plan['proposed_row']],'actual range/echo')
    for k,v in [('updatedRows',1),('updatedColumns',4),('updatedCells',4)]: need(type(u[k]) is int and u[k]==v,'actual response integer')
    base = a/'root/private/actual_instance08_root_copy/private'
    need(digest(base/'source_14_account.json')=='77cfa06407b40e66b72b4f7cc056d47b7066d604bcf9cd21d8d1619aa99bde00','197 baseline hash')
    need(digest(base/'source_10_ledger_live.json')=='9e2d9dbcc21f4ab9d26be5386ad1450176a273e2425fba0a1b3260b07d4c6acb','181 baseline hash')
    old = read(base/'source_14_account.json'); new = read(raw/'account.json')
    need(old['query']==new['query']=='' and old['total']==new['total']==197,'account total/query')
    old = {r['id']:r for r in old['records']}; records = new['records']; new = {r['id']:r for r in records}
    need(old.keys()==new.keys() and len(records)==len(new)==len(old)==197,'account IDs')
    counters = {'downloads','unique_downloads','version_downloads','version_unique_downloads','views','unique_views','version_views','version_unique_views'}
    differences = []
    def compare(x,y,path=()):
        need(type(x) is type(y),'account type')
        if isinstance(x,dict):
            need(x.keys()==y.keys(),'account keys')
            for k in x: compare(x[k],y[k],path+(k,))
        elif isinstance(x,list):
            need(len(x)==len(y),'account list')
            for i,(l,r) in enumerate(zip(x,y)): compare(l,r,path+(i,))
        elif len(path)==2 and path[0]=='stats' and path[1] in counters:
            need(type(x) is int and x>=0 and y>=0,'account counter')
            if x!=y: differences.append(path)
        else: need(x==y,'account identity')
    for identifier in old: compare(old[identifier],new[identifier])
    post = a/'root/private/post_reconciliation_9922cf201bef4aea8e997a28c32e9625'
    need(read(post/'formula_after.json')['values']==after,'separate formula view')
    need(read(post/'raw/pr1156/ledger_live.json')['response']['values']==after,'separate post ledger')
    for pr in [read(raw/'pr.json'),read(post/'live_pr.json')]:
        need((pr['head']['sha'],pr['base']['sha'])==(plan['head'],plan['base']),'action/post PR head/base')
        need(hashlib.sha256(pr['body'].encode()).hexdigest()==plan['body_sha256'],'action/post PR body')
        need(pr['state']=='open' and pr['merged'] is False and pr['draft'] is True,'action/post PR state')
    print(json.dumps({'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'immutable_paths_checked':count,'publications':pubs,'accepted_v2_review_pins':len(ac['review_pins']),'account_records':197,'permitted_counter_differences':len(differences),'before_rows':181,'after_rows':182,'fresh_live_and_separate_formula_view_exact':True,'all_checks_passed':True},indent=2))

if __name__=='__main__': main()
