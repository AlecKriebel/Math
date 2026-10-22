"""Write authored-claim classifications; does not run any PR-delivered code."""
import collections
import datetime
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROGRAM = HERE.parents[1]
INTAKE = PROGRAM / "intake"

def evidence(n, name, a=None, b=None, role="claim_and_boundary"):
    path = HERE / "inputs" / f"pr{n}" / name
    if not path.exists():
        path = INTAKE / f"pr{n}" / "artifacts" / name
    out = {"path": str(path), "role": role}
    if a is not None:
        out.update(start_line=a, end_line=b or a)
    return out

def record(n, classification, target, strongest, mechanism, boundaries, gap, ev,
           resolution_scope=None, negative=None, companions=None, scope_hold=False):
    p = json.loads((INTAKE / f"pr{n}" / "pr.json").read_text())
    pins = json.loads((INTAKE / f"pr{n}" / "PINS.json").read_text())
    return {
        "pr": n, "problem_id": pins["problem_id"], "title": p["title"],
        "url": p["url"], "head_oid": p["headRefOid"], "state": p["state"],
        "is_draft": p["isDraft"], "classification": classification,
        "original_target_as_stated_in_authored_artifacts": target,
        "strongest_asserted_result": strongest,
        "mechanism": mechanism, "quantifiers_and_boundaries": boundaries,
        "asserted_full_resolution_scope": resolution_scope,
        "new_unqualified_original_resolution_claimed": False,
        "novelty_certified_by_this_review": False,
        "literal_or_subquestion_negative_claims": negative or [],
        "bundled_companions": companions or [], "exact_remaining_gap": gap,
        "requires_scope_reconciliation_before_exclusion": scope_hold,
        "evidence": ev + [{"path": str(INTAKE / f"pr{n}" / "pr.json"),
                           "json_field": "body", "role": "PR_authored_claim_and_disposition"}],
        "queue_status_used_for_decision": False,
        "mathematical_truth_audit_performed": False,
        "independent_priority_audit_performed": False,
        "delivered_code_executed": False,
    }

