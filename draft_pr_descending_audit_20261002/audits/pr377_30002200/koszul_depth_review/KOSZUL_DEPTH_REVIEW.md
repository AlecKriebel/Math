# Frozen-head algebra audit: PR 377 / problem 30002200

Verdict: REQUEST ALGEBRA REPAIRS at frozen head `75bea4d3be9904e90c3843892671a440ba4d2c42`. The requested all-rank sharpness is verified as Franz's prior result, and the guide's nonsplit-depth proof establishes it over Q. The frozen packet is not fully correct: one rank-five extension-direction mistake appears in its guide, its author checker, its previous review, and its previous review checker. No new solution, novelty certification, or acceptance follows from any finite controls.

## Independence and evidence

Read and visually rendered the literal Franz OWR contribution, printed 2954–2956, before opening candidate, history, root or sibling material. Independently reconstructed regular-sequence Koszul exactness, its local depth/Ext consequences, the actual inclusion map, extension depths and even-rank polynomial extension. The independent proof and executable were sealed at `2026-10-03T05:05:49.694629+00:00` in `INDEPENDENT_SEAL.json`; only then opened the frozen snapshot. Independent chain controls use an exact rational sparse eliminator, without SymPy or candidate imports. Full candidate replays used an isolated private SymPy 1.14.0 environment under ignored raw_sources/.

The original report has undeclared n in its numerical bound. AFP v2 Corollary 1.4 and the actual proof of Proposition 5.12 make this torus rank r. The bound is floor((r-1)/2) for a nonfree module, with freeness threshold ceil(r/2), not a bound involving dim X. The field and topology hypotheses are explicitly recorded in the independent derivation. All four independently retrieved primary PDFs match the frozen SOURCE_MANIFEST byte counts and SHA-256 hashes.

## Mandatory repair: free target and free quotient are reversed

At a=b=1, r=5, m=2, corrected Proposition 5.1 and formulas (5.11)–(5.12) give

    C=(coker iota)[15]=R[0] ⊕ R[3]^5 ⊕ K_2[6],
    Q=(ker iota)[14]=K_4[9] ⊕ R[10]^5 ⊕ R[13],
    0 -> C -> H_T^*(X) -> Q -> 0.

Therefore extensions from the quotient K_4[9] to a free target in C involve R[0] and R[3]. Their target-minus-quotient shift differences are -9 and -6. The guide's alleged target shifts 10 and 13 belong to the FREE QUOTIENT Q. Free quotients split automatically; they cannot be used as those Ext targets. The split conclusion nevertheless remains correct: AFP Lemma 2.4 says Ext1(K_4[9],R[l])_0 is zero unless l-9=2. Neither l=0 nor l=3 is exceptional. The remaining K_4[9]-to-K_2[6] extension vanishes by parity. Thus this is a checkable mistake in the justification, not a counterexample to the exact-order conclusion.

Required corrections at this frozen head:

| Frozen artifact | Location | Required change |
|---|---|---|
| CREDITED_PROOF_GUIDE.md | line 54 | Use target shifts 0,3 and differences -9,-6; identify 10,13 as free quotients. |
| verify_source_cases.py | lines 58–59 | Replace wrong-target arithmetic with the correct Ext direction and preferably derive target shifts from r,m,d and the original V/W degrees. |
| review/REVIEW.md | extension paragraph, line 23 | Correct claimed differences 1,4 to -9,-6 and explain which side is the quotient. |
| review/independent_check.py | line 33 | Correct the left/right shift test; its existing [1,4] arithmetic replays but validates the wrong objects. |

After any revision, rerun checks and refresh all affected nested/publication bindings. The source-credited all-rank conclusion survives these repairs; promotion of the current frozen packet is withheld until they are made.

## Exhaustive algebra-guide claim assessment

