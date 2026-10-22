# Independent acceptance audit: fixed-degree mesh preservation

Problem 2200009 / AMR-021-0009, queue rank 1030. Audit date: 2026-10-08 UTC.

## Decision

**Accept as previously solved, with credit to Jonathan Leake and Nick Ryder.**
The author's operator reduction is correct under its expressly stated convention
that a zero output is permitted. Its additional condition for preservation with
nonzero outputs only is also correct. No mathematical correction to the frozen
report is required.

The appropriate campaign accounting is **0 new mathematical search approaches,
Turns 0/5**. This audit and the normalization diagnostics do not consume a search
approach or establish a new solution. The inherited source/deduplication gate is
bounded historical evidence, not an exhaustive search for all prior work. This
audit did not repeat every campaign duplicate query, change the queue, publish
anything, or evaluate hosted CI.

The accepted dependency is the cited universal convolution theorem. The audit
independently establishes the normalization and boundary reduction; it does not
claim a new, fully independent proof of that universal theorem.

## 1. Exact source match and inspection depth

Shapiro's versioned problem list, Section V, page 3, Conjecture 5, uses finite
constant-real-coefficient backward integer translations, degrees at most m, and
the falling factorial test polynomial. Its following convolution formulation
uses forward differences. This is the target actually reviewed, rather than the
different classification of preservers on polynomials of every degree. [S]

In Leake–Ryder v1, page 2 defines the convolution by the backward b-difference,
divided by b. Theorem 1.4 assumes real-rooted inputs of degree **at most n**, root
mesh at least b, and b>0; it has no positivity-of-coefficients, positivity-of-roots,
equal-degree, or monicity restriction. Setting b=1 gives exactly the convolution
needed here. Page 3 notes the other difference direction. I inspected the proof
on page 13 and the direct-proof discussion on pages 17–19. Page 13 handles equality
at the mesh boundary by approximation; page 19 explicitly extends to smaller
degrees by adding roots tending to infinity. This confirms the theorem's intended
scope. It is a dependency and scope audit, not line-by-line verification of every
auxiliary lemma or the entire paper. [LR]

One harmless normalization typo appears in the direct proof: for
h_(a,t)=a f-(x-t)g, the coefficient limit is h_(a,t)/t -> g, rather than
h_(a,t) -> g. This follows immediately by division by t; the roots are unchanged,
so the root-limit argument is unaffected. The frozen report does not repeat
this typo. [LR]

The publisher's primary record independently confirms the authors, title,
Advances in Mathematics volume 374 (2020), article 107334, and DOI. The mathematical
pin remains arXiv v1; no assertion that journal theorem numbering is identical is
needed. [P]

Brändén–Krasikov–Shapiro v2 assigns mesh zero to a repeated root and infinite mesh
in degrees at most one (page 1). It treats the backward difference as a preserver
(page 2) and allows zero in proper-position conventions (page 5). Its fixed-degree
conjectures are numbered 2 and 3 in this version, on pages 9–10. These facts
support the report's multiplicity and low-degree conventions. They are not an
explicit numerical definition of mesh(0). [BKS]

## 2. Independent algebraic reconstruction

Let V_m=R[x] of degree at most m, E f(x)=f(x-1), D=I-E, and

    F_j(x)=x(x-1)...(x-j+1),
    U_j(x)=x(x+1)...(x+j-1),
    F_0=U_0=1.

Every D reduces a positive degree by one, so D^(m+1)=0 on V_m. Consequently a
finite stencil T=sum a_j E^j has the exact representation

    T=sum_{s=0}^m c_s D^s,
    c_s=(-1)^s sum_{j>=s} binom(j,s) a_j.

This remains valid for stencil length greater than m; the discarded terms are
zero operators, rather than an approximation. The identity D U_j=j U_{j-1}
follows by cancelling the shared factors, including j=1. Because U_j(0)=0 for
j>0, evaluation of D^s U_j at zero is j! for s=j and zero otherwise.

