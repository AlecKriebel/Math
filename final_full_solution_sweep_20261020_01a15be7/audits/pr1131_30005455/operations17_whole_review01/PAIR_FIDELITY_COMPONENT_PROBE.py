from pathlib import Path
import json,hashlib,http.client,types,datetime,socket,urllib.request,subprocess,os
D=Path(__file__).resolve().parent
p=D.parents[3]/'zenodo_deposit_tool/zenodo.py'
b=p.read_bytes()
if hashlib.sha256(b).hexdigest()!='a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca':raise RuntimeError('SDK anchor')
attempts=[]
def deny(*a,**k):attempts.append('unexpected external adapter');raise RuntimeError('No real provider/process')
socket.socket=socket.create_connection=socket.getaddrinfo=deny
urllib.request.urlopen=urllib.request.OpenerDirector.open=deny
subprocess.Popen=subprocess.run=deny;os.system=os.popen=deny
n={'__file__':str(p),'__name__':'actual_checked_SDK_no_main'}
exec(compile(b,str(p),'exec',dont_inherit=True,optimize=0),n)
raw=b'{"id":777,"submitted":false,"title":"literal pair '+bytes.fromhex('eda0bdedb880')+b'"}'
exchanges=[]
class Transport:
 def __init__(self,*a,**k):pass
 def putrequest(self,method,target):exchanges.append([method,target])
 def putheader(self,key,value):
  if key=='Authorization'and value!='Bearer OFFLINE_SENTINEL_NO_CREDENTIAL':raise RuntimeError('Not inert token')
 def endheaders(self):pass
 def send(self,data):pass
 def getresponse(self):return types.SimpleNamespace(status=200,read=lambda maximum:raw)
 def close(self):pass
http.client.HTTPSConnection=Transport
value=n['ZenodoClient']('production','OFFLINE_SENTINEL_NO_CREDENTIAL').create({'title':'inert'})
encoded=(json.dumps({'response':value},sort_keys=True,ensure_ascii=True,indent=2)+'\n').encode('ascii')
replayed=json.loads(encoded)['response']
out={'at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_unchanged_SDK_parser_admitted_complete_original':True,'SDK_sha256':hashlib.sha256(b).hexdigest(),'wire_hex':raw.hex(),'input_title_codepoints':[ord(c)for c in value['title']],'ASCII_receipt_reloaded_title_codepoints':[ord(c)for c in replayed['title']],'typed_string_content_preserved':value['title']==replayed['title'],'distinct_Python_parser_strings_share_one_ASCII_JSON':json.dumps(value,sort_keys=True,ensure_ascii=True)==json.dumps(replayed,sort_keys=True,ensure_ascii=True),'inert_exchanges':exchanges,'actual_effects':0,'actor_world_yet_exercised':False,'network_attempts':attempts}
(D/'private/PAIR_FIDELITY_COMPONENT_PROBE.json').write_text(json.dumps(out,ensure_ascii=True,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=True))
