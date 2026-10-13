# An exact marked Deligne connection with bounded geometric recognition

## Result and scope

For an ordinary absolutely simple abelian-threefold isogeny class over a finite field, a terminating exact procedure realizes each specified principal-polarized Deligne ideal with its integral Frobenius and polarization marking. Beauville–Ritzenthaler recognition then computes the finite-field Serre descent character of that particular polarized object. In its smooth-theta branch, the required good point can be found over an explicitly selected odd extension of degree at most seven; more than one sixth of the rational points over that extension are good. Enumerating every ideal and principal-polarization orbit therefore decides whether the original isogeny class contains a genus-three Jacobian.

This is a standalone strengthening of the aggregate counted-model connection. All proofs of its arithmetic, model, marked-realization, bounded-point, and recognition interfaces are included below. The earlier aggregate route remains an independently valid alternative. The proofs use established classification, geometry, arithmetic, and topology theorems at their stated hypotheses. There is no useful overall running-time bound, implemented end-to-end geometric calculation, or worldwide novelty claim.

## 1. Input and exact outputs

Let \(k=\mathbb F_q\), \(q=p^r\), be represented by exact finite-field arithmetic. Let \(h\in\mathbb Z[x]\) be a promised realizable degree-six Weil polynomial of an ordinary absolutely simple abelian-threefold isogeny class. Testing this promise is not part of the theorem. Define
\[
 K=\mathbb Q[x]/(h),\quad \pi=x\bmod h,\quad
 R=\mathbb Z[\pi,q/\pi],\quad \bar\pi=q/\pi.
\]
Here \(K\) denotes the CM number field in the arithmetic and marked parts. In the geometric parts, a separately stated \(K=\mathbb F_Q\) denotes a finite counting field; the two uses are local to their respective parts.

Fix once and for all the effective full comparison convention of Section D1. It specifies compatible primes and residue embeddings on the complex algebraic numbers and their algebraic unramified subring at \(p\). Its induced CM type is
\[
\Phi=\{\varphi:K\hookrightarrow\mathbb C:v_p(\varphi(\pi))>0\}.
\]
This convention is an effective choice, not an unspecified embedding or a realization oracle. For a marked input, supply a full fractional \(R\)-ideal \(I\), with a \(\mathbb Z\)-basis, and \(a\in K^\times\) satisfying
\[
 aI=\bar I^{\,t},\qquad \bar a=-a,\qquad
 \operatorname{Im}\varphi(a)>0\quad(\varphi\in\Phi).
\]
The trace dual is \(J^t=\{z:\operatorname{Tr}_{K/\mathbb Q}(zJ)\subseteq\mathbb Z\}\). No invertibility of \(I\), maximal-order assumption, or restriction on \(p\) is imposed.

**Theorem A, marked realization and character.** There is a terminating exact algorithm that returns a theta-equipped projective principally polarized abelian threefold \((A,\lambda)/k\), with a finite certificate identifying its polarized Deligne module with the supplied \((I,a)\). It then returns the Serre descent character of that specified polarized object. In the nonhyperelliptic branch the output is the sign
\[
 s=\epsilon_A(\operatorname{Frob}_q)\in\{+1,-1\},
\]
which determines the character because the finite-field absolute Galois group is procyclic. The sign \(+1\) means that \((A,\lambda)\) is the canonically polarized Jacobian of a curve over \(k\); \(-1\) means that it is the nontrivial negation twist of such a Jacobian. In the hyperelliptic branch the obstruction is trivial and the output is \(+1\). This convention includes characteristic two: the signs name elements of a constant group of order two, not distinct scalars in \(k\).

**Theorem B, bounded geometric search.** For every geometrically indecomposable principally polarized abelian threefold over \(\mathbb F_q\) with a smooth rational theta divisor, and every extension \(\mathbb F_Q\), the Beauville–Ritzenthaler exceptional set satisfies
\[
 \#\Sigma_A(\mathbb F_Q)\le
 B(Q)=2Q^2+18Q^{3/2}+2321Q+24\sqrt Q+2270.
\]
For \(Q\ge81\), more than one sixth of \(A(\mathbb F_Q)\) lies outside \(\Sigma_A\). The least positive odd \(n\) with \(q^n\ge81\) is at most seven. Ordinarity is unnecessary for this geometric theorem.

**Theorem C, complete isogeny-class decision.** From \((q,h)\), enumerate all Deligne ideal classes and all principal-polarization orbits by M2, apply Theorem A to each, and answer YES precisely when at least one output sign is \(+1\). This is a terminating exact decision of Jacobian existence over the original \(k\). An alternative computes the unweighted number \(N(q,h)\), obtains the complete unlabeled model list by M3–M6, and applies the same bounded recognition to every model. The marked route labels each model by its actual ideal and polarization orbit rather than arbitrarily matching two lists.

A curve equation is an optional stronger output, not required for these decisions. Absolute simplicity ensures geometric indecomposability. Ordinarity is used for Deligne classification and its marked inverse; it is not used in the geometric recognition or the point bound. Characteristics two and three are included throughout.

## 2. Meaning relative to the source question

Howe's 2006 IPAM talk asks, on PDF pages 37–38, whether either of the described recognition approaches can be combined with the Deligne-module description to determine Jacobian existence in an ordinary absolutely simple threefold class given by its Weil polynomial. The displayed problem imposes no complexity bound. [Howe 2006](https://ewhowe.com/talks/IPAM.pdf)

The construction here meets that literal mathematical request under its displayed input promise. The connection is now genuinely per-ideal: the Frobenius matrix and positive integral polarization form are certified against the input ideal before its descent character is reported. Applying this to every polarization orbit supplies the class-level answer. No additional mathematical requirement in the displayed question has been identified as unmet. Efficiency, useful explicit height or precision bounds, implementation, an intended practical endpoint, historical priority, and worldwide novelty are distinct matters not supplied by this theorem. This scope statement does not decide a historical status label.

The recognition method used is the geometric Beauville–Ritzenthaler approach. The source's alternative wording does not require both that method and a modular-form method. Principal polarizability somewhere in a simple odd-dimensional isogeny class is already known from Howe; testing only one polarization would still not decide Jacobian existence. [Howe 1996](https://arxiv.org/abs/2001.05111v2)

## 3. Proof organization and finite certificates

Part I proves complete ideal/polarization enumeration, exact projective-model checks, the Weil-polynomial fingerprint, and the independent aggregate count-to-model route. Part II gives the full marked inverse under the fixed comparison convention. Part III proves the uniform good-point bound. Part IV gives all-characteristic recognition and the exact base-field character. Part V proves the compositions and states their dependency and validation boundaries.

All searches enumerate finite encodings or finite sets, and each individual candidate check terminates. In the marked search, the model, lift, topology witnesses, and integral matching matrix are enumerated together; a wrong candidate is never allowed to start a nonterminating search for its missing isomorphism. Existence of the canonical lift and its full finite descent tuple guarantees that one complete successful certificate occurs. The bounded good-point search needs only the returned equations, not a curve already known to underlie the ppav or equations for the exceptional set.

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

