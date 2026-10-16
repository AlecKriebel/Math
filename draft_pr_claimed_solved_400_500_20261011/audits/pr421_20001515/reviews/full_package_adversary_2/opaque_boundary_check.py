"""Check unrelated tree-entry preservation without reading foreign blob bodies."""
import datetime, hashlib, json, pathlib
OUT=pathlib.Path(__file__).resolve().parent
P=OUT.parents[1]/"private_sources/full_package_adversary_2"
def need(condition,message):
    if not condition: raise ValueError(message)
def verified(tree):
    need(not tree["truncated"],"truncated tree")
    order=sorted(tree["tree"],key=lambda e:(e["path"]+("/" if e["type"]=="tree" else "")).encode())
    body=b"".join(e["mode"].lstrip("0").encode()+b" "+e["path"].encode()+b"\0"+bytes.fromhex(e["sha"]) for e in order)
    need(hashlib.sha1(b"tree "+str(len(body)).encode()+b"\0"+body).hexdigest()==tree["sha"],"tree SHA mismatch")
    return {e["path"]:(e["mode"],e["type"],e["sha"]) for e in order}
def main():
    original=json.loads((P/"opaque_preservation_gets.json").read_text())
    current=json.loads((P/"targeted_tree_native_gets.json").read_text())
    old=[json.loads(r["structuredContent"]["content"]) for r in original["trees"]]
    newer={r["sha"]:json.loads(r["response"]["structuredContent"]["content"]) for r in current["responses"]}
    path=[
      ("", "unsolved_math_prioritization", "f2649daec6286218bf44b8279bb5d7475b334957"),
      ("unsolved_math_prioritization","attempts","0c9ecad4bca4b0255f40be34e27b83e1eff953d4"),
      ("unsolved_math_prioritization/attempts","20001515","7d60844722714c31b8e9214a7998bf116410ff91")]
    rows=[]
    for tree,(ancestor,allowed,sha) in zip(old,path):
        before=verified(tree);after=verified(newer[sha])
        need(set(before)==set(after),"ancestor entry added/deleted outside selected subtree")
        changed={k for k in before if before[k]!=after[k]}
        need(changed=={allowed},"foreign ancestor child changed")
        for k in before:
            if k!=allowed: need(before[k]==after[k],"opaque foreign identity changed")
        rows.append({"ancestor_path":ancestor,"original_tree_sha":tree["sha"],"current_tree_sha":sha,
                     "only_changed_child":allowed,"unchanged_opaque_entry_count":len(before)-1,
                     "all_other_modes_types_object_shas_identical":True,"object_shas_independently_verified":True})
    need([p["sha"] for p in current["head"]["parents"]]==["d5bf8b5a25cabb177433338fae60af52ebfecf1c"],"unexpected current parent")
    receipt={"time_utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),
      "original_source_head":"d5bf8b5a25cabb177433338fae60af52ebfecf1c",
      "actual_head":"2e85a0b10c3793ed1d46726b50efac5a6306b707",
      "actual_parent_is_original_source_head":True,"comparisons":rows,
      "no_foreign_blob_body_read":True,"all_outside_selected_attempt_preserved_from_original_source_head":True,"status":"PASS"}
    (OUT/"OPAQUE_BOUNDARY_PRESERVATION.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps(receipt,indent=2))
if __name__=="__main__":main()