For h=T F_m, put r(x)=h(x+m-1). Translation invariance gives r=T U_m, also for
m=0. Applying D^(m-s) and evaluating at zero therefore gives m! c_s. Thus

    sum_{s=0}^m D^s f(x) D^(m-s) r(0) = m! T f(x).

This is precisely the claimed formula. It holds for every real f in V_m, without
root assumptions. It proves that h determines T on V_m; h=0 forces every c_s=0
and hence T=0 on V_m. No division by a leading coefficient or by h is hidden in
the argument.

For the forward difference N f(x)=f(x+1)-f(x), use N F_j=j F_{j-1}. On V_m,
E=(I+N)^(-1), with the inverse a terminating power series, so T is a polynomial
in N. The same coefficient-extraction argument yields

    T f = C_m^+(f,h)/m!.

If R f(x)=f(-x), D R=-R N gives

    C_m(R f,R g)=(-1)^m R C_m^+(f,g).

All signs, the shift m-1, and the factor m! agree with the report. The two
conventions therefore cannot produce a counterexample to the criterion.

For completeness, expanding f and g in the divided rising-factorial basis
gives an explicitly symmetric expression:

    f=sum alpha_i U_i/i!,  g=sum beta_j U_j/j!,
    C_m(f,g)=sum_{i+j>=m} alpha_i beta_j U_(i+j-m)/(i+j-m)!.

This also verifies the symmetry tested by the scripts, independently of an
appeal to the literature.

## 3. Lower degrees, multiplicities, closure, and the zero operator

For a nonzero polynomial, admissibility means real roots with multiplicities
counted and separation at least one. Thus every root is simple. Constants and
linears are admitted. Let H_m contain these polynomials and also zero.

The relevant closure facts can be checked independently. In a coefficient limit
to a nonzero polynomial of bounded degree, every finite root of the limit is
approached with its multiplicity by roots of the approximants. Nonreal roots
cannot appear from real-rooted approximants. Two roots cannot coalesce or end at
distance less than one when every approximant has separation at least one.
Roots escaping to infinity merely reduce the degree. A zero limit is already
in H_m. Hence H_m is closed in V_m.

Conversely, any nonzero degree-d admissible polynomial can be approximated by
degree-m polynomials with strictly greater mesh. First multiply its real roots
by 1+epsilon. Then append m-d sufficiently distant, mutually separated positive
roots R_j using factors (1-x/R_j). Let epsilon tend to zero and all R_j tend to
infinity. These factors converge coefficientwise to 1, so the polynomial itself,
including its scalar, is recovered. Constants follow the same construction.
Zero is a limit of small nonzero multiples of any fixed strictly separated
degree-m polynomial. This supplies an explicit closure argument for all
degree drops and boundary inputs, even if one starts from the theorem's strict,
full-degree case.

For nonzero inputs of degrees d,e<=m, the convolution vanishes when d+e<m:
every summand then differentiates at least one factor too many times. When
d+e>=m, the index s=m-e uniquely contributes the highest degree d+e-m, with
leading coefficient

    lc(f) lc(g) d! e!/(d+e-m)!.

It is nonzero. This identifies all possible zero outputs without assigning an
unsupported numerical value to mesh(0).

Necessity of the test is immediate because F_m is admissible. For sufficiency,
if h is nonzero, its translate r is admissible and the imported convolution
theorem applies to f and r in V_m. The factor 1/m! leaves roots unchanged. If
h=0, the operator is zero on V_m by the algebra above. For m=0 and m=1 the whole
space is H_m, and the result also follows directly without invoking the theorem.

## 4. Alternative convention requiring nonzero outputs

Write A=sum a_j. Every translation has the same leading term as its input, so
if A!=0 the operator preserves the degree of every nonzero input. Since F_m is
monic, this is equivalent to deg(h)=m. If A=0, T annihilates the admissible
constant 1. Therefore, when every admissible nonzero input must have a nonzero
output, the exact criterion is h admissible **and deg(h)=m**. This includes
m=0.

The examples T=D, D^2 and D^3 on V_2 respectively give test polynomials
2(x-1), 2, and zero. D kills constants even though its degree-two test has a
nonzero admissible image. These are distinctions between conventions, not
counterexamples under the report's stated closed-output convention.

