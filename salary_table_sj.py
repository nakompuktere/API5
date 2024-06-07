import requests
from tools import predict_rub_salary


def get_sj_statistic(sj_secret_key):
    languages = ["python", "JavaScript", "Ruby", "Java", "PHP", "C++", "C#", "C"]
    url = "https://api.superjob.ru/2.0/vacancies/"
    vacancies_sj = { }
    specialization_id = 48
    number_of_results = 100

    for language in languages:
        vacancies_processed_sj = 0
        average_vacancy_salary = 0
        for page in range(5):

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
            vacancies = response.json()["objects"]
            total_vacancies = response.json()["total"]
            for vacancy in vacancies:
                if vacancy["currency"] == "rub":
                    average_vacancy_salary += predict_rub_salary(vacancy["payment_from"], vacancy["payment_to"])
                    if average_vacancy_salary > 0:
                        vacancies_processed_sj += 1

            if vacancies_processed_sj:
                average_salary_sj = int(average_vacancy_salary/vacancies_processed_sj)
            else:
                average_salary_sj = 0
                
        vacancies_sj[language] = {
            "average_salary": average_salary_sj,
            "vacancies_found": total_vacancies, 
            "vacancies_processed": vacancies_processed_sj
        }
        
    return vacancies_sj