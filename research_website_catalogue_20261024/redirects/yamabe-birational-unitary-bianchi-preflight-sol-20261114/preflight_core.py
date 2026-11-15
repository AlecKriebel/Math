"""Read-only released-object and derivative authentication/search; no extraction."""
from pathlib import Path
from html.parser import HTMLParser
import hashlib, json, os, re, subprocess, unicodedata

O=Path(__file__).resolve().parent
P=O.parent.parent
R=P.parent
PRIOR=P/'redirects/artin-devissage-preflight-sol-20261025'
COMMIT='f89eae652394165a7f0e42aa41e9d0cce8dcfab7'
TREE='7a24ec1dcb73a5e06ba82ff9cccda54e73f9deec'
RECORDS=['23383952','23539734','22929857','23320818']
ENV=dict(os.environ,GIT_OPTIONAL_LOCKS='0',PYTHONDONTWRITEBYTECODE='1')
def need(v,m):
    if not v: raise RuntimeError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def binding(p):
    b=Path(p).read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def load(p):return json.loads(Path(p).read_text())
def git(*a):return subprocess.run(['git',*a],cwd=R,env=ENV,capture_output=True,check=True,timeout=45).stdout
def norm(s):
    s=unicodedata.normalize('NFKC',s).replace('\u00ad','').replace('’',"'").replace('‘',"'")
    s=''.join(c for c in unicodedata.normalize('NFKD',s) if not unicodedata.combining(c))
    s=re.sub(r'(?<=\w)-\s*\n\s*(?=\w)','',s)
    return re.sub(r'\s+',' ',re.sub('[‐‑‒–—−]','-',s)).casefold()
class HTMLIdentity(HTMLParser):
    def __init__(self):
        super().__init__();self.parts=[];self.skip=0;self.links=[];self.canonicals=[];self.ids=[]
    def handle_starttag(self,t,a):
        d=dict(a)
        if t in ['script','style']: self.skip+=1
        if t in ['p','h1','h2','h3','li','div','section','br']:self.parts.append('\n')
        if t=='a' and 'href' in d:self.links.append(d['href'])
        if t=='link' and d.get('rel')=='canonical':self.canonicals.append(d.get('href'))
        if 'id' in d:self.ids.append(d['id'])
    def handle_endtag(self,t):
        if t in ['script','style']:self.skip-=1
    def handle_data(self,d):
        if not self.skip:self.parts.append(d)
def prior_authenticate():
    m=load(PRIOR/'FINAL_MANIFEST.json');s=load(PRIOR/'FINAL_SEAL.json')
    need(sha((PRIOR/'FINAL_MANIFEST.json').read_bytes())==s['manifest_sha256'],'Prior manifest seal')
    need(s['docs_tree']==TREE,'Prior docs tree')
    out=[]
    for x in m['files']:
        p=PRIOR/x['path'];need(binding(p)=={k:x[k] for k in ['bytes','sha256']},'Prior payload '+str(p))
        out.append({'path':str(p),**binding(p)})
    for n in ['FINAL_MANIFEST.json','FINAL_SEAL.json']:
        out.append({'path':str(PRIOR/n),**binding(PRIOR/n)})
    return out
