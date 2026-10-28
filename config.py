import os
from pathlib import Path
ROOT=Path(__file__).resolve().parent
for d in ('products','workspace','reports','data'):(ROOT/d).mkdir(exist_ok=True)
DB_PATH=ROOT/'data'/'auto_earn.sqlite3'
USER_AGENT=os.getenv('AUTO_EARN_USER_AGENT','AutoEarnAIUltra/1.0 public-feed-client')
TIMEOUT=int(os.getenv('REQUEST_TIMEOUT','20'))
MAX_ITEMS=int(os.getenv('MAX_ITEMS_PER_SOURCE','1000'))
GITHUB_TOKEN=os.getenv('GITHUB_TOKEN','')
ENABLE_JOBS=os.getenv('ENABLE_PUBLIC_JOB_FEEDS','1')=='1'
ENABLE_GITHUB=os.getenv('ENABLE_GITHUB_SEARCH','1')=='1'
ENABLE_CRYPTO=os.getenv('ENABLE_CRYPTO_MARKET_DATA','1')=='1'
ENABLE_EXECUTION=os.getenv('ENABLE_EXECUTION','1')=='1'
MIN_SCORE=float(os.getenv('MIN_OPPORTUNITY_SCORE','45'))
SEARCH_TERMS=['paid microtask','remote data annotation','AI evaluation task','bug bounty','open source bounty','paid documentation','paid programming task','agent gig','crypto testnet rewards','web3 bug bounty','paid usability study','data labeling','translation task','transcription task','QA testing task','Python automation task','paid research task','software testing bounty']