rows = [
    record(1000, "PRIOR_CREDITED_LITERAL_NEGATIVE",
        "Motion groups of links associated to forests/trees versus symmetric automorphism subgroups of their RAAGs, using the full smooth unordered/unoriented R^3 quotient.",
        "For the single-edge tree K2 and standard Hopf link H, pi1(E(H))=Q8 is not isomorphic to any actual subgroup of Aut(A(K2))=GL2(Z); the literal universal identification is false. Dahm image V4, central kernel C2, nonsplit extension.",
        "Import the explicitly credited Boyd–Bregman smooth Q8 theorem, then average a faithful real representation into O(2) and use Q8's single involution to exclude an embedding. Endpoint rotations compute the Dahm image.",
        ["Single-edge tree is in the literal source scope.", "Full quotient forgets labels and orientations; R^3, not S^3.", "Automorphism means an actual subgroup of Aut(Z^2).", "Smooth topology is a prior imported theorem; finite group checks cannot prove it.", "Cover clarification: oriented-labelled connected cover has degree four and fundamental group C2; full decoration cover degree eight with two components."],
        "The literal universal subgroup identification is claimed fully refuted by a prior-known example. The intended revised conjecture and general connected-forest motion-group computation remain unresolved.",
        [evidence(1000,"original/PROOF_APPLICATION.md",5,23), evidence(1000,"original/PROOF_APPLICATION.md",29,51), evidence(1000,"original/PROOF_APPLICATION.md",79,96), evidence(1000,"ACCEPTANCE.md",3,7), evidence(1000,"SCOPE.json",14,30)],
        resolution_scope="Full negative answer to the literal universal automorphism-subgroup identification, explicitly prior credited; no original/new solution claim.",
        negative=[{"claim":"Literal universal motion-group/RAAG-subgroup isomorphism fails already for K2.","full_in_its_literal_scope":True,"prior_known_credit":True,"not_general_motion_group_computation":True}]),
    record(1001, "SCOPED_FULL_INTERPRETATION_HOLD",
        "Karpenkov Problem 4: which subgraphs of Kn define the same stratifications? The source does not separately define cross-graph sameness.",
        "For every n>=1 and d>=1 and simple graphs G,H on the same labelled [n], their full connected sign-equivalence partitions of (R^d)^n are equal iff E(G)=E(H). Includes collisions and deficient affine span. Under a specified label permutation, equality is equivalent to the corresponding graph relabelling.",
        "Detect a collapsed edge by singleton-support stress (Panina Lemma 4, credited); use positive diagonal stress transport along a collinear path with no H-edge collapse to put two configurations in one H-stratum while G separates them.",
        ["Full Cartesian configuration space; positive d and n.", "Equality is equality of collections of subsets of the same fixed-label space.", "Connected components, not merely endpoint fibre equivalence.", "No quotient by affine/Euclidean transformations, arbitrary ambient homeomorphisms, or abstract adjacency posets.", "The literal theorem is a full answer under its exact equality convention, not merely a low-codimension or collinear restricted theorem."],
        "The exact original question's cross-graph equivalence convention is unresolved. Arbitrary ambient-homeomorphism or abstract adjacency classification is not supplied. Novelty is not certified. Do not exclude this complete literal theorem merely because STATUS retains a hold; root must reconcile scope.",
        [evidence(1001,"REPORT.md",3,27), evidence(1001,"REPORT.md",31,70), evidence(1001,"REPORT.md",72,95), evidence(1001,"ACCEPTANCE.md",3,9), evidence(1001,"STATUS.json",2,13)],
        resolution_scope="Complete universal classification under literal full fixed-label partition equality; unqualified original interpretation remains on HOLD.", scope_hold=True),
    record(1002, "PARTIAL_UNRESOLVED",
        "Determine the restricted Iwahori Hecke module M(pi)=(Res_GL_n pi)^(I_H) for unramified generic GL_(n+1) representations, including parameter dependence and compatible Steinberg products.",
        "Known rank-two failure of parameter independence via Prasad 1993, plus rank-one regularity, Jordan/Fitting obstructions, six flag charts and a conditional lattice reduction.",
        "GL3 parameters 1⊕1⊕1 and xi⊕xi⊕xi have different trivial GL2 quotients; Bernstein projection and exact Iwahori invariants carry the distinction to Hecke modules. Elementary finite/rank-one analyses expose reconstruction gaps.",
        ["F non-Archimedean local; smooth complex representations.", "Unramified generic here means irreducible Whittaker-generic and spherical.", "Steinberg products use normalized parabolic products of unramified twists and are separate from finite Steinberg types.", "The generally infinite-dimensional module is not restriction of finite-dimensional pi^(I_G).", "Hom-to-trivial is a quotient, not a subrepresentation."],
        "No general H_n-module presentation, parameter-dependent extension/boundary gluing, or compatible Steinberg-product treatment. Five approaches exhausted.",
        [evidence(1002,"PARTIAL_ANALYSIS.md",3,36), evidence(1002,"PARTIAL_ANALYSIS.md",38,79), evidence(1002,"PARTIAL_ANALYSIS.md",208,217), evidence(1002,"ACCEPTANCE.md",3,12), evidence(1002,"STATUS.json",2,12)],
        negative=[{"claim":"Parameter independence fails already in rank two.","prior_known_credit":True,"credit":"Prasad 1993","only_subquestion_resolved":True}]),
    record(1003, "CREDITED_CONVENTION_CORRECTION_SOURCE_HOLD",
        "Exact application of OWR 28/2021 Theorem 1/Conjecture 2 to completion recursion for finite-area odd quadratic strata, including normalization and existence conditions.",
        "Authored convention correction q_a=2^(2a-1)b_a, product 2^(2G-h), reconciles sunflower conversions and reconstructs Q(5,3) special-star terms. Q(3,-1^3) correction pi^4/9, completed 2pi^4/3; Q(5,3) completed 73pi^6/420.",
        "Track quadratic versus abelian tautological top powers, coupled product volumes, imported intersection formulas, and explicit coefficient comparisons.",
        ["All odd m_i>=-1, sum=4g-4; finite area and non-square quadratic strata.", "n is even; prior DGY n>=3 means n>=4, and n=2 needs special-star terms.", "Original OWR coefficients are 2^h times DGY's; matching needs declared P_OWR=2^(-h)P_DGY.", "Stratum genus compatibility is not nonemptiness.", "This is an authored correction, not an author-issued erratum; zero new proof turns."],
        "OWR's mixed-product normalization and all-displayed-strata-exist versus empty-corrections-zero interpretation remain unresolved. Corrected broader formulas are not verified transcriptions of the exact OWR statement.",
        [evidence(1003,"REPORT.md",5,26), evidence(1003,"REPORT.md",42,44), evidence(1003,"REPORT.md",171,199), evidence(1003,"STATUS.json",3,35), evidence(1003,"README.md",3)],
        resolution_scope="Prior completion results and an authored convention repair; exact-source application explicitly remains on HOLD."),
    record(1004, "PARTIAL_UNRESOLVED",
        "Relationship of combinatorial mutations, cluster mutations and Escobar–Harada flips for higher Grassmannians beyond known two-plane/family results.",
        "Five boundary results: local min/max identity repair; nonconvex image of the unadjusted max map in specified Gr(3,6) coordinates; nonadditive prescribed Plucker-label transport; nonadjacency of fixed-labelled block cones; coherent hexagonal non-SAGBI test.",
        "Exact local algebra, monomial relation/rank comparisons, a midpoint separation certificate, and a degree-two Hilbert mismatch.",
        ["Cone toric degenerations require prime binomial initial ideals.", "EH comparison needs adjacent codimension-one cones, compatible full-rank valuations/common projection, and fixed lattice/grading conventions.", "Matching fields need coherence and all-degree SAGBI equality.", "Local HN display defect applies only to inspected arXiv v2; published 2023 body not inspected.", "Finite Hilbert agreement is not an all-degree SAGBI proof; no actual EH theorem counterexample claimed."],
        "No global characterization, arbitrary relevant adjacent-prime-cone coverage/coordinate-normalized map identification, or treatment of non-degree-one-generated valuation semigroups. Five approaches exhausted.",
        [evidence(1004,"REPORT.md",5,23), evidence(1004,"REPORT.md",25,47), evidence(1004,"REPORT.md",100,104), evidence(1004,"ACCEPTANCE.md",3,9), evidence(1004,"STATUS.json",2,11)]),
    record(1005, "CREDITED_PRIOR_STANDARD_RESOLUTION_SOURCE_HOLD",
        "Remove Jiang–Su stability from relative-absorption KK uniqueness in Gabe's OWR 36/2022 ideal/ambient formulation.",
        "Credited standard theorem: separable C, stable sigma-unital ideal D in E, ordinary multiplier-absorbing lambdaPhi/lambdaPsi agreeing modulo D: KK pair zero iff proper asymptotic conjugacy by norm-continuous u(t) in U(1+D), u(0)=1. A separate unital/unitally absorbing version for separable stable D omits initial-1 assertion.",
        "Application of Szabó's general uniqueness/K1-injectivity results, proper-path transfer, canonical multiplier action for nonessential extensions; separate credited unital bridge.",
        ["Pointwise-in-c norm asymptotic conjugacy; no Z-stability/nuclearity/UCT or essential-extension assumptions.", "Ordinary and unital absorption are distinct hypotheses.", "Unital version needs separable D and does not assert u(0)=1.", "Literal OWR relative absorption is undefined and ideal stability unstated.", "A stabilized path cannot simply be compressed to remove the stabilization."],
        "Exact relative-absorption convention/source bridge unresolved; no arbitrary nonstable-ideal theorem. The standard general resolution is explicitly attributed to Szabó, with zero new proof-search turns.",
        [evidence(1005,"PROOF_APPLICATION.md",3,19), evidence(1005,"PROOF_APPLICATION.md",68), evidence(1005,"PROOF_APPLICATION.md",169,178), evidence(1005,"ACCEPTANCE.md",3,7), evidence(1005,"STATUS.json",2,11)],
        resolution_scope="Complete credited standard stable-multiplier formulation; exact literal OWR scope remains on HOLD."),
    record(1006, "PARTIAL_UNRESOLVED",
        "A(K)=Arf(K) for every smooth concordance-torsion knot K, including identity; rational sliceness and algebraic torsion are different hypotheses.",
        "Additive-character reduction on T/(2T+Q), formal long-box obstruction/repair, literal figure-eight tensor-square maps, surgery nonadditivity, and a certified geometric two-torsion search family with missing involution computation.",
        "Reduce residual parity character; test formal involutive chain axioms, tensor descent, surgery correction terms, and known satellite families.",
        ["All smooth concordance torsion, not merely quasi-alternating torsion (already known).", "Formal complexes are not asserted knot-realizable.", "The long-box ansatz is not a classification of full involutions.", "Ordinary surgery invariants and general surgery additivity do not supply torsion involutive parity.", "Finite chain checks cannot decide unknown knots' smooth sliceness/concordance order."],
        "No universal vanishing/realizability/parity theorem or actual torsion-knot computation giving unequal A and Arf. Five approaches exhausted.",
        [evidence(1006,"REPORT.md",5,29), evidence(1006,"FORMAL_COMPLEX_AUDIT.md",3,27), evidence(1006,"FORMAL_COMPLEX_AUDIT.md",46,70), evidence(1006,"GEOMETRIC_ROUTE_AUDIT.md",18,28), evidence(1006,"GEOMETRIC_ROUTE_AUDIT.md",63,65), evidence(1006,"STATUS.json",9,21)]),
    record(1007, "CREDITED_PRIOR_COMPLETE_ORIGINAL",
        "Wild finite acyclic quiver over algebraically closed F admits a rational slope with positive denominator and uniform expansion families for all cutoffs delta in (0,1).",
        "Complete affirmative original target, explicitly already proved by Reineke's published Theorem 2.4 forward implication. A rational slope and one unbounded family work for every delta, with a positive gap depending on delta and uniform over the family.",
        "Attributed reconstruction of Reineke's spectral/incidence construction, integral rational slope choices, and extension by zero from a wild connected component.",
        ["Every algebraically closed characteristic; finite acyclic quivers, disconnected included via wild component.", "Exists slope; for each delta<1 exists epsilon>0, uniform across unbounded family and nonzero subrepresentations with kappa(U)<=delta*kappa(V).", "No uniform positive gap as delta tends to one.", "No arbitrary fields, oriented cycles, prescribed slopes or explicit matrices.", "Published converse not needed and not independently reconstructed here."],
        "No remaining bridge is asserted for the original target. The result is expressly credited prior work, not a new/full original contribution by this PR.",
        [evidence(1007,"PROOF_APPLICATION.md",5,29), evidence(1007,"PROOF_APPLICATION.md",198,208), evidence(1007,"ACCEPTANCE.md",3,5), evidence(1007,"STATUS.json",2,18)],
        resolution_scope="Complete original target, explicitly already proved by Markus Reineke; no novelty or new solution claim."),
    record(1008, "PARTIAL_MAIN_WITH_PRIOR_COMPLETE_COMPANION",
        "Main 30005923: positive determinant moments on a strict row ball uniformly in variable count g, not just matrix dimension N. Companion 30005922: fixed-parameter determinant covariance/stable-polynomial limit.",
        "Main: finite C(g,k,r,m) for fixed finite g,k, 0<=r<1, m>=0, uniformly over N and coefficient tuples in that fixed row ball. Companion: credited repaired fixed-parameter covariance on strict outer spectral radius and local uniformity on fixed-dimensional product row balls.",
        "Reconstruct Jury–van Rensburg–Roman proof with operator-valued norm, concentration, Parraud trace approximation, second-order free covariance and joint normal-family continuation; disclose seven repairs.",
        ["g,k and coefficient-size parameters finite and fixed.", "N-uniformity is claimed; g-uniformity is explicitly not proved.", "Exact centering restricted to positive/inverse-positive words; pure power/periodic rotation multiplicity retained.", "Strict row-contractive representations for stable-polynomial OWR Lemma 9.", "No optional sharp constant, monotonicity, unrestricted mixed-word theorem, full quotient theorem or entire-manuscript acceptance."],
        "No verified bound on C(g,k,r,1) as g varies. Fixed-dimensional compactness and estimates retain g. Main target remains HOLD_VARIABLE_COUNT_UNIFORMITY.",
        [evidence(1008,"FIXED_G_PROOF.md",3,32), evidence(1008,"FIXED_G_PROOF.md",101,105), evidence(1008,"FIXED_G_PROOF.md",177,193), evidence(1008,"PROOF_INTERFACE_ADDENDUM.md",13,33), evidence(1008,"ACCEPTANCE.md",3,9), evidence(1008,"STATUS.json",2,21)],
        companions=[{"problem_id":30005922,"classification":"CREDITED_PRIOR_FIXED_PARAMETER_RESOLUTION_WITH_REPAIRS","novel_claim":False,"remaining_main_target_gap":"Does not give the all-g constant needed by 30005923."}]),
    record(1009, "PARTIAL_UNRESOLVED",
        "Rational Riemann selection and general (possibly small-data) BV Cauchy theory for hysteretic HLWR/HARZ traffic systems with switching.",
        "Conditional global common-scanning-band construction, velocity TVD/first-order contact effect, constitutive closure obstruction, common C2 entropy obstruction, and local flat-scanning rational waves/nonuniform BV propagation for 0<t<=1.",
        "Scalar frozen-parameter transport on a safe band, exact interaction calculation, thin-memory-pulse constitutive example, entropy PDE obstruction, and local resonance profiles.",
        ["Source specifies no smallness norm/reference state/hyperbolicity constant; these must be declared.", "Global scanning construction assumes coherent compact common band, positive slope, and separation from switching boundaries.", "Jump endpoints alone omit smooth and diffuse/Cantor memory conditions.", "Thin pulse is not a sequence of conservative PDE solutions.", "Wavewise profiles do not construct one global viscous approximating sequence; C2 entropy obstruction is scope restricted."],
        "Coherent general switching formulation, uniform full-state BV estimates/continuation, source-compatible memory closure through jumps/diffuse/Cantor parts, and global viscous approximants are missing. Five approaches exhausted.",
        [evidence(1009,"REPORT.md",3,17), evidence(1009,"REPORT.md",80), evidence(1009,"REPORT.md",99,110), evidence(1009,"REPORT.md",410,420), evidence(1009,"ACCEPTANCE.md",3,9), evidence(1009,"STATUS.json",10,25)]),
    record(1010, "PARTIAL_UNRESOLVED",
        "For every infinite finite-rank Coxeter group W, does some finite-index subgroup of Aut(W) surject onto an infinite Coxeter group?",
        "Invariant-kernel quotient sufficient conditions, finite-centralizer overlap bound, surjective direct-factor reduction, nonhomomorphic conjugator/retraction obstruction, and a standard reflection-implementation obstruction.",
        "Clique-conjugating finite-index subgroup preserves certain normal closures; finite-Out quotient lifting and finite centralizer counting cover special families; direct factors reduce to irreducibles; two routes are falsified.",
        ["Finite-edge graph retains label 2; absent edge means infinity.", "Invariant quotient must remain infinite with finite Out; this is not universal.", "Overlap criterion requires connected spanning tree with finite overlap centralizers.", "Direct-factor restriction must be onto full factor automorphism group, not just a finite-index image.", "Counterexamples to retractions/orthogonal implementation are not counterexamples to the abstract quotient conjecture."],
        "Infinite irreducible groups with infinite Out remain; no universal invariant infinite finite-Out quotient, no control of infinite overlap centralizers, and no alternative universal genuine epimorphism. Five approaches exhausted.",
        [evidence(1010,"01_equivariant_quotients.md",5,25), evidence(1010,"01_equivariant_quotients.md",49,51), evidence(1010,"02_clique_overlap_rigidity.md",9,19), evidence(1010,"03_direct_factor_reduction.md",5,35), evidence(1010,"04_conjugator_cocycle_obstruction.md",5,17), evidence(1010,"05_standard_representation_obstruction.md",5,21), evidence(1010,"STATUS.json",10,26)]),
    record(1011, "PARTIAL_UNRESOLVED",
        "For every degree d>=2 monic polynomial with marked fixed point 0 and |P'(0)|>=1, extend external-ray rotation uniquely and continuously, with multiplier-angle value at neutral boundary, without a connected Julia assumption.",
        "Generalized-ray rotation continuous on strictly repelling marked locus; smooth-ray domain dense and any continuous extension unique; connected-Julia neutral-boundary limit; exact multiplier-argument-shortcut obstruction.",
        "Positive-potential persistence, compact monotone degree-one extensions and rotation continuity; normalized invariant-Beltrami wringing for density; connected-Julia multiplier estimate.",
        ["Coefficient topology; fixed point always 0; degree d>=2.", "Source allows disconnected Julia sets.", "Ordinary smooth rays versus canonical generalized left/right continuations distinguished.", "Finite rotation formula requires cyclic-order-preserving permutation.", "No assumed smooth ray at singleton component, or rationality of repelling rotation."],
        "For P_j strictly repelling converging to any neutral P, show rho(P_j) tends to multiplier angle without connectedness/nondegenerate component/rationality or angle separation; also match every initially accessible indifferent point. Five approaches exhausted.",
        [evidence(1011,"RESULT.md",5,23), evidence(1011,"RESULT.md",150), evidence(1011,"RESULT.md",194,207), evidence(1011,"STATUS.json",9,20)]),
    record(1012, "PARTIAL_UNRESOLVED",
        "For a positive zero-Dirichlet extremal semilinear solution with isolated interior singularity in arbitrary smooth bounded Omega, is limsup_(x->0)|x|^2 f'(u*(x)) finite?",
        "Stability mass/liminf estimates and conditional thickness bridge; exact form-stable concentrated potential; nonlinear derivative countertests; n>=10 stable-entire Liouville obstruction; nonlinear realization/cylindrical constraints.",
        "Cutoff stability, Sobolev bump construction, exact differentiation, normalized blow-up and smooth entire examples, and compatibility equations for one common nonlinearity.",
        ["Differentiable positive increasing convex f, f(0)>0, finite integral of 1/f, superlinearity; finite strictly positive lambda*.", "Normalization V=lambda* f'(u*) equivalent to target.", "Constant may depend on the fixed problem; no universal cross-problem bound required.", "C3 differentiations are additional route-specific assumptions.", "Form-stable potential and entire stable profile do not meet extremal bounded-domain boundary data; radial bound is credited prior work."],
        "Need nonlinear spatial nonconcentration for genuine extremal branch or a compatible positive zero-Dirichlet extremal counterexample with one admissible f and isolated singularity. Five routes do neither.",
        [evidence(1012,"CLAIM_AND_SCOPE.md",5,26), evidence(1012,"RESULT.md",3,19), evidence(1012,"ROUTE_2_STABLE_POTENTIAL_OBSTRUCTION.md",5,17), evidence(1012,"ROUTE_5_NONLINEAR_REALIZATION.md",5,15), evidence(1012,"ROUTE_5_NONLINEAR_REALIZATION.md",52,54), evidence(1012,"STATUS.json",2,18)]),
    record(1013, "PARTIAL_UNRESOLVED",
        "Relationship of two-loop SLE cascade measure to concrete O(n) lattice pair measures and same-realization CLE pair counting; full embedded-pair Radon–Nikodym/lattice comparison.",
        "Six propositions: finite positive-fugacity identities, Palm/descendant-kernel reduction, conformal-modulus obstruction and conditional shape criterion, credited ARS annulus consequences, and conditional pair-measure scaling convergence/UI criterion.",
        "Partition-function deletion surgery, Campbell disintegration, descendant resolvent, conditional law disintegration, imported ARS transforms, finite matching plus factorial-moment uniform integrability.",
        ["Finite simple graph, vertex-disjoint cycles, n,x>0 and explicit boundary/sampling conventions.", "CLE pairs ordered/distinct/from same realization; intensity not independent realizations.", "Standard Borel and sigma-finite intensity required.", "Descendant resolvent only origin-surrounding outer-to-inner pairs, not all sphere pairs.", "Modulus marginals/Mobius invariance do not determine embedded shape law; continuum theorem and lattice convergence are not finite tests."],
        "Complete embedded-pair RN kernel comparison, actual annular factor and conditional embedded shapes, plus model-specific full lattice configuration limit and pair-moment UI. Five approaches exhausted.",
        [evidence(1013,"REPORT.md",7,26), evidence(1013,"REPORT.md",70,112), evidence(1013,"REPORT.md",140), evidence(1013,"REPORT.md",180,214), evidence(1013,"ACCEPTANCE.md",3,9), evidence(1013,"STATUS.json",10,23)]),
    record(1014, "PARTIAL_UNRESOLVED",
        "Sullivan Problem 21: finite combinatorial types in global equal-pressure Euclidean R3 foam, tetrahedral occurrence, dodecahedral occurrence, and next-page two-faced-cell continuation.",
        "Necessary edge-curvature budget, local plane/two-catenoid junction, compact-support obstruction, conditional per-cell-curvature finite-type criterion and periodic stellar insertion count obstruction.",
        "Cellwise Gauss–Bonnet/Plateau angles, norm-one conormal sum, exact minimal junction, first variation, finite incidence enumeration and average face-count comparison.",
        ["Global locally finite R3 partition by minimal interfaces with usual Plateau junctions; no equal volumes/periodicity/convexity/area-minimizing assumption.", "Cellwise proofs restrict to regular finite ball cells, disk faces and interval borders with finite curvature.", "Local sheets are truncated planar patch/catenoid annuli, not completed disks or global foam.", "Compact stationarity requires compact support, finite area and no external boundary.", "N=9 is arithmetic threshold only; necessary average bound does not realize cells or exclude sparse tetrahedral defects."],
        "Unproved uniform per-cell Q+T bound and global minimal-interface realization/gluing. Finite types, tetrahedral and dodecahedral occurrence, and two-faced continuation all remain unresolved. Five approaches exhausted.",
        [evidence(1014,"current/RESULTS.md",5,15), evidence(1014,"current/RESULTS.md",124,134), evidence(1014,"current/RESULTS.md",136,170), evidence(1014,"STATUS.json",2,16), evidence(1014,"ACCEPTANCE.md",3,5)]),
    record(1015, "PARTIAL_UNRESOLVED",
        "Compact connected complex Z of dimension n+p with compact Y of dimension p-1 and Griffiths-positive normal bundle; compact normal parameter space covers Z by analytic n-cycles. Must a(Z)>=p?",
        "Finite-incidence and first-normal-data caveats; generic local full-rank finite-Taylor separation under joint point separation; graph modification can lose positivity; base/fibre algebraic dimensions not automatically additive; conditional polynomial-boundary-growth extension bridge.",
        "Exact projective incidence examples, local rank lemma, blowup normal bundle calculation, standard elliptic K3 field example, normal-space extension under polynomial growth, and exponential trace essential-singularity calculation.",
        ["n>=0,p>=1; ambient compact connected complex, not necessarily Kahler; cycles need not be deformations of Y.", "Source finite-incidence/local-separation requirements are not automatic.", "Local full rank does not give global finite fibres or compact meromorphic extension.", "Boundary bridge assumes normality/effective Cartier divisor/algebraically independent functions/polynomial growth.", "Proper finite field bridge begins with whole-space meromorphic functions; examples only refute shortcuts, not target; Peternell p=2 needs Kahler ambient."],
        "No global controlled meromorphic extensions recovering enough parameters, no exclusion of residual parameter geometry, and no target counterexample. Five approaches exhausted.",
        [evidence(1015,"current/REPORT.md",3,23), evidence(1015,"current/REPORT.md",25,39), evidence(1015,"current/JET_SEPARATION.md",15,31), evidence(1015,"current/BOUNDARY_GROWTH.md",5,29), evidence(1015,"STATUS.json",2,13), evidence(1015,"ACCEPTANCE.md",3,5)]),
]

