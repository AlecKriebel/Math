"""Offline PR786 production-adapter regression; never call external APIs/state/auth."""
from pathlib import Path
import argparse,copy,hashlib,html,importlib.util,json,sys,tempfile,types
APIN="1961db795e823a5a9149c733d7f7f68ea8f5f86bdc02a0475f98f13dace1da8e"
ZPIN="a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca"
MPIN="309a2dd51cee7be8d35bef49659c26818ed2e7f40ec78d639f2c83fa227ec3c5"
ID=23418581
def need(c,m):
    if not c:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def canonical(x):return json.dumps(x,sort_keys=True,separators=(",",":"),default=str).encode()
def load_pinned(path,name,pin):
    need(sha(path.read_bytes())==pin,"Code pin mismatch before import")
    spec=importlib.util.spec_from_file_location(name,path);module=importlib.util.module_from_spec(spec)
    sys.modules[name]=module;spec.loader.exec_module(module);return module
def deny(*a,**k):raise RuntimeError("NETWORK_AUTH_STATE_ACTION_FORBIDDEN")
def main():
    a=argparse.ArgumentParser();a.add_argument("--adapter",required=True,type=Path)
    a.add_argument("--tool",required=True,type=Path);a.add_argument("--frozen",required=True,type=Path)
    a.add_argument("--scratch",required=True,type=Path);x=a.parse_args()
    z=load_pinned(x.tool,"zenodo",ZPIN);adapter=load_pinned(x.adapter,"pr786_production_adapter",APIN)
    need(sha((x.frozen/"zenodo-metadata.json").read_bytes())==MPIN,"Frozen metadata pin")
    metadata,files=z.load_manifest(x.frozen/"zenodo-deposit.json")
    need(metadata==json.loads((x.frozen/"zenodo-metadata.json").read_text())["metadata"],"Manifest metadata differs")
    # All forbidden integration surfaces are disabled before adapter installation.
    for name in ("token_for","local_state","save_state","ZenodoClient","build_opener"):
        setattr(z,name,deny)
    original=z.verify;fixture={"id":ID,"submitted":False,"metadata":copy.deepcopy(metadata),
        "files":[{"filename":f["name"],"filesize":f["size"],"checksum":"md5:"+f["md5"]} for f in files]}
    before_input=canonical({"metadata":metadata,"fixture":fixture})
    need(original(fixture,metadata,files)==[],"Original exact baseline failed")
    escaped=copy.deepcopy(fixture);escaped["metadata"]["description"]=metadata["description"].replace("n>=2","n&gt;=2")
    try:original(escaped,metadata,files)
    except z.DepositError:pass
    else:raise ValueError("Original unexpectedly accepts observed exception")
    installation=adapter.install(z,x.frozen/"zenodo-metadata.json")
    cases=[]
    def probe(name,deposit,local=None,expected=True):
        local=metadata if local is None else local
        before=canonical({"deposit":deposit,"metadata":local,"files":files})
        try:
            result=z.verify(deposit,local,files);accepted=True;error=None
        except Exception as e:result=None;accepted=False;error=type(e).__name__+": "+str(e)
        need(canonical({"deposit":deposit,"metadata":local,"files":files})==before,"Input mutated:"+name)
        need(accepted is expected,"Wrong acceptance:"+name+" "+str(error))
        cases.append({"case":name,"accepted":accepted,"input_unchanged":True,
                      "normalizations":result,"error":error})
        return result
    need(probe("exact_frozen_description",copy.deepcopy(fixture))==[],"Spurious exact normalization")
    changes=probe("single_observed_html_entity",copy.deepcopy(escaped))
    need(len(changes)==1 and changes[0]["draft_id"]==ID
         and changes[0]["metadata_sha256"]==MPIN
         and changes[0]["visible_text_unchanged"] is True,"Normalization receipt wrong")
    need(html.unescape(escaped["metadata"]["description"])==metadata["description"],"Visible text differs")
    # Retain original file representation conventions, without any new relaxation.
    aliases=copy.deepcopy(escaped)
    for item in aliases["files"]:
        item["key"]=item.pop("filename");item["size"]=str(item.pop("filesize"))
        item["checksum"]=item["checksum"].upper()
    probe("existing_tool_file_alias_conventions",aliases)
    for value in (ID+1,0,-1,str(ID),float(ID),True,None):
        d=copy.deepcopy(escaped);d["id"]=value;probe("different_id_"+repr(value),d,expected=False)
    d=copy.deepcopy(escaped);d.pop("id");probe("missing_id",d,expected=False)
    for key in metadata:
        local=copy.deepcopy(metadata);local[key]="CHANGED_LOCAL_"+key
        probe("local_metadata_"+key,copy.deepcopy(escaped),local,False)
        remote=copy.deepcopy(escaped);remote["metadata"][key]="CHANGED_REMOTE_"+key
        probe("remote_metadata_"+key,remote,expected=False)
    for mode in ("missing","extra"):
        local=copy.deepcopy(metadata)
        if mode=="missing":local.pop("title")
        else:local["new_metadata_key"]="X"
        probe("local_"+mode+"_metadata_key",copy.deepcopy(escaped),local,False)
    desc=escaped["metadata"]["description"]
    variants={
      "changed_math":desc.replace("r=2p-1","r=2p+1"),
      "changed_rank":desc.replace("n&gt;=2","n&gt;=3"),
      "numeric_gt_entity":desc.replace("&gt;","&#62;"),
      "double_encoded_gt":desc.replace("&gt;","&amp;gt;"),
      "whole_html_escape":html.escape(metadata["description"],quote=False),
      "additional_amp_entity":desc.replace("Young module","Young&nbsp;module",1),
      "escaped_apostrophe":desc.replace("'","&#39;",1),
      "stripped_tags":desc.replace("<p>","").replace("</p>",""),
      "removed_tag":desc.replace("<p>","",1),
      "leading_space":" "+desc,
      "trailing_newline":desc+"\n",
      "entity_elsewhere":desc.replace("n&gt;=2","n>=2").replace("I_n(lambda)","I_n&#40;lambda)"),
    }
    for name,value in variants.items():
        need(value!=desc and value!=metadata["description"],"Ineffective negative:"+name)
        d=copy.deepcopy(escaped);d["metadata"]["description"]=value;probe("description_"+name,d,expected=False)
    for index in range(len(files)):
        for field in ("checksum","filesize","filename"):
            d=copy.deepcopy(escaped);item=d["files"][index]
            item[field]={"checksum":"md5:"+"0"*32,"filesize":files[index]["size"]+1,
                         "filename":"changed-"+files[index]["name"]}[field]
            probe("file_"+str(index)+"_"+field,d,expected=False)
    for mode in ("missing","extra","duplicate","invalid_list","invalid_entry"):
        d=copy.deepcopy(escaped)
        if mode=="missing":d["files"].pop()
        elif mode=="extra":d["files"].append({"filename":"extra.txt","filesize":0,"checksum":"md5:"+"0"*32})
        elif mode=="duplicate":d["files"].append(copy.deepcopy(d["files"][0]))
        elif mode=="invalid_list":d["files"]={}
        else:d["files"][0]="not-an-entry"
        probe("files_"+mode,d,expected=False)
    guard_cases=[]
    def install_reject(name,tool,path):
        before=tool.verify
        try:adapter.install(tool,path)
        except Exception as e:error=type(e).__name__+": "+str(e)
        else:raise ValueError("Install guard accepted:"+name)
        need(tool.verify is before,"Failed install mutated verifier")
        guard_cases.append({"case":name,"rejected":True,"error":error,"verifier_unchanged":True})
    template=lambda:types.SimpleNamespace(__file__=str(x.tool),verify=original,DepositError=z.DepositError)
    with tempfile.TemporaryDirectory(prefix="adapter-pins-",dir=x.scratch) as temp:
        b=Path(temp);bad_metadata=b/"metadata.json";bad_metadata.write_bytes((x.frozen/"zenodo-metadata.json").read_bytes()+b" ")
        install_reject("frozen_metadata_byte_pin",template(),bad_metadata)
        bad_tool=b/"changed_tool.py";bad_tool.write_bytes(x.tool.read_bytes()+b"\n# changed\n")
        obj=template();obj.__file__=str(bad_tool);install_reject("tool_byte_pin",obj,x.frozen/"zenodo-metadata.json")
        copied=b/"same_tool.py";copied.write_bytes(x.tool.read_bytes())
        obj=template();obj.__file__=str(copied);install_reject("tool_function_filename",obj,x.frozen/"zenodo-metadata.json")
        obj=template();obj.verify=lambda d,m,f:[];install_reject("nonoriginal_verifier_module",obj,x.frozen/"zenodo-metadata.json")
        changed=b/"adapter.py";changed.write_bytes(x.adapter.read_bytes()+b"\nraise RuntimeError('BAD_CODE')\n")
        try:load_pinned(changed,"must_not_import",APIN)
        except ValueError as e:guard_cases.append({"case":"adapter_code_pin_before_import","rejected":True,"error":str(e)})
        else:raise ValueError("Altered adapter executed")
    install_reject("double_install",z,x.frozen/"zenodo-metadata.json")
    need(canonical({"metadata":metadata,"fixture":fixture})==before_input,"Original fixture changed")
    need(sha(x.tool.read_bytes())==ZPIN and sha(x.adapter.read_bytes())==APIN,"Reviewed code changed")
    print(json.dumps({"result":"PASS","scope":"Offline administrative encoding adapter; not another whole-paper review.",
        "adapter_sha256":APIN,"tool_sha256":ZPIN,"frozen_metadata_sha256":MPIN,"known_id":ID,
        "installation":installation,"verification_cases":cases,"install_guards":guard_cases,
        "verification_case_count":len(cases),"install_guard_count":len(guard_cases),
        "network_auth_state_actions_performed":False,"inputs_unchanged":True,
        "original_file_checks":"The unchanged repository verifier compares exact expected filenames, MD5 and size from the frozen local manifest. No new SHA256 or arbitrary caller-file-list guarantee is asserted.",
        "optimized":bool(sys.flags.optimize)},indent=2,sort_keys=True))
if __name__=="__main__":main()
