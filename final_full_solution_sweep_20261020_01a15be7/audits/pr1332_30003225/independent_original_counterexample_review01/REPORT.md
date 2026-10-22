# Independent original-scope and counterexample audit: PR1332 /30003225

Audit target: head `300ad33db51517aba03ce04aa7f257de3d7757c1`, all eight changed blobs bound in `PINNED_MEMBER_HASHES.json`. Review performed independently of the cited acceptances and their claimed executions. Family: original formulation, free-chain counterexample, and priority. Overall parent sweep remains 80%.

## Verdict and strongest justified claim

No fatal mathematical gap was found in the five-free-blowup counterexample **as an equality of closed sets of arcs, under the expressly listed contact/index conventions**. Its family is exhaustive, its closure argument is valid, and its exclusion covers every positive integer contact multiplicity and every reference prefix divisor. This supports the existing **qualified** claimed-solved wording. It does not authenticate an erratum, settle an unspecified intended replacement of the source's undefined bare relation, or establish worldwide novelty.

The actual arXiv v3 Conjecture 1, printed p.31, uses an intersection. The catalogue's union is a transcription discrepancy. Visual inspection confirms that the conjecture writes a bare relation with subscript i0, while the preceding definition and Remark 4.14 use a contact-at-least relation. These are genuine notation issues, but do not erase the literal qualified negative result: the five-blowup example defeats each identified natural interpretation, including fixing the selected free point. Nothing in the source's definitions restricts its prime-divisor quantifier to satellite divisors or to minimal embedded resolutions of singular branches.

A precise result label is:

> Five free blowups refute the displayed Nash-intersection assertion under the explicit natural contact/index readings: the intersections have weights (3,5) and (2,5), neither a positive integer multiple of any reference prefix divisor (1,j). Printed bare-relation and index conventions remain unauthenticated; no unspecified replacement, broader Nash, or novelty claim is made.

This is proposed wording only. No row, PR, service, Git index, ref, or publication was changed.

## 1. Primary-source reconstruction

Sources were fetched afresh, hashed, and read at the exact locations in `SOURCE_INDEX.md`. The v3 PDF bytes match the identity recorded by the PR, but acceptance was not inferred from that match. Printed and PDF page numbers agree for v3. I visually inspected v3 pp.5–7 and 31 and workshop printed p.2679.

The source works with prime exceptional divisors over the smooth complex surface germ. It defines their minimal point-blowup models and combinatorial type, and counts contact by common blown-up centers. The definitions explicitly encompass nonsatellite divisors and record extra free blowups after resolving associated curves. Thus smooth curvettas are allowed. The selected center c3 in this audit is free in the explicit smooth-point definition; no convention about whether the original point itself is free is needed.

At v3 pp.24–25, the Nash set is the closure of lifted arcs meeting a divisor, and its transverse sublocus has the same closure. At p.30, the defined equivalence adds contact at least i to equal combinatorial type; the contact-multiple cylinder is the closure of exact multiplicity q. Workshop p.2679 instead describes at-least-q multiplicity. The two definitions yield the same closures in the explicit examples below.

Conjecture 1 at p.31 proposes that the same-type-family intersection associated to a chosen free point is a multiple-contact cylinder of the divisor created there. The displayed bare equivalence has no inequality sign. Remark 4.14 specializes index 1 to varying tangents and the first exceptional divisor, which conflicts with a mechanical global zero-based created-point reading. I do not supply an author correction. The workshop repeats the bare relation and explicitly identifies the right-hand divisor as the one created at the selected point.

## 2. Independent construction and exhaustive free family

Use centers c1=0,c2,...,cn and let Dj be created at cj. Along the reference smooth branch y=0, after j blowups a chart is

    (x,u_j) ↦ (x,y=x^j u_j).

For j≥2 the newest Dj is x=0 and its unique intersection with the previous exceptional component is u_j=∞. Blow up a finite center u_j=a. Two charts are

    u_j=a+xu_(j+1),
    x=vh, u_j=a+h.

