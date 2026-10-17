# An exact counted-model connection from Deligne modules to Jacobian recognition

**Scope.** This is a theoretical, all-characteristic aggregate algorithm for an ordinary, absolutely simple abelian-threefold isogeny class. It combines the existing polarized Deligne classification and Marseglia algorithms with exact projective-model enumeration and Beauville–Ritzenthaler recognition. It has no useful complexity bound and is not an implemented geometric computation, a per-ideal inverse to Deligne's functor, a direct efficient criterion from a marked lattice, or a claim of worldwide novelty. Its content is the explicit count-certified connection between those established theories, not a new bare decidability headline.

## 1. Input, output and theorem

Let \(k=\mathbb F_q\), where \(q=p^r\), be supplied by exact finite-field arithmetic, and let \(h\in\mathbb Z[x]\) be a promised realizable degree-six Weil polynomial of an ordinary, absolutely simple abelian-threefold isogeny class over \(k\). One may equivalently construct a standard exact representation of \(k\) from \(q\). No test of the input promise is claimed or required.

**Theorem.** There is a terminating exact algorithm that decides whether that isogeny class contains the Jacobian of a smooth projective geometrically connected genus-three curve over \(k\). More precisely, it:

1. Computes the unweighted number \(N(q,h)\) of principally polarized \(k\)-isomorphism classes with Weil polynomial \(h\), using all Deligne ideal classes and all principal-polarization orbits.
2. Produces a complete **unlabeled** set of exactly \(N(q,h)\) exact theta-equipped projective models, one for every such polarized class. The Deligne count certifies both completeness and the stopping time of this model enumeration.
3. Decides, for every model, whether its specified principal polarization is the canonical polarization of a Jacobian over \(k\), using exact Beauville–Ritzenthaler geometry and an odd-extension descent test.
4. Returns YES if at least one answer is YES, and NO otherwise.

A polarized isomorphism here is a group isomorphism over \(k\) preserving the polarization morphism. It need not preserve an initially chosen theta divisor. The output models are not labeled by individual fractional ideals; no arbitrary ideal-to-model matching is used. A curve equation is an optional stronger output, not part of the decision theorem.

Absolute simplicity ensures that every resulting ppav is geometrically indecomposable. Ordinarity is used in the Deligne-count stage, not in the geometric recognition stage. Both characteristics two and three are included.

## 2. Relation to the source question

Howe's 2006 IPAM talk, *Low-genus curves over finite fields: Problems and variations*, asks on PDF pages 37–38 whether the recognition approaches can be connected to the Deligne-module description to decide Jacobian existence in an ordinary absolutely simple threefold class specified by its Weil polynomial. The question is about a Jacobian over the original finite field and about existence somewhere in the class. Those slides impose neither an odd-characteristic restriction nor a complexity requirement. [Howe 2006](https://ewhowe.com/talks/IPAM.pdf)

The theorem above supplies a literal no-complexity-bound, set-level connection: the polarized Deligne count is essential to the exhaustive stopping certificate, and the resulting exact geometric models are essential inputs to the recognition theorem. It does not attach unused module information to an exhaustive genus-three curve search. On the other hand, this weak aggregate interface does not establish that the historical research direction has reached its intended practical endpoint. The broad historical problem is not declared solved, and no priority claim is made for this synthesis.

Principal polarizability is not the unresolved step for this promised class. Howe's Theorem 1.2 already gives a principally polarizable member in every simple odd-dimensional finite-field isogeny class. The required remaining distinction is the finite-field descent character of each polarized object. Rejecting a single polarization cannot justify rejection of the whole isogeny class. [Howe 1996, reproduced preprint](https://arxiv.org/abs/2001.05111v2)

For clarity, finite enumeration of genus-three curve equations already provides an elementary decidability baseline. That observation does not itself connect the Deligne description to a recognition procedure. The present theorem claims the counted-model connection just stated, rather than that baseline as a new result.

## 3. Algorithm overview

First execute Sections M2–M6 to obtain the complete polarized model set. On each returned model execute Sections G1–G6. The main geometric algorithm uses the finite rational-line test in G5; the Clifford-algebra, determinant and Artin–Schreier calculations are separately proved alternatives.

All searches are over explicit finite encodings or finite fields, and each candidate is subjected to terminating exact tests. Four potentially unbounded searches have specific stopping proofs:

- Number-field ideal and unit computations use the established exact algorithms underlying the finite polarized count.
- The model enumeration stops on reaching the exact count \(N\), after certified polarized deduplication.
- The prime-to-characteristic torsion search stops when all \(M^6\) torsion points have split.
- The good-point search uses only odd extension degrees and stops by Lang–Weil on a nonempty geometrically integral open subset.

No step stops merely because an approximation looks stable or because no new model has appeared recently. No recognition step is supplied an unverified complex period matrix in place of algebraic input.

# Part I  The exact count and complete projective model set

## M2. Exact arithmetic count

For the promised input, \(h\) is irreducible and square-free. Indeed, the simple Honda–Tate class has \(h=m^e\), where the exponent comes from the denominators of the local invariants. Ordinary slopes are zero and one, and there are no real Weil roots, so those denominators are one. In particular the square-free hypotheses below apply.

Set
\[
 K=\mathbb Q[x]/(h),\qquad \pi=x\bmod h,\qquad
 R=\mathbb Z[\pi,q/\pi],\qquad \bar\pi=q/\pi.
\]
Compute representatives \(I\) of **all** full fractional \(R\)-ideal classes, including classes noninvertible in their multiplicator rings. The following explicit version of the established ideal-class-monoid routine makes its arbitrary-order scope clear; no Bass or Gorenstein hypothesis is imposed.

