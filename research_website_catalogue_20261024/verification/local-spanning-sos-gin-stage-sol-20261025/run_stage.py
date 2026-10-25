"""Render only the authorized3 and check the actual minimal private overlay."""
from pathlib import Path
from html.parser import HTMLParser
from html import unescape
import datetime,hashlib,json,os,re,signal,subprocess,xml.etree.ElementTree as ET
O=Path(__file__).resolve().parent;P=O.parents[1];S=O/'public';LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
PY='/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3';ENV=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONPATH=str(O)+os.pathsep+str(P/'scripts'))
IDS=['23181280','23442760','23395703']
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(n,x):(O/n).write_text(x if isinstance(x,str) else json.dumps(x,indent=2,ensure_ascii=False)+'\n')
def run(args,opt=False):
    proc=subprocess.Popen([PY,'-B']+(['-O'] if opt else [])+args,env=ENV,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
    try:out,err=proc.communicate(timeout=90)
    except subprocess.TimeoutExpired:os.killpg(proc.pid,signal.SIGTERM);out,err=proc.communicate(timeout=5);raise RuntimeError('bounded_private_child_timeout')
    return {'argv':args,'optimized':opt,'exit':proc.returncode,'stdout':out,'stderr':err}
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
    baseline=json.loads((O/'protected-before.json').read_text());frozen=json.loads((O/'FROZEN_INPUT_SET.json').read_text());(S/'research').mkdir(parents=True,exist_ok=True)
    for rel in ['research/index.html','research/sitemap.xml']:
        path=LIVE/rel;ref=next(x for x in baseline['files'] if x['path']==str(path))
        if sha(path)!=ref['SHA256']:raise RuntimeError('actual_current_baseline_changed')
        (S/rel).write_bytes(path.read_bytes())
    receipts=[]
    for rid in IDS:
        proc=run([str(O/'render_page.stage.py'),rid])
        if proc['exit'] or proc['stderr']:raise RuntimeError(proc)
        receipts.append(json.loads(proc['stdout']))
    save('RENDER_RECEIPTS.json',receipts)
    proc=run([str(O/'stage_reader.py'),str(O/'final-content-check.stage.py'),*IDS,'--site',str(S),'--output-dir',str(O),'--output-stem','target-checks'])
    save('target-checks.execution.json',proc);report=json.loads((O/'target-checks.json').read_text())
    if proc['exit'] or proc['stderr'] or report['status']!='PASS':
        save('target-initial-failure-'+datetime.datetime.now(datetime.timezone.utc).strftime('%H%M%S')+'.json',{'execution':proc,'report':report});raise RuntimeError(report['issues'])
    for rid in IDS:
        c=json.loads((P/'papers'/rid/'publication.json').read_text());h=(S/'research'/c['slug']/'index.html').read_text();v=Visible(h)
        save('public-copy-'+rid+'.txt','\n\n'.join(' '.join(x.split()) for x in ''.join(v.parts).split('\n') if x.strip())+'\n')
        save('public-sections-'+rid+'.json',[{'id':sid,'paragraphs':[unescape(x) for x in re.findall('<p>(.*?)</p>',seg,re.S)],'list_items':[unescape(re.sub('<[^>]+>','',x)) for x in re.findall('<li>(.*?)</li>',seg,re.S)]} for sid,seg in re.findall('<section id="([^"]+)">(.*?)</section>',h,re.S)])
    old=(LIVE/'research/index.html').read_text();new=(S/'research/index.html').read_text();jl=lambda s:json.loads(re.search('<script type="application/ld\\+json">(.*?)</script>',s,re.S).group(1))['mainEntity'];a,b=jl(old),jl(new)
    oldlis=re.findall('<li>.*?</li>',old,re.S);newlis=re.findall('<li>.*?</li>',new,re.S)
    newurls=['https://aleckriebel.com/research/'+json.loads((P/'papers'/r/'publication.json').read_text())['slug']+'/' for r in IDS]
    if not(len(oldlis)==62 and len(newlis)==65 and newlis[:62]==oldlis and b['itemListElement'][:62]==a['itemListElement'] and b['numberOfItems']==65 and [x['url'] for x in b['itemListElement'][62:]]==newurls):raise RuntimeError('exact_existing62_index_boundary')
    urls=lambda p:[e.text for e in ET.fromstring(p.read_text()).iter() if e.tag.endswith('loc')];oldxml,newxml=urls(LIVE/'research/sitemap.xml'),urls(S/'research/sitemap.xml')
    if not(len(oldxml)==63 and len(newxml)==len(set(newxml))==66 and newxml[:63]==oldxml and newxml[63:]==newurls):raise RuntimeError('exact_sitemap_boundary')
    files=sorted(str(p.relative_to(S)) for p in S.rglob('*') if p.is_file())
    if len(files)!=14:raise RuntimeError('only14_overlay_files')
    save('OVERLAY_CHECKS.json',{'status':'PASS','actual_files':files,'file_count':14,'old_visible_index_entries_byte_identical':62,'old_structured_index_entries_unchanged_in_order':62,'old_sitemap_URLs_unchanged_in_order':63,'new_URLs_only':newurls,'index_items':65,'sitemap_URLs':66,'predicted_whole_public_files':504,'native_gate_not_advanced':True})
    print(json.dumps({'status':'PASS_ACTUAL_PRIVATE_TARGETS','checks':sum(len(x['checks']) for x in report['papers'].values()),'overlay_files':14,'index':65,'sitemap':66},indent=2))
if __name__=='__main__':main()
