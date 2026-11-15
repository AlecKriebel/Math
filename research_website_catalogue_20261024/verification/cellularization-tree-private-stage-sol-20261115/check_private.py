"""Read-only two-target output contracts, independent of renderer functions."""
from pathlib import Path
import argparse
import html
import json
import re
import xml.etree.ElementTree as ET
from stage_model import HERE, Frozen, load_records, output_paths, require, same, digest, validate_record, verify_live_baseline
from stage_dom import ClosedDocument


def check_page(raw, r, build_date):
    text = raw.decode(); p = r["pub"]; url = p["proposed_canonical_url"]
    dom = ClosedDocument().finish(text)
    require(dom.title == p["title"] + " | Alec Kriebel", "exact full title")
    actual_main = re.findall(r'<main id="main">.*?</main>', text, re.S)
    require(actual_main == [r["main"]], "entire adopted main tree with only declared changes")
    names = {}; properties = {}; charset = []
    for m in dom.metas:
        if 'charset' in m: charset.append(m)
        else:
            group, key = (names, 'name') if 'name' in m else (properties, 'property')
            require(set(m) == {key, 'content'} and m[key] not in group, "unambiguous metadata")
            group[m[key]] = m['content']
    expected_names = {"viewport": "width=device-width, initial-scale=1", "description": p["description"], "author": p["author"], "robots": "index,follow",
        "citation_title": p["title"], "citation_author": p["author"], "citation_author_orcid": p["orcid"], "citation_publication_date": "2026/10/17",
        "citation_version": p["version"], "citation_doi": p["doi"], "citation_pdf_url": url + "assets/" + p["pdf_filename"], "citation_language": "en", "twitter:card": "summary"}
    require(charset == [{"charset": "utf-8"}] and names == expected_names, "complete citation/SEO/original date/version metadata")
    require(properties == {"og:type": "article", "og:title": p["title"], "og:description": p["description"], "og:url": url, "og:site_name": "Alec Kriebel"}, "complete OG")
    require(dom.link_elements == [{"rel": "canonical", "href": url}, {"rel": "icon", "href": "/favicon.ico"}, {"rel": "stylesheet", "href": "/research/research.css"}], "proposed canonical and only installed CSS/favicon")
    require(len(dom.scripts) == 1, "single JSON-LD only")
    graph = json.loads(dom.scripts[0])
    require(set(graph) == {"@context", "@graph"} and graph['@context'] == 'https://schema.org' and len(graph['@graph']) == 2, "closed structured graph")
    webpage, article = graph['@graph']
    require(webpage == {"@type": "WebPage", "@id": url + '#page', "url": url, "name": p['title'], "dateModified": build_date, "mainEntity": {"@id": url + '#article'}}, "WebPage build date separate from original paper date")
    expected_article = {"@type": "ScholarlyArticle", "@id": url + '#article', "url": url, "headline": p['title'], "name": p['title'], "description": p['description'], "abstract": p['abstract'],
        "author": {"@type": "Person", "name": p['author'], "sameAs": p['orcid']}, "datePublished": '2026-10-17', "version": p['version'], "creativeWorkStatus": 'Unrefereed preprint',
        "identifier": {"@type": "PropertyValue", "propertyID": 'DOI', "value": p['doi']}, "sameAs": 'https://doi.org/' + p['doi'], "license": p['license_url'], "keywords": p['keywords']}
    enc = article.get('encoding'); without = {k: v for k, v in article.items() if k != 'encoding'}
    require(without == expected_article, "whole original abstract and scholarly identity")
    native_assets = r['ready']['all_native_assets_in_original_order']
    expected_enc = []
    for a, mime in zip(native_assets, ('application/zip', 'application/pdf')):
        native = a['original_api_file_object']
        expected_enc.append({'@type': 'MediaObject', 'encodingFormat': mime, 'contentUrl': url + 'assets/' + native['key'], 'sameAs': native['links']['self'], 'license': p['license_url']})
    require(same(enc, expected_enc), "original ZIP then PDF encodings and actual source/license")
    frames = [a for t, a in dom.attrs if t == 'iframe']
    frame = frames[0]
    require(frame['src'] == 'assets/' + p['pdf_filename'] + '#view=FitH' and ('four-page' if p['pdf_pages'] == 4 else 'three-page') in frame['title'], "complete actual PDF reader")
    for filename in (p['pdf_filename'], p['supplement_filename'], 'citation.bib'):
        require(any(a.get('href') == 'assets/' + filename and 'download' in a for a in dom.links), "local unchanged download with disposition: " + filename)
    # Exact main bytes above protect every abstract/math/status/collaboration/background/rights sentence.
    # This independent wrapper reconstruction also disallows extra hidden or competing content outside it.
    e = lambda v: html.escape(str(v), quote=True)
    native = ' · '.join('<a href="' + e(a['original_api_file_object']['links']['self']) + '">' + e(a['original_api_file_object']['key']) + '</a>' for a in native_assets)
    prefix = '<body>\n<a class="skip-link" href="#main">Skip to content</a>\n<header>\n<p class="site-title"><a href="/">Alec Kriebel</a></p>\n<nav aria-label="Main navigation"><a href="/research/">Research</a> | <a href="/blog/">Blog</a> | <a href="' + e(p['orcid']) + '">ORCID</a></nav>\n<p>Original Zenodo files: ' + native + '</p>\n</header>\n'
    suffix = '\n<footer>\n<hr>\n<p><a href="/research/">Research home</a></p>\n<p class="copyright">© 2013–' + build_date[:4] + ' Kriebel LLC.</p>\n</footer>\n</body>\n</html>\n'
    require(text[text.index('<body>'):] == prefix + r['main'] + suffix, "exact existing-style visible navigation/body/footer")
    return {"record_id": r['id'], "complete_main_bytes": len(r['main'].encode()), "PDF_pages": p['pdf_pages'], "closed_visible_DOM": True,
        "full_abstract_and_all_main_prose_preserved": True, "iframe_rawtext_empty": True, "native_asset_order": ['ZIP', 'PDF'], "license": p['license']}


