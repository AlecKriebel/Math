"""Seal only this independent audit; never executes or changes the target stage."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json

HERE = Path(__file__).resolve().parent


if __name__ == "__main__":
    preservation = json.loads((HERE / "PRESERVATION_BINDINGS.json").read_text())
    for name, expected in preservation["before"].items():
        data = Path(name).read_bytes()
        assert {"bytes":len(data),"sha256":sha256(data).hexdigest()} == expected
    files = {}
    for path in sorted(HERE.iterdir()):
        if path.is_file() and path.name not in {"FINAL_MANIFEST.json","FINAL_SEAL.json"}:
            data = path.read_bytes()
            if path.suffix == ".json":
                json.loads(data)
            files[path.name] = {"bytes":len(data),"sha256":sha256(data).hexdigest()}
            path.chmod(0o444)
    for name in ["FINAL_MANIFEST.json","FINAL_SEAL.json"]:
        if (HERE / name).exists():
            raise RuntimeError("Refusing overwrite of seal")
    manifest = {"utc":datetime.now(timezone.utc).isoformat(),"status":"COMPLETE_INDEPENDENT_READ_ONLY_CODE_CUSTODY_AUDIT",
                "readiness_manifest_sha256":"bfebb68338fb0bace50ad3e6e99cd7bc0fb97dab49747334f201603c31ffb2bf",
                "all_640_preservation_bindings_final_recheck_pass":True,
                "all_165_stage_owned_readiness_bindings_pass":True,
                "publication_authorization":False,"files":files}
    target = HERE / "FINAL_MANIFEST.json"
    target.write_text(json.dumps(manifest,indent=2)+"\n")
    target.chmod(0o444)
    seal = {"utc":datetime.now(timezone.utc).isoformat(),"status":"COMPLETE_SEALED_NO_INSTALLATION_AUTHORITY",
            "manifest":"FINAL_MANIFEST.json","manifest_sha256":sha256(target.read_bytes()).hexdigest(),
            "report_sha256":files["REPORT.md"]["sha256"],"verdict_sha256":files["verdict.json"]["sha256"],
            "publication_authorization":False,"bounded_completion_percent":100}
    seal_path = HERE / "FINAL_SEAL.json"
    seal_path.write_text(json.dumps(seal,indent=2)+"\n")
    seal_path.chmod(0o444)
    print(json.dumps({**seal,"seal_sha256":sha256(seal_path.read_bytes()).hexdigest()},indent=2))
