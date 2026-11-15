"""Bounded released docs reader; read-only Git object access, no PDF extraction."""
from pathlib import Path
from html.parser import HTMLParser
import os,subprocess,hashlib,json,re,unicodedata
O=Path(__file__).resolve().parent
P=O.parent.parent
REPO=P.parent
TREE='7a24ec1dcb73a5e06ba82ff9cccda54e73f9deec'
def require(ok,label):
    if not ok:raise RuntimeError(label)
def load(p):return json.loads(Path(p).read_text())
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(p):
    b=Path(p).read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def object_command(args):
    # Only cat-file/ls-tree with fixed object IDs. No ref/index/worktree mutation.
    require(args[0] in ['cat-file','ls-tree'],'read-only object command allowlist')
    return subprocess.run(['git',*args],cwd=REPO,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0','PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,check=True,timeout=45).stdout
def norm(s):
    s=unicodedata.normalize('NFKC',s).replace('\u00ad','').replace('’',"'").replace('‘',"'")
    s=''.join(c for c in unicodedata.normalize('NFKD',s) if not unicodedata.combining(c))
    s=re.sub(r'(?<=\w)-\s*\n\s*(?=\w)','',s)
    return re.sub(r'\s+',' ',re.sub('[‐‑‒–—−]','-',s)).casefold()
class HTML(HTMLParser):
    def __init__(self):super().__init__();self.skip=0;self.text=[];self.links=[];self.title=[];self.in_title=False
    def handle_starttag(self,t,a):
        a=dict(a)
        if t in ['script','style']:self.skip+=1
        if t=='title':self.in_title=True
        if t in ['p','div','h1','h2','h3','br','li','section']:self.text.append('\n')
        if t=='a' and 'href' in a:self.links.append(a['href'])
    def handle_endtag(self,t):
        if t in ['script','style']:self.skip-=1
        if t=='title':self.in_title=False
    def handle_data(self,d):
        if not self.skip:self.text.append(d)
        if self.in_title:self.title.append(d)
def corpus():
    expected=load(O/'DOCS_OBJECT_BINDINGS.json');extracts=load(O/'REUSED_EXTRACT_BINDINGS.json')
    listing=object_command(['ls-tree','-r','-l','-z',TREE]);actual=[]
    for row in listing.rstrip(b'\0').split(b'\0'):
        a,path=row.split(b'\t',1);mode,kind,oid,size=a.decode().split();actual.append({'path':'docs/'+path.decode(),'mode':mode,'kind':kind,'blob':oid,'bytes':int(size)})
    require(actual==[{k:r[k] for k in ['path','mode','kind','blob','bytes']} for r in expected],'complete fixed docs tree inventory')
    bypdf={r['public_path']:r for r in extracts};require(len(bypdf)==76,'76 distinct reused PDFs')
    proc=subprocess.Popen(['git','cat-file','--batch'],cwd=REPO,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0','PYTHONDONTWRITEBYTECODE':'1'},stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    proc.stdin.write(('\n'.join(r['blob'] for r in actual)+'\n').encode());proc.stdin.close()
    reps=[];html=[];data={}
    for r in expected:
        require(proc.stdout.readline().decode().split()==[r['blob'],'blob',str(r['bytes'])],'object framing')
        b=proc.stdout.read(r['bytes']);require(proc.stdout.read(1)==b'\n','object terminator')
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob'] and sha(b)==r['sha256'],'whole blob identity '+r['path']);data[r['path']]=b
        if r['path'].endswith('.pdf'):
            x=bypdf[r['path']];require(x['pdf_blob']==r['blob'] and x['pdf_sha256']==sha(b),'PDF parent authentication')
            require(bind(x['path'])=={k:x[k] for k in ['bytes','sha256']},'existing complete derivative authentication')
            reps.append({'path':r['path'],'kind':'complete_reused_PDF_text','text':Path(x['path']).read_text()})
        else:
            try:s=b.decode('utf8')
            except UnicodeDecodeError:continue
            if '\0' in s:continue
            reps.append({'path':r['path'],'kind':'raw_UTF8_blob','text':s})
            if r['path'].endswith('.html'):
                doc=HTML();doc.feed(s);reps.append({'path':r['path'],'kind':'decoded_visible_HTML','text':''.join(doc.text)})
                html.append({'path':r['path'],'blob':r['blob'],'sha256':sha(b),'title':''.join(doc.title),'hrefs':doc.links})
    require(proc.wait(timeout=30)==0 and not proc.stderr.read(),'read-only object process exit')
    require(len(expected)==254 and len(html)==47 and len(reps)==260 and sum(x['pages'] for x in extracts)==854,'bounded coverage counts')
    return expected,extracts,reps,html,data
def queries(targets):
    q={}
    for id,r in targets.items():
        q[id+'_record_or_DOI']=[re.escape(id),re.escape(str(r['conceptrecid'])),re.escape(r['doi'])]
        q[id+'_exact_title']=[re.escape(norm(r['title']))]
    q.update({
        '23441890_distinctive':[r'two.tail.{0,35}ambient',r'ambient.{0,20}conjugat.{0,35}dlab',r'21[. -]149',r'\bdlab\b'],
        '23441890_broad':[r'zenkov',r'medvedev',r'kourovka',r'two.tail',r'ambient.{0,20}conjugat'],
        '23174283_distinctive':[r'spherical.{0,15}fibonacci',r'exact.{0,20}chordal.{0,20}separation',r'owr[ _-]*12012[ _-]*001'],
        '23174283_broad':[r'\bfibonacci\b',r'\bbrauchart\b',r'\bzaremba\b',r'spherical.{0,25}(separation|minimum|distance)',r'\blambert\b']})
    return q
def search(reps,q):
    out=[]
    for r in reps:
        s=norm(r['text']);groups={}
        for group,pats in q.items():
            hits=[]
            for pat in pats:
                for m in re.finditer(pat,s):hits.append({'pattern':pat,'match':m.group(),'offset':m.start(),'context':s[max(0,m.start()-150):m.end()+230]})
            groups[group]=hits
        out.append({'path':r['path'],'kind':r['kind'],'normalized_characters':len(s),'groups':groups})
    return out