def check_index(raw, records):
    text = raw.decode(); old = (HERE / 'baseline/research/index.html').read_text()
    pattern = r'(<script type="application/ld\+json">\s*)(.*?)(\s*</script>)'
    matches = list(re.finditer(pattern, text, re.S)); oldm = re.search(pattern, old, re.S)
    require(len(matches) == 1, "single index JSON-LD")
    m = matches[0]; obj = json.loads(m.group(2)); oldobj = json.loads(oldm.group(2)); li = obj['mainEntity']
    require(li['numberOfItems'] == len(li['itemListElement']) == 87, "index87")
    require(same(li['itemListElement'][:85], oldobj['mainEntity']['itemListElement']), "all85 old ItemList objects/types/order unchanged")
    tail = li['itemListElement'][85:]
    require(tail == [{'@type': 'ListItem', 'position': 86 + i, 'url': r['pub']['proposed_canonical_url'], 'name': r['pub']['title']} for i, r in enumerate(records)], "exact two appended ItemList objects")
    del li['itemListElement'][85:]; li['numberOfItems'] = 85
    require(same(obj, oldobj), "all other index JSON fields unchanged")
    restored = text[:m.start(2)] + oldm.group(2) + text[m.end(2):]
    for r in records:
        p = r['pub']; path = '/research/' + p['slug'] + '/'
        # Identify and validate the whole new visible row independently of builder helpers.
        candidates = re.findall(r'      <li><a href="' + re.escape(path) + r'">.*?</li>\n', restored, re.S)
        require(len(candidates) == 1, "one appended visible index row")
        row = candidates[0]
        e = lambda value: html.escape(str(value), quote=True)
        expected_row = '      <li><a href="' + path + '">' + e(p['title']) + '</a><br><span class="entry-meta">17 October 2026 · Unrefereed preprint</span><p>' + e(p['description']) + '</p><p><a href="' + path + 'assets/' + e(p['pdf_filename']) + '">PDF</a> · <a href="https://doi.org/' + e(p['doi']) + '">Zenodo</a></p></li>\n'
        require(row == expected_row, "complete visible new index row; no hiding wrappers or attributes")
        require(html.unescape(re.search(r'">(.*?)</a>', row).group(1)) == p['title'], "index full title")
        require('<span class="entry-meta">17 October 2026 · Unrefereed preprint</span>' in row, "original publication date/status in index")
        require('<p>' + html.escape(p['description'], quote=True) + '</p>' in row, "index exact description")
        require('href="' + path + 'assets/' + p['pdf_filename'] + '"' in row and 'href="https://doi.org/' + p['doi'] + '"' in row, "index PDF/native DOI")
        restored = restored.replace(row, '', 1)
    require(restored == old, "all old85 visible entries and every other old index byte unchanged")
    require(text.count('<li>') == old.count('<li>') + 2, "exact two visible entry additions")
    return True


