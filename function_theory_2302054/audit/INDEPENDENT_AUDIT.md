# Independent audit of Rubel Problem 2.54

**Verdict: PASS.** The counterexample in Sakari Toppila's 1983 Theorem 2 gives a known negative answer to the exact question. The detailed verification in the five reviewed artifacts is mathematically sound. In particular, the asserted product lower bound and the 32-step Harnack argument are valid. No new-resolution claim is warranted.

Audit date: 2026-10-03. This is an independent mathematical review, not a formal proof-assistant certification or a claim of journal peer review.

## 1. Question and primary-source match

The question asks whether a closed subset of the complex plane with two separately available transcendental entire witnesses must have one transcendental entire witness satisfying both properties: uniform boundedness on the set and a uniform positive lower bound for the modulus on its complement. The quantifiers allow the two premise witnesses and their constants to differ. They impose no growth-order or normalization condition.

Both pages of [Toppila, *Solutions of problems of Miller and Rubel*, Ann. Acad. Sci. Fenn. Ser. A I Math. 8 (1983), 369–370](https://www.acadsci.fi/mathematica/Vol08/vol08pp369-370.pdf) were inspected, including the printed formulas. Page 369 explicitly attributes Problem A to Rubel and identifies it as Problem 2.54 of Anderson, Barth and Brannan's 1977 collection. Its formulation matches the question above. Theorem 2 states the negative result; section 3 on page 370 supplies the two functions and proves that every simultaneous entire witness is constant. The DOI printed on page 369 is [10.5186/aasfm.1983.0826](https://doi.org/10.5186/aasfm.1983.0826).

The displayed Problem 2.54 on printed page 43 of the [2018 Hayman–Lingham edition](https://arxiv.org/abs/1809.07200v2) was also visually checked. It matches the formulation in Toppila. The 1977 collection itself was not inspected in full. The exact-source identification is supported by Toppila's explicit reproduction and citation, independently corroborated by the later edition.

The original paper abbreviates the product estimate and invokes repeated Schottky estimates for the last step. The reviewed proof expands the former and uses a separately checked Harnack argument for the latter. Its validity does not depend on accepting an unproved uniformity assertion from the original abbreviation.

## 2. The set and first witness

Write \(q=e^4\), \(t=e^2=\sqrt q>4\), and
\[
E=[0,\infty)\cup\bigcup_{k\ge1}\overline D(q^k,1).
\]
The disk centers escape every compact set. Thus the closed disks form a locally finite family, their union is closed, and adjoining the closed ray preserves closedness. Every disk has real part at least \(q^k-1>0\). It follows that \(f(z)=e^{-z}\) is bounded by 1 on all of \(E\); it is transcendental entire.

Including 0 in the ray is appropriate for the closed-set hypothesis. It creates no change to either witness estimate or to the rigidity proof. No ambiguous convention about an open positive ray is needed.

## 3. Infinite product and uniform lower bound

For each finite \(R\), \(\sum_{k\ge1}Rq^{-k}<\infty\). The infinite product
\[
g(z)=\prod_{k\ge1}(1-z/q^k)
\]
therefore converges locally uniformly to an entire function. Its value at 0 is 1 and it vanishes at each of the infinitely many distinct points \(q^k\). This proves transcendence without assuming any unstated growth property.

Define
\[
c=1-t^{-1}>3/4,
\qquad C=1-\frac{t}{t^2-1}>1/2.
\]
The last inequality follows from \(t^2-2t-1>0\), valid for \(t>4\). For the tail comparison,
\[
\sum_{j\ge1}q^{1/2-j}=\frac{t}{q-1},
\qquad
\prod_{j\ge1}(1-q^{1/2-j})\ge1-\frac{t}{q-1}=C.
\]
Indeed, all the factors lie in \((0,1)\), the finite-product inequality \(\prod(1-x_j)\ge1-\sum x_j\) applies, and the finite products converge monotonically to a limit at least \(C\). This supplies an actual positive lower bound for the tail, not merely convergence of that tail.

Take any \(z\) outside all the open unit disks and put \(r=|z|\). This is a stronger domain than the required \(\mathbb C\setminus E\). When \(r\le t\), every factor has modulus at least \(1-q^{1/2-k}\), so \(|g(z)|\ge C>q^{-2}\).

Otherwise choose \(n\ge1\) with \(q^{n-1/2}\le r\le q^{n+1/2}\). For \(k<n\), the ratio \(q^k/r\le q^{-1/2}\), and the reverse triangle inequality gives
\[
|1-z/q^k|\ge c r/q^k.
\]
The excluded open disk gives \(|1-z/q^n|\ge q^{-n}\), including equality on a disk boundary. For \(k=n+j>n\), \(r/q^k\le q^{1/2-j}\), so the whole tail is bounded below by \(C\). Taking limits of the finite-product inequalities yields
\[
|g(z)|\ge Cc^{n-1}r^{n-1}q^{-n(n-1)/2-n}
\ge Cc^{n-1}q^{(n^2-4n+1)/2}.
\]
The substitution of the lower bound for \(r\) has the correct direction because \(n-1\ge0\). The exponent was independently expanded as a polynomial identity.

For \(A_n=c^{n-1}q^{(n^2-4n+1)/2}\),
\[
\frac{A_{n+1}}{A_n}=cq^{n-3/2}.
\]
The ratio for \(n=1\) is \(c/t<1\), while all the ratios for \(n\ge2\) are at least \(ct=t-1>3\). Consequently the minimum over all positive integers is exactly \(A_2=cq^{-3/2}\). Thus
\[
|g(z)|\ge Cc q^{-3/2}
>\frac12\frac34\,tq^{-2}
>\frac32q^{-2}>q^{-2}=e^{-8}.
\]
The uniform lower bound is correct on the entire required complement. Endpoints of the radial bands, the first band \(n=1\), unit-circle boundaries around the zeros, arbitrarily large \(n\), and the small-radius case all satisfy the argument. No finite sampling is used to justify its global character.

## 4. The annular rigidity argument

Suppose an entire \(h\) satisfies \(|h|\le M\) on \(E\) and \(|h|\ge m>0\) on its complement. For \(k\ge1\), let
\[
r_k=e^{4k+2},\qquad A_k=\{r_k/e<|z|<er_k\}.
\]
For every disk with index at most \(k\), its greatest modulus is at most \(e^{4k}+1<e^{4k+1}\). For every disk with index at least \(k+1\), its least modulus is at least \(e^{4k+4}-1>e^{4k+3}\). Both inequalities are strict already when \(k=1\), using \(e>2\). Hence \(A_k\) meets \(E\) only on the positive real ray.

Every point of that ray in \(A_k\) is a limit of points in \(A_k\setminus E\). Continuity extends the lower bound to the whole annulus. In particular, \(M\ge m>0\), so the logarithms in the proof are well-defined. The function
\[
u_k(z)=\log(|h(z)|/m)
\]
is nonnegative and harmonic on \(A_k\). Zero-freeness suffices: harmonicity of the log modulus is local and does not require a single-valued holomorphic logarithm on the multiply connected annulus.

For \(z=r_ke^{i\theta}\), choose \(0\le\theta<2\pi\) and \(z_j=r_ke^{ij\theta/32}\). Each disk of radius \(r_k/2\) centered at a \(z_j\), including its closure, lies inside \(A_k\), because its moduli lie between \(r_k/2\) and \(3r_k/2\), and
\[
r_k/e<r_k/2<3r_k/2<er_k.
\]
For \(j=1,\ldots,32\),
\[
|z_j-z_{j-1}|\le r_k\theta/32<\pi r_k/16<r_k/4.
\]
Harnack's disk bound applied in the disk centered at \(z_{j-1}\) therefore gives
\[
u_k(z_j)\le\frac{(r_k/2)+(r_k/4)}{(r_k/2)-(r_k/4)}u_k(z_{j-1})
=3u_k(z_{j-1}).
\]
For a merely nonnegative harmonic function the same conclusion follows by applying the positive version to \(u_k+\varepsilon\) and sending \(\varepsilon\) to zero. This also handles the boundary case \(M=m\).

There are exactly 32 comparisons; their number, relative disk radii and factors are independent of \(k\). Since \(r_k\in E\),
\[
u_k(z)\le3^{32}\log(M/m),
\qquad
|h(z)|\le m(M/m)^{3^{32}}=:K
\quad (|z|=r_k).
\]
The finite number \(K\) is the same on every comparison circle. For each point of the plane, one of these circles encloses it. Applying the maximum-modulus principle inside that circle yields the global bound \(|h|\le K\). Liouville's theorem then makes \(h\) constant.

The complement is nonempty, so the zero constant violates the positive-lower-bound premise. Nonzero constants are possible, but none is transcendental. Thus the argument proves exactly the obstruction needed for a negative answer.

## 5. Executable verification and artifact integrity

The verifier was inspected and executed. It exits successfully, reports 17 passing checks, and reproduces `verification.json` byte-for-byte. Its exact rational calculations agree with the proof. In particular, \(3^{32}=1853020188851841\).

The executable is supplementary. Several of its checks encode only a conservative endpoint or a simple equality; the general monotonicity, convergence, harmonicity and maximum-principle arguments still require the written proof. Its quadratic identities are checked at enough distinct points given their evident degree bounds, but the independent audit also expanded those identities directly. The verifier is not a mechanical certificate for the entire complex-analysis theorem, and the artifacts correctly disclose that limitation.

The reviewed SHA-256 digests are:

- `artifacts/PROOF.md`: `7a9fe164116f58b466df93649e9b25820bedd56265e4747e408f78b4a5798725`
- `artifacts/README.md`: `1c811692f0a54fd7f8946a8ec28b71708a6f95ddd1bbd10faca1eee244000674`
- `artifacts/SOURCES.md`: `af1789d32e5344037ef94868054d7259e6184eaedc243949c1e9334779d42a16`
- `artifacts/verification.json`: `5fa3fc16cb9a40837e59c0262c9f7862482d4b2ac50c08944a832e201ca1bf72`
- `artifacts/verify.py`: `7ab1c1b56698310b55317be0f76c912db703c214ea8780b5a8acc0de200651dd`

## 6. Qualifications and final disposition

- **Mathematical defects found:** none. The exact construction, both transcendental witnesses, uniform lower bound, annular geometry, 32-step estimate and global constancy conclusion pass.
- **Classification:** already solved negatively by Toppila in 1983. The added exposition is a verification of that result, with no mathematical novelty or priority claim.
- **Historical wording:** the 2018 update literally says that no progress was reported to its authors. Such a reporting statement can coexist with an earlier published theorem. It should be described as failing to reflect this resolution; its existence does not establish a logical contradiction or the authors' awareness. This is a nonblocking qualification to the README's word “inconsistent.”
- **Source-access limit:** the exact original question was checked through its explicit reproduction in Toppila and the matching 2018 statement. No claim is made here to have independently inspected every page of the 1977 collection, every later citation, or an exhaustive correction history.
- **Scope of this verdict:** it certifies the mathematical conclusion and the stated artifact contents at the recorded hashes. It does not certify an administrative attempt count or a complete historical literature census.

**Final result: PASS, with the source-access and historical-wording qualifications above.**
