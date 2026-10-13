"""Offline checks of selected deposit adapter and this case's native metadata."""
import copy, datetime, hashlib, importlib.util, json, pathlib, sys
sys.dont_write_bytecode = True
OUT = pathlib.Path(__file__).resolve().parent
CASE = OUT.parents[1]
ROOT = CASE.parents[2]
ADAPTER = ROOT / "zenodo_deposit_tool/zenodo.py"
MANIFEST = CASE / "publication/zenodo-deposit.json"
def need(condition, message):
    if not condition:
        raise ValueError(message)
def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    need(sha(ADAPTER) == "a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca", "Adapter drift")
    need(sha(MANIFEST) == "dab7b5905850e99e2224d6b5bce1a74f0c7ecd860247dfa019c9baf0a85c23a4", "Metadata drift")
    spec = importlib.util.spec_from_file_location("selected_deposit_adapter", ADAPTER)
    adapter = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(adapter)
    metadata, files = adapter.load_manifest(MANIFEST)
    need(metadata["version"] == "1.0" and metadata["language"] == "eng", "Version/language disagreement")
    need(metadata["upload_type"] == "publication" and metadata["publication_type"] == "preprint", "Wrong resource")
    need(metadata["access_right"] == "open" and metadata["license"] == "cc-by-4.0", "Wrong access/license")
    need(metadata["creators"] == [{"name":"Kriebel, Alec","affiliation":"Independent researcher","orcid":"0009-0001-9320-500X"}], "Wrong creator")
    expected = {
      "aim_5_2_two_cube_cubulation.pdf":"3dfdfca7c0b9d41c54ed03dc9500afd8d8013fef2ebd589b2806712f84781841",
      "aim_5_2_source.zip":"a244ddbbbb0f7ca6d9ca073d21589bef1e9c0a98a404daaca195ee9fc87f6935",
      "aim_5_2_verification.zip":"8ff6e88f6d4a539680667b22931e080365dfd905dd64f795f408e23cc7bb8f01"
    }
    need({f["name"]:f["sha256"] for f in files} == expected, "Upload files disagree")
    remote = {"id":421,"submitted":False,"metadata":copy.deepcopy(metadata),
              "files":[{"filename":f["name"],"filesize":f["size"],"checksum":"md5:"+f["md5"]} for f in files]}
    adapter.validate_record(remote,421)
    need(adapter.verify(remote,metadata,files)==[], "Exact synthetic read-back rejected")
    negatives=[]
    def reject(label, actual, function=adapter.verify):
        try:
            function(actual,metadata,files)
        except adapter.DepositError as error:
            negatives.append({"label":label,"rejected":True,"exception":"DepositError","message":str(error)})
        else:
            raise ValueError("Corruption accepted: "+label)
    for key in metadata:
        changed=copy.deepcopy(remote); changed["metadata"][key]="__substantive_corruption__"
        reject("changed_metadata."+key, changed)
    for key in ("version","language","license"):
        changed=copy.deepcopy(remote);del changed["metadata"][key]
        reject("missing_metadata."+key,changed)
    changed=copy.deepcopy(remote);changed["files"][0]["checksum"]="md5:"+"0"*32
    reject("wrong_file_md5",changed)
    changed=copy.deepcopy(remote);changed["files"][0]["filesize"]+=1
    reject("wrong_file_size",changed)
    changed=copy.deepcopy(remote);changed["files"].append({"filename":"unlisted.txt","filesize":0,"checksum":"md5:"+"0"*32})
    reject("unlisted_remote_file",changed)
    for label,field,value in [("wrong_deposit_id","id",422),("nonboolean_submitted","submitted","true")]:
        changed=copy.deepcopy(remote);changed[field]=value
        try:adapter.validate_record(changed,421)
        except adapter.DepositError as error:negatives.append({"label":label,"rejected":True,"exception":"DepositError","message":str(error)})
        else:raise ValueError("Record corruption accepted: "+label)
    result={"time_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "optimization_enabled":not __debug__,"adapter_sha256":sha(ADAPTER),"manifest_sha256":sha(MANIFEST),
            "mode":"offline import/load_manifest/verify/validate_record; no API client instantiated",
            "supplied_metadata_keys":sorted(metadata),"local_files":[{"name":f["name"],"bytes":f["size"],"sha256":f["sha256"]} for f in files],
            "exact_synthetic_readback_passed":True,"negative_cases":negatives,"negative_count":len(negatives),
            "live_api_acceptance_tested":False,"live_mutation_performed":False,"status":"PASS"}
    name="METADATA_ADAPTER_OPTIMIZED.json" if not __debug__ else "METADATA_ADAPTER_NORMAL.json"
    (OUT/name).write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({"status":"PASS","negative_count":len(negatives),"optimization_enabled":not __debug__}))
if __name__ == "__main__":main()
