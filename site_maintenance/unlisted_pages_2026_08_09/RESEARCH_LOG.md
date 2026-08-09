# Research log: unlisted GitHub Pages routes

## 2026-08-09 10:31 PDT

- Started from commit `43ee9f7a` on the fetched `origin/main` history in a dedicated clean worktree because the existing `main` worktree contains unrelated uncommitted research.
- Recorded the 13 requested paper and workstream routes as sitemap-only destinations.
- Removed their homepage cards and all HTML anchors targeting those routes, including cross-page navigation, related-paper links, structured-data relationships, and self-referential citation links.
- Preserved each target page, its own canonical and scholarly metadata, and its entry in `docs/sitemap.xml` so search engines can continue to discover and index it.
- Initial audit result: zero target-route anchors across `docs/**/*.html`; all 13 target routes remain in the sitemap.

## 2026-08-09 10:35 PDT

- Validated all 35 public HTML files: every JSON-LD block parses and resolving every anchor against its source URL finds no cross-page link to any requested target route.
- Validated that each of the 13 target pages has its own canonical URL, has no `noindex` directive, and appears exactly once in the valid XML sitemap.
- Updated sitemap modification dates for every public page changed by this cleanup.
- Rendered the revised homepage locally and confirmed the remaining eight paper cards and one linked research program have a clean layout with no browser console errors.
- `git diff --check` passed.