For every over-order \(S\) between \(R\) and the maximal order \(\mathcal O_K\), set \(\mathfrak f=(S:\mathcal O_K)\). There are finitely many over-orders, found among the additive subgroups of \(\mathcal O_K/R\), with multiplication and identity checked by exact lattice arithmetic. Enumerate all \(S\)-submodules \(I\) with \(\mathfrak f\subseteq I\subseteq\mathcal O_K\), retain precisely those with \((I:I)=S\), and deduplicate them by the weak-equivalence test
\[
 1\in(I:J)(J:I).
\]
The finite quotient \(\mathcal O_K/\mathfrak f\) makes this enumeration finite. Marseglia's ideal-monoid Proposition 5.1, with \(T=\mathcal O_K\), proves coverage of every weak-equivalence class having multiplicator ring \(S\). Compute \(\operatorname{Pic}(S)\), and multiply every retained weak-class representative by each invertible ideal-class representative. Theorem 4.6 proves that these products give every isomorphism class with multiplicator ring \(S\), without duplicates. The strata for distinct multiplicator rings are disjoint. The filter \((I:I)=S\) is essential; applying \(\operatorname{Pic}(S)\) indiscriminately to all ideals would not have the asserted free action. This specifies a complete duplicate-free list \(\operatorname{ICM}(R)\).

Fix the CM type as in the polarized-variety paper's equation (5.1) and Algorithm 2:
\[
 \Phi=\{\varphi:K\hookrightarrow\mathbb C:
                v_p(\varphi(\pi))>0\}.
\]
The choice uses a prime above \(p\) and a compatible complex embedding; it is part of the Deligne convention, not a positivity test chosen independently.

Write \(J^t=\{z\in K:\operatorname{Tr}_{K/\mathbb Q}(zJ)\subseteq\mathbb Z\}\). The principal-polarization multipliers on \(I\) are
\[
 \mathcal P(I)=\{a\in K^\times:
 aI=\bar I^{\,t},\quad \bar a=-a,\quad
 \operatorname{Im}\varphi(a)>0\ (\varphi\in\Phi)\}.
\]
For \(S=(I:I)\), the equivalence is
\[
 a\sim a'\quad\Longleftrightarrow\quad
 a=\bar u\,a' u\quad\text{for some }u\in S^\times.
\]
Marseglia's Theorem 5.4 classifies these multipliers, and his principal-polarization orbit method computes a finite representative set. For definiteness, use the fully guarded degree-one procedure proved below, which directly checks the scalar ideal equality before counting any multiplier. Therefore
\[
 N(q,h)=\sum_{[I]\in\operatorname{ICM}(R)}
               |\mathcal P(I)/S^\times|
\]
is a computable **unweighted integer**: the number of principally polarized \(k\)-isomorphism classes with Weil polynomial \(h\). It is not the mass weighted by automorphism orders, an unpolarized class count, or a geometric class count. Different representatives \([I]\) cannot become isomorphic as polarized objects over \(k\), because that would already give an unpolarized \(k\)-isomorphism.

The number-field operations can be carried out by terminating certified algorithms, without GRH. A specific unconditional dependency is Lenstra's Theorem 5.4 and the following construction in *Algorithms in algebraic number theory*: finite bounded-height \(S\)-unit enumeration and the displayed exact sequence compute full units and the class group. Here the letter \(S\) in Lenstra's \(S\)-unit terminology denotes a finite set of primes, not the order denoted \(S\) above. Marseglia's ideal-monoid Remark 3.8 transfers the maximal-order computations to arbitrary orders through finite conductor quotients. Use these terminating procedures for unit groups, Picard groups and principal ideal decisions, rather than relying on an unproved termination claim for a provisional software computation followed by attempted certification. No tentative complexity estimate from Lenstra's Theorem 5.5 is needed.

Likewise no floating-point sign decision or numerical recognition step is used: signs of nonzero algebraic imaginary parts are decided by exact real-algebraic isolation. All subsequent stages use only the resulting integer \(N\); its ideal list and polarization orbits remain the completeness certificate.

### A complete degree-one ideal-isomorphism guard

Fix \(I\), put \(S=(I:I)\), \(H=\bar I^{\,t}\) and \(J=(H:I)\). All the following equalities are equalities of full integral lattices and are decidable by exact integer linear algebra.

1. Compute the fractional \(S\)-ideal \(J\).
2. Test invertibility by \(J(S:J)=S\). If this fails, there is no scalar isomorphism \(I\to H\).
3. For invertible \(J\), use a terminating certified principal-ideal algorithm for the order \(S\). Reject if \(J\) is not principal. Otherwise obtain a nonzero generator \(x_0\) with \(J=x_0S\).
4. Check the actual equality \(x_0I=H\). Reject if it fails; otherwise retain \(x_0\) as a certified scalar isomorphism.

Success is sound by the final equality. For completeness, if \(aI=H\), then
\[
 J=(aI:I)=a(I:I)=aS.
\]
Thus \(J\) is invertible and principal. Every generator is \(x_0=au\) for some unit \(u\in S^\times\), and \(uI=I\), so every generator satisfies \(x_0I=H\). Hence none of the rejection branches can reject a genuine scalar isomorphism. If one generator fails the final equality, all generators fail, and no scalar isomorphism exists. This argument needs no unverified weak-equivalence premise. Equivalently one can use the full established ideal-isomorphism algorithm, including its weak-equivalence test.

This guard is a precision safeguard, not an assertion that a published algorithm fails in the special conjugate-dual setting. It prevents the operational count from replacing the required condition \(aI=H\) by a principal-colon condition alone.

### Complete principal-polarization enumeration after the guard

After success, every scalar isomorphism \(I\to H\) is exactly \(x_0u\), \(u\in S^\times\). The trace dual has the same multiplicator ring as the original ideal, giving
\[
 (H:H)=(\bar I^{\,t}:\bar I^{\,t})=\bar S.
\]
The equality \(H=x_0I\) also gives \((H:H)=S\), so \(S\) is conjugation-stable. Therefore
\[
 \mathcal N(S^\times)=\{v\bar v:v\in S^\times\}\subseteq S^\times
\]
is a subgroup generated by the norms of a finite set of unit-group generators. The quotient \(S^\times/\mathcal N(S^\times)\) is finite: for a CM unit \(u\), the algebraic integer \(u/\bar u\) has every complex absolute value one and is a root of unity. If its order is \(w\), then \(u^{2w}=(u\bar u)^w\). Every unit class in the quotient is thus torsion, and a finitely generated torsion abelian group is finite. Exact unit coordinates and integer normal forms compute quotient representatives.

