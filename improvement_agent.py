import json,time
from config import ROOT
from database import add_improvement
VERSION='1.0.0'
def propose_improvements(summary):
 ps=[]
 if summary.get('sources_failed'):ps.append('Add exponential backoff and source-health monitoring.')
 if not summary.get('opportunities_found'):ps.append('Inspect feed schema changes and add permitted public feeds.')
 if summary.get('products_created'):ps.append('Add product tests, better design, and marketplace-specific packaging.')
 if not ps:ps.append('Collect more run evidence before changing scoring weights.')
 for p in ps:add_improvement(p,summary)
 out=ROOT/'reports'/'improvement_proposals.json';out.write_text(json.dumps({'version':VERSION,'next_candidate':'1.0.1','created_at':int(time.time()),'proposals':ps,'policy':'No self-editing production code; review, test and approve changes.'},indent=2),encoding='utf-8');return ps