Use the full comparison convention of D1, whose induced CM type agrees with the polarized-variety paper's equation (5.1) and Algorithm 2:
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

Likewise no floating-point sign decision or numerical recognition step is used: signs of nonzero algebraic imaginary parts are decided by exact real-algebraic isolation. The aggregate model route M3–M6 uses only the resulting integer \(N\); the marked route D1–D6 instead uses the actual ideal and polarization representatives. The ideal list and polarization orbits certify completeness for both routes.

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

This is the precise role played by Deligne modules in the aggregate route: they certify **when a model enumeration is exhaustive**, without a canonical-lift recognition oracle or an individual ideal-to-equations matching routine. Stopping merely because no new model appeared for some time would be invalid; stopping at the exact polarized count is what makes this a decision procedure.



# Part II  The marked polarized inverse

The notation and input pair are those of Theorem A. The output contract is the theta-equipped model contract M3, strengthened by a finite integral marking certificate.

## D1. A computable full comparison convention

Use the usual computable field Qbar_C of complex algebraic numbers, with roots represented by exact polynomials and isolating rectangles. Enumerate its elements and build a nested sequence of finite normal number fields E_n whose union is Qbar_C. Begin with any prescribed finite normal field and prime data used for the input CM type. Inductively choose a prime P_(n+1) above P_n by exact ideal factorization and contraction; a deterministic ordering of finite encodings fixes the choice. Extend residue-field embeddings into a fixed computable algebraic closure of F_p at every stage. Both choices are possible by elementary extension theory and finite-field arithmetic.

This constructs a p-adic place v on Qbar_C, computable on every finite collection of algebraic numbers. To evaluate it on an element, advance the tower until the element is included and use the chosen prime there. Contraction guarantees independence from later stages. Integrality, reduction, ramification index, residue degree and field operations at the selected prime are effective number-field calculations.

Let H be the subfield of Qbar_C whose elements generate unramified extensions locally at v, and let D be its valuation ring. Equivalently, H is the intersection of Qbar_C with the maximal unramified algebraic extension of Q_p inside the local algebraic closure selected by v. Finite composita stay locally unramified, so this is a field. D is the algebraic strict henselization of Z_(p), with residue field Fpbar; its completion is W(Fpbar). The inclusion D into C is the comparison convention. It is effective on all finite data used below. An abstract extension to the completed Witt ring may be chosen to invoke Deligne's language; no computation on transcendental p-adic coefficients is needed.

Enumerate finite subfields L of H by testing e(P/p)=1 for their selected prime. The local rings O_(L,P) are cofinal for finite subsets of D. The complex embedding of L is always its fixed inclusion into Qbar_C, never an independently chosen embedding for a successful candidate. Identify the explicitly supplied k with its fixed subfield in Fpbar by finite-field arithmetic.

Deligne's original §3 states that the canonical lift descends to this algebraic ring D and that the resulting complex abelian variety depends only on the embedding of D. His §8 determines the complex structure by positive v-valuations of Frobenius eigenvalues. Thus this convention extends the finite prime data used in the usual CM-type computation, while also removing its residual global ambiguity. [Deligne 1969](https://publications.ias.edu/sites/default/files/Number6.pdf)

## D2. Finite lift certificates

A certificate contains the following finite exact objects.