For each quotient representative \(u\), set \(a=x_0u\). Retain it exactly when
\[
 \bar a=-a,\qquad \operatorname{Im}\varphi(a)>0\quad(\varphi\in\Phi).
\]
The equality \(aI=H\) already holds, and may also be rechecked explicitly. The tests are invariant under multiplication by \(v\bar v\), because every complex embedding of that element is strictly positive real. Marseglia's polarization theorem therefore identifies the surviving quotient classes exactly with the principal-polarization isomorphism classes on \(I\). This proves soundness and completeness of the exact count, including the noninvertible-ideal cases.

## M3. Recursively enumerable, decidably valid presentations

A candidate is finite data over \(k\) consisting of:

1. Homogeneous equations for a closed subscheme \(A\subset\mathbb P^{26}_k\), and homogeneous equations for \(\Theta\subset A\).
2. A point \(e\in A(k)\), and finite affine-chart descriptions of morphisms \(m:A\times A\to A\) and \(i:A\to A\).
3. Finite local data certifying that \(\Theta\) is an effective Cartier divisor and that
   \[
     \mathcal O_A(1)\simeq\mathcal O_A(3\Theta).
   \]

Such data can be enumerated by increasing finite encoding length. A map description uses finite principal-open refinements of standard affine charts, ring maps given by polynomials and fractions with certified invertible denominators, and compatible maps on overlaps. A line-bundle isomorphism uses finite trivializing covers, units and their inverses, with checked transition equations. These are ordinary finite algebraic data, not assertions accepted on trust.

Perform the following terminating checks:

- \(A\) is smooth, of dimension three, and \(H^0(A,\mathcal O_A)=k\).
- Its Hilbert polynomial relative to the given embedding is \(27t^3\), and its saturated ideal has no nonzero linear form.
- All supplied local charts cover their claimed source schemes, denominators are invertible where used, maps agree on overlaps, and their images lie in the target schemes.
- The morphisms satisfy associativity, identity, inverse and commutativity as identities of morphisms, not merely on \(k\)-rational points.
- The local ideal of \(\Theta\) is generated by the stated non-zero-divisor on each chart, the divisor charts cover \(A\), and the line-bundle isomorphism displayed above holds.

Here is why these are effective checks. Gröbner bases compute ideal membership, saturation, Hilbert polynomials, annihilators and localization relations; chart covers are checked by emptiness of the closed complements, and morphism equalities by checking coordinate identities on a common finite refinement. The Jacobian/Fitting-ideal criterion decides smoothness over the perfect field \(k\). Computation of coherent-sheaf cohomology on projective schemes over a computable field is exact by graded-module, Gröbner-basis and syzygy algorithms; in particular \(H^0(A,\mathcal O_A)\) is computable. One may use Smith's Theorem 1 and Algorithms 3.3–3.6. None of these checks requires knowing whether \(A\) is a Jacobian.

For clarity, a finite morphism description need not give a single homogeneous formula valid everywhere. Using multiple affine charts is essential for complete and honest group-law coverage. Every genuine morphism between these projective schemes admits the indicated finite descriptions by quasi-compactness. Every genuine line-bundle isomorphism and effective Cartier divisor likewise has finite local witnesses.

### Soundness of the presentation checks

Smoothness, projectivity and \(H^0(A,\mathcal O_A)=k\) imply geometric connectedness: after any algebraic field extension, flat base change leaves the algebra of global functions equal to that extension; the proper smooth scheme has no nontrivial idempotent and is connected. With the checked group axioms, \(A\) is an abelian threefold.

Put \(L=\mathcal O_A(\Theta)\) and \(H=\mathcal O_A(1)\). The certified equality \(L^{\otimes3}\simeq H\) makes \(L\) ample. Riemann–Roch on an abelian threefold gives
\[
 \chi(A,H^{\otimes t})=27t^3\chi(A,L).
\]
The checked Hilbert polynomial thus gives \(\chi(A,L)=1\). The polarization formula \(\deg\phi_L=\chi(A,L)^2\) shows that \(\lambda=\phi_L\) is principal. The index theorem for nondegenerate line bundles on abelian varieties says that cohomology is supported in a single degree. Here the displayed theta section makes \(H^0(A,L)\ne0\), and \(H\) is very ample, so in both cases that degree is zero. It follows that
\[
 h^0(A,L)=1,\qquad h^0(A,L^{\otimes3})=27.
\]
The 27 ambient linear forms restrict independently, since no linear form is in the saturated ideal. They therefore form the complete space of sections of \(L^{\otimes3}\). This proves that the given embedding really is a complete \(|3\Theta|\)-embedding.

### Completeness of the presentation enumeration

Every principally polarized \(k\)-abelian threefold has a theta divisor over \(k\): its theta-divisor torsor under \(A\) is trivial by Lang's theorem. Equivalently one may use the standard Picard descent and \(\operatorname{Br}(k)=0\). The associated line bundle \(L\) is ample with \(h^0(L)=1\), and \(L^{\otimes3}\) is very ample over \(k\). A \(k\)-basis of its 27-dimensional section space gives exactly an embedding of the required type. Its equations, group law, inverse, identity, Cartier charts and line-bundle identification are finite data over the finite field and therefore eventually appear in the enumeration.

Thus the accepted presentations cover every principally polarized \(k\)-isomorphism class, with possibly many redundant presentations and many theta translates.

## M4. A terminating exact Weil-polynomial fingerprint

This step filters accepted presentations to the specified isogeny class. It deliberately does not infer the six Frobenius coefficients from a few point counts on the threefold using the genus-three-curve formula.

Choose a prime \(\ell\ne p\), and a power \(M=\ell^s>40q^3\). Compute multiplication by \(M\) using the checked group law. For \(d=1,2,\ldots\), enumerate the finite set of projective points over \(k_d=\mathbb F_{q^d}\), retain those on \(A\) killed by \(M\), and stop as soon as their number is \(M^6\).

Termination is guaranteed because \(A[M]\) is finite étale with geometric group \((\mathbb Z/M\mathbb Z)^6\), hence all its points are rational over some finite extension. Its geometric cardinality is exactly \(M^6\), so the stopping condition is also an exact completeness test. One need not assume any bound for its splitting-field degree.

By finite exhaustive group calculations find a basis of this free \(\mathbb Z/M\mathbb Z\)-module. Apply the \(q\)-power map to the coordinates of each basis point and express the result in the basis. This gives the Frobenius matrix on \(A[M]\), hence its characteristic polynomial modulo \(M\).