now = datetime.datetime.now(datetime.timezone.utc).isoformat()
counts = dict(collections.Counter(r["classification"] for r in rows))
out = {
    "schema": "actual-authored-claim-scope-review-v1", "reviewer": "independent claim_scope_01 subagent",
    "captured_utc": now, "range": [1000,1015], "ascending_order": True,
    "claim_scope_completion_percent": 100,
    "mathematical_acceptance_completion_percent": 0,
    "assessment_boundary": "This is independent authored-claim and target-scope intake. Assertions attributed to PR authors are not independently proved or priority-certified. No delivered code, GitHub mutation, outreach, queue edit or publication was performed.",
    "review_inputs": ["pr.json.body", "README.md", "ACCEPTANCE.md", "SCOPE.json/STATUS.json where present", "pinned primary authored report/proof/route files"],
    "counts": counts, "root_scope_reconciliation_flags": [1000,1001,1003,1005,1008],
    "new_unqualified_original_full_resolution_candidates": [],
    "complete_literal_candidate_with_interpretation_hold": [1001],
    "complete_prior_credited_resolution_scopes": [1000,1007],
    "prs": rows,
}
(HERE / "CLASSIFICATIONS.json").write_text(json.dumps(out, indent=2, ensure_ascii=False)+"\n")

def cite(e):
    p = Path(e["path"])
    label = str(p.relative_to(PROGRAM))
    if "start_line" in e:
        label += ":"+str(e["start_line"])
        if e["end_line"] != e["start_line"]:
            label += "–"+str(e["end_line"])
        return f"[{label}]({p}:{e['start_line']})"
    return f"[{label} #/{e['json_field']}]({p})"

