#!/usr/bin/env python3
"""Read-only audit of the FPS redirect proposal; no Git index or working-tree writes."""
from pathlib import Path
from html.parser import HTMLParser
import argparse, datetime, hashlib, json, subprocess, xml.etree.ElementTree as ET

E=Path(__file__).resolve().parent
P=E.parents[1]
REPO=P.parent

def sha(data): return hashlib.sha256(data).hexdigest()
def read(name): return json.loads((E/name).read_text())
def git(*args): return subprocess.check_output(['git','-c','gc.auto=0',*args],cwd=REPO)

class HTML(HTMLParser):
    def __init__(self): super().__init__(); self.nodes=[]
    def handle_starttag(self,tag,attrs): self.nodes.append((tag,dict(attrs)))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write-receipt',action='store_true');args=ap.parse_args()
    problems=[];proposal=read('proposal.json');remote=read('remote-preflight.json');base=read('preservation-before.json')
    effective_pin=remote['origin_main']
    if (E/'remote-revalidation.json').exists():
        revalidation=read('remote-revalidation.json')
        effective_pin=revalidation['final_fresh_pin']
        if revalidation['meaningful_conflict'] or not revalidation['all_docs_tree_unchanged'] or revalidation['changed_docs_paths']:
            problems.append('remote-revalidation-conflict')
    if proposal['base_origin_main']!=effective_pin:problems.append('proposal-effective-pin')
    allow=['docs/papers/fps-equality/index.html','docs/index.html']
    if proposal['allowlist']!=allow:problems.append('allowlist')
    actual=sorted(str(f.relative_to(E/'proposed')) for f in (E/'proposed').rglob('*') if f.is_file())
    if actual!=sorted(allow):problems.append('proposed-files')
    dest=proposal['target_url'];old=proposal['old_url']
    html=(E/'proposed'/allow[0]).read_text();parser=HTML();parser.feed(html)
    canon=[a.get('href') for t,a in parser.nodes if t=='link' and a.get('rel')=='canonical']
    refresh=[a.get('content') for t,a in parser.nodes if t=='meta' and a.get('http-equiv','').lower()=='refresh']
    anchors=[a.get('href') for t,a in parser.nodes if t=='a']
    if canon!=[dest] or refresh!=['0; url='+dest] or anchors.count(dest)!=1:problems.append('canonical-refresh-fallback')
    if any(t in ['script','iframe','form','base'] for t,a in parser.nodes):problems.append('unneeded-active-content')
    if not all(x in anchors for x in ['./paper.pdf','./source-and-verification.zip','./paper.tex']):problems.append('original-file-links')
    before=(E/'before/docs/index.html').read_bytes();after=(E/'proposed/docs/index.html').read_bytes()
    oldhref=b'href="./papers/fps-equality/"';newhref=('href="'+dest+'"').encode()
    if before.count(oldhref)!=1 or after!=before.replace(oldhref,newhref) or after.replace(newhref,oldhref)!=before:problems.append('exact-single-index-href')
    if b'href="./papers/fps-equality/paper.pdf"' not in after:problems.append('historical-manuscript-link')
    sitemap=(E/'before/docs/sitemap.xml').read_bytes();root=ET.fromstring(sitemap)
    locs=[x.text for x in root.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url/{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    if old in locs or (E/'proposed/docs/sitemap.xml').exists():problems.append('unwarranted-sitemap-change')
    for r in remote['objects']:
        b=git('show',effective_pin+':'+r['path'])
        if len(b)!=r['bytes'] or sha(b)!=r['sha256'] or b!=(E/'before'/r['path']).read_bytes():problems.append('remote-object-'+r['path'])
    pre=json.loads((P/'redirects/fps-legacy-identity-preflight-root-20261025.json').read_text())
    for r in pre['assets']:
        b=(E/'before'/r['path']).read_bytes()
        if len(b)!=r['bytes'] or sha(b)!=r['sha256']:problems.append('identity-preflight-'+r['path'])
    for r in proposal['exact_latest_remote_source_identities']:
        if (E/'before'/r['remote_path']).read_bytes()!=Path(r['current_source']).read_bytes():problems.append('current-source-'+r['remote_path'])
    for r in proposal['path_changes']:
        for side in ['before','after']:
            b=(E/('before' if side=='before' else 'proposed')/r['path']).read_bytes()
            if len(b)!=r[side+'_bytes'] or sha(b)!=r[side+'_sha256']:problems.append(side+'-proposal-binding-'+r['path'])
    changed=[]
    for r in base['files']:
        f=Path(r['path'])
        if not f.is_file() or f.stat().st_size!=r['bytes'] or sha(f.read_bytes())!=r['sha256']:changed.append(r['path'])
    if changed:problems.append({'changed_originals':changed})
    local=read('git-local-before.json')
    if git('branch','--show-current').decode().strip()!='main' or git('rev-parse','HEAD').decode().strip()!=local['HEAD']:problems.append('local-branch-or-HEAD')
    if sha((REPO/'.git/index').read_bytes())!=local['shared_index_sha256']:problems.append('shared-index')
    if git('show',effective_pin+':docs/sitemap.xml')!=sitemap:problems.append('sitemap-original')
    if (E/'evidence-manifest.json').exists():
        for r in read('evidence-manifest.json')['files']:
            f=E/r['file']
            if not f.is_file() or f.stat().st_size!=r['bytes'] or sha(f.read_bytes())!=r['sha256']:problems.append('manifest-'+r['file'])
        if sha((E/'evidence-manifest.json').read_bytes())!=read('SEAL.json')['evidence_manifest_sha256']:problems.append('manifest-seal')
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_REVIEWABLE_PROPOSAL_ONLY' if not problems else 'FAIL',
        'base_origin_main':effective_pin,'base_docs_blobs':remote['docs_blobs'],'proposed_changed_paths':len(allow),
        'all_other_remote_docs_blobs_planned_unchanged':remote['docs_blobs']-len(allow),'sitemap_entries_unchanged':len(locs),
        'original_bindings':len(base['files']),'unchanged_original_bindings':len(base['files'])-len(changed),
        'local_shared_index_HEAD_branch_preserved':not any(x in problems for x in ['local-branch-or-HEAD','shared-index']),
        'no_live_browser_native_or_remote_installation_verification_claim':True,'problems':problems}
    if args.write_receipt:(E/'audit-receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2));return bool(problems)

if __name__=='__main__':raise SystemExit(main())
