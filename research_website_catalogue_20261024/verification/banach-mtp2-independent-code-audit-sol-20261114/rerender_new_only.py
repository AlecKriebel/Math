#!/usr/bin/env python3
"""Reproduce only the two new articles in this audit's private directory.
No old article fixtures or old content campaigns; guard every output boundary.
"""
from pathlib import Path
import builtins,contextlib,hashlib,io,json,sys
sys.dont_write_bytecode=True
A=Path(__file__).resolve().parent;P=A.parents[1]
E=P/'verification/local-banach-mtp2-stage-sol-20261025/resume'
LIVE=Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
sys.path[:0]=[str(E),str(P/'scripts')]
H=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
if len(sys.argv)!=1:raise RuntimeError('No arguments accepted')
site=A/'new-only-render/public/research';site.mkdir(parents=True,exist_ok=True)
for name in ['index.html','sitemap.xml']:(site/name).write_bytes((LIVE/'research'/name).read_bytes())
original=(E/'render_page.proposed.py').read_text()
source=original.replace('ROOT = Path(__file__).resolve().parents[1]',f'ROOT = Path({str(P)!r})').replace("SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public/research')",f'SITE = Path({str(site)!r})')
if source==original or source.count(f'SITE = Path({str(site)!r})')!=1:raise RuntimeError('Renderer redirection failed')
op=builtins.open;iop=io.open;mk=Path.mkdir
def guard(p):
 if not Path(p).resolve().is_relative_to(A):raise RuntimeError('Refused write outside own audit: '+str(p))
def guarded_open(file,mode='r',*a,**kw):
 if any(c in mode for c in 'wax+') and isinstance(file,(str,bytes,Path)):guard(file)
 return op(file,mode,*a,**kw)
def guarded_mkdir(p,*a,**kw):guard(p);return mk(p,*a,**kw)
rows=[]
stageindex=(E/'public/research/index.html').read_text()
records=['23217863','23146753']
records.sort(key=lambda rid:stageindex.index('href="/research/'+json.loads((P/'papers'/rid/'publication.json').read_text())['slug']+'/"'))
try:
 builtins.open=io.open=guarded_open;Path.mkdir=guarded_mkdir
 for rid in records:
  sys.argv=[str(E/'render_page.proposed.py'),rid]
  with contextlib.redirect_stdout(io.StringIO()) as buf:exec(compile(source,str(E/'render_page.proposed.py'),'exec'),{'__file__':str(E/'render_page.proposed.py'),'__name__':'__main__'})
  rows.append({'record':rid,'actual_renderer_stdout':json.loads(buf.getvalue())})
finally:builtins.open=op;io.open=iop;Path.mkdir=mk
print(json.dumps({'status':'TWO_NEW_ARTICLES_REPRODUCED_ONLY','code_sha256':H(E/'render_page.proposed.py'),'runs':rows,'output_files':[{'path':str(p.relative_to(A)),'bytes':p.stat().st_size,'sha256':H(p)} for p in sorted((A/'new-only-render').rglob('*')) if p.is_file()],'old69_campaign_repeated':False,'old_article_fixture_trees_created':False},indent=2))
