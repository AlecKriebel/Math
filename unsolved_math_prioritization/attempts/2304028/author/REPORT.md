# Acceptance report: nonreal zeros of a polynomial square plus its derivative

Problem identifier: 2304028 / AMR-022-4028. Reviewed 2026-10-08.

## Disposition

**KNOWN-SOLVED.** The general lower bound is an established theorem, including a stronger distinct-root conclusion. This is a literature-status correction and a checked application of existing mathematics, not a new solution. There is no remaining mathematical gap for the specified polynomial problem. No new proof-search approaches were spent: the prior-solution stopping condition was met first.

The [Hayman–Lingham source, Update 4.28](https://arxiv.org/html/1809.07200) explicitly credits Sheil-Small with solving the problem and identifies Eremenko's alternative argument. Thus a status summary retaining only the real-rooted special case is incomplete. The source's current arXiv version is v2, dated 21 September 2018.

## Domain and multiplicity contract

Let P belong to R[z], let d = deg P >= 2, and write Q = P^2 + P'. Zeros are considered in C. No monicity, leading-coefficient sign, squarefreeness, or real-rootedness assumption is imposed. Complex coefficients are outside the audited theorem. The leading term of Q has degree 2d, since P' has degree d-1.

The imported conclusion supplies at least d-1 **distinct** points in C minus R where Q vanishes and P does not vanish. It therefore implies the lower bound whether the original root count is interpreted with or without multiplicities. Arbitrary repeated roots of P are allowed.

At a root a of P of multiplicity m, write P(z)=(z-a)^m u(z), u(a) != 0. Direct expansion gives

Q(z)=(z-a)^(m-1) [m u(z)+(z-a)u'(z)+(z-a)^(m+1)u(z)^2].

The bracket has nonzero value m u(a). Consequently Q has multiplicity exactly m-1 there. The imported lower bound deliberately does not use these shared roots, so they cannot conceal a multiplicity-counting shortfall.

## Primary-source chain and application

1. Terence Sheil-Small, [On the zeros of the derivatives of real entire functions and Wiman's conjecture](https://annals.math.princeton.edu/1989/129-1/p07), Annals of Mathematics 129 (1989), 179–193, DOI 10.2307/1971490. The publisher record verifies bibliographic identity. Its full original proof was not retrieved for this audit.
2. Walter Bergweiler, Alex Eremenko and Jim K. Langley, [Zeros of differential polynomials in real meromorphic functions](https://doi.org/10.1017/S0013091504000690), Proceedings of the Edinburgh Mathematical Society 48 (2005), 279–293. The published PDF was inspected: Theorem A, p.279, states the stronger polynomial result; Lemma 2.1 and the proof of Corollary 1.1, pp.282–283, give the alternative dynamical argument.
3. The [author-hosted 2004 manuscript](https://www.maths.nottingham.ac.uk/plp/pmzjkl/PAPERS/realz-edin.pdf) agrees on the polynomial statement. Its numbering differs: Lemma 10 and Corollary 1. The journal version, rather than manuscript numbering, governs this report.

Applying Theorem A with f=P immediately proves the target. Since d>=2 the bound is positive, and conjugation supplies a nonreal pair. The real-rooted special case is historically credited in the journal article to Prüfer, via Pólya and Szegő's collection; no claim of a new attribution is made here.

### Checked argument with an explicit imported dependency

This is an authored short exposition of the existing dynamical proof, not an independent discovery. Import the rational-map case of the Fatou/Leau-domain lemma cited above: a parabolic fixed point of multiplicity mu supplies mu-1 disjoint invariant domains, with equally spaced limiting approach directions, each containing a critical value.

Set F(z)=z-1/P(z). The calculation below makes infinity parabolic of multiplicity d+2. Of the d+1 directions, at most two are real. A domain with a nonreal direction cannot contain a real critical value: its forward orbit would stay real, contradicting its limiting direction. Choosing one critical value in each remaining domain gives distinct nonreal critical values and hence distinct nonreal critical points. None is a pole, because poles map to infinity; infinity is itself fixed. At each selected point, F'=Q/P^2=0. This yields at least d-1 distinct nonreal zeros of Q outside P's zeros. The Fatou lemma is imported, not proved or computationally certified here.

### Local algebra audit

There is no cancellation in F=(zP-1)/P: a common divisor of numerator and denominator divides 1. Thus F is a rational map of degree d+1 >= 3. Put w=1/z and A(w)=w^d P(1/w), so A(0) is the nonzero leading coefficient of P. The inverse-coordinate map is exactly

G(w)=1/F(1/w)=w A(w)/(A(w)-w^(d+1)),

G(w)-w=w^(d+2)/(A(w)-w^(d+1)).

The denominator is nonzero at zero, proving fixed-point multiplicity d+2 without a numerical asymptotic estimate. Infinity has local degree one and is not a critical point. Finite critical points whose value is finite avoid every root of P. These checks eliminate the pole/critical-point ambiguity in converting the dynamical count back to zeros of Q.

## Exact sharpness and boundary checks

Conjugation makes the distinct nonreal count even. Hence the established lower bound implies at least 2 floor(d/2) distinct nonreal zeros. This parity-adjusted bound is attained for every d>=2 by P(z)=-z^d:

Q(z)=z^(d-1)(z^(d+1)-d).

The nonzero roots are simple. For odd d, the second factor has exactly two real roots, leaving d-1 nonreal roots. For even d, it has one real root, leaving d nonreal roots. The zero at the origin is real with multiplicity d-1. Thus the minimum is d-1 in odd degrees and d in even degrees, under either nonreal counting convention. This calculation is an elementary consequence audit; no novelty claim is attached.

The degree restriction matters: P=-z gives Q=z^2-1, with no nonreal roots. Replacing polynomials by rational functions is also outside scope: P=1/z^2 gives Q=(1-2z)/z^4, whose only finite zero is real. These examples are not counterexamples to the polynomial theorem.

## Finite computation and acceptance boundary

`cases.json` contains 24 newly authored finite test cases, including 22 nonlinear polynomials, two linear boundary cases, both leading-coefficient signs, and repeated real/nonreal roots. Expectations were generated with SymPy 1.14.0, using rational polynomial arithmetic and squarefree factors. `verify.py` independently recomputes them with Python's standard-library Fraction arithmetic, Euclidean polynomial gcd and Sturm chains. It checks distinct nonreal roots both before and after removing shared roots, real roots with multiplicity, degree, parity, and the inverse-coordinate identity.

The finite tests do not establish the universal theorem. The theorem's acceptance rests on the published result and its inspected proof; the tests check implementation and guard the exact interpretation. There is no floating-point root classification and no numerical tolerance.

The verifier rejects booleans as integers, fractional/float coefficients, nonfinite numbers, duplicate JSON keys, unknown keys, leading-zero encodings and unbounded input sizes. No acceptance check uses Python `assert`. Required isolated mode blocks cwd/PYTHONPATH module injection; the script rejects non-isolated invocation. Actual nonroot execution is required.

Reproduction: run `python -I -B verify.py --manifest FREEZE.json --expected-sha256 EXTERNALLY_RECORDED_DIGEST`, with optional `-O` or `-OO` placed before the script. The manifest lives outside the four-file public payload. Its expected SHA-256 must come from a trusted external record, never from an untrusted payload. An independent caller must first validate the verifier's own bytes; a compromised verifier cannot authenticate itself.

The frozen payload contains only this authored report, verifier, authored test cases and public bibliographic/retrieval metadata. No source PDFs, copied question text, source datasets, private coordination material, or private filesystem paths are included. PDF hashes identify inspected bytes; they do not grant redistribution rights or prove a theorem. Audit receipts separately record optimization-mode, read-only, hostile-directory and mutation-control results against the externally pinned freeze.
