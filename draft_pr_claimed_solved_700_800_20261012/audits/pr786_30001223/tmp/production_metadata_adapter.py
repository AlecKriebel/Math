"""PR786-only exact observed Zenodo paragraph entity normalization.

No network, metadata mutation, file upload or publication is performed here.
The repository tool retains all original verification except one exact,
visually identical serialization of the frozen description for known draft23418581.
"""
from pathlib import Path
import copy,hashlib,json
EXPECTED_TOOL_SHA256="a91f961bcabadb15f92bb738c3194f0277cd47f1f87167ac8db8eb7c4fd3b9ca"
EXPECTED_METADATA_SHA256="309a2dd51cee7be8d35bef49659c26818ed2e7f40ec78d639f2c83fa227ec3c5"
EXPECTED_ID=23418581
def install(tool,metadata_path):
    if hashlib.sha256(Path(tool.__file__).read_bytes()).hexdigest()!=EXPECTED_TOOL_SHA256:
        raise ValueError("Repository Zenodo tool changed")
    original=tool.verify
    if original.__module__!="zenodo" or Path(original.__code__.co_filename).resolve()!=Path(tool.__file__).resolve():
        raise ValueError("Expected original repository verifier")
    raw=Path(metadata_path).read_bytes()
    if hashlib.sha256(raw).hexdigest()!=EXPECTED_METADATA_SHA256:
        raise ValueError("Frozen PR786 metadata bytes changed")
    expected=json.loads(raw)["metadata"]
    description=expected["description"]
    if description.count("n>=2")!=1 or "n&gt;=2" in description:
        raise ValueError("Unexpected frozen normalization locus")
    escaped=description.replace("n>=2","n&gt;=2")
    def verified(deposit,metadata,files):
        if type(deposit.get("id")) is not int or deposit["id"]!=EXPECTED_ID:
            raise tool.DepositError("Adapter is bound to the single known PR786 draft")
        if metadata!=expected:
            raise tool.DepositError("Adapter accepts only complete frozen PR786 metadata")
        actual=deposit.get("metadata",{}).get("description")
        if actual==escaped:
            checked=copy.deepcopy(deposit)
            checked["metadata"]["description"]=description
            changes=original(checked,metadata,files)
            return changes+[{"field":"description","kind":"single_observed_paragraph_text_gt_entity_n_ge_2",
                "local_text":"n>=2","stored_html_text":"n&gt;=2","visible_text_unchanged":True,
                "metadata_sha256":EXPECTED_METADATA_SHA256,"draft_id":EXPECTED_ID}]
        return original(deposit,metadata,files)
    tool.verify=verified
    return {"result":"INSTALLED_CASE_BOUND_NORMALIZATION","id":EXPECTED_ID,
        "repository_tool_sha256":EXPECTED_TOOL_SHA256,"metadata_sha256":EXPECTED_METADATA_SHA256,
        "description_sha256":hashlib.sha256(description.encode()).hexdigest(),
        "stored_description_sha256":hashlib.sha256(escaped.encode()).hexdigest(),
        "normalization":"Exactly one literal > in n>=2 becomes &gt;; every other description byte and all other tool checks retained.",
        "network_actions_performed":False}
