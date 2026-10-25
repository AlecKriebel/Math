"""Seal this own review after repeating all original-object and primary bindings.

No original verification program or prior review opinion is executed/consumed.
Only own namespace is written or chmodded; originals are read-only.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json
import runpy

HERE=Path(__file__).resolve().parent
SOURCES=HERE.parents[1]/"sources"


def h(data):return sha256(data).hexdigest()


def write(name,value):
    target=HERE/name
    if target.exists():raise RuntimeError("Refusing immutable evidence overwrite: "+name)
    target.write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n")


if __name__=="__main__":
    early_bytes=(HERE/"EARLY_SEAL.json").read_bytes()
    assert h(early_bytes)=="3689eca607c5eb8a172f49526ad8b75fccf5cc7cef7e83ab590e91c6771ea0aa"
    early=json.loads(early_bytes)
    assert h((HERE/early["ledger"]).read_bytes())==early["ledger_sha256"]
    functions=runpy.run_path(str(HERE/"checks.py"))
    final_custody=functions["custody"]()
    assert functions["prior_packet_custody"]()==json.loads((HERE/"PRIOR_PACKET_PRESERVATION.json").read_text())
    write("FINAL_ORIGINAL_BINDING_RECEIPT.json",final_custody)
    primary=json.loads((HERE/"PRIMARY_INTERFACES.json").read_text())
    for item in primary["objects"]:
        data=Path(item["path"]).read_bytes()
        assert len(data)==item["bytes"] and h(data)==item["sha256"]
        assert h(Path(item["own_ignored_extraction"]).read_bytes())==item["extraction_sha256"]
    for item in primary["renderings"]:
        data=Path(item["path"]).read_bytes()
        assert len(data)==item["bytes"] and h(data)==item["sha256"]
    reads=[]
    interpreted={"Convex_Body_SOS_Density_Note_v1.0.pdf":"Complete actual5pp PDF, layout-preserving extraction read before early seal",
                 "published-source/manuscript/main.tex":"Complete controlling TeX read before early seal",
                 "SOURCE_READY.json":"Source identity/custody metadata only",
                 "record.raw.json":"Edition metadata only; no author scientific descriptions adopted as evidence"}
    for item in final_custody["bindings"]:
        reads.append({"path":str(SOURCES/item["path"]),"bytes":item["bytes"],"sha256":item["sha256"],
                      "read_scope":interpreted.get(item["path"],"Byte authentication only; historical mathematical opinions not read")})
    for name in ["SOURCE_READY_MANIFEST.json","SOURCE_READY_SEAL.json"]:
        data=(SOURCES/name).read_bytes()
        reads.append({"path":str(SOURCES/name),"bytes":len(data),"sha256":h(data),"read_scope":"Custody authentication manifest only"})
    for item in primary["objects"]:
        reads.append({"path":item["path"],"bytes":item["bytes"],"sha256":item["sha256"],"read_scope":item["passages_independently_inspected"],"phase":"After early independence seal"})
    write("READ_LEDGER.json",{"utc":datetime.now(timezone.utc).isoformat(),"originals_and_primary_reads":reads,
          "all_own_executed_source_inspected_first":["checks.py","primary_receipt.py","finalize.py"],
          "prior_packets":"Seals/manifests and owned artifacts byte-hashed only; no substantive opinions consumed.",
          "relevant_skill":"/Users/alec/.codex/plugins/cache/openai-primary-runtime/pdf/26.1020.11618/skills/pdf/SKILL.md; read-only visual primary equation inspection",
          "historical_or_current_review_opinions_read":False})
    files=[]
    for path in sorted(HERE.iterdir()):
        if path.is_file() and path.name not in {"FINAL_MANIFEST.json","FINAL_SEAL.json"}:
            data=path.read_bytes()
            if path.suffix==".json":json.loads(data)
            files.append({"path":path.name,"bytes":len(data),"sha256":h(data)})
            path.chmod(0o444)
    write("FINAL_MANIFEST.json",{"utc":datetime.now(timezone.utc).isoformat(),
          "status":"COMPLETE_IMMUTABLE_BOUNDED_ADVERSARIAL_REVIEW","record_id":23442760,"row":95,
          "completion_percent":100,"whole_original_bindings_rechecked":161,"original_archive_members_CRC_rechecked":152,
          "source_ready_seal_sha256":early["source_ready_seal_sha256"],
          "prior_discotope_and_CFH_packets_unchanged":True,"foreign_full_text_cache_excluded":"replay-work/primary/",
          "public_promotion_authority":False,"files":files})
    (HERE/"FINAL_MANIFEST.json").chmod(0o444)
    mapping={entry["path"]:entry for entry in files}
    final_seal={"utc":datetime.now(timezone.utc).isoformat(),"status":"COMPLETE_SEALED_NO_PROMOTION_AUTHORITY",
                "manifest":"FINAL_MANIFEST.json","manifest_sha256":h((HERE/"FINAL_MANIFEST.json").read_bytes()),
                "report_sha256":mapping["REPORT.md"]["sha256"],"verdict_sha256":mapping["verdict.json"]["sha256"],
                "derivations_sha256":mapping["DERIVATIONS.md"]["sha256"],"early_seal_sha256":h(early_bytes),
                "original_objects_and_primary_bytes_unchanged":True,"prior_packets_unchanged":True,
                "bounded_completion_percent":100,"overall_203_paper_goal":"ONGOING"}
    write("FINAL_SEAL.json",final_seal)
    (HERE/"FINAL_SEAL.json").chmod(0o444)
    print(json.dumps({**final_seal,"seal_sha256":h((HERE/"FINAL_SEAL.json").read_bytes())},indent=2))
