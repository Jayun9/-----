import requests
from bs4 import BeautifulSoup

LIMIT = 50
URL = f'https://stackoverflow.com/jobs?q=python'


def extract_pages():
    result = requests.get(URL)
    soup = BeautifulSoup(result.text, "html.parser")
    pages = soup.find('div', {'class': 's-pagination'}).find_all('a')
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    title = html.find('h2').find('a')['title']
    company, location = html.find('h3').find_all('span', recursive=False)
    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = html['data-jobid']
    return {
        'title': title,
        'company': company,
        'location': location,
        'apply_link': f'https://stackoverflow.com/jobs/{job_id}'
    }


def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        print(f'so{page+1}페이지를 스크래핑 하는 중')
        result = requests.get(f'{URL}&pg={page+1}')
        soup = BeautifulSoup(result.text, "html.parser")
        results = soup.find_all('div', {'class': '-job'})
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = extract_pages()
    jobs = extract_jobs(last_page)
    return jobs
