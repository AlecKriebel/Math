# Independent reconstruction of Farb Question 7.6

Author of this reconstruction: Codex research family `source_question_family`, working from the original question and mathematical background only. Prepared 2026-10-17. This document makes no priority or novelty claim.

## 1. Exact claim and conventions

Let S_g be the closed oriented surface of genus g >= 2 and let Mod_g consist of orientation-preserving mapping classes. Put pi_0 = pi_1(S_g), pi_{j+1} = [pi_0, pi_j], and

    I_g(k) = ker(Mod_g -> Out(pi_0 / pi_k)).

Thus I_g(1) is Torelli and I_g(2) is the Johnson kernel. This is the indexing on printed p.14 of Farb's chapter, PDF p.21 of the author-hosted volume [F].

For H <= Mod_g and t > 0, define

    m_H(t) = #{[f]_{Mod_g}: f is pseudo-Anosov,
                              f belongs to H, log(lambda(f)) = t}.

The conjugacy is in Mod_g, even when H is a proper subgroup. The issue is whether a single finite constant, allowed to depend on g and k, bounds m_{I_g(k)}(t) for every t. The target includes powers. It is not the simple-loop restriction in Question 7.7.

**Theorem reconstructed here.** For each fixed g >= 2 and each fixed finite k >= 3, and every positive integer N, there exist N pseudo-Anosov elements in I_g(k) with one common dilatation and pairwise distinct Mod_g conjugacy classes. In particular the answer to Question 7.6 is negative.

The proof below uses Horowitz's established trace-word theorem, the established Thurston disk construction, standard hyperbolic ping-pong, and an elementary compact-core lemma proved in full here. No unsupported multiplicity transfer from subgroup conjugacy is used.

## 2. Centrality and its indexing

Write gamma_n(pi) for the conventional lower central series with gamma_1(pi)=pi, so pi_j=gamma_{j+1}(pi). Let A(k) consist of automorphisms acting identically on pi/pi_k. The elementary lower-central-series automorphism calculation gives

    alpha in A(k), x in pi_j  =>  alpha(x) x^{-1} in pi_{k+j}.

One proves this by induction on j, expanding commutators and using

    [pi_i, pi_j] <= pi_{i+j+1}.

Products and inverses preserve the asserted congruence, so it suffices at the inductive step to use generators [u,v] with u in pi_0 and v in pi_j. Substituting alpha(u)=u times an element of pi_k and alpha(v)=v times an element of pi_{k+j} changes [u,v] by an element of pi_{k+j+1}.

If alpha in A(k), beta in A(l), write alpha(x)=x u and beta(x)=x v with u in pi_k and v in pi_l. Modulo pi_{k+l}, the preceding calculation gives

    alpha beta(x) = x u v,
    beta alpha(x) = x v u.

These agree because [pi_k,pi_l] <= pi_{k+l+1} <= pi_{k+l}. Consequently

    [A(k), A(l)] <= A(k+l).

For an outer automorphism trivial on pi/pi_k, choose an automorphism representative and compose it with an inner automorphism lifting the inner automorphism induced on that quotient. The resulting representative belongs to A(k). Applying the calculation to such representatives proves

    [I_g(k), I_g(l)] <= I_g(k+l).                 (2.1)

This argument handles the outer-automorphism convention explicitly. In particular, an r-fold lower-central commutator in elements of I_g(2) lies in I_g(2r).

## 3. A hyperbolic element at any specified depth

Choose filling separating simple curves a,b on S_g. Existence in every genus g >= 2 is stated in [F], printed p.51. One can also see existence by taking any separating a and b=f^n(a), where f is pseudo-Anosov and n is sufficiently large: otherwise a sequence of normalized curves disjoint from both a and f^n(a) would have a measured-lamination limit disjoint from the filling, uniquely ergodic attracting lamination of f; the limit would be proportional to that lamination and could not also be disjoint from a.

