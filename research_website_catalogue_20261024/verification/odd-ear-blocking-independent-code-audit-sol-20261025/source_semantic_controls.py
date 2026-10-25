"""Literal new-helper and independently parsed HTML controls; no fixture writes."""
from pathlib import Path
from copy import deepcopy
from html import escape
import json, sys
from independent_semantics import P, STAGE, IDS, inspect_html
sys.dont_write_bytecode=True
sys.path[:0]=[str(STAGE),str(P/'scripts')]
from odd_ear_blocking_source import validate_oeb_assets, odd_ear_blocking_source_view

observations=[]
def check(name, fn, reason=None):
    try:fn()
    except ValueError as e:
        if reason is None or str(e)!=reason:raise
        observations.append({'control':name,'outcome':'rejected','exact_reason':str(e)});return
    if reason is not None:raise ValueError('control accepted:'+name)
    observations.append({'control':name,'outcome':'accepted'})

for rid in IDS:
    paper=P/'papers'/rid;c=json.loads((paper/'publication.json').read_text());g=json.loads((paper/'promotion.json').read_text())
    raw=json.loads((paper/'sources/SOURCE_READY.json').read_text());api=json.loads((paper/'sources/record.raw.json').read_text())
    check(rid+':source_view_pristine',lambda:odd_ear_blocking_source_view(paper,c,g))
    check(rid+':literal_assets_pristine',lambda:validate_oeb_assets(paper,rid,raw,api))
    a,b=deepcopy(raw),deepcopy(api);a['all_assets'].reverse();b['files'].reverse()
    check(rid+':whole_API_agrees_but_native_order_wrong',lambda:validate_oeb_assets(paper,rid,a,b),'odd_ear_blocking:exact_record_specific_asset_order')
    a=deepcopy(raw);a['files']=deepcopy(a['all_assets'])
    check(rid+':invented_files_alias',lambda:validate_oeb_assets(paper,rid,a,api),'odd_ear_blocking:no_source_aliases')
    a,b=deepcopy(raw),deepcopy(api);a['all_assets'][0]['bytes']=float(a['all_assets'][0]['bytes']);a['all_assets'][0]['original_api_file_object']['size']=float(a['all_assets'][0]['original_api_file_object']['size']);b['files'][0]['size']=float(b['files'][0]['size'])
    check(rid+':numeric_equality_with_float_sizes',lambda:validate_oeb_assets(paper,rid,a,b),'odd_ear_blocking:integer_asset_sizes')
    a=deepcopy(raw);a['all_assets'][0]['sha256']=a['all_assets'][0]['sha256'].upper()
    check(rid+':upper_case_native_SHA',lambda:validate_oeb_assets(paper,rid,a,api),'odd_ear_blocking:native_lowercase_hashes')
    wrong=deepcopy(g);wrong['reviews']['analytic']['verdict']['audit_invented_qualification']=True
    check(rid+':whole_custom_verdict_mutation',lambda:odd_ear_blocking_source_view(paper,c,wrong),'odd_ear_blocking:whole_passed_objects_equal_actual_types')
    html=(STAGE/'public/research'/c['slug']/'index.html').read_text()
    check(rid+':own_HTML_pristine',lambda:inspect_html(rid,html))
    mutations=[('title',html.replace('<h1><a href="/research/'+c['slug']+'/">','<h1><a href="/research/">',1),'title_resolves_to_own_article'),
               ('Research',html.replace('<a href="/research/">Research</a>','<a href="/research/'+c['slug']+'/">Research</a>',1),'Research_resolves_to_index'),
               ('hidden',html.replace('<main id="main"><article>','<main id="main"><article hidden>',1),'body_has_no_hidden_content'),
               ('comment_priority',html.replace('<p>'+escape(c['limitations'][-1])+'</p>','<!--'+escape(c['limitations'][-1])+'-->',1),'complete_ordered_limits')]
    for name,mutant,reason in mutations:
        if mutant==html:raise ValueError('unapplied fault:'+name)
        check(rid+':own_HTML_'+name,lambda m=mutant:inspect_html(rid,m),reason)

print(json.dumps({'mode':'optimized' if sys.flags.optimize else 'normal','observations':observations,'total':len(observations),'pristine':sum(x['outcome']=='accepted' for x in observations),'rejected':sum(x['outcome']=='rejected' for x in observations),'source_or_stage_bytes_written':False},indent=2))
