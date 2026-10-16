"""MIT licensed. Manuscript/source-binding consistency, not mathematical proof."""
import hashlib,json,pathlib,re,stat
root=pathlib.Path(__file__).resolve().parent
status=json.loads((root/"STATUS.json").read_bytes())
meta=json.loads((root/"ZENODO_METADATA_DRAFT.json").read_bytes())
bindings=json.loads((root/"BINDINGS.json").read_bytes())
tex=(root/"integer_endpoint_discontinuity.tex").read_text()
assert status["scientific_disposition"]=="claimed_solved"
assert status["substantive_proof_attempts"]==1 and status["budget"]==5
assert status["audit_turn_increment"]==0 and status["submission_ready"] is False
assert status["human_peer_reviewed"] is False and status["manuscript_compiled"] is False
assert meta["creators"]==[{"name":"Kriebel, Alec","orcid":"0009-0001-9320-500X"}]
assert meta["license"]=="cc-by-4.0" and "doi" not in meta and "publication_date" not in meta
labels=set(re.findall(r"\\label\{([^}]+)\}",tex))
refs=set(re.findall(r"\\(?:eqref|ref)\{([^}]+)\}",tex))
assert refs<=labels, sorted(refs-labels)
bib=set(re.findall(r"\\bibitem\{([^}]+)\}",tex))
cites=set()
for c in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}",tex): cites.update(c.split(","))
assert cites<=bib, sorted(cites-bib)
for s in [r"A=HH^{\mathsf T}",r"B^i=-H_{ia}",r"K>4C_0",
          r"\partial_x^{r+1}(f-\id)(0)=-(r+1)!",r"3 January 2018",
          r"Extensive",r"unrefereed",r"indirect"]:
    if s==r"Extensive": assert "extensive AI assistance" in tex
    else: assert s in tex,s
assert len(bindings["original_science"])==17
for e in bindings["original_science"]+bindings["audited_in_place"]:
    p=pathlib.Path(e["path"]); body=p.read_bytes()
    assert len(body)==e["bytes"] and hashlib.sha256(body).hexdigest()==e["sha256"],e["path"]
    assert stat.S_IMODE(p.stat().st_mode)==int(e["full_mode_07777"],8),e["path"]
assert bindings["head"]=="4ecc453d6f9ec2e64cdb2d4b41c018fffbe85b29"
print(json.dumps({"status":"PASS_PREPARATION_CONSISTENCY_ONLY","original_objects":17,
 "latex_bytes":len(tex.encode()),"latex_labels":len(labels),"bibliography_keys":sorted(bib),
 "universal_mathematical_test":False,"compiler":False,"new_independent_review":False,
 "ROOT_helpers_executed":False,"submission_ready":False},sort_keys=True))
