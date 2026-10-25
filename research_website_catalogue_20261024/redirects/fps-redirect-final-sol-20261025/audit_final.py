#!/usr/bin/env python3
"""Read-only additive FPS final-gate and predecessor custody audit."""
from pathlib import Path
from html.parser import HTMLParser
import argparse,datetime,hashlib,json,subprocess,re
E=Path(__file__).resolve().parent
P=E.parents[1]
R=P.parent
OLD=P/'redirects/fps-redirect-release-sol-20261025'
DEST='https://aleckriebel.com/research/fps-second-moment-equality/'
OLDURL='https://aleckriebel.github.io/Math/papers/fps-equality/'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def bound(p,r):return p.is_file() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
def git(*a):return subprocess.check_output(['git','-c','gc.auto=0',*a],cwd=R).decode().strip()
class HTML(HTMLParser):
    def __init__(self):super().__init__();self.nodes=[]
    def handle_starttag(self,t,a):self.nodes.append((t,dict(a)))

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write-receipt',action='store_true');args=ap.parse_args();issues=[]
    if sha(OLD/'SEAL.json')!='60c2ad21428552344264b191f02399ed6238368a5b6aae1f936bb931203ecfb3' or sha(OLD/'evidence-manifest.json')!='9cde21efc72d8bec2815e9caf94045229152f71c19f1d5ecc505f0053b9fff40':issues.append('predecessor_seal')
    original=read(OLD/'preservation-before.json')['files'];previous=read(OLD/'evidence-manifest.json')['files']
    for r in original:
        if not bound(Path(r['path']),r):issues.append('original:'+r['path'])
    for r in previous:
        if not bound(OLD/r['file'],r):issues.append('predecessor:'+r['file'])
    build=read(E/'pages-build-final.json')['response'];lineage=read(E/'completed-build-lineage.json')
    if build['status']!='built' or build['commit']!=lineage['build_commit'] or git('rev-parse',build['commit']+':docs')!='7a24ec1dcb73a5e06ba82ff9cccda54e73f9deec':issues.append('completed_build_docs')
    if subprocess.run(['git','merge-base','--is-ancestor','549c43a6d76f211aa9a5f9b0e2c5f9f2765b185a',build['commit']],cwd=R).returncode:issues.append('build_release_ancestry')
    live=read(E/'live/receipt.json')
    if len(live['responses'])!=9 or not live['all9_exact']:issues.append('nine_live_checks')
    for r in live['responses']:
        if not bound(E/r['body_file'],r) or (E/r['body_file']).read_bytes()!=Path(r['expected_path']).read_bytes() or not r['ordinary_GET_no_cache_bypass'] or r['status']!=200:issues.append('live_body:'+r['key'])
    h=HTML();h.feed((E/'live/old_article.html').read_text())
    canonical=[a.get('href') for t,a in h.nodes if t=='link' and a.get('rel')=='canonical'];refresh=[a.get('content') for t,a in h.nodes if t=='meta' and a.get('http-equiv','').lower()=='refresh'];links=[a.get('href') for t,a in h.nodes if t=='a']
    if canonical!=[DEST] or refresh!=['0; url='+DEST] or DEST not in links or not all(x in links for x in ['./paper.pdf','./source-and-verification.zip','./paper.tex']):issues.append('served_redirect_semantics')
    browser=read(E/'browser-arrival.json');cleanup=read(E/'browser-cleanup.json')
    if browser['only_goto_URL']!=OLDURL or browser['requested_URL']!=OLDURL or browser['actual']['url']!=DEST or browser['actual']['canonical']!=DEST or not browser['automatic_arrival_PASS'] or browser['direct_target_navigation_used'] or browser['fallback_click_used']:issues.append('actual_automatic_arrival')
    title='Equality in the Fradelizi–Paouris–Schütt second-moment inequality'
    if 'Paper moved' not in (E/'automatic-arrival.dom.txt').read_text() or title not in (E/'automatic-arrival-settled.dom.txt').read_text() or DEST not in (E/'automatic-arrival.ax.txt').read_text():issues.append('actual_DOM_AX_chain')
    for r in read(E/'screenshot-manifest.json')['screenshots']:
        f=E/r['file']
        if not bound(f,r):issues.append('raw_frame_binding')
        s=subprocess.check_output(['/usr/bin/sips','-g','pixelWidth','-g','pixelHeight',str(f)],text=True);dims=[int(re.search(r'pixelWidth: (\d+)',s)[1]),int(re.search(r'pixelHeight: (\d+)',s)[1])]
        if dims!=[2056,1146] or dims!=[r['width'],r['height']]:issues.append('raw_frame_dimensions')
    if not cleanup['all_created_absent'] or cleanup['remaining_own'] or cleanup['original_count']!=11 or not cleanup['all_original_ID_URL_preserved'] or not cleanup['viewport_reset']:issues.append('cleanup')
    state=read(E/'git-local-before.json')
    if git('rev-parse','HEAD')!=state['HEAD'] or git('branch','--show-current')!=state['branch'] or sha(R/'.git/index')!=state['shared_index_sha256']:issues.append('local_git_state')
    if (E/'evidence-manifest.json').exists():
        for r in read(E/'evidence-manifest.json')['files']:
            if not bound(E/r['file'],r):issues.append('manifest:'+r['file'])
        if sha(E/'evidence-manifest.json')!=read(E/'SEAL.json')['evidence_manifest_sha256']:issues.append('own_seal')
    result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_FINAL_LIVE_FPS_STATIC_REDIRECT' if not issues else 'FAIL','all_pass':not issues,'predecessor_owned_outputs_rehashed':len(previous),'original_bindings_rehashed':len(original),'ordinary_live_exact_checks':len(live['responses']),'completed_build':build['commit'],'actual_automatic_browser_arrival':browser['automatic_arrival_PASS'],'owned_tabs_closed':len(cleanup['created_ids']),'original_tabs_preserved':cleanup['original_count'],'raw_arrival_frames':1,'no_Git_site_core_native_writes':True,'overall_goal_complete':False,'issues':issues}
    if args.write_receipt:(E/'audit-receipt.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2));return bool(issues)

if __name__=='__main__':raise SystemExit(main())
