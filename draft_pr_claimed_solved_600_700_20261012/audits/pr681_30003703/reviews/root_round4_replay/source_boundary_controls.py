#!/usr/bin/env python3
"""New low-level response/secret/environment probes; fake transports only."""
import hashlib,http.client,io,json,sys,types
from pathlib import Path
R=Path(__file__).absolute().parent;A=R.parent.parent;K=A.parents[2]/'zenodo_deposit_tool/zenodo.py'
source=K.read_bytes();k=types.ModuleType('round4_captured_exact_kit');k.__file__=str(K)
exec(compile(source,str(K),'exec'),k.__dict__)
results=[];wire=[];status=200;body=b'{"ok":true}';TOKEN='FAKE_ONLY_TOKEN_681'
def need(c,m):
 if not c:raise RuntimeError(m)
def check(n,f):f();results.append({'name':n,'status':'PASS'})
def reject(n,f,redacted=False):
 try:f()
 except k.DepositError as exc:
  if redacted:need(TOKEN not in str(exc),'fake secret leaked')
  results.append({'name':n,'status':'REJECTED','error':str(exc)});return
 raise RuntimeError('accepted '+n)
class Conn:
 def __init__(self,host,timeout):need(host=='zenodo.org','host');wire.append(['connection',host]);self.headers={}
 def putrequest(self,method,path):wire.append([method,path])
 def putheader(self,n,v):self.headers[n]=v
 def endheaders(self):need(self.headers['Authorization']=='Bearer '+TOKEN,'auth')
 def send(self,b):wire.append(['send',len(b)])
 def getresponse(self):return types.SimpleNamespace(status=status,read=lambda n:body)
 def close(self):pass
k.http=types.SimpleNamespace(client=types.SimpleNamespace(HTTPSConnection=Conn,HTTPException=http.client.HTTPException));c=k.ZenodoClient('production',TOKEN)
for i,(s,b)in enumerate([(200,b'null'),(200,b'[]'),(200,b'{}'),(200,b'not JSON'),(200,b'\xff'),(200,b'x'*(k.MAX_RESPONSE_BYTES+1)),(302,b'{"message":"redirect"}'),(429,b'{"message":"wait"}'),(403,b'<html>unusual traffic</html>'),(400,json.dumps({'message':TOKEN,'errors':[TOKEN]}).encode())]):
 status,body=s,b;reject('invalid_or_unconfirmed_HTTP_response_'+str(i),lambda:c.request('GET','https://zenodo.org/api/fake'),True)
status,body=200,b'{"ok":true}'
check('exact_valid_JSON_object_transport',lambda:need(c.request('GET','https://zenodo.org/api/fake')=={'ok':True},'positive'))
for url in ['https://zenodo.org.evil.invalid/x','https://zenodo.org@evil.invalid/x','https://name:password@zenodo.org/x','https://zenodo.org:444/x','http://zenodo.org/x','https://sandbox.zenodo.org/x']:
 before=len(wire);reject('API_URL_boundary_'+url,lambda:c.request('POST',url,{}));need(len(wire)==before,'bad URL constructed connection')
# DOI resolution redirects are public and have no API token. HTTPS plus no
# userinfo is enforced by the exact redirect handler before following a target.
handler=k.PublicDOIRedirects();request=k.Request('https://doi.org/10.5281/zenodo.999999991',method='HEAD')
for url in ['http://evil.invalid/x','https://user@zenodo.org/x','https://user:pw@zenodo.org/x']:
 try:handler.redirect_request(request,None,302,'',{},url)
 except k.HTTPError:results.append({'name':'unsafe_public_DOI_redirect_'+url,'status':'REJECTED'})
 else:raise RuntimeError('unsafe redirect accepted')
# Selected action state validates bool exactly and exact deposition integer.
for bad in [{'id':999999991,'submitted':1},{'id':True,'submitted':False},{'id':'999999991','submitted':False},{'id':999999992,'submitted':False}]:reject('record_state_identity_'+str(bad),lambda:k.validate_record(bad,999999991))
print(json.dumps({'schema':'pr681-round4-source-boundaries-v1','status':'PASS','mode':'optimized'if sys.flags.optimize else'normal','count':len(results),'controls':results,'source_sha256':hashlib.sha256(source).hexdigest(),'real_token_lookups_HTTP_Git_GWS_or_external_mutations':0,'wire':wire},indent=2,sort_keys=True))