On the new component in the second chart, h=0; the old component is v=0. On the overlap u_(j+1)=1/v. Hence exactly one point is omitted from the finite-center chart, and that point is satellite. Every free choice is represented by one complex a, with no omitted free direction.

Fix a prefix of k≥2 centers and n>k; flatten its branch jet to z=0 in regular coordinates (x,z). The common tangent is fixed, so x is a parameter of every associated smooth curvetta. Successively subtracting a finite coefficient and dividing by x proves inductively that all completions are indexed by

    P(x)=a_k x^k+...+a_(n-1)x^(n-1),  a_j∈C.

The final chart is z=P(x)+x^n w. Conversely every such polynomial gives exactly n successive free blowups with the fixed prefix. The same combinatorial type cannot include a satellite blowup: it changes proximity data (and forces an older self-intersection below -2). Nor can a next center on an older component away from the newest one occur in the minimal model of the final divisor: the intervening blowup would be extraneous. The source treats proximity data as an encoding of combinatorial type, so this exhaustion is within its own definitions. Different polynomials first differing below degree n give different centers and divisors. Later curve coefficients do not affect the divisor already created.

For n=5 the full graph is (-2)-(-2)-(-2)-(-2)-(-1), and the full F2 and F3 parameter spaces are respectively C³ and C². No singularity or satellite-final hypothesis has been smuggled into this step.

## 3. Exact closure, including satellite limits and x=0

Set z_P=z-P(x). The polynomial coordinate change (x,z)↦(x,z_P) is invertible. Define

    S_P={ord_t x≥1, ord_t z_P≥n},   ord_t 0=∞.

Its coordinate ring is a polynomial ring in the unrestricted arc coefficients. Thus it is a reduced irreducible cylinder, and its nonempty open locus ord x=1 is dense. Every arc in that open lifts in the final chart with w=z_P/x^n∈C[[t]], meets the new divisor transversely, and misses its sole intersection with older components.

For the reverse containment, the two charts covering the final component have maps

    x=x, z_P=x^n w;
    x=vh, z_P=v^(n-1)h^n.

Any nonconstant lifted arc centered on the component satisfies the defining order inequalities in either chart. Thus the raw Nash set is contained in S_P, while its transverse part contains a dense open of S_P. This proves exactly

    Nbar(E_P)=S_P.

This uses closure and explicit charts, not an unsupported converse from valuative domination to Nash inclusion. In particular, a limiting arc may meet the satellite point and still belong to every S_P. A direct specialization confirms all such closure memberships: given any arc (x0,z0)∈S_P, put

    x_e=x0+e t,
    z_e=P(x_e)+z0-P(x0).

At e=0 this is the original arc; for all but at most one nonzero e its x-order is 1, while z_e-P(x_e) has order at least n. Coefficients are polynomial in e. This also handles identically zero x and the constant arc, with the harmless exceptional parameter avoided. No common wedge for all P is required: membership in each closure is a separate statement.

For a reference Dj, the same argument with z=x^j u and its second chart x=vh,z=v^(j-1)h^j proves, for each positive integer q,

    Cont^q(Dj)=C(q ord_Dj)={ord x≥q, ord z≥jq}.

The dense locus ord x=q has exactly q contact in the first chart. Every at-least-q lift is contained in the displayed closed cylinder, so taking its closure gives that same cylinder as well. This verifies both primary-source contact conventions in this example.

## 4. Intersection and the all-integer obstruction

The members P=0 and P=x^k force ord z≥n and ord x^k≥n. Orders of nonzero series in C[[t]] are integral, so the latter condition is ord x≥ceil(n/k). Conversely these two inequalities imply ord P(x)≥n for every permitted polynomial, since all its exponents are at least k. Therefore, for the complete family,

    I_k={ord x≥ceil(n/k), ord z≥n}.

If the bare relation were interpreted as exact contact k, rather than at least k, the same conclusion holds: use P=x^k and P=2x^k. Both first differ from the zero reference at the first movable center; subtracting the two equations forces ord x^k≥n, and then ord z≥n. This is a conditional calculation, not a claim that the source defines its bare relation in that way.

