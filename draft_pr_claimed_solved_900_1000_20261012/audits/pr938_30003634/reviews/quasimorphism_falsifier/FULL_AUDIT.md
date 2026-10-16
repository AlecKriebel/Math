# Independent adversarial audit of the new signature-quasimorphism mechanism

## Disposition and scope

**PASS for the mathematical mechanism; NO HISTORICAL PRIORITY DEFEAT ESTABLISHED.** The mechanism proposed to this reviewer is valid, with the precise power argument below. It proves

\[
 P_m^{(k)}\not\subset\mathcal F_1^m\qquad(m\ge3,\ k\ge1\text{ finite}),
\]

and consequently

\[
 P_m^{(n+2)}\not\subset\mathcal F_n^m\qquad(m\ge3,\ n\ge1).
\]

These are deductions assembled and checked in this audit, not quotations of an older complete theorem and not a revision of the immutable candidate. The immutable submitted proof proves the explicit n=1 result. This review adds zero positive proof-search turns to the separately counted new mechanism. No materially new approach was introduced here.

This reviewer read the complete target record and original proof, recorded an independent plan before historical source audits or sibling conclusions, and communicated only with the parent. All 44 pinned actual Git blobs were checked against copied disk bytes and the fixed inventory at the start and end. The submitted proof hash is `0492e0e0de785be263174e86d69855120b2f5c24b105c6479739cd72d64abe3b`; its outer manifest is `149e6144f0ad90ee12945c29155318100b65c6faee8ba2661d2c09db58b9ae30`. Neither was modified.

## 1. Fixed conventions and imported facts

