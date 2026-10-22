from pathlib import Path
import json,hashlib,datetime
A=Path("draft_pr_claimed_solved_900_1000_20261012/audits/pr967_2616"); R=A/"reviews/computational_adversary_01"
rows=[json.loads(x) for x in (R/"receipts/new_execution_commands.jsonl").read_text().splitlines()]
assert len(rows)==409 and len({x["label"] for x in rows})==409
mode_counts={}
for mode in ["normal","O","OO"]:
 group=[x for x in rows if x["label"].startswith(mode+":")]; assert len(group)==136
 good=[x for x in group if x["label"].split(":",1)[1] in ["positive","maximum_accepted_size","external_bootstrap"]]
 bad=[x for x in group if x not in good]; assert len(good)==3 and len(bad)==133
 assert all(x["returncode"]==0 and x["stderr"]=="" for x in good)
 assert all(type(x["returncode"]) is int and x["returncode"]!=0 for x in bad)
 deep=[x for x in bad if x["label"].endswith(":deep_array")];assert len(deep)==1 and "RecursionError" in deep[0]["stderr"]
 for x in bad:
  if x not in deep: assert json.loads(x["stderr"])["ok"] is False
 mode_counts[mode]={"actual_children":136,"positive":3,"rejected":133,"only_unstructured":"deep_array"}
baseline=json.loads((R/"receipts/actual_reproduction.json").read_text())
assert len(baseline["commands"])==6
baseline_summary=[]
for i,x in enumerate(baseline["commands"]):
 assert x["returncode"]==0 and x["stderr"]==""
 v=json.loads(x["stdout"]);assert v["status"]=="PASS" and v["uid"]==v["euid"]==501
 key="optimization" if i<3 else "harness_optimization";assert v[key]==i%3
 if i<3:
  assert v["author_finite_checks_per_mode"]==43533 and v["independent_finite_checks"]==192528
  assert v["fresh_source_bindings"]==v["fresh_corpus_bindings"]=="NOT_RUN"
 else: assert v["negative_controls"]==len(set(v["negative_labels"]))==53
 baseline_summary.append({"label":x["label"],"utc":x["launch_utc"],"exit":x["returncode"],"optimization":v[key]})
outer=json.loads((R/"receipts/outer_cli_boundaries.json").read_text());assert len(outer)==22 and all(x["returncode"]!=0 for x in outer)
before=json.loads((R/"receipts/original_before.json").read_text());after=json.loads((R/"receipts/original_after.json").read_text());assert before["files"]==after["files"] and before["total_bytes"]==after["total_bytes"]==147731
finite=[];archive=[]
for mode in ["normal","O","OO"]:
 for kind,dest in [("finite",finite),("archive",archive)]:
  v=json.loads((R/f"receipts/{kind}_{mode}_launch.json").read_text()); assert v["returncode"]==0 and v["stderr"]==""
  d=json.loads(v["stdout"]);d.pop("utc");d.pop("optimization");dest.append(d)
assert finite[0]==finite[1]==finite[2] and archive[0]==archive[1]==archive[2]
assert len(archive[0]["observations"])==31 and all(v["accepted"]==v["expected_accept"] for v in archive[0]["observations"])
out={"utc":datetime.datetime.now(datetime.timezone.utc).isoformat(),"all_root_raw_receipt_checks_passed":True,"actual_baseline":baseline_summary,"new_commands":409,"modes":mode_counts,"outer_cli_negatives":22,"independent_new_finite_modes_equal":True,"archive31_observations_modes_equal":True,"all26_original_before_after_equal":True,"historical_runtime":"NOT_REPRODUCED; actualPython3.14.6/UID501","original_write_denial":"NOT_REPRODUCED; no original mutation/writeprobe","deep_json_optional_defect_independently_root_reproduced":"root_execution_checks/ROOT_NESTED_JSON_REPRODUCTION.json"}
(A/"ROOT_COMPUTATIONAL_RAW_RECEIPT_CHECKS.json").write_text(json.dumps(out,indent=2)+"\n"); print(json.dumps(out,indent=2))
