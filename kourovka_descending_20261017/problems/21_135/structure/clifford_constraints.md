# Structural constraints from a hypothetical solvable radical

Status: **partial deductions only; Kourovka 21.135 remains unresolved.** Discovery completion estimate: **12%**. The estimates concern progress toward a complete solution, not a probability that the deductions are correct. This note studies the exact input multiset, without importing character values, tensor products, kernels, or an identification of the socle.

Let D be a finite group's irreducible complex degree multiset, with multiplicities m(d), and put

\[
 n=\sum_d m(d)d^2,\qquad L=\mathop{\rm lcm}_{m(d)>0}d,
 \qquad c=n/L,\quad g=\gcd_d m(d).
\]

All groups below are finite. A nontrivial solvable radical contains a minimal normal subgroup V that is elementary abelian: take a nontrivial minimal normal subgroup inside the last nontrivial derived subgroup of the radical. Thus the absence of abelian normal subgroups is equivalent to trivial solvable radical.

## 1. Itô's denominator bound

**Lemma 1.** If H has degree multiset D and V is abelian normal in H, then |V| divides c.

**Proof.** Itô's theorem says each d in D divides |H:V|. Hence their least common multiple L divides n/|V|, or |V| divides n/L. This theorem concerns normal abelian subgroups; replacing normality by an arbitrary abelian subgroup would give a size bound but not the required divisibility. ∎

An equivalent proof of the underlying divisibility uses Clifford theory. For λ in Irr(V), let I=I_H(λ). A constituent θ of an irreducible χ restricted over λ has degree e, and χ(1)=|H:I|e. The subgroup V/ker λ is central in I/ker λ. Schur's degree divisibility by the index of the center gives e dividing |I:V|, hence χ(1) dividing |H:V|. No assumption that λ extends to I is needed.

**Corollary 2.** If c=1, then every group with degree multiset D has trivial solvable radical. Equivalently, it suffices that for every prime p dividing n there is a degree whose p-part equals the p-part of n. The latter is often phrased as existence of a p-defect-zero character for each p. The characters for different primes may be different.

The equivalence follows by taking prime valuations of L. This is a direct application of a classical theorem, with no originality claim. For direct products, n and L both multiply: the maximum p-valuation among product degrees is the sum of the maxima in the two factors. In particular, every direct power of A5 satisfies c=1, since its degrees are 1,3,3,4,5 and L=60. A5^k therefore presents no radical-recognition obstruction even though complete isomorphism recognition is a stronger question.

The criterion is not universal for radical-free source groups. A7 has degrees

\[
 1,6,10,10,14,14,15,21,35,
\]

with n=2520, L=210, c=12. Direct powers A7^k have c=12^k. These statements are reproduced by exact hook-length and product-convolution arithmetic in the accompanying script.

## 2. The exact Clifford packet behind a minimal normal V

Suppose V is elementary abelian of order p^a. Put Q=H/V and q=|Q|=n/p^a. Let O run through the H-orbits on Irr(V), and write t_O=|O|. Choose λ in O and put I=I_H(λ).

The irreducible characters above O are exactly the inductions from Irr(I|λ). Because λ is linear, their degrees have the form

\[
 \{t_O e_{O,j}:j\in J_O\}.
\]

The numbers e_{O,j} are the degrees of the irreducible projective representations of I/V for the *one common Clifford factor set* associated with λ (or its inverse, according to convention). In particular

\[
 \sum_{j\in J_O} e_{O,j}^2=|I:V|=q/t_O,
 \qquad
 \sum_{\chi\text{ above }O}\chi(1)^2=q t_O.
\]

The orbit masses sum correctly because \(\sum_O t_O=|V|\). The principal orbit has t=1 and trivial factor set, and its degrees are exactly D(Q), including multiplicities. These are exact identities, not estimates. The mass identity also follows directly from Frobenius reciprocity: Ind_V^I λ has degree |I:V| and decomposes as \(\sum_\theta\theta(1)\theta\), since \(\theta|_V=\theta(1)\lambda\).

Thus any candidate radical gives all the following necessary data:

1. An integer p^a dividing c, not merely n.
2. An irreducible F_p action of H on V. Its image B=H/C_H(V) is a subgroup of GL_a(p), is a quotient of H, and has order dividing both n and |GL_a(p)|. The action need not be faithful as an action of Q: its kernel is C_H(V)/V.
3. A partition of D into the above orbit packets, with all degrees in a packet divisible by t_O, square mass q t_O, and \(\sum_Ot_O=p^a\).
4. For each packet, a genuine twisted group algebra of the actual inertia factor I/V. Matching the numerical square sums alone does not construct this algebra or the group extension.