If \(h_A=x^6+c_1x^5+\cdots+c_6\), the Weil bounds imply
\[
 |c_j|\le {6\choose j}q^{j/2}\le20q^3\qquad(1\le j\le6).
\]
Reduction modulo \(M>40q^3\) is injective on the integer interval \([-20q^3,20q^3]\). Consequently each coefficient is uniquely recovered as its centered integer representative. The characteristic polynomial on \(A[M]\) is the reduction of that on the \(\ell\)-adic Tate module, so this recovers \(h_A\) exactly. Retain the presentation if and only if \(h_A=h\).

Every step is finite arithmetic with known termination. A more practical exact Frobenius algorithm could replace this one without changing the proof.

## M5. Finite exact polarized-isomorphism testing

Let two accepted presentations be \((A,\Theta_A,e_A,m_A)\) and \((B,\Theta_B,e_B,m_B)\), in their complete \(|3\Theta|\)-embeddings. Put \(L_A=\mathcal O_A(\Theta_A)\) and \(L_B=\mathcal O_B(\Theta_B)\).

Enumerate every element \(G\in\operatorname{PGL}_{27}(k)\). Test, by equality of saturated homogeneous ideals, that \(G(A)=B\) and \(G(\Theta_A)=\Theta_B\) as schemes. For each such element let \(g=G|_A\), let \(b=g(e_A)\), and form
\[
 f=t_{-b}\circ g:A\longrightarrow B
\]
using \(B\)'s group law, where the subtraction is relative to \(e_B\). Verify directly that \(f\) respects the group laws. Return isomorphic exactly when some \(G\) passes these tests. The group is finite and all checks are exact.

**Soundness.** Such an \(f\) is a group isomorphism. Since \(g^*L_B\simeq L_A\) and translations do not change the polarization induced by a line bundle, \(f^*\lambda_B=\lambda_A\). Thus the accepted test is a polarized \(k\)-isomorphism. In fact the group-law check also follows from rigidity, but performing it explicitly avoids relying on that shortcut.

**Completeness.** Suppose \(f:A\to B\) is a polarized \(k\)-group isomorphism. Then
\[
 M_0=L_A\otimes(f^*L_B)^{-1}\in\operatorname{Pic}^0(A)(k).
\]
The principal morphism \(\phi_{f^*L_B}:A\to A^\vee\) is an isomorphism over \(k\), so there is \(x\in A(k)\) with
\[
 t_x^*f^*L_B\simeq L_A.
\]
Take \(g=f\circ t_x\). Equality here is equality of actual line bundles over \(k\): both sides are defined over \(k\), and the usual Picard descent ambiguity vanishes over a finite field (also the rational origin rigidifies line bundles). The two nonzero effective divisors \(g^{-1}(\Theta_B)\) and \(\Theta_A\) are the divisors of nonzero sections of the same line bundle \(L_A\), whose section space has dimension one. They are therefore equal. Moreover \(g^*(L_B^{\otimes3})\simeq L_A^{\otimes3}\), so, because both embeddings use complete section spaces over \(k\), \(g\) is induced by an element of \(\operatorname{PGL}_{27}(k)\). That element appears in the finite loop; translating its image of the origin back recovers the original group isomorphism \(f\).

This proves both directions. Crucially, the test preserves the actual theta divisor after a rational translation. It does not try to infer equality of principal polarizations by cancelling 3 from equal cubic polarizations. Thus there is no characteristic-three gap. Nor does it assume a polarized isomorphism preserves the initially chosen theta divisor.

## M6. Counted enumeration algorithm and proof of termination

Compute the integer \(N=N(q,h)\) in Section M2. If \(N=0\), return the empty list. Otherwise:

1. Enumerate the finite candidate data of Section M3 in increasing encoding length.
2. Reject data failing any presentation check.
3. Compute its Weil polynomial by Section M4 and reject it unless it is \(h\).
4. Compare it with all retained presentations by the finite test of Section M5. Retain it only if it is new.
5. Stop and return the list when it has exactly \(N\) entries.

Soundness gives an injection from the retained list into the finite set of polarized \(k\)-classes counted by \(N\). Completeness gives at least one finite candidate encoding for each of those classes. Each such encoding occurs at a finite position; there are only finitely many classes; and every preceding validation and deduplication operation terminates. Therefore after finitely many operations the retained list has \(N\) entries. At that point the injection between two finite sets of cardinality \(N\) is a bijection. This proves termination and completeness.

This is the precise role played by Deligne modules: they certify **when a model enumeration is exhaustive**, without a canonical-lift recognition oracle or an individual ideal-to-equations matching routine. Stopping merely because no new model appeared for some time would be invalid; stopping at the exact polarized count is what makes this a decision procedure.


# Part II  Exact geometric recognition and descent

Every output of Part I supplies the exact input required here: finite projective equations for a geometrically indecomposable principally polarized abelian threefold \((A,\lambda)\), exact group-law/inverse/origin data, and a \(k\)-rational effective Cartier divisor \(\Theta\) representing \(\lambda\). The model checks certify this contract; no extra realization oracle is assumed.

The recognition input is used scheme-theoretically. Equality, pullback and morphism operations refer to finite presentations on affine charts, not just tables on rational points. The theta divisor need not be symmetric.

The geometric theorems used below are Beauville–Ritzenthaler [BR], Proposition 2.1, Proposition 2.4, Proposition 3.1, Theorem 3.4, and, for the optional arithmetic alternatives, the even-Clifford paragraph preceding Proposition 3.5. They work over perfect fields and the statements used here do not exclude characteristic two. The odd-characteristic qualification in their §2.2 concerns a Prym identification not required below. Their §2.6 leaves an intrinsic equation for one exceptional component unresolved in characteristic two; the algorithm never uses that equation.

## G1. Detect the hyperelliptic case exactly

Test whether Θ is smooth over k using its equations and the Jacobian criterion on affine charts. Finite fields are perfect, so this is geometric smoothness. If Θ is singular, return YES. For a geometrically indecomposable principally polarized threefold, [BR, §3.3] identifies this as the geometric hyperelliptic case, and [BR, Proposition 3.1] says its Serre character is trivial. Thus this is a Jacobian over k, not merely over an algebraic extension.