Let A=T_a and B=T_b. Both lie in I_g(2). Set mu=i(a,b). Since the curves fill, Euler characteristic gives mu >= 2g-1, and separating curves have even geometric intersection. Therefore mu >= 4, including when g=2.

Thurston's rectangle construction supplies a Teichmuller disk D stabilized by F_0=<A,B>, with faithful derivative representation. After a choice of coordinates its generator matrices are

    a_mu = (1  mu)       b_mu = ( 1  0)
           (0   1),            (-mu 1).

For mu>2 these generate a free group, also directly by projective-line ping-pong. The construction and the faithful representation for filling pairs are the mechanism discussed in [F], printed p.51; the disk-stabilizer facts used below are recorded in [L], Theorems 3.1-3.2.

Define c_1=A and c_r=[B,c_{r-1}] for r>=2, with [x,y]=xyx^{-1}y^{-1}. By (2.1),

    c_r belongs to I_g(2r).                       (3.1)

There is a particularly transparent check that c_r is hyperbolic. If C=(p q; r s) is a determinant-one matrix, then

    ([b_mu,C])_12 = -mu q^2,
    tr([b_mu,C]) = 2 + mu^2 q^2.                 (3.2)

Starting with q=mu for c_1 gives, for r>=2,

    (rho(c_r))_12 = -mu^(2^r-1),
    tr(rho(c_r)) = 2 + mu^(2^r) > 2.             (3.3)

Thus c_r is a genuine hyperbolic element of the derivative group, not a possibly trivial abstract commutator.

Fix k>=3 once and for all and choose

    r = max(2, ceil(k/2)).

Then c=c_r belongs to I_g(k). Choose a sufficiently large integer M and set d=B^M c B^{-M}. Normality of I_g(k) shows d belongs to the very same fixed term. The fixed points of rho(c) do not contain 0, since its upper-right entry is nonzero. The parabolic rho(B)^M sends every boundary point other than 0 towards 0 as |M| tends to infinity. Hence M can be chosen so that the two fixed-point sets of rho(c) and rho(d) are disjoint.

Standard hyperbolic ping-pong now supplies L>=1 such that

    H = <c^L,d^L> <= I_g(k)

is free of rank two and rho(H) is a convex-cocompact Fuchsian group. More explicitly, take disjoint small boundary intervals about the four fixed points. Large powers pair disjoint hyperbolic half-planes with closures separated in H^2. The resulting classical Schottky fundamental region has compact quotient of the convex hull of the limit set. Every nonidentity element of H has hyperbolic derivative and is pseudo-Anosov.

Only this last subgroup H, chosen after k was fixed, will be used in the multiplicity argument. Neither k nor g changes when the required number N grows.

## 4. Uniform control of conjugacy fusion

**Compact-core lemma.** Let G be any discrete subgroup of PSL(2,R), and let J<=G be convex cocompact. There is a finite constant C=C(J,G) such that a G-conjugacy class of hyperbolic elements contains at most C distinct J-conjugacy classes of elements of J.

**Proof.** Let X be the convex hull of the limit set of J. Choose a compact set K in X with J K=X; such a K exists by convex cocompactness. Proper discontinuity of G on H^2 implies that

    S = {s in G: s K intersects K}

is finite. We show C=|S| works.

Fix a hyperbolic u in J. Its axis is in X. Conjugating u inside J if necessary, choose a point x on its axis that lies in K. Suppose v in J and v=t u t^{-1} for t in G. Then t x lies on the axis of v and hence in X. There is j in J with j t x in K. The element s=j t sends x in K into K, so s belongs to S. Moreover

    j v j^{-1} = s u s^{-1}.

Consequently every J-conjugacy class under consideration is represented by s u s^{-1} for at least one s in the fixed finite set S. The same S works for all hyperbolic u. This proves the lemma. QED.

No finite-index, malnormality, or finite-generation condition on G was used. Compactness of the subgroup core is essential: arbitrary infinite-index normal subgroups can have infinitely many subgroup-conjugacy classes in a single ambient class.

