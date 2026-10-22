# Independent mathematical audit: Function Theory 3.21

## Decision

Accept the author freeze unchanged as a credited verification of an existing affirmative result. Recommend `already_solved`, authored effort `1/5`. No new solution, exhaustive equality classification, human peer review, or formal proof verification is asserted. No mathematical correction patch is required.

This audit separates mathematical reasoning below from finite computer checks. The latter do not establish the general theorem.

## Source and exact theorem match

FitzGerald, Rodin, and Warschawski's Theorem 2 gives the diameter lower bound for a continuum in the closed unit disk. Their initial exclusion of the observation point and subsequent component-based definition govern its meaning. The author-posted extraction explicitly connects the theorem with Problem 3.21. It also identifies Gaier's anchored estimate and a continuum extension as proof inputs. Damaged symbols in the extraction prevent treating it as a clean typeset formula. [FRW, 1985](https://doi.org/10.1090/S0002-9947-1985-0768733-1), [author-posted text](https://www.researchgate.net/publication/243079947_Estimates_of_the_Harmonic_Measure_of_a_Continuum_in_the_Unit_Disk).

Hayman and Lingham's version-2 PDF was independently rehashed and its printed page 67 freshly rendered and inspected. Update 3.21 records the affirmative resolution; reference 270 identifies FRW, Transactions AMS 287(2), 681-685 (1985). Its undamaged problem formula confirms that the inverse-sine argument is d/2. [Problem and update, PDF page 68](https://arxiv.org/pdf/1809.07200v2#page=68).

Solynin's publisher abstract independently specifies the component containing 0, excludes 0 from the continuum, and states the same bound for positive diameters through 2. This is corroboration, not an additional proof dependency or a verified equality classification. [Publisher abstract](https://www.mathnet.ru/eng/znsl/v144/p146).

FRW PDF bytes and page images, Solynin full-text bytes, and Gaier's original proof remain unavailable to this audit. The general continuum comparison is an accurately identified published external input, not a reconstructed proof claimed complete.

## Independent operator and boundary audit

Let D be the open unit disk, let E be a nonempty compact connected subset of its closure, and first assume 0 is outside E. Since E is closed, 0 has a neighborhood in D minus E. Let U be the component containing 0. The quantity is

    h(E) = omega_U(0, E intersect boundary(U)).

The boundary payoff is 1 precisely at obstacle boundary points, including obstacle points on the unit circle; it is 0 elsewhere. Boundary values are understood through harmonic measure, not as an assertion of classical pointwise attainment at every possibly irregular boundary point.

The boundary of U is contained in E union boundary(D). Indeed, a point in D minus E has a sufficiently small connected neighborhood contained there, so it cannot be a boundary point of a different component. For a continuous path starting at 0, exit from U occurs on first reaching E or first exiting D. Thus, for Brownian motion with obstacle hitting time tau and disk exit time T, the payoff event is tau <= T. The use of <= incorporates contact on boundary(D). No claim of simple connectivity or boundary smoothness is needed.

A positive-length boundary arc is never hit strictly before T, while its ordinary disk harmonic measure at 0 is positive. Consequently the strict event tau < T would give the wrong problem. Likewise, measuring only E intersect boundary(D) in the unpunctured disk loses an interior obstacle: for the circle E = {|z| = 1/2}, the latter set is empty, whereas U is the disk of radius 1/2 and h(E) = 1.

These tests validate the author's operator interpretation and expose two tempting but incorrect replacements.

## Diameter, application, and endpoint audit

Compactness makes the diameter a maximum, and the triangle inequality gives 0 <= d <= 2. Applying the cited theorem with this same E gives

    h(E) >= asin(d/2)/pi.

There is no replacement set, diameter reduction, or extra regularity condition in this application. The principal inverse sine has values from 0 to pi/2 here. Reading the right-hand side as d times asin(1/2)/pi would be a different expression; at d=2 it would give 1/3 instead of 1/2.

For d=0 the lower bound is zero and follows from nonnegativity. If 0 belongs to E, there is no component of D minus E containing 0 and classical interior-point harmonic measure at 0 is inapplicable. The separately stated absorbing convention h(E)=1 is consistent with a process killed immediately, and its extended inequality is automatic because the bound never exceeds 1/2. This extension must not be presented as a hypothesis-free instance of the classical theorem.

## Independent sharpness proof for every allowed diameter

For d in [0,2], define theta = asin(d/2) and let A consist of exp(it) for -theta <= t <= theta. This is compact and connected. For any two parameters s,t in this interval,

    |exp(is)-exp(it)| = 2|sin((s-t)/2)| <= 2 sin(theta) = d.

The inequality follows from |s-t|/2 <= theta <= pi/2 and monotonicity of sine on that interval. The endpoint pair attains d, so the diameter is exact. Since A lies on the unit circle, U=D. Rotational invariance, equivalently the Poisson kernel at 0, makes harmonic measure normalized angular length. Hence h(A)=2theta/(2pi)=asin(d/2)/pi.

At d=0 this is a singleton with measure zero. At d=2 this is a semicircle with measure 1/2. A longer circular arc also has diameter 2 but larger harmonic measure, so an unspecified diameter-2 arc is not necessarily an extremizer. The author correctly selects minor arcs and the semicircle and does not claim to classify all equality cases.

## Independent necessity check

The disconnected set E={-1,1} has diameter 2 and lies on the boundary. Its harmonic measure is zero because normalized angular measure assigns zero mass to a finite set. The proposed bound would be 1/2. Connectedness is therefore essential, and this example does not contradict the continuum theorem.

## Evidence and scope of acceptance

The complete local catalog, problem corpus, and review corpus were read and freshly hashed. The unique rank-853 target, statement digest, and complete-problem/complete-review default-JSON digest all match. The inherited matched report describes literature triage rather than a substantive mathematical proof attempt. The author's bounded repository-search history was reviewed but not upgraded to an independent exhaustive search.

The exact original author archive, external bootstrap, external manifest, and author-validation receipt are pinned in `replay_author.py`. The seven extracted members match the original packet. A 46-case matrix (8 positive and 38 negative controls) passed, with that entire matrix rerun under an optimized outer interpreter. Both normal and optimized child executions are covered. Attack fixtures are rejected before packet execution, and original bytes remain unchanged.

The direct in-packet checker is not an authenticated execution gate. Trust begins with the independently pinned external bootstrap. Integrity tests establish the frozen-byte and declared-scope checks, not mathematical truth or protection against a concurrent hostile filesystem writer.

Acceptance remains limited to credited prior-result verification, the independently reasoned interpretation and extremizer checks above, and the recorded source-access limits. No publication was performed by this audit.