Assume henceforth that Θ is smooth.

## G2. Find a certified good point over an odd extension

For n = 1, 3, 5, ... construct K = F_(q^n), enumerate every a in A(K), and form the scheme-theoretic intersection

    Y_a = Θ_K ∩ (Θ_K + a).

Accept the first a for which all of the following finite tests succeed:

1. Y_a is a nonempty smooth projective curve of pure dimension one.
2. dim_K H^0(Y_a, O_Ya) = 1.

All the tests are exact. Dimension and smoothness are computed from saturated homogeneous ideals or affine charts. Projective coherent-sheaf cohomology is computable by Gröbner bases and syzygies; [Smith, Theorem 1 and Algorithms 3.3–3.6] supplies a characteristic-independent algorithm. For a proper smooth K-scheme, the second condition is equivalent to geometric connectedness here: H^0 commutes with field extension, and a proper smooth scheme over an algebraically closed field has one copy of that field per connected component.

### Why this is the required good-point test

Over an algebraic closure, (A, λ) is a nonhyperelliptic genus-three Jacobian. Under any such polarized group isomorphism, Θ is a translate of the standard degree-two theta divisor. [BR, Proposition 2.1] states that Y_a is smooth and connected exactly when a lies outside their divisor Σ_A, and that the involution used below is then fixed-point-free. These statements are independent of the chosen geometric Jacobian identification. The algorithm only tests their left-hand side.

### Why the odd-extension search terminates

The exceptional set Σ_A is a proper closed subset of A of dimension at most two, defined over k. Here its existence and descent are theoretical facts from [BR, §3.3]: it is defined geometrically using a geometric Jacobian identification, is independent of that choice, and is Galois-stable. The algorithm does not construct that identification or the equations of Σ_A. This remains so in characteristic two: geometrically its two pieces are the image of a theta divisor under the finite morphism [2], and the image C−C of a surface. Hence U = A\Σ_A is a nonempty geometrically integral open variety of dimension three. Lang–Weil gives

    #U(F_(q^n)) = q^(3n) + O(q^(5n/2))

as n tends to infinity, with a constant depending on U. In particular U has a rational point over every sufficiently large extension, and therefore over a sufficiently large odd extension. Such a point passes both finite tests.

No explicit constant is needed for a terminating search, and no equation for U or Σ_A is used by the machine. Lang–Weil is the mathematical termination proof. This is not an assertion that U(k) is nonempty. For an accessible detailed statement of the estimate, see [Poonen, Theorem 7.7.1]; the original source is [Lang–Weil].

## G3. Construct the involution without a symmetric rational theta divisor

The principal polarization implies that there is a unique b in A(K) satisfying the exact divisor equality

    (−Θ_K) + b = Θ_K + a.

Existence and uniqueness are [BR, §3.3 and the paragraph preceding Theorem 3.4]. Uniqueness also proves rationality: the data are K-rational, so every Galois conjugate of b is b. Find b by enumerating the finite set A(K) and comparing the translated divisors scheme-theoretically. Define

    τ(z) = b − z.

This exchanges the two theta divisors and preserves Y = Y_a. For auditability one may additionally check τ² = identity and that the fixed subscheme of τ on Y is empty. The good-point test and [BR, Proposition 2.1] guarantee these checks. A symmetric theta divisor over K is unnecessary.

The free action is an action of the constant group C_2, including in characteristic two. It is not an action of μ_2. Its quotient π: Y → X is a finite étale torsor of degree two. By [BR, Theorem 3.4], X is a smooth nonhyperelliptic curve of genus four and its canonical image lies on a unique smooth quadric Q in P^3_K. Adjunction gives genus(Y)=7, consistently with the étale Hurwitz formula.

## G4. Obtain the canonical quadric without computing a quotient model

Compute the seven-dimensional space H^0(Y, Ω_Y/K), the exact matrix of τ* on it, and the invariant subspace

    W = ker(τ* − identity).

Because π is étale, Ω_Y/K = π* Ω_X/K. Faithfully flat descent identifies W with H^0(X, Ω_X/K); hence dim W = 4 in every characteristic. This is a kernel computation, not averaging by (1+τ*)/2. In characteristic two that averaging would be invalid.

Compute multiplication of differential sections and the kernel

    R = ker(Sym² W → H^0(Y, Ω_Y/K tensor Ω_Y/K)).

Pullback from X is injective, and the canonical image of a nonhyperelliptic genus-four curve has a unique quadratic relation. Therefore dim R = 1. In a chosen basis of W, any nonzero generator of R is the desired quadratic polynomial F(x_1,x_2,x_3,x_4). Its quadric Q = V(F) is smooth by [BR, Theorem 3.4]. Check this smoothness directly as a consistency certificate. The target space has dimension 18; the ten products have rank nine.

Everything in this step is effective from projective equations. The differential sheaf is obtained from the conormal/Euler presentations; tensor powers, pullbacks and products have finite module presentations. Smith's sheaf-cohomology algorithm computes global sections, and their transformations and products are obtained by exact module/rational-section equality. No genus-four equations, invariant-ring averaging, transcendental approximation, or zero test for a theta series is required.

### Explicit section-map arithmetic

There is no separate pullback-of-sections oracle hidden in the previous paragraph. To make the implementation interface explicit, represent Ω_Y by the conormal sequence and the kernel of the projective Euler map. Kernels, cokernels and tensor products of these graded modules are computed by syzygies. Smith's degree-zero Hom construction gives actual section representatives, not just their dimension. Choose the permitted truncation index r nonnegative. If a section is represented by a degree-zero map from R_(≥r) to a graded module M, its local representative on x_j≠0 is obtained from the image of x_j^r divided by x_j^r.

Y is geometrically integral: on a smooth curve the geometric irreducible components are disjoint, and geometric connectedness therefore leaves one component. Choose a nonempty affine chart with integral coordinate ring, and work in its computable fraction field E=K(Y). From the affine conormal presentation, row reduction over E finds a nonzero coordinate differential η, a basis of the one-dimensional E-space Ω_E/K. Each global section becomes f_i η for a rational function f_i. The given rational formulas for τ and the chain rule compute τ*(f_i η). Their difference from f_i η is another explicit rational multiple of η.

