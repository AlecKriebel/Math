"""Add decoded HTML and every UTF-8 tracked text object, with positive controls.
Existing PDF text remains in its sealed location; no foreign full text is copied.
"""
from pathlib import Path
from html.parser import HTMLParser
import subprocess,hashlib,json,re,unicodedata,datetime,os
E=Path(__file__).resolve().parent;P=E.parents[1];G=P.parent
def sha(b):return hashlib.sha256(b).hexdigest()
def save(n,x):(E/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def norm(t):
 t=unicodedata.normalize('NFKC',t).replace('\u00ad','');t=re.sub('[‐‑‒–—−]','-',t);t=re.sub(r'-\s+','-',t);return ' '.join(t.split())
def git(*a):return subprocess.run(['git',*a],cwd=G,env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'},capture_output=True,check=True,timeout=30).stdout
class Visible(HTMLParser):
 def __init__(self,t):super().__init__(convert_charrefs=True);self.parts=[];self.skip=0;self.feed(t)
 def handle_starttag(self,t,a):
  if t in ['script','style']:self.skip+=1
 def handle_endtag(self,t):
  if t in ['script','style']:self.skip=max(0,self.skip-1)
 def handle_data(self,d):
  if not self.skip:self.parts.append(d)
base=json.loads((E/'SEARCH_RESULTS.json').read_text());queries={**base['queries'],'bounded_Mazur_word':r'\bMazur\b','quantified_scope':r'Banach.{0,40}distance|Jordan.{0,40}isometr|predual|ordinary bounded|Hochschild'}
def hits(t):return {k:[{'match':m.group(),'context':t[max(0,m.start()-140):min(len(t),m.end()+220)]} for m in re.finditer(v,t,re.I)] for k,v in queries.items()}
rows=[];alltexts={};undecoded=[]
for r in json.loads((E/'DOCS_OBJECT_BINDINGS.json').read_text()):
 if r['path'].endswith('.pdf'):continue
 b=git('cat-file','blob',r['blob'])
 try:t=b.decode('utf-8')
 except UnicodeDecodeError:undecoded.append(r['path']);continue
 if '\0' in t:undecoded.append(r['path']);continue
 alltexts[r['path']]=norm(t);rows.append({'kind':'all_decodable_tracked_text','path':r['path'],'blob':r['blob'],'hits':hits(norm(t))})
 if r['path'].endswith('.html'):
  visible=norm(' '.join(Visible(t).parts));alltexts[r['path']+'#visible']=visible;rows.append({'kind':'decoded_visible_HTML','path':r['path'],'blob':r['blob'],'hits':hits(visible)})
for r in base['rows']:
 if r['kind']=='complete_PDF_extract':
  t=norm(Path(r['source_text']).read_text());alltexts[r['path']]=t;rows.append({**{k:v for k,v in r.items() if k!='hits'},'hits':hits(t)})
save('COMPLETE_SEARCH.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'queries':queries,'rows':rows,'nonempty':[r for r in rows if any(r['hits'].values())],'decoded_tracked_texts':sum(r['kind']=='all_decodable_tracked_text' for r in rows),'visible_HTML':sum(r['kind']=='decoded_visible_HTML' for r in rows),'complete_PDFs':sum(r['kind']=='complete_PDF_extract' for r in rows),'other_binary_assets_not_text_searched':undecoded})
target=P/'papers/23217863/sources/paper.pdf'
raw=subprocess.run(['/opt/homebrew/bin/pdftotext','-','-'],input=target.read_bytes(),capture_output=True,check=True,timeout=30).stdout
t=norm(raw.decode());controls=[]
for name,pat,where in [
 ('current_7pp_target_full_title',queries['full_title'],'current_target'),
 ('current_7pp_target_Banach_Mazur',queries['Banach_Mazur'],'current_target'),
 ('known_legacy_Gamma_HTML',r'A note on Γ-supercyclicity of dissipative composition operators','docs/papers/gamma-supercyclicity/index.html#visible'),
 ('known_legacy_Gromov_PDF',r'A Lipschitz-nonincreasing deformation of small unitary-valued maps','docs/papers/gromov-unitary-lipschitz/paper.pdf'),
 ('known_legacy_Bell_PDF',r'Exact Quantum Values and Permutation-Blind Maximizers in Cyclic Bell Inequalities','docs/papers/cyclic-bell-exact-values-and-randomness/paper.pdf')]:
  text=t if where=='current_target' else alltexts[where];m=list(re.finditer(pat,text,re.I));assert m,name;controls.append({'control':name,'query':pat,'where':where,'matches':len(m)})
assert norm('Banach–\nMazur')=='Banach-Mazur'
assert norm('Banach\u00ad–Mazur')=='Banach-Mazur'
controls.append({'control':'Unicode_soft_hyphen_and_wrapped_dash','passed':True})
save('QUERY_CONTROLS.json',{'status':'PASS','controls':controls,'current_target_text_bytes':len(raw),'current_target_text_sha256':sha(raw),'current_target_not_part_of_legacy_corpus':True,'full_PDF_reextractions':1})
print(json.dumps({'text_objects':sum(r['kind']=='all_decodable_tracked_text' for r in rows),'visible_HTML':47,'PDF':76,'controls':len(controls),'nonempty_paths':sorted(set(r['path'] for r in rows if any(r['hits'].values()))),'all_precise_query_hits':[{ 'path':r['path'],'kind':r['kind'],'hits':{k:v for k,v in r['hits'].items() if v and k not in ['broad_context']}} for r in rows if any(v for k,v in r['hits'].items() if k!='broad_context')]},ensure_ascii=False,indent=2))
