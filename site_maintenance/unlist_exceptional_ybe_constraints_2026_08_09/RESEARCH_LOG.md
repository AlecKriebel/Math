# Research log: exceptional YBE constraints page visibility

## 2026-08-09

- Started from the latest fetched `origin/main` commit `8ec8b1b0` in the
  dedicated clean site-maintenance worktree.
- Located the public homepage card, its paper-page and PDF links, the
  paper's self-referential citation link, and its sitemap entry.
- Removed the homepage card and self-referential anchor while preserving the
  route, PDF, canonical metadata, structured metadata, and sitemap entry.
- Updated the sitemap modification date for the changed page.
- Verified across all published HTML that no anchor resolves to the paper
  page; also validated sitemap XML, JSON-LD, canonical metadata, indexability,
  retained route artifacts, and patch whitespace.
