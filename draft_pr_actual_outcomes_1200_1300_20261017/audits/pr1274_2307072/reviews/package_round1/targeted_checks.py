from pathlib import Path
import copy, datetime, hashlib, importlib.util, json, runpy, sys, tempfile, types
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;A=R.parent.parent;P=A/"publication"
def load(p):
    s=importlib.util.spec_from_file_location("review_target_"+p.stem+str(id(p)),p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
def expect_reject(fn,label):
    try:fn()
    except (ValueError,RuntimeError,KeyError,TypeError):return label
    raise RuntimeError("Adversarial invalid input accepted: "+label)
m=load(P/"check_public_downloads.py");c=load(A.parents[1]/"publication_coordinators/pr1274.py");v=load(P/"verification/verify.py")
meta=json.loads((P/"zenodo-deposit.json").read_text())["metadata"]
actual=copy.deepcopy(meta);actual["resource_type"]={"type":actual.pop("upload_type"),"subtype":actual.pop("publication_type")};actual["license"]={"id":actual["license"]}
fields=m.verify_public_metadata(actual,meta);rejections=[]
for key in meta:
    bad=copy.deepcopy(actual)
    if key=="upload_type":bad["resource_type"]["type"]="wrong"
    elif key=="publication_type":bad["resource_type"]["subtype"]="wrong"
    elif key=="license":bad["license"]["id"]="wrong"
    else:bad[key]=None
    rejections.append(expect_reject(lambda:m.verify_public_metadata(bad,meta),"actual_metadata_"+key))
kit=c.load_exact_kit();localmeta,files=kit.load_manifest(P/"zenodo-deposit.json")
deposit={"metadata":copy.deepcopy(localmeta),"files":[{"filename":f["name"],"size":f["size"],"checksum":"md5:"+f["md5"]} for f in files]}
if kit.verify(deposit,localmeta,files)!=[]:raise RuntimeError("Actual metadata positive strict-kit control failed")
for key in localmeta:
    bad=copy.deepcopy(deposit);bad["metadata"][key]=None
    try:kit.verify(bad,localmeta,files)
    except kit.DepositError:rejections.append("actual_strict_kit_"+key)
    else:raise RuntimeError("Strict kit accepted actual field drift")
with tempfile.TemporaryDirectory(prefix="targeted_",dir=R/"own_local") as tmp:
    root=Path(tmp);(root/"case_name.md").write_text("authored bytes\n")
    rejections.append(expect_reject(lambda:v.member(root,"CASE_NAME.md"),"physical_case_mismatch"))
    (root/"alias").symlink_to(root/"case_name.md")
    rejections.append(expect_reject(lambda:v.member(root,"alias"),"symlink_member"))
    base=root/"reviews/family";base.mkdir(parents=True);(base/"member.md").write_text("selected relative membership\n")
    payload=(base/"member.md").read_bytes();manifest=base/"MANIFEST.json"
    record={"relative_path":"member.md","bytes":len(payload),"sha256":hashlib.sha256(payload).hexdigest(),"path":"/UNAVAILABLE/ABSOLUTE/RECEIPT","input_path":"/UNAVAILABLE/SOURCE"}
    manifest.write_text(json.dumps({"authored_files":[record]}));reg={"path":"reviews/family/MANIFEST.json","base":"reviews/family","entries_key":"authored_files","path_key":"relative_path","size_key":"bytes","sha256":hashlib.sha256(manifest.read_bytes()).hexdigest(),"role":"math"}
    v.authenticate_nested_manifests(root,[reg],require_complete=False)
    bad=copy.deepcopy(reg);bad["path_key"]="input_path"
    rejections.append(expect_reject(lambda:v.authenticate_nested_manifests(root,[bad],require_complete=False),"unused_input_path_not_membership"))
    bad=copy.deepcopy(reg);bad["path_key"]="path"
    rejections.append(expect_reject(lambda:v.authenticate_nested_manifests(root,[bad],require_complete=False),"unused_absolute_path_not_membership"))
    record.pop("relative_path");manifest.write_text(json.dumps({"authored_files":[record]}));reg["sha256"]=hashlib.sha256(manifest.read_bytes()).hexdigest()
    rejections.append(expect_reject(lambda:v.authenticate_nested_manifests(root,[reg],require_complete=False),"no_fallback_for_missing_selected_member"))
result={"schema":"math-pr1274-review-targeted-checks-v1","at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"status":"PASS","actual_metadata_fields":fields,"actual_strict_kit_two_file_positive_control":True,"explicit_relative_membership_ignores_unused_absolute_receipts":True,"rejected_controls":rejections,"limits":"Direct current real metadata/local artifacts and actual read-only kit verification only. No credentials, API, Git mutation or production integration."}
print(json.dumps(result,indent=2))
