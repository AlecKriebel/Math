"""Explicit private ten-path builder. Importing this module performs no work."""
from pathlib import Path
import argparse
import datetime
import html
import json
import re
from stage_model import HERE, Frozen, load_records, output_paths, require


def esc(value):
    return html.escape(str(value), quote=True)


def date_arg(value):
    require(datetime.date.fromisoformat(value).isoformat() == value, "explicit ISO build date")
    return value


def page(r, build_date):
    p = r["pub"]; url = p["proposed_canonical_url"]
    assets = r["ready"]["all_native_assets_in_original_order"]
    pdf_url = url + "assets/" + p["pdf_filename"]
    article = {"@type": "ScholarlyArticle", "@id": url + "#article", "url": url,
        "headline": p["title"], "name": p["title"], "description": p["description"], "abstract": p["abstract"],
        "author": {"@type": "Person", "name": p["author"], "sameAs": p["orcid"]},
        "datePublished": p["publication_date"], "version": p["version"], "creativeWorkStatus": "Unrefereed preprint",
        "identifier": {"@type": "PropertyValue", "propertyID": "DOI", "value": p["doi"]},
        "sameAs": "https://doi.org/" + p["doi"], "license": p["license_url"], "keywords": p["keywords"],
        "encoding": [{"@type": "MediaObject", "encodingFormat": "application/zip" if i == 0 else "application/pdf",
            "contentUrl": url + "assets/" + a["original_api_file_object"]["key"],
            "sameAs": a["original_api_file_object"]["links"]["self"], "license": p["license_url"]} for i, a in enumerate(assets)]}
    graph = {"@context": "https://schema.org", "@graph": [
        {"@type": "WebPage", "@id": url + "#page", "url": url, "name": p["title"], "dateModified": build_date,
         "mainEntity": {"@id": url + "#article"}}, article]}
    meta = [("description", p["description"]), ("author", p["author"]), ("robots", "index,follow"),
        ("citation_title", p["title"]), ("citation_author", p["author"]), ("citation_author_orcid", p["orcid"]),
        ("citation_publication_date", p["publication_date"].replace("-", "/")), ("citation_version", p["version"]),
        ("citation_doi", p["doi"]), ("citation_pdf_url", pdf_url), ("citation_language", "en"), ("twitter:card", "summary")]
    head = ['<!DOCTYPE html>', '<html lang="en">', '<head>', '  <meta charset="utf-8">',
        '  <meta name="viewport" content="width=device-width, initial-scale=1">',
        '  <title>' + esc(p["title"]) + ' | Alec Kriebel</title>']
    head += ['  <meta name="' + k + '" content="' + esc(v) + '">' for k, v in meta]
    head += ['  <link rel="canonical" href="' + esc(url) + '">', '  <link rel="icon" href="/favicon.ico">',
        '  <link rel="stylesheet" href="/research/research.css">']
    head += ['  <meta property="' + k + '" content="' + esc(v) + '">' for k, v in (
        ("og:type", "article"), ("og:title", p["title"]), ("og:description", p["description"]), ("og:url", url), ("og:site_name", "Alec Kriebel"))]
    head += ['  <script type="application/ld+json">' + json.dumps(graph, ensure_ascii=False).replace("</", "<\\/") + '</script>', '</head>']
    native = ' · '.join('<a href="' + esc(a["original_api_file_object"]["links"]["self"]) + '">' + esc(a["original_api_file_object"]["key"]) + '</a>' for a in assets)
    body = '<body>\n<a class="skip-link" href="#main">Skip to content</a>\n<header>\n<p class="site-title"><a href="/">Alec Kriebel</a></p>\n<nav aria-label="Main navigation"><a href="/research/">Research</a> | <a href="/blog/">Blog</a> | <a href="' + esc(p["orcid"]) + '">ORCID</a></nav>\n<p>Original Zenodo files: ' + native + '</p>\n</header>\n'
    footer = '\n<footer>\n<hr>\n<p><a href="/research/">Research home</a></p>\n<p class="copyright">© 2013–' + build_date[:4] + ' Kriebel LLC.</p>\n</footer>\n</body>\n</html>\n'
    return ('\n'.join(head) + '\n' + body + r["main"] + footer).encode()


def aggregate_index(records):
    text = (HERE / "baseline/research/index.html").read_text()
    pattern = r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)'
    m = re.search(pattern, text, re.S); require(m is not None, "index single JSON-LD")
    original = m.group(2); obj = json.loads(original)
    require(json.dumps(obj, ensure_ascii=False) == original, "index original JSON serialization retained")
    listing = obj["mainEntity"]; require(listing["numberOfItems"] == len(listing["itemListElement"]) == 85, "old85 index")
    rows = []
    for r in records:
        p = r["pub"]; listing["itemListElement"].append({"@type": "ListItem", "position": len(listing["itemListElement"]) + 1, "url": p["proposed_canonical_url"], "name": p["title"]})
        path = "/research/" + p["slug"] + "/"
        rows.append('      <li><a href="' + path + '">' + esc(p["title"]) + '</a><br><span class="entry-meta">17 October 2026 · Unrefereed preprint</span><p>' + esc(p["description"]) + '</p><p><a href="' + path + 'assets/' + esc(p["pdf_filename"]) + '">PDF</a> · <a href="https://doi.org/' + esc(p["doi"]) + '">Zenodo</a></p></li>\n')
    listing["numberOfItems"] = 87
    text = text[:m.start(2)] + json.dumps(obj, ensure_ascii=False) + text[m.end(2):]
    require(text.count('    </ul>') == 1, "unique visible collection insertion point")
    return text.replace('    </ul>', ''.join(rows) + '    </ul>', 1).encode()


def aggregate_sitemap(records, build_date):
    old = (HERE / "baseline/research/sitemap.xml").read_text()
    require(old.count('</urlset>') == 1, "single old sitemap root")
    nodes = ''.join('  <url><loc>' + r["pub"]["proposed_canonical_url"] + '</loc><lastmod>' + build_date + '</lastmod></url>\n' for r in records)
    return old.replace('</urlset>', nodes + '</urlset>', 1).encode()


def build_bytes(records, frozen, build_date):
    date_arg(build_date)
    out = {"research/index.html": aggregate_index(records), "research/sitemap.xml": aggregate_sitemap(records, build_date)}
    for r in records:
        p = r["pub"]; prefix = "research/" + p["slug"] + "/"
        out[prefix + "index.html"] = page(r, build_date)
        for a in r["ready"]["all_native_assets_in_original_order"]:
            out[prefix + "assets/" + a["original_api_file_object"]["key"]] = frozen.read(a["path"])
        out[prefix + "assets/citation.bib"] = r["bib"]
    require(set(out) == output_paths(records), "exact ten output paths")
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument('--output-root', required=True); ap.add_argument('--build-date', required=True)
    args = ap.parse_args(); output = Path(args.output_root).resolve()
    require(HERE.resolve() in output.parents and output != HERE.resolve(), "output must be a new owned private descendant")
    require(not output.exists(), "independent build output must not already exist")
    frozen = Frozen(); frozen.verify_all(); records = load_records(frozen)
    data = build_bytes(records, frozen, args.build_date)
    for rel, raw in data.items():
        path = output / rel; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(raw)
    print(json.dumps({"status": "PRIVATE_BUILD_ONLY", "output_root": str(output), "build_date": args.build_date, "files": len(data)}, indent=2))


if __name__ == '__main__':
    main()