def check_sitemap(raw, records, build_date):
    text = raw.decode(); old = (HERE / 'baseline/research/sitemap.xml').read_text(); ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    root = ET.fromstring(raw); previous = ET.fromstring(old)
    loc = [u.find('s:loc', ns).text for u in root]; oldloc = [u.find('s:loc', ns).text for u in previous]
    require(len(loc) == 88 and len(oldloc) == 86 and loc[:86] == oldloc and loc[86:] == [r['pub']['proposed_canonical_url'] for r in records], "old86 sitemap plus exacttwo")
    for r in records:
        node = '  <url><loc>' + r['pub']['proposed_canonical_url'] + '</loc><lastmod>' + build_date + '</lastmod></url>\n'
        require(text.count(node) == 1, "one dated sitemap addition"); text = text.replace(node, '', 1)
    require(text == old, "all old sitemap bytes unchanged")
    return True


def read_tree(root):
    root = Path(root); require(root.is_dir() and not root.is_symlink(), "actual private output root")
    result = {}
    for p in root.rglob('*'):
        require(not p.is_symlink(), "no output symlink")
        if p.is_file(): result[str(p.relative_to(root))] = p.read_bytes()
    return result


def check_outputs(out, records, frozen, build_date):
    require(set(out) == output_paths(records), "exact ten-path overlay fence")
    results = []
    for r in records:
        validate_record(r, frozen); p = r['pub']; prefix = 'research/' + p['slug'] + '/'
        results.append(check_page(out[prefix + 'index.html'], r, build_date))
        for a in r['ready']['all_native_assets_in_original_order']:
            rel = prefix + 'assets/' + a['original_api_file_object']['key']
            require(out[rel] == frozen.read(a['path']), "complete unchanged native asset: " + rel)
        require(out[prefix + 'assets/citation.bib'] == r['bib'], "unchanged prepared BibTeX")
    check_index(out['research/index.html'], records); check_sitemap(out['research/sitemap.xml'], records, build_date)
    base = json.loads((HERE / 'FRESH_BASELINE.json').read_text()); oldpaths = {r['path'] for r in base['public_files']}
    require(len(oldpaths | set(out)) == 593 and oldpaths & set(out) == {'research/index.html', 'research/sitemap.xml'}, "hypothetical593 namespace; only old aggregate paths replaced")
    return {"status": "QUALIFIED_PRIVATE_INTEGRATION_PASS", "records": results, "overlay_files": len(out), "hypothetical_public_files": 593, "hypothetical_index": 87, "hypothetical_sitemap": 88, "publication_or_live_claim": False}


def main():
    ap = argparse.ArgumentParser(description=__doc__); ap.add_argument('--output-root', required=True); ap.add_argument('--build-date', required=True); ap.add_argument('--check-live-baseline', action='store_true')
    args = ap.parse_args(); frozen = Frozen(); frozen.verify_all(); records = load_records(frozen)
    result = check_outputs(read_tree(args.output_root), records, frozen, args.build_date)
    if args.check_live_baseline: result['actual_baseline_fence'] = verify_live_baseline()
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
