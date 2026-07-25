# Research log: all-vertical top obstruction

All times are UTC.

## 2026-07-25T07:05:00Z — valuation route opened

- Kept the first-integral descent
  \(G^4/P^3=R(q/p)\), but compared two primes in the same vertical fibre
  rather than evaluating one horizontal prime.
- Found the exact same-fibre congruence
  \[
  4(v_{f_1}G-v_{f_2}G)=3(v_{f_1}P-v_{f_2}P).
  \]
- In the genuine \(h=\ell^2,p=\ell m\) shape this gives \(4N=6\).
- In the split \(h=\ell_1\ell_2\) shape it gives \(4N=3\) unless each
  residual line repeats its corresponding factor of \(h\).

## 2026-07-25T07:09:00Z — split shape closed

- Coprimality rules out crossing \(m_1=\ell_2\) or
  \(m_2=\ell_1\).
- Avoiding both congruence obstructions forces
  \(p=\ell_1^2,q=\ell_2^2\).
- This is a quadratic composition of the linear pencil
  \(\langle\ell_1,\ell_2\rangle\), contradicting minimality.
- Recorded the nonminimal exact counterexample
  \(h=yz,p=y^2,q=z^2\), whose cubic top kernel has dimension four.

## 2026-07-25T07:12:00Z — p=h shape classified

- Factored the top derivation as
  \[
  \operatorname{Jac}(h^2,hq,G)
  =2h^2\operatorname{Jac}(h,q,G).
  \]
- A parity comparison in the divisor descent shows that a nonzero cubic
  first integral requires a double-line member of the quadratic pencil.
- Minimality makes that double member unique.
- Reduced every minimal quadratic pencil with a double member to exactly
  \(\langle x^2,yz\rangle\) or
  \(\langle x^2,y^2+xz\rangle\).
- Computed the complete cubic kernels
  \(\langle x^3,xyz\rangle\) and
  \(\langle x^3,x(y^2+xz)\rangle\).

## 2026-07-25T07:15:00Z — exact witness tests complete

- Verified zero cubic kernels on two square-shape samples, a split sample,
  and a no-double \(p=h\) sample.
- Verified two-dimensional kernels on both canonical double-line pencils
  and on an irreducible \(p=h\) sample whose other member is a double
  line.
- Verified generic conic smoothness for every sample used to claim
  minimality.
- Added a standalone exact SymPy verifier and recorded the remaining
  top-identity frontier.
- Did not edit global documents and did not commit.

## 2026-07-25T08:05:00Z — hostile audit passed

- An independent audit reconstructed the same-fibre valuation equality,
  divisor parity, uniqueness and exhaustive pencil normal forms, both
  cubic kernels, and the scope of the quadratic-component exit.
- Exact PARI/\(\mathbb Q\), dependency-free modulo-\(101\), and injected
  fault tests pass.
- Characteristics \(5\) and \(11\) were discarded after producing
  spurious modular kernels; they are not counted as verification.
- Verdict: PASS.  The theorem is ready for global promotion.
