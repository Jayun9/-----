import requests

indeed_result = requests.get('https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=python&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius=25&l=%EB%8C%80%EC%A0%84&fromage=any&limit=50&sort=&psf=advsrch&from=advancedsearch')

print(indeed_result)
