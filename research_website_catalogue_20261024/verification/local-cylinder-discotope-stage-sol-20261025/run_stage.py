"""Render only the authorized pair and check the real minimal overlay."""
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
import ast,datetime,hashlib,json,os,re,subprocess,signal
import xml.etree.ElementTree as ET

O=Path(__file__).resolve().parent;R=O.parents[1];S=O/'public';LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'
ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(O)+os.pathsep+str(R/'scripts'))
IDS=['23387774','23074543']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,x):(O/n).write_text(x if isinstance(x,str) else json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def run(cmd):
    proc=subprocess.Popen([PY,'-B',*cmd],env=ENV,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    try:out,err=proc.communicate(timeout=90)
    except subprocess.TimeoutExpired:
        os.killpg(proc.pid,signal.SIGTERM);out,err=proc.communicate(timeout=5);raise RuntimeError('private_child_timeout')
    return {'argv':cmd,'exit':proc.returncode,'stdout':out,'stderr':err}
def records():
    baseline=json.loads((O/'protected-before.json').read_text())
    for rel in ['research/index.html','research/sitemap.xml']:
        p=LIVE/rel;b=next(x for x in baseline['files'] if x['path']==str(p));assert sha(p)==b['sha256']
    index=(LIVE/'research/index.html').read_text();ilist=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',index,re.S).group(1))['mainEntity']
    oldurls=[x['url'] for x in ilist['itemListElement']];mapped={}
    for p in (R/'papers').glob('*/publication.json'):
        c=json.loads(p.read_text());url='https://aleckriebel.com/research/'+c['slug']+'/'
        if url in oldurls:mapped[url]=p.parent.name
    checker=ast.parse((O/'inputs/final-content-check.py').read_text());oldtex=next(ast.literal_eval(n.value) for n in checker.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='TEX_PATHS' for t in n.targets))
    oldids=[mapped[u] for u in oldurls if u in mapped]
    assert len(oldurls)==60 and len(oldids)==len(oldtex)==59 and set(oldids)==set(oldtex)
    result={'UTC':datetime.datetime.now(datetime.timezone.utc).isoformat(),'baseline_index_urls_in_order':oldurls,'old_configured_record_ids_in_order':oldids,'old_checker_record_ids':list(oldtex),'unmapped_manual_native_urls':[u for u in oldurls if u not in mapped],'authorized_new_record_ids':IDS,'expected_merged_index_items':62,'expected_sitemap_urls':63,'no_glob_promotion':'All config globs are filtered by the frozen60 native URLs;94/95 and any unrelated preparation files are out of scope.'}
    save('FROZEN_INPUT_SET.json',result);return result

class Visible(HTMLParser):
    def __init__(self,h):super().__init__();self.body=False;self.parts=[];self.feed(h)
    def handle_starttag(self,t,a):
        if t=='body':self.body=True
        if self.body and t in ['p','h1','h2','li','br','section','header','footer']:self.parts.append('\n')
    def handle_endtag(self,t):
        if t=='body':self.body=False
        if self.body and t in ['p','h1','h2','li','section']:self.parts.append('\n')
    def handle_data(self,t):
        if self.body:self.parts.append(t)

def main():
    frozen=records();(S/'research').mkdir(parents=True,exist_ok=True)
    for rel in ['research/index.html','research/sitemap.xml']:(S/rel).write_bytes((LIVE/rel).read_bytes())
    receipts=[]
    for rid in IDS:
        proc=run([str(O/'render_page.stage.py'),rid]);assert proc['exit']==0 and not proc['stderr'],proc
        receipts.append(json.loads(proc['stdout']))
    save('render-receipts.json',{'scope':'PRIVATE_OVERLAY_ONLY','receipts':receipts})
    cmd=[str(O/'stage_reader.py'),str(O/'final-content-check.stage.py'),*IDS,'--site',str(S),'--output-dir',str(O),'--output-stem','target-checks']
    proc=run(cmd);save('target-checks.stdout.txt',proc['stdout']);save('target-checks.stderr.txt',proc['stderr'])
    report=json.loads((O/'target-checks.json').read_text()) if (O/'target-checks.json').exists() else None
    if proc['exit'] or proc['stderr'] or report is None or report['status']!='PASS':
        save('target-initial-failure.json',{'execution':proc,'report':report});raise RuntimeError('target_checks_failed:'+str(report['issues'] if report else proc['stderr']))
    for rid in IDS:
        c=json.loads((R/'papers'/rid/'publication.json').read_text());h=(S/'research'/c['slug']/'index.html').read_text();v=Visible(h)
        save('public-copy-'+rid+'.txt','\n\n'.join(' '.join(x.split()) for x in ''.join(v.parts).split('\n') if x.strip())+'\n')
        sections=[{'id':sid,'heading':unescape(re.search('<h2>(.*?)</h2>',seg,re.S).group(1)),'paragraphs':[unescape(re.sub('<[^>]+>','',x)) for x in re.findall('<p>(.*?)</p>',seg,re.S)],'list_items':[unescape(re.sub('<[^>]+>','',x)) for x in re.findall('<li>(.*?)</li>',seg,re.S)]} for sid,seg in re.findall('<section id="([^"]+)">(.*?)</section>',h,re.S)]
        save('public-sections-'+rid+'.json',{'record_id':rid,'source':'ACTUAL_PRIVATE_RENDERER_OUTPUT','sections':sections})
    old_index=(LIVE/'research/index.html').read_text();new_index=(S/'research/index.html').read_text()
    ilist=lambda text:json.loads(re.search('<script type="application/ld\\+json">(.*?)</script>',text,re.S).group(1))['mainEntity']
    old,new=ilist(old_index),ilist(new_index);oldlis=re.findall('<li>.*?</li>',old_index,re.S);newlis=re.findall('<li>.*?</li>',new_index,re.S)
    newurls=['https://aleckriebel.com/research/'+json.loads((R/'papers'/rid/'publication.json').read_text())['slug']+'/' for rid in IDS]
    assert len(oldlis)==old['numberOfItems']==60 and len(newlis)==new['numberOfItems']==62 and newlis[:60]==oldlis and new['itemListElement'][:60]==old['itemListElement']
    assert [x['url'] for x in new['itemListElement'][60:]]==newurls and len({x['url'] for x in new['itemListElement']})==62
    xmlurls=lambda p:[x.text for x in ET.fromstring(p.read_text()).iter() if x.tag.endswith('loc')]
    oldxml,newxml=xmlurls(LIVE/'research/sitemap.xml'),xmlurls(S/'research/sitemap.xml')
    assert len(oldxml)==61 and newxml[:61]==oldxml and newxml[61:]==newurls and len(newxml)==len(set(newxml))==63
    files=sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
    assert len(files)==10
    save('index-sitemap-overlay-checks.json',{'status':'PASS','old_visible_entries_byte_identical':60,'old_structured_entries_unchanged_in_order':60,'merged_index_count':62,'old_sitemap_entries_unchanged_in_order':61,'merged_sitemap_count':63,'only_new_URLs_in_order':newurls,'actual_private_overlay_files':files,'overlay_file_count':10,'predicted_whole_public_files':492,'CSS_robots_favicon_old_assets':'Read-only fallback to protected production; not copied.'})
    print(json.dumps({'status':'PASS_TARGET_AND_INDEX_CHECKS','target_checks':sum(len(x['checks']) for x in report['papers'].values()),'overlay_files':10,'index':62,'sitemap':63},indent=2))

if __name__=='__main__':main()