For any finite collection of such rational functions, clear their denominators and reduce the resulting numerators modulo a Gröbner basis of the affine ideal. Coefficient comparison gives a finite matrix over K whose kernel is exactly their K-linear dependence space. This computes W directly from the seven differences τ*(f_i η)−f_i η. After obtaining invariant basis elements g_j η, apply the same dependence calculation to the ten rational functions g_i g_j. The unique relation is F. Consequently computing the entire target H^0(Y,Ω²) is optional; the same kernel is obtained by exact rational-function arithmetic. Identity on the chosen dense chart is identity of global sections because Ω and Ω² are line bundles on an integral curve. This method works in every characteristic.

### Optional explicit quotient construction

If a quotient model is desired separately, there is also an elementary fixed-field recipe valid in characteristic two. Let E = K(Y), choose t with τ(t) ≠ t, and let x_i generate E over K. Define

    u = t + τ(t),  v = t τ(t),
    d_i = (x_i − τ(x_i))/(t − τ(t)),
    c_i = x_i − d_i t.

Each u,v,c_i,d_i is invariant. Their generated field L has E=L(t), and t satisfies T²−uT+v=0. Because t is not invariant, [E:L]=2, so L=E^τ. Elimination and normalization then give X. This optional construction is not needed for the decision algorithm.

## G5. Decide the ruling character by a finite rational-line test

The aggregate decision algorithm uses the following finite line test; it requires no Clifford-algebra implementation. Write \(B(v,w)=F(v+w)-F(v)-F(w)\) for the polar form. Enumerate all two-dimensional K-linear subspaces of K^4, for instance by their unique reduced row-echelon basis matrices. For a basis v,w of such a subspace, test

    F(v)=0,  F(w)=0,  B(v,w)=0.

These conditions are exactly the polynomial identity F(sv+tw)=0; thus they certify that its projectivization is a line on Q. There are finitely many subspaces. Return YES if any passes, and NO if none passes.

Here is a source-local justification of the converse, stronger than the general finite-field conic argument. If the constructed Q has a K-line, its unique geometric ruling is fixed by Galois, so the action on the two rulings is trivial. Theorem 3.4 gives ε_A=1. Conversely, if ε_A=1, Proposition 3.1 identifies (A_K,λ_K) with a Jacobian over K. Applying Proposition 2.4 to the same good-point construction shows that Q is K-isomorphic to the split quadric P^1×P^1, and therefore has a K-line. This applies to the special Q constructed here and uses no additional rational-point theorem for conics. It is not the false assertion that one K-point on an arbitrary smooth quadric proves that its rulings split. The test uses polynomial identities, not sampled values on Q(K).

### Optional Clifford algebra and scalar checks

Theorem 3.4 of [BR] identifies the Serre character of (A_K, λ_K) with the Galois action on the two rulings of Q. The paragraph preceding Proposition 3.5 identifies the corresponding degree-two étale algebra with the center Z(C^+(F)) of the even Clifford algebra. Thus the character is trivial exactly when that center is K×K.

A convention-free finite algorithm constructs the 16-dimensional Clifford algebra from

    e_i² = F(e_i),
    e_i e_j + e_j e_i = B(e_i,e_j),
    B(v,w) = F(v+w) − F(v) − F(w).

Use the ordered square-free monomials in e_1,...,e_4 as its basis. The eight even monomials form C^+(F). Solve linear commutator equations for its center, a two-dimensional finite étale K-algebra. Enumerate its elements and test z²=z. The algebra is split if and only if there is an idempotent other than 0 and 1. This is a finite exact test, in either characteristic. Return YES exactly in the split case.

Two faster equivalent scalar tests, with their normalizations fixed, are:

- If char(K) is odd, write F(x)=x^T M x with symmetric M, so an off-diagonal entry is half the corresponding cross-term coefficient. Test whether det(M) is a square in K*. The discriminant sign is (+1) in dimension four because (−1)^(4·3/2)=+1. Equivalently, in an orthogonal basis the Clifford volume element squares to the product of the four diagonal coefficients.
- If char(K)=2, put B into symplectic normal form and write

      F = a x_1² + x_1 x_2 + b x_2²
        + c x_3² + x_3 x_4 + d x_4².

  Set Δ = ab+cd. In the Clifford algebra, z=e_1e_2+e_3e_4 is central in the even part and satisfies z²+z=Δ. Thus the center is K[T]/(T²+T+Δ), so the test is Tr_(K/F_2)(Δ)=0. The image of w↦w²+w is exactly the trace-zero subspace: inclusion follows by telescoping the trace and equality by comparing kernel dimension one. A change of symplectic basis changes Δ by an Artin–Schreier element; the invariant algebra, rather than a memorized pseudo-discriminant convention, fixes the normalization.

Smoothness of Q ensures the polar form B is nondegenerate in the characteristic-two four-dimensional case. Indeed an alternating B with nonzero radical has radical dimension at least two; over a perfect field F restricts there to the square of a linear form, which has a nonzero zero, giving a singular geometric point.


## G6. Why an odd extension gives the base-field answer

For the nonhyperelliptic geometric Jacobian, let ε_A: Gal(kbar/k) → {±1} be the Serre character of [BR, Proposition 3.1]. It is trivial exactly when (A,λ) is a Jacobian over k. The character of A_K is its restriction. If s=ε_A(Frob_q), then

    ε_(A_K)(Frob_(q^n)) = s^n = s

because n is odd. Hence the character over K is trivial if and only if the original character is trivial. Returning the split status of Q over K therefore gives exactly the answer over k. Passing instead to an arbitrary even extension could erase the obstruction and would make the algorithm unsound.

This proves termination and correctness. The construction is a decision procedure for the given polarized variety. Applying it to a certified complete finite list of polarized models from the module stage decides the target isogeny-class question. A list of numerical period matrices alone is not this required interface.


# Part III  Composition, dependencies and verification scope

## C1. Proof of the aggregate theorem