lines = [
    "# Independent claim-scope review: PRs #1000–#1015", "",
    f"Checkpoint {now}. **100% of this 16-PR authored-claim intake complete; 0% of fresh mathematical/priority acceptance.**", "",
    "No PR here asserts a new unqualified full solution of its complete original target. This conclusion comes from PR bodies, acceptance boundaries and pinned mathematical claim documents, not QUEUE.md or titles. It does not independently validate their mathematics or establish worldwide priority/openness.", "",
    "The complete literal tensegrity theorem in #1001 must remain visible for root scope reconciliation: it answers one precise literal equality convention universally, while the source's intended equivalence remains on HOLD. Do not silently treat that theorem as merely partial or exclude it based on its status field. #1000 gives a full negative answer to a literal universal identification but explicitly credits a known Hopf-link result. #1007 says the complete original target was already proved by Reineke. #1008 also bundles a credited fixed-parameter companion result while its main all-variable-count question remains unresolved.", "",
    "Eleven main targets explicitly remain partial/unresolved; three records have exact source/convention holds (#1001, #1003, #1005); two record complete prior-credited literal/original resolution scopes (#1000, #1007). Each strongest claim, quantifier boundary, mechanism and exact gap is recorded below and in CLASSIFICATIONS.json. Only #1001 requires reconciliation of a possibly original complete literal theorem before it can be excluded. The credit and complete negative claims in #1000/#1007/#1008 are retained separately.", "",
    "No delivered code was executed. No mathematical acceptance, fresh priority audit, queue edit, GitHub action, publication or external communication was made. Input SHA-256s and pinned PR heads are in INPUT_PINS.json; primary artifacts were read at those immutable heads. Root retains final workflow eligibility decisions.", "",
]
for r in rows:
    lines += [f"## PR #{r['pr']} / problem {r['problem_id']}", "",
              f"**{r['classification']}**. Head `{r['head_oid']}`.", "",
              "**Original target.** "+r["original_target_as_stated_in_authored_artifacts"], "",
              "**Strongest asserted result.** "+r["strongest_asserted_result"], "",
              "**Mechanism.** "+r["mechanism"], "",
              "**Quantifiers and boundaries.** "+" ".join(r["quantifiers_and_boundaries"]), "",
              "**Exact gap.** "+r["exact_remaining_gap"], "",
              "**Evidence.** "+"; ".join(cite(e) for e in r["evidence"])+".", ""]
    if r["asserted_full_resolution_scope"]:
        lines += ["**Preserved resolution claim.** "+r["asserted_full_resolution_scope"], ""]
    if r["literal_or_subquestion_negative_claims"]:
        lines += ["**Preserved negative scope.** "+" ".join(x["claim"] for x in r["literal_or_subquestion_negative_claims"])+" This must not be promoted to a new solution or to a stronger unproved target.", ""]
    if r["bundled_companions"]:
        lines += ["**Companion.** Problem 30005922 is explicitly a credited repaired fixed-parameter result; it does not give the all-g bound for main problem 30005923.", ""]
