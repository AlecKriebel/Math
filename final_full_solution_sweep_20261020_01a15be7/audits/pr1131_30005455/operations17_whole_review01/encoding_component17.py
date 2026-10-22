"""All2048 lone surrogate units through pinned SDK parser and physical receipt.
Component evidence only: no phase invocation/provider effect/acceptance claim.
"""
from pathlib import Path
import json,hashlib,http.client,sys
ROOT=Path(__file__).resolve().parent;S=ROOT/'source';saved=ROOT/'private/candidate_inputs16_02'
CANDIDATE=(saved/'SOURCE_MANIFEST.json').read_bytes();read_before=Path.read_bytes
def read_candidate(path):return CANDIDATE if path==S/'SOURCE_MANIFEST.json'and not path.exists()else read_before(path)
Path.read_bytes=read_candidate
engine=ROOT/'ENGINE17.py';text=engine.read_text().replace("DEST=REVIEW/'private'/('final_phase17_'+MODE)","DEST=REVIEW/'private'/('encoding_component17_'+MODE)")
needle='    for p in SOURCE.iterdir():(src/p.name).write_bytes(p.read_bytes())'
if not(S/'SOURCE_MANIFEST.json').exists():text=text.replace(needle,needle+"\n    (src/'SOURCE_MANIFEST.json').write_bytes(CANDIDATE)")
exec(compile(text,str(engine)+'[encoding component candidate MF only]','exec',dont_inherit=True,optimize=0),globals())
SDK_CLIENT=c.zenodo.ZenodoClient;w=setup('all_parser_string_units_component')
strings=[chr(x)for x in range(0xd800,0xe000)]+['ASCII','café Δ','😀','backslash \\ud800','\x00\n\t',chr(0x10ffff),chr(0xffff),chr(0x80)]
supplied={'id':777,'submitted':False,'title':'inert string domain component','strings':strings}
raw=json.dumps(supplied,sort_keys=True,ensure_ascii=True).encode('ascii');exchanges=[]
class Transport:
 def __init__(self,*a,**k):pass
 def putrequest(self,method,target):exchanges.append([method,target])
 def putheader(self,key,value):
  if key=='Authorization':need(value=='Bearer OFFLINE_SENTINEL_NO_CREDENTIAL','Not inert token')
 def endheaders(self):pass
 def send(self,data):pass
 def getresponse(self):return types.SimpleNamespace(status=200,read=lambda maximum:raw)
 def close(self):pass
metadata,_=c.zenodo.load_manifest(pub.MANIFEST)
with model.patch((http.client,'HTTPSConnection',Transport)):parsed=SDK_CLIENT('production','OFFLINE_SENTINEL_NO_CREDENTIAL').create(metadata)
need(m.SHEET_POLICY.typed_equal(parsed,supplied),'SDK string-unit roundtrip')
(w.place/'COMPONENT_ONLY_SDK_RESPONSE_ASCII.json').write_bytes(raw)
(w.place/'COMPONENT_ONLY_PARSED_RESPONSE_ASCII.json').write_text(json.dumps(parsed,ensure_ascii=True,sort_keys=True)+'\n',encoding='ascii')
client=m.EdgeDelegate(w.native,types.SimpleNamespace(deposit_id=777),'stage')
value,path,pin=client.capture('create',parsed,known_fact={'kind':'create','requested_or_known_id':777,'returned_positive_id':777,'manifest':str(pub.MANIFEST),'sources_sha256':MS,'rule':'INERT COMPONENT DATA ONLY; no provider outcome or phase was executed'})
actual=path.read_bytes();expected=(json.dumps(json.loads(actual),sort_keys=True,ensure_ascii=True,indent=2)+'\n').encode('ascii')
need(actual==expected and c.pin(actual)==pin and all(x<128 for x in actual)and m.SHEET_POLICY.typed_equal(value,parsed),'Expected and actual ASCII representation differ')
need(not w.native.calls and not CLI_INVOCATIONS and not model.ATTEMPTS,'Component invoked phase/provider')
v={'case':w.place.name,'status':'PASS_COMPONENT_ONLY','all2048_surrogate_units':True,'string_count':len(strings),'SDK_parser_exchanges':exchanges,'expected_actual_ascii_bytes_identical':True,'full_typed_object_preserved':True,'receipt_pin':pin,'source_manifest_sha256':MS,'bootstrap_sha256':BS,'initial_manifest_virtual':not(S/'SOURCE_MANIFEST.json').exists(),'phase_invocations':0,'provider_effects':0,'actual_effects':0,'publication_ready':False}
(DEST/(w.place.name+'.json')).write_text(json.dumps(v,indent=2)+'\n');(ROOT/'private/ENCODING_COMPONENT_RESULTS.json').write_text(json.dumps(v,indent=2)+'\n');archive_completed();print(json.dumps(v,indent=2))
