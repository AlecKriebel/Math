"""Independently compare the sealed stage's actual own outputs with its manifest.

Read-only outside this audit namespace. No staged code is executed.
"""
from pathlib import Path
from hashlib import sha256
from datetime import datetime, timezone
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
STAGE = ROOT / "verification/local-cubic-fps-hessian-stage-sol-20261025"


if __name__ == "__main__":
    manifest_bytes = (STAGE / "stage-readiness-manifest.json").read_bytes()
    assert sha256(manifest_bytes).hexdigest() == "bfebb68338fb0bace50ad3e6e99cd7bc0fb97dab49747334f201603c31ffb2bf"
    manifest = json.loads(manifest_bytes)
    preservation = json.loads((HERE / "PRESERVATION_BINDINGS.json").read_text())
    compared = []
    for label in ["owned_output_bindings", "original_input_bindings"]:
        for name, expected in manifest[label].items():
            path = Path(name)
            if not path.is_absolute():
                path = STAGE / path
            if label == "original_input_bindings" and str(path) not in preservation["before"]:
                continue
            if label == "owned_output_bindings":
                assert path.resolve().is_relative_to(STAGE.resolve())
            data = path.read_bytes()
            actual = {"bytes":len(data),"sha256":sha256(data).hexdigest()}
            assert actual == expected, (label, str(path), actual, expected)
            compared.append({"kind":label,"path":str(path),**actual})
    # Recheck this worker's full scope once more at the end of code review.
    for name, expected in preservation["before"].items():
        data = Path(name).read_bytes()
        assert {"bytes":len(data),"sha256":sha256(data).hexdigest()} == expected
    output = {
        "utc":datetime.now(timezone.utc).isoformat(),
        "status":"ALL_STAGE_OWNED_OUTPUTS_AND_IN_SCOPE_ORIGINAL_BINDINGS_MATCH",
        "readiness_manifest_sha256":sha256(manifest_bytes).hexdigest(),
        "all_owned_outputs_checked":sum(x["kind"]=="owned_output_bindings" for x in compared),
        "in_scope_original_inputs_checked":sum(x["kind"]=="original_input_bindings" for x in compared),
        "independent_preservation_bindings_rechecked":preservation["count"],
        "compared":compared,
        "full_out_of_scope_original_site_input_set_rehashed":False,
    }
    target = HERE / "READINESS_BINDING_CHECK.json"
    if target.exists():
        raise RuntimeError("Refusing evidence overwrite")
    target.write_text(json.dumps(output,indent=2)+"\n")
    print(json.dumps({k:v for k,v in output.items() if k!="compared"},indent=2))
