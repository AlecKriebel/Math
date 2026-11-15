#!/usr/bin/env python3
"""Ten new bounded changes to actual in-memory HTML/overlay buffers only.
No renderer, native/scientific code, previous campaign, writes or network.
The imported own stage module is inert; only held source/baseline data is read.
"""
import json
import re
import sys
import stage as st
rs=st.records();wb=st.obj(st.A/'WEBSITE_BASELINE.json')
rows={x['path']:x for x in wb['files']}
def old(n):return (st.A/rows[str(st.W/'public'/n)]['blob']).read_bytes()
oldg,_=st.json_script(old('research/index.html').decode());oldnodes=re.findall(r'<url>.*?</url>',old('research/sitemap.xml').decode(),re.S)
base=['research/'+r['root']['future_proposed_slug']+'/' for r in rs]
expected=sorted([n for b,r in zip(base,rs) for n in [b+'index.html',b+'citation.bib']+[b+a['original_api_file_object']['key'] for a in r['ready']['all_native_assets_in_original_order']]]+['research/index.html','research/sitemap.xml'])
buffers={n:(st.A/'candidate-a/public'/n).read_bytes() for n in expected}
def check(v):
 st.need(sorted(v)==expected,'all11 exact paths including native TeX')
 for b,r in zip(base,rs):
  text=v[b+'index.html'].decode();rule=r['root']['future_exact_reader_only_transform_authorized']
  wanted=r['main'].replace('<main>','<main id="main">',1).replace(rule['from'],rule['to'],1)
  st.need(re.findall(r'<main\b[^>]*>.*?</main>',text,re.S)==[wanted],'entire main only exact root changes')
  g,_=st.json_script(text);article=g['@graph'][1]
  st.need(article['abstract']==r['publication']['abstract'],'whole original abstract')
  if not r['publication']['version_field_present']:st.need('version' not in article and 'citation_version' not in text,'no synthesized absent version')
  for a,enc in zip(r['ready']['all_native_assets_in_original_order'],article['encoding']):
   name=a['original_api_file_object']['key'];st.need(v[b+name]==st.source_bytes(a['path']),'whole original native download')
   st.need(enc['contentUrl'].endswith('/'+name) and enc['encodingFormat']==a['whole_original_native_files_entry']['mimetype'],'native encoding actual order/MIME')
   st.need(enc['license']==st.CC,'actual broad CC BY, no invented MIT')
  st.need(v[b+'citation.bib']==r['bib'],'whole original BibTeX')
 g,_=st.json_script(v['research/index.html'].decode());st.need(st.same(g['mainEntity']['itemListElement'][:92],oldg['mainEntity']['itemListElement']),'all92old typed index items')
 st.need(re.findall(r'<url>.*?</url>',v['research/sitemap.xml'].decode(),re.S)[:93]==oldnodes,'all93old whole XMLnodes')
check(buffers);results=[]
def fault(name,fn):
 v=dict(buffers);fn(v);st.need(v!=buffers,'fault actually applied '+name)
 try:check(v)
 except (ValueError,KeyError) as e:results.append({'name':name,'applied':True,'rejected':True,'exception':type(e).__name__,'reason':str(e)});return
 raise ValueError('fault escaped '+name)
def replace(v,target,before,after):
 st.need(before in v[target].decode(),'exact actual mutation anchor');v[target]=v[target].decode().replace(before,after,1).encode()
def graph(v,target,fn):
 t=v[target].decode();g,_=st.json_script(t);fn(g);v[target]=st.replace_script(t,json.dumps(g,ensure_ascii=False)).encode()
p130=base[0]+'index.html';p131=base[1]+'index.html'
fault('130at-least-five-inflated-to-exactly-five',lambda v:replace(v,p130,'an incoming center and at least five outgoing choices','an incoming center and exactly five outgoing choices'))
fault('130absent-version-synthesized',lambda v:graph(v,p130,lambda g:g['@graph'][1].__setitem__('version','1.0')))
fault('130native-standalone-TeX-omitted',lambda v:v.pop(base[0]+'five_centers.tex'))
fault('130unauthorized-reader-transform',lambda v:replace(v,p130,'five_centers.pdf#view=FitH','five_centers.pdf#view=FitV'))
fault('131exact-additivity-replaced-by-lower-bound',lambda v:replace(v,p131,'dim F = dim F₁ + dim F₂','dim F ≥ dim F₁ + dim F₂'))
fault('131artificial-maximum-added',lambda v:replace(v,p131,'No artificial minimum or maximum is adjoined.','An artificial maximum is adjoined.'))
fault('131native-ZIP-PDF-order-reversed',lambda v:graph(v,p131,lambda g:g['@graph'][1]['encoding'].reverse()))
fault('130invented-MIT-encoding-license',lambda v:graph(v,p130,lambda g:g['@graph'][1]['encoding'][2].__setitem__('license','https://opensource.org/license/mit/')))
fault('old92typed-index-record-changed',lambda v:graph(v,'research/index.html',lambda g:g['mainEntity']['itemListElement'][0].__setitem__('name','changed old item')))
fault('old93whole-XMLnode-changed',lambda v:replace(v,'research/sitemap.xml',oldnodes[0],re.sub(r'<lastmod>.*?</lastmod>','<lastmod>1999-01-01</lastmod>',oldnodes[0])))
print(json.dumps({'optimization_level':sys.flags.optimize,'positive_actual_buffers_checked':11,'new_memory_only_faults':results,'fault_count':len(results),'actual_candidate_or_source_writes':False,'renderer_scientific_native_or_old_campaign_execution':False,'network_subprocess_or_writes':False},ensure_ascii=False,indent=2))
