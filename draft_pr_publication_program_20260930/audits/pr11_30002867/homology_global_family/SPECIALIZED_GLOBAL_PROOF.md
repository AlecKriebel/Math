# Checkable specialized global proof for finite-colength ideals

**Supplemental status:** independent reconstruction passed a separate in-depth falsification audit; optional source/transition clarifications were then applied. The core candidate acceptance does not depend on this supplement, because the original Mohan Kumar theorem has been directly verified.

This is an independently reconstructed proof of the precise global bridge required by the frozen candidate. It reduces the general stable-range theorem to two classical projective-module inputs and elementary finite-algebra arguments. It does not claim a new theorem.

## Classical inputs

(A) Quillen's global monic-inversion theorem (1976, Theorem 3, printed p.169): if B is a Noetherian ring, P is finitely generated projective over B[X], and P_f is free for a monic f in B[X], then P is free. In particular, a unimodular row over B[X] with a monic entry is completable to an invertible matrix: its projective kernel becomes free after inverting that entry, so (A) makes its kernel free, and a choice of a splitting plus kernel basis completes the row.

(B) Quillen–Suslin: every finitely generated projective module over a polynomial ring over a field is free.

These are exactly the two freeness inputs used in Mohan Kumar's original 1978 proof on printed p.235, citing Quillen [7, Theorems 3 and 4]. The original 1978 theorem itself has now been directly inspected. This reconstruction is useful for checking how those inputs work for the finite-colength case; its individual steps do not rely on a general Murthy conjecture or on the erroneous 2016 stronger lifting assertion.

## Proposition

Let R=C[x_1,...,x_d], with proper finite-positive-colength I, and put r=mu_{R/I}(I/I^2). If r>=2, then mu_R(I)=r.

### Step 1: a monic conormal representative

Let B=C[x_1,...,x_{d-1}] and X=x_d, so R=B[X]. Choose r elements a_1,...,a_r of I whose classes generate I/I^2. Let h(X) be the characteristic polynomial of multiplication by X on the finite algebra R/I. Cayley–Hamilton, applied to its unit class, proves h(X) in I. The polynomial is monic. Choose m>=2 such that m deg_X h>deg_X a_1. Then f_1=a_1+h^m is monic in X and has the same class in I/I^2 as a_1. Write J=I intersect B. The injection B/J -> R/I makes B/J a finite-dimensional C-algebra. Consequently

    C_0=R/(JR+(f_1))

is a finite-dimensional C-algebra, because f_1 is monic.

### Step 2: remove finitely many extraneous points over J

There are finitely many maximal ideals p of R containing JR+(f_1). Call one bad if it does not contain I. For each bad p, I^2+p=R. By the Chinese remainder theorem, the map I^2 -> product_{bad p} R/p is surjective: the image is an ideal of that product that projects onto every field factor, hence is the entire product. Choose b in I^2 whose residue at every bad p is 1-a_2. Put

    f_2=a_2+b,   f_i=a_i (i>=3),   F=(f_1,...,f_r).

Then I=F+I^2, and every maximal ideal containing F+JR contains I. This uses r>=2. No prime-avoidance assertion about an infinite collection of primes is needed.

### Step 3: generation near the support with a denominator from B

Let S=1+J subset B. Since I is proper, J is proper and 0 is not in S. Every maximal ideal of S^{-1}B contains J: if a maximal ideal avoided an element j in J, the image of j would be nonzero in its residue field, and the inverse of j in its residue field could be represented by b/u with b in B and u in S, so u-bj, an element of 1+J, would vanish; this contradicts that 1+J has been inverted. More formally, this is the standard localization placing J in the Jacobson radical. The finite integral extension

    S^{-1}B -> S^{-1}R/(f_1)

therefore places J in the Jacobson radical of the target as well. Any maximal ideal of S^{-1}R containing F thus contains J, and its contraction to R contains I by Step 2 (the quotient C_0 is Artinian, so primes containing f_1+J are maximal).

At a maximal ideal q of S^{-1}R containing F, the equality I=F+I^2 and I subset q let local Nakayama give I_q=F_q. At a maximal ideal not containing F, both are the unit ideal. Hence S^{-1}I=S^{-1}F. Since I/F is finitely generated, there is g in S annihilating it. Write g=1+s with s in J; then I_g=F_g. If s=0, already I=F and the conclusion follows.

### Step 4: compatible surjections on a two-open cover

Assume s!=0. Since s in J subset I, I_s=R_s. The two principal opens D(g),D(s) cover Spec R because g-s=1. On D(g) take the surjection

    q_g:R_g^r -> I_g,       q_g(v)=sum f_i v_i.

On D(s) take the surjection

    q_s:R_s^r -> I_s=R_s,  q_s(v)=v_1.

On D(gs), the row f=(f_1,...,f_r) is unimodular and f_1 remains monic over B_{gs}[X]. Its kernel is finitely generated projective and becomes free when f_1 is inverted, so input (A) makes it free. Choose U in GL_r(R_{gs}) satisfying fU=(1,0,...,0). Thus q_g U=q_s on the overlap.

Glue R_g^r and R_s^r by the transition v_g=U v_s from the s-chart to the g-chart. The result is a finitely generated locally free R-module P of rank r, hence a finitely generated projective module. The compatible maps q_g and q_s glue to a surjection P -> I. This is ordinary gluing of vector bundles on the cover, and avoids the Ext-group machinery of the original proof. It makes no assertion that I itself is locally free when r>d.

### Step 5: global freeness and equality

Input (B) makes P free of rank r. Hence I has r polynomial generators. Conversely any ideal generating list maps to a conormal generating list, so mu_R(I)>=r. Therefore equality holds.

For d>=2 the earlier homological height bound gives r>=d>=2, so this proposition applies to every ideal in the target, including ideals that are not locally complete intersections. When d=1, the PID argument covers r=1 separately.

## Bridge audit

* Cayley–Hamilton is applied to the regular quotient algebra, so an operator relation is a polynomial relation in I.
* B/J is finite-dimensional; adjoining X and imposing a monic relation preserves finite-dimensionality, so the bad set is actually finite.
* Altering f_2 by I^2 preserves conormal generation and removes every bad maximal ideal.
* Nakayama is applied only after localization at maximal ideals containing I; no false global Nakayama is used.
* The denominator g is in B, so monicity survives both localizations used in the overlap.
* The overlap row is unimodular because s lies in I, not merely because the rows generate conormal classes.
* The glued object is a rank-r projective module surjecting I. Its kernel near the support may be nonprojective. Gluing the free source bundles bypasses this issue.
* No lift of an arbitrarily prescribed conormal basis is claimed; the proof first modifies representatives.

## Direct source record

Mohan Kumar, *On Two Conjectures About Polynomial Rings*, Invent. Math.46 (1978), pp225–236, original Theorem5 printed pp234–235: https://gdz.sub.uni-goettingen.de/download/pdf/PPN356556735_0046/LOG_0020.pdf . Theorem5 explicitly permits a field or PID base and uses the non-strict inequality mu(I/I^2)>=dim(R/I)+2. Independent visual inspection of pp234–235 agrees with the frozen candidate's field specialization. The source was recovered by the primary-source family and then inspected independently here.

Quillen, *Projective modules over polynomial rings*, Invent. Math.36 (1976), 167–171, original Theorems3–4 on p.169: https://gdz.sub.uni-goettingen.de/download/pdf/PPN356556735_0036/LOG_0016.pdf . Theorem3 uses an arbitrary commutative base ring; freeness after one monic inversion implies its stated freeness after all monic inversions.