No subgroup-stabilizer order, orbit decomposition, projective factor set, or particular quotient-character subset is singled out by the degree multiset. Treating an arbitrary mass-compatible subset as D(Q) would silently add the main missing information.

## 3. Central prime-order constraints

Let Z≤Z(H) have order p. For λ in Irr(Z), let D_λ be the multiset of degrees of Irr(H|λ). Then

\[
 \sum_{d\in D_\lambda}d^2=n/p.\tag{1}
\]

Indeed Ind_Z^H λ decomposes with multiplicity χ(1) over these characters. Galois automorphisms of a splitting cyclotomic field act transitively on nontrivial λ and preserve χ(1). Therefore all nontrivial D_λ have one common degree multiset, say b(d), while the principal sector has a(d), and

\[
 m(d)=a(d)+(p-1)b(d),\qquad
 \sum_d a(d)d^2=\sum_d b(d)d^2=n/p.\tag{2}
\]

**Lemma 3.** If g=1, then every central subgroup of prime order lies in H′.

**Proof.** If Z is not contained in H′, some linear character θ is nontrivial on Z. Tensoring by powers of θ gives degree-preserving bijections between all p central-character sectors, including the principal sector. Hence every m(d) is divisible by p, contradicting g=1. ∎

**Lemma 4.** If Z≤H′ has order p, every character in a nontrivial central sector has degree divisible by p.

**Proof.** In an irreducible representation of degree d, z∈Z acts as ζI by Schur's lemma. Its determinant is a linear character of H, hence kills H′. For ζ a nontrivial pth root, 1=ζ^d implies p|d. ∎

Write \(S_p(D)=\sum_{p\nmid d}m(d)d^2\). If g=1 and H has a central subgroup of order p, these lemmas and (1) imply

\[
 S_p(D)\le n/p.\tag{3}
\]

They also imply p^3 divides n, since the right side of (1) is a sum of squares of multiples of p. A refinement of (3), using the Galois multiplicity in (2), is

\[
 \sum_{p\mid d}\left\lfloor\frac{m(d)}{p-1}\right\rfloor d^2\ \ge n/p.\tag{4}
\]

Failure of any one of these necessary conditions excludes a central p-kernel. Satisfying them does not create a group.

## 4. A rigorous small-action criterion

Suppose m(1)=1, so H is perfect. For each p^a dividing c, the image of a hypothetical elementary abelian minimal normal subgroup V of order p^a is a perfect subgroup of GL_a(p). If GL_a(p) is solvable, this image is trivial. Minimality then forces V central of order p. This proves the following usable criterion.

**Proposition 5.** Suppose m(1)=1. For every p dividing c, assume that GL_a(p) is solvable for all 1≤a≤v_p(c), and that at least one of (3), p^3|n, or (4) fails. Then every H with degree multiset D has R(H)=1.

The solvable-linear-group hypothesis holds when v_2(c)≤2, v_3(c)≤2, and v_p(c)≤1 for every p≥5: GL_1(p) is abelian, GL_2(2)≅S3, and GL_2(3) is a central extension of S4 and hence solvable. These sufficient bounds do not describe all solvable GL_a(p).

For A7, c=12, so only dimensions a≤2 in characteristic 2 and a≤1 in characteristic 3 can arise. Both image groups are solvable. The exact masses are

\[
 S_2=1+15^2+21^2+35^2=1892>1260,
\]
\[
 S_3=1+2\cdot10^2+2\cdot14^2+35^2=1818>840.
\]

Thus these elementary constraints exclude a radical for the A7 multiset. This is an illustration of the mechanism, not a new recognition result: full recognition of simple groups by complex group algebras is already known.

## 5. A checkable obstruction to promoting the numerical route

The central constraints are not a universal contradiction even on radical-free source groups. For A7^3, the exact arithmetic script constructs a partition of the entire degree multiset into two packets of equal square mass

\[
 |A7|^3/2=8{,}001{,}504{,}000.
\]

All odd-degree characters belong to the principal packet, all degrees in the other packet are even, the principal packet has exactly one linear character, each packet degree divides |A7|^3/2, and no multiplicity exceeds its available multiplicity. Thus this artificial partition passes (1)–(4), the determinant condition, and the degree divisibility constraint for a central C2. The two explicit integer multiplicity lists are in character_constraints_results.json. A second independent arithmetic checker is supplied separately.

