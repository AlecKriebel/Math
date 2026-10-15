"""Use the unmodified repository kit with one exact frozen HTML transport guard."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,sys
A=Path(__file__).resolve().parent;R=Path("/Users/alec/Documents/Math")
def require(c,m):
 if not c:raise RuntimeError(m)
def pin(p):
 b=p.read_bytes();return {"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def guarded_verify(original,deposit,metadata,files):
 expected=json.loads((A/"publication_package_v2/metadata.json").read_text())
 require(metadata==expected,"Transport guard is restricted to the exact frozen submitted metadata")
 e=expected["description"]
 require(e.count("n>=3")==1 and e.count("n>=4")==1,"Frozen exact comparator count differs")
 canonical=e.replace("n>=3","n&gt;=3").replace("n>=4","n&gt;=4")
 actual=deposit.get("metadata",{}).get("description")
 if actual==canonical:
  transport={**metadata,"description":canonical}
  allowances=original(deposit,transport,files)
  return allowances+[{"field":"description","transformation":"Exactly the two frozen paragraph-text n>=3/n>=4 greater-than characters serialized as &gt;; every other character, paragraph/tag and submitted metadata field unchanged","raw_intended_metadata_unchanged":True}]
 return original(deposit,metadata,files)
def main():
 parser=argparse.ArgumentParser()
 parser.add_argument("command",choices=["inspect","publish"])
 parser.add_argument("manifest",type=Path)
 parser.add_argument("--confirm-id",type=int)
 parser.add_argument("--check-doi",action="store_true")
 args=parser.parse_args();args.sandbox=False
 gate=json.loads((A/"ROOT_PUBLICATION_GATE.json").read_text())
 tg=json.loads((A/"ROOT_PUBLICATION_TRANSPORT_GATE.json").read_text())
 require(tg["status"]=="EXACT_HTML_DESCRIPTION_TRANSPORT_GUARD_INDEPENDENTLY_VERIFIED","Transport guard not independently cleared")
 require(tg["guard_identity"]==pin(Path(__file__)),"Guard changed")
 require(args.manifest.resolve()==(A/"zenodo-deposit.v2.json").resolve() and hashlib.sha256(args.manifest.read_bytes()).hexdigest()==gate["deposit_manifest_sha256"],"Unexpected frozen manifest")
 for n,v in gate["kit_files"].items():require(pin(R/n)==v,"Original repository kit changed")
 sp=importlib.util.spec_from_file_location("original_zenodo_kit",R/"zenodo_deposit_tool/zenodo.py");kit=importlib.util.module_from_spec(sp);sp.loader.exec_module(kit)
 place,state=kit.local_state(args.manifest.resolve(),"production")
 require(state is not None and state["id"]==23318851,"Known original draft state absent or changed")
 require(args.command!="publish" or args.confirm_id==23318851,"Wrong publication confirmation ID")
 original=kit.verify;kit.verify=lambda deposit,metadata,files:guarded_verify(original,deposit,metadata,files)
 result=kit.run(args)
 require(result["id"]==23318851,"A different deposit was selected")
 print(json.dumps(result,indent=2))
if __name__=="__main__":main()
