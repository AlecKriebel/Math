# Post-freeze primary correction: independent assessment

This assessment is fixed after the preserved initial adjudication, and before reading ROOT's AFTER_FIRST_PRIOR_BOUND_COMPARISON_20261004.md. The original TARGET_SCOPE_PIN.md and SOURCE_FIRST_ASSESSMENT_FROZEN.md remain unmodified.

I inspected the primary PDF retained at ROOT_priority_20261004/private_sources/process_evidence/matthews2009_pdf/stdout.bin through a new independently captured pdftotext extraction. The PDF banner identifies arXiv:0810.2327v2, 26 Oct 2008; its internal title date is 10 October 2008. Actual reading: header, Section2A uniform-POVM definition/Theorem9 p8, complete Section4 pp17–19 including Eq24 and the paragraph explicitly correcting the earlier 2×n restriction. Other sections were only searched for navigation, not cleared as fully read.

The initial report's dimensional exclusion is wrong. Matthews–Wehner–Winter explicitly justify the locally isotropic/Haar POVMs as LOCC in arbitrary finite bipartite dimensions. Their Eq24 supplies a general lower bound. For a pure ensemble its readily evaluated value is at most 1/(306 ln2), below .005 bits, which does not imply a strict rate above two bits. A small lower bound alone is not a converse and does not exclude the sharper information quantity.

A separate elementary measurement-specific check can bound the sharper information quantity itself without evaluating the W ensemble. For the dimension-d isotropic POVM d|ψ><ψ| dψ, define qρ(ψ)=d<ψ|ρ|ψ> relative to normalized Haar measure. The information for any input ensemble is

I(X:Y)=sum_x p_x D(qρx || 1)-D(qρbar || 1) <= max_ρ D(qρ || 1).

Convexity makes the maximum occur at a pure state. Haar invariance and t=|<ψ|φ>|² with density (d−1)(1−t)^(d−2) give the exact maximum

c_d = [ln d + 1 − H_d]/ln2.

For independent local Haar measurements, the chain rule gives I(X:Y_A,Y_B) <= c_dA+c_dB: first use the bound for the A marginal, then condition on A's outcome and apply the same bound to the resulting B ensemble. This applies to mixed conditional states as well. For the receiver laboratories 4×4, the bound is 2c_4, approximately .8742 bits. If each laboratory instead performs a single Haar measurement on an entire n-copy block, it is 2c_(4^n) < 2(1−γ)/ln2 <1.22 bits per block. This is a bound on this specific isotropic measurement, not a bound on general LOCC accessible information or LOCC capacity. It does not exclude differently structured measurements or a different older coding theorem application.

Consequently the actual corrected local-isotropic measurement instrument does not by itself give the target strict rate. The primary theorem does not state a W4 strict-rate code. The corrected arbitrary-dimension result deserves acknowledgement; the priority gate may retain its bounded pass if other conditions are met. The measurement check is a priority-instrument scope check, not a search for a new central W4 proof.

The Das note is authenticated by publisher-deposited Crossref metadata: DOI10.1103/PhysRevA.92.069903, title “Publisher's Note: Distributed quantum dense coding with two receivers in noisy environments [Phys. Rev. A92,052330 (2015)]”, published online 10 December 2015, by Tamoghna Das, R. Prabhu, Aditi Sen(De), and Ujjwal Sen. APS recent-articles search metadata independently reports the date/title. No legitimate primary body was recovered from APS abstract/PDF/DOI or publisher-harvest routes so far; the failed routes are retained. No inference about its substantive content follows from the note label. This is an explicit version limitation, but neither its title nor available metadata suggests a strict W4 protocol or alteration of the upper-bound nature stated by the original published abstract. It currently supplies no specific material priority obstruction; categorical final-body clearance remains unavailable.

Provisional revised verdict: pass with required attribution and narrow application wording, replacing the erroneous dimensional exclusion with the corrected theorem/measurement comparison. No ROOT comparison conclusions have been read for this assessment.
