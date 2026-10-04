# PR 65 — independent universal analytic/Bloch audit

**Scoped verdict: verified; no defect found in the submitted global Bloch estimate or its compact convergence/denominator argument.** This is one mathematical audit family, not an overall certificate that the exact target is solved or novel.

Reviewed immutable head: `5cc1602c05d79502defb07cec7027963149494d2` of `AlecKriebel/Math`, target `2305051` / `AMR-022-5051`. The original candidate is 13,491 bytes, git blob `7802cf06a9daa4b19e894e3b7a276740948bc37d`, SHA-256 `0a15d03ab92cbd13f17042a4708f75c3d592f4884810c7ffadc6a5f34f1cb6c4`. Full-body authentication is preserved in `INPUT_AUTHENTICATION.json`.

## Exact claim and audit independence

The original target asks for an explicit Blaschke product `B` in the disk, with `B(0)=0`, such that `(1+B)/(1-B)` is Bloch. This family's success criterion is an independently checkable proof that the submitted recursive measure's Herglotz transform `F` is holomorphic and satisfies a single global derivative bound, together with verification that the prescribed approximants converge to its Cayley transform and that no disk denominator is silently assumed away.

The original `CANDIDATE.md` was read first, before author reviews. The original `source_record.json` and `SOURCES.md` were then authenticated and read. No submitted author review, independent checker, prior reviewer verdict, or another adversary's mathematics was used to form this conclusion. The bounded checker was written independently from the recursion. Repository instructions and the queue README/selected original row were read; no queue, native status, Git reference/index, PR, or publication state was changed.

## Strongest independently verified result

The full proof is in `UNIVERSAL_DERIVATION.md`. It verifies all-stage positivity, conservation of mass and the circular neighbor bound; closes the weak-limit endpoint argument; proves the candidate's second-difference constant 24; and directly reconstructs the analytic sufficiency step. Specifically,

\[
\sup_{z\in\mathbb D}(1-|z|^2)|F'(z)|
\le 240\pi(\pi^2+1)<8196.
\]

The constant is intentionally inefficient. Its finiteness and uniformity are the relevant properties. The proof controls both components of the derivative: a Poisson-kernel second-derivative estimate bounds the angular derivative of `Re F`, and a harmonic gradient estimate applied to `Im(zF')` bounds `Re(zF')`. The argument includes `z=0`, radii up to one, every angle, arcs wrapping the circle, and grid endpoints.

The kernel midpoint bound yields exactly the candidate's locally uniform error

\[
\sup_{|z|\le r}|B-B_n|\le\frac{4\pi r}{(1-r)^2}4^{-n}
\quad(0<r<1).
\]

The reconstruction additionally proves compact derivative convergence with

\[
\sup_{|z|\le r}|F'-F_n'|\le\frac{2\pi(1+r)}{(1-r)^3}4^{-n}.
\]

Both `F` and `F_n` have positive real part. Their `+1` denominators have modulus at least one, and `|1-B(z)|>=1-r` on a disk of radius `r`. There is no disk pole and no claimed fixed denominator lower bound near the boundary. The exact derivative identity recovers the Bloch bound even when `1-B` is small.

## Adversarial checks and limitations

`diagnostics.py` independently checks nine full generations (`n=0,...,8`), all 1,293 bounded neighboring configurations with values between 0 and 12 and parent differences at most two, and exact rational second differences at selected mesh/interior/cyclic points and scales. All assertions pass. These checks are explicitly labeled finite diagnostics; they do not prove the universal statements.

A negative control confirms that compact convergence cannot by itself justify a uniform boundary estimate. Every fixed atomic approximant has a boundary pole. Already at stage zero,

\[
(1-r^2)|F_0'(-r)|=2(1+r)/(1-r)\to\infty.
\]

This does **not** contradict the candidate, which bounds the limiting measure using Zygmund smoothness and states convergence only on fixed compact disks. It identifies an important failure mode for any attempted purely numerical verification of the conclusion.

The cited analytic criterion is correctly stated in the proof of Theorem 3.5 on printed p.333 of [Aleksandrov–Anderson–Nicolau (1999), author PDF](https://mat.uab.cat/~artur/data/innerfunctions,blochspacesand.pdf): Bloch membership of a positive-measure Herglotz transform is equivalent to the Zygmund measure property. The primary page was checked, and a fetched full PDF is preserved. The direct derivation above means this audit does not depend solely on that citation.

The positive-measure converse Fatou result is stated on printed pp.207–208 of [Carmona–Donaire (1999), published PDF](https://msp.org/pjm/1999/191-2/pjm-v191-n2-p02-p.pdf). This supporting theorem check agrees with the candidate's distinction between ordinary and symmetric density. Full application to inner-factor purity was deliberately left to the other assigned audit family.

**Exact remaining gap in this family: none identified.** Pure Blaschke factorization, the meaning of explicit construction in the original question, historical priority and comprehensive literature status are outside this family's verdict. No human referee, formal proof system, priority certification, release, DOI, or authorization to publish is asserted.

## Reproducibility and provenance

`ACTUAL_COMMANDS.jsonl` records real child PIDs, UTC start/end times, command arguments, exit codes, and separate stdout/stderr files for all subsequent audit commands. The initial tool reads occurred before the recorder existed, are noted honestly in the log, and were not assigned invented PIDs. Input hashes cover the complete originals read, and the final `ARTIFACT_MANIFEST.json` identifies the new audit outputs. All new writes are confined to this family's dedicated folder.
