#!/usr/bin/env python3
"""Owned, bounded offline renderer for this one private editorial packet."""
from pathlib import Path
import hashlib
import html
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent.parent / "sources"


def load(path):
    raw = path.read_bytes()
    return json.loads(raw), {"path": str(path), "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest()}


def render():
    model, model_pin = load(HERE / "PAGE_MODEL.json")
    record, record_pin = load(SOURCE / "record.response.body")
    ready, ready_pin = load(SOURCE / "SOURCE_READY.json")
    if model["record_id"] != 23204591 or record["id"] != 23204591:
        raise ValueError("Unexpected record")
    if any(model[k] is not None for k in ("canonical_url", "base_url", "AA", "follow_up")) or model["private_preview"] is not True:
        raise ValueError("Private-preview authority boundary changed")
    meta = record["metadata"]
    if meta["version"] != "1.0.0" or meta["publication_date"] != "2026-10-06" or meta["license"] != {"id": "cc-by-4.0"}:
        raise ValueError("Native edition or rights changed")
    title = html.escape(meta["title"])
    doi = record["doi_url"]
    source_body = (HERE / "ARTICLE_BODY.html").read_bytes()
    body = source_body.decode("utf-8")
    native_description = html.unescape(meta["description"])
    files = []
    (HERE / "assets").mkdir(exist_ok=True)
    expected_order = ["README.md", "verification-supplement.zip", "source.zip", "paper.pdf"]
    if [r["original_api_file_object"]["key"] for r in ready["all_native_assets_in_original_order"]] != expected_order:
        raise ValueError("Native file order changed")
    for entry in ready["all_native_assets_in_original_order"]:
        native = entry["original_api_file_object"]
        raw = Path(entry["path"]).read_bytes()
        if len(raw) != entry["bytes"] or hashlib.sha256(raw).hexdigest() != entry["SHA256"]:
            raise ValueError("Original asset mismatch")
        if "md5:" + hashlib.md5(raw).hexdigest() != native["checksum"]:
            raise ValueError("Native checksum mismatch")
        (HERE / "assets" / native["key"]).write_bytes(raw)
        files.append({"key": native["key"], "bytes": len(raw), "sha256": hashlib.sha256(raw).hexdigest(), "url": native["links"]["self"]})
    links = " | ".join(f'<a href="{html.escape(row["url"], quote=True)}">{html.escape(row["key"])}</a>' for row in files)
    bib = "@misc{kriebel2026bilinearergodichilbert,\n  author = {Kriebel, Alec},\n  title = {" + meta["title"] + "},\n  year = {2026},\n  month = oct,\n  version = {1.0.0},\n  publisher = {Zenodo},\n  doi = {10.5281/zenodo.23204591},\n  url = {https://doi.org/10.5281/zenodo.23204591},\n  note = {Preprint; published October 6, 2026}\n}\n"
    (HERE / "citation.bib").write_text(bib, encoding="utf-8")
    main = f'''<main id="main">
<nav aria-label="Site"><a href="/">Alec Kriebel</a> · <a href="/research/">Research</a></nav>
<article>
<header><h1>{title}</h1>
<p class="byline"><a rel="author" href="https://orcid.org/0009-0001-9320-500X">Alec Kriebel · ORCID</a><br>Published <time datetime="2026-10-06">October 6, 2026</time> · Zenodo version 1.0.0 · Preprint</p>
</header>
<section aria-labelledby="paper"><h2 id="paper">Read the paper</h2>
<p><a href="assets/paper.pdf#view=FitH">Open the original PDF</a> · <a href="assets/paper.pdf" download="Kriebel-2026-bilinear-ergodic-Hilbert-variation.pdf">Download PDF</a> · <a href="{doi}">Zenodo DOI: 10.5281/zenodo.23204591</a></p>
<p class="files">Original Zenodo files: {links}</p>
<iframe title="Original published paper, five pages" src="assets/paper.pdf#view=FitH" loading="lazy"></iframe>
<p class="small">The PDF is an unchanged copy of the published Zenodo file. The printed paper is dated October 6, 2026 and carries no printed version label; 1.0.0 is the Zenodo version.</p>
</section>
<section aria-labelledby="abstract"><h2 id="abstract">Abstract</h2><p id="printed-abstract">{model["abstract_html"]}</p></section>
{body}
<section aria-labelledby="record-description"><h2 id="record-description">Zenodo record description</h2><p id="native-description">{html.escape(native_description)}</p></section>
<section aria-labelledby="citation"><h2 id="citation">Citation</h2>
<p>Alec Kriebel. <cite>{title}</cite>. Version 1.0.0, Zenodo, October 6, 2026. Preprint. <a href="{doi}">doi:10.5281/zenodo.23204591</a>.</p>
<p><a href="citation.bib" download>Download BibTeX</a></p><pre><code>{html.escape(bib)}</code></pre>
</section>
<footer><p class="small">The original note, code and accompanying original verification materials are licensed under <a rel="license" href="https://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International</a>. Cited third-party works retain their own rights.</p></footer>
</article>
</main>'''
    scholarly = {"@context": "https://schema.org", "@type": "ScholarlyArticle", "@id": doi, "name": meta["title"], "headline": meta["title"], "author": {"@type": "Person", "name": "Alec Kriebel", "identifier": "https://orcid.org/0009-0001-9320-500X"}, "datePublished": meta["publication_date"], "version": meta["version"], "identifier": {"@type": "PropertyValue", "propertyID": "DOI", "value": record["doi"]}, "description": model["abstract_text"], "creativeWorkStatus": "Preprint", "license": "https://creativecommons.org/licenses/by/4.0/", "isBasedOn": model["upstream_url"], "encoding": {"@type": "MediaObject", "encodingFormat": "application/pdf", "contentUrl": files[3]["url"]}, "keywords": meta["keywords"]}
    style = """body{margin:0;background:#fff;color:#202020;font:18px/1.65 Arial,Helvetica,sans-serif}main{max-width:850px;margin:0 auto;padding:32px 24px 64px}nav{font-size:16px;margin-bottom:36px}h1{font-size:34px;line-height:1.22;font-weight:600;margin:0 0 18px}h2{font-size:25px;line-height:1.3;margin:38px 0 14px}p{margin:0 0 18px}a{color:#145db0;text-underline-offset:3px}a:focus-visible{outline:2px solid #145db0;outline-offset:3px}.byline,.small,.files{font-size:16px;color:#4b4b4b}.byline{line-height:1.55;margin-bottom:26px}iframe{display:block;width:100%;height:480px;border:1px solid #d1d1d1;margin:22px 0 16px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f6f6f6;border:1px solid #ddd;padding:16px;font-size:14px;line-height:1.55}code{font-size:.9em;overflow-wrap:anywhere}li{margin-bottom:12px}.equation{overflow-wrap:anywhere;padding:12px 0;font-family:Arial,Helvetica,sans-serif}footer{border-top:1px solid #ddd;margin-top:38px;padding-top:22px}@media(max-width:600px){body{font-size:17px}main{padding:22px 18px 44px}h1{font-size:28px}h2{font-size:23px}iframe{height:400px}nav{margin-bottom:28px}}"""
    citation_meta = {"citation_title": meta["title"], "citation_author": "Kriebel, Alec", "citation_publication_date": "2026/10/06", "citation_doi": record["doi"], "citation_pdf_url": files[3]["url"], "citation_version": meta["version"]}
    head = "\n".join(f'<meta name="{k}" content="{html.escape(v, quote=True)}">' for k, v in citation_meta.items())
    doc = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(model["page_title"])}</title><meta name="description" content="{html.escape(model["meta_description"], quote=True)}">