Two independent coordinate order cylinders with finite thresholds are equal only when both thresholds coincide. To see necessity, take one coordinate to have exactly its lower threshold and the other to have arbitrarily high order, then interchange the coordinates. Thus I_k=C(q ord_Dk) if and only if k divides n, with q=n/k.

Take n=5. For k=2 and 3 respectively,

    I2={ord x≥3, ord y≥5},
    I3={ord x≥2, ord y≥5}.

If either were C(q ord_Dj), then respectively (q,jq)=(3,5) or (q,jq)=(2,5). Neither 3j=5 nor 2j=5 admits an integer j. This excludes every q≥1 and even every integer j≥1, stronger than the required j∈{1,...,5}.

For an explicit uniform separation put r=3 or 2. If q<r, the polynomial arc (t^q,t^max(5,jq)) is in the reference cylinder and outside I_k. If q>r, (t^r,t^5) is in I_k and outside the reference cylinder. If q=r, use (t^r,t^5) when jr>5, and (t^r,t^(jr)) when jr<5. The sole equality case jr=5 never occurs. These witnesses are nonconstant and convergent.

The resulting intersections themselves are Nash sets of other prime divisors: the primitive toric weights are (3,5) and (2,5). Direct charts are x=u³v,y=u⁵v² and x=u²v,y=u⁵v³. Both exponent matrices have determinant 1; the inverse pairs are (u,v)=(x²/y,y³/x⁵) and (x³/y,y²/x⁵). Exact order pairs lift with u-order 1 and v a unit. Their dense loci give the stated cylinders. The counterexample therefore refutes the *specified reference multiple*, and does not refute a weaker claim allowing an arbitrary divisorial valuation.

## 5. Source-index map, edge cases, and attempted repairs

Choose the genuinely free middle center c3, leaving c4,c5 after it.

| Explicit reading | Family intersection | Right-hand reference | Failure |
|---|---|---|---|
| Last-shared divisor normalization | F2, thresholds(3,5) | D2 | q=3,2q=5 impossible |
| Zero-based p0=c1,p1=c2,p2=c3; nearby contact≥2 definition | F2 | divisor at p2=D3 | q=3,3q=5 impossible |
| Fix the selected c3 as well | F3, thresholds(2,5) | D3 | q=2,3q=5 impossible |
| One-based local p3=c3 and contact≥3 | F3 | D3 | same obstruction |
| Conditional exact-contact 2 or 3 | same I2 or I3 | any reference Dj | no integer reference ray |

The five-blowup choice matters. In the minimal n=3,k=2 example, fixing its selected final center would leave a singleton and remove that version of the counterexample. Here both relevant prefixes leave a positive-dimensional family. Merely shifting the reference divisor cannot repair either I2 or I3, because every reference j is already excluded.

The smallest normalized example n=3,k=2 gives weights(2,3), agreeing with the PR's supplementary satellite calculation. Divisible positive cases such as n=6,k=2 or3 satisfy the reference equality. A fixed final center (k=n) is a singleton and gives Dn with q=1. At the first-exceptional specialization, varying all tangents is essential: for an all-free length-n type, the two tangent choices y=0 and y=x force both x and y to have order at least n; these bounds satisfy every tangent/branch completion. Its intersection is C(n ord_D1), consistent with Remark4.14 rather than a contradiction to it.

Raw transverse loci have ord x=1 and their different-parameter intersection can be empty. The conjecture concerns their **closures**, so substituting those raw loci would change the question. Similarly, nonreduced scheme intersections differ from their supports. For n=5,k=2, after eliminating y1,...,y4, the two-member coefficient ideal is generated by x1²,2x1x2,x2²+2x1x3. Its radical kills x1,x2; the ideal itself does not kill x1. For k=3 the corresponding generators x1³,3x1²x2 have radical (x1). These are precisely the reduced supports used above. The claimed equality is not a nonreduced scheme assertion.

