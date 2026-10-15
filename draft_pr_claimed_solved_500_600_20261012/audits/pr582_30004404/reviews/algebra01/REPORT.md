# PR582 / problem 30004404: algebra, quantifiers and reproduction audit

Review completed 15 October 2026 UTC. Completion estimate: 100% of this assigned review. This is independent verification of the completed candidate recorded at 1/5, not an additional proof-search turn.

**Mathematical verdict: PASS for the negative answer to the literal universal OWR question. No mathematical correction is required.** Every rank-two free subgroup of the figure-eight knot group has a nonidentity element killed by longitude filling. This does not decide whether at least one other hyperbolic knot admits a persistent free subgroup.

**Frozen reproduction: PASS.** All 22 captured original files match the inventory at head `e4b27ac757babc1aea75149ea986ed2beea438f9`; both deterministic outputs reproduce byte for byte. One nonblocking verifier limitation was found: its source-exclusion flag is unconditional and does not enforce an exclusion policy against an enlarged outer manifest. The actual frozen inventory is clean. See Finding R1 below.

## Independence and binding

Before opening the candidate or older verdict, I read the complete OWR contribution at printed pp.491-493 and the persistence definition and §7.1 in the April 2026 primary. I inspected the rendered OWR final question. `EARLY_CHECKPOINT.md` records the independently derived obstruction at 05:23:38 UTC and has its own checkpoint hash. Only afterward did I read the complete author proof, scope, sources, validation, logs, controls and manifests, publication status, release verifier, and older independent audit materials.

The author manifest binding is `4f6575af14a3e8b72e61202c45e411b4febcaa7770c3e7e8af45576eda6218f8`; the earlier audit binding is `b48c8afd46275ecffa62325d34ea5e3c8d68d8a104ee4ce6c3158c024003f72a`. The complete 22-file inventory is in `REPRODUCTION_RECEIPT.json`. The review never rewrites these originals.

An independent child adversary received only the abstract algebra application interface and no candidate or old verdict. It independently checked the free word, arbitrary basis quantifiers and general semidirect calculus. Its report and controls are in `subreview/`, with an ordinary `SHA256SUMS`. I independently replayed its full result in ignored scratch and verified its seal. No other review shard was read or contacted. No Git index/branch mutation, remote action, release, DOI, or outside communication occurred.

## Exact question and its negation

