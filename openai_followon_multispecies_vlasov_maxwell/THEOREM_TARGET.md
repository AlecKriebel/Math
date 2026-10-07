# Exact research target and certification state

Status: **unproved research hypothesis**. Neither upstream release text nor a formalization catalogue is certification.

For a fixed integer N≥1, masses m_a>0, real charges e_a, and speed of light and vacuum permittivity normalized to one, let F_a(t,x,p)≥0 be number densities in physical momentum. Set v=p/m_a and f_a(t,x,v)=m_a^3 F_a(t,x,m_a v). The velocity is u(v)=v/sqrt(1+|v|²). The proposed equations are

∂_t f_a+u·∇_x f_a+(e_a/m_a)(E+u×B)·∇_v f_a=0,
∂_t E−curl B=−Σ_a e_a∫u f_a dv,
∂_t B+curl E=0,
div E=Σ_a e_a∫f_a dv, div B=0.

Candidate initial class: nonnegative f_a,0∈C_c^∞(R⁶), E_0,B_0∈C_b^∞(R³;R³)∩L² satisfying both constraints. This is the upstream candidate class, not yet accepted as sufficient for the follow-on proof. Needed versus convenient field decay will be audited.

Target conclusion: unique global classical solution, smooth on every finite time interval, compact particle phase support there, and both propagated constraints. The intended continuation criterion is bounded max_a momentum support on a finite maximal lifespan; its exact dependency and regularity hypotheses remain to be verified.

First gate: N=2, m_1=m_2=1, e_1=+1, e_2=−1, arbitrary data in the verified class. Full gate: all fixed N,m_a,e_a above. Constants may depend on those fixed parameters and the data/horizon. No uniformity as m_a→0 is claimed.

Required checks: source/receiver pair signed impulse; angular occupation with species-specific acceleration; selected receiver-force coefficient; simultaneous bootstrap over all species; zero charges; coinciding species; one-species reduction; opposite signs; extreme fixed positive mass ratios; energy normalization; Maxwell constraints; neutrality role.

Excluded: massless particles, collisions, noncompact momentum tails, curved spacetime. A two-species result alone does not complete the core target.

Success means a checkable complete proof, pivotal dependencies validated, priority checked on exact statements, independently reviewed exact package, verified production Zenodo publication and DOI tracker entry. Partial algebra or a conditional implication is not success.
