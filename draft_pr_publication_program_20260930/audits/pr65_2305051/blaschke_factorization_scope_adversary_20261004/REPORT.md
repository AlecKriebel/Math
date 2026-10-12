# PR65: independent factorization, construction, and full-target audit

**Family verdict: PASS — no essential gap found in the original complete construction.** This is an independent AI mathematical audit of one approach family, not human/referee review, formal proof certification, or priority clearance.

## Frozen object, scope, and independence

- Repository: `AlecKriebel/Math`, PR65.
- Immutable head: `5cc1602c05d79502defb07cec7027963149494d2`.
- Linked recursive tree: `1870fd8a628fef3ee14ba1ca917f2faf91bb823e`; the tree response is not truncated.
- Original candidate: `unsolved_math_prioritization/attempts/2305051/CANDIDATE.md`.
- Candidate Git blob: `7802cf06a9daa4b19e894e3b7a276740948bc37d`.
- Candidate SHA-256: `0a15d03ab92cbd13f17042a4708f75c3d592f4884810c7ffadc6a5f34f1cb6c4` (13,491 bytes, tree mode `100644`).

All 18 original attempt blobs were independently recomputed from the source authenticator's downloaded bodies and compared against the immutable Git tree; all identities and modes pass. The commit-to-tree link was checked separately. These checks authenticate bodies, not the mathematics. `AUTHENTICATED_INPUTS.json` gives every body hash. The submitted queue entry is literal `claimed_solved`, `2/5`; no attempt/status/queue mutation was performed.

The original candidate and complete imported source record were read before the original author review, corroborating code, or other agents' scientific verdicts. The candidate-first analysis was frozen in `INDEPENDENT_CANDIDATE_FIRST_CHECKPOINT.json` at 2026-10-04T05:24:47.305504+00:00. Only afterward were the old review and code inspected. Root's early messages supplied authentication and source scope, not a mathematical verdict. The later old review agrees with the independent density/factorization analysis; it was not used as a proof certificate.

This audit validates the existing complete candidate. It does not continue a central-proof search or add a substantive attempt response; the original 2/5 record is unchanged. Work and logs are confined to this audit folder. There was no outreach, Git index/ref mutation, commit, push, release, PR edit, editor mutation, or status change.

## Exact claim and success criteria