Now take

    G = DA_D(Stab_Mod_g(D)),  J = rho(H).

The image G is discrete and the derivative kernel is finite by [L], Theorem 3.1. The restriction to F_0, and therefore H, is faithful. The compact-core lemma applies to J<=G.

If f,h in H are conjugate by z in Mod_g, then z(D)=D. Indeed, f stabilizes D, h stabilizes z(D), and h is pseudo-Anosov. A pseudo-Anosov stabilizes a unique Teichmuller disk by [L], Theorem 3.2. Thus z is in the full stabilizer of D and rho(f),rho(h) are G-conjugate. The lemma therefore bounds by C the number of H-conjugacy classes contained in any one Mod_g-conjugacy class of elements of H. The finite derivative kernel introduces no additional difficulty: faithfulness on H identifies its conjugacy classes with those of J, and ambient conjugacy always implies derivative conjugacy.

This is the required bridge from subgroup multiplicity to the source's ambient multiplicity.

## 5. Arbitrarily large common-length families

Use a free basis x,y for H. Horowitz's original Example 8.2 [H], printed pp.648-649, gives, for each m, 2^m pairwise nonconjugate words having identical trace under every SL(2,C) representation of the rank-two free group. An explicit version is

    W_0 = x,
    W_j = W_{j-1}^{-epsilon_j} y^{2j}
          W_{j-1}^{ epsilon_j} y^{2j-1}
          W_{j-1}^{-epsilon_j} y^{2j}
          W_{j-1}^{ epsilon_j},                 (5.1)

where each epsilon_j is +1 or -1. Here 2j means twice j, not 2 to the power j. The 2^m choices of signs give the family at level m. The unique distinguished syllable y^{2m-1} in its cyclic reduction records the last sign, and the earlier signs are recovered inductively. This is the free-word nonconjugacy mechanism in that example.

For completeness, the trace mechanism uses the basic rank-two trace identity: the trace of any word in U,V is a polynomial in tr(U), tr(V), tr(UV). At the jth sign choice put U=W_{j-1}. All later words are words in U^{-1} y U and y. Replacing U by U^{-1} preserves the traces of those two generators and of their product:

    tr(U^{-1} y U) = tr(U y U^{-1}) = tr(y),
    tr(U^{-1} y U y) = tr(U y U^{-1} y).

It therefore preserves the traces of the later words. Flip one sign at a time to conclude that all members of (5.1) at depth m have the same trace.

Since H is free, its representation into PSL(2,R) lifts to SL(2,R) by choosing lifts of x,y. All the W_m are nonidentity, and every nonidentity element of H is hyperbolic. For a hyperbolic matrix u,

    length_H2(u) = 2 arcosh(|tr(u)|/2).

Thus these 2^m elements have one common positive hyperbolic translation length ell_m. Their associated pseudo-Anosovs have

    log(lambda(W_m)) = ell_m/2

by [L], Theorem 3.1(3). In particular they have exactly the same dilatation, rather than an asymptotically close value.

At most C of their H-conjugacy classes can merge into one Mod_g-conjugacy class. We therefore obtain at least ceil(2^m/C) ambient conjugacy classes at the single value ell_m/2. For a prescribed N, choose m with 2^m>=C N and retain representatives of N ambient classes. All belong to the previously fixed H<=I_g(k). This proves the theorem.

## 6. Boundary cases and scope