**Termination.** Section M2 computes a finite exact integer \(N\). Every individual presentation check terminates by M3, every Frobenius fingerprint terminates by M4, and every equivalence comparison terminates by M5. Completeness of the presentation enumeration and the count argument in M6 therefore return exactly \(N\) models after finitely many operations. On each of these finitely many models, G1 is a finite smoothness test. In the smooth-theta branch, G2 terminates by the odd-degree Lang–Weil argument; G3 is a finite search over \(A(K)\); G4 is exact coherent-sheaf and rational-function linear algebra; and G5 is a finite subspace enumeration. Thus the entire algorithm terminates, including when its answer is NO.

**YES soundness.** A singular theta is the hyperelliptic case and is already a Jacobian over \(k\), by G1. Otherwise G5 detects exactly triviality of the Serre character over the chosen extension \(K\), and G6 proves that its odd degree preserves triviality over \(k\). Thus a YES model is a principally polarized Jacobian over \(k\). Its Weil polynomial is exactly \(h\), by M4. Honda–Tate identifies the finite-field isogeny class from this polynomial, so its underlying abelian variety lies in the requested class.

**YES completeness and NO soundness.** If a genus-three curve over \(k\) has its Jacobian in the class, that Jacobian and its canonical principal polarization form one of the polarized \(k\)-classes counted by \(N\). M6 supplies a polarized-isomorphic model, and G1–G6 accept it. Consequently rejection of every model proves that no such curve exists over \(k\). Completeness requires every principal-polarization orbit, not merely every unpolarized abelian variety or one selected polarization per ideal.

The case \(N=0\) is a harmless empty-list branch of the general counting construction. Howe's principal-polarizability theorem rules it out for the promised simple dimension-three input, but this existence fact is not needed to make the count-and-search stopping argument work.

This proves the theorem. It is a theorem about exact aggregate computability using established results, with no unresolved model-input assumption remaining between the two parts.

## C2. Characteristic safeguards

**Characteristic two.** Prime-to-\(p\) torsion is used for the Frobenius fingerprint. The exceptional set is avoided by a smooth, geometrically connected intersection test rather than by its unavailable intrinsic equation. The involution acts through the constant étale group \(C_2\), not \(\mu_2\). Invariant differential sections are computed as a kernel, without dividing by two. The line test uses polynomial identities on a two-dimensional subspace. The optional scalar test is an Artin–Schreier trace test with a proved normalization, not a multiplicative square test. Odd extension degree prevents erasure of the quadratic character.

**Characteristic three.** The complete \(|3\Theta|\) embedding exists and has 27 sections in every characteristic. Polarized equivalence is decided by preserving the actual theta divisor after a rational translation. No equality of polarizations is inferred by canceling multiplication by three. Thus the embedding and deduplication stage does not introduce a characteristic-three exception.

## C3. Required and optional dependencies

The following are established inputs to this proof, not new theorems proved by the synthesis:

1. Deligne's classification in the ordinary case, the square-free ideal description, and Marseglia's arbitrary-order ideal-class-monoid and polarization results, with the exact degree-one guard proved in M2. Their output supplies the exact unweighted count. Lenstra's unconditional full-unit/class-group construction and the finite conductor-quotient transfer supply the required number-field arithmetic. A GRH-dependent shortcut is not part of the theorem.
2. The standard abelian-variety facts used in M3–M5: a rational theta divisor over a finite field; very ampleness of three times an ample divisor; Riemann–Roch, the degree formula and the index theorem; prime-to-characteristic torsion and the Weil bounds; the principal-polarization isomorphism to the dual and Picard descent. Relevant primary expositions are listed below.
3. Terminating projective and affine algebra over computable fields, including Gröbner bases, saturation, syzygies, effective morphism/Cartier/line-bundle checks and global sections. Smith supplies the exact global-section machinery; G4 explicitly supplies the section-transformation and multiplication interface.
4. The Beauville–Ritzenthaler all-characteristic recognition and descent results with precisely the hypotheses checked in Part II, plus étale torsor descent for differentials.
5. Lang–Weil for eventual points on a geometrically integral finite-field open variety. No effective numerical Lang–Weil constant is required for the search's mathematical termination proof.
6. Honda–Tate for the isogeny-class interpretation of equality of Weil polynomials.

Howe's principal-polarizability result supplies context, not an additional algorithmic oracle. The Clifford-center calculation and its scalar formulas are optional implementations of G5; the main algorithm may use the proved finite rational-line test alone. Numerical canonical lifts, period matrices, modular-form normalization formulas, characteristic-two exceptional-divisor equations, and genus-three curve enumeration are not used as algorithmic dependencies.

The proof is relative to these established theorems, as a mathematical algorithm proof normally is. It neither reproves the literature nor replaces exact computational prerequisites with unknown recognition or realization procedures.

## C4. What an exact execution could certify

A complete execution may retain the full ideal and principal-polarization orbit output and \(N\); every accepted model's equations and group/Cartier/line-bundle witnesses; the torsion modulus, splitting field, torsion basis, Frobenius matrix and reconstructed coefficients; and enough finite polarized-comparison data to verify \(N\) distinct classes.

For a smooth-theta model, the geometric certificate may additionally retain the odd extension degree, the point \(a\), equations for the smooth geometrically connected curve \(Y\), the translating point \(b\) and involution, the differential-section representatives, invariant basis, unique canonical quadratic relation, and the complete finite line-test result. A YES line is a short positive arithmetic witness; a NO in this deliberately noncompetitive procedure can be certified by exhaustive finite comparisons. Singular-theta outputs use the certified singularity branch and the cited descent theorem.

These are finite replayable records of a possible execution. This manuscript does **not** report that the full count-to-model-to-geometry algorithm was implemented or executed on a nontrivial input.

## C5. Validation actually available

There are two distinct validation levels.

**Finite arithmetic sanity checks.** One exact checker compared scalar splitting criteria with rational-point counts for 71,472 canonical four-dimensional quadratic forms over \(\mathbb F_2,\mathbb F_4,\mathbb F_8,\mathbb F_{16},\mathbb F_3,\mathbb F_5,\mathbb F_7\); all tested cases passed. A separate implementation constructed Clifford multiplication, the even center and its idempotents, enumerated lines by reduced-row-echelon subspaces, and compared the scalar tests on 622 forms over \(\mathbb F_2,\mathbb F_4,\mathbb F_8,\mathbb F_3,\mathbb F_5\); all tested cases passed. The tests over \(\mathbb F_8\) in the second implementation were a 78-form systematic sample, not exhaustive. These checks support the tested arithmetic conventions only.

