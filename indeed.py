import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f'https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=python&limit={LIMIT}'
# 'https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=python&limit=50'


def get_last_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, 'html.parser')
    pagination = soup.find('div', {'class': 'pagination'})
    links = pagination.find_all('a')

    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))
    max_page = pages[-1]

    return max_page


def extract_job(html):
    title = html.find('h2', {'class': 'title'}).find('a')['title']
    company = html.find('span', {'class': 'company'})
    if company:
        company_anchor = company.find('a')
        if company_anchor is None:
            company = str(company.string)
        else:
            company = str(company_anchor.string)
        company = company.strip()
    else:
        company = None
    location = html.find('div', {'class': 'recJobLoc'})['data-rc-loc']
    job_id = html['data-jk']
    return {
        'title': title,
        'company': company, 
        'location': location, 
        'link': f'https://kr.indeed.com/%EC%B1%84%EC%9A%A9%EB%B3%B4%EA%B8%B0?jk={job_id}'
        }


def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f'indeed{page+1}페이지를 스크래핑 하는 중')
        result = requests.get(f'{URL}&start={page*LIMIT}')
        soup = BeautifulSoup(result.text, 'html.parser')
        results = soup.find_all("div", {'class': 'jobsearch-SerpJobCard'})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs():
    last_page = get_last_pages()
    jobs = extract_indeed_jobs(last_page)
    return jobs