The [primary Hayman–Lingham source](https://arxiv.org/pdf/1809.07200v2), Problem 5.51, printed p.105, asks for an explicit construction of a disk Blaschke product normalized by `B(0)=0` whose Cayley transform is Bloch. Its 2018 update is dated source context, not current-priority evidence.

For this candidate the required checks are: the deterministic integer recursion actually defines every stage; the stated rational functions converge to a nonconstant analytic disk contraction; the normalization is exact; the limit is a pure Blaschke product, including its zero condition and absence of a singular factor; the specified Cayley transform is the proved Bloch Herglotz transform; and explicitness does not merely invoke an existence theorem or unspecified choice.

The source does not require a short closed-form enumeration of individual zeros. A fully specified recursive limit with an effective compact-uniform approximation modulus is a concrete explicit construction. This reading is an assessment of the source's ordinary wording, not a formal definition supplied by Holland. Priority and novelty remain unestablished here.

## 1. The dangerous implication is not being assumed

Local uniform convergence of finite Blaschke products, even with a zero at the origin, does **not** prove that the limit has no singular factor. A checkable negative control is

\[
 C_n(z)=z\left(\frac{a_n-z}{1-a_nz}\right)^n,
 \qquad a_n=1-\frac cn,\quad c>0,\quad n>c.
\]

Every `C_n` is a finite Blaschke product and `C_n(0)=0`. On each compact disk,

\[
 \log\frac{a_n-z}{1-a_nz}
 =-\frac cn\frac{1+z}{1-z}+O_r(n^{-2}),
\]

where the logarithm tending to zero is well defined for sufficiently large `n`. Thus

\[
 C_n(z)\longrightarrow z\exp\left(-c\frac{1+z}{1-z}\right),
\]

an inner function with a nonzero singular factor. This directly falsifies the shortcut one would otherwise be tempted to use. The candidate explicitly rejects that shortcut and provides a separate density obstruction in Section 5.

## 2. Existence and uniqueness of the measure do not conceal a selection oracle

Every positive integer parent has two `+1` and two `-1` increments, chosen by fixed comparisons and a finite ordered list. Zero parents remain zero. Therefore the child masses sum to the parent mass, all masses are nonnegative rational numbers, and a generation-n mass is at most `(n+1)4^{-n}`. Neighbor-directed endpoint rules give the uniform circular neighbor bound of 2, with equality, positive/zero, and cyclic cases explicitly covered by the candidate.

The weak-limit phrase in Section 2 can be checked without presupposing atomlessness. At a fixed point choose, at generation `n`, a small open neighborhood contained in at most two adjacent cells. Every later density measure assigns it mass at most `2(n+1)4^{-n}`. The open-set inequality in weak convergence gives the same upper bound for any weak limit. Letting `n` grow proves the weak limit has no atoms. Hence generation-n cell boundaries are continuity sets and the exact cell masses pass to the limit. The interval algebra fixes that limit uniquely.

Thus compactness establishes existence of the uniquely predetermined measure; it does not choose the output from several possibilities. More decisively, the answer is defined by the explicit finite rational functions and their proved modulus of convergence. No implementation must select a weak-limit subsequence. There is no unspecified covering map, parameter, or good Frostman shift.

The absorbed simple random walk proves that the union of zero-mass cells has full Lebesgue measure. Those cells have zero limiting measure, so the measure `mu` is singular. This alone would be insufficient to prove purity of the Cayley transform.

## 3. Strict contraction, exact normalization, and innerness

For the constructed probability measure,

\[
 F(0)=1,\qquad \Re F(z)=P[\mu](z)>0\quad(z\in\mathbb D).
\]

The strict inequality follows from positivity of the Poisson kernel and total mass one, including when the measure is singular. Consequently `F+1` never vanishes in the disk,

\[
 B=\frac{F-1}{F+1},\qquad B(0)=0,\qquad |B(z)|<1.
\]

The identity

\[
 1-|B|^2=\frac{4\Re F}{|F+1|^2}\le4\Re F
\]

and the zero Lebesgue-a.e. radial limit of the Poisson integral of a singular measure show radial modulus one a.e.; the bounded-analytic boundary theorem gives the boundary values. This establishes innerness. Nonconstancy follows from uniqueness of the Herglotz representation: the only constant `F` compatible with `F(0)=1` is 1, whose measure is Lebesgue measure, contradicting the singular probability measure. The inverse identity `(1+B)/(1-B)=F` holds everywhere in the disk because strict contraction excludes `B=1` there.

## 4. Pointwise density exclusion, including endpoints

For **each** circle point, follow the specified nested half-open four-adic cells. Their exact density ratios are the corresponding integer values in the recursion. Either the path reaches zero and stays zero, or adjacent ratios differ by exactly 1 forever. An eventually zero sequence cannot tend to a finite positive number; a sequence whose successive differences all have modulus 1 cannot converge to any finite number.

An ordinary density `L>0`, defined by all shrinking intervals with the point strictly inside, would also force these ratios to approach `L`. For a nonendpoint the chosen cells already have the point inside. At a four-adic endpoint the cells eventually lie on one side. The endpoint reduction can be made quantitative: compare `(x,x+h)` with `(x-h^2,x+h)`. The latter interval contains `x` strictly inside and its mass is `L(h+h^2)+o(h)`. Ordinary density on symmetric intervals bounds the extra piece's mass by `O(h^2)`, by positivity. Hence the one-sided ratio tends to `L`. The opposite side is identical. Atomlessness makes the inclusion or exclusion of endpoints irrelevant. Thus no point, including a grid endpoint, can have finite positive ordinary density.

The obstruction is pointwise, rather than Lebesgue-a.e. This matters because a hypothetical singular-factor measure could be supported on a Lebesgue-null exceptional set, even if the original Herglotz measure is singular.

## 5. Singular-factor exclusion: all hypotheses match

Use canonical inner factorization, writing the hypothetical singular factor as `S_nu` with nonzero finite positive singular measure `nu`. Differentiation with respect to `nu` implies, at `nu`-a.e. boundary point `xi`, that

\[
 \frac{\nu(I(\xi,\delta))}{\delta}\longrightarrow+\infty.
\]

For `z` in a fixed Stolz cone at `xi` and `delta=1-|z|`, the Poisson kernel on this centered arc is bounded below by a cone-dependent positive constant times `1/delta`. Therefore `P[nu](z)` tends to infinity throughout every fixed cone. The standard singular-factor identity `|S_nu(z)|=exp(-P[nu](z))` gives `S_nu -> 0` nontangentially. All other inner factors have modulus at most one, so `B -> 0` nontangentially and consequently `F -> 1`, with `Re F -> 1`, at these points.

The precise classical input was checked directly in [Carmona–Donaire](https://msp.org/pjm/1999/191-2/pjm-v191-n2-p02-p.pdf), printed pp.207–208. Their stated Loomis theorem says that positivity and a finite nontangential Poisson limit give the ordinary derivative. Its separate radial assertion only gives the symmetric derivative. The candidate uses the nontangential hypothesis and positivity, so it invokes the correct assertion, with `L=1` finite. No infinite-limit converse, signed-measure converse, or merely radial implication is being substituted.

The disk-to-half-plane passage is checkable explicitly. Rotate `xi` to 1, put

\[
 z=\frac{1+iw}{1-iw},\quad w=x+iy,\qquad
 \zeta(t)=\frac{1+it}{1-it},\quad t\in\mathbb R.
\]

Then

\[
 \frac{1-|z|^2}{|\zeta(t)-z|^2}
 =\frac{y(1+t^2)}{(x-t)^2+y^2}.
\]

If `sigma` is the pushforward of the rotated circle measure, set `d tau(t)=pi(1+t^2)d sigma(t)`. The disk Poisson integral is exactly the half-plane Poisson integral `P[tau]`, with normalization `1/pi`. There is no contribution from the antipodal point because the candidate measure is atomless, and

\[
 \int_{\mathbb R}\frac{d\tau(t)}{1+t^2}=\pi\mu(\mathbb T)<\infty,
\]

as required by the primary theorem. Locally the normalized angle is `theta=arctan(t)/pi`, so `d theta/dt=1/pi` at 0. The factor `pi` in `tau` cancels this coordinate factor. Half-plane density 1 becomes density 1 with respect to normalized circle length. The smooth conformal map preserves nontangential approach locally at this finite boundary point.

Loomis therefore gives ordinary density 1 for `mu` at `nu`-a.e. `xi`. Section 4 excludes this at every point. Hence `nu=0`. This is a complete exclusion of a concealed singular factor; no generic shift has been used.

## 6. Zeros, summability, and infiniteness

The zeros of the nonzero analytic function `B` are discrete, with finite multiplicity. Let `m>=1` be the zero order at 0 and put `g=B/z^m`. Repeated Schwarz's lemma gives `|g|<=1`, and `g(0) != 0`. Jensen's formula gives, for radii avoiding zeros,

\[
 \sum_{0<|a_k|<r}\log\frac r{|a_k|}
 \le-\log|g(0)|.
\]

Monotone convergence as `r` tends to 1 gives

\[
 \sum_k\log\frac1{|a_k|}<\infty,
 \qquad \sum_k(1-|a_k|)<\infty.
\]

Thus the zero divisor satisfies the actual Blaschke condition. With the singular canonical measure now zero, canonical inner factorization identifies `B` as the unimodularly normalized product of its zeros (and the origin factor). Lack of a closed-form zero list is not a missing summability proof or a hidden singular factor.

A finite nonconstant Blaschke product maps the boundary onto the circle. At a point mapped to 1, its boundary derivative is nonzero: the angular phase derivative is the sum of the positive Poisson terms associated to its zeros. Its Cayley transform then has a simple boundary pole; its derivative grows like `(1-r)^{-2}` on an inward radius, violating the Bloch bound. Hence the constructed Blaschke product is infinite. The atomless Herglotz measure also excludes such a pole.

## 7. Rational stages and effective explicitness

The atomic midpoint measure has exactly the same mass as `mu` in every generation-n cell, total mass one, and nonnegative rational weights. Its Herglotz transform `F_n` has positive real part in the disk. Away from its finitely many atoms its boundary values are purely imaginary, so the Cayley transform `B_n` has boundary modulus one. At a positive atom, the simple pole of `F_n` becomes a removable point of `B_n` with value 1. Distinct atom locations ensure the displayed polynomial denominator at that atom is nonzero after the pole is removed. Elsewhere on the circle `F_n+1` cannot vanish because its real part is 1. Thus `B_n` is rational inner and has no disk or circle pole; factoring its finitely many disk zeros and applying the maximum principle to the remaining zero-free quotient proves it is a finite Blaschke product. Rational weights and specified roots of unity give algebraic coefficients. Every `B_n(0)=0` exactly.

For the kernel `K(x,z)=(e^{2 pi i x}+z)/(e^{2 pi i x}-z)`,

\[
 |\partial_x K(x,z)|\le\frac{4\pi r}{(1-r)^2}\quad(|z|\le r<1).
\]

Each midpoint move costs at most `4^{-n}/2` in normalized angular length. Integrating against total mass one gives the claimed `F` error, and

\[
 B-B_n=\frac{2(F-F_n)}{(F+1)(F_n+1)},\qquad
 |F+1|,|F_n+1|\ge1
\]

gives the stated error

\[
 \sup_{|z|\le r}|B-B_n|
 \le\frac{4\pi r}{(1-r)^2}\,4^{-n}.
\]

This is compact-uniform, not boundary-uniform. It does not claim a uniform Bloch bound for the atomic transforms; their boundary poles would forbid that. The candidate instead establishes the global Zygmund estimate for the **limit** measure and invokes the classical Herglotz–Zygmund criterion for that measure. This preserves the required Bloch Cayley transform while using finite stages only to specify and approximate the output.

The imported correspondence was also independently checked in the [full Aleksandrov–Anderson–Nicolau primary paper](https://mat.uab.cat/~artur/data/innerfunctions,blochspacesand.pdf), in the proof of Theorem 3.5 on printed p.333. It states the Bloch/Zygmund equivalence for a positive measure's Herglotz integral. The same paper's introductory canonical-factorization statement on printed p.318 corroborates the standard decomposition used above. Neither paper's separate existence construction is used as the answer to Holland.

For a concrete precision algorithm, choose rational `r<1` with `|z|<=r`, and rational error `epsilon>0`. Compute the least `n` such that

\[
 \frac{13r}{(1-r)^2}4^{-n}\le\epsilon/2.
\]

Since `4 pi<13`, the truncation error is at most `epsilon/2`. Compute the finite recursion to this `n`, its exact algebraic atoms/coefficients, and evaluate `B_n(z)` to error at most `epsilon/2`. Standard effective evaluation applies to computable inputs; the denominators are separated from zero on this compact disk. This terminates and determines `B` to the requested precision, with no unevaluated central search. It is not necessary for an algorithm to find or certify all limit zeros before evaluating the constructed product.

## 8. Corroborating artifacts and limits of the verdict

The original submitted checker and original prior independent checker were read after the candidate-first checkpoint. Their finite assertions support recursion, mass, neighbor, and algebraic identities. They cannot establish the no-singular-factor conclusion, and this audit does not infer that conclusion from their reported assertion counts.

The new `exact_factorization_controls.py` imports no author code and passes **4,534 exact rational controls**, including the disk-to-half-plane kernel identity, strict Cayley contraction, defect and difference identities, denominator bounds, and deterministic precision stages. `EXACT_CONTROL_RESULTS.json` and captured command 011 record the execution. These are bounded consistency checks, not a universal factorization or boundary proof. The analytic derivations and correctly scoped classical inputs above provide the mathematical basis of the family verdict.

**Strongest verified result in this family:** the candidate's deterministic rational-inner limit defines a nonconstant infinite pure Blaschke product with its asserted normalization and effective compact-uniform convergence, and the construction matches the source's requested type and Cayley transform. No mandatory mathematical correction was found within the assigned family. The other proof families must separately audit the all-stage Bloch/recursion reasoning; this report does not replace their independent gate.

**Exact remaining gap:** none identified for factorization, zeros, normalization, convergence, or recursive explicitness. Historical priority, novelty of the specified recursion/application, a closed-form zero list, human peer review, and formal verification have not been established. No such extra claim is needed to validate this family's mathematics, and none is certified here. The assigned validation task is complete; original discovery progress is not advanced.

## Provenance

`ACTUAL_COMMANDS.jsonl` records actual subprocess argv, working directory, UTC start/end, exit code, and stdout/stderr hashes for commands 001 onward, with corresponding sidecars. The initialization and instruction-read tool calls preceded that recorder and are not retrospectively represented as captured executions. `PRIMARY_SOURCE_MANIFEST.json` records downloaded primary PDFs and hashes. `WEB_TOOL_CALLS.json` records actual web inputs and the incorrect initial Carmona PDF route, which was recognized as a different paper and not used as theorem evidence. The correct published paper was then read and downloaded.

`RESEARCH_LOG.md` records checkpoints with UTC timestamps and completion estimates. `VERDICT.json` supplies a machine-readable bounded verdict. `SELF_MANIFEST.json` covers all finished audit artifacts other than itself and records the exact immutable head. No file in the original source-authentication folder was modified.
