# PR26 / AMR-103-0115: independent modular-family audit

**Mathematical verdict: PASS for the low-strand partial result and printed-source
correction.** No full solution for n >= 4 is supplied. One minor scope wording
repair is recommended before promoting the packet: qualify the standalone
README's unresolved assertion as a conclusion of this investigation. The parent
owns repairs, the fresh complete gate, integration, and any publication decision.

Reviewed frozen head: `762f5808268a85a5cb5373d3f7d60ad160b828f5`.
Frozen main mathematical artifact: `source_snapshot/OBSTRUCTION.md`, SHA-256
`8237a910fc2423e3d55ca09cd9bf0bc4300d588e9279b25fe78d41f0037a3995`.
All fourteen frozen attempt files match their recorded bytes, SHA-256 and
Git-blob SHA-1, computed without invoking Git. No originals were edited.

## Independence and source record

Before reading any historical proof, review, program, receipt or source-record
contents, this family read and visually inspected the complete literal source
page, independently consulted primary author texts about braid and modular
presentations, and wrote the claim, falsification criteria and derivation in
`EARLY_SEAL.md`. Its UTC seal is **2026-10-01T22:07:32.719861+00:00**, SHA-256
`14d51d2c90631359d292467f1fa8010a36535e85b4d8a5f0725b39c868800010`.
The seal has not been rewritten after comparison with the historical packet.

