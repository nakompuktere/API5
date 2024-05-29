def predict_rub_salary(vacancy_salary_from, vacancy_salary_to):
    if vacancy_salary_from and vacancy_salary_to:
        return int((vacancy_salary_from + vacancy_salary_to)/2)
    elif vacancy_salary_to:
        return int(vacancy_salary_to * 0.8)
    else:
        return int(vacancy_salary_from * 1.2)