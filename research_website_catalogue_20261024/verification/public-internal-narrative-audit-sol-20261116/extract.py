"""Read only the indexed public HTML; write an audit corpus beside this script."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import hashlib
import json

W = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com')
OUT = Path(__file__).resolve().parent

class Node:
    def __init__(self, tag='', attrs=(), line=0):
        self.tag, self.attrs, self.line, self.children = tag, dict(attrs), line, []
    def descendants(self, tag=None):
        for child in self.children:
            if isinstance(child, Node):
                if tag is None or child.tag == tag:
                    yield child
                yield from child.descendants(tag)
    def text(self):
        if self.tag in ('script', 'style'):
            return ''
        return ' '.join(' '.join(c.text() if isinstance(c, Node) else c for c in self.children).split())
    def rawtext(self):
        return ''.join(c.rawtext() if isinstance(c, Node) else c for c in self.children)

class Parser(HTMLParser):
    void = {'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
    def __init__(self, html):
        super().__init__(convert_charrefs=True)
        self.root = Node()
        self.stack = [self.root]
        self.feed(html)
        self.close()
    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.getpos()[0])
        self.stack[-1].children.append(node)
        if tag not in self.void:
            self.stack.append(node)
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.void:
            self.handle_endtag(tag)
    def handle_endtag(self, tag):
        for i in range(len(self.stack)-1, 0, -1):
            if self.stack[i].tag == tag:
                self.stack = self.stack[:i]
                break
    def handle_data(self, data):
        self.stack[-1].children.append(data)

index_path = W / 'public/research/index.html'
index_bytes = index_path.read_bytes()
index = Parser(index_bytes.decode()).root
collections = [json.loads(s.rawtext()) for s in index.descendants('script') if s.attrs.get('type') == 'application/ld+json']
lists = [j['mainEntity'] for j in collections if isinstance(j, dict) and isinstance(j.get('mainEntity'), dict) and j['mainEntity'].get('@type') == 'ItemList']
assert len(lists) == 1
items = lists[0]['itemListElement']
assert len(items) == lists[0]['numberOfItems'] == 107
urls = [item['url'] for item in items]
assert len(set(urls)) == 107
visible = {a.attrs.get('href') for li in index.descendants('li') for a in li.descendants('a')}
assert all(url in visible or urlsplit(url).path in visible for url in urls)

articles = []
for position, item in enumerate(items, 1):
    path = W / 'public' / urlsplit(item['url']).path.lstrip('/') / 'index.html'
    assert path.resolve().is_relative_to(W / 'public/research')
    data = path.read_bytes()
    dom = Parser(data.decode()).root
    article_nodes = list(dom.descendants('article'))
    assert len(article_nodes) == 1, str(path)
    article = article_nodes[0]
    sections = []
    for section in article.descendants('section'):
        headings = [h for h in section.descendants() if h.tag in ('h2','h3','h4')]
        blocks = []
        for b in section.descendants():
            if b.tag in ('p','li','figcaption','summary','pre','tr'):
                blocks.append({'tag':b.tag,'id':b.attrs.get('id'),'line':b.line,'text':b.text()})
        sections.append({'id':section.attrs.get('id'),'aria_labelledby':section.attrs.get('aria-labelledby'),'line':section.line,'headings':[{'id':h.attrs.get('id'),'tag':h.tag,'text':h.text(),'line':h.line} for h in headings],'blocks':blocks,'text':section.text()})
    header_nodes = [c for c in article.children if isinstance(c,Node) and c.tag=='header']
    outside = [c.text() for c in article.children if isinstance(c,Node) and c.tag not in ('section','script','style')]
    headings, article_blocks, current_heading = [], [], None
    for node in article.descendants():
        if node.tag in ('h2','h3','h4'):
            current_heading = {'id':node.attrs.get('id'),'tag':node.tag,'text':node.text(),'line':node.line}
            headings.append(current_heading)
        elif node.tag in ('p','li','figcaption','summary','pre','tr'):
            article_blocks.append({'heading':current_heading,'tag':node.tag,'id':node.attrs.get('id'),'line':node.line,'text':node.text()})
    articles.append({'position':position,'url':item['url'],'name':item['name'],'path':str(path),'bytes':len(data),'SHA256':hashlib.sha256(data).hexdigest(),'header': ' '.join(h.text() for h in header_nodes),'outside_sections':outside,'headings':headings,'article_blocks':article_blocks,'sections':sections})

result = {'schema':'bounded-public-copy-corpus-v1','W_root':str(W),'scope':'107 actual index-listed article HTML files; no asset or science-body reading','index':{'path':str(index_path),'bytes':len(index_bytes),'SHA256':hashlib.sha256(index_bytes).hexdigest()},'articles':articles}
(OUT / 'CORPUS.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'articles':len(articles),'sections':sum(len(a['sections']) for a in articles),'blocks':sum(len(s['blocks']) for a in articles for s in a['sections']),'index_SHA256':result['index']['SHA256'],'corpus_bytes':(OUT/'CORPUS.json').stat().st_size}))
