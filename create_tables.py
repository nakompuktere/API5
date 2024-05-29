from terminaltables import AsciiTable
from salary_table_hh import get_hh_statistic
from salary_table_sj import get_sj_statistic


def create_terminaltables(vacancy_statistic, title):
    table_data = [
        ['Язык программирования', 'Вакансий найдено', "Вакансий обработано", "Средняя зарплата"]
    ]
    for language, statistic in vacancy_statistic.items():
        table_data.append([
            language, 
            statistic["vacancies_found"],
            statistic["vacancies_processed"],
            statistic["average_salary"]
        ])
    table = AsciiTable(table_data, title)
    return table.table
    
def main():
    title_hh = "Headhunter Moscow"
    title_sj = "SuperJob Moscow"
    print(create_terminaltables(get_hh_statistic(), title_hh))
    print(create_terminaltables(get_sj_statistic(), title_sj))

if __name__ == "__main__":
    main()