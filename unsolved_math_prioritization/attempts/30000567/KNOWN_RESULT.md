# Every separable infinite-dimensional Banach space supports disjoint-hypercyclic tuples

**Status:** Credited known resolution; separate source/proof review is pending. Recommend `already_solved`, with zero new proof attempts. This package checks existing results and their elementary transport argument; it makes no discovery claim.

## 1. Exact original target

Juan Bès's contribution, *Disjointness in Hypercyclicity*, in Oberwolfach Report 37/2006, pp. 2235–2238, defines a tuple \(T_1,\ldots,T_m\) to be disjointly hypercyclic when **one vector** \(x\in X\) has a co-orbit
\[
 \{(T_1^n x,\ldots,T_m^n x):n\ge0\}
\]
dense in the full product \(X^m\). Problem 10, printed p. 2238, asks whether every separable infinite-dimensional Banach space supports a pair or more such operators. The definitions and exact problem page were visually checked in the [complete original report](https://ems.press/content/serial-article-files/46067).

The target is existence of a simultaneous dense co-orbit with the **same iterate n and same starting vector** in all coordinates. It does not add commutativity, separability of the dual, or density of the set of all such starting vectors. Nearby statements concerning disjoint transitivity, disjoint mixing, or hypercyclic subspaces must not be appended to Problem 10.

## 2. Existing theorem answers the question

Stanislav Shkarin, *A short proof of existence of disjoint hypercyclic operators*, **Theorem D**, states the following stronger result:

For every separable infinite-dimensional Fréchet space \(X\) over either \(\mathbb R\) or \(\mathbb C\), and every prescribed finite \(m\ge1\), there are continuous linear operators \(R_1,\ldots,R_m\) on \(X\) and a vector \(x\) whose simultaneous co-orbit is dense in \(X^m\).

The complete [primary manuscript](https://arxiv.org/abs/1209.1212) was read, including Theorem D, Proposition 1.3 and Lemmas 2.1–2.2 with their proof. Its arXiv deposit is dated 6 September 2012, but the journal publication is **2010**: *Journal of Mathematical Analysis and Applications* 367(2), 713–715, DOI [10.1016/j.jmaa.2010.01.005](https://doi.org/10.1016/j.jmaa.2010.01.005). The arXiv journal reference and publisher-deposited Crossref metadata agree. The full final publisher-typeset text was not recovered; the complete author manuscript supplies the mathematical statement and argument audited here.

Shkarin explicitly credits earlier constructions to Bès–Martin–Peris and to Salas, and presents a shorter reduction. Accordingly this package does not assign the original existence discovery to this campaign, or claim that Shkarin was the first discoverer. Every Banach space in the original question is a Fréchet space, and continuous linear operators on it are bounded. Taking any finite \(m\ge2\) therefore answers the full original question affirmatively.

## 3. The known short argument, with its dependency explicit

### The input is stronger than mere hypercyclicity

The existing input is Shkarin's Proposition 1.3: on each separable infinite-dimensional Fréchet space there is an operator \(T\) for which
\[
 T^{\oplus m}=T\oplus\cdots\oplus T
\]
is hypercyclic for every finite \(m\). The proposition is credited there to the constructions and observations of Bonet–Peris, Grivaux, and Bès–Peris. It is **not** inferred from existence of an arbitrary hypercyclic operator.

For the Banach setting, the mixing-operator existence used in this input is also explicitly stated in Grivaux, *Hypercyclic operators, mixing operators, and the Bounded Steps Problem*, Theorem 2.6, printed pp. 152–153. The [complete published paper](https://jot.theta.ro/jot/archive/2005-054-001/2005-054-001-010.pdf) and the relevant proof were inspected. Finite products of a mixing operator are mixing: for finitely many product-open source and target sets, take the maximum of their finitely many mixing thresholds. On a separable complete metric space, the usual Baire argument then yields a dense orbit. We use this established existence input with attribution rather than claiming to reconstruct the underlying biorthogonal-system construction from first principles. Shkarin's statement expressly covers both scalar fields.

### Bounded invertible maps can identify the coordinates

Let \(u,v\) be nonzero vectors in a Banach space. If \(v=\lambda u\), \(\lambda\ne0\), use \(S=\lambda I\). Otherwise Hahn–Banach gives bounded linear functionals \(f,g\) with
\[
 f(u)=1,\quad f(v)=0,\qquad g(u)=0,\quad g(v)=1.
\]
Set
\[
 Sz=z+(g(z)-f(z))u+(f(z)-g(z))v.
\tag{1}
\]
Then \(Su=v\), \(Sv=u\), and \(S\) fixes \(\ker f\cap\ker g\). Equivalently, if \(N=S-I=(u-v)\otimes(g-f)\), then \(N^2=-2N\), so \(S^2=I\). Thus \(S\) and \(S^{-1}\) are bounded. This is Shkarin's Lemma 2.2, with the involution check made explicit. It uses no basis or complemented infinite-dimensional subspace of \(X\).

### Transport the dense product orbit to a diagonal starting point

Fix \(m\ge2\). By the stated input choose \(T\) and a hypercyclic vector \((u_1,\ldots,u_m)\) for \(T^{\oplus m}\). Each \(u_i\ne0\), since projecting the dense product orbit to coordinate i gives a dense orbit in \(X\). Fix any nonzero \(x\in X\). Choose bounded invertible \(S_i\) with \(S_i u_i=x\), and define
\[
 R_i=S_iTS_i^{-1}.
\]
Then, for every nonnegative integer \(n\),
\[
 (R_1^n x,\ldots,R_m^n x)
 =(S_1T^n u_1,\ldots,S_mT^n u_m).
\tag{2}
\]
The product map \(S_1\oplus\cdots\oplus S_m\) is a homeomorphism of \(X^m\), so the right side of (2) has dense range as \(n\) varies. This proves disjoint hypercyclicity with one common vector and one common time index, exactly as required. Each \(R_i\) is bounded and individually hypercyclic by projection. No commutation between different \(S_i\) or \(R_i\) has been assumed. This is Shkarin's Lemma 2.1 and proof of Theorem D.

The proof treats every prescribed **finite** family size. The original use of “or more” occurs in the finite-tuple framework of Definition 1; no assertion about an uncountable family is needed. Separability of \(X'\) belongs to the separate dual-hypercyclic Theorem S and is not a hypothesis of Theorem D.

## 4. Status correction and verification limits

The pinned dataset's August 2026 triage labels the original existence question open, but the complete primary theorem and its proof above supply a known affirmative answer dating to at least the 2010 publication. This is an `already_solved` source correction, not a new research result.

The finite exact checker tests the bounded-map algebra, inverse identities, similarity powers, and common-vector orbit equality in finite-dimensional rational models. Such models are **not hypercyclic witnesses**. Density in the infinite-dimensional space comes from the credited existence theorem and the topological transport argument. The checker cannot establish that theorem by finite computation.

The package does not claim disjoint transitivity, disjoint mixing, a dense set or closed subspace of disjoint-hypercyclic starting vectors, dual hypercyclicity without its extra hypothesis, or a commuting construction. These are separate properties. No uncertainty about those stronger questions affects the exact existential answer to Problem 10.

## References

- Juan Bès, joint work with Alfredo Peris, *Disjointness in Hypercyclicity*, OWR 37/2006, pp. 2235–2238, Definition 1 and Problem 10. [Original report](https://ems.press/content/serial-article-files/46067), DOI [10.4171/OWR/2006/37](https://doi.org/10.4171/OWR/2006/37). Workshop August 2006; report published June 2007.
- Stanislav Shkarin, *A short proof of existence of disjoint hypercyclic operators*, J. Math. Anal. Appl. 367 (2010), 713–715. [Full author manuscript](https://arxiv.org/abs/1209.1212v1), [DOI](https://doi.org/10.1016/j.jmaa.2010.01.005). Theorem D, Proposition 1.3, Lemmas 2.1–2.2.
- Sophie Grivaux, *Hypercyclic operators, mixing operators, and the Bounded Steps Problem*, J. Operator Theory 54 (2005), 147–168. [Published full text](https://jot.theta.ro/jot/archive/2005-054-001/2005-054-001-010.pdf), Theorem 2.6 and its proof.
- Earlier existence constructions are credited in Shkarin's introduction to J. Bès, Ö. Martin and A. Peris, *Disjoint hypercyclic linear fractional composition operators* (then a 2009 preprint; subsequently JMAA 381 (2011), 843–856), and H. N. Salas, *Dual disjoint hypercyclic operators* (then a 2009 preprint; subsequently JMAA 374 (2011), 106–117). Their complete proofs were not independently reconstructed in this source audit.