**This is not a group, not a constructed central extension, and not a counterexample to 21.135.** The principal packet has not been proved to be the degree multiset of any group; the nonprincipal packet has not been proved to arise from a common projective factor set. It demonstrates precisely why degree divisibility, central-character square masses, and Galois congruences do not themselves finish the argument. These constraints leave apparently compatible arithmetic data already on a small direct power of a simple group.

## 6. Realizing the artificial packet as one central unit still does not construct a group basis

The numerical A7^3 packet has a concrete algebra interpretation. In the Wedderburn algebra A=C[A7^3], put z=+I on every principal-packet block and z=−I on every other block. Then z is a nontrivial central involution. For the regular left-multiplication trace,

\[
 \operatorname{Tr}_{\mathrm{reg}}(z)
 =\sum_d a(d)d^2-\sum_d b(d)d^2=0.
\]

All negative blocks have even dimension, so z has determinant 1 in every matrix block. It is even a single commutator of finite-order units. In each negative block of dimension 2r, use r copies of

\[
 J=\begin{pmatrix}0&1\\-1&0\end{pmatrix},\qquad
 D=\begin{pmatrix}1&0\\0&-1\end{pmatrix},\qquad [J,D]=-I_2,
\]

and use identity matrices in each positive block. The resulting global units u,v satisfy u^4=v^2=1 and [u,v]=z. Their finite subgroup is a copy of D8. These units are not asserted to be elements of a group basis: for example \(\operatorname{Tr}_{\rm reg}(u)=n/2\), while any nonidentity group-basis element would have regular trace zero.

Adjoining z to the original group G=A7^3 cannot solve the problem. Since Z(G)=1, z is not in G, so the generated subgroup of A× is G×C2, of order 2n. It acts on A through a quotient of C[G×C2], rather than giving a group basis of A. Moreover it has only one subgroup of index 2: every homomorphism G×C2→C2 kills the perfect group G, leaving the subgroup G. Thus taking an index-2 subgroup after adjoining z also produces no new group basis.

For clarity, a finite subgroup K≤A× of order n would give a group basis if its nonidentity elements all had regular trace zero. Indeed a putative linear relation among elements of K can be multiplied by each k^{-1} and traced; all coefficients must vanish. The artificial z supplies one admissible-looking element, but no finite subgroup of order n with this property. The missing condition is a genuine global multiplication law with the trace/independence property, not merely construction of central units or isolated commutators.

## 7. Failed reductions and exact remaining gap

- Deleting the characters of H/V does not give a canonically identified subset on the G side. Induction on |G| therefore cannot be invoked merely because the remaining multiset has the right order.
- Quotienting by R(H) provides a radical-free group H/R(H), but its degree multiset is only an unidentified submultiset of D, of lower order. The original problem supplies no radical-free group of that lower order with that multiset.
- The action on V yields only a quotient image B. Replacing the full inertia factor I/V by its action quotient B_λ omits C_H(V)/V and the projective obstruction; it is unjustified when the kernel is nontrivial.
- For split affine examples V⋊B the relevant λ extends and the packet is t_O times the ordinary degrees of B_λ. This special simplification cannot be imposed on an arbitrary extension H.
- Extending the c=1 proof to all radical-free sources would require a false premise: A7 itself has c=12, and c grows multiplicatively under powers.

The remaining structural task is to use the radical-free source's full degree pattern to rule out every actual elementary abelian Clifford configuration, not just its numerical relaxation, or to construct a genuine equal-multiset pair realizing one. No mechanism accomplishing either task has been found here. All target claims remain hypotheses. There is no complete solution and no publication claim.

## Primary source

Noboru Itô, “On the degrees of irreducible representations of a finite group,” Nagoya Mathematical Journal **3** (1951), 5–6, DOI [10.1017/S0027763000012162](https://doi.org/10.1017/S0027763000012162). The original theorem and its proof were read in the publisher's two-page primary PDF. The paper states the maximal-abelian-normal-subgroup version; every abelian normal subgroup is contained in one, which gives the stated version by divisibility of indices. All additional deductions here are elementary consequences, without an originality claim. The Hook-length formula and the standard restriction of Sn irreducibles to An are explicit assumptions of the arithmetic generator and can be bypassed by supplying the displayed A7 degree list directly.