The original source fixes a hyperbolic knot without finite surgery, then asks for a free rank-two subgroup avoiding the union of rational filling kernels. Its slope is `p/q`, represented by `mu^p lambda^q`; thus 0 means longitude and infinity means meridian. All rational slopes, including 0, are allowed. The exact source is [Motegi, with Ito and Teragaito, OWR 8/2020, pp.491-493](https://ems.press/content/serial-article-files/46844), DOI 10.4171/OWR/2020/8.

With `N_r = ker(q_r)`, the positive assertion is

    for every eligible K, there exists H <= G(K), H isomorphic to F2,
    such that for every r in Q, H intersect N_r = {1}.

This follows from `H intersect (union_r N_r) = union_r (H intersect N_r)`. Therefore the restrictions `q_r|H` must each be injective. It would be a quantifier error to replace the union by an intersection, or to substitute joint injectivity into the product of filling groups. A counterexample needs one eligible K for which every H fails at at least one rational r. Here r=0 works for all H; the witness element may depend on H and its basis.

The later [Ito-Motegi-Teragaito v1 primary](https://arxiv.org/pdf/2604.01697v1), pp.2-3 and16-17, again defines persistence using every nonmeridional filling and every nonidentity subgroup element. Q7.1 fixes an arbitrary hyperbolic K; no slope exclusion is printed there. Its surrounding discussion motivates a separate search for even one hyperbolic example. The subgroup minimizer results earlier in that paper assume no torsion surgeries, meaning no finite or reducing surgery. These hypotheses must not silently change the printed original target or Q7.1. The present counterexample refutes a universal affirmative reading; the existential search and any question omitting exceptional slopes remain open within this review.

## Universal algebraic proof

Let `q:G -> Q` be a homomorphism with `Q''={1}`. For any subgroup `H` abstractly isomorphic to `F2`, choose a free basis a,b of H. Put

    c = [a,b], d = a c a^-1, w = [c,d],
    [u,v] = u v u^-1 v^-1.

Normality of H' gives c,d in H', hence w in H''. A homomorphism maps the second derived subgroup into the second derived subgroup of its codomain, so `q(H'')={1}`.

To certify that H'' is nontrivial, use the free letters x,y and their inverses X,Y. The expansion of the same word reduces to

    xyXYxxyXYXyxxYXX.

This has 16 letters and no adjacent inverse pair. The free normal-form theorem makes it nonidentity. The free-basis isomorphism carries it to a nonidentity element of H, and inclusion carries that nonidentity element into G. No assumption concerns ambient generators. No assertion that two arbitrary elements freely generate is needed. Therefore

    {1} != H'' <= H intersect ker(q).

The word has also been independently evaluated to a nonidentity permutation in S4, providing a second falsifiable nontriviality check. The universal proof uses free reduction, not this finite check.

For a torus bundle, the homotopy exact sequence gives an injection of pi_1(T2)=Z2 into the total group because pi_2(S1)=0, and a surjection onto Z. Thus the commutator subgroup lies in an abelian kernel. The total group is metabelian and infinite. Splitting follows by lifting a generator of Z, but splitting is unnecessary for this deduction.

In the convention `t(v,0)t^-1=(Av,0)`, an explicit model for every `A in GL(2,Z)` is

    (v,n)(u,m) = (v + A^n u, n+m),
    (v,n)^-1 = (-A^(-n)v, -n),
    [(v,n),(u,m)] = ((I-A^m)v + (A^n-I)u, 0).

Unimodularity ensures integral negative powers; the inverse works on both sides and associativity follows from `A^(n+m)=A^n A^m`. Commutators lie in Z2 at height zero and commute. In fact the derived subgroup equals `(A-I)Z2` at height zero, by the Laurent factorization of `A^n-I` for every integer n and the commutators `[t,(u,0)]`. No division by A-I is used. This covers singular A-I, identity, finite-order, unipotent, negative-unipotent, hyperbolic and orientation-reversing cases. Finite-order A does not make the height generator finite: the quotient remains Z. Changing action convention replaces A by A^-1 consistently and leaves metabelianity unchanged.

## Topology interface and all slopes

The algebra alone cannot certify that the chosen filling is a torus bundle or that the knot meets the no-finite-surgery hypothesis. Those are imported classical facts. I downloaded all six primary PDFs afresh; every byte length and SHA-256 matches the frozen receipts. The private PDFs and rendered pages remain below ignored `.cache`. `SOURCE_EVIDENCE.json` records identities and inspected locations, without redistributing source texts.

- [Thurston, Chapter 4](https://library.slmath.org/nonmsri/gt3m/PDF/4.pdf), §4.3, constructs the figure-eight complete hyperbolic structure. Theorem 4.7 at printed p.61 covers the rational slopes outside the nine exceptions, with sign symmetry. Its mapping-torus account at p.70 supports the zero filling, but the disclosed D-shaped coordinate glyph is not the sole basis of identification.
- [Brittenham-Wu, Theorem 1.1(4)](https://homepage.math.uiowa.edu/~wu/papers/p32.pdf), pp.1-2, uses standard rational coordinates, excludes infinity, lists the nine exceptional slopes and identifies 0,+/-4 as toroidal. Its case is explicitly credited to Thurston.
- [Khoi, printed p.524](https://math.ac.vn/public/uploads/files/0803519.pdf), expressly identifies figure-eight zero surgery as a torus bundle. This supplies the unambiguous filling identification required by the algebraic interface.
- [Gukov-Manolescu, §9.4, printed p.71](https://web.stanford.edu/~cm5/surgeries.pdf), gives positive-slope cone orders (2,3,7), (2,4,5), (3,3,4). The disclosed middle negative-slope subscript error is not used. Negative slopes use Thurston's independent sign symmetry.

The no-finite-surgery deduction exhausts Q, not merely tested integer samples:

| Rational slope class | Imported type | Reason the group is infinite |
| --- | --- | --- |
| Outside {0,+/-1,+/-2,+/-3,+/-4} | Closed hyperbolic | A finite fundamental group would make the noncompact universal cover H3 a finite cover of a compact manifold, impossible. |
| 0,+/-4 | Toroidal | An incompressible torus injects Z2. Zero independently surjects to Z by the bundle. |
| +/-1,+/-2,+/-3 | Seifert with the three stated bases | Killing the regular fiber surjects to the triangle orbifold group, which is infinite. |

For the last row, the exact Euler characteristics are -1/42, -1/20, -1/12. Each triangle with angles pi/a, pi/b, pi/c is hyperbolic; its reflection group and orientation-preserving index-two subgroup are infinite, giving the standard triangle-group realization. This avoids the invalid inference that every Seifert fibered group is infinite. The Euclidean and spherical comparison triples give 0 and +1/30 and are explicitly tested. Infinity is the meridional S3 filling and lies outside Q.

Consequently 4_1 is eligible, q0 has metabelian target, and for every free rank-two H,

    {1} != H intersect ker(q0) <= H intersect (union_(r in Q) ker(q_r)).

Only q0 is claimed metabelian. In particular H'' is not asserted to lie in every other filling kernel. Cyclic persistent groups and persistent individual generators are compatible with the obstruction.

## Reproducible controls

`reproduce.py` copies the 22-file frozen release below `.cache/reproduction`, compares all 22 size/hash pairs to the captured head inventory, runs every supplied implementation, compares the entire JSON objects and every stdout byte for both supplied expected outputs, and confirms the original inventory is unchanged afterward. It also stores complete stdout JSON, timestamps, output lengths, hashes, runtime and stderr status in `REPRODUCTION_RECEIPT.json`.

The author replay matches SHA-256 `7034c750d744e98c7f2f6c27d595ab6a947d2060d9a3868abd85889caea03c28`: all 30,625 ordered pair checks, the noncommuting controls, explicit word, rational arithmetic and declared partition. The earlier independent replay matches `605d27d976b1c125d3462e2fabf048827f2ea99daa300425978a193af8ffa07e`: all 10,125 matrix parameter pairs, full non-metabelian matrix output, all manifest and arithmetic fields, and every limit field. This is full-output agreement, not agreement of selected counters.

The original `verify_release.py --self-test` passes its outer inventory/hashes, both bound nested manifests and both replays, then rejects its four declared mutations. The outer manifest lists 21 files and excludes itself, so the actual snapshot has 22 files; the nested author/audit manifests respectively list 10 and7 payload files. Safe relative paths, unique paths and symlink rejection were inspected; fresh parent-path and symlink controls fail as intended.

`fresh_controls.py` uses a new first-adjacent-pair deletion reduction and finite permutation groups, importing no supplied implementation. All 244 ordered pairs in S3, A4 and D8 satisfy the law, with noncommuting examples in each. In S4 the same word evaluates to (01)(23), rejecting an evaluator that makes every group pass. Three explicit free-basis automorphisms preserve nontriviality. A pair of individually surviving, noncommuting S3 generators has the witness killed, exposing the generator-survival fallacy. Exact orbifold arithmetic and boundary signs are also checked.

The independent child supplied a second mechanism check across ten unimodular matrices: 20,250 commutator formula evaluations, 20,250 witness evaluations, 4,050 associativity triples, 450 group inverses, 170 Laurent factorizations and ten matrix inverse checks. Heights include negatives. `RUN_RECEIPTS.json` preserves the full fresh outputs and their byte-exact replays. These finite controls supplement proofs; none establishes knot topology, all-slope classification, source accuracy or novelty.

## Finding R1: source-exclusion flag is not an enforced policy

Severity: P2 verifier/reporting limitation, nonblocking for the mathematical conclusion and the exact frozen inventory. Location: original `verify_release.py` lines29-41 and45-53, particularly line53.

`check_manifest` enforces equality with the supplied manifest. The outer manifest is not bound to a fixed allowlist or fixed digest by this script. `source_files_included` is then set to false unconditionally. In isolated controls I added either a synthetic `source.pdf` or synthetic `imported_corpus.txt`, recorded its correct length/hash in the outer manifest, and changed no author/audit payload or nested manifest. Both altered releases passed the full verifier and both mathematical replays while reporting `source_files_included:false` and 22 listed files. The four supplied self-test mutations do not exercise this rehashed-manifest case.

This does not show contamination of the real release: the actual 22-file inventory was separately inspected and bound to the captured snapshot. Nor can a hash, by itself, decide semantic authorship. It shows that the verifier's safe-only source-exclusion claim needs an additional trust assumption or implementation rule.

Action: before relying on the script as an exclusion-policy gate, require the exact permitted release paths (and/or externally bind the outer manifest), then derive the source-exclusion result from that policy. Add manifested PDF/corpus regression cases. If it is intended only to check integrity relative to an already trusted manifest, narrow its documentation and report so it does not claim independently to establish source exclusion. Do not rewrite either frozen nested package to apply this recommendation; any correction belongs in a separately reviewable publication step.

## Disposition and limits

The exact literal counterexample supports `claimed_solved, 1/5` for problem30004404. The original proof is complete under explicitly credited classical topology. No circularity, free-basis substitution error, union/intersection reversal, omitted rational slope, or hidden need to prove injectivity on generators was found. The older audit's mathematical conclusion is confirmed independently.

This is not a claim of original topological classification, first solution, formal proof certification or human peer review. No fresh comprehensive priority search or current remote/publication-state assessment was performed by this algebra review. The separate existential hyperbolic problem, variants omitting finitely many slopes and any claim that all hyperbolic knots fail are outside the verified result. No paper currently exists in this review and no publication action is authorized by the mathematical PASS. The parent mathematical gate can proceed while recording R1 for any subsequent publication verification.
