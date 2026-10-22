# Independent audit: equal radial slits

## Verdict

PASS: source-matched published prior resolution, with the packet's stated primary-proof access limitation retained. No blocking mathematical, scope, or attribution defect was found. The recommended outcome is `already_solved`; the recorded authored effort remains 1/5. This audit is not an additional claimed proof attempt, a new solution, or a reconstruction of the complete published comparison argument.

This audit binds to the nine-file frozen packet, comprising its eight manifested files and `MANIFEST.json`, whose SHA-256 is `bf8748c37a3e7ba2ac905a6159e246ec087a7ec7b643ebe8b5e1b418f32638c5`. The original packet was not changed. All original files were read, both supplied commands were replayed, and separate exact controls were written without importing the original checker.

## Source and scope match

[Hayman-Lingham, Problem/Update 7.45](https://arxiv.org/abs/1809.07200v2), printed page 174, fixes the count and each slit length and asks for the minimum outer-circle harmonic measure at the origin. Its update credits Dubinin. A fresh versioned PDF matched the recorded hash; the relevant page was visually inspected and reference [201] checked.

[Dubinin's journal theorem](https://www.mathnet.ru/eng/sm2051), DOI [10.1070/SM1985v052n01ABEH002888](https://doi.org/10.1070/SM1985v052n01ABEH002888), covers the identical boundary-attached straight radial cuts, common inner radius, evaluation point, and unrestricted angular configurations. It maximizes the cuts' harmonic measure and gives rotation as the equality freedom. This proves the original optimization after complementation. The English publication is from 1985; the Russian original is from 1984.

The journal HTML has readable mathematical notation. Seven-page primary text extraction, including the proof section, was inspected. OCR loses consequential symbols. This audit's direct PDF request returned 403 and its screenshot request failed. Accordingly, source identification and theorem matching pass, while complete symbol-by-symbol verification of the published proof is expressly not claimed. No successful Dubinin PDF-byte retrieval, hash, or image inspection is claimed.

## Adversarial mathematical review

### 1. Domain, parameters, and topology

The normalization r = 1 - ell is exact because each removed radial segment has Euclidean length ell in the unit disk. The nondegenerate problem requires 0 < ell < 1, and p is a positive integer. The origin lies in the disk of radius r, which is entirely retained. Each remaining point can be joined radially to that inner disk without crossing a removed segment, so the domain is connected. Its complement in the sphere is the exterior closed disk with finitely many attached radial segments; that complement is connected, giving simple connectivity of the domain. This verifies the topology invoked by the Riemann-map argument.

Distinct angular directions give exactly p cuts. Relabeling changes no set. A global rotation preserves the evaluation point and the boundary target. An arbitrary rotated regular arrangement can therefore be rotated to the p-th roots of unity before applying the power map. There is no total-length optimization hidden in this reduction, and no claim is made for curved, unequal, disconnected, or interior cuts.

### 2. Complement, endpoint capacity, and multiplicity

Let C be the outer circle and E the union of cuts. Then the boundary is C union E, and C intersect E is precisely the finite set of attachment points. Each attachment point has only finitely many accesses from the domain: locally the radial cut divides the interior side of the circle into two sectors. The finite analytic boundary description makes the prime-end preimage finite. It therefore has zero harmonic measure. Slit tips are likewise single geometric points of zero harmonic measure; both banks nevertheless contribute to the measure of the whole cut.

An alternative check uses polarity of individual planar points, avoiding any ambiguity over prime-end versus geometric-boundary counting. Countably many such points would still have zero measure by countable additivity, but no assertion about arbitrary uncountable exceptional sets is needed here. Finiteness is more than enough.

Consequently omega(C) + omega(E) = 1, not 2 and not a formula missing a bank multiplicity. Maximizing omega(E) minimizes omega(C); the inequality direction in the packet is correct. Equality is unaffected by this exact affine transformation. The finite exceptional set also validates uniqueness for bounded harmonic functions with the specified boundary data away from the junctions.

### 3. Power map and the critical origin

For the regular configuration, the full inverse image of [r^p,1) under z^p is exactly the union of its p radial cuts, and the full inverse image of the unit disk is the unit disk. Thus the image domain is the single-slit disk with endpoint a = r^p. The map is p-to-one away from zero and has a critical point at zero; it must not be treated as a conformal bijection.

The packet instead pulls back the bounded single-slit harmonic solution. Locally write that solution as the real part of a holomorphic function. Composition with z^p remains holomorphic even at zero, so the pullback is harmonic everywhere. On the boundary it has the required values, with only finitely many exceptional attachments. Uniqueness identifies it with the regular configuration's outer-circle harmonic measure. The value at zero is unchanged, with no factor of p. Our exact Poisson-kernel identities for degrees 2 and 4 independently reject the tempting but incorrect degree multiplier.

### 4. Single-slit maps and branch choice

For 0 < a < 1, T(w) = (w-a)/(1-aw) has no pole in the closed unit disk, maps the disk to itself, sends a to zero and zero to -a, and preserves the outer circle. Its restriction to the removed real interval is increasing, since T'(x) = (1-a^2)/(1-ax)^2 > 0.

On the disk with the nonnegative radius deleted, arg(v) in (0,2 pi) is a globally valid branch. Its half sends the domain onto the upper half-disk. This is essential: the ordinary principal root would send points just below the positive cut into the lower half-plane. The packet specifies the correct branch. At v = -a the image is i sqrt(a).

The map q = (1+s)/(1-s) takes the diameter to the positive real axis and the upper semicircle to the positive imaginary axis. Interior real and imaginary parts are strictly positive. Thus (2/pi) arg(q), rather than its complement, is the required outer-arc harmonic function. At s = i t, with t = sqrt(a) in (0,1), the argument is 2 arctan(t) in (0,pi/2). The value is therefore exactly (4/pi) arctan(r^(p/2)). The normalization, branch, factor 4, and exponent p/2 all pass.

### 5. Equality and limiting cases

The geometric equality class in the cited theorem transfers to the unordered set of angles because all p rays are distinct and nonempty. For p = 1 all configurations are rotations, as required. The endpoints ell = 0 and ell = 1 cannot inherit the nondegenerate uniqueness statement: the first removes no interior slit, while the second removes the evaluation point. The packet correctly treats the latter formula value as a limit only.

If a nominal p-tuple repeats directions, it has q < p actual slits. Applying the q-slit bound gives a strictly larger minimum because r^(q/2) > r^(p/2). This excludes coincident rays as competitors without extending the comparison theorem beyond its stated distinct-ray setting. The value increases strictly with r and decreases strictly with p. The half-value example p = 2, r = sqrt(2)-1 is correct.

## Replay and new controls

The original 3,186 exact control instances and 25 separately labeled floating configurations replay successfully, with the recorded result matching. The checker does not establish global comparison, and the packet correctly discloses this. Its allowance for platform-dependent last bits affects only the two explicitly numerical diagnostics; exact group counts and all other recorded fields are compared unchanged.

The new independent checker passes 15,217 exact assertions. It tests inverse slit maps on a different rational grid and extreme rational endpoints, correct root-sheet geometry, quadrant inverses, harmonicity of real and imaginary monomial pullbacks, degree-2/4 Poisson averaging, repeated-ray monotonicity, and negative controls for wrong branch, degree factor, complement, and square-root normalization.

Six values also receive rational interval enclosures using alternating arctangent remainders and Machin's identity for pi. At p = 2, r = 1/2 the interval lies strictly between 0.59033447060 and 0.59033447061. This is a certified finite numerical control, not evidence replacing the analytic extremal argument. Full rational endpoints are in `INDEPENDENT_RESULTS.json`.

The independent binding checker validates the exact frozen manifest bytes and every original file. Mutation tests cover altered content, a changed manifest, an omitted file, and an extra file, in disposable copies. None changes the freeze.

## Publication boundary and remaining limitation

The bound audit deliverable contains authored analysis, code, checks, hashes, byte counts, public bibliographic metadata and inspection results only. It contains no source PDF, source image, extracted source text, dataset content, private coordination material, or raw browsing output. Repository publication was not performed by this auditor.

There is no mathematical correction required before publishing the packet as an attributed prior-resolution finding. Its qualification that the original comparison proof was not fully rederived or symbol-by-symbol audited must remain. The bounded repository duplicate searches and expected full-dataset hashes were not independently rerun or upgraded by this audit; their original explicit limits remain in force.
