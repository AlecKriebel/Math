#!/usr/bin/env python3
"""Read-only custody/exact-commit audit. It cannot convert pending live evidence to PASS."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,datetime,hashlib,json,os,re,subprocess
E=Path(__file__).resolve().parent
P=E.parents[1]
R=P.parent

def sha(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        while b:=f.read(1048576):h.update(b)
    return h.hexdigest()

def read(n):return json.loads((E/n).read_text())
def bound(p,r):return p.is_file() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
def git(*args):
    env=dict(os.environ,GIT_OPTIONAL_LOCKS='0')
    return subprocess.check_output(['git','-c','gc.auto=0',*args],cwd=R,env=env)
def tree(raw):return {r.split(b'\t',1)[1]:r.split(b'\t',1)[0] for r in raw.split(b'\0') if r}

class HTML(HTMLParser):
    def __init__(self):super().__init__();self.nodes=[]
    def handle_starttag(self,tag,attrs):self.nodes.append((tag,dict(attrs)))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write-receipt',action='store_true');args=ap.parse_args()
    issues=[];b=read('preservation-before.json');c=read('commit-receipt.json');push=read('push-receipt.json')
    for r in b['files']:
        if not bound(Path(r['path']),r):issues.append({'kind':'original','path':r['path']})
    auth=json.loads((P/'redirects/fps-redirect-root-proposal-acceptance-20261025.json').read_text())
    if sha(P/'redirects/fps-redirect-root-proposal-acceptance-20261025.json')!='712e50c550a1b1fe0b8a951931e1277607880bd71922e6f59a2becf69c21b3d7':issues.append({'kind':'root_authority'})
    changed=git('diff-tree','--no-commit-id','--name-only','-r',c['parent'],c['commit']).decode().splitlines()
    if sorted(changed)!=sorted(auth['allowlist']):issues.append({'kind':'commit_allowlist','actual':changed})
    prep=P/'redirects/fps-redirect-preparation-sol-20261025'
    for path in changed:
        if git('show',c['commit']+':'+path)!=(prep/'proposed'/path).read_bytes() or (E/'proposed'/path).read_bytes()!=(prep/'proposed'/path).read_bytes():issues.append({'kind':'exact_approved_bytes','path':path})
    old=tree((E/'before/docs-tree.raw').read_bytes());new=tree(git('ls-tree','-r','-z',c['commit'],'--','docs'))
    untouched=[p for p in old if p.decode() not in changed]
    if set(old)!=set(new) or any(old[p]!=new[p] for p in untouched):issues.append({'kind':'other_docs_modes_blobs'})
    for r in read('remote-preflight.json')['objects']:
        bb=git('show',c['parent']+':'+r['path'])
        if len(bb)!=r['bytes'] or hashlib.sha256(bb).hexdigest()!=r['sha256']:issues.append({'kind':'fresh_parent_object','path':r['path']})
        if r['path'] not in changed and git('show',c['commit']+':'+r['path'])!=bb:issues.append({'kind':'protected_asset','path':r['path']})
    if push['exit_code'] or not push['remote_equals_exact_commit'] or push['commit']!=c['commit']:issues.append({'kind':'ordinary_push'})
    local=read('git-local-before.json')
    if git('rev-parse','HEAD').decode().strip()!=local['HEAD'] or git('branch','--show-current').decode().strip()!='main' or sha(R/'.git/index')!=local['shared_index_sha256']:issues.append({'kind':'shared_local_git'})
    if (E/'runtime/isolated-index').exists():issues.append({'kind':'temporary_index_left'})
    parser=HTML();parser.feed((E/'proposed/docs/papers/fps-equality/index.html').read_text())
    dest=auth['target_URL'];canonical=[a.get('href') for t,a in parser.nodes if t=='link' and a.get('rel')=='canonical'];refresh=[a.get('content') for t,a in parser.nodes if t=='meta' and a.get('http-equiv','').lower()=='refresh']
    if canonical!=[dest] or refresh!=['0; url='+dest]:issues.append({'kind':'static_redirect_target'})
    live=read('live/attempt-1/receipt.json')
    for r in live['responses']:
        if not bound(E/r['body_file'],r):issues.append({'kind':'raw_HTTP_body','key':r['key']})
    arrivals=read('browser-arrival.json');cleanup=read('browser-cleanup.json')
    if arrivals['automatic_arrival_PASS']:issues.append({'kind':'unexpected_pending_report_conflict'})
    if not cleanup['own_tabs_closed'] or cleanup['remaining_own'] or not cleanup['all_original_ID_URL_preserved']:issues.append({'kind':'browser_cleanup'})
    for s in read('screenshot-manifest.json')['screenshots']:
        if not bound(E/s['file'],s):issues.append({'kind':'raw_frame'})
        out=subprocess.check_output(['/usr/bin/sips','-g','pixelWidth','-g','pixelHeight',str(E/s['file'])],text=True)
        dims=[int(re.search(r'pixelWidth: (\d+)',out)[1]),int(re.search(r'pixelHeight: (\d+)',out)[1])]
        if dims!=[2056,1146] or dims!=[s['width'],s['height']]:issues.append({'kind':'raw_frame_dimensions'})
    if (E/'evidence-manifest.json').exists():
        for r in read('evidence-manifest.json')['files']:
            if not bound(E/r['file'],r):issues.append({'kind':'manifest','file':r['file']})
        if sha(E/'evidence-manifest.json')!=read('SEAL.json')['evidence_manifest_sha256']:issues.append({'kind':'seal'})
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'EXACT_RELEASE_AND_CUSTODY_PASS_LIVE_REDIRECT_PENDING' if not issues else 'FAIL',
        'all_static_custody_checks_pass':not issues,'original_bindings':len(b['files']),'current_site_files':484,'local_docs_files':257,
        'commit':c['commit'],'parent':c['parent'],'changed_paths':changed,'remote_docs_total':len(old),'other_docs_blobs_modes_preserved':len(untouched),
        'ordinary_HTTP_responses':len(live['responses']),'ordinary_HTTP_exact_expected':sum(r['exact_expected'] for r in live['responses']),
        'owned_tabs_closed':len(cleanup['created_ids']),'original_tabs_preserved':cleanup['original_count'],'raw_browser_frames':1,
        'live_automatic_redirect_PASS':False,'remaining_gap':'GitHub Pages build/cache propagation, exact old article/index served bytes and fresh actual automatic arrival under newly granted UI ownership',
        'issues':issues}
    if args.write_receipt:(E/'audit-receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2));return bool(issues)

if __name__=='__main__':raise SystemExit(main())
