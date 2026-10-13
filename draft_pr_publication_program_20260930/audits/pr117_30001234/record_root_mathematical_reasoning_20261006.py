"""Record root's completed reasoning and actually rehash read source artifacts."""
from pathlib import Path
import hashlib,json,os,datetime
A=Path(__file__).resolve().parent
def pin(p):
    b=p.read_bytes()
    return {"path":str(p.relative_to(A)),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
F=A/"original_head_authentication_20261006"
auth=json.loads((F/"ORIGINAL_AUTHENTICATION.json").read_text())
for e in auth["original_files"]:
    got=pin(F/"original_attempt"/e["path"])
    if (got["bytes"],got["sha256"])!=(e["bytes"],e["sha256"]):raise ValueError("Original changed")
scope=A/"primary_source_scope_adversary_20261006"
retrieval=json.loads((scope/"RETRIEVAL_RECEIPT.json").read_text())
sourcepins=[]
for e in retrieval["sources"]:
    p=scope/"private_sources"/e["name"]
    got=pin(p)
    if (got["bytes"],got["sha256"])!=(e["byte_count"],e["sha256"]):raise ValueError("Source changed")
    sourcepins.append({**got,"requested_url":e["requested_url"],"final_url":e["final_url"]})
visualnames=["owr21_2009_physical_p37.png","owr21_2009_physical_p38.png","owr21_2009_physical_p39.png","shibuta_takagi_0810.1278v3_physical_p6.png","shibuta_takagi_0810.1278v3_physical_p8.png"]
visualpins=[pin(scope/"private_renders"/n) for n in visualnames]
prior=json.loads((F/"PRIOR_REPORT.json").read_text())
if prior!={}:raise ValueError("Unexpected prior")
utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
record={
"schema":"pr117-root-mathematical-reasoning/v1","UTC":utc,"actual_operator_PID":os.getpid(),
"PR":117,"problem_id":30001234,"immutable_head":auth["original_head"],"original_attempt_budget":"1/5",
"candidate":pin(F/"original_attempt/CANDIDATE.md"),"all_original_20_files_unchanged":True,
"claim":"For the specified minimal cyclic generating set of the generic 2x3-minor ideal, no rational optimum of the exact original augmented LP has a singleton image fiber.",
"source_scope":{
"ring":"Characteristic-zero polynomial ring k[x1,x2,x3,y1,y2,y3], coefficients gamma_i=1 and nonzero integral exponent vectors.",
"operative_target":"OWR21/2009 Proposition5 and Question8; Shibuta-Takagi0810.1278v3 Proposition2.1 and Question2.2.",
"quantifiers":"There exists one rational optimizer z whose image differs from the image of every distinct rational optimizer. To negate it, every optimizer must have a distinct optimizer with equal image.",
"bounds":"Az<=1, nonnegative rational variables; bottom rows (I3 I3) retained.",
"positive_theorem_restrictions":"Regular sequence and space monomial curve assumptions belong to positive sufficient theorems, not the general question.",
"root_visually_read_actual_renders":visualpins,
"root_extracted_text_read":"Complete Takagi contribution printed1136-1139; ST Prop2.1 full proof, Question2.2, Theorem2.4 statement and Example3.2.",
"example3_2_boundary":"One bad optimizer in Example3.2 does not answer the existential question negatively; that source also supplies a good optimizer."
},
"unrestricted_proofs":[
{"claim":"No nonzero monomial belongs to the polynomial ideal.","proof":"Evaluation of all six variables at1 kills every generator and sends any nonzero scalar multiple of a monomial to that scalar. Membership is therefore impossible."},
{"claim":"Three generators are minimal globally and at the homogeneous maximal ideal.","proof":"The ideal is homogeneous generated in degree2. The six quadratic supports are disjoint, so its three displayed degree2 elements are k-linearly independent. They form a basis of I/mI: higher-degree elements are in mI. Localization at m preserves this vector-space dimension by Nakayama, so at least three generators are necessary."},
{"claim":"The ideal equals the prime Segre kernel; primeness is optional for the source.","proof":"Under xi->szi, yi->tzi, two monomials have equal images exactly if their three column totals and total x degree agree. If their x allocations differ, choose excess j and deficit i. The first monomial is divisible by xj yi. Exchanging it for xi yj uses one of the signed minors and decreases allocation L1 distance by2. Induction joins every image fiber. Grouping a polynomial by image monomials, coefficients in each fiber sum to zero, so each group is a linear combination of differences from a fixed representative and lies in I. Thus kernel=I. The image is a subring of a domain."},
{"claim":"Localizing at m introduces no monomial; inverting a variable changes minimality.","proof":"The prime I is contained in m, hence I S_m contracts to I, so monomial exclusion persists at m. By contrast x3 f1+x1 f2+x2 f3=0 makes f3 redundant when x2 is inverted. A Laurent-ring interpretation would require new minimality analysis, but is not the source question."},
{"claim":"The objective maximum is3 and all rational optimizers have a common image.","proof":"The bottom three inequalities imply sum_i(mu_i+nu_i)<=3. The two endpoints, and every z(t)=(t,t,t,1-t,1-t,1-t), rational0<=t<=1, have image1_9, attaining3. At any optimum each bottom cap equals1, so nu_i=1-mu_i. The first three top inequalities force mu1<=mu3<=mu2<=mu1, hence all equal t. Nonnegativity forces0<=t<=1. This proves the full optimal set, not just a sampled subset."},
{"claim":"Every optimum has a distinct rational partner, including endpoints.","proof":"For t!=0 choose t'=0; for t=0 choose t'=1. This distinct rational point is optimal and has identical image1_9. The source condition therefore fails for every optimizer."},
{"claim":"The exact kernel has dimension1 and rank5.","proof":"Bottom homogeneous equations give dnu_i=-dmu_i; cyclic top equations force all dmu_i equal. Therefore ker A=Q(1,1,1,-1,-1,-1). A is9x6 so rank5."},
{"claim":"Equal augmented image of any feasible point implies equal objective.","proof":"The objective is the sum of the last three image coordinates. Thus any feasible same-image point to an optimizer is automatically an optimizer; feasible-fiber and optimal-fiber singleton formulations agree here."}
],
"diagnostics":{
"original_normal_reproduction":pin(A/"ROOT_ORIGINAL_CHECKER_REPRODUCTION_20261006.json"),
"effective_guard_validation":pin(A/"ROOT_EFFECTIVE_GUARD_VALIDATION_20261006.json"),
"guard_repair":"Original assertion-based checkers are cleared only in normal mode. Effective diagnostic copies replace only ck assertions with explicit exceptions. Normal/-O output semantics agree with original JSON except verifier hash. False controls reject in both effective modes.",
"written_proof_is_authority":"Finite exact arithmetic, vertices and monomial straightening controls supplement rather than establish the unrestricted proofs."
},
"source_pins":sourcepins,"full_native_prior_report":prior,"new_central_proof_search_turns":0,
"root_individual_math_assessment":"PASS","root_cross_family_mathematical_gate":"Pending sealed reports and full root authentication/reproduction.",
"priority_clearance":False,"preprint_readiness":False,"service_or_native_mutations":False,
"best_guess_math_source_completion_percent":90,"best_guess_pr_workflow_completion_percent":20,
"program_completed":19,"dated_eligible_baseline":99,"goal_active":True
}
out=A/"ROOT_MATHEMATICAL_REASONING_20261006.json"
out.write_text(json.dumps(record,indent=2,sort_keys=True)+"\n")
with (A/"RESEARCH_LOG.md").open("a") as f:
 f.write("\n"+utc+": Root independently verified exact source quantifiers, polynomial hypotheses, all-degree Segre argument, graded minimality, full rational optimal face and every endpoint fiber. All20 originals unchanged. Original normal diagnostics reproduce exactly; separate guard-only repair passes normal/-O with false-control rejection. Three distinct families report preliminary PASS and are sealing; cross-family mathematical gate pending. No priority clearance, paper or remote mutation. Best guess math/source90%; PR workflow20%; program19/99=19.19%; goal active. Source bodies/renders private excluded. Main/index writer remains released to other chat.\n")
print(json.dumps({"status":"RECORDED","actual_PID":os.getpid(),"UTC":utc,"output":pin(out),"private_source_count":len(sourcepins),"root_actual_visually_inspected_renders":len(visualpins),"priority_clearance":False}))

