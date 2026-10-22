#!/usr/bin/env python3
"""Compile only the exact reviewed account-search function; no service access."""
import ast,copy,hashlib,json
from pathlib import Path
from urllib.parse import urlencode,urlparse
D=Path(__file__).resolve().parent;S=D.parent.parents[1]/'audits/pr0399_30001179/prepublication_check.py'
tree=ast.parse(S.read_text());fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='account_search')
def identity_projection(r):
 if not isinstance(r.get('metadata'),dict) or not isinstance(r.get('files'),list):raise RuntimeError('Unexpected account metadata/full files schema')
 return {'metadata':r['metadata'],'files':r['files']}
ns={'urlencode':urlencode,'urlparse':urlparse,'identity_projection':identity_projection};exec(compile(ast.Module(body=[fn],type_ignores=[]),str(S),'exec'),ns)
class Client:
 base='https://zenodo.org'
 def __init__(self,pages):self.pages=iter(pages);self.calls=[]
 def request(self,method,url):
  if method!='GET':raise RuntimeError('mutation attempt')
  self.calls.append(url);return copy.deepcopy(next(self.pages))
def record(i):return {'id':i,'metadata':{},'files':[]}
def page(rs,total,next=None):return {'hits':{'total':total,'hits':rs},'links':({'next':next} if next else {})}
results=[]
def test(name,pages,accept):
 c=Client(pages)
 try:v=ns['account_search'](c,'');status='accepted';extra={'total':v['total'],'pages':v['pages']}
 except Exception as e:status='blocked';extra={'reason':str(e)}
 results.append({'name':name,'expected':'accepted' if accept else 'blocked','observed':status,'expectation_met':(status=='accepted')==accept,'calls':len(c.calls),**extra})
test('empty_account_terminal',[page([],0)],True)
test('exact_page_count_empty_terminal',[page([record(i) for i in range(1,26)],25,'https://zenodo.org/api/user/records?page=2'),page([],25)],True)
test('dict_total_exact',[page([record(1)],{'value':1,'relation':'eq'})],True)
test('truncated_terminal',[page([record(1)],2)],False)
test('total_changed',[page([record(1)],2,'https://zenodo.org/api/user/records?page=2'),page([record(2)],3)],False)
test('repeated_id',[page([record(1),record(1)],2)],False)
test('foreign_next',[page([record(1)],1,'https://foreign.example/api/user/records')],False)
test('loop_next',[page([record(1)],1,'https://zenodo.org/api/user/records?q=&size=25')],False)
test('inexact_total',[page([record(1)],{'value':1,'relation':'gte'})],False)
test('draft_missing_files',[page([{'id':1,'metadata':{}}],1)],False)
(D/'ACCOUNT_READER_CONTROL_RESULTS.json').write_text(json.dumps({'source_sha256':hashlib.sha256(S.read_bytes()).hexdigest(),'controls':results},indent=2)+'\n');print(json.dumps(results,indent=2))
