"""Public citation indexes are discovery aids, never mathematical proof evidence."""
import datetime, json, pathlib, urllib.request
ROOT=pathlib.Path(__file__).resolve().parent
QUERIES={
 "openalex_exact_doi":"https://api.openalex.org/works/https://doi.org/10.4418/2022.77.1.8",
 "openalex_title_search":"https://api.openalex.org/works?search=The%20Geometry%20of%20Discotopes&per-page=25",
 "semantic_scholar_exact_doi":"https://api.semanticscholar.org/graph/v1/paper/DOI:10.4418/2022.77.1.8?fields=title,year,authors,citationCount,citations.title,citations.year,citations.externalIds,citations.url,references.title,references.year,references.externalIds",
 "crossref_exact_doi":"https://api.crossref.org/works/10.4418/2022.77.1.8",
}
if __name__=="__main__":
 results=[]
 for key,url in QUERIES.items():
  item={"query":key,"url":url,"retrieved_at_utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
  try:
   with urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Public scholarly literature priority audit"}),timeout=35) as response:
    data=json.load(response)
   (ROOT/(key+".json")).write_text(json.dumps(data,indent=2)+"\n")
   item.update(status="retrieved",filename=key+".json")
   if key=="openalex_exact_doi":
    citing_url="https://api.openalex.org/works?filter=cites:"+data["id"].split("/")[-1]+"&per-page=200"
    with urllib.request.urlopen(citing_url,timeout=35) as response: citations=json.load(response)
    (ROOT/"openalex_citing_works.json").write_text(json.dumps(citations,indent=2)+"\n")
    item["citing_url"]=citing_url
    item["citing_works"]=[{"title":w["title"],"doi":w["doi"],"year":w["publication_year"],"id":w["id"]} for w in citations["results"]]
   if key=="semantic_scholar_exact_doi": item["citing_works"]=data.get("citations")
  except Exception as error: item.update(status="failed",error=str(error))
  results.append(item)
 (ROOT/"citation_index_manifest.json").write_text(json.dumps(results,indent=2)+"\n")
 print(json.dumps(results,indent=2))
