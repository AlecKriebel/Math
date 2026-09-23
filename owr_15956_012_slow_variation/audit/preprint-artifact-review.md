# Parent artifact review — version 1.0.0 baseline

The fresh mathematical reviewer is independent of this engineering check. No mathematical defect is alleged here.

## Worthwhile fixes

1. **Supporting files are hard to locate from the standalone PDF.** The manuscript refers to accompanying scripts and audits but gives no project, source-package or code URL. Add a concise availability paragraph with the public project URL, so a reader of the PDF alone can obtain and run the checks.
2. **The source archive README links to a local upload-kit file that is not included.** The builder can create it, but that step is not stated alongside the link. Point the README download link to the published kit and explain that the local build recreates it. The source archive cannot contain its own outer upload envelope without circularity.

## Checks already passed

- Both baseline archive manifests match every included file.
- The verifier extracted from the source archive passes with Python optimization and reproduces saved results.
- All 14 site/mirror files match, and the website download manifest verifies.
- Version, title, author, ORCID and scope agree across the baseline manuscript, website, citation file and Zenodo metadata.

The lack of PDF title/author metadata is also a small discoverability improvement worth including with these edits. No new theorem or numerical claim is needed. Historical review records should keep their original hashes and version scope.
