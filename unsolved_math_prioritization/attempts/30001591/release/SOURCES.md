# Source and scope reconciliation

## Original question

Claudio Muñoz's contribution in **Nonlinear Waves and Dispersive Equations**, Oberwolfach Reports 7 (2010), 2393–2463, places the equality question in Remark 1 on page 2405. The workshop was in September 2010; the report was published on 2 March 2011. The adjacent Theorems 4–6 exclude equality in their conclusions. The printed transmitted amplitude has a negative exponent, 2^(-1/(m-1)); this was visually checked, rather than trusting a search extraction that lost the minus sign. [Official report](https://ems.press/journals/owr/articles/4429), [official PDF](https://ems.press/content/serial-article-files/46300), [DOI](https://doi.org/10.4171/OWR/2010/41).

## Precise theorem setting and endpoint gap

The detailed author manuscript **Dynamics of soliton-like solutions for slowly varying, generalized gKdV equations: refraction vs. reflection**, arXiv:1009.4905v1, supplies the precise setting: a is C^3, 1<a<2, a'>0; a approaches its end values exponentially; derivatives of orders 1–3 decay exponentially; and |(a^(1/m))'''|<=K(a^(1/m))'. Epsilon is sufficiently small for each fixed lambda. Equations (1.23), (2.19), (3.1) identify the threshold and reduced system. Remark 1.13 describes a prospective almost-bound-state behavior without proving it. Remark 3.3 identifies the endpoint escape-time failure. The reduced ODE in PARTIAL_RESULTS.md is taken from this model; its critical infinite-incoming normalization and the stated deductions are proved there. [Versioned manuscript](https://arxiv.org/abs/1009.4905v1), [journal record, SIAM J. Math. Anal. 44 (2012), 1–60](https://doi.org/10.1137/100809763).

## Later credited result

Muñoz's **Inelastic character of solitons of slowly varying gKdV equations**, arXiv:1107.5328v1, Theorem 1.4 and Remark 1.3, gives quantitative outgoing-defect lower bounds for fixed positive lambda different from the threshold. Equality is explicitly excluded. The inspected publisher abstract confirms that restriction in the published article, Communications in Mathematical Physics 314 (2012), 817–852. The author's later inelastic result is therefore not a solution of this target. [Versioned manuscript](https://arxiv.org/abs/1107.5328v1), [publisher record](https://link.springer.com/article/10.1007/s00220-012-1463-6).

## Bounded current search and inspection limits

Searches on 7 October 2026 included exact title/parameter combinations and “gKdV borderline potential”, “Muñoz critical refraction”, and “slowly varying gKdV threshold”. A 2026 Chile conference program was also inspected: its related presentations concern Boussinesq, water-wave, or NLS models and do not supply this gKdV endpoint result. [Program](https://eventos.cmm.uchile.cl/asympstab2026/program/).

No resolution was located in this bounded search. This is not proof of global openness or exhaustive coverage. The two complete author manuscripts and the official OWR PDF were downloaded and inspected. The final SIAM/CMP journal full texts were not inspected; their publisher records/abstracts were. The theorem-scope conclusions above distinguish those levels of inspection. The OWR download initially timed out and succeeded on retry. Web screenshot calls failed; local PDF rendering succeeded for OWR page 2405 and the 2010 manuscript page 8.

## Dependencies of the partials

The algebraic/ODE and stationary-state arguments are proved directly. The cubic compactness and energy-matching claims assume the conservation/monotonicity identities stated in their hypotheses; their extension from smooth decaying solutions to the actual H^1 flow is an external PDE input, not re-proved. The signed-integral arguments require additional integral control explicitly stated in Section 4. No PDE approximation theorem at the critical parameter is assumed or claimed.
