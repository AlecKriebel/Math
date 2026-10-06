#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,datetime,os,sys
D=Path(__file__).resolve().parent; A=D.parent
def pin(path):
    p=Path(path)
    if p.is_symlink() or not p.is_file(): raise ValueError(str(p))
    h=hashlib.sha256()
    with p.open("rb") as stream:
        for chunk in iter(lambda:stream.read(1024*1024),b""):h.update(chunk)
    return {"path":str(p),"bytes":p.stat().st_size,"sha256":h.hexdigest()}
inputs=[A/"ROOT_MATHEMATICAL_GATE_20261006.json",
 A/"original_head_authentication_20261006/original_attempt/source_record.json",
 A/"original_head_authentication_20261006/original_attempt/prior_imported_report.json",
 A/"original_head_authentication_20261006/original_attempt/PROOF.md",
 A/"original_head_authentication_20261006/POLICY_AGENTS.md",
 A/"original_head_authentication_20261006/POLICY_unsolved_math_prioritization_AGENTS.md",
 A/"PRIMARY_SOURCE_DOWNLOAD_PINS_20261006.json",
 A/"primary_sources_private/reznik_garcia_koiller_arxiv_v11.pdf",
 A/"primary_sources_private/reznik_garcia_koiller_published2021.pdf",
 Path("/Users/alec/.codex/plugins/cache/openai-primary-runtime/pdf/26.904.11930/skills/pdf/SKILL.md")]
pins=[pin(p) for p in inputs]
if pins[3]["sha256"]!="8478d2a792944c5fb9e8a53324e0c6bce8eba317de29c31a6fcbd6ca0205709d": raise ValueError("original proof mismatch")
gate=json.loads(inputs[0].read_text())
if gate["original_head"]!="3d159f0a00d0bd7ff8d558d6fbc75af5094f7a35" or not gate["mathematical_clearance"]:raise ValueError("mathematical gate")
if not json.loads(inputs[2].read_text()):raise ValueError("empty prior")
if pins[7]["sha256"]!="c56bb4ea29734ed04ee153206bb8619286df544714fd3f77fe97bdc945dfe1da":raise ValueError("arxiv source")
if pins[8]["sha256"]!="c2a2e644521fd03a15833a23bd57c2498b5644036f6bc8fe682c40581f640d42":raise ValueError("published source")
sources=[
("ivory_1610.01384.pdf","https://arxiv.org/pdf/1610.01384","ivory_download","Author preprint v2, 51pp; complete relevant §§2.1–2.2 and3.3.4–3.3.5 read; entire remainder not claimed read."),
("bicentric_published2021.pdf","https://amj.math.stonybrook.edu/pdf-Springer-final/021-0188.pdf","bicentric_download","Complete Theorem2 proof, Corollary1, definitions and AppendicesA–C; Fig4 and Lemmas2–3 visually checked."),
("chasles1828.pdf","https://www.numdam.org/article/AMPA_1827-1828__18__269_1.pdf","chasles1828_download","Complete pp269–276 read; relevant pp272,275–276 visually checked."),
("darboux1879.pdf","https://www.numdam.org/item/BSMA_1879_2_3_1_64_1.pdf","darboux1879_download","Complete pp64–72 read; sign correction pp64–65 visually checked."),
("bricard1908.pdf","https://www.numdam.org/item/NAM_1908_4_8__317_1.pdf","bricard1908_download","Complete pp317–330 read, including reproduced Darboux statement and new elementary proof."),
("negative_pedal_gheorghe2022.pdf","https://ijgeometry.com/wp-content/uploads/2022/01/1.-5-16.pdf","negative_pedal_download","Complete relevant §§2–4 definitions/propositions/proofs read; p7 visually checked."),
("salmon_higher_plane_curves1879.pdf","https://upload.wikimedia.org/wikipedia/commons/3/32/A_treatise_on_the_higher_plane_curves-_intended_as_a_sequel_to_A_treatise_on_conic_sections_%28IA_treatisehigherpl00salmrich%29.pdf","salmon1879_download","Third edition1879; title and complete Arts121–122/examples pp105–107 read; all three relevant pages visually checked."),
("chasles1828_errata.pdf","https://www.numdam.org/item/AMPA_1827-1828__18__386_0.pdf","chasles_errata_download","Complete pp386–387 read; p386 visual read confirms both-foci correction.")
]
registry=[]
for name,url,label,coverage in sources:
    record=pin(D/"private_sources"/name); record["url"]=url;record["read_coverage"]=coverage
    receipt=json.loads((D/"actual_operations"/label/"execution.json").read_text())
    if receipt["exit_code"]!=0:raise ValueError("download failed")
    record["actual_download_PID"]=receipt["child_PID"];record["actual_download_start_UTC"]=receipt["UTC_start"]
    registry.append(record)
