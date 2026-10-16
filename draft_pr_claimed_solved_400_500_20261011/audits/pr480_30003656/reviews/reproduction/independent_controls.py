#!/usr/bin/env python3
"""Independent extensional finite semantics and actual executable mutations.

No unbounded theorem, formal proof, or historical priority is certified.
"""
import itertools as it
import json
from pathlib import Path
import importlib.util
from replay import HERE, SOURCE, run, sha, utc, check_manifests

def require(condition, label):
    if not condition:
        raise RuntimeError(label)

def arrows(bound, injective):
    # Deliberately construct both categories by Cartesian products + filters.
    result = {}
    for size in range(1,bound+1):
        result[size] = [(target,(0,)+tail)
                        for target in range(1,bound+1)
                        for tail in it.product(range(target),repeat=size-1)
                        if not injective or len(set((0,)+tail))==size]
    return result

def negate_fibers(category, fibers):
    # Complement in the lattice of natural subobjects of the carrier functor.
    return {size: {a for a in range(size)
                   if all(f[a] not in fibers[target] for target,f in row)}
            for size,row in category.items()}

def finite_lattice_controls():
    rows = []
    compositions = 0
    source_result = json.loads((SOURCE/"exact_results.json").read_text())
    for bound in range(1,6):
        for inj in [False,True]:
            category = arrows(bound,inj)
            lookup = {(s,t):set(f for target,f in row if target==t)
                      for s,row in category.items() for t in category}
            for s,row in category.items():
                require(tuple(range(s)) in lookup[s,s],"missing identity")
                for t,f in row:
                    require(f[0]==0 and len(f)==s and all(0<=a<t for a in f),"invalid map")
                    for u,g in category[t]:
                        require(tuple(g[a] for a in f) in lookup[s,u],"category not closed")
                        compositions += 1
            equality = {size:{0} for size in category}
            ne = negate_fibers(category,equality)
            nne = negate_fibers(category,ne)
            beta = {size:all(nne[t]==set(range(t)) for t,f in row)
                    for size,row in category.items()}
            alpha = {size:all(not beta[t] for t,f in row)
                     for size,row in category.items()}
            decidable = {size:all(equality[t]|ne[t]==set(range(t)) for t,f in row)
                         for size,row in category.items()}
            actual = [{"stage_n":s-1,"beta":beta[s],"alpha":alpha[s],
                       "exists_nonbasepoint":bool(ne[s]),"decidable_basepoint":decidable[s]}
                      for s in category]
            if bound==5:
                expected = source_result["pointed_injections" if inj else "all_pointed_maps"]
                require(actual==expected["rows"],"source row mismatch")
                require(sum(map(len,category.values()))==expected["arrows"],"arrow count mismatch")
            rows.append({"bound_cardinality":bound,"injective":inj,
                         "map_count":sum(map(len,category.values())),"rows":actual,
                         "negation_fibers":{str(s):sorted(ne[s]) for s in category},
                         "double_negation_fibers":{str(s):sorted(nne[s]) for s in category}})
    # Universal cardinality cutoffs are true in a truncation yet refuted by one
    # explicitly larger object. This is an artifact demonstration, not a claim
    # that the target alpha itself is incorrect.
    truncations=[]
    for bound in range(1,6):
        checked=0
        for size in range(1,bound+1):
            for values in it.product(range(size),repeat=bound+1):
                require(len(set(values))<len(values),"pigeonhole control unexpectedly false")
                checked+=1
        distinct=tuple(range(bound+1))
        require(len(set(distinct))==len(distinct),"larger-stage countertuple invalid")
        truncations.append({"bound":bound,"formula":"forall x0..xK, OR_(i<j)(xi=xj), K=bound",
                            "truncated_valuations_checked":checked,
                            "truncated_universal_true":True,
                            "next_stage_cardinality":bound+1,"next_stage_countertuple":distinct,
                            "next_stage_universal_false":True})
    return {"rows":rows,"composition_checks":compositions,
            "truncation_artifact_controls":truncations}

