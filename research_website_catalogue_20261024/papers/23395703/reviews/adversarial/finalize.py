"""Seal only this own review after complete original and primary byte rechecks."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json
import runpy

HERE=Path(__file__).resolve().parent
SOURCE=HERE.parents[1]/"sources"


def h(data):return sha256(data).hexdigest()


def write(name,value):
    target=HERE/name
    if target.exists():raise RuntimeError("Refusing immutable evidence overwrite: "+name)
    target.write_text(json.dumps(value,indent=2,ensure_ascii=False)+"\n")


if __name__=="__main__":
    early_bytes=(HERE/"EARLY_SEAL.json").read_bytes()
    assert h(early_bytes)=="ab4b1ac29419f2662e811a9cabd49c8fcf2dd1270e381b1ff383691f1b75604d"
    early=json.loads(early_bytes)
    assert h((HERE/early["ledger"]).read_bytes())==early["ledger_sha256"]
    own=runpy.run_path(str(HERE/"checks.py"))
    custody=own["custody"]()
    assert own["prior_custody"]()==json.loads((HERE/"PRIOR_PACKET_PRESERVATION.json").read_text())
    write("FINAL_ORIGINAL_BINDING_RECEIPT.json",custody)
    primaries=json.loads((HERE/"PRIMARY_INTERFACES.json").read_text())
    for item in primaries["objects"]:
        data=Path(item["path"]).read_bytes()
        assert len(data)==item["bytes"] and h(data)==item["sha256"]
        assert h(Path(item["ignored_extraction"]).read_bytes())==item["extraction_sha256"]
    for item in primaries["renderings"]:
        data=Path(item["path"]).read_bytes()
        assert len(data)==item["bytes"] and h(data)==item["sha256"]
    special={"seven_plane_gin.pdf":"Complete actual six-page PDF read by full layout-preserving extraction before early seal",
             "seven_plane_gin.tex":"Complete separately deposited controlling TeX read before early seal",
             "SOURCE_READY.json":"Source identity/custody data only",
             "record.raw.json":"Edition metadata only; no author's description adopted as evidence",
             "published-source/audits/exact_reproduction_audit_01/reproduce_exact.py":"Complete supplied program inspected after early seal; not executed/imported",
             "published-source/audits/exact_reproduction_audit_01/orthogonal_checks.py":"Complete supplied program inspected after early seal; not executed/imported",
             "published-source/audits/exact_reproduction_audit_01/EXACT_CERTIFICATE.json":"Actual mathematical data parsed and independently checked: polynomials/Macaulay matrices/minors/complete left kernels/Hilbert-Burch data",
             "published-source/audits/exact_reproduction_audit_01/ORTHOGONAL_CERTIFICATE.json":"Actual mathematical data parsed and independently checked within stated finite scopes; no historical opinions adopted"}
    reads=[{"path":str(SOURCE/item["path"]),"bytes":item["bytes"],"sha256":item["sha256"],
            "scope":special.get(item["path"],"Byte authentication only; historical/current review opinions not consumed")}
           for item in custody["bindings"]]
    for name in ["SOURCE_READY_MANIFEST.json","SOURCE_READY_SEAL.json"]:
        data=(SOURCE/name).read_bytes()
        reads.append({"path":str(SOURCE/name),"bytes":len(data),"sha256":h(data),"scope":"Custody manifest only"})
    for item in primaries["objects"]:
        reads.append({"path":item["path"],"bytes":item["bytes"],"sha256":item["sha256"],
                      "scope":item["passages_independently_inspected"],"phase":"After early independence seal"})
    write("READ_LEDGER.json",{"utc":datetime.now(timezone.utc).isoformat(),"reads":reads,
          "own_executed_code_inspected_first":["checks.py","scope_controls.py","primary_receipt.py","finalize.py"],
          "source_worker_handoff":"Raw primary paths/hashes/transport facts only; no evaluations supplied",
          "historical_or_current_review_opinions_read":False,
          "prior_packets":"All three owned-artifact manifests and seals rehashed only; no opinions consumed",
          "Ilardi_full_body":"Unavailable; institutional listing/abstract only",
          "visual_source_inspection":"BPT printed7 and OWR printed234 rendered with Poppler into preignored cache and inspected; PDF skill used read-only"})
    files=[]
    for path in sorted(HERE.iterdir()):
        if path.is_file() and path.name not in {"FINAL_MANIFEST.json","FINAL_SEAL.json"}:
            data=path.read_bytes()
            if path.suffix==".json":json.loads(data)
            files.append({"path":path.name,"bytes":len(data),"sha256":h(data)})
            path.chmod(0o444)
    write("FINAL_MANIFEST.json",{"utc":datetime.now(timezone.utc).isoformat(),"status":"COMPLETE_IMMUTABLE_BOUNDED_ADVERSARIAL_PACKET",
          "record_id":23395703,"row":96,"version":None,"version_field_absent":True,"completion_percent":100,
          "original_bindings_rechecked":88,"original_ZIP_members_CRC_rechecked":78,
          "source_ready_seal_sha256":early["source_ready_seal_sha256"],"three_prior_packets_unchanged":True,
          "foreign_full_text_cache_excluded":"replay-work/primary/","public_promotion_authority":False,"files":files})
    (HERE/"FINAL_MANIFEST.json").chmod(0o444)
    mapping={item["path"]:item for item in files}
    seal={"utc":datetime.now(timezone.utc).isoformat(),"status":"COMPLETE_SEALED_NO_PROMOTION_AUTHORITY",
          "manifest":"FINAL_MANIFEST.json","manifest_sha256":h((HERE/"FINAL_MANIFEST.json").read_bytes()),
          "report_sha256":mapping["REPORT.md"]["sha256"],"verdict_sha256":mapping["verdict.json"]["sha256"],
          "derivations_sha256":mapping["DERIVATIONS.md"]["sha256"],"early_seal_sha256":h(early_bytes),
          "all_original_primary_and_prior_packet_bytes_unchanged":True,"bounded_completion_percent":100,
          "overall203_paper_goal":"ONGOING"}
    write("FINAL_SEAL.json",seal)
    (HERE/"FINAL_SEAL.json").chmod(0o444)
    print(json.dumps({**seal,"seal_sha256":h((HERE/"FINAL_SEAL.json").read_bytes())},indent=2))