The exact source is [Ohtsuki's problem list](https://msp.org/gtm/2002/04/gtm-2002-04-024s.pdf),
Problem 6.7, printed p. 470 / physical PDF 98. It asks for algebraic-coefficient
faithful braid representations and places the higher-strand range in its
historical context. The adjacent two-dimensional integral claim is literally
printed there. The preseal publisher `024p.pdf` and original-packet `024s.pdf`
variants were both inspected; the latter download exactly reproduces the
original source checksum. Source statement, field bar and the neighboring
remark agree across the variants. A historical problem list alone cannot
certify current worldwide openness.

The primary texts consulted before seal were [Milne, Theorem 2.12 and Remark
2.14](https://www.jmilne.org/math/CourseNotes/MF.pdf), printed pp. 32-33, and
[Tuba-Wenzl, section 1.1](https://arxiv.org/pdf/math/9912013), pp. 1-2. After
seal, the citation in the original review to [Kassel-Turaev, Appendix A, Lemma
A.1 and Theorem A.2](https://web.math.ucsb.edu/~bigelow/books/kasselturaev.pdf)
was followed through its complete proof on printed pp. 311-314, including visual
inspection. It supports exactly the indicated quotient and generator matrices.
The independent action proof below does not assume the quotient isomorphism
merely because a citation or prior review asserted it.

The other URL in the original source/readiness records,
[Scherich 2023](https://msp.org/agt/2023/23-5/agt-v23-n5-p03-s.pdf), was retrieved
with the original checksum. Theorem 1.1 and its proof, and the complete relevant
section 3.3, yield discreteness of the stated specializations. They do not
supply the injectivity missing from the general target. This family makes no
claim to have exhausted later literature; the parent source-status family owns
that broader bounded search.

Download URLs, UTC times, locations and hashes are retained in `sources/`.
Foreign PDFs, text extractions, renders and isolated execution copies are in
ignored `tmp/`; those third-party documents are not incorporated into the
publication artifact manifest.

## Strongest universally verified mathematical claims

With x=sigma_1 and y=sigma_2, let A=xyx, B=xy and z=(xy)^3. Then

\[
B_3\cong\langle A,B\mid A^2=B^3\rangle,\qquad
Z(B_3)=\langle z\rangle\cong\mathbb Z,\qquad
B_3/\langle z\rangle\cong C_2*C_3\cong\mathrm{PSL}_2(\mathbb Z).
\]

Put

\[
U=\begin{pmatrix}1&1\\0&1\end{pmatrix},\quad
V=\begin{pmatrix}1&0\\-1&1\end{pmatrix}.
\]

The assignment x -> 2U, y -> 2V gives a faithful representation
B_3 -> GL_2(Q), with central image rho(z)=-64I. B_1 and B_2 also have
faithful rational representations, the latter by its generator -> 2 in Q^*.
Conversely B_3 has **no** faithful representation into GL_2(Z). The statements
concern these coefficient fields and degree exactly as written; they do not
exclude higher-dimensional integral representations.

Here is the complete logical mechanism, with boundary cases explicit.

1. From xyx=yxy, one obtains A^2=B^3. Conversely in the A,B presentation, set
   x=B^-1 A, y=A^-1 B^2. Then xy=B, xyx=A and yxy=A^-1 B^3=A. Thus the
   presentations are isomorphic. The element z=A^2=B^3 is central and is
   infinite-order because the exponent homomorphism e(x)=e(y)=1 has e(z)=6.
   Factoring by z leaves exactly the free-product presentation. Since the
   normal closure of a central element is cyclic, the quotient kernel is
   exactly <z>. Free-product normal forms show its center is trivial, so no
   additional central elements in B_3 were omitted.
2. Direct multiplication gives UVU=VUV=S=[[0,1],[-1,0]], R=UV=[[0,1],[-1,1]],
   and S^2=R^3=-I. This defines phi:B_3 -> SL_2(Z) and a homomorphism of the
   free-product quotient to PSL_2(Z). Its injectivity is checked by action on
   the real projective line: S(t)=-1/t and R(t)=1/(1-t). The two nonidentity
   R-powers send t<0 into (0,1) and (1,infinity), respectively; S sends t>0
   to t<0. Every reduced odd-length word beginning and ending in one factor
   sends the other factor's domain into that factor's domain. An even-length
   word is cyclically rotated to start with a and end with b^r. Conjugating
   by b^t, t in {1,2}, t != r, produces an odd-length reduced word beginning
   and ending with b. Thus every nonempty reduced word acts nontrivially.
3. Surjectivity is a separate Euclidean-algorithm argument. R^-1 S=U, and
   left multiplication by powers of U and by S reduces the primitive first
   column of any determinant-one integer matrix to (+/-1,0). The remaining
   upper-triangular matrix is generated by U and the sign S^2=-I. Consequently
   the quotient is all of PSL_2(Z), ker(projective phi)=<z>, phi(z)=-I and
   ker(phi)=<z^2>. No desired faithfulness of a scalar twist was used here.
4. For any nonzero rational c, rho_c(g)=c^{e(g)} phi(g) is a representation,
   including inverse generators c^-1 U^-1 and c^-1 V^-1. Its kernel is central
   by step 2, and rho_c(z)=-c^6 I. Hence rho_c is faithful if and only if
   -c^6 has infinite multiplicative order. For c=2, (-64)^k=1 forces k=0
   for all integer k. Alternatively det(rho_2(g))=4^{e(g)} first forces
   e(g)=0, and a central g=z^k has e(g)=6k, again forcing k=0. Rational
   twists c=1,-1 fail because z^2 maps to I; c=2,-2,1/2 pass. Positive
   generator matrices at c=2 have integer entries but determinant 4, and
   their inverses have denominators, so this is GL_2(Q), not GL_2(Z).
5. The argument does not assume torsion-freeness. Nontrivial finite-order
   elements in C_2*C_3 are conjugate into one factor; this follows by cyclic
   reduction and growth of powers of a reduced length >=2 word. Their
   exponent modulo 6 is 3, 2 or 4. If a braid were torsion, its integer
   exponent would be zero, excluding those images. Its remaining central
   form z^k also has nonzero exponent unless k=0. Projective torsion therefore
   creates no hidden torsion or lifting gap.

For the integral assertion, a nonscalar rational two-by-two matrix C admits a
cyclic vector v with v,Cv independent. A commuting operator is determined by
its value av+bCv at v, and commutation determines its value at Cv. Thus its
entire centralizer is the commutative algebra Q[C]. This covers nonsplit,
Jordan, reducible and irreducible cases, without an unjustified use of Schur's
lemma. A faithful integral image must send infinite-order central z to an
infinite-order matrix. Scalar units of GL_2(Z) are only +/-I, so its image
cannot be scalar. If it is nonscalar, both generator images lie in its
commutative centralizer, contrary to the nonabelian B_3. The scalar argument
fails over Q because -64I has infinite order there; the centralizer argument
need not be commutative in larger degree. Reduction over finite fields cannot
preserve this infinite-group faithfulness, and the c=2 twist is singular in
characteristic 2.

## New adversarial implementation evidence

`modular_controls.py` is a newly written standard-library program rather than
a restatement of the historical 35 assertions. It independently multiplies
matrix words and implements a central normal form z^k times alternating
A/B remainders, retaining integer carries from A^2=z and B^3=z. Its exact
exponent is 6k plus weights 3 for A and 2 for B. Uniqueness follows from the
free-product quotient normal form and infinite order of z. The program uses
integers and rational fractions, with explicit type controls excluding floats.

The final run passed **316,447 assertions**, covering all **39,365 freely
reduced braid words of length at most 9**, and **441 reduced quotient words of
at most 12 syllables**. There are **252** even-word conjugacy witnesses and
**5,371** distinct projective-image/exact-exponent pairs in the braid sample.
These counts audit implementation consistency; universal faithfulness rests
on the preceding proof, not on finite search.

Materially new controls include:

- Agreement of independently computed braid normal forms, exponents, matrices,
  projective kernels and twisted determinants, including negative words.
- An explicit exponent-zero commutator with matrix [[1,1],[1,2]], rejecting
  determinant-only detection; z and z^2 reject projective-only and untreated
  +/-I detection; adding z to a word exposes exponent-modulo-six ambiguity.
- Center powers from -12 through 12 at five twists, intentionally distinguishing
  the valid rational twists from c=1,-1; unequal scales 2U and 3V fail the
  relation before any faithfulness test.
- Rational centralizer equations for nonsplit, Jordan, split, determinant-minus-one,
  hyperbolic unimodular and scaled Jordan matrices, plus the scalar exception.
- Deliberate finite-field kernels sigma_1^{p(p-1)} at p=3,5,7,11 and
  characteristic-two singularity, checking exactly where the rational proof
  ceases to apply.
- Finite-order projective lifts and the n=1,2 boundaries.

An isolated replay using a second pre-existing Python environment reproduced
all mathematical receipt fields. Timestamps and interpreter version were
excluded as environmental metadata. `modular_results.json` and
`modular_replay_receipt.json` record versions, UTC times and script hashes.
An initial new-script run completed its checks but failed while serializing
Fraction residues; that implementation issue was corrected and logged before
the passing final run. No failed result was passed off as a final receipt.

## Historical reconciliation and provenance

After seal, all fourteen original files were read completely, including the
full obstruction, historical review, both programs and saved JSON receipts.
The original §4 agrees with the independent proof. The original note also
states the Qbar/Q restriction-of-scalars equivalence with degree increase, and
its countermodel to automatic algebraic specialization is correctly delimited
as a general inference counterexample. Neither statement extends the low-strand
construction to the missing range. This family did not search for a new
higher-strand proof and does not claim mathematical novelty for the sealed
elementary derivation.

The two original programs were replayed only in `tmp/original_replay` using a
pre-existing SymPy **1.14.0** environment. Both output receipts reproduced
**byte for byte**, including the historical program hash in the independent
receipt. The original README accurately distinguishes those finite examples
from universal proofs. `original_replay_receipt.json` records these checks.

The historical review's artifact hash and own document hash both match.
The readiness `review_hash` is a source/triage context hash: independently
computing SHA256(json.dumps([source_record,prior_report], sort_keys=True).encode())
gives the recorded value
`16717ef9457560e93f7f319a303a38bc2693cf47ed6bd54c70a429f019d60420`.
It should not be compared to the hash of REVIEW.md. `turns.jsonl` contains
exactly turn 1, readiness records used=1 and maximum=5, and the original
research log describes one substantive attempt. The correct ledger remains
**1/5**. This audit adds **zero** substantive proof-search attempts.

## Actionable finding, disposition and exact gap

There is no required mathematical correction to the low-strand claim.
However, frozen `README.md` line 5 has an unqualified assertion that the target
remains unresolved for n >= 4. Replace it with **“This investigation does not
resolve the target for n >= 4.”** The main note and review summary already
preserve that limitation, so this is a narrow consistency repair. A direct
modular-presentation citation in §4 would also make that note independently
easier to follow, but is optional; the existing review provides the correct
reference.

Disposition must remain **unsolved / verified partial analysis**, with the
original **1/5** ledger. The strongest result is the universally faithful
rational representation for n <= 3 and the falsification of the printed
GL_2(Z) assertion. The missing result is one finite-dimensional representation
over algebraic numbers whose injectivity is proved for every braid word in
the higher-strand range, or a general impossibility proof. No such result is
supplied here. Discreteness and finite-word survival do not fill that gap.

Family audit completion estimate: **100%**. The original packet's 10% full-goal
estimate and this family's 5% estimate are heuristic planning judgments, not
mathematical evidence or fractions of strand indices solved. No Git action,
shared ledger mutation, canonical repair, researcher contact, installation,
PR operation, publication, release or DOI creation was performed by this family.
