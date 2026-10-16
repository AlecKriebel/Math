#!/usr/bin/env python3
"""Independently read production public Zenodo payloads and metadata; no tokens.

HTTP response bodies are held in memory and never added to the authored packet.
Only supplied metadata values are compared: public-record schema wrappers for
license and resource_type are explicitly projected to the deposition schema.
List order, length and every supplied scalar remain exact.
"""
import argparse, copy, datetime, hashlib, json, sys, urllib.parse, urllib.request
from pathlib import Path
sys.dont_write_bytecode = True
T = Path(__file__).resolve().parents[2]
MF = "5d7bccdc118a464da0e149804c4b512c88a9d28cbff2d8b3bc280d963dd4f348"

def need(value, reason):
    if not value:
        raise RuntimeError(reason)

def supplied_projection(actual, wanted, path="metadata"):
    if isinstance(wanted, dict):
        need(isinstance(actual, dict), "Object absent at "+path)
        return {k: supplied_projection(actual.get(k), v, path+"."+k) for k,v in wanted.items()}
    if isinstance(wanted, list):
        need(isinstance(actual, list) and len(actual) == len(wanted), "List length/order differs at "+path)
        return [supplied_projection(a, w, path+"[%d]" % i) for i,(a,w) in enumerate(zip(actual,wanted))]
    need(type(actual) is type(wanted) and actual == wanted, "Supplied metadata differs at "+path)
    return actual

def compare_metadata(remote, wanted):
    normalized = copy.deepcopy(remote)
    translations = []
    for key, publickey in (("upload_type", "type"), ("publication_type", "subtype")):
        if key not in normalized:
            need(isinstance(normalized.get("resource_type"), dict), "Missing public resource type")
            normalized[key] = normalized["resource_type"].get(publickey)
            translations.append(key+" <- resource_type."+publickey)
    if isinstance(normalized.get("license"), dict):
        normalized["license"] = normalized["license"].get("id")
        translations.append("license <- license.id")
    projection = supplied_projection(normalized, wanted)
    need(projection == wanted, "Supplied metadata projection differs")
    return translations

def controls(wanted):
    public = copy.deepcopy(wanted)
    public["resource_type"] = {"type": public.pop("upload_type"), "subtype": public.pop("publication_type"), "title": "Server display title"}
    public["license"] = {"id": public["license"], "url": "https://creativecommons.org/licenses/by/4.0/"}
    rows = []
    def test(name, obj, expected):
        try:
            compare_metadata(obj, wanted); accepted = True
        except RuntimeError:
            accepted = False
        rows.append({"case": name, "accepted": accepted, "control_pass": accepted == expected})
    test("all_supplied_metadata_exact_public_schema_wrappers", public, True)
    for key in wanted:
        obj = copy.deepcopy(public)
        if key == "upload_type": obj["resource_type"]["type"] = "dataset"
        elif key == "publication_type": obj["resource_type"]["subtype"] = "article"
        elif key == "license": obj["license"]["id"] = "cc-by-nc-4.0"
        elif isinstance(wanted[key], list): obj[key] = obj[key][:-1]
        else: obj[key] = "CONTROL changed value"
        test("changed_supplied_"+key, obj, False)
    need(all(x["control_pass"] for x in rows), "Metadata control failed")
    return rows

def fetch(url, method="GET"):
    req = urllib.request.Request(url, headers={"User-Agent": "PR789-independent-public-custody-audit"}, method=method)
    with urllib.request.urlopen(req, timeout=90) as r:
        need(r.status == 200, "Public response is not HTTP200")
        return r.read(), r.status, r.url

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--record-id", type=int); p.add_argument("--doi")
    p.add_argument("--controls-only", action="store_true"); p.add_argument("--out", type=Path)
    a = p.parse_args()
    inv = json.loads((T/"preprint/PACKAGE_INVENTORY.json").read_text())
    need(inv["source_manifest_sha256"] == MF, "Source manifest pin changed")
    for row in inv["files"]:
        raw = (T/"preprint"/row["path"]).read_bytes()
        need(len(raw) == row["bytes"] and hashlib.sha256(raw).hexdigest() == row["sha256"], "Frozen package artifact changed")
    meta = json.loads((T/"preprint/zenodo-metadata.json").read_text())["metadata"]
    manifest = json.loads((T/"preprint/zenodo-deposit.json").read_text())
    need(meta == manifest["metadata"], "Two supplied metadata objects differ")
    result = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(), "source_manifest_sha256": MF,
              "metadata_file_sha256": hashlib.sha256((T/"preprint/zenodo-metadata.json").read_bytes()).hexdigest(),
              "controls": controls(meta), "credentials_loaded": False, "HTTP_bodies_saved": False}
    if a.controls_only:
        need(a.record_id is None and a.doi is None, "Controls must not imply an actual public check")
        result["result"] = "PASS_METADATA_PROJECTION_CONTROLS_ONLY"
    else:
        need(a.record_id and a.record_id > 0 and a.doi == "10.5281/zenodo."+str(a.record_id), "Exact known production record DOI required")
        raw,status,url = fetch("https://zenodo.org/api/records/"+str(a.record_id))
        record = json.loads(raw)
        need(type(record["id"]) is int and record["id"] == a.record_id and record["metadata"]["doi"] == a.doi, "Public record/DOI identity differs")
        translations = compare_metadata(record["metadata"], meta)
        rows = record["files"]; names = [r["key"] for r in rows]
        expected = {r["name"]: r["path"] for r in manifest["files"]}
        need(len(expected) == 2 and len(names) == 2 and len(set(names)) == 2 and set(names) == set(expected), "Public exact two-file list differs")
        inventory = {r["path"]: r for r in inv["files"]}
        payloads = []
        for row in rows:
            name = row["key"]; wanted = inventory[expected[name]]
            need(row["size"] == wanted["bytes"], "Public advertised size differs")
            raw,status,url = fetch("https://zenodo.org/records/"+str(a.record_id)+"/files/"+urllib.parse.quote(name, safe="")+"?download=1")
            digest = hashlib.sha256(raw).hexdigest()
            need(len(raw) == wanted["bytes"] and digest == wanted["sha256"], "Public downloaded payload SHA256/size differs")
            payloads.append({"name": name, "bytes": len(raw), "sha256": digest, "HTTP_status": status, "final_url": url})
        raw,status,url = fetch("https://doi.org/"+a.doi, "HEAD")
        dest = urllib.parse.urlsplit(url)
        need(dest.scheme == "https" and dest.hostname in ("zenodo.org", "www.zenodo.org")
             and dest.path.rstrip("/") in ("/record/"+str(a.record_id), "/records/"+str(a.record_id)), "DOI200 does not resolve to the exact known record")
        result.update(result="PASS_PUBLIC_EXACT_METADATA_PAYLOADS_AND_DOI", record_id=a.record_id, doi=a.doi,
                      every_supplied_metadata_value_exact=True, public_schema_wrapper_projections=translations,
                      public_files=payloads, DOI={"HTTP_status": status, "final_url": url},
                      primary_public_bodies_or_auth_material_in_authored_packet=False)
    raw = json.dumps(result, indent=2)+"\n"
    if a.out:
        need(a.out.resolve().is_relative_to(Path(__file__).resolve().parents[1]), "Output outside owned admin area")
        a.out.write_text(raw)
    print(raw)

if __name__ == "__main__": main()
