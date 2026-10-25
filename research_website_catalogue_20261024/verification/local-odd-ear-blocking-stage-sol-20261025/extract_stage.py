"""Extract all actual public body words; check the ten-file partial overlay."""
import sys
sys.dont_write_bytecode=True
from pathlib import Path
from html.parser import HTMLParser
import datetime,hashlib,json,re
O=Path(__file__).resolve().parent;P=O.parents[1];L=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
sys.path[:0]=[str(O),str(P/'scripts')]
from oeb_body_contract import BodyText,expected_body
def need(x,tag):
    if not x:raise RuntimeError('extract_stage:'+tag)
class Readable(HTMLParser):
    def __init__(self,s):
        super().__init__(convert_charrefs=True);self.body=False;self.skip=0;self.parts=[];self.feed(s)
    def handle_starttag(self,t,a):
        if t=='body':self.body=True
        if self.body and t in ('script','style'):self.skip+=1
        if self.body and not self.skip:self.parts.append('\n\n' if t=='br' else ' ')
    def handle_endtag(self,t):
        if t in ('script','style') and self.skip:self.skip-=1;return
        if self.body and not self.skip:self.parts.append('\n\n' if t in ('p','h1','h2','li') else ' ')
        if t=='body':self.body=False
    def handle_data(self,s):
        if self.body and not self.skip:self.parts.append(s)
    def output(self):
        return '\n\n'.join(' '.join(p.split()) for p in ''.join(self.parts).split('\n\n') if p.strip())+'\n'
frozen=json.loads((O/'FROZEN_INPUT_SET.json').read_text());records=[];expected_files={'research/index.html','research/sitemap.xml'}
for rid in frozen['authorized_new_record_ids']:
    B=P/'papers'/rid;c=json.loads((B/'publication.json').read_text());folder=O/'public/research'/c['slug'];h=(folder/'index.html').read_text();body=BodyText(h);text=Readable(h).output()
    need(' '.join(text.split())==body.text==expected_body(c),'entire_approved_body:'+rid)
    (O/f'public-copy-{rid}.txt').write_text(text)
    sections={}
    for name in ('abstract','plain-language','result','proof','limits','status','paper','materials','collaborate','cite','background'):
        segment=re.search('<section id="'+name+'">(.*?)</section>',h,re.S).group(1)
        sections[name]=Readable('<body>'+segment+'</body>').output().strip()
    (O/f'public-sections-{rid}.json').write_text(json.dumps(sections,ensure_ascii=False,indent=2)+'\n')
    names={'index.html','citation.bib',c['pdf_filename'],c['supplement_filename']}
    need({p.name for p in folder.iterdir() if p.is_file()}==names,'exact_four_files')
    for name in (c['pdf_filename'],c['supplement_filename']):need((folder/name).read_bytes()==(B/'sources'/name).read_bytes(),'literal_original_asset')
    need((folder/'citation.bib').read_text()==c['prepared_bibtex'],'literal_prepared_BibTeX')
    expected_files|={'research/'+c['slug']+'/'+n for n in names}
    records.append({'record_id':rid,'article_files':sorted(names),'whole_approved_body_equal':True,'PDF_ZIP_literal_bytes_equal_to_originals':True,'prepared_BibTeX_literal_equal':True,'actual_visible_body_sha256':hashlib.sha256(text.encode()).hexdigest()})
actual=sorted(str(p.relative_to(O/'public')) for p in (O/'public').rglob('*') if p.is_file());need(set(actual)==expected_files and len(actual)==10,'exact_overlay_files')
oldindex=(L/'research/index.html').read_text();newindex=(O/'public/research/index.html').read_text();olditems=re.findall(r'<li>.*?</li>',oldindex,re.S);newitems=re.findall(r'<li>.*?</li>',newindex,re.S)
need(len(olditems)==68 and len(newitems)==70 and newitems[:68]==olditems,'old_visible_entries_byteidentical')
olddata=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',oldindex,re.S).group(1));newdata=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',newindex,re.S).group(1))
need(newdata['mainEntity']['itemListElement'][:68]==olddata['mainEntity']['itemListElement'] and newdata['mainEntity']['numberOfItems']==70,'old_JSONLD_entries_unchanged')
urls=re.findall(r'<loc>(.*?)</loc>',(O/'public/research/sitemap.xml').read_text());need(urls[:69]==frozen['baseline_sitemap_URLs_in_order'] and len(urls)==71,'sitemap_prefix_unchanged')
receipt={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','actual_files':actual,'overlay_files':10,'records':records,'existing68_visible_index_entries_byteidentical':True,'existing68_JSONLD_entries_unchanged':True,'index_items':70,'existing69_sitemap_URLs_unchanged_in_order':True,'sitemap_URLs':71,'predicted_integrated_public_files':524,'no_old_output_or_fixture_tree_copied':True}
(O/'OVERLAY_CHECKS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k not in ('records','actual_files')}))
