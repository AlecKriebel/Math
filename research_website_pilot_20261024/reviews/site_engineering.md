# Website pilot: initial engineering assessment

Checkpoint: 2026-10-24 22:49 UTC. Initial engineering assessment: **100% complete**. Independent review of the new research pages: **pending implementation**. No site files, hosting state, redirects, or remote repositories were changed by this review.

## Scope and evidence

Read the site's `firebase.json`, `README.md`, and selected files within `public/`. Read the Math repository's existing `docs/` filenames and searched its HTML, Markdown, JSON, and YAML for `spanningforest23575190`, `graph.square`, and `spanning forest`. Did not inspect backups, mail, SSL data, credentials, or Firebase account configuration.

Ten directly fetched live assets matched the local source **byte for byte**: `/`, `/style.css`, `/blog/`, `/robots.txt`, `/404.html` (served as `/404/`), `/apps/`, `/tapball/`, `/coin/`, `/pictures/WebBG.png`, and `/pictures/Logos/NameWhite.png`. These are a representative sample, not a proof that the entire hosting release matches the checkout. The live `/research/` returned HTTP 404.

The `docs/` search had no matches for the selected graph-square/spanning-forest paper, and no corresponding paper filename appeared in the existing inventory. There is therefore no verified old paper landing-page URL to redirect for this pilot. An existing repository-wide research index is not a paper-specific predecessor.

## Hosting and integration

- Firebase serves the `public/` directory with clean URLs and trailing slashes enabled. `public/research/index.html` and `public/research/<paper-slug>/index.html` fit that layout without a rewrite or redirect change.
- The homepage currently links to `https://aleckriebel.github.io/Math/` in two places: the top RESEARCH navigation item and the Math Explorations card. Change both to `/research/` when publishing the intended navigation update. Keep the old GitHub index accessible until the user approves redirect migration.
- The existing global stylesheet uses a full-page background image, fixed-width 400px cards with additional padding, and older 768px wrappers. For readable mathematical content and small-screen support, use research-scoped styling rather than changing those global rules. The blog already uses an independent inline style block, so a dedicated research stylesheet is consistent with the site's existing loose structure.
- Existing Firebase redirects cover only blog tags, categories, authors, and feeds. No redirect rule conflicts with `/research/`.
- The custom 404 document immediately navigates to the homepage with JavaScript. This can hide broken research links during visual testing; test HTTP response codes and local file existence in addition to browser navigation.
- `robots.txt` allows crawling everywhere. Avoid publishing draft placeholders or unverified claims as though they were final findings. A local preview is the simplest review surface before publication.

## Recommended release sequence

1. Add the research index, first paper page, and research-scoped assets under `public/research/`; preserve the current Firebase routing configuration.
2. Preview the completed files locally using the repository's documented Firebase emulator workflow. Verify desktop and narrow-mobile layouts, mathematical readability, heading structure, keyboard focus, meaningful link text, local asset references, paper/source/download links, and canonical URL consistency.
3. Confirm the actual hosting project/site target before any deployment; this review deliberately did not inspect account or target configuration. The README documents `firebase deploy --only hosting`, which publishes the hosting contents and configuration as a whole, so a clean diff and an unchanged-source check matter even for a small addition.
4. Deploy the pilot only within the authorization provided to the parent task, then check live HTTP status and content for the two new pages, their assets, the homepage, and sampled existing pages.
5. Apply GitHub Pages redirects only after the user's separate review/approval gate. Avoid guessing a paper-specific source URL: none was found for this paper. A future migration should maintain an explicit old-to-new URL map and retain access to PDFs and verification artifacts.

## Concrete risks for final review

- **Scope creep in a full hosting deployment:** unrelated public files or hosting configuration could be released with the pilot. The sampled baseline currently matches live, which reduces but does not eliminate this risk.
- **Misleading success checks:** the site's JavaScript 404 redirect can make broken links look like successful homepage loads.
- **Mobile overflow inherited from legacy CSS:** a 400px card plus padding already exceeds common narrow viewports. Isolate the new layout and check it at roughly 375px width.
- **Premature redirect migration:** a general research index exists, but this paper has no identified predecessor page. Leave migration mappings uncommitted until approved.
- **Claim and artifact mismatch:** the landing page must distinguish the strongest checked result from the original open problem and link the exact reviewed paper/source artifacts. Mathematical review is outside this engineering assessment and remains the parent review's responsibility.

## Sources

- Local: `/Users/alec/Desktop/alec-dev/aleckriebel.com/firebase.json`, `README.md`, `public/index.html`, `public/style.css`, `public/blog/index.html`, `public/404.html`, `public/robots.txt`.
- Live direct comparison: <https://aleckriebel.com/>, <https://aleckriebel.com/blog/>, and the asset paths listed above, fetched at this checkpoint.
- Existing research landing pages: `/Users/alec/Documents/Math/docs/`.
