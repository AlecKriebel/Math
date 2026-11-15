"""New owned exact10 writer from frozen approved sources and freshly captured623 buffers.
Writes only paired private candidates; never source helpers, website, Git or deployment.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import html
import json
import re
import verify_stage as V

O = Path(__file__).resolve().parent


def article_page(publication, candidate, main, scholarly):
    V.need(candidate.count(main) == 1, 'whole approved MAIN occurs exactly once')
    head, ending = candidate.split(main)
    old_graph = re.findall(rb'<script type="application/ld\+json">(.*?)</script>', head, re.S)
    V.need(len(old_graph) == 1, 'one original scholarly graph')
    V.same(json.loads(old_graph[0]), scholarly)
    url = publication['proposed_canonical_url']
    V.need(url == 'https://aleckriebel.com/research/' + publication['slug'] + '/', 'root-approved slug only')
    graph = json.loads(old_graph[0]); graph['url'] = url
    graph['mainEntityOfPage'] = {'@type':'WebPage','@id':url}
    head = head.replace(old_graph[0], json.dumps(graph,ensure_ascii=False).encode(), 1)
    V.need(head.count(b'noindex,nofollow,noarchive') == 1, 'one original private robots field')
    head = head.replace(b'noindex,nofollow,noarchive',b'index,follow',1)
    e = html.escape
    metadata = '<link rel="canonical" href="' + e(url,quote=True) + '"><link rel="icon" href="/favicon.ico">'
    for key,value in [('og:type','article'),('og:title',publication['title']),('og:description',publication['description']),
                      ('og:url',url),('og:site_name','Alec Kriebel'),('article:published_time',publication['publication_date'])]:
        metadata += '<meta property="' + key + '" content="' + e(value,quote=True) + '">'
    for key,value in [('twitter:card','summary'),('twitter:title',publication['title']),('twitter:description',publication['description'])]:
        metadata += '<meta name="' + key + '" content="' + e(value,quote=True) + '">'
    V.need(head.count(b'</head>') == 1, 'one complete original head')
    head = head.replace(b'</head>',metadata.encode()+b'</head>',1)
    page = head + main + ending
    V.need(page.count(main) == 1, 'entire original body and FitH reader unchanged')
    return page


def aggregate_pages(publications, baseline):
    def baseline_body(suffix):
        row = next(r for r in baseline['files'] if r['path'].endswith('/public/' + suffix))
        return V.pin(O / row['blob'],row)
    old_index = baseline_body('research/index.html')
    pattern = rb'<script type="application/ld\+json">\s*(.*?)\s*</script>'
    matches = re.findall(pattern,old_index,re.S); V.need(len(matches) == 1, 'actual whole current index graph')
    raw = matches[0]; graph = json.loads(raw); listing = graph['mainEntity']
    V.need(listing['numberOfItems'] == len(listing['itemListElement']) == 94
           and raw.endswith(b']}}') and raw.count(b'"numberOfItems": 94') == 1, 'actual stable94 graph interface')
    additions = [{'@type':'ListItem','position':95+i,'url':p['proposed_canonical_url'],'name':p['title']}
                 for i,p in enumerate(publications)]
    V.need(not ({r['url'] for r in listing['itemListElement']} & {p['proposed_canonical_url'] for p in publications}),
           'both actual new index targets absent')
    new_raw = raw.replace(b'"numberOfItems": 94',b'"numberOfItems": 96',1)
    new_raw = new_raw[:-3] + b', ' + b', '.join(json.dumps(p,ensure_ascii=False).encode() for p in additions) + b']}}'
    index = old_index.replace(raw,new_raw,1)
    V.need(index.count(b'    </ul>') == 1, 'actual sole paper-list closing marker')
    index = index.replace(b'    </ul>',b''.join(V.index_card(p) for p in publications)+b'    </ul>',1)
    old_xml = baseline_body('research/sitemap.xml')
    V.need(old_xml.count(b'</urlset>') == 1, 'actual sole sitemap closing marker')
    added = ''.join('  <url><loc>' + p['proposed_canonical_url'] + '</loc><lastmod>2026-11-15</lastmod></url>\n'
                    for p in publications).encode()
    xml = old_xml.replace(b'</urlset>',added+b'</urlset>',1)
    return {'research/index.html':index,'research/sitemap.xml':xml}


def render():
    inputs = V.source_fences(); baseline = V.baseline_fences()
    rows = {r['path']:r for r in inputs['files']}
    def cached(path):
        row = rows[str(path)]; return V.pin(O / row['blob'],row)
    output = {}; publications = []
    for item in inputs['records']:
        editorial = V.P / 'papers' / item['record_id'] / 'reviews/editorial'
        publication = json.loads(cached(editorial / 'publication.json')); publications.append(publication)
        prefix = 'research/' + publication['slug'] + '/'
        output[prefix+'index.html'] = article_page(publication,cached(editorial / 'candidate/index.html'),
            cached(editorial / 'PUBLIC_MAIN.html'),json.loads(cached(editorial / 'SCHOLARLY_METADATA.json')))
        output[prefix+'citation.bib'] = cached(editorial / 'citation.bib')
        for asset in publication['native_assets_in_original_order']:
            name = asset['original_api_file_object']['key']
            V.need('/' not in name and '\\' not in name, 'article-root native asset filename')
            output[prefix+name] = cached(Path(asset['path']))
    output.update(aggregate_pages(publications,baseline))
    expected = sorted(V.obj(O / 'ADAPTER_REQUIREMENTS.json')['eight_article_root_leaves'] + ['research/index.html','research/sitemap.xml'])
    V.need(sorted(output) == expected and len(output) == 10, 'exact8 new leaves and2 aggregates')
    return output


def main():
    V.need(sys.argv[1:] in [['normal'],['optimized']], 'explicit new private authoring mode')
    V.need(not (O / 'FINAL_SEAL.json').exists(), 'immutable final packet cannot be reauthored')
    mode = sys.argv[1]; destination = O / ('candidate-a' if mode == 'normal' else 'candidate-b') / 'public'
    V.need(not destination.parent.exists(), 'fresh owned candidate namespace only')
    output = render()
    for name,body in output.items():
        path = destination / name; path.parent.mkdir(parents=True,exist_ok=True); path.write_bytes(body)
    print(json.dumps({'status':'PRIVATE_EXACT10_AUTHORING_COMPLETE_NO_PRODUCTION_AUTHORITY','mode':mode,
                      'optimization_level':sys.flags.optimize,'files':
                      [{'path':n,'bytes':len(b),'SHA256':V.sha(b)} for n,b in sorted(output.items())],
                      'actual_baseline':[623,94,95],'proposed_counts':[631,96,97],
                      'whole_MAIN_transforms':0,'source_native_science_or_old_renderer_execution':False,
                      'production_authority':False,'canonical_url':None,'AA':None},indent=2))

if __name__ == '__main__':
    main()