**End-to-end geometry.** No complete Deligne-count execution followed by counted model recovery, theta intersection, genus-seven differential calculation and final recognition was performed. The mathematical termination and correctness proofs above are the evidence for that theoretical algorithm. The finite arithmetic tests do not establish the source theorems, the global section construction, general geometric correctness, or practical performance. File hashes, archive recovery and byte comparisons establish artifact identity only.

## References and bounded inspection record

The cited dependencies are credited to their existing authors. The inspection record reports the source work supporting the component proofs and source audit; it is not a claim that every original proof and every underlying dependency was independently reproved.

- **[Howe 2006]** Everett W. Howe, *Low-genus curves over finite fields: Problems and variations*, IPAM workshop talk, October 2006. PDF pages 37–38 are the target; pages 29–36 supply recognition and descent context. These relevant pages were inspected; the complete slide deck was retained, not reread in full. https://ewhowe.com/talks/IPAM.pdf
- **[Marseglia]** Stefano Marseglia, *Computing square-free polarized abelian varieties over finite fields*, Math. Comp. 90 (2021), 953–971, arXiv:1805.10223v3. Sections 3–6, especially Theorem 5.4, Algorithms 1–3 and Theorems 6.1–6.4, give the ideal and polarization interfaces. The conjugate trace dual and positivity convention were visually checked in Theorem 5.4. Section 8 is existing canonical-lift period work, not an exact geometric realization oracle here. The relevant theorem/algorithm portions were inspected; a fresh proof audit of every source result is not claimed. https://arxiv.org/abs/1805.10223v3
- **[Ideal monoid]** Stefano Marseglia, *Computing the ideal class monoid of an order*, J. London Math. Soc. (2) 101 (2020), 984–1007, arXiv:1805.09671v3. Theorem 4.6, Proposition 5.1 and the algorithms in §6 cover arbitrary orders, including noninvertible ideals. Remark 3.8 supplies the arbitrary-order unit/Picard transfer. The relevant portions were directly inspected for the count dependency. https://arxiv.org/abs/1805.09671v3
- **[Lenstra]** H. W. Lenstra, Jr., *Algorithms in algebraic number theory*, Bull. Amer. Math. Soc. 26 (1992), 211–244, arXiv:math/9204234v1. Theorem 5.4 and the following construction, PDF pages 23–24, provide the unconditional finite full-unit/class-group computation used here. This does not invoke the tentative complexity discussion in Theorem 5.5. The relevant portions were directly inspected for that dependency. https://arxiv.org/abs/math/9204234v1
- **[BR]** Arnaud Beauville and Christophe Ritzenthaler, *Jacobians among abelian threefolds: a geometric approach*, Math. Ann. 350 (2011), 793–799, arXiv:1005.3683v1. The complete seven-page retained text was read. The needed locations are Proposition 2.1, Proposition 2.4, Proposition 3.1, Theorem 3.4, the Clifford discussion before Proposition 3.5, and the finite-field rational-theta observation on the final page. The retained PDF's internal September 25, 2018 date is not a new arXiv version. https://arxiv.org/abs/1005.3683v1
- **[Smith]** Gregory G. Smith, *Computing Global Extension Modules for Coherent Sheaves on a Projective Scheme*, J. Symbolic Comput. 29 (2000), 729–746, arXiv:math/9807170v1. Complete PDF retained; introduction, Theorem 1 and §3, especially Algorithms 3.3–3.6, inspected. The algorithms work over an arbitrary field. https://arxiv.org/abs/math/9807170v1
- **[Milne notes]** J. S. Milne, *Abelian Varieties*, author course notes, version 1.1, July 27, 1998. Section 5 supplies very ampleness of \(3D\); Theorem 6.2 and Remark 6.3 supply prime-to-characteristic torsion; Section 10 supplies the cohomology and polarization formulas. The full PDF was retained and these relevant portions inspected, not the entire text independently audited. https://www.jmilne.org/math/CourseNotes/AV110.pdf
- **[Milne 1986]** J. S. Milne, *Abelian Varieties*, in *Arithmetic Geometry* (1986), Section 13, especially Remark 13.2 and Theorem 13.3. Relevant author-hosted extracted portions were inspected for finite-field line-bundle representation and degree/Riemann–Roch. A complete local PDF retrieval was unsuccessful; no complete retained copy is claimed. https://www.jmilne.org/math/articles/1986b.pdf
- **[Lang–Weil]** Serge Lang and André Weil, *Number of Points of Varieties in Finite Fields*, Amer. J. Math. 76 (1954), 819–827. The original journal page was located but its full text was not accessible in the supporting source work; the required estimate was checked in Poonen's theorem below. https://doi.org/10.2307/2372655
- **[Poonen]** Bjorn Poonen, *Rational Points on Varieties*, author-hosted book, Theorem 7.7.1 and proof, printed pages 222–223 (PDF pages 236–237). These portions were inspected for the Lang–Weil estimate and eventual-point consequence. The full book was retained but not read in full. https://math.mit.edu/~poonen/papers/Qpoints.pdf
- **[Descent]** Stacks Project, fpqc descent of quasi-coherent sheaves, tag 023R. Used for the standard descent formalism; the invariant-section condition is made explicit in G4. This reference was inspected through its public text, not retained as a full local source. https://stacks.math.columbia.edu/tag/023R
- **[Howe 1996]** Everett W. Howe, *Kernels of polarizations of abelian varieties over finite fields*, J. Algebraic Geom. 5 (1996), 583–608, Theorem 1.2. The arXiv:2001.05111v2 record is a January 2020 reproduction of the August 1995 preprint, not a new 2020 theorem. The introduction and statement of Theorem 1.2 were inspected; the full proof was not independently audited. https://arxiv.org/abs/2001.05111v2

Deligne's 1969 original and Howe's 1995 original were not fully inspected in the supporting source audit; the module interface relies on Marseglia's later primary exposition. A bounded literature audit verified no complete treatment of this exact synthesis, which does not certify worldwide originality, openness, or nonexistence of prior work.