def corpus():
    need(git('rev-parse',COMMIT+':docs').decode().strip()==TREE,'Released docs tree')
    prior_authenticate()
    old=load(PRIOR/'DOCS_OBJECT_BINDINGS.json');extracts=load(PRIOR/'REUSED_EXTRACT_BINDINGS.json')
    bypdf={x['public_path']:x for x in extracts}
    raw=git('ls-tree','-r','-l','-z',COMMIT,'--','docs');rows=[]
    for part in raw.rstrip(b'\0').split(b'\0'):
        a,p=part.split(b'\t',1);mode,kind,oid,size=a.decode().split()
        rows.append({'path':p.decode(),'mode':mode,'kind':kind,'blob':oid,'bytes':int(size)})
    need(rows==[{k:x[k] for k in ['path','mode','kind','blob','bytes']} for x in old],'Full released corpus inventory differs')
    reps=[];html=[];data_by_path={};bindings=[]
    proc=subprocess.Popen(['git','cat-file','--batch'],cwd=R,env=ENV,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    proc.stdin.write(('\n'.join(x['blob'] for x in rows)+'\n').encode());proc.stdin.close()
    for row,expected in zip(rows,old):
        need(proc.stdout.readline().decode().split()==[row['blob'],'blob',str(row['bytes'])],'Git blob batch header')
        data=proc.stdout.read(row['bytes']);need(proc.stdout.read(1)==b'\n','Git blob framing')
        need(hashlib.sha1(('blob '+str(len(data))+'\0').encode()+data).hexdigest()==row['blob'],'Git blob SHA1')
        b={**row,'sha256':sha(data)};need(b==expected,'Prior/current exact binding '+row['path']);bindings.append(b)
        data_by_path[row['path']]=data
        if row['path'].lower().endswith('.pdf'):
            x=bypdf[row['path']]
            need(x['pdf_blob']==row['blob'] and x['pdf_sha256']==sha(data),'Reused PDF source binding')
            need(binding(x['path'])=={k:x[k] for k in ['bytes','sha256']},'Reused extract bytes')
            reps.append({'path':row['path'],'kind':'complete_reused_PDF_text','text':Path(x['path']).read_text()})
        else:
            try:text=data.decode('utf8')
            except UnicodeDecodeError:continue
            if '\0' in text:continue
            reps.append({'path':row['path'],'kind':'raw_UTF8_blob','text':text})
            if row['path'].lower().endswith('.html'):
                h=HTMLIdentity();h.feed(text);visible=''.join(h.parts)
                reps.append({'path':row['path'],'kind':'decoded_visible_HTML','text':visible})
                ti=re.search(r'<title[^>]*>(.*?)</title>',text,re.I|re.S)
                html.append({'path':row['path'],'blob':row['blob'],'sha256':sha(data),'title':ti.group(1) if ti else None,
                             'canonical_links':h.canonicals,'hrefs':h.links,'ids':h.ids})
    need(proc.wait(timeout=30)==0 and not proc.stderr.read(),'Git blob batch exit')
    need(len(bindings)==254 and len(extracts)==76 and len(html)==47 and len(reps)==260,'Corpus counts')
    return bindings,extracts,reps,html,data_by_path,raw
def targets():
    out={};external=[]
    for r in RECORDS:
        T=P/'papers'/r;ready=load(T/'sources/SOURCE_READY.json');record=load(T/'sources/record.raw.json')
        files=[T/'sources/SOURCE_READY.json',T/'sources/record.raw.json']
        publication=T/'publication.json';pub=load(publication) if publication.exists() else None
        if pub:files.append(publication)
        assets=ready.get('all_assets_in_original_order',ready.get('all_native_assets_in_original_order'))
        actual=[]
        for x in assets:
            p=Path(x['path']);p=p if p.is_absolute() else T/'sources'/p
            # Row111's original schema spells SHA256 uppercase; preserve the native object.
            digest_key='SHA256' if r=='22929857' else 'sha256'
            need(binding(p)=={'bytes':x['bytes'],'sha256':x[digest_key]},'Native target asset '+str(p))
            need(x['original_api_file_object']==record['files'][len(actual)],'Native file object and order')
            need(hashlib.md5(p.read_bytes()).hexdigest()==record['files'][len(actual)]['checksum'].split(':',1)[1],'Native API MD5')
            actual.append({'path':str(p),**binding(p),'native_digest_field':digest_key,'native_asset_ordinal':len(actual)+1})
            files.append(p)
        tex=[]
        for p in sorted((T/'sources/published-source').rglob('*.tex')):
            # Only native authored TeX is read for literal project/citation links; no program execution.
            if p.stat().st_size>100000:continue
            text=p.read_text(errors='strict');urls=re.findall(r'https?://[^\s<>}]+',text)
            tex.append({'path':str(p),**binding(p),'literal_urls_in_order':urls})
            files.append(p)
        for p in files:external.append({'path':str(p),**binding(p)})
        m=record['metadata']
        out[r]={'title':record['title'],'DOI':record['doi'],'concept_record_id':record['conceptrecid'],
                'native_version':m.get('version'),'declared_publication_date':m.get('publication_date'),
                'native_related_identifiers':m.get('related_identifiers'),'assets_in_native_order':actual,
                'native_TeX_link_bindings':tex,'publication_present':pub is not None,
                'publication_title':pub.get('title') if pub else None,
                'publication_slug':pub.get('slug') if pub else None,
                'canonical_url':pub.get('canonical_url') if pub else None,
                'proposed_canonical_url':pub.get('proposed_canonical_url') if pub else None,
                'AA':None,'publication_observation':'current private metadata; proposed URL is not publication authority'}
    return out,external
def queries(target):
    q={}
    for r,x in target.items():
        q[r+'_record_or_DOI']=[re.escape(r),re.escape(str(x['concept_record_id'])),re.escape(x['DOI'])]
        q[r+'_exact_title']=[re.escape(norm(x['title']))]
    q.update({
      '23383952_distinctive':[r'weighted.{0,15}yamabe',r'yamabe.{0,30}heat.{0,10}trace',r'finite.{0,30}counterexample.{0,50}heat'],
      '23383952_broad':[r'\byamabe\b',r'\bmorpurgo\b',r'\bpinocchio\b',r'weighted.{0,10}heat.{0,10}trace'],
      '23539734_distinctive':[r'fixed.{0,15}birational',r'prime.field.{0,30}cycle',r'cycle.distribution.{0,12}(limit|nonlimit)'],
      '23539734_broad':[r'\bbirational\b',r'\bvivaldi\b',r'cycle.{0,20}distribution',r'finite.field.{0,20}dynamics'],
      '22929857_distinctive':[r'gromov.unitary.lipschitz',r'lipschitz.nonincreasing',r'small.{0,12}unitary',r'unitary.{0,15}valued'],
      '22929857_broad':[r'\bgromov\b',r'unitary.{0,35}deformation',r'cayley.{0,20}transform'],
      '23320818_distinctive':[r'regular.{0,15}zero.area.{0,15}singular',r'weak.{0,10}bianchi.{0,10}defect'],
      '23320818_broad':[r'\bbianchi\b',r'zero.area.{0,15}singular',r'\bburtscher\b',r'dadhich.{0,15}kar',r'\bkiessling\b',r'tahvildar']})
    return q
def search(reps,q):
    results=[]
    for x in reps:
        s=norm(x['text']);groups={}
        for g,pats in q.items():
            hits=[]
            for pat in pats:
                for m in re.finditer(pat,s):
                    hits.append({'pattern':pat,'match':m.group(),'offset':m.start(),'context':s[max(0,m.start()-160):m.end()+260]})
            groups[g]=hits
        results.append({'path':x['path'],'kind':x['kind'],'normalized_characters':len(s),'groups':groups})
    return results
def controls(reps,target):
    unitary=[x['text'] for x in reps if x['path']=='docs/papers/gromov-unitary-lipschitz/paper.pdf']
    cs=[{'name':'unitary actual public complete PDF title','passed':len(unitary)==1 and norm(target['22929857']['title']) in norm(unitary[0])},
        {'name':'known public positive recurrence phrase','passed':any('positive recurrence for single-linkage bimolecular' in norm(x['text']) for x in reps)},
        {'name':'native unitary explicit legacy project URL in actual current article','passed':any(x['path']=='docs/papers/gromov-unitary-lipschitz/index.html' and 'https://aleckriebel.github.io/Math/papers/gromov-unitary-lipschitz/' in x['text'] for x in reps)},
        {'name':'accent apostrophe subscript normalization','passed':norm('déformation Uₙ’s')==norm("deformation Un's")},
        {'name':'ligature soft hyphen and line wrap normalization','passed':norm('ﬁxed non\u00adnegative prime-\nfield')==norm('fixed nonnegative primefield')}]
    need(all(x['passed'] for x in cs),'Search positive controls')
    return cs
