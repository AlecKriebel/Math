#!/usr/bin/env python3
"""New, bounded source-only editorial renderer. No scientific execution/imports.

Only --render writes the four named candidate leaves and editorial interfaces
inside this new namespace. No website, Git, Sheet or network access.
"""
from pathlib import Path
import hashlib
import html
import json
import shutil
import sys

A = Path(__file__).resolve().parent


def load(name):
    return json.loads((A / name).read_bytes())


def dump(name, obj):
    p = A / name
    if p.exists():
        raise ValueError("new output required: " + name)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def text_file(name, text):
    p = A / name
    if p.exists():
        raise ValueError("new output required: " + name)
    p.write_text(text)


def render():
    c = load("public-sections.json")
    protocol = load("SOURCE_PROTOCOL_BINDINGS.json")
    ready = protocol["whole_original_source_ready"]
    authority = protocol["whole_literal_root_authority"]
    if not authority["editorial_preparation_authorized"] or authority["site_install_deploy_browser_canonical_AA_authorized"]:
        raise ValueError("exact source-only authority required")
    if ready["version"] != "1.0" or ready["record_id"] != 23418581:
        raise ValueError("native identity")
    slug = "simple-young-nonprojective-injectives"
    bib = """@misc{kriebel2026simpleyoung,
  author = {Kriebel, Alec},
  title = {Simple Young modules with nonprojective polynomial injective hulls},
  year = {2026},
  month = oct,
  day = {16},
  version = {1.0},
  publisher = {Zenodo},
  doi = {10.5281/zenodo.23418581},
  url = {https://doi.org/10.5281/zenodo.23418581},
  note = {Unrefereed preprint}
}
"""
    metadata = {
        "@context": "https://schema.org", "@type": "ScholarlyArticle",
        "name": c["title"], "headline": c["title"], "description": c["description"],
        "abstract": c["abstract"], "author": {"@type": "Person", "name": "Alec Kriebel", "sameAs": "https://orcid.org/0009-0001-9320-500X"},
        "datePublished": "2026-10-16", "version": "1.0", "identifier": "https://doi.org/10.5281/zenodo.23418581",
        "url": "https://doi.org/10.5281/zenodo.23418581", "creativeWorkStatus": "Unrefereed preprint",
        "license": "https://creativecommons.org/licenses/by/4.0/", "inLanguage": "en",
        "encoding": [{"@type": "MediaObject", "encodingFormat": "application/pdf", "contentUrl": "paper.pdf"}, {"@type": "MediaObject", "encodingFormat": "application/zip", "contentUrl": "source-and-verification.zip"}]
    }
    publication = dict(c)
    publication.update({
        "schema": "private_editorial_23418581_v1", "slug": slug,
        "author": "Alec Kriebel", "orcid": "https://orcid.org/0009-0001-9320-500X",
        "abstract_is_original": True, "publication_date": "2026-10-16", "publication_date_label": "16 October 2026",
        "version_field_present": True, "version": "1.0", "printed_version_field_present": True, "printed_version": "1.0", "printed_date": "16 October 2026",
        "native_record_created": ready["created"], "native_record_updated": ready["updated"], "doi": "10.5281/zenodo.23418581",
        "pdf_filename": "paper.pdf", "pdf_pages": 4, "supplement_filename": "source-and-verification.zip", "supplement_label": "Complete original source-and-verification ZIP", "additional_assets": [],
        "license": "CC BY 4.0", "license_url": "https://creativecommons.org/licenses/by/4.0/", "authored_package_license": "CC BY 4.0", "code_license": None,
        "code_license_basis": "Broad original authored-material CC BY4.0; no separate code-specific instrument or MIT default.",
        "status": "Unrefereed preprint", "follow_up": None, "canonical_url": None, "AA": None, "native_sheet_aa_url": None, "proposed_canonical_url": None,
        "production_authority": False, "root_full_copy_config_adoption_pending": True,
        "seo": {"title": c["title"] + " | Alec Kriebel", "description": c["description"], "robots": "noindex,nofollow", "candidate_only": True},
        "keywords": ["Young modules", "Schur algebras", "polynomial representations", "injective modules", "rank truncation", "Miyachi Conjecture 7"],
        "citation_text": "Alec Kriebel. Simple Young modules with nonprojective polynomial injective hulls. Version 1.0. Zenodo, 16 October 2026. doi:10.5281/zenodo.23418581.",
        "prepared_bibtex": bib,
        "source_binding": {"whole_original_source_ready": ready, "whole_native_API_objects": protocol["whole_native_API_objects_in_original_role_order"], "native_asset_order": [x["original_api_file_object"]["key"] for x in ready["all_native_assets_in_original_order"]], "native_deposit_description_HTML_original": protocol["native_description_HTML_original"]},
        "review_metadata": {"root_authority": {"original": protocol["root_authority_original"], "whole_literal_object": authority}, "whole_original_scientific_verdicts": protocol["whole_original_scientific_verdicts"], "private_informed_editorial_role_not_new_science_family": True}
    })
    esc = html.escape
    paragraphs = lambda xs: "\n".join("<p>" + esc(x) + "</p>" for x in xs)
    parts = ['<main id="main-content">', '<article>', '<header>', '<h1>' + esc(c["title"]) + '</h1>', '<p class="byline">Alec Kriebel · <time datetime="2026-10-16">16 October 2026</time> · Version 1.0 · Unrefereed preprint</p>', '<p><a href="https://orcid.org/0009-0001-9320-500X">ORCID</a> · <a href="https://doi.org/10.5281/zenodo.23418581">doi:10.5281/zenodo.23418581</a></p>', '</header>', '<section aria-labelledby="explanation"><h2 id="explanation">The idea</h2>', paragraphs(c["plain_language"]), '</section>', '<section aria-labelledby="abstract"><h2 id="abstract">Original abstract</h2><p>' + esc(c["abstract"]) + '</p></section>']
    for key, heading in [("result", "The result"), ("why_it_works", "Why it works"), ("definitions_and_limits", "Scope and limits"), ("background", "Classical inputs and priority")]:
        parts += ['<section><h2>' + heading + '</h2>', paragraphs(c[key]), '</section>']
    parts += ['<section aria-labelledby="paper"><h2 id="paper">Read the paper</h2><p>' + esc(c["reader_intro"]) + '</p>', '<p class="downloads"><a href="paper.pdf" target="_blank" rel="noopener">Open PDF</a> · <a href="paper.pdf" download>Download PDF</a> · <a href="source-and-verification.zip" download>Source and verification ZIP</a> · <a href="citation.bib" download>BibTeX</a></p>', '<iframe class="paper" src="paper.pdf#view=FitH" title="Complete original paper: Simple Young modules with nonprojective polynomial injective hulls" loading="lazy"></iframe>', '<p>If the PDF viewer is unavailable, <a href="paper.pdf">open the original PDF</a>.</p></section>', '<section><h2>Related reading</h2><ul>']
    for item in c["related_resources"]:
        parts.append('<li><a href="' + esc(item["url"], quote=True) + '">' + esc(item["label"]) + '</a>. ' + esc(item["note"]) + '</li>')
    parts += ['</ul></section>', '<section><h2>Status and collaboration</h2><p>' + esc(c["ai_disclosure"]) + '</p><p>' + esc(c["collaboration"]) + '</p><p>' + esc(c["rights_notice"]) + '</p></section>', '<section><h2>Citation</h2><p>' + esc(publication["citation_text"]) + '</p><p><a href="citation.bib" download>Download BibTeX citation</a></p></section>', '</article></main>']
    main = "\n".join(parts) + "\n"
    style = "body{margin:0;background:#fff;color:#202124;font-family:Arial,Helvetica,sans-serif;font-size:17px;line-height:1.65}main{max-width:850px;margin:0 auto;padding:36px 24px 60px}h1{font-size:2.05rem;line-height:1.2;margin:0 0 18px}h2{font-size:1.35rem;line-height:1.35;margin-top:2rem}a{color:#1659a5;text-underline-offset:3px}a:focus-visible{outline:3px solid #1a73e8;outline-offset:3px}.byline{color:#555;font-size:.95rem}.paper{display:block;border:1px solid #ccc;width:100%;height:760px;box-sizing:border-box}li{margin-bottom:12px}.skip{position:absolute;left:-10000px}.skip:focus{left:16px;top:8px;background:white;padding:8px}@media(max-width:600px){main{padding:28px 16px 44px}h1{font-size:1.7rem}.paper{height:560px}}"
    head = '<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>' + esc(publication["seo"]["title"]) + '</title><meta name="description" content="' + esc(c["description"], quote=True) + '"><meta name="author" content="Alec Kriebel"><meta name="citation_title" content="' + esc(c["title"], quote=True) + '"><meta name="citation_author" content="Alec Kriebel"><meta name="citation_publication_date" content="2026/10/16"><meta name="citation_doi" content="10.5281/zenodo.23418581"><meta name="citation_pdf_url" content="https://zenodo.org/records/23418581/files/paper.pdf"><meta name="citation_version" content="1.0"><style>' + style + '</style><script type="application/ld+json">' + json.dumps(metadata, ensure_ascii=False).replace('<', '\\u003c') + '</script></head><body><a class="skip" href="#main-content">Skip to article</a>\n'
    candidate = A / "candidate"
    if candidate.exists():
        raise ValueError("candidate must be newly absent")
    candidate.mkdir()
    for item in ready["all_native_assets_in_original_order"]:
        src = Path(item["path"])
        if hashlib.sha256(src.read_bytes()).hexdigest() != item["SHA256"]:
            raise ValueError("native asset drift")
        shutil.copyfile(src, candidate / item["original_api_file_object"]["key"])
    text_file("PUBLIC_MAIN.html", main)
    text_file("candidate/index.html", head + main + '</body></html>\n')
    text_file("citation.bib", bib)
    text_file("candidate/citation.bib", bib)
    copy = "# " + c["title"] + "\n\n16 October 2026 · Version 1.0 · Unrefereed preprint\n\n"
    for key, heading in [("plain_language", "The idea"), ("abstract", "Original abstract"), ("result", "The result"), ("why_it_works", "Why it works"), ("definitions_and_limits", "Scope and limits"), ("background", "Classical inputs and priority")]:
        values = c[key] if isinstance(c[key], list) else [c[key]]
        copy += "## " + heading + "\n\n" + "\n\n".join(values) + "\n\n"
    copy += "## Status and collaboration\n\n" + c["ai_disclosure"] + "\n\n" + c["collaboration"] + "\n\n" + c["rights_notice"] + "\n\n## Related reading\n\n" + "\n\n".join('[' + x["label"] + '](' + x["url"] + '). ' + x["note"] for x in c["related_resources"]) + "\n"
    text_file("PUBLIC_COPY.md", copy)
    dump("SCHOLARLY_METADATA.json", metadata)
    dump("publication.json", publication)
    dump("promotion.json", {"schema": "source_only_promotion_23418581_v1", "record_id": 23418581, "slug_proposal": slug, "editorial_preparation_authorized": True, "root_full_copy_config_adoption_pending": True, "independent_informed_fact_audit_pending": True, "publication_authority": False, "production_authority": False, "canonical_url": None, "AA": None, "follow_up": None})
    dump("PUBLICATION_REQUIREMENTS.json", {"full_original_abstract": True, "distinct_whole_native_description_retained": True, "complete_original_result": load("INITIAL_EXPECTATIONS.json")["claim"], "all_odd_primes_algebraically_closed_q1": True, "stable_FI_label": True, "simple_dimension_2p_minus2": True, "all_n_at_least2_nonprojective_injective": True, "exact_labelled_truncation_not_arbitrary_projectivity_preservation": True, "p3_equal_dimensions_distinct_labels": True, "broad_Miyachi7_and_stronger_sufficient_family_distinct": True, "classical_credit_and_unresolved_priority": True, "native_printed_version": "1.0", "original_date": "2026-10-16", "native_asset_order": ["source-and-verification.zip", "paper.pdf"], "unchanged_PDF_pages": 4, "archive_containers": 4, "regular_ZIP_occurrences": 243, "embedded_PDFs": 0, "broad_CC_BY_authored_support_code_no_MIT": True, "public_internal_audit_date_count_replay_narrative": False, "passive_contribution_based_collaboration": True, "extensive_AI_unrefereed_status": True, "whole_original_custom_objects_and_historical_flags_preserved": True, "follow_up": None, "production_authority": False, "canonical_url": None, "AA": None})
    dump("SCHEMA_ADAPTER.json", {"schema": "private_native_editorial_adapter_23418581_v1", "source_READY_schema": ready["schema"], "source_protocol": "SOURCE_PROTOCOL_BINDINGS.json", "publication_config": "publication.json", "promotion_config": "promotion.json", "public_main": "PUBLIC_MAIN.html", "public_sections": "public-sections.json", "private_candidate": "candidate/index.html", "actual_interfaces": {"native_API": "publication.source_binding.whole_native_API_objects, original role/key/list/type/null order", "assets": "ZIP then PDF, both article-root relative names unchanged", "root_authority": "publication.review_metadata.root_authority.whole_literal_object", "scientific_verdicts": "publication.review_metadata.whole_original_scientific_verdicts, whole heterogeneous objects", "native_description": "publication.source_binding.native_deposit_description_HTML_original; distinct from full printed abstract", "history": "Original UNREAD/CLOSED fields retained literally; present editorial observations are separate."}, "future_leaf_files": ["index.html", "source-and-verification.zip", "paper.pdf", "citation.bib"], "future_integration_requirements": ["Root full copy/config adoption and separate informed fact audit first.", "Preserve exact complete article main and original relative download names.", "Any production canonical/indexfollow/index/sitemap changes require separate authority and actual new baseline.", "Native/source/root/custom objects, nulls and history remain whole."], "existing_generator_or_core_changed": False, "publication_authority": False, "production_authority": False, "canonical_url": None, "AA": None, "follow_up": None})
    print(json.dumps({"status": "SOURCE_ONLY_EDITORIAL_RENDERED", "candidate_leaves": 4, "PDF_and_ZIP_original_bytes": True, "website_access": False, "scientific_execution": False}))


if __name__ == "__main__":
    if sys.argv[1:] == ["--render"]:
        render()
    elif not sys.argv[1:]:
        print("Source-only renderer. Explicit --render creates the new editorial outputs.")
    else:
        raise SystemExit("Only --render is supported")