private=[]
for prefix in ["private_sources","private_review_materials"]:
    for p in sorted((D/prefix).rglob("*")):
        if p.is_file():
            r=pin(p);r["relative_path"]=p.relative_to(D).as_posix();private.append(r)
operations=[]
for p in sorted((D/"actual_operations").glob("*/execution.json")):
    r=json.loads(p.read_text());base=p.parent
    for key in ["stdout","stderr"]:
        q=pin(base/r[key]["path"])
        if q["bytes"]!=r[key]["bytes"] or q["sha256"]!=r[key]["sha256"]:raise ValueError("stream mismatch")
    if r["exit_code"]!=0:raise ValueError("prior subprocess failed")
    operations.append({"receipt":p.relative_to(D).as_posix(),"actual_PID":r["child_PID"],"exit_code":r["exit_code"]})
for label,pid,optimization in [("quantity_controls_normal",21078,0),("quantity_controls_optimized",21077,1)]:
    value=json.loads((D/"actual_operations"/label/"stdout.bin").read_text())
    if value["actual_operator_PID"]!=pid or value["checks"]!=41 or value["optimization"]!=optimization:raise ValueError("controls")
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(name,value):(D/name).write_text(json.dumps(value,indent=2,sort_keys=True)+"\n")
write("INPUT_AUTHENTICATION.json",{"schema":"pr110-classical-priority-inputs/v1","UTC":now,"actual_operator_PID":os.getpid(),"inputs":pins,"original_prior_nonempty":True,"source_gate_authentic":True,"independent_report_scope":"Only original source/claim/proof and root mathematical gate; no other fresh priority reports."})
write("PRIVATE_SOURCE_CUSTODY.json",{"schema":"pr110-classical-priority-private-custody/v1","UTC":now,"actual_operator_PID":os.getpid(),"sources":registry,"private_files":private,"copyrighted_bodies_redistributed":False,"public_prefix_exclusions":["private_sources/","private_review_materials/"]})
write("ACTUAL_PROCESS_AUTHENTICATION.json",{"schema":"pr110-classical-priority-subprocess-authentication/v1","UTC":now,"actual_operator_PID":os.getpid(),"actual_completed_operations":operations,"normal_and_optimized_checks_each":41,"finite_controls_are_not_novelty_proof":True})
write("RESEARCH_LOG.json",{"schema":"pr110-classical-priority-research-log/v1","UTC_checkpoint":now,"actual_checkpoint_writer_PID":os.getpid(),"completion_percent":100,"family_only":True,"findings":["Primary classical closure/perimeter/polar/negative-pedal results do not supply literal focal antipedal sum equality.","Negative-pedal = polar(inverse) is old background, not a new construction.","Even centrally symmetric subcase is old; general odd-primitive component remains substantive relative to inspected corpus.","Forty-one exact quantity controls completed in normal and optimized modes.","Lockwood1957 full text explicitly unread; no identified essential covering theorem gap."],"new_central_proof_search_turns":0,"no_outreach":True,"no_git_index_mutation":True,"combined_priority_clearance":False,"publication_ready":False})
print(json.dumps({"actual_operator_PID":os.getpid(),"inputs_authenticated":len(pins),"primary_downloads":len(registry),"private_files_pinned":len(private),"prior_completed_operations":len(operations),"family_completion_percent":100}))