- **Genus 2:** the construction uses separating filling curves and mu>=4, so it includes g=2. It uses no Johnson homomorphism that degenerates in this genus.
- **Depth:** each finite k is fixed before H is chosen. Increasing N changes Horowitz depth m, not Johnson depth k.
- **Conjugacy:** classes are distinguished after allowing all orientation-preserving mapping classes as conjugators. No assumption identifies H-conjugacy with ambient conjugacy.
- **Length:** each finite family has one common exact length. A common length for all values of N is not claimed.
- **Finite versus infinite multiplicity:** the conclusion is unbounded multiplicity, namely sup_t m_{I_g(k)}(t)=infinity. It does not assert an infinite multiplicity at a single t. Each common-length family constructed here is finite. No assertion about finiteness of all ambient multiplicities is needed.
- **Powers and primitivity:** the target includes powers, so no ambient primitivity is required or asserted. Horowitz words can be root-free in H; root-freeness in H does not by itself prove root-freeness in Mod_g. A version restricted to ambient primitive elements of I_g(k) is not established here.
- **Simple loops:** no claim is made for Question 7.7 or for simple closed Teichmuller loops.
- **No limiting subgroup:** no claim is made about the intersection of all Johnson terms. The construction is for each finite depth separately.

## 7. Distinct route families tested

| Family | Mechanism | Evidence | Status and exact gap |
|---|---|---|---|
| A. Thurston disk + compact free core + trace words | Deep commutators supply independent hyperbolics; a compact core controls ambient conjugacy; Horowitz gives common traces | Equations (2.1), (3.2)-(3.3), full compact-core proof, established disk/trace theorems | Full-scope derivation above; no mathematical gap identified in this family's audit; independent adversarial review remains appropriate |
| B. Orientable lattice/translation-surface route | Use a familiar lattice Veech curve and enforce Johnson membership via its quotient | [L], Proposition 3.4, printed p.1315: the stabilizer's action on homology is faithful when q is a square | Blocked for that mechanism: its intersection with Torelli is trivial, hence cannot supply the required deep elements. A nonorientable lattice construction would require new input, and is not asserted |
| C. Direct transition-matrix collision route | Engineer equal Perron roots in deep Johnson mapping classes and distinguish their ambient conjugacy | No verified construction obtained in this independent run | Incomplete; simultaneous exact filtration membership, common Perron root, and ambient conjugacy distinction remain unsupported. No conclusion drawn from it |

These routes were considered independently of any submitted proof. Route B's obstruction and Route C's unproved goals are not used as evidence for the theorem.

## 8. Reproducibility and references

`verification.py` uses exact integer arithmetic to check (3.2)-(3.3) for mu=4,5,6 and r=2,...,5, and checks (5.1) through m=5: 32 distinct cyclic conjugacy classes at the largest level, root-free cyclic words, no inverse-conjugate pairs, and a common trace in each of three exact representations. These are finite consistency checks, not replacements for the general proof. See `verification_results.json`.

[F] Benson Farb, *Some problems on mapping class groups and moduli space*, in *Problems on Mapping Class Groups and Related Topics*. Author-hosted volume: https://www.math.uchicago.edu/~farb/papers/mcgbook.pdf . Relevant inspected material: printed p.14 and pp.49-51, PDF pp.21 and 56-58.

[H] Robert D. Horowitz, *Characters of Free Groups Represented in the Two-Dimensional Special Linear Group*, Communications on Pure and Applied Mathematics 25 (1972), 635-649. DOI: https://doi.org/10.1002/cpa.3160250602 . Primary paper copy: https://www.math.purdue.edu/~eremenko/Pdf/horowitz.pdf . Example 8.2, printed pp.648-649, PDF pp.14-15.

[L] Christopher J. Leininger, *On groups generated by two positive multi-twists: Teichmuller curves and Lehmer's number*, Geometry & Topology 8 (2004), 1301-1359. DOI: https://doi.org/10.2140/gt.2004.8.1301 . Publisher PDF: https://msp.org/gt/2004/8-3/gt-v8-n3-p10-s.pdf . Relevant Theorems 3.1-3.2 and Proposition 3.4, printed pp.1314-1315, PDF pp.14-15; printed pp.1313-1318 were inspected.

Exploratory background retrieved but not needed as an authority for the proof: James W. Anderson, *Variations on a theme of Horowitz*, https://eprints.soton.ac.uk/29876/1/horowitz.pdf . Source inspection details, including this exploratory reading and discovery-only web snippets, are in `SOURCES.json`.
