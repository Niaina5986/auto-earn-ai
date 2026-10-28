import re
from config import MIN_SCORE
POS={'paid':10,'bounty':16,'reward':10,'salary':10,'stipend':12,'microtask':8,'annotation':6,'bug bounty':12,'open source':5,'documentation':5,'testing':5,'remote':3,'python':3,'ai evaluation':7,'data labeling':6,'translation':4,'transcription':4,'crypto testnet':5}
RISK={'deposit required':'upfront payment','pay to apply':'upfront payment','guaranteed profit':'unrealistic profit promise','double your money':'unrealistic profit promise','seed phrase':'wallet credential risk','private key':'wallet credential risk','send crypto':'crypto transfer risk','investment required':'capital required','pyramid scheme':'pyramid-scheme indicator','captcha bypass':'policy bypass'}
def analyze_opportunity(x):
 text=(x.get('title','')+' '+x.get('description','')+' '+x.get('reward_text','')).lower(); score=15
 for word,points in POS.items():
  if word in text:score+=points
 if re.search(r'(\$|usd|eur|€)\s?\d+',text):score+=8
 if any(w in text for w in ('worldwide','anywhere','global','international')):score+=4
 if len(x.get('description',''))<60:score-=5
 risks=[v for k,v in RISK.items() if k in text]
 if risks:score-=30*len(risks)
 if not x.get('url','').startswith('http'):score-=10
 x['score']=round(max(0,min(100,score)),1);x['risk']='high' if risks else ('medium' if x.get('source')=='github' else 'low/unknown');x['risk_reasons']=risks
 x['recommended']=x['score']>=MIN_SCORE and not risks;x['analysis_note']='Heuristic only; verify eligibility, payout, country support and terms.'
 return x
def analyze_opportunities(items):return sorted((analyze_opportunity(x) for x in items),key=lambda x:x['score'],reverse=True)