def mutation_controls():
    original = (SOURCE/"audit/audit_controls.py").read_text()
    mutations = {
        "pointwise_universal":("successors = [(size,tuple(range(size)))] if pointwise_all else arrows[size]",
                                 "successors = [(size,tuple(range(size)))]"),
        "alpha_as_current_existential":("EXTRA = ('E',neg(eq(0,-1)))",
                                          "EXTRA = ('E',neg(eq(0,-1)))\nALPHA = EXTRA"),
        "drop_double_negation":("BETA = ('A',neg(neg(eq(0,-1))))","BETA = ('A',eq(0,-1))"),
        "remove_all_transition_maps":("if discrete:","if True:"),
        "injections_used_for_generic":("for f in maps(s,t,injective)]","for f in maps(s,t,True)]"),
        "omit_growth":("    @lru_cache(None)",
                        "    arrows = {s: [(t,f) for t,f in row if t <= s] for s,row in arrows.items()}\n    @lru_cache(None)"),
        "postulate_classical_validity":("    for label,killed in mutations.items():",
                                          "    check('alpha_classically_valid',discrete(ALPHA,1))\n    for label,killed in mutations.items():")
    }
    receipts=[]
    for label,(old,new) in mutations.items():
        require(original.count(old)==1,"mutation target ambiguous: "+label)
        folder = HERE/"mutations"/label
        folder.mkdir(parents=True,exist_ok=True)
        program = folder/"audit_controls.py"
        program.write_text(original.replace(old,new))
        for optimized in [False,True]:
            receipt = run(label+("_optimized" if optimized else "_normal"),program,optimized)
            require(receipt["returncode"]!=0,"audit failed to reject mutation: "+label)
            stderr = (HERE/receipt["stderr_path"]).read_text()
            require("AssertionError" in stderr,"mutation failed for unrelated reason: "+label)
            receipt["failed_assertion"] = stderr.strip().splitlines()[-1]
            receipt["mutation_rejected"] = True
            receipts.append(receipt)
    # The author's uses of Python assert disappear under -O. Demonstrate a
    # semantic error that then nevertheless returns PASS, rather than merely
    # relying on documentation of Python behavior.
    author = (SOURCE/"check_exact.py").read_text()
    old="    arrows = category(injective)"
    require(author.count(old)==1,"author mutation target ambiguous")
    mutant=author.replace(old,"    arrows = {n: [(n,tuple(range(n+1)))] for n in range(MAX_N+1)}")
    folder = HERE/"mutations/author_discrete_category"
    folder.mkdir(parents=True,exist_ok=True)
    program=folder/"check_exact.py"
    program.write_text(mutant)
    normal=run("author_discrete_normal",program,False)
    optimized=run("author_discrete_optimized",program,True)
    require(normal["returncode"]!=0,"author normal mode failed to reject mutation")
    require(optimized["returncode"]==0,"author optimized false-PASS demonstration failed")
    invalid=json.loads((folder/"exact_results.json").read_text())
    require(invalid["status"]=="PASS" and invalid["all_pointed_maps"]["rows"][1]["beta"]==False,
            "optimized author mutation did not expose false PASS")
    return {"audit_mutation_runs":receipts,"all_fourteen_rejected":True,
            "author_assertion_stripping":{"normal":normal,"optimized":optimized,
                                           "wrong_output_still_reports_PASS":True,
                                           "wrong_output_sha256":sha(folder/"exact_results.json")}}

def certificate_boundary():
    # Existing verifier trusts the supplied equality closure; it is a local
    # witness consistency check, not a trusted derivation kernel for E.
    spec=importlib.util.spec_from_file_location("frozen_audit_controls",SOURCE/"audit/audit_controls.py")
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    phi=module.eq(0,1)
    honest_relation,q,roots=module.closure(3,[])
    forged_relation=[[True]*3 for _ in range(3)]
    proof=("equality",1,2)
    honest=module.verify_proof(phi,proof,honest_relation)
    forged=module.verify_proof(phi,proof,forged_relation)
    require(not honest and forged,"certificate boundary control unexpected")
    malformed_raises=None
    try:
        module.verify_proof(("&",module.T),(),honest_relation)
    except (IndexError,TypeError) as error:
        malformed_raises=type(error).__name__
    require(malformed_raises is not None,"malformed-proof boundary changed")
    return {"honest_empty_premise_rejects_unrelated_equality":not honest,
            "supplied_forged_relation_is_trusted":forged,
            "malformed_certificate_raises":malformed_raises,
            "meaning":"A finite verifier over precomputed Erel, not a self-contained proof kernel."}

def main():
    before=check_manifests()
    receipt={"started_utc":utc(),"scope":"finite computational evidence only",
             "completion_estimate_percent":85,"source_hash_checks":len(before),
             "lattice_controls":finite_lattice_controls(),
             "mutation_controls":mutation_controls(),
             "certificate_boundary":certificate_boundary(),
             "finished_utc":utc(),"frozen_source_preserved":check_manifests()==before}
    (HERE/"independent_controls_receipt.json").write_text(json.dumps(receipt,indent=2)+"\n")
    print(json.dumps({"finished_utc":receipt["finished_utc"],
                      "composition_checks":receipt["lattice_controls"]["composition_checks"],
                      "audit_mutants_rejected":14,"author_optimized_false_PASS_demonstrated":True,
                      "frozen_source_preserved":receipt["frozen_source_preserved"]},indent=2))

if __name__=="__main__": main()
