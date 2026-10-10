# Audit of the twice punctured surface potential theorem

## Verdict and exact scope

The original conjecture has a prior positive resolution. The accepted statement is: for every compact connected oriented surface of genus at least one, with empty boundary and exactly two marked points, and every tagged triangulation, its quiver has a nondegenerate potential, and all its nondegenerate potentials belong to one weak right equivalence class over every algebraically closed field. There is no characteristic zero assumption.

Credit belongs to Jan Geuenich, Daniel Labardini-Fragoso and José Luis Miranda-Olvera. Their Theorem 1.1(2) and Theorem 4.1 appear in arXiv:2008.10168v1 and in *Séminaire Lotharingien de Combinatoire* 84 (2022), Article B84c. The [journal record](https://www.mat.univie.ac.at/~slc/wpapers/s84geuen.html) explicitly records acceptance and the final version on February 8, 2022. The [journal PDF](https://www.mat.univie.ac.at/~slc/wpapers/s84geuen.pdf) has 21 pages. This published resolution is the source of the theorem; the mathematical checks below address its precise hypotheses and formulas.

Acceptance includes the elementary indexing corrections and zero-case conventions specified in PROOF_CORRECTIONS.md. Several printed formulas, retained in the journal version, are not literally valid as written. The corrected formulas follow directly from the pictured quiver and the stated substitutions. Their verification leaves no unresolved gap in this target. This source-credit audit and the authored local corrections are AI-assisted and unrefereed, with no external human peer review claimed. No new solution, novelty, priority, formal machine proof, or author-issued erratum is claimed.

## Original statement and conventions

The [Oberwolfach report](https://ems.press/content/serial-article-files/46490), printed pages 3390–3392, fixes an algebraically closed field, works in the complete path algebra, defines nondegeneracy by arbitrary finite mutation sequences, and poses the two-puncture uniqueness conjecture. Its PDF pages 12–14 were inspected visually. The separately stated once-punctured phenomenon does not replace this target.

Write R for the vertex algebra and m for the arrow ideal. A potential is a possibly infinite sum of cycles, considered modulo the m-adic closure of cyclic differences. Weak right equivalence permits an idempotent-fixing continuous automorphism and multiplication by a nonzero scalar. These conventions agree with Definition 2.1 in the [2020 preprint](https://arxiv.org/pdf/2008.10168v1), page 3. All substitutions checked here fix R and have either invertible diagonal linear part or identity linear part. They are therefore automorphisms of the completed algebra, not merely polynomial substitutions or endomorphisms.

The target includes genus one, arbitrary algebraically closed positive characteristic, all tagged triangulations, and infinite potentials. It does not assert ordinary right equivalence without a scalar, uniqueness over arbitrary nonclosed fields, uniqueness of every potential, or a result for one puncture.

## Existence and transport to every tagged triangulation

Labardini-Fragoso's [Removing boundary assumptions](https://arxiv.org/pdf/1206.1798v5), Theorem 8.1 and Corollary 9.1, PDF pages 30–32, provide compatibility of the surface potentials with tagged flips and their nondegeneracy. The positive-genus closed-surface clause explicitly permits any positive number of punctures. The excluded small spheres are irrelevant. The construction uses any choice of nonzero puncture coefficients and has no characteristic zero or uncountability assumption. In particular, setting both coefficients to one supplies existence in the exact target.

This use of an explicit surface potential is important. The generic DWZ existence theorem assumes an uncountable field and would not by itself cover an algebraic closure of a finite field. It is not the existence argument used here.

Fomin–Shapiro–Thurston [Cluster algebras and triangulated surfaces, Part I](https://arxiv.org/pdf/math/0608367), Proposition 7.10, PDF page 28, connects all tagged triangulations by finite tagged flips except for the one-puncture closed case. Two punctures satisfy this proposition. Their following Theorem 7.11 has a two-puncture exclusion for a different assertion about cluster complexes; importing that exclusion into Proposition 7.10 would be an error.

DWZ [Quivers with potentials and their representations I](https://arxiv.org/pdf/0704.0649), Theorems 4.6, 5.2 and 5.7, make reduced QP mutation well defined on right equivalence classes and involutive where the mutated vertex has no incident 2-cycle. Nondegeneracy guarantees that condition along each finite sequence. Mutation also preserves weak right equivalence: the premutation of a scalar multiple differs from the scalar multiple of the premutation only in its newly added cubic terms; rescaling one family of reversed arrows corrects that factor. This works for every nonzero scalar over every field. Splitting and reduction then preserve the weak equivalence, and involutivity gives a bijection on nondegenerate weak equivalence classes.

Consequently, it is enough to audit uniqueness for the one explicitly pictured ideal triangulation. There is no assumption that every triangulation satisfies the favorable combinatorial conditions used in Section 2. Self-folded configurations and tag changes are handled by the imported tagged-flip theorem.

## The test triangulation and the first normal form

Put n=4g. In the fan triangulation of Figures 3 and 4, there are n triangles, 6g arcs and two punctures. Their valencies are 2n and n. Every puncture has valency at least four. The associated quiver has no loops, 2-cycles or parallel arrows in the same direction. The explicit incidence model in PROOF_CORRECTIONS.md verifies these properties also for g=1.

Each arrow has exactly two possible successors. The permutation f follows triangles; the other successor permutation, denoted h here to avoid confusing it with the genus, follows punctures. Its two orbits have lengths n and 2n. A cycle either follows only f, only h, or has a transition between them. In the last case a cyclic rotation exposes two consecutive triangle arrows followed by the other continuation. A length-three mixed cycle would require a second arrow between the same two vertices, so mixed cycles have length at least four. This checks the cycle partition used in Lemma 2.2 without dividing by the number of rotations, including in positive characteristic.

Every triangle coefficient of a nondegenerate potential is nonzero. The exact input is the induced-cycle test of Geiss–Labardini-Fragoso–Schröer [The representation type of Jacobian algebras](https://arxiv.org/pdf/1308.0478v3), Proposition 2.4 and Corollary 2.5, PDF page 9. Their ambient convention is C, so it would be incorrect simply to quote these statements as arbitrary-field theorems. The particular argument is field-independent: restriction preserves nondegeneracy by Labardini-Fragoso [Quivers with potentials associated to triangulated surfaces](https://arxiv.org/pdf/0803.1328), Proposition 21 and Corollary 22, PDF page 12. On an induced directed cycle, successively shortening the cycle by mutation reaches a triangle. If its primitive-cycle coefficient is zero, mutation of that triangle leaves an uncancellable 2-cycle. This argument uses no division by an integer. It verifies the needed implication over the present K. On each triangle the no-parallel-arrow condition supplies precisely that induced cycle.

Since the triangle orbits are disjoint, scaling one arrow of each triangle normalizes its coefficient to one. Thus a nondegenerate potential is right equivalent to T+U, where T is the sum of the triangle cycles and U has order at least four and is rotationally disjoint from T. This proves the use of Lemma 2.4 at its actual hypotheses.

## Elimination of nonpuncture terms

Lemma 2.5 removes the shortest pure-triangle or mixed contribution by a unitriangular substitution. If its length is L, the substitution changes an arrow first in length L−2 and has depth at least L−3. Its linear effect on T cancels the chosen contribution. The change in a remainder of order at least four begins in length at least L+1. In the mixed case the quadratic and cubic substitution errors have lengths at least 2L−3 and 3L−6, respectively, also greater than L for L≥4. The last displayed bound on page 7 has an A_g/A_f typographical error, corrected in the companion note.

Proposition 2.6 always processes a shortest one of the two unwanted types. Its unwanted remainder order increases by at least one every two steps. The newly accumulated puncture-only part changes only in degrees strictly above the just-processed degree. Thus the unwanted remainder tends to zero, the puncture series converges degree by degree, and the depths of the substitutions tend to infinity. It follows that T+U is right equivalent to T+W, with W a possibly infinite sum of powers of the two puncture cycles. This is a convergent formal normal-form operation and imposes no finiteness assumption on the original potential.

For completeness, the convergence criterion does yield an automorphism: for any fixed N, all sufficiently late substitutions induce the identity on the algebra modulo m^N. The finite composites and their inverses stabilize there. The compatible inverse system of these maps defines inverse continuous automorphisms of the completed algebra. The cyclic-difference space is closed, so cyclic equivalences survive the limit. This also checks the imported Lemma 2.4 of Removing boundary assumptions, rather than interpreting its limit as a merely pointwise map.

## Both primitive puncture coefficients must survive

Write the two puncture cycles as A and P, of lengths n and 2n. Let the coefficients of A and P in W be y and z.

The full subquiver on the n radial arcs is exactly the directed n-cycle A. Restriction and the induced-cycle test give y≠0.

For z, Proposition 4.4 mutates every outer arc once. These vertices are pairwise nonadjacent, so the premutations do not interfere at a later outer vertex. Each produces four composites. After all outer mutations, the diagonal composites d_j=[b_j c_j] pair with a_j in quadratic terms of coefficient one. The off-diagonal composites D_j=[b_j c_{ι(j)}], where ι pairs the two sides carrying the same polygon label, remain.

The printed sum indexed by all j from 1 to 2g is wrong for g≥2 under the displayed arrow numbering. The correct summation is over the first two entries of each block of four, pairing j with j+2. The mate-involution formula in PROOF_CORRECTIONS.md removes this ambiguity. The same indexing slip remains in the journal's page 19.

An explicit splitting verifies that these slips do not affect the conclusion. Set e_j=c_j* b_j*. The part involving the removable arrows has the form

    sum_j (a_j+e_j)d_j + F(a_1…a_n),

where F(t)=yt+terms of order at least two. First replace a_j by a_j−e_j. Expand F((a_1−e_1)…(a_n−e_n)), and cyclically write the difference from F((-e_1)…(-e_n)) as sum_j a_j R_j. Each R_j has length at least n−1 and contains no d or D arrow. The substitution d_j↦d_j−R_j finishes the splitting. Both changes are unitriangular and fix every D_j and every reversed arrow. This is a direct check of the source's splitting step, valid for formal series.

In the reduced quiver, the full subquiver on the radial arcs consists exactly of the D_j. These form one simple directed n-cycle D: in each block, the radial traversal is 4h→4h+3→4h+2→4h+1→4h+4, cyclically across blocks. The restricted reduced potential is zD plus powers D^r with r≥2. Neither the splitting correction nor the new cubic terms contributes a D-only cycle. Restriction and the same induced-cycle test force z≠0. This proves the exact Proposition 4.4 conclusion in every genus, without relying on a genus-one picture or an unverified identification of the whole mutated quiver.

## Removal of higher puncture powers

At this point the potential is S(x_p,x_q)+V, with both x_p,x_q nonzero and V containing only powers at least two of the puncture cycles. Its order is at least 2n=8g.

Lemma 2.7 replaces a mixed cycle with a long puncture segment by a longer one with that segment shortened by one arrow. The substitution cancels the original term against T. Its change in the baseline puncture potential contributes the new mixed term. The identity hf^−1=fh^−1 follows from the involution exchanging the two continuations. The new cycle gains L_p−3 arrows, where L_p≥4 is the affected puncture valency, so its length strictly increases. If the fixed cutoff is m, the other errors have order greater than m from the two inequalities used in the source: the old remainder has order at least m and twice the processed length minus three exceeds m.

Corollary 2.8 applies this move a finite number t of times. In its use here the trailing path is one arrow, so t is the processed length minus three. The final mixed term has length at least twice that initial length minus three, hence greater than m. Proposition 2.6 turns these errors into puncture powers without decreasing their order. The terminal t=0 is a stopping case, not an additional invocation requiring a positive t.

In Lemma 4.3, for a puncture cycle G of length L and a current least exponent r≥2, the arrow substitution

    a ↦ a − (λ_r/x) a G^(r−1)

cancels λ_r G^r through the baseline term xG. The extra triangle contribution has length L(r−1)+3. Its doubled length minus three is 2L(r−1)+3≥Lr+3, greater than the cutoff m≤Lr. Corollary 2.8 therefore pushes this contribution past m. Cancelling the least exponent at each of the two punctures leaves a puncture-only remainder of order greater than m.

The source assigns exponent infinity to a missing series but then writes a formula with that exponent. The rigorous convention is to skip that step and use the identity. The undefined coefficient λ_q,n in the second arrow substitution is λ_q,r_q,m. These are explicitly corrected, not silently evaluated.

The resulting composite at cutoff m has depth at least

    min(m−3, L_p(r_p−1), L_q(r_q−1)),

omitting absent terms. Since Lr≥m and r≥2 imply L(r−1)≥m/2, these depths tend to infinity. A zero remainder thereafter uses identity maps. The preceding inverse-limit argument produces an actual right equivalence to S(x_p,x_q). No division by r occurs; in particular r divisible by the characteristic causes no obstruction.

## Nonzero coefficients and algebraic closure

The remaining standard potentials have one weak equivalence class. The source cites GLS Lemma 8.5; Removing boundary assumptions, Proposition 10.4, page 34, explicitly states the algebraically closed K version. Its hypothesis can also be checked directly on this fan.

Scaling all arrows by v and then dividing the potential by v^3 changes the two coefficients to y v^(n−3) and z v^(2n−3). Choose a nonzero v satisfying v^(3n−6)=(yz)^−1. Such a v exists over every algebraically closed field because 3n−6=12g−6 is positive; separability is unnecessary. The new coefficient product is one. Scaling a_1 by u and b_1 by u^−1 preserves each triangle coefficient, multiplies the A coefficient by u, and the P coefficient by u^−1. Choosing u to be the reciprocal of the new A coefficient makes both puncture coefficients one. Every scalar used is nonzero. This checks precisely where algebraic closure is used and why no restriction on characteristic is introduced by the C-based reference.

Together with tagged transport and existence, the audited chain proves the full original assertion.

## Verification limits and provenance

The arithmetic and quiver checks accompanying this audit are regression checks of the specified formulas. Finite tested genera or characteristics are not offered as a proof of the infinite theorem; the parameterized arguments above supply that proof audit. Imported published theorems are used at their checked hypotheses, rather than being re-proved in their full generality.

Public source identities and the precise inspection scope are recorded in VERIFICATION_METADATA.json. Those inspections belong to the accepted audit; preparation of this edition does not claim a fresh inspection of the sources. The complete authored mathematical argument is contained here and in PROOF_CORRECTIONS.md, with the cited published theorems used at their stated hypotheses. Finite regression checks are supplementary.
