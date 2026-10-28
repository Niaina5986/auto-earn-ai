import json,time
from config import ROOT
def prepare_publication_queue(paths):
 items=[{'path':str(p),'status':'draft_only','checklist':['check originality and licenses','proofread and test','choose marketplace available in your country','configure payout/tax details','publish only after explicit approval']} for p in paths]
 out=ROOT/'reports'/'publication_queue.json';out.write_text(json.dumps({'created_at':int(time.time()),'items':items},indent=2),encoding='utf-8');return str(out)
