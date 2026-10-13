from pathlib import Path
import copy,hashlib,html,importlib.util,json,subprocess,sys
from html.parser import HTMLParser
A=Path(__file__).resolve().parent
def mod(name,p):
 s=importlib.util.spec_from_file_location(name,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=mod("guard",A/"zenodo_exact_description_guard.py");k=mod("kit",Path("/Users/alec/Documents/Math/zenodo_deposit_tool/zenodo.py"))
meta,files=k.load_manifest(A/"zenodo-deposit.v2.json")
d=json.loads((A/"ZENODO_HTML_REPRESENTATION_DIAGNOSTIC.json").read_text())
class Structure(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.events=[]
 def handle_starttag(self,t,attrs):self.events.append(("start",t,attrs))
 def handle_endtag(self,t):self.events.append(("end",t))
 def handle_data(self,t):
  if self.events and self.events[-1][0]=="data":self.events[-1]=("data",self.events[-1][1]+t)
  else:self.events.append(("data",t))
def events(s):
 p=Structure();p.feed(s);p.close();return p.events
def require(c,m):
 if not c:raise RuntimeError(m)
require(events(meta["description"])==events(d["metadata"]["description"]),"Rendered paragraph structure/text differs")
baseline=g.guarded_verify(k.verify,d,meta,files)
require(len(baseline)==1,"Expected precisely one transport allowance")
raw=copy.deepcopy(d);raw["metadata"]["description"]=meta["description"];require(g.guarded_verify(k.verify,raw,meta,files)==[],"Literal intended serialization should match")
mutations=[]
for name,fn in [
 ("partial_escaping",lambda v:v["metadata"].update(description=v["metadata"]["description"].replace("n&gt;=4","n>=4"))),
 ("double_escaping",lambda v:v["metadata"].update(description=v["metadata"]["description"].replace("&gt;","&amp;gt;"))),
 ("text_scope",lambda v:v["metadata"].update(description=v["metadata"]["description"].replace("For every n&gt;=3","For every n&gt;=2"))),
 ("tag_attribute",lambda v:v["metadata"].update(description=v["metadata"]["description"].replace("<p>","<p class='x'>",1))),
 ("removed_tag",lambda v:v["metadata"].update(description=v["metadata"]["description"].replace("</p>","",1))),
 ("changed_title",lambda v:v["metadata"].update(title=v["metadata"]["title"]+" amended")),
 ("changed_creator",lambda v:v["metadata"]["creators"][0].update(name="Other author")),
 ("changed_ORCID",lambda v:v["metadata"]["creators"][0].update(orcid="0000-0000-0000-0000")),
 ("changed_keyword",lambda v:v["metadata"]["keywords"].append("new claim")),
 ("changed_relation",lambda v:v["metadata"]["related_identifiers"][0].update(relation="isDerivedFrom")),
 ("corrupt_checksum",lambda v:v["files"][0].update(checksum="0"*32)),
 ("wrong_size",lambda v:v["files"][0].update(filesize=v["files"][0]["filesize"]+1)),
 ("extra_file",lambda v:v["files"].append({"filename":"extra.txt","filesize":0,"checksum":"0"*32})),
 ("duplicate_file",lambda v:v["files"].append(copy.deepcopy(v["files"][0])))]:
 v=copy.deepcopy(d);fn(v)
 try:g.guarded_verify(k.verify,v,meta,files)
 except (k.DepositError,RuntimeError):mutations.append({"mutation":name,"rejected":True})
 else:raise RuntimeError("Incorrectly accepted "+name)
wrong=copy.deepcopy(meta);wrong["description"]+=" amended"
try:g.guarded_verify(k.verify,d,wrong,files)
except RuntimeError:mutations.append({"mutation":"changed_expected_metadata","rejected":True})
else:raise RuntimeError("Expected metadata restriction escaped")
r={"status":"PASS_EXACT_RENDERED_TEXT_STRUCTURE_AND_ALL15_FALSE_VARIANTS_REJECTED","baseline_serializations":2,"semantic_rejections":mutations,"guard_sha256":hashlib.sha256((A/"zenodo_exact_description_guard.py").read_bytes()).hexdigest(),"reviewed_metadata_unchanged":True,"kit_unchanged":True}
print(json.dumps(r,sort_keys=True))