Potential repairs requiring satellite final divisors, singular curvettas, or minimal embedded resolutions would impose additional hypotheses absent from the inspected source. Such new statements are not evaluated here. Likewise no bounded enumeration of q, no assumption on practical runtime, and no implementation requirement is imposed on this elementary proof.

## 6. Independent guards and their limits

`independent_controls.py` is newly written standard-library code, with no imports from author programs. It evaluates actual truncated branch polynomials over F3 for all 6,561 centered four-jet pairs in each family. It checks all 27 F2 and nine F3 parameter tuples, and their exact-contact subfamilies. The resulting supports have nine and27 points respectively, matching the coordinate radicals. It also checks 1,800 polynomial witness cases,432 wedge specializations, both unimodular toric charts, and six boundary/negative guards. Normal, -O, and -OO outputs agree byte for byte. Three deliberate mutations (floor instead of ceiling, one completion instead of the full family, and a zero reference substituted for exact-contact completions) are each rejected with RuntimeError in all three modes; the results are recorded separately.

These finite guards can catch an off-by-one exponent, confusion of F2/F3, an incorrect exact-contact interpretation, or a false witness. They do not prove complex-parameter exhaustion, infinite-arc density, source intent, or universal quantifiers. Those are proved above. No author verifier is included among the actual eight changed paths, and none was replayed; the PR's reported18/44 checks and archive-restoration claims were treated as claims only.

## 7. Priority, provenance, and exact remaining limits

The fresh mandatory GWS read preceded substantive mathematics. Its191rows had no match for the recorded targeted strings; the request, response digest, and no-mutation status are in `GWS_DUPLICATE_CHECK.json`. This is a duplicate check in the accessible tracker, not a worldwide priority certificate.

The DOI [10.1016/j.aim.2017.09.035](https://doi.org/10.1016/j.aim.2017.09.035) identifies Fernández de Bobadilla, Pe Pereira, and Popescu-Pampu's *On the generalized Nash problem for smooth germs and adjacencies of curve singularities*, Advances in Mathematics320(2017),1269–1317. It is the original conjecture/background paper, not an authenticated publication of this negative solution. The title/authors/journal identity is independently supported by the arXiv record and publisher-indexed metadata.

The original already supplies combinatorial invariance and finite cylindrical intersections. Ishii's earlier Example2.10/Proposition3.4 and Lemma3.11 supply the standard maximal-divisorial/toric framework; they are dependencies and consistency checks, not full coverage of the displayed free-family counterexample. The direct proof above does not depend on importing its central calculation from them.

The authors'2018 survey, arXiv1805.01418§8,p16, still refers to Conjectures1 and2 of the2017 paper as conjectures; it does not state this negative example there. Bounded mechanism/title/citation searches recovered the original and unrelated or adjacent Nash literature, without an authenticated prior full-negative result. This does **not** prove that no earlier correction, observation, thesis, unpublished note, or later publication exists. No new-negative DOI or novelty claim is justified by this audit. Search scope and exact links are recorded in `SOURCE_INDEX.md` and `PRIORITY_SEARCH_LOG.json`.

Publisher full text returned403 and the institutional handle was inaccessible through the browsing tool. The publisher-typeset conjecture was not inspected. The conclusion is tied to the exact arXivv3 and2016workshop formulations read and visually checked here. The undefined bare relation/global indexing remains an interpretation limit, not a newly discovered flaw in the explicit mathematics. An unspecified alternative intended conjecture remains unauthenticated. No external consultation was initiated or prepared.

## 8. Closure and integrity

All new files are confined to this audit directory, under the8MiB cap. Earlier PR1327 and PR1330 sealed audits were left untouched. The review is an independent mathematical audit by an agent, not human or formal proof verification. `MANIFEST.json` closes the member set and hashes the payload; `verify_manifest.py` performs a read-only integrity, pinned-blob, branch, cap, and exact-control replay. No Git or remote mutation is part of verification.
