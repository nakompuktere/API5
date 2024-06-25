import requests
from itertools import count
import os
from tools import predict_rub_salary


def get_hh_statistic():
    url = "https://api.hh.ru/vacancies"
    languages = ["python", "JavaScript", "Ruby", "Java", "PHP", "C++", "C#", "C"]
    hh_statistic = { }
    town_id = 1
    per_page = 100

    for language in languages:
        total_salary = 0
        vacancies_processed = 0
        for page in count(0, 1):
            payload = {
                "page": page,
                "area": town_id,
                "text": f"Программист {language}",
                "per_page": per_page,
            }
            response = requests.get(url, params=payload)
            response.raise_for_status()
            head_hunter_results = response.json()
            total_pages = head_hunter_results["pages"]
            vacancies = head_hunter_results["items"]
            if page >= total_pages - 1:
                break

            for vacancy in vacancies:
                vacancy_salary = vacancy["salary"]
                if vacancy_salary and vacancy_salary["currency"] == "RUR":
                    if vacancy_salary["from"] or vacancy_salary["to"]:
                        total_salary += predict_rub_salary(vacancy_salary["from"], vacancy_salary["to"])
                        vacancies_processed += 1
        try:
            average_salary = int(total_salary/vacancies_processed)
        except ZeroDivisionError:
            average_salary = 0


        hh_statistic[language] = {
            "average_salary": average_salary,
            "vacancies_found": head_hunter_results["found"], 
            "vacancies_processed": vacancies_processed
        }
    return hh_statistic