<meta name="robots" content="noindex,nofollow"><meta name="referrer" content="no-referrer">
{head}
<script type="application/ld+json">{json.dumps(scholarly, ensure_ascii=False).replace('<', chr(92)+'u003c')}</script><style>{style}</style></head><body>{main}</body></html>'''
    (HERE / "public-main.html").write_text(main + "\n", encoding="utf-8")
    (HERE / "preview.html").write_text(doc + "\n", encoding="utf-8")
    (HERE / "METADATA.json").write_text(json.dumps({"canonical_url": None, "base_url": None, "AA": None, "proposed_slug": model["proposed_slug"], "follow_up": None, "private_preview": True, "native_publication_date": meta["publication_date"], "native_created_UTC": record["created"], "native_version_field_present": "version" in meta, "native_version": meta["version"], "printed_version": None, "printed_date": model["printed_date"], "full_printed_abstract": model["abstract_text"], "whole_native_description_original": meta["description"], "scholarly": scholarly, "citation_meta": citation_meta, "native_files_in_original_order": files, "source_inputs": [model_pin, record_pin, ready_pin, {"path": str(HERE / "ARTICLE_BODY.html"), "bytes": len(source_body), "sha256": hashlib.sha256(source_body).hexdigest()}], "scientific_authority": "verification/root-clearance-23204591-20261115.json", "production_authority": False}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PRIVATE_PREVIEW_RENDERED", "assets": files, "source_program_executions": 0, "network_requests": 0}, indent=2))


if __name__ == "__main__":
    render()
