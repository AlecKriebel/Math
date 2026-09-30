# Brauer groups of tame curves: a generically schematic formula and the gerbe gap

**Target:** 30005975 / OWR-14298584-008.  
**Status:** full arbitrary-stack question unresolved; partial deductions awaiting separate adversarial review. Three approaches used. No novelty or human peer-review claim.

## 1. Exact scope and convention

Achenjang's original Question 1, OWR 40/2024, printed p.2337, concerns tame stacky curves over an algebraically closed field. The definition on p.2336 is a separated, finite-type algebraic stack, pure of dimension one, with finite inertia. It does not assume smoothness, properness, trivial generic stabilizers or the Deligne–Mumford condition. It explicitly defines

\[
\operatorname{Br}'(\mathcal X)=H^2_{\mathrm{et}}(\mathcal X,\mathbb G_m)_{\mathrm{tors}}.
\]

We use this cohomological convention throughout; on algebraic stacks, cohomology is taken on the lisse-étale site, with the usual comparison to fppf cohomology for the smooth coefficient group Gm. No general equality with the Azumaya Brauer group is asserted here. [Complete original report, pp.2336–2339](https://ems.press/content/serial-article-files/50042).

Tame means that the finite geometric stabilizer group schemes are linearly reductive. In characteristic p this permits connected diagonalizable groups such as μp. It means prime-to-p stabilizer order only in the Deligne–Mumford case.

The original report already proves a restricted locally-Brauerless formula. Achenjang's current preprint supplies more general tools. Bishop computes arbitrary singular tame Deligne–Mumford curves with trivial generic stabilizer, and studies μr-gerbes over them. These results do not automatically cover the original definition. The deductions below use and credit these inputs.

## 2. A formula when there is a dense schematic open

**Theorem 1.** Let k be algebraically closed and let X be a separated, finite-type, tame algebraic stack with finite inertia, pure of dimension one, with coarse space c:X→C. Suppose there is a dense open U⊂C meeting every irreducible component such that X_U→U is an isomorphism. Let z1,…,zs be the points of the finite complement C\U, and choose geometric points of X over them. Let G_i be their finite stabilizer group schemes and Q_i their maximal étale quotients, regarded as finite abstract groups. Then

\[
H^2(\mathcal X,\mathbb G_m)
\cong\bigoplus_{i=1}^s H^2(Q_i,k^\times),
\tag{1}
\]

with trivial actions on k×. The groups on the right are finite, so (1) also computes Br′(X). Unstacky points contribute zero. In characteristic p>0 there is no p-primary contribution to (1).

No smoothness or properness is required. For Deligne–Mumford X this is Bishop's Proposition 3.7 in degree two. The argument below includes connected tame inertia by applying Achenjang's local results. This is a deduction from those prior results; priority for this formulation is not established.

**Local calculation.** Work at a closed point of C. The local quotient theorem for tame stacks gives, after strict henselization, a presentation [Spec A/G] with A strictly henselian local and finite over the strictly henselian coarse local ring. The residue field is k. Write

\[
1\longrightarrow\Delta\longrightarrow G\longrightarrow Q\longrightarrow1
\]

for the connected–étale sequence. In characteristic p>0, Δ is diagonalizable of p-power order and |Q| is prime to p. In characteristic zero Δ is trivial.

Achenjang's Propositions 4.3–4.4 give H²([Spec A/Δ],Gm)=0, show that its Picard group M is killed by |Δ|, and give the exact tail

\[
M^Q\longrightarrow H^2(Q,k^\times)
\longrightarrow H^2([\operatorname{Spec}A/G],\mathbb G_m)
\longrightarrow0.
\tag{2}
\]

The middle group is killed by |Q|, by the transfer argument for finite-group cohomology. The first group is killed by |Δ|. These orders are coprime, so the first arrow is zero. Therefore the last map in (2) is an isomorphism. In characteristic zero M=0 and the same conclusion holds. This is also compatible with restriction to the residual gerbe, whose corresponding computation gives H²(BG_i,Gm)=H²(Q_i,k×).

**Global calculation.** The coarse space is a separated finite-type one-dimensional algebraic space over k. It is a scheme, since separated locally Noetherian algebraic spaces are schemes at all points of local dimension at most one. [Stacks Project, Tag 0ADD](https://stacks.math.columbia.edu/tag/0ADD).

For q>0, R^q c_*Gm vanishes over U and is supported on the finite complement. A sheaf supported on finitely many algebraically closed points has no positive cohomology. Also H^j(C,Gm)=0 for j≥2 by the curve form of Tsen's theorem, including singular and nonreduced curves; this form is recorded as Bishop's Theorem 2.7. The low-degree terms of Leray therefore give

\[
H^2(\mathcal X,\mathbb G_m)
\cong H^0(C,R^2c_*\mathbb G_m).
\]

Indeed H²(C,Gm), H¹(C,R¹c_*Gm), H²(C,R¹c_*Gm) and H³(C,Gm) all vanish, so no differential enters or leaves the remaining total-degree-two term. The local calculation identifies its stalks, proving (1). Finite-group Schur multipliers and the prime-to-p orders of Q_i give the finiteness and p-primary assertions. ∎

The relevant local results and their proofs were checked in [Achenjang, Sections 4.1–4.2](https://arxiv.org/pdf/2410.06217v3). The finite-support Leray argument in the Deligne–Mumford case is explicitly [Bishop, Proposition 3.7](https://arxiv.org/pdf/2507.08780v2). The theorem above does not permit replacing the dense-schematic-open hypothesis by a statement about only the set of geometric automorphisms: the whole stabilizer **group scheme** must be trivial there.

## 3. The same coarse curve and stabilizers can give different Brauer groups

Let ℓ be a prime invertible in k, and choose an identification μℓ≅Z/ℓ. Write

\[
\mathcal Y=\sqrt[\ell]{\mathcal O_{\mathbb P^1}(1)/\mathbb P^1}
\]

for the gerbe of ℓth roots of O(1), not the root stack along a divisor. Consider

\[
\mathcal X_0=\mathbb P^1\times B(\mu_\ell\times\mu_\ell),
\qquad
\mathcal X_1=\mathcal Y\times B\mu_\ell.
\]

Both are smooth proper tame Deligne–Mumford curves. Both have coarse space P¹ and stabilizer μℓ×μℓ at every geometric point, including the generic point. Nevertheless,

\[
\operatorname{Br}'(\mathcal X_0)\cong\mathbb Z/\ell,
\qquad
\operatorname{Br}'(\mathcal X_1)=0.
\tag{3}
\]

Here the global gerbe class, rather than an isolated orbifold-point list, changes the answer. This is a diagnostic against computing the arbitrary case from only a coarse curve and stabilizer isomorphism types, not a counterexample to the original request to compute the full stack's Brauer group.

**The neutral case.** For the finite constant group A=(Z/ℓ)², descent gives H²(BA,Gm)=H²(A,k×). Central extensions by k× are classified by the alternating commutator of lifts of the two generators: their ℓth powers can be normalized to one since k× is divisible, and the remaining commutator is an arbitrary ℓth root of unity. Thus H²(A,k×)≅μℓ. Explicitly, for a primitive root ζ, the cocycle

\[
c((a,b),(a',b'))=\zeta^{ba'}
\]

has commutator ζ^(ba'−b'a) and generates this group.

Projection P¹×BA→BA has R¹Gm=Z, R²Gm=0 and the global relative O(1). The differential from H⁰(BA,Z) vanishes because O(1) exists; H¹(BA,Z)=Hom(A,Z)=0. Its Leray sequence therefore identifies H²(P¹×BA,Gm) with H²(BA,Gm), proving the first claim. This neutral Schur-multiplier contribution is already discussed in Achenjang's Example 1.10; the projective-line factor changes none of it.

**The nonneutral case.** The gerbe Y has a tautological line bundle L with L^ℓ=π*O(1). The usual character-weight exact sequence

\[
0\longrightarrow\operatorname{Pic}(\mathbb P^1)
\longrightarrow\operatorname{Pic}(\mathcal Y)
\longrightarrow\mathbb Z/\ell\longrightarrow0
\]

and the weight-one bundle L show that Pic(Y)=Z generated by L, with π*O(1) corresponding to ℓ. In particular Pic(Y) has no ℓ-torsion. Its global units are k×. Kummer therefore gives H¹(Y,μℓ)=0, hence H¹(Y,Z/ℓ)=0.

For an ℓth-root gerbe the local higher pushforwards are R¹π_*Gm=Z/ℓ and R²π_*Gm=0. These follow étale-locally from the cyclic group calculation over strictly henselian local rings; units are ℓ-divisible. Since H²(P¹,Gm)=0 and H¹(P¹,Z/ℓ)=0, Leray gives H²(Y,Gm)=0. Apply the same relative cyclic-gerbe calculation to X1=Y×Bμℓ→Y. All its total-degree-two terms vanish, so H²(X1,Gm)=0, as required. ∎

These computations use standard gerbe and cyclic-classifying-stack sequences appearing in Achenjang and Bishop; they are not new theorems about those sequences. Neither X0 nor X1 satisfies the dense-schematic-open hypothesis of Theorem 1.

## 4. Connected tame generic inertia can produce an infinite p-primary group

Suppose char k=p>0. The stack

\[
\mathcal Z=\mathbb A^1_k\times B\mu_p
\]

is a tame algebraic stack of the original source's type. The group μp is diagonalizable and linearly reductive even though it is not étale; its representations are graded by Z/p, and taking the degree-zero summand is exact. Thus Z is not Deligne–Mumford, and excluding it would narrow the target.

Achenjang's Proposition 3.9, applied to the connected cyclic group μp over A¹, gives

\[
H^2(\mathcal Z,\mathbb G_m)
\cong H^2(\mathbb A^1,\mathbb G_m)
\oplus H^1_{\mathrm{et}}(\mathbb A^1,\mathbb Z/p)
\cong k[x]/\{h^p-h:h\in k[x]\}.
\tag{4}
\]

The second identification is the Artin–Schreier exact sequence and H¹(A¹,O)=0. This is a group quotient for addition, not an ideal quotient of rings. Every element is killed by p, so H² here already equals Br′.

There is an explicit additive normal form:

\[
\operatorname{Br}'(\mathcal Z)
\cong\bigoplus_{\substack{d\ge1\\p\nmid d}}(k,+)
\quad\text{as }\mathbb F_p\text{-vector spaces}.
\tag{5}
\]

Indeed constants vanish in (4) because k is algebraically closed. If a positive-degree term ax^(pe) occurs, choose the unique pth root b=a^(1/p) in the perfect field k; subtracting (bx^e)^p−bx^e replaces it by bx^e and lowers its degree. Repeating leaves only positive exponents prime to p. The representative is unique: if a nonzero polynomial in those exponents were h^p−h with h nonconstant, its top degree would be p·deg h, divisible by p, a contradiction. A constant h cannot supply such a polynomial. The reduction is additive and Fp-linear because Frobenius and its inverse are additive.

Thus a finite list of stabilizer group schemes is not, by itself, a reason to expect the Brauer group to be finite. Formula (5) is a structural formula over an arbitrary algebraically closed field; an executable algorithm for coefficients presupposes effective field operations and Frobenius-root access. This example is a direct application of a credited classifying-stack theorem, supplemented by the elementary Artin–Schreier normal form. It does not contradict Theorem 1: μp is the nontrivial generic stabilizer.

## 5. What remains unresolved

The original arbitrary-stack request includes nontrivial generic inertia, nontrivial global bands and gerbe classes, and singular coarse curves. Theorem 1 computes a large but explicitly smaller case. Equations (3) show why merely inserting all pointwise Schur multipliers into that formula fails for generic gerbes. Equations (4)–(5) explain why the source's non-Deligne–Mumford cases cannot be dismissed as wild or assumed to have finite output.

The coarse-space Leray spectral sequence remains a useful organization of the general problem. When generic inertia is present, R¹c_*Gm and R²c_*Gm need not have finite support, and their cohomology, transgressions and resulting extensions require actual computation. Naming these terms is not a computation of the arbitrary Brauer group. No general determination of those maps and extensions is supplied here.

All literature inputs and special cases are credited. Later work on tame nodal curves retains proper Deligne–Mumford and trivial-generic-stabilizer conventions, and later classifying-stack computations for smooth connected semisimple groups address different inertia. No retrieved result has been verified to cover the full original scope, but this bounded search is not a certification that no such result exists. The target remains unresolved by this package.