Put s(beta)=sigma(hat(beta)), the ordinary signature of the oriented standard braid closure, with positive trefoil signature -2. Its domain includes links. Set q(beta)=lim_{r to infinity}s(beta^r)/r on B3. At omega=-1, Theorem A and Remark 1 of [Gambaudo--Ghys, published 2005](https://www.numdam.org/item/10.24033/bsmf.2496.pdf), journal pp.544--545, give bounded defect, with the safe bound 2n=6 on B3. Their journal p.575 explicitly gives existence, homogeneity, the quasimorphism property and |q-s|<=6. For B3 the ordinary Burau representation acts on a real 2-dimensional symplectic space; no root-order exception occurs at this ordinary root. The source's larger bound suffices, so no optimal-defect claim is required.

[Calegari, scl](https://www.math.uchicago.edu/~dannyc/books/scl/scl.pdf), Proposition 2.65, printed p.33/PDF p.42, proves that homogeneous quasimorphisms on amenable groups are homomorphisms. Printed p.27 lists solvable groups among amenable groups. This author's PDF is pinned by actual downloaded bytes, and the [author's institutional publication record](https://authors.library.caltech.edu/records/rcpw2-ejn35/latest) identifies the book as MSJ Memoirs 20 (2009), DOI 10.2969/msjmemoirs/020010000. Its PDF has no separately asserted dated version label.

[Otto, published 6 November 2014](https://msp.org/agt/2014/14-5/agt-v14-n5-p05-s.pdf), Definition 2.3 and the surrounding paragraphs, journal pp.2631--2632/PDF pp.5--6, use the ordinary derived series. They define string-link solvability by standard closure, state the filtration consists of normal subgroups of string-link concordance, and display its nesting. Thus Fn is contained in F1 for n>=1.

The exact source question is [Harvey's contribution, joint work with Park and Ray, OWR50/2017](https://publications.mfo.de/bitstream/handle/mfo/3612/OWR_2017_50.pdf?isAllowed=y&sequence=1), Question 3, PDF p.35/journal p.3021. The workshop was in October 2017; the EMS publication was 19 December 2018. The exponent means ordinary derived depth. All source bytes, locations and private visual inspections are recorded in SOURCE_PINS.json and SOURCE_INSPECTION.md.

## 2. The restriction to P3 really is nonhomomorphic

This cannot be inferred merely from nonhomomorphy on B3. Here is a direct check inside P3.

Let x=sigma1, y=sigma2 and put

\[
 a=x^2,\quad b=y^2,\quad c=yx^2y^{-1},\quad z=(xy)^3.
\]

All four braids are pure: a,b are squares of transpositions; purity is preserved by conjugation; the permutation of xy has order 3. Use the braid relation xyx=yxy to calculate

\[
 acb=x^2yx^2y=x(xyx)xy=x(yxy)xy=(xy)^3=z.
\]

The ordinary closure signature on two strands is s(x^ell)=1-ell for ell>=1, as given in Gambaudo--Ghys Remark 3, journal p.545. Adding a split trivial third strand does not alter that signature: extend the Seifert form by a zero summand. Thus q(a)=-2. Conjugate closures are isotopic, so q is conjugation invariant on B3. The generators x,y are conjugate (for example (xy)x(xy)^-1=y); c is conjugate to a. Hence q(a)=q(b)=q(c)=-2.

Here z is the full twist Delta3^2, while z^2 is Delta3^4. Lemma 4.1, journal pp.568--569, says s(alpha Delta3^4)=s(alpha)-8. Since s(1)=0, iteration gives s(z^{2r})=-8r and therefore q(z)=-4. This also agrees with Proposition 5.2: at n=3, theta=1/2, its interior interval gives q(xy)=-4/3. We need neither a claim about knots only nor extrapolation from small powers.

If q restricted to P3 were a homomorphism, the displayed product identity would instead give q(z)=-6. The contradiction proves nonhomomorphy inside P3, independently of the original explicit candidate's pointwise signature.

## 3. The normal-subgroup descent step is exact

**Lemma.** If q:G->R is a homogeneous quasimorphism with finite defect D, N is normal in G, and q vanishes identically on N, then q factors as a homogeneous quasimorphism on G/N.

**Proof.** For g in G and u in N, normality gives (gu)^r=g^r u_r with u_r in N for every positive integer r: both sides have the same quotient image. Apply the defect inequality once, to g^r and u_r:

\[
 |r q(gu)-r q(g)|=|q(g^r u_r)-q(g^r)-q(u_r)|\le D.
\]

Divide by r and let r tend to infinity. Thus q(gu)=q(g). This proves exact constancy on right cosets, so qbar(gN)=q(g) is well-defined. Its product defect and integer homogeneity follow by choosing representatives. No sum of r defect errors is used. Normality is essential to the claim that u_r belongs to N. End of proof.

For completeness, the amenable conclusion can be reconstructed directly. If f is a quasimorphism on an amenable discrete group H, choose a right invariant mean M on bounded functions of h. The function u_g(h)=f(hg)-f(h) is bounded and differs uniformly from f(g) by at most its defect. Define ell(g)=M(u_g). The identity u_{ab}(h)=u_b(ha)+u_a(h), followed by right invariance, makes ell a homomorphism; |ell(g)-f(g)|<=D. If f is homogeneous, apply this bound to g^r and divide by r to obtain ell=f. This reproduces the needed conclusion without importing an unproved stronger bounded-cohomology theorem.

Take G=P3 and N=G^(k). The subgroup N is characteristic, hence normal. The quotient G/N is solvable of derived length at most k, since quotient maps send the jth derived term onto the jth derived term. It is therefore amenable. If q vanished identically on N, descent and the amenable conclusion would force q on G to be a homomorphism, contrary to Section 2. Consequently

\[
 q\big|_{P_3^{(k)}}\not\equiv0\quad\text{for every finite }k\ge1.
\]

This conclusion concerns each finite depth separately. It does not produce one nontrivial braid in the intersection of all derived terms, and it does not assert any fixed commutator has nonzero q.

## 4. Independent reconstruction of the 1-solution obstruction

The needed statement is: if an algebraically split oriented link L has an integral smooth 1-solution W in Otto's sense, then its ordinary pointwise signature at -1 vanishes.

Let H2(W;Z) have the prescribed surface basis L_i,D_i, i=1,...,r. Let alpha send every meridian of the zero surgery M_L to -1. Since the zero-framed linking matrix is zero, H1(M_L;Z)=Z^m. The actual inclusion-induced H1 isomorphism extends this character over W. Its local coefficient system is one-dimensional, real and factors through Z/2. In particular both surface fundamental groups, lying in the commutator subgroup of pi1(W), act trivially.

Choose cellular lifts in a finite CW structure for W. A twisted boundary matrix evaluates group elements to +/-1. Modulo 2 it becomes exactly the ordinary cellular boundary matrix. A minor nonzero over F2 has odd determinant and stays nonzero over Q. Therefore rank_Q(d_j^alpha)>=rank_F2(d_j) for each j. The chain dimensions agree, so

\[
 \dim_Q H_2(W;Q_\alpha)\le\dim_{F_2} H_2(W;F_2)=2r.
\]

The last equality uses the integral universal coefficient sequence: H2(W;Z) is free on the given basis, while H1(W;Z)=Z^m has no 2-torsion. This inequality uses neither a generic character nor an Alexander-root restriction.

Because each basis surface has trivial restricted local system, its fundamental class gives a twisted 2-cycle after choosing a trivialization at a point. The twisted intersection matrix of the 2r classes is hyperbolic: framed self-intersections vanish, surfaces with different indices are disjoint, and each dual pair meets exactly once, with coefficient +1 or -1 in this rank-one system. Rescale one class per pair to get off-diagonal +1. Hence the 2r classes are linearly independent. The upper bound makes them a full basis of twisted H2. Thus the twisted intersection form has signature zero, as does the ordinary hyperbolic intersection form. This treats possible ambient radicals by dimension saturation; none are silently discarded.

The surgery step is [Toffoli, published 2022](https://epub.uni-regensburg.de/52299/1/the-atiyahpatodisinger-rho-invariant-and-signatures-of-links.pdf), bounding formula (1.1), Remark 4.25/equation (4.21), or Corollary 4.28. In the single-colour, zero-linking situation, the Seifert framing is zero and its entire framed linking matrix vanishes. The surgery formula gives rho_alpha(M_L)=-sigma_L(-1); the bounding formula gives rho_alpha(M_L)=sigma(W)-sigma_alpha(W)=0. Corollary 4.28 permits every non-1 unit value. It applies to a link, not only a knot; the meridian character is the one already extended above. No average over signatures is substituted. The cited early-view PDF positions 31--32 correspond to journal pp.434--435. A global reversal of the signature convention changes both sides and does not affect vanishing.

This is the same universal topological obstruction as in the submitted proof, reconstructed here rather than inferred from a finite word computation. Its proof and imported surgery formula do not assume closure signature is a homomorphism on string links or that unbased closed links carry a stacking operation.

## 5. Closing the implication and checking quantifiers

Fix finite k>=1. Suppose every braid in P3^(k) represents a member of F1^3. If beta is in P3^(k), every positive power beta^r is still in that subgroup. Its pairwise linking numbers are zero: linking numbers are homomorphisms on P3 and vanish on P3', which contains every positive derived term. By the assumed containment and the preceding obstruction, s(beta^r)=0 for every r. Therefore q(beta)=0. Since beta was arbitrary, q vanishes identically on P3^(k), contradicting Section 3. This proves noncontainment.

Equivalently choose beta in P3^(k) with q(beta)!=0. For a sufficiently large r, s(beta^r)!=0; the bound |s-q|<=6 even gives the sufficient condition r|q(beta)|>6. Thus gamma=beta^r supplies a checkable existential non-1-solvable closure in the same derived term. **One cannot omit this power step and infer s(beta)!=0 solely from q(beta)!=0.** The proposed mechanism itself, phrased as a contradiction of containment, uses the power step correctly.

The full F1 subgroup theorem is true, but this contradiction needs only that the derived term is closed under powers. This avoids any extra claim about powers of an arbitrary link under an undefined operation.

For n>=1 put k=n+2 and use Fn^3 subset F1^3. For m>3, add split trivial strands to gamma. This is a braid homomorphism, preserves kth-derived membership, and preserves ordinary signature by a zero summand in a Seifert form. Apply the same 1-solution obstruction with m meridians and then the same filtration nesting. This proves the two formulas in the disposition for every m>=3.

For m=1, P1 is trivial; for m=2, P2 is infinite cyclic. Their positive derived terms are trivial and are contained in every filtration term. The k=0 group P3 also fails containment in F1 (already a has nonzero linking), but the algebraic-splitting argument above deliberately starts at k=1. No conclusion about F0 or fractional filtration levels is being smuggled into the result.

## 6. Historical disposition and exact limits of the search

Old ingredients establish the mathematical deduction but do not, by themselves, identify a previous complete solution. The primary-source search and body inspections are logged in SEARCH_LOG.json. No full published theorem with the displayed universal derived-depth noncontainment and its complete closure-solvability bridge was identified in this review.

Gambaudo--Ghys supplies the signature quasimorphism and its exact small-strand values. Its actual body has no derived-series or solvable-filtration statement. Calegari supplies the general amenability theorem, not the link application. Otto gives relevant pure-braid commutator examples, but Theorem 5.3 is a nonabelian quotient result and does not state an obstruction at every derived depth. This audit does not mistake its second-derived example for membership in the third derived term.

[Brandenbursky--Kedra (2015)](https://msp.org/agt/2015/15-5/agt-v15-n5-p11-s.pdf), Proposition 3.6, explicitly uses the known nonhomomorphy of homogeneous signature on B3, and Section 4 contains exact signature examples. The paper's closure-to-knot quasihomomorphism and first commutator results do not supply the source question's every-derived-depth/string-link F1 bridge. [Brandenbursky's arXiv:0907.2626v4, 2 July 2012](https://arxiv.org/pdf/0907.2626v4) concerns braid/knot quasimorphisms and Hamiltonian applications. Its body was searched and the relevant construction read; no such bridge was located.

[Cochran--Harvey--Horn, arXiv:1003.4977v3, 2 August 2011](https://arxiv.org/pdf/1003.4977v3), Example 2.4 and Proposition 7.1, explicitly relate higher-order rho invariants to pure-braid closures and their zero surgeries. They do not in those statements prove nonvanishing of this ordinary q on every finite P3 derived term or the required noncontainment conclusion. Theorems about genus>=2 Torelli/Johnson subgroups or a free surface group's derived series cannot be substituted for the precise pure-braid statement without a further argument. This route is recorded as related machinery, with that exact missing historical bridge, rather than as a defeat.

The Rice repository download for the published Cochran--Harvey--Horn file returned non-PDF bytes locally. The version-specific arXiv v3 full body was then retrieved and pinned. This review makes no claim to have authenticated the inaccessible published bytes. No outside person was contacted. Some indexed results were irrelevant; neither their existence nor empty text searches certify absence. The Calegari errata URL attempted by the web tool was inaccessible; the needed proposition also has the direct proof above.

After the independent reconstruction, the parent supplied a new lead: [Kawasaki, Kimura, Maruyama, Matsushita and Mimura, The space of nonextendable quasimorphisms, AGT25 (2025), 1169--1226](https://msp.org/agt/2025/25-2/agt-v25-n2-p15-s.pdf), published 16 May 2025. Its actual PDF was authenticated and Lemma 7.12, printed p.1207/PDF p.40, visually inspected together with its proof and preceding Lemma 7.10. It states D_G(f)=D_N(f|N) whenever G/N is solvable. Applying it with N=G^(k) shows that a nonhomomorphic homogeneous quasimorphism stays nonhomomorphic on each finite derived term. Thus a stronger general group fact is explicitly prior literature. It must receive credit; the group lemma here is not a novelty claim. The paper's braid discussion, printed pp.1220--1221, concerns mixed stable commutator length. No complete ordinary-closure-signature/F1 noncontainment bridge was identified there. This is a prior lemma, not an identified earlier whole answer to the source question.

Thus mathematical verification is complete for this mechanism. Historical priority remains a bounded-search conclusion: no complete predecessor established here, no exhaustive absence, no current-open or firstness assertion, and no publication authorization. Further historical evidence could change that disposition without changing the mathematical proof. The original explicit construction remains independently meaningful, and the stronger existential theorem must be credited to the separately recorded new mechanism and its classical inputs.

## 7. Review of the root's complete candidate and native accounting

After recording the independent argument above, this reviewer read the root candidate at `strengthening/unsolved_math_prioritization/attempts/30003634/PROOF.md`, authenticated SHA256 `8fbe6571b9dd691ca5b78a70bfb5ac0361607a0b3c196dfe527ba2180fcd9fb6`. Its complete inference, including the left-invariant-mean variant, exact pure-braid relation, full-twist asymptotics, taking a power, each-finite-depth quantifiers and split-strand extension, agrees with the independently reconstructed proof. No mathematical logic or quantifier correction is required. The 2025 lemma requires the exact attribution just supplied when the candidate is promoted; its placeholder acknowledgment already avoids claiming a new general group theorem. The universal topology proof above supplies the details abbreviated in that candidate.

The root supplied `NATIVE_TURN_RECEIPT.json`, `ATTEMPT_LEDGER.json`, `NATIVE_HISTORY.jsonl` and `READINESS.json`. All were read completely. The four history records have counts 0,1,1,2; their candidate_turn entries are 1 and 2. The final state equals the last history record, and its evidence equals READINESS. Only target 30003634 occurs. Current shared queue.py, state.json, history.jsonl and QUEUE.md hashes equal the receipt's supplied pins. This is a read-only crosscheck of the receipt, history, code and current bytes; this reviewer did not reexecute native mutations or independently observe the earlier child processes.

The accounting distinction is correct: the immutable original says 1/5; the isolated native turn1 event is a reconciliation recorded now, expressly not a backdated historical CLI invocation. Turn2 is the one newly developed stronger mechanism. Verification adds zero, giving the documented combined total 2/5 in the isolated selected ledger. The shared global ledger remains unchanged by this review and by the recorded parent operations under the receipt pins. Publication acceptance is false.

One implementation detail must be preserved in interpretation: native status() copies prior fields, so the third history record (an in_progress status update) retains `event=proof_attempt_turn` while turns_used stays 1 and candidate_turn is removed. Counting raw event-tag occurrences would incorrectly report three turns. The exact unmodified code explains this inherited tag; actual count transitions and candidate_turn entries establish two substantive turns. No native history was edited to conceal or normalize it. ROOT_CANDIDATE_REVIEW.json records the pins and this caveat.
