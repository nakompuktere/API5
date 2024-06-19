import requests
from tools import predict_rub_salary
from itertools import count


def get_sj_statistic(sj_secret_key):
    languages = ["python", "JavaScript", "Ruby", "Java", "PHP", "C++", "C#", "C"]
    url = "https://api.superjob.ru/2.0/vacancies/"
    vacancies_sj = { }
    specialization_id = 48
    number_of_results = 100

    for language in languages:
        vacancies_processed_sj = 0
        vacancy_salary_sum = 0
        for page in count(0, 1):

            headers = {
                "X-Api-App-Id": sj_secret_key
            }

            payload = {
                "count": number_of_results,
                "keyword": language,
                "catalogues": specialization_id,
                "town": "Moscow",
                "page": page
            }

            response = requests.get(url, headers=headers, params=payload)
            response.raise_for_status()
            super_job_results = response.json()
            vacancies = super_job_results["objects"]
            total_vacancies = super_job_results["total"]
            for vacancy in vacancies:
                if (vacancy["payment_from"] or vacancy["payment_to"]) and vacancy["currency"] == "rub":
                    if  vacancy["payment_from"] != 0 or vacancy["payment_to"] != 0:
                        vacancy_salary_sum += predict_rub_salary(vacancy["payment_from"], vacancy["payment_to"])
                        vacancies_processed_sj += 1
            if not super_job_results["more"]:
                break

        if vacancies_processed_sj:
            average_salary_sj = int(vacancy_salary_sum/vacancies_processed_sj)
        else:
            average_salary_sj = 0
                
        vacancies_sj[language] = {
            "average_salary": average_salary_sj,
            "vacancies_found": total_vacancies, 
            "vacancies_processed": vacancies_processed_sj
        }
        
    return vacancies_sj