| Claim in guide | Assessment and independent mechanism |
|---|---|
| Rational coefficients and primary scope | Pass. Franz v4 p.3 and FH Section 2 explicitly allow every characteristic-zero field. Real introductory language in FH is not a rational gap. No integer/positive-characteristic equivariant theorem follows. |
| Euler coefficient and shuffle sign | Pass at a=b=1. Euler class is t_i; general b would require t_i^b. The sign counts elements of J greater than i, consistent with right wedge multiplication. |
| Free presentation via Lemmas 4.4–4.5 / Proposition 4.6 | Pass. PAL duality shifts coker by rd, ker by rd-1; equivariant homology is not Borel homology. |
| Koszul middle map and indices | Pass. Removing short V columns leaves the wedge map at m to m+1; complement self-duality gives coker K_m and kernel K_{m+2}. For m>=2 both are strictly below terminal free K_r. |
| Corrected nonfree grading | Pass. v4 gives md and (m+2)d-2*dbar-1; at a=b=1 these are 3m and 3m+3. |
| Free grading | Formula passes, but the next sentence incorrectly assigns high free shifts to the target side of the extension. Mandatory repair above. |
| Parity splitting between Koszul terms | Pass. Intrinsic K terms are even, their shifts differ by 3, so degree-zero Ext between them is absent. |
| Exceptional rank-five extension | The rank condition is right, but the target shifts/differences are wrong. The corrected Ext calculation proves splitting. |
| Exact order from minimal Koszul tail | Pass. pd K_j=r-j, full-maximal depth j. Away from m one variable is invertible and the localized complex contracts, so the localized syzygy criterion is satisfied. Nonzero top Ext independently witnesses nonfreeness. |
| Extensions preserve the m-syzygy lower bound | Pass. Depth inequalities at every prime give the lower bound. At m, C has depth m while Q has depth m+2, forcing the middle depth to be m, even if nonsplit. |
| Extra sphere factor | Pass. Euler class of 1⊕L vanishes; Gysin gives Q[s]⊕Q[s][3]. Equivariant Kunneth gives two shifts of polynomial extension. |
| Exact order after polynomial extension | Pass. Faithful extension preserves a failing regular sequence. Independently, the prime (t_1,...,t_{2m+1}) excludes s, retains height 2m+1 and depth m. Full maximal depth increases to m+1 and is insufficient alone. |
| Rank-five / rank-six boundaries | Pass for exact order: both are order 2. Full homogeneous maximal depth is 2 at rank five and 3 at rank six; the even witness prime still has depth 2. |
| Arbitrary r>=5 | Pass by the universal proof and source theorem, not by finite enumeration. Odd/even choices cover every requested rank. |
| Source qualification and credits | The conclusion is Franz's published prior answer. Minimal dimension, general-length classification proof, integer and positive-characteristic results are outside the checked assertion. |

The candidate's geometric/Morse assertions were read, and the symbolic Hessian claims replayed. This algebra review does not independently certify the geometric cycle construction; a separate adversarial geometry audit is needed for a combined disposition. The primary universal upper bound mechanism was checked directly through AFP Theorem 5.7, Lemma 5.6 and Proposition 5.12.

## Exact controls, replay and bindings

The independent executable covers 34 exact homogeneous Koszul-chain components for r=3,5,6 and b=1,2, verifies H0=R/(t_i^b) and all higher homology zero, and rejects unsigned differentials and wrong powers. Its universal mathematical derivation supplies the all-rank conclusion. Post-seal actual-inclusion matrices independently verify 16 graded components in the rank-five left/right decomposition above, without importing either frozen checker.

Author controls replay in full: 358,064 assertions, 131,040 length-subset cases, 35 angular-Hessian cases and 8,100 formal Koszul-square cases; stdout is byte-exact to SOURCE_CASE_CHECKS.json and review/AUTHOR_REPLAY.json. The previous review's 983 controls likewise replay byte-exact. verify_publication.py succeeds byte-exact and explicitly does not reverify primary PDFs; this audit independently reverified their hashes. Replay success is not semantic correctness of the flawed extension assertions.

The outer frozen snapshot's 20 files all match hashes. Nested manifests explicitly bind 10 author, 4 prior-review and 17 publication entries; their printed counts 11,5,18 include the respective manifest themselves. Their hashes are bound by the outer snapshot (and inner publication binding as applicable). Full stdout and empty stderr are preserved for each successful replay and independent executable. The bounded final manifest names exactly the owned audit files and private primary PDF hashes; it contains no all-repository or all-literature exhaustiveness claim.

## Source-level b>1 caution, outside candidate scope

The printed generalization of Proposition 5.1's free-target splitting assertion to b>1 is too broad algebraically. General Ext1(K_{b,r-1},R)=A[-2b], A=R/(t_i^b), not a one-degree copy of k. For example r=3,b=2 admits Ext1(K_{2,2},R)_0=A_4 of dimension 3 although l-l'=0 differs from 2b. For the actual corrected rank-five shifts, a=1,b=5 yields Ext1(K_{5,4}[41],R[11])_0=A_40 of dimension 1. This does not establish that the actual topological extension is nonzero; the separate Puppe splitting theorem cited in v4's footnote was not reconstructed. No such issue affects candidate a=b=1, or the universal nonsplit-depth sharpness argument. This caution is an independent falsification control, not a novelty claim.

Strongest verified result: the rational requested sharpness follows for every r>=5 by the credited construction, and its algebraic exact-order mechanism is independently verified. Exact remaining gap for this frozen packet: correct the rank-five extension direction and its echoed assertions/review, refresh bindings, and integrate the independent geometric audit before an overall endorsement.