## 5. Integrity and independent computation

Before executing the packet I checked the separately supplied bootstrap,
manifest, report, and archive hashes and byte counts. All eight manifest
payloads matched. The archive has exactly eleven distinct safe relative entries;
each decompressed entry equals its corresponding frozen file or author receipt.
The author freeze was not changed. The author's replay script then independently
completed with exactly the supplied receipt bytes:

- 8,829 finite checks per diagnostic run;
- 9 positive replays across normal, -O and -OO modes;
- 33 integrity cases, producing 99 rejections;
- 37 semantic cases, producing 111 rejections;
- real UID/EUID 1000;
- all three read-only write-denial probes passed, and bytes stayed unchanged.

I read the bootstrap, mathematical verifier, and control script. Required checks
do not rely on assert. A pinned manifest is checked before executing payload
code; isolated Python startup suppresses current-directory and PYTHONPATH import
poisoning. The controls exercise missing/extra/corrupt files, replacement
manifests, hostile code, symlinks, directories, FIFOs, and exact-type semantic
mutations. Forged manifest cases are rejected by the external hash, so those
tests alone should not be described as direct branch coverage of every schema
validator. Authentication assumes a trusted externally pinned bootstrap and
standard-library interpreter, with a static package during checking/execution;
this is not a proof against concurrent filesystem substitution.

The separately authored independent_checks.py imports no author-packet code.
It computes finite differences directly from binomial evaluation sums, uses
rational evaluations and grid interpolation, and checks the backward and forward
bridges through ambient degree 12. It includes long stencils, zero and lower-degree
inputs, coefficient recovery, symmetry, reflection, degree/leading-coefficient
identities, the nonzero-only degree criterion, and explicit wrong-formula
witnesses. There are **12,339 independent checks**. Its 135 additional exact
mesh cases through degree six include 35 nontrivial Sturm root-isolation
certificates; the remainder are zero/constant/linear boundary cases. No
floating-point root approximation is used.

INDEPENDENT_REPLAY.json records replay of this final independent script in a
source-free read-only copy under all three interpreter modes, including failed
creation/overwrite probes. It also records the script and output hashes. The
normal, -O and -OO output bytes agree. These computations are reproducible finite
diagnostics, not proof of the universal theorem.

## 6. Disposition, limitations, and publication boundary

No unresolved mathematical gap was found in the operator reduction or in its
application of the credited result. No correction patch is needed. The original
author packet's historical independent_review=pending fields should remain
unchanged in the immutable freeze. This separate audit records the completed
independent acceptance; it must not rewrite the historical receipt.

The source-free public allowlist is explicit in PUBLIC_ALLOWLIST.json. It permits
the authored frozen packet, its public metadata and receipts, and this authored
audit with its diagnostic programs and acceptance metadata. It excludes source
PDFs, source extracts or page images, dataset contents, private coordination,
raw tool transcripts, and temporary work. Source inspection metadata describes
what was actually inspected; source-free replay does not fetch or inspect a PDF.

The separately delivered manifest/archive hashes must be authenticated outside
the artifact itself. A co-shipped manifest does not establish its own trust.
No public upload, branch change, queue change, or CI success is asserted here.

## References

[S] Boris Shapiro, *Problems around polynomials: the good, the bad and the ugly*,
arXiv:1503.05295v1, Section V, page 3.
https://arxiv.org/abs/1503.05295v1

[LR] Jonathan Leake and Nick Ryder, *Connecting the q-Multiplicative Convolution
and the Finite Difference Convolution*, arXiv:1712.02499v1, Theorem 1.4.
https://arxiv.org/abs/1712.02499v1

[P] Publisher record, *Advances in Mathematics* 374 (2020), 107334.
https://www.sciencedirect.com/science/article/abs/pii/S0001870820303625
https://doi.org/10.1016/j.aim.2020.107334

[BKS] Petter Brändén, Ilia Krasikov and Boris Shapiro, *Elements of Pólya–Schur
theory in the finite difference setting*, arXiv:1204.2963v2.
https://arxiv.org/abs/1204.2963v2