1. A theta-equipped ppav A/k in a complete |3 Theta_A| embedding, represented and checked as in the model presentation theorem M3. Its Weil polynomial is checked to be h by M4's exact torsion fingerprint.
2. A number field L contained in H, its selected unramified prime P, and an abelian scheme B over O=O_(L,P), with a relative theta line bundle L_B, a relative effective theta divisor, and a certified equality O_B(1)=L_B^3. Its generic and special fibers have dimension three and Hilbert polynomial 27t^3 in this embedding.
3. A residue-field identification O/P=k'=F_(q^m), for some m>=1, using the fixed embedding of k into Fpbar from D1, and a group isomorphism j:B_(k') -> A_(k') preserving the principal polarizations. To check the last assertion concretely, supply a point t in A(k') and equality of the transported theta divisor with a translate of Theta_A. This equality implies equality of polarization morphisms.
4. An O-group endomorphism F_B of B, with exact morphism equalities

   h(F_B)=0,
   j o (F_B mod P) o j^(-1)=(Frob_(q,A))_(k').

   The right-hand side is the base change of A's q-power Frobenius. It is a k'-linear endomorphism. It is not the absolute q-power map on coefficients in k', and not a semilinear p-Frobenius lift.
5. The finite integral-topology data in D4, and an integral invertible matrix U satisfying the marked equalities in D5.

A finite ring presentation, multiplication table and selected prime make O effective. On each affine chart, flatness over this DVR is equivalent to absence of p-torsion; it can be checked by saturation and module calculations over a number-field local ring. Alternatively finite standard-smooth chart presentations and their inverse maps can be supplied as witnesses. A finite cover by standard-smooth charts proves smoothness directly. Generic and special fiber Jacobian/Fitting tests, together with flatness, give the same verification. The generic and special fibers are the only two fibers of Spec(O).

Projectivity is part of the embedding. Smooth fiberwise dimension three, geometric connectedness of both fibers, and the checked group-law, identity and inverse identities make B an abelian scheme. The connectedness checks can use H0(O) on the two proper smooth fibers, as in M3. Affine-chart ring maps, covers, denominator inverses, overlap agreements, Cartier witnesses and the cube line-bundle isomorphism are all finite algebraic data. Ideal membership and the supplied polynomial identities are checked in localized rings. The theta bundle is relatively ample because its cube is O(1). The fiberwise Hilbert polynomial gives chi(L_B)=1 and hence principal polarizations.

These checks need not call a black-box moduli or canonical-lift routine. Smooth charts, algebraic identities and topological witnesses can all be enumerated with the presentation. Every genuine finite-type smooth object and map admits such finite witnesses. All purported witnesses receive terminating exact checks.

## D3. Why the lift certificate forces the canonical lift

**Lemma.** Let B be an abelian scheme over a mixed-characteristic complete DVR with residue field containing k, and suppose its special fiber is identified with A after residue extension. Suppose an endomorphism F_B reduces to A's q-Frobenius and satisfies h(F_B)=0, where h is ordinary. Then the p-divisible group of B is the split lift of the connected and étale factors of A[p^infinity]. Hence B is the canonical Serre–Tate lift after base extension.

**Proof.** Hensel factorization gives h=h_et h_mult in Z_p[x], with h_et having unit roots, h_mult having positive-valuation roots, and coprime reductions. Ordinarity gives h_mult mod p=x^3 and h_et(0) a p-adic unit. Chinese remainders produce complementary idempotents in Z_p[x]/(h). The equality h(F_B)=0 lets them act on B[p^infinity]; at each finite p-power level this is an ordinary finite polynomial operation modulo a sufficiently high power of p. Thus they split B[p^infinity] into two p-divisible direct factors.

On the special fiber, Frobenius acts invertibly on the étale factor and has positive slopes on the multiplicative factor. The CRT idempotents are exactly the corresponding projectors. At every finite level, the first direct factor is finite flat with étale special fiber. It is étale over the DVR: its relative differentials vanish modulo the maximal ideal and hence vanish by Nakayama. For the second factor apply the same argument to its Cartier dual. It is of multiplicative type. Étale p-divisible groups, and their Cartier duals, lift uniquely over a complete henselian base with fixed residue data. Consequently this direct sum is the canonical split p-divisible lift. Serre–Tate deformation equivalence identifies the abelian scheme with the canonical lift, with its specified special-fiber identification. This proves the lemma. No argument uses p>2 or discards torsion deformation parameters. In fact the lemma also applies to ramified bases; the search itself needs only unramified bases. □

The endomorphism in the certificate is consequently the canonical lift of the specified q-Frobenius. Uniqueness of lifting a homomorphism follows from Serre–Tate full faithfulness (or rigidity). Likewise the generic-fiber polarization is the canonical lift of the special-fiber polarization. The finite-field extension k'/k therefore does not erase or replace the original q-Frobenius marking.

The splitting characterization is recalled in Deligne §3. Katz's Theorem 2.1(1),(4), printed pp.148–149, supplies the deformation equivalence and its homomorphism criterion. [Katz, Serre–Tate local moduli](https://web.math.princeton.edu/~nmk/old/serretatelocmod.pdf) Neither an arbitrary CM lift nor the mere presence of extra endomorphisms is accepted as a certificate. [Deligne 1969](https://publications.ias.edu/sites/default/files/Number6.pdf)

## D4. Exact integral topology, including the polarization

The topology needed here is integral homology and actual induced maps, not Betti numbers alone.

Represent complex projective space as the compact real-algebraic set of Hermitian rank-one projectors P with P^2=P and tr(P)=1. A complex algebraic projective variety, its morphism graphs and all products thereby have exact compact semialgebraic representations over the real algebraic numbers. Quantifier elimination converts between their finite descriptions as needed.

A finite triangulation witness consists of a finite simplicial complex and a semialgebraic homeomorphism from its realization to the target. Totality, bijectivity, image equality and continuity are first-order statements over a real closed field. Continuity can be written with epsilon-delta quantifiers; compactness then makes a continuous bijection a homeomorphism. Exact real quantifier elimination verifies all these assertions. The semialgebraic triangulation theorem guarantees that some such witness exists. Thus even exhaustive witness enumeration is a terminating method, without a complexity claim. Classical effective triangulation is also an available implementation. [Basu–Karisani 2023, introduction](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/efficient-simplicial-replacement-of-semialgebraic-sets/C32B4A3FA99FAF864D70274612ADA1C2)

For a continuous semialgebraic map between triangulated compact sets, enumerate barycentric subdivisions of the domain and vertex maps to the target. Check the simplicial condition and the open-star condition

  f(star(v)) subset star(s(v))

for every domain vertex. These are finite first-order semialgebraic inclusion tests, so are decidable. The simplicial approximation theorem and the Lebesgue-number lemma guarantee success after sufficiently many subdivisions. A successful map is homotopic to f and computes its exact map on integral homology. Subdivision identifications are the standard integral subdivision chain maps. This supplies certified maps for F_B, the group law, and the projective embedding. It avoids any assumption that every semialgebraic map admits a simultaneous exact triangulation.

Smith normal forms of simplicial boundary matrices compute the full integral homology and cohomology, with cycle/cocycle representatives and integral bases. Cross products use the standard ordered product triangulation and shuffle map. In particular, write T=H1(B_C,Z), compute the integral matrix M of (F_B)_*, and compute m_*(x cross y) for every pair of basis classes x,y of T.

To compute the positive hyperplane generator eta in H^2(CP^26,Z), use the standard complex-oriented CP^1 inclusion. Fix an explicit integral outward 2-cycle on the boundary of the rational octahedron |x|+|y|+|z|=1, with each triangular face oriented outward. Radial projection to the unit sphere is a semialgebraic orientation-preserving homeomorphism. Its certified induced map supplies the outward sphere class, independent of any arbitrary triangulation orientation. Identify CP^1 with this sphere through

  (x,y,z) -> (1/2) [[1+z,x-iy],[x+iy,1-z]].

Near the north pole the complex coordinate is (x+iy)/(1+z), so this orientation is positive. The homology and cohomology calculations identify the unique eta evaluating to +1 on this class. Pull eta back along B_C -> CP^26. Since O_B(1)=L_B^3, divide this class by three in the free group H^2(B_C,Z), obtaining c1(L_B). Existence and uniqueness follow from the displayed line-bundle identity and the torsion-free cohomology of a complex torus; the integral calculation also verifies divisibility.

Define the integral alternating form

  E_B(x,y)=<c1(L_B), m_*(x cross y)>.

For a complex torus, the group-law cross product identifies x cross y with the natural wedge class in H2. This is exactly the alternating form of the first Chern class, with E_B(v,Jv)>0 for an ample line bundle.

**Sign convention.** For a in the input, use

  E_a(s,t)=Tr_(K/Q)(a s conjugate(t)).

This is the positive-Chern-class convention. Marseglia's §8 instead prints b(s,t)=Tr(conjugate(t a)s), so b=-E_a. The printed bar covers both t and a. For Phi-positive a, E_a(v,Jv)=2 sum_phi Im(phi(a)) |phi(v)|^2>0. In the elementary test K=Q(i), a=i/2, E_a(1,i)=1. For completeness, the positive Hermitian form is H(s,t)=2 sum_phi Im(phi(a)) phi(s) conjugate(phi(t)), and b=Im(H). Its Chern form (i/2) sum H_jk dz_j wedge dbar(z_k) evaluates on the oriented (s,t)-torus as -Im(H(s,t))=E_a(s,t). The formula is stated in [Schnell, Lecture 4, p.3](https://www.math.stonybrook.edu/~cschnell/mat615/lectures/lecture4.pdf). Thus comparing c1 with b without this minus sign would be wrong. [Marseglia 1805.10223v3, §8](https://arxiv.org/abs/1805.10223v3)

## D5. The marked check and its meaning

From an input Z-basis of I compute the integral Frobenius matrix F_I for multiplication by pi and the integral alternating matrix E_I for E_a. Their entries are exact algebraic traces. The principal-polarization condition makes E_I unimodular.

The certificate contains U in GL_6(Z), and checks

  M U = U F_I,
  U^t E_B U = E_I.

These are terminating integer calculations. One can enumerate U together with all other finite witnesses; there is no need to decide nonisomorphism of a mismatched candidate by an unbounded search.

The canonical-lift lemma identifies (T,M) with the actual Deligne module of A/k under the full comparison convention. Deligne's fully faithful equivalence and the polarization compatibility then identify the two displayed matrix equalities with an isomorphism of polarized Deligne objects. In particular the output belongs to the specified ideal class and specified polarization orbit. Equality of Weil polynomials alone, local Tate modules alone, or matching endomorphism rings would not imply this conclusion.

## D6. Termination and completeness

Enumerate finite encodings of all candidates and all listed witnesses by increasing total encoding length. Verify each in finite time. Stop at the first complete successful certificate and return its A/k.

For the promised (I,a), the polarized Deligne equivalence gives an actual ppav A/k. A rational theta divisor and a complete |3Theta| model exist as established in M3. The underlying canonical abelian scheme descends to D by Deligne's algebraic descent statement. The entire marked tuple descends as follows. Write H=Frac(D) and Hhat=Frac(W(Fpbar)). H is relatively algebraically closed in Hhat: an element algebraic over H is algebraic over Q, and its finite local extension of Q_p lies inside Hhat, whose value group is Z. That local extension has ramification index one, hence is unramified, so the element already belongs to H. Every finitely generated intermediate coefficient field of Hhat/H is consequently regular, since characteristic zero supplies separability. Milne's Corollary 15.4(b) therefore descends each generic-fiber homomorphism of the canonical lift, including F and the polarization map, to H. The Néron mapping property for abelian schemes over a DVR extends these homomorphisms uniquely to D. The resulting maps agree with the canonical ones after completion, by uniqueness. [Milne, AV110, Corollary 15.4(b)](https://www.jmilne.org/math/CourseNotes/AV110.pdf), [Bosch–Lütkebohmert–Raynaud, Néron Models, §1.2, Proposition 8, printed p.15](https://math.arizona.edu/~cais/scans/BLR-Neron_Models/neron1.pdf). An abelian scheme over a DVR is the Néron model of its generic fiber; this is the original source of the extension property used here.

Its principal polarization is represented by an ample line bundle after an étale localization: the relevant Pic^lambda torsor under the dual abelian scheme is smooth, and over the strictly henselian base a special-fiber point lifts. Rigidification at the zero section makes the lifted Picard point an actual line bundle; equivalently the Brauer obstruction vanishes over this strictly henselian DVR. The line bundle may be chosen to reduce to a theta representative after a translation. Its rank-one space of sections gives a relative theta divisor, and its third power gives the projective embedding.

All equations, maps, divisor data, Frobenius, polarization, special-fiber identification and finite chart witnesses involve finitely many elements of D. They therefore descend to some O_(L,P) with L locally unramified at v. Enlarge the residue field if needed so it contains k and all the special-fiber data. The equality h(F_B)=0 holds for the canonical lift because it holds for Frobenius on A and lifting is functorial. The topology witnesses and the integral matrix U exist by D4 and the given polarized Deligne identification. Thus at least one finite certificate is valid and eventually occurs. Every test terminates, so the search terminates.

Soundness is D2–D5. The procedure is therefore a genuine per-ideal realization algorithm, although its search is far less practical than existing specialized constructions. The proof uses the existence and algebraic descent of canonical lifts only to guarantee a finite successful certificate; the verifier establishes canonicity independently through the CRT lemma.

## D7. Exact interface to recognition

Run G1–G6 on the returned theta-equipped model. If its theta is singular, return the trivial character. Otherwise use the bounded odd degree from Part III and return \(+1\) when the constructed quadric has a rational line and \(-1\) when it does not. Section G6 proves that this is \(\epsilon_A(\operatorname{Frob}_q)\), not merely the answer after extension. D5 identifies \((A,\lambda)\) with exactly \((I,a)\), so the sign belongs to that specified ideal and polarization orbit.

The base extension in a lift certificate and the extension used in recognition serve different purposes. The former carries the canonical-lift comparison but retains the original \(q\)-Frobenius endomorphism. The latter has odd degree and is used only to find a good theta intersection. Neither step substitutes an unmarked isogeny-class representative or loses the original-field character.


# Part III  A uniform odd-extension bound

## B0. Uniform theorem and its hypotheses

Let \((A,\lambda)\) be a geometrically indecomposable principally polarized abelian threefold over \(k=\mathbb F_q\), and let \(\Theta\) be a smooth \(k\)-rational theta divisor. No ordinarity hypothesis is needed in this note. Characteristics two and three are included.

Write \(\Sigma_A\) for the exceptional set of Beauville–Ritzenthaler (BR), so that \(a\notin\Sigma_A\) exactly when \(\Theta\cap(\Theta+a)\) is smooth and geometrically connected. Put
\[
B(Q)=2Q^2+18Q^{3/2}+2321Q+24\sqrt Q+2270.
\]

**Theorem.** For every finite extension \(\mathbb F_Q/k\),
\[
\#\Sigma_A(\mathbb F_Q)\le B(Q),\qquad
\#A(\mathbb F_Q)\ge(\sqrt Q-1)^6.
\]
Consequently, if \(Q\ge81\), a good point exists over \(\mathbb F_Q\). In fact, more than one sixth of \(A(\mathbb F_Q)\) consists of good points.

**Odd-extension consequence.** Let \(n\) be the least positive odd integer such that \(q^n\ge81\). Then \(n\le7\), and the BR construction can be performed over \(\mathbb F_{q^n}\). Explicitly:

- \(q=2\): choose \(n=7\), so \(Q=128\).
- \(q=3\) or \(4\): choose \(n=5\), so \(Q=243\) or \(1024\).
- \(5\le q<81\): choose \(n=3\).
- \(q\ge81\): choose \(n=1\).

Only prime-power values of \(q\) are relevant. Oddness preserves the quadratic Serre character, including its characteristic-two Artin–Schreier interpretation. This quantitative bound supplies the good-point stopping guarantee in G2.

The bound is deliberately conservative and is not claimed optimal. It assembles established geometry and point bounds; it makes no practical-running-time, end-to-end-computation, or priority claim.

## B1. Geometric description and descent

It suffices to work over an arbitrary finite field \(K=\mathbb F_Q\). BR Proposition 3.1 supplies a nonhyperelliptic genus-three curve \(C/K\) and a character \(\epsilon\) of order at most two such that \(A\) is the twist of \(J=\operatorname{Jac}(C)\) by \(\epsilon\) acting through \([-1]\). Smoothness of \(\Theta\) is precisely the nonhyperelliptic branch. No equation for \(C\), and no determination of \(\epsilon\), is required to use the numerical conclusion.

Set \(T=\operatorname{Sym}^2 C\). Since \(C\) is nonhyperelliptic, every effective degree-two divisor class has exactly one effective representative. The Abel map therefore identifies \(T\) with the smooth degree-two theta divisor in \(\operatorname{Pic}^2(C)\). Riemann–Roch gives \(h^0(K_C-E)=h^0(E)=1\), so residual canonical intersection defines a regular involution
\[
\jmath:T\longrightarrow T,\qquad E\longmapsto\langle K_C-E\rangle.
\]
Consider the finite morphism
\[
f:T\longrightarrow J,\qquad E\longmapsto2E-K_C.
\]
Finiteness follows by identifying \(T\) over \(\overline K\) with a theta translate and restricting the finite isogeny \([2]:J\to J\). Its image is \(\Sigma'_J\), and
\[
f\circ\jmath=[-1]\circ f.
\]
Twisting the source by \(\jmath\) and the target by \([-1]\) with the same character descends \(f\) to a finite surjection
\[
f_\epsilon:S=T^{(\epsilon,\jmath)}\longrightarrow\Sigma'_A\subset A.
\]
Here \(S\) is a smooth projective geometrically connected surface, geometrically isomorphic to \(T\). These twists use a constant Galois group of order two. They remain valid in characteristic two; no identification with \(\mu_2\), no division by two in the ground field, and no symmetric rational theta divisor is used.

For the other exceptional component, the difference morphism
\[
d:C\times C\longrightarrow J,\qquad(p,r)\longmapsto p-r
\]
is equivariant for exchange of the two factors on the source and negation on the target. It likewise descends under the character \(\epsilon\) to a morphism from the exchange twist of \(C\times C\) onto \(\Sigma''_A\). This is the all-characteristic definition of \(\Sigma''_A\) in BR §3.3.

## B2. Point bound for the twisted theta surface

The geometric \(\ell\)-adic Betti numbers of \(T\), for a prime \(\ell\ne\operatorname{char}K\), are
\[
(b_0,b_1,b_2,b_3,b_4)=(1,6,16,6,1).
\]
Here is an all-characteristic derivation. The finite quotient map \(\rho:C\times C\to\operatorname{Sym}^2C\) has geometric fibers equal, on their underlying point sets, to the orbits of factor exchange. Thus
\[
\mathbb Q_\ell=(\rho_*\mathbb Q_\ell)^{\mathfrak S_2},
\qquad R^i\rho_*\mathbb Q_\ell=0\quad(i>0).
\]
The second equality follows from proper base change and the vanishing of higher étale cohomology of finite geometric fibers. Taking invariants is a direct summand over \(\mathbb Q_\ell\), so
\[
H^*(T_{\overline K},\mathbb Q_\ell)
 =H^*((C\times C)_{\overline K},\mathbb Q_\ell)^{\mathfrak S_2}.
\]
Künneth now gives the displayed numbers. In degree two, the two outer one-dimensional terms contribute one invariant dimension, and exchange on \(H^1(C)\otimes H^1(C)\) includes the graded minus sign, giving \(\bigwedge^2H^1(C)\) of dimension \(\binom62=15\). Degrees one and three each contribute six dimensions. The coefficient field \(\mathbb Q_\ell\) has characteristic zero even when \(K\) has characteristic two; this cohomological splitting is not division by two in \(K\).

Twisting does not change geometric Betti numbers. The trace formula and the Weil bounds for a smooth projective surface therefore give
\[
\#S(K)\le Q^2+6Q^{3/2}+16Q+6\sqrt Q+1. \tag{1}
\]
Only the dimensions and weights are used; no assertion that the Frobenius action on the twist is unchanged is made.

## B3. Rational image points without rational preimages

It is not valid in general to bound \(\#\Sigma'_A(K)\) by \(\#S(K)\). A rational image point can have several geometric preimages permuted by Frobenius. We control precisely that possibility.

Work geometrically and identify the source with a theta divisor \(D\) in \(J\). Up to translation, the map is \([2]|_D\). Two distinct geometric points in one fiber differ by a nonzero element
\[
t\in J[2](\overline K).
\]
There are at most \(2^6-1=63\) such nonzero elements. In characteristic two this is only a bound on geometric points, not a claim that the full group scheme \(J[2]\) is reduced or étale. Its scheme length is \(2^6\), so the bound is valid in every characteristic.

For each such \(t\), let
\[
Y_t=D\cap(D+t).
\]
The two divisors are distinct: equality would put \(t\) in the kernel of the principal polarization \(\phi_{\mathcal O(D)}\), which is trivial. Since \(D\) is geometrically irreducible, they have no common divisor component. Their scheme-theoretic intersection is therefore a pure one-dimensional complete intersection, with cycle class \(\theta^2\). Possible nonreduced components are retained with their positive intersection multiplicities.

Let \(Z_t\) be the reduced image of \(Y_t\) under \([2]\), with the translation and polarized identification back to \(A\) understood. Use the actual \(K\)-rational \(|3\Theta|\) embedding of \(A\), with hyperplane class \(H=3\theta\). The projection formula and \([2]^*\theta\equiv4\theta\) yield
\[
\deg_H([2]_*[Y_t])
=([2]^*H)\cdot\theta^2
=12\theta^3=72. \tag{2}
\]

Translation by \(t\) preserves \(Y_t\), is fixed-point-free on its geometric points, and leaves \([2]\) unchanged. Each geometric generic fiber over an irreducible component of \(Z_t\) consequently contains at least two distinct points. The sum of the generic degrees, with the positive multiplicities from \([Y_t]\), is at least two. This remains true if translation exchanges two different irreducible components of \(Y_t\); it does not require each component to be preserved. Therefore, as effective cycles,
\[
[2]_*[Y_t]\ \ge\ 2[Z_t],
\qquad \deg_H Z_t\le36. \tag{3}
\]
Inseparable multiplicities can only increase the coefficient on the left. No separability of \([2]\) was assumed.

The union \(Z=\bigcup_{t\ne0} Z_t\) is thus a reduced union of projective curves of total degree at most
\[
63\cdot36=2268. \tag{4}
\]
Its degree does not increase under the geometric translations or polarized identifications used above. The projective degree bound of Lachaud–Rolland, Theorem 2.1, applies even to a geometric algebraic set not individually defined over \(K\), and gives
\[
\#(Z\cap A(K))\le2268(Q+1). \tag{5}
\]

Every point of \(\Sigma'_A(K)\setminus Z\) has exactly one geometric preimage under the descended finite map \(f_\epsilon\). That geometric point is Frobenius-fixed and therefore belongs to \(S(K)\). This implication remains true for a nonreduced fiber: nilpotent structure does not create further geometric points, and the finite field is perfect. Hence
\[
\#\Sigma'_A(K)
\le\#S(K)+2268(Q+1). \tag{6}
\]
This is the step that prevents the otherwise incorrect rational-image counting shortcut.

## B4. Exact counts for the difference component

Write \(N_i=\#C(\mathbb F_{Q^i})\). For nonzero difference classes the geometric pair \((p,r)\) is unique. Indeed, if \(p-r=p'-r'\), then \(p+r'\sim p'+r\). A nonhyperelliptic genus-three curve has no degree-two pencil, so these effective degree-two divisors are equal. Either the difference is zero, or \(p=p'\) and \(r=r'\). The whole diagonal maps to zero.

If \(\epsilon\) is trivial, the nonzero rational differences are consequently the ordered distinct pairs of \(K\)-points, giving
\[
\#\Sigma''_A(K)=N_1^2-N_1+1. \tag{7}
\]
If \(\epsilon\) is nontrivial, the rationality condition on the unique off-diagonal pair is
\[
\operatorname{Frob}_Q(p)=r,\qquad
\operatorname{Frob}_Q(r)=p.
\]
There are \(N_2-N_1\) such ordered pairs, giving
\[
\#\Sigma''_A(K)=N_2-N_1+1. \tag{8}
\]
These are statements about the twist's actual Frobenius action, so no rational preimage assumption is hidden in them.

The genus-three Weil bounds give
\[
Q+1-6\sqrt Q\le N_1\le Q+1+6\sqrt Q,
\quad N_2\le Q^2+1+6Q.
\]
In the trivial-character case, bounding the positive square above and the negative term below gives
\[
N_1^2-N_1+1
\le Q^2+12Q^{3/2}+37Q+18\sqrt Q+1. \tag{9}
\]
In the nontrivial-character case the sharper bound is
\[
N_2-N_1+1\le Q^2+5Q+6\sqrt Q+1,
\]
which is also bounded by the right side of (9). Thus (9) bounds \(\Sigma''_A\) uniformly, without deciding the character.

## B5. Explicit separation and density

Adding (1), (6), and (9), and permitting overlap between the exceptional components, gives
\[
\#\Sigma_A(K)
\le2Q^2+18Q^{3/2}+2321Q+24\sqrt Q+2270=B(Q).
\]
For an abelian threefold, the usual paired Frobenius eigenvalue formula gives
\[
\#A(K)\ge(\sqrt Q-1)^6=L(Q).
\]
At \(Q=81\),
\[
L(81)=262144,\quad B(81)=216731,
\quad L(81)-B(81)=45413>0.
\]
For a fully algebraic verification at every larger \(Q\), put \(s=\sqrt Q-9\ge0\). Direct expansion gives
\[
L(Q)-B(Q)
=s^6+48s^5+958s^4+10150s^3
 +57661s^2+144600s+45413>0. \tag{10}
\]
The stronger density inequality follows from
\[
5L(Q)-6B(Q)
=5s^6+240s^5+4788s^4+50660s^3
 +284526s^2+670992s+10334>0. \tag{11}
\]
Consequently
\[
\frac{\#\Sigma_A(K)}{\#A(K)}
\le\frac{B(Q)}{L(Q)}<\frac56,
\]
so more than one sixth of the rational points are good.

For the smallest starting field, \(q=2\), the prescribed extension is \(Q=128\). Formula (10), with \(s=8\sqrt2-9>0\), certifies positivity without a floating-point comparison. There is no exceptional small-characteristic branch.

## B6. Algorithmic replacement and limits

In the smooth-theta branch G2:

1. Choose \(n\) from the four cases in the theorem, and construct \(K=\mathbb F_{q^n}\).
2. Enumerate \(A(K)\). For each candidate \(a\), perform the already specified exact tests that \(\Theta\cap(\Theta+a)\) is a smooth projective curve and has \(H^0(\mathcal O)=K\).
3. At least one candidate passes. Continue with the genus-seven involution, genus-four quotient canonical quadric, and splitting test.

The auxiliary curve \(C\), the character \(\epsilon\), the twisted surface \(S\), and the collision curves are used only to prove the bound. Constructing them is not an extra algorithmic input. The exact good-point test in G2 is unchanged, and no equation for the characteristic-two exceptional divisor is required.

If an independent uniform sampler for \(A(K)\) is available, repeated independent sampling requires fewer than six good-point tests on average by the density bound. This conditional observation does not supply or claim an efficient uniform sampler, and does not make the overall marked or aggregate algorithm practical.


# Part IV  Exact geometric recognition and descent

Every model returned by M3–M6 or D1–D6 supplies the exact input required here: finite projective equations for a geometrically indecomposable principally polarized abelian threefold \((A,\lambda)\), exact group-law/inverse/origin data, and a \(k\)-rational effective Cartier divisor \(\Theta\) representing \(\lambda\). The model checks certify this contract; no extra realization oracle is assumed.

The recognition input is used scheme-theoretically. Equality, pullback and morphism operations refer to finite presentations on affine charts, not just tables on rational points. The theta divisor need not be symmetric.

The geometric theorems used below are Beauville–Ritzenthaler [BR], Proposition 2.1, Proposition 2.4, Proposition 3.1, Theorem 3.4, and, for the optional arithmetic alternatives, the even-Clifford paragraph preceding Proposition 3.5. They work over perfect fields and the statements used here do not exclude characteristic two. The odd-characteristic qualification in their §2.2 concerns a Prym identification not required below. Their §2.6 leaves an intrinsic equation for one exceptional component unresolved in characteristic two; the algorithm never uses that equation.

## G1. Detect the hyperelliptic case exactly

Test whether Θ is smooth over k using its equations and the Jacobian criterion on affine charts. Finite fields are perfect, so this is geometric smoothness. If Θ is singular, return the character value +1, equivalently YES. For a geometrically indecomposable principally polarized threefold, [BR, §3.3] identifies this as the geometric hyperelliptic case, and [BR, Proposition 3.1] says its Serre character is trivial. Thus this is a Jacobian over k, not merely over an algebraic extension.

Assume henceforth that Θ is smooth.

## G2. Find a certified good point over an odd extension

Choose the least positive odd n with q^n≥81, using the explicit cases in Part III. Thus n≤7. Construct K = F_(q^n), enumerate every a in A(K), and form the scheme-theoretic intersection

    Y_a = Θ_K ∩ (Θ_K + a).

Accept the first a for which all of the following finite tests succeed:

1. Y_a is a nonempty smooth projective curve of pure dimension one.
2. dim_K H^0(Y_a, O_Ya) = 1.

All the tests are exact. Dimension and smoothness are computed from saturated homogeneous ideals or affine charts. Projective coherent-sheaf cohomology is computable by Gröbner bases and syzygies; [Smith, Theorem 1 and Algorithms 3.3–3.6] supplies a characteristic-independent algorithm. For a proper smooth K-scheme, the second condition is equivalent to geometric connectedness here: H^0 commutes with field extension, and a proper smooth scheme over an algebraically closed field has one copy of that field per connected component.

### Why this is the required good-point test

Over an algebraic closure, (A, λ) is a nonhyperelliptic genus-three Jacobian. Under any such polarized group isomorphism, Θ is a translate of the standard degree-two theta divisor. [BR, Proposition 2.1] states that Y_a is smooth and connected exactly when a lies outside their divisor Σ_A, and that the involution used below is then fixed-point-free. These statements are independent of the chosen geometric Jacobian identification. The algorithm only tests their left-hand side.

### Why this bounded search terminates

Part III proves that more than one sixth of \(A(K)\) lies outside the Beauville–Ritzenthaler exceptional set when \(q^n\ge81\). Every such point passes the two finite tests. Therefore the single finite enumeration over the prescribed field terminates successfully. No construction of the auxiliary genus-three curve, no determination of its twist in advance, and no equation for the exceptional set is an algorithmic input.

The explicit degree bound replaces the earlier unbounded odd-extension search justified by Lang–Weil. It does not claim that a good point must already exist over the original field, or that enumeration of \(A(K)\) is efficient.

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

These conditions are exactly the polynomial identity F(sv+tw)=0; thus they certify that its projectivization is a line on Q. There are finitely many subspaces. Return the character value +1 (YES) if any passes, and −1 (NO) if none passes.

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

This proves termination and correctness. The construction is a decision procedure for the given polarized variety. Applying it to the marked model of D1–D6 decides the character of that ideal and polarization. Applying it to every representative from M2, or to the complete aggregate list M6, decides the target isogeny-class question. A list of numerical period matrices alone is not this required interface.



# Part V  Composition and claim boundaries

## C1. Proof of marked realization and descent

D1 fixes effective arithmetic and comparison choices on every finite algebraic coefficient set. D2 lists finite certificates and terminating checks over number-field localizations and finite fields. D3 proves that a lifted original \(q\)-Frobenius satisfying \(h(F)=0\) forces the canonical Serre–Tate deformation, including characteristic two. D4 computes genuine integral homology, induced maps, and the positive first-Chern polarization pairing, with the orientation fixed explicitly. The two exact matrix equalities in D5 consequently identify the returned object's polarized Deligne module with the input pair. D6 proves that the entire canonical tuple descends to one enumerated finite unramified localization and has finite topology and marking witnesses. Hence the search terminates and is sound for each specified pair.

The rational theta divisor and model data returned by that search satisfy exactly the G1 input contract. A singular theta gives the hyperelliptic Jacobian case and trivial obstruction. For a smooth theta, Part III chooses one odd extension of degree at most seven with a good point. G2–G4 construct the certified theta intersection, free constant-order-two involution, invariant differential space, and canonical smooth quadric. G5 identifies the existence of a rational line with triviality of its ruling character and hence with triviality of the Serre character. G6 proves that oddness preserves its value on the original Frobenius. Returning \(+1\) or \(-1\) therefore computes the exact character of the specified polarized ideal. This proves Theorem A, using Theorem B proved in B0–B6.

## C2. Proof of the isogeny-class decision

M2 computes all full ideal classes and every principal-polarization orbit by terminating unconditional arithmetic. There are finitely many pairs. For each, Theorem A terminates and returns the correct original-field character. If any output is \(+1\), the corresponding ppav is a canonically polarized genus-three Jacobian over \(k\); its verified Weil polynomial is \(h\), so Honda–Tate places its underlying abelian variety in the requested class. This proves YES soundness.

Conversely, any genus-three curve over \(k\) with Jacobian in that class yields a polarized Deligne object among the complete pairs of M2. The marked realization gives a polarized-isomorphic model, so its character is trivial and it returns \(+1\). Therefore rejecting all pairs proves nonexistence. This proves YES completeness and NO soundness. It is essential to consider every principal polarization, not just one polarization on each unpolarized object.

Alternatively, M3–M6 return exactly the unweighted count \(N(q,h)\) of pairwise distinct polarized classes. The injection from the retained models into the counted classes is a bijection at that cardinality, and every needed candidate occurs after finite time. Applying bounded G1–G6 to this finite complete list has the same YES and NO proofs. The alternative does not acquire labels merely from the count; genuine labels are supplied only by Part II.

The empty-list branch \(N=0\) is harmless. Howe's principal-polarizability theorem excludes it for the promised simple odd-dimensional class, but the general count-and-search logic does not rely on that existence result. This proves Theorem C.

## C3. Characteristic and marking safeguards

In characteristic two, the Frobenius fingerprint uses prime-to-characteristic torsion. The lift certificate uses the original base-linear \(q\)-Frobenius and the full polynomial relation, not an arbitrary CM deformation. The geometric involution is the constant étale group of order two. Invariant differential sections are a kernel, with no division by two. The ruling decision is a polynomial-identity line test; its optional scalar alternative is an Artin–Schreier trace test. The good-point bound counts geometric two-torsion points only and retains inseparable multiplicities. Odd extension preserves the order-two character even though the scalar signs coincide in the ground field.

In characteristic three, the complete \(|3\Theta|\) embedding still exists. The model comparison preserves an actual theta divisor after translation and never cancels three from a polarization morphism. The division by three in D4 occurs instead in torsion-free integral cohomology of the complex canonical lift, with a certified cube identity. These are different operations.

The residue extension of a lift certificate never replaces \(q\)-Frobenius by \(q^m\)-Frobenius. Matching only a characteristic polynomial, CM type, endomorphism ring, or local Tate modules would be insufficient. The fixed comparison and the integral unimodular equalities are what certify the particular ideal and polarization orbit.

## C4. Established inputs and exact uses

1. Deligne's ordinary equivalence and algebraic canonical-lift descent, and Marseglia's polarized square-free and arbitrary-order ideal-class-monoid results, supply the objects and finite orbit list. M2 proves the additional scalar-equality guard explicitly. Lenstra's unconditional unit/class-group construction and the finite conductor-quotient transfer supply the arithmetic. No GRH-dependent termination assumption is made.
2. Standard abelian-variety theory supplies rational theta divisors over finite fields, very ampleness of \(3\Theta\), the cohomology and degree formulas, prime-to-characteristic torsion, Weil bounds, and Picard descent. M3–M5 make the finite scheme, divisor, torsion, and comparison witnesses explicit.
3. Exact projective algebra, Gröbner bases, syzygies, localization and coherent-sheaf calculations supply the finite geometric checks. Smith's algorithms supply actual global-section representatives; G4 gives their pullback and multiplication arithmetic.
4. Serre–Tate deformation equivalence, homomorphism descent over regular extensions, and the Néron property of an abelian scheme supply the lift/descent facts used in D3 and D6. D3 separately proves canonicity from the checked Frobenius relation. D6 separately accounts for the homomorphisms, polarization, theta section, and complete finite tuple.
5. Semialgebraic triangulation, real quantifier elimination, simplicial approximation, and integral simplicial homology justify D4. The finite-witness method computes maps and integral classes, not just rational Betti numbers.
6. Beauville–Ritzenthaler supplies the all-characteristic recognition and Serre-character equality under the checked hypotheses. Étale/fpqc descent supplies the invariant differential interface. The optional Clifford-center and scalar calculations are alternatives to the main finite line test.
7. The finite-quotient cohomology calculation, Künneth, trace formula, pure Weil weights, intersection theory, and the Lachaud–Rolland geometric projective-degree bound prove B0–B6. The numerical threshold replaces the need for Lang–Weil as a stopping dependency in this strengthened algorithm.
8. Honda–Tate interprets equality of Weil polynomials as equality of finite-field isogeny classes.

The established recognition theorem and classification theorems are credited inputs, not newly asserted theorems of this synthesis. The proof requires no numerical period recognition, theta-series zero oracle, modular-form normalization formula, or characteristic-two equation for the exceptional divisor. It is relative to the cited established results, as an exact mathematical algorithm proof normally is.

## C5. Certificates and validation boundaries

A possible complete execution can retain the ideal and polarization-orbit list; all projective equations, group laws, Cartier and line-bundle witnesses; the exact torsion fingerprint; and either count-certified deduplication records or the marked lift certificates. A marked certificate includes its number-field localization, special-fiber identification, original Frobenius lift, semialgebraic topology witnesses, integral maps and pairings, and the unimodular matching matrix. A smooth-theta recognition certificate includes the selected odd extension, good point, intersection, involution, differential representatives, canonical quadric, and exact ruling test. A YES line is a short positive witness; exhaustive finite checks can certify a NO in this deliberately noncompetitive procedure.

No such nontrivial end-to-end model or marked-lift computation has been performed for this manuscript. The earlier arithmetic validation compared scalar splitting with point counts on 71,472 canonical four-dimensional forms over \(\mathbb F_2,\mathbb F_4,\mathbb F_8,\mathbb F_{16},\mathbb F_3,\mathbb F_5,\mathbb F_7\). An independent 622-form Clifford/line/scalar check covered \(\mathbb F_2,\mathbb F_4,\mathbb F_8,\mathbb F_3,\mathbb F_5\), with a 78-form systematic sample over \(\mathbb F_8\). All reported tests passed. These finite checks support only the tested arithmetic conventions.

For the bounded theorem, independent exact arithmetic reproduced the two shifted polynomial identities, their positive coefficients, the boundary values, and every small-field degree case. An independent graded-swap calculation reproduced the symmetric-square Betti numbers. These are finite checks of arithmetic and linear algebra; the geometry is justified by the written proof. Independent mathematical reviews accepted the aggregate theorem, marked inverse, and bounded-point theorem at their stated theoretical scopes. This integrated presentation is an assembly of those arguments, not an additional computational proof experiment.

## C6. Stated requirements and practical aspirations

The exact source input, the original-field existence output, completeness across polarization orbits, and a connection through the geometric recognition method are all supplied. The additional per-ideal marking makes that connection objectwise. The full comparison convention is effective mathematical bookkeeping required to give a marked Deligne input its meaning; it is not an unfulfilled source requirement. Any other effective full convention may be used consistently, and the class-level existence answer is independent of the convention because every polarized class is included.

No stated mathematical requirement in the displayed source problem remains identified as unmet by this theorem. A fast direct criterion, useful height or precision bounds, short practical certificates, production software, a nontrivial end-to-end instance, optimality of the extension bound, historical intent, and priority remain separate questions. They should not be silently promoted into source hypotheses, and their absence should not be hidden by an unqualified practical claim. No worldwide novelty or historical closure assertion is made.


## References and bounded inspection record

The cited dependencies are credited to their existing authors. The inspection record reports the source work supporting the component proofs and source audit; it is not a claim that every original proof and every underlying dependency was independently reproved.

- **[Howe 2006]** Everett W. Howe, *Low-genus curves over finite fields: Problems and variations*, IPAM workshop talk, October 2006. PDF pages 37–38 are the target; pages 29–36 supply recognition and descent context. These relevant pages were inspected; the complete slide deck was retained, not reread in full. https://ewhowe.com/talks/IPAM.pdf
- **[Marseglia]** Stefano Marseglia, *Computing square-free polarized abelian varieties over finite fields*, Math. Comp. 90 (2021), 953–971, arXiv:1805.10223v3. Sections 3–6, especially Theorem 5.4, Algorithms 1–3 and Theorems 6.1–6.4, give the ideal and polarization interfaces. The conjugate trace dual and positivity convention were visually checked in Theorem 5.4. Section 8 supplies existing canonical-lift period conventions. Part II gives its own finite certificate realization and does not call that discussion as a geometric realization oracle. The relevant theorem/algorithm portions were inspected; a fresh proof audit of every source result is not claimed. https://arxiv.org/abs/1805.10223v3
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

The earlier source audit did not fully inspect Deligne's original; the marked-inverse work subsequently read its complete six-page text, and the independent marked audit directly checked the relevant comparison and descent sections. Howe's 1995 original was not fully inspected. The combined literature inspection remains bounded and does not certify worldwide originality, openness, or nonexistence of prior work.

### Additional marked and bounded references

- **[Deligne 1969]** Pierre Deligne, *Variétés abéliennes ordinaires sur un corps fini*, Invent. Math. 8 (1969), 238–243. The marked work read the complete six-page retained original. Sections 1–3 and 6–8 were independently checked for comparison, algebraic descent, Frobenius, and equivalence. https://publications.ias.edu/sites/default/files/Number6.pdf
- **[Katz]** Nicholas M. Katz, *Serre–Tate local moduli*. Theorem 2.1(1),(4), printed pp.148–149, was directly inspected for deformation equivalence and the homomorphism criterion; the full paper was retained but not independently audited in full. https://web.math.princeton.edu/~nmk/old/serretatelocmod.pdf
- **[BLR]** Siegfried Bosch, Werner Lütkebohmert, Michel Raynaud, *Néron Models*, §1.2 Proposition 8 and proof, printed p.15. The original chapter scan was retained and visually inspected for the theorem that an abelian scheme is the Néron model of its generic fiber. This is the original source used in D6. https://math.arizona.edu/~cais/scans/BLR-Neron_Models/neron1.pdf
- **[Hom descent]** Milne, *Abelian Varieties*, AV110, Corollary 15.4(b) and proof, printed pp.58–59, were inspected for homomorphism descent over regular extensions. https://www.jmilne.org/math/CourseNotes/AV110.pdf
- **[Basu–Karisani]** Saugata Basu and Negin Karisani, *Efficient simplicial replacement of semialgebraic sets*, Forum of Mathematics, Sigma (2023). The introduction was inspected for classical semialgebraic triangulation and quantifier-elimination context. Its efficient rational-homology results are not substituted for the explicit integral-map witnesses in D4. https://arxiv.org/abs/2207.10497
- **[Schnell]** Christian Schnell, Lecture 4 on the Appell–Humbert theorem, p.3, was inspected for the Chern-form convention. Together with visual inspection of Marseglia §8, it fixes the explicitly proved sign conversion in D4. https://www.math.stonybrook.edu/~cschnell/mat615/lectures/lecture4.pdf
- **[Lachaud–Rolland]** Gilles Lachaud and Robert Rolland, *On the Number of Points of Algebraic Sets over Finite Fields*, Theorem 2.1 and Proposition 2.3. The definitions and relevant statements and surrounding argument were inspected for geometric projective sets not defined over the counting field. The whole paper was not independently audited. https://arxiv.org/abs/1405.3027
- **[Étale cohomology]** Milne, *Lectures on Étale Cohomology*, Proposition 8.3(c), Example 12.3, Theorem 17.7, Theorem 22.1, Proposition 27.3, and Theorem 27.15 were inspected for finite pushforward, base change, Künneth, trace, and weights. The symmetric-square invariant calculation is written out in B2; the full notes were not independently audited. https://www.jmilne.org/math/CourseNotes/LEC.pdf

The complete Beauville–Ritzenthaler text was reread for the bounded theorem and its independent audit. The constants 2268 and \(B(Q)\), the sufficient threshold 81, and the odd-degree-at-most-seven and density consequences are derived in Part III; no such numerical bound was located in the inspected BR text. The bounded public search does not establish that the specialization never appeared elsewhere. Standard dependencies are credited, and their original proofs are not all reproduced here.