(HERE / "REPORT.md").write_text("\n".join(lines)+"\n")

log = [
    "# Research log", "",
    f"- {now}: Independent claim-scope intake finished in ascending order for #1000–#1015. Best-guess completion: 100% of assigned scope classification, 0% of fresh full mathematical/priority/publication acceptance. No new unqualified complete-original solution claim found. Complete literal/prior assertions remain explicit for #1000/#1001/#1007 and companion #30005922 in #1008. Root scope-reconciliation flags: #1000/#1001/#1003/#1005/#1008.",
    f"- {now}: Checkpoint artifacts: REPORT.md, CLASSIFICATIONS.json, INPUT_PINS.json. All authored PR code remains unexecuted. Evidence references are pinned to immutable PR heads; scope confidence is high for assertions, while original-source interpretation and mathematical/priority truth require separate review. Root owns integration/commit/publication; no shared-branch mutation was made by this subagent.", "",
]
(HERE / "RESEARCH_LOG.md").write_text("\n".join(log))

pins = json.loads((HERE/"INPUT_PINS.json").read_text())
for item in pins["inputs"]:
    data=Path(item["local_path"]).read_bytes()
    if len(data)!=item["bytes"] or hashlib.sha256(data).hexdigest()!=item["sha256"]:
        raise ValueError("Pinned input mismatch: "+item["local_path"])
for r in rows:
    for e in r["evidence"]:
        data=Path(e["path"]).read_text()
        if "start_line" in e:
            if not 1<=e["start_line"]<=e["end_line"]<=len(data.splitlines()):
                raise ValueError("Citation line outside artifact: "+str(e))
assert [r["pr"] for r in rows] == list(range(1000,1016))
print(json.dumps({"rows":len(rows),"counts":counts,"cited_inputs_checked":len(pins["inputs"]),"complete":True}))
