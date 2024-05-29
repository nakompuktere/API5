import requests
import os
from dotenv import load_dotenv


def predict_rub_salary_sJ(vacancy):
    if vacancy["payment_from"] and vacancy["payment_to"]:
        return int((vacancy["payment_from"] + vacancy["payment_to"])/2)
    elif vacancy["payment_from"]:
        return int(vacancy["payment_from"] * 0.8)
    else:
        return int(vacancy["payment_to"] * 1.2) 


def get_sj_statistic():
    load_dotenv()
    sj_secret_key = os.getenv("SJ_SECRET_KEY")
    languages = ["python", "JavaScript", "Ruby", "Java", "PHP", "C++", "C#", "C"]
    url = "https://api.superjob.ru/2.0/vacancies/"
    vacancies_sj = { }

    for language in languages:
        vacancies_processed_sj = 0
        average_vacancy_salary = 0
        for page in range(5):

            headers = {
                "X-Api-App-Id": sj_secret_key
            }

            payload = {
            "count": 100,
            "keyword": language,
            "catalogues": 48,
            "town": "Moscow",
            "page": page
            }

            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()

            for vacancy in response.json()["objects"]:
                if vacancy["currency"] == "rub":
                    average_vacancy_salary += predict_rub_salary_sJ(vacancy)
                    vacancies_processed_sj += 1
                
            if vacancies_processed_sj:
                average_salary_sj = int(average_vacancy_salary/vacancies_processed_sj)
            else:
                average_salary_sj = 0
                
            vacancies_sj[language] = {
            "average_salary": average_salary_sj,
            "vacancies_found": response.json()["total"], 
            "vacancies_processed": vacancies_processed_sj
            }
        
    return vacancies_sj