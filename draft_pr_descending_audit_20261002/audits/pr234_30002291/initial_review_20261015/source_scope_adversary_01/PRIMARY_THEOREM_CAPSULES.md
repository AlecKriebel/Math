# Controlling primary theorem facts

The mathematical statements below are source paraphrases, not claims of novelty. Each source capsule is deliberately short; deductions are in REPORT.md. The downloaded PDFs and whole extracted texts are private and excluded by .gitignore.

## Basse-O'Connor–Heinrich–Podolskij (BHP), arXiv1604.02307v2

Source facts (under 200 words): PDF pp.2–6, especially Theorem1.2(i), specifies
$X_t=\int_{-\infty}^t[g(t-s)-g_0(-s)]\sigma_{s-}dL_s$.
$L$ is symmetric, pure-jump, two-sided Lévy relative to the filtration; $\sigma$ is adapted càdlàg. Independence is not required. Existence is assumed.
At $p=2,k=1$, (A) means $g(t)\sim c_0t^\alpha$, $g\in C^1(0,\infty)$,
$\exists\theta\in(0,2]:\limsup_{r\to\infty}r^\theta\nu(|x|\ge r)<\infty$,
$g-g_0\in L^\theta\cap L^\infty$,
$|g'(t)|\le Ct^{\alpha-1}$ near zero, and $|g'|\in L^\theta(\delta,\infty)$ decreasing there.
For $H_s=g'(-s)\sigma_s1_{s\le-\delta}$, (B1) requires
$\exists\rho\in(0,1\wedge\theta],\beta'>\beta,\beta'\ge2:
E\int_\mathbb R(|H_s|^\rho\vee|H_s|^{\beta'})ds<\infty$;
if $\theta=1$, choose $\rho<1$.
With $\beta<2$ and $0<\alpha<1/2$, the conclusion is original-$\mathcal F$-stable $M_1$ convergence
\[
n^{2\alpha}V(2;1)^n_t\Rightarrow c_0^2\sum_{T_m\le t}|\sigma_{T_m-}\Delta L_{T_m}|^2\sum_{l=0}^\infty h_1(l+U_m)^2,
\quad h_1(x)=x_+^\alpha-(x-1)_+^\alpha.
\]
Uniform marks are independent of the original $\mathcal F$. Remark1.4 rejects $J_1$ and $J_2$ in general.

Primary link: https://arxiv.org/pdf/1604.02307v2 . All five controlling pages were locally rendered and visually inspected.

## Basse-O'Connor–Lachièze-Rey–Podolskij (BLP), AOP2017

Source facts (under 200 words): The published article is *Power variation for a class of stationary increments Lévy driven moving averages*, AOP45(6B),4477–4528, DOI10.1214/16-AOP1170; the arXiv1506.06679 title differs. Published pp.4478–4480 impose the symmetric pure-jump two-sided Lévy model with $\sigma\equiv1$. At $k=1$, (A) is the condition above. Additionally (A-log), $\int_\delta^\infty |g'(s)|^\theta\log(1/|g'(s)|)ds<\infty$, is required when $\theta=1$. Theorem1.1(i), $p=2,k=1$, assumes $\beta<2$, $0<\alpha<1/2$ and proves the displayed marked-jump law at terminal time1 with $\sigma=1$. The natural filtration is denoted bold $\mathbb F$; theorem stability concerns the original calligraphic $\mathcal F$, as the downloaded arXiv definition in §3 confirms. Those objects must not be conflated. The published first-order statement was cross-checked via the author's institution final PDF. Local arXiv pp.2–4 were rendered and visually inspected; the final PDF's direct download/render returned403.

Primary links: https://arxiv.org/pdf/1506.06679 and https://pure.au.dk/portal/files/120886195/euclid.aop.1513069265.pdf .
