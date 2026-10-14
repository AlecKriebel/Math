# Supplemental acceptance: independent-step charging certificate

This is a narrow supplement to the frozen PASS1 game audit. It changes no prior audit artifact and does not constitute another proof pass. The unrestricted two-dimensional Time-Bomb conjecture remains unresolved.

## Public edition and exact audited input

This public edition omits one ancillary summary citation. The mathematical
audit below is unchanged. The original acceptance note is identified in
[ORIGINAL_IDENTITIES.json](../ORIGINAL_IDENTITIES.json); its original hash
does not identify this adapted edition.

- `../pass1_invariant/INDEPENDENT_STEP_POTENTIAL_OBSTRUCTION.md`, SHA-256 `50178e944724a1d0b2c64cfdf634ed516ce701f307af3473de35c412db9e90fa`.

The previously frozen `AUDIT.md` has SHA-256 `8c1452cfd3b1076e20ff45e121d53a786247eec0cd544a3e298825fbd4f189de` and is unchanged.

## Accepted endpoint-mass bound

Let X_1,…,X_h be independent random vectors taking values in {−1,0,1}², with any distributions prescribed in advance. Identical distributions are unnecessary. Let S_h be their sum and m=E[S_h]. For coordinate i∈{1,2}, each X_(j,i) lies in [−1,1], so its variance is at most 1. Independence across increments gives

Var(S_(h,i)) = sum_(j=1)^h Var(X_(j,i)) ≤ h.

No independence between the two coordinates of an increment is assumed or needed. Chebyshev's inequality gives probability at most 1/4 that a specified coordinate deviates from its mean by more than 2√h. The union bound therefore places probability at least 1/2 inside

[m_1−2√h,m_1+2√h] × [m_2−2√h,m_2+2√h].

An interval of length 4√h contains at most floor(4√h)+1≤4√h+1 integers, even when its center is nonintegral. The square consequently contains at most

(4√h+1)² ≤ 25h

integer points, using h≥1. At least one endpoint has probability at least

max_z P(S_h=z) ≥ 1/(50h).

This proves the claimed bound uniformly over all prescribed independent increment laws, including degenerate laws and nonzero drift. The same proof applies to any prescribed length-h suffix/window of such a sequence.

## Accepted consequence, with its exact limitation

For a fixed independent continuation law and one terminal time T, let K_h be the endpoint law with h moves remaining, and let the potential be the sum of K_h(b−a) over distinct already announced terminal-bomb positions b. The convolution averaging identity permits an Angel move that does not increase the pre-update potential. A newly announced bomb increases it by at most max_z K_h(z), with duplicates adding nothing.

Starting with no announcements, the sufficient charging condition is

sum_(h=1)^(T−1) max_z K_h(z) < 1.

There are exactly T−1 potentially effective announcements before the terminal move, with successive remaining lengths T−1,…,1. At the terminal move, a potential below one guarantees the current position is not bombed.

The audited lower bound gives

sum_(h=1)^(T−1) max_z K_h(z) ≥ (1/50) sum_(h=1)^(T−1) 1/h.

The right side diverges. Thus for sufficiently large T this particular charging condition cannot hold. The bound is uniform, so choosing a different prescribed independent law for each T does not repair that all-horizon certificate. Predetermined time-inhomogeneous independent increments also do not repair it: every remaining window obeys the same bound.

This establishes only an obstruction to the specified certificate, which charges the worst new-bomb increment and credits Angel moves merely with nonincrease. It does not prove that an actual minimizing policy loses: its moves may create favorable decreases that this accounting discards. It does not exclude correlated, history-dependent, nonlinear, multiscale, or other potential arguments. It does not address mixed detonation times by itself.

## Decision

Accepted without a mathematical correction. The narrow statement may be included among the verified PASS1 partial results with the above scope. No computation or rerun of the prior finite-game certificate was necessary.
