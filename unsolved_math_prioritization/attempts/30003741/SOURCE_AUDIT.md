# Source, literature and prior-attempt audit

Checked 2026-09-30 UTC.

## Exact original and network

The complete [OWR 8/2018 report](https://ems.press/content/serial-article-files/46732) was retrieved. Rendall's complete contribution, *Initiation of T cell signalling*, printed pp.487–489, was read; the question and its context on p.488 were rendered and visually checked. The official publisher dates the volume 2018 and its online publication 5 January 2019, explaining the different dates in the imported citation.

The contribution points to François et al.'s model and Rendall–Sontag's analysis. The complete [2017 published paper](https://www.sontaglab.org/FTPDIR/2017_rendall_sontag_tcells_royal_open_reprint.pdf) was retrieved from Sontag's site. The exact equations, rate positivity, conservation laws and feasible region are in Section 2, pp.3–4. The equilibrium total reduction and the explicit agonist-only restriction are in Section 3, pp.5–6. Theorem 3.1 on p.7 proves uniqueness for one or two sites and the sharp three-state result for three sites. The subsequent p.8 paragraph leaves larger N open and gives the earlier degree bounds.

The OWR prose uses a single ligand amount L, a single unbinding rate and the single-ligand response formula. It does not explicitly repeat every restriction at the final open-question sentence. We therefore retain the agonist-only scope for the attempted theorem and leave a clear interpretation qualification. We do not claim that introducing an antagonist answers that narrower question.

The full two-ligand system has separate ligand pools and dissociation rates. The reduced model used here removes the antagonist variables entirely. Its physical positivity includes every remaining receptor state, active and inactive phosphatase, and free ligand/receptor. Steady bound receptor total is not itself a conserved quantity. No requirement of stability is stated by the count question, and the new certificate does not classify it.

## Current literature and the external candidate

[Bali–Rendall's recent comparative study](https://pmc.ncbi.nlm.nih.gov/articles/PMC12722356/) was inspected for its discussion of negative feedback and multiple steady states. Its “Validation of previous findings” paragraph cites the 2017 three-state result and reports numerical validation. It does not provide a new proof in the inspected text of a universal three-state bound for all N. The exact scope of the cited theorem must remain attached to that summary.

A current search also found [*Exactly five positive steady states in a two-ligand T-cell activation model*](https://evidencepress.org/releases/tcell-exactly-five/), dated 20 September 2026, with a linked public repository [ipitchford/tcell-exactly-five](https://github.com/ipitchford/tcell-exactly-five) and DOI 10.5281/zenodo.22861212. The announcement explicitly identifies itself as an unrefereed candidate, takes N=100 and two ligand species, and excludes an agonist-only resolution, stability and physiological relevance. The announcement was read; the complete external proof and executable certificate were not independently audited or used here.

This source is relevant prior research, not a prior Alec repository attempt and not campaign novelty. Its two-ligand count must neither be silently transferred to the single-ligand target nor described as externally peer-reviewed. The current attempt does not contest or certify it.

The bounded search did not locate a complete resolution of the agonist-only higher-N question. That is a search result, not an exhaustive literature claim. Novelty of the even-N coefficient bound and explicit four-site witness is unconfirmed.

## Prior-attempt and duplicate gate

After fetching remote main at c6975ca76f9f667f1250ba403d0e6da2aafe14d0, row 158 was queued with 0/5. Exact-ID and attempt-path Git history, campaign state, reset/history and assessment ledgers, related-target groups, branch names and all-state GitHub PR searches showed no earlier attempt for 30003741. No matching T-cell activation research folder was found in the remote tree.

The full pinned dataset has one record with this code and statement; no ambiguous report join or identical target was found. No keyed imported research report was present. The imported August 2026 literature assessment is a triage statement, not a proof.

Repository instructions, README, queue and policy were read. Actual model: GPT-6 Astra at xhigh reasoning. Two substantive routes were used; no queue generator or shared status file was changed. The numerical exploration was bounded at 240 parameter triples and is explicitly not a root-count certificate.

## Attribution and access

Dataset: *UnsolvedMath: A Curated Collection of Open Mathematics Problems*, UnsolvedMath Contributors (2026), [ulamai/UnsolvedMath](https://huggingface.co/datasets/ulamai/UnsolvedMath), revision 37e53eabe540fb458758e198be61634bd02ee008; curation and metadata [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/).

The initial unsolvedmath landing-page request and DOI redirects were unavailable through the web tool. Official EMS and author-hosted full PDFs supplied the source instead. Primary PDFs and rendered pages remain outside the publication folder. The original model, equilibrium-total mechanism and previously proved small-N cases remain credited to their authors.
