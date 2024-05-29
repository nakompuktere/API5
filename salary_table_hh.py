import requests
from itertools import count
import os
from tools import predict_rub_salary


def get_hh_statistic():
    url = "https://api.hh.ru/vacancies"
    languages = ["python", "JavaScript", "Ruby", "Java", "PHP", "C++", "C#", "C"]
    hh_statistic = { }

    for language in languages:
        total_salary = 0
        vacancies_processed = 0
        for page in count(0, 1):
            payload = {
                "page": page,
                "area": 1,
                "text": f"Программист {language}",
                "per_page": 100,
                "only_with_salary": "true"
            }
            response = requests.get(url, params=payload)
            response.raise_for_status()
            if page >= response.json()["pages"] - 1:
                break

            for vacancy in response.json()["items"]:
                vacancy_salary = vacancy["salary"]
                if vacancy_salary["currency"] == "RUR":
                    total_salary += predict_rub_salary(vacancy_salary["from"], vacancy_salary["to"])
                    vacancies_processed += 1
                
            average_salary = int(total_salary/vacancies_processed)
                
            hh_statistic[language] = {
                "average_salary": average_salary,
                "vacancies_found": response.json()["found"], 
                "vacancies_processed": vacancies_processed
            }
    return hh_statistic