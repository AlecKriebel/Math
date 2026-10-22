from pathlib import Path
import sys,json,hashlib,importlib.util,copy,tempfile,types,datetime
R=Path("/Users/alec/Documents/Math");D=R/"draft_pr_claimed_solved_700_800_20261012";T=D/"audits/pr786_30001223/tmp";P=T/"preprint";M=T/"root-receipts"
sys.path.insert(0,str(R/"zenodo_deposit_tool"));import zenodo as z
adapter=T/"production_metadata_adapter.py";pin="1961db795e823a5a9149c733d7f7f68ea8f5f86bdc02a0475f98f13dace1da8e"
if hashlib.sha256(adapter.read_bytes()).hexdigest()!=pin:raise RuntimeError("Adapter changed before root read/execute")
spec=importlib.util.spec_from_file_location("pr786_metadata_adapter",adapter);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
metadata,files=z.load_manifest(P/"zenodo-deposit.json");base=z.verify
def fresh_tool():return types.SimpleNamespace(__file__=z.__file__,verify=base,DepositError=z.DepositError)
tool=fresh_tool();installed=module.install(tool,P/"zenodo-metadata.json")
deposit={"id":23418581,"metadata":copy.deepcopy(metadata),"files":[{"filename":f["name"],"filesize":f["size"],"checksum":f["md5"]}for f in files]}
desc=metadata["description"];escaped=desc.replace("n>=2","n&gt;=2");rows=[]
def run(name,remote,expected_metadata=metadata,expected_files=files,ok=False):
 before=copy.deepcopy(remote)
 try:response=tool.verify(remote,expected_metadata,expected_files);passed=True;reason=None
 except Exception as e:response=None;passed=False;reason=type(e).__name__+": "+str(e)
 if passed!=ok:raise RuntimeError("Incorrect result "+name+" "+str(reason))
 if remote!=before:raise RuntimeError("Verifier mutated input")
 rows.append({"case":name,"expected":"PASS"if ok else"REJECT","outcome":"PASS"if passed else"REJECT","reason":reason,"normalizations":response,"input_response_unchanged":True})
run("exact_raw",copy.deepcopy(deposit),ok=True)
encoded=copy.deepcopy(deposit);encoded["metadata"]["description"]=escaped
run("single_observed_entity",copy.deepcopy(encoded),ok=True)
for key in metadata:
 if key=="description":continue
 bad=copy.deepcopy(encoded);bad["metadata"][key]=None
 run("changed_remote_"+key,bad)
for name,description in [
 ("wrong_inequality",desc.replace("n>=2","n&lt;=2")),
 ("double_encoding",escaped.replace("&gt;","&amp;gt;")),
 ("drop_equal",escaped.replace("&gt;=2","&gt;2")),
 ("change_bound",escaped.replace("&gt;=2","&gt;=3")),
 ("add_priority",escaped+"<p>This is a first solution.</p>"),
 ("remove_disclosure",escaped.replace("unrefereed","refereed")),
 ("drop_paragraph_tags",escaped.replace("<p>","").replace("</p>","")),
 ("change_root_parameter",escaped.replace("q=1","q=2")),
 ("entity_in_other_locus",escaped.replace("p=3","p&#61;3")),
 ("different_whitespace",escaped+" "),
 ("missing_description",None)]:
 bad=copy.deepcopy(encoded);bad["metadata"]["description"]=description;run(name,bad)
for name,value in [("wrong_id",23418582),("boolean_id",True),("missing_id",None)]:
 bad=copy.deepcopy(encoded);bad["id"]=value;run(name,bad)
for name in ["missing_file","extra_file","changed_size","changed_checksum","duplicate_file"]:
 bad=copy.deepcopy(encoded)
 if name=="missing_file":bad["files"].pop()
 elif name=="extra_file":bad["files"].append({"filename":"extra","filesize":1,"checksum":"0"*32})
 elif name=="changed_size":bad["files"][0]["filesize"]+=1
 elif name=="changed_checksum":bad["files"][0]["checksum"]="0"*32
 else:bad["files"].append(copy.deepcopy(bad["files"][0]))
 run(name,bad)
for key in ["title","description","creators"]:
 altered=copy.deepcopy(metadata);altered[key]=None;bad=copy.deepcopy(encoded);bad["metadata"][key]=None
 run("changed_frozen_expected_"+key,bad,altered)
with tempfile.TemporaryDirectory(prefix="adapter-root-",dir=T)as folder:
 scratch=Path(folder);wrong=scratch/"metadata.json";wrong.write_bytes((P/"zenodo-metadata.json").read_bytes()+b"\n")
 for name,subject,where in [
  ("wrong_metadata_pin",fresh_tool(),wrong),
  ("wrong_tool_pin",types.SimpleNamespace(__file__=str(wrong),verify=base,DepositError=z.DepositError),P/"zenodo-metadata.json"),
  ("replaced_original_verifier",types.SimpleNamespace(__file__=z.__file__,verify=lambda *x:[],DepositError=z.DepositError),P/"zenodo-metadata.json")]:
  try:module.install(subject,where)
  except Exception as e:rows.append({"case":name,"expected":"REJECT","outcome":"REJECT","reason":type(e).__name__+": "+str(e)})
  else:raise RuntimeError("Bad installation accepted:"+name)
print(json.dumps({"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"result":"PASS","runtime":sys.version,"optimized":sys.flags.optimize,"adapter_sha256":pin,"installed":installed,"positive_cases":sum(r["expected"]=="PASS"for r in rows),"negative_cases":sum(r["expected"]=="REJECT"for r in rows),"cases":rows,"network_actions":0,"reviewed_six_files_changed":False},indent=2))
