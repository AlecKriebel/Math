# Literal 2018 v1 smooth-perturbation domain control

This control was added after the independent early seal and after reading the literal [arXiv v1](https://arxiv.org/pdf/1804.03788v1), Section 4, printed pp. 18–21. It audits an old route, without changing the current candidate or asserting the authors' reasons for revision.

Remark 16 and the decomposition (4.2) assert a solution class consisting of a fixed translated peaked profile plus a smooth periodic perturbation. Lemma 10 then invokes smooth Sobolev local evolution with a long lifespan for that perturbation equation. Smoothness of the perturbation does not put the total datum in the domain of the ordinary smooth-data theorem. There is also a concrete obstruction to persistence of that particular decomposition.

Take u0(x)=phi(x)+e sin(x), with e nonzero and small. This is continuous, mean zero, periodic, and belongs to the corner-compatible Banach class. At the unique corner x=0, the two physical slopes are w+(0)=-kappa+e and w-(0)=kappa+e. Thus J(0)=w-(0)-w+(0)=2kappa. The verified characteristic jump identity gives

    J'(0)=-(w-(0)+w+(0))J(0)=-4 kappa e !=0.

A representation u(t,x)=phi(x-a(t))+v(t,x-a(t)), with v smooth and periodic, must align the translated peak with the actual unique corner; otherwise v has a corner at one or both locations. Once aligned, a smooth v adds equal one-sided derivatives, so that representation forces J(t)=2kappa at every time. Its zero derivative contradicts the exact identity above at t=0. Hence the general asserted smooth-perturbation class is not invariant. This is not a counterexample to weaker-norm nonlinear instability; it is a counterexample to a claimed evolution mechanism for its old proof.

The current candidate allows both corner slopes to evolve, and directly constructs total-data evolution in C1 on the cut interval. It therefore avoids this historical domain obstruction. The old route is blocked at this point unless a materially different evolution theorem or mechanism is supplied. No such new proof search is part of this audit.
