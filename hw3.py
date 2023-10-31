from collections import defaultdict


def start():
    '''Just start this program'''
    option = 0
    options = ['1', '2', '3']
    print(
        'Программа может выполнить три команды:\n',
        '1) Вывести иерархию команд, т.е.',
        'департамент и все команды, которые входят в него\n',
        '2) Вывести сводный отчёт по департаментам: название, численность,',
        'вилка зарплат в виде мин – макс, среднюю зарплату\n',
        '3) Сохранить сводный отчёт из предыдущего пункта в виде csv-файла.'
    )
    while option not in options:
        print('Выберите: команда {}, {} или {}'.format(*options))
        option = input()
    if option == '1':
        dep_hierarchy()
    elif option == '2':
        consolidated_report_printer()
    else:
        csv_maker()


def file_opener() -> list:
    '''This hepls to open the file'''
    lines_ar = []
    with open('Corp_Summary.csv', encoding='utf-8') as f:
        read_data = f.readlines()
    for line in read_data:
        lines_ar.append(line.split(';'))
    lines_ar.pop(0)
    return lines_ar


def dep_hierarchy():
    '''You can do department's hierarchy by doing dictionary of sets'''
    file = file_opener()
    dep_ar = {}
    for row in file:
        dep_column = row[1]
        team_column = row[2]
        if dep_column in dep_ar:
            dep_ar[dep_column].add(team_column)
        else:
            dep_ar[dep_column] = set([team_column])
    dep_hierarchy_printer(dep_ar)


def dep_hierarchy_printer(dep_ar: dict):
    '''Print hierarchy of departments in nice way'''
    for dep, team in dep_ar.items():
        print('В отдел {} входят команды: {}'.format(dep, ', '.join(team)))


def consolidated_report_printer():
    '''Just print this report'''
    report_ar = consolidated_report()
    for line in report_ar:
        print('{}: {} человек,'.format(line['dep_name'], line['cnt_workers']),
              'вилка зарплат: {},'.format(line['salary_fork']),
              'средняя - {}'.format(line['avg_salary']))


def consolidated_report() -> list:
    '''Make 2d list of info for second task'''
    file = file_opener()
    dep_ar = defaultdict(list)
    for row in file:
        dep_name = row[1]
        salary = row[5]
        dep_ar[dep_name].append(n_remover(salary))
    dep_ar_new = final_array_maker(dep_ar)
    return dep_ar_new


def n_remover(salary_str: str) -> int:
    '''Put any number with \n and this function change it to integer'''
    salary_int = int(salary_str.rstrip('\n'))
    return salary_int


def count_workers(salaries: list) -> int:
    '''Count indexes in list'''
    return len(salaries)


def salary_fork(salaries: list) -> str:
    '''Make nice string with lowest and highest number in list'''
    fork = '{} - {}'.format(min(salaries), max(salaries))
    return fork


def avg_salary(salaries: list) -> int:
    '''Make average number from list'''
    return round(sum(salaries)/count_workers(salaries))


def final_array_maker(dep_ar: dict) -> list:
    '''Convert dict to list with final metrics'''
    dep_ar_new = []
    for dep_name, dep_sal in dep_ar.items():
        one_dep = {}
        one_dep.update({'dep_name': dep_name})
        one_dep.update({'cnt_workers': count_workers(dep_sal)})
        one_dep.update({'salary_fork': salary_fork(dep_sal)})
        one_dep.update({'avg_salary': avg_salary(dep_sal)})
        dep_ar_new.append(one_dep)
    return dep_ar_new


def csv_maker():
    '''Write data in a new csv file'''
    print('Сводный отчет будет сохранён как Departmental_Summary_Report.csv')
    final_ar = str_maker(consolidated_report())
    new_file = open('Departmental_Summary_Report.csv', 'w', encoding='utf-8')
    new_file.write('Название;Численность;Вилка зарплат;Средняя зарплата\n')
    for line in final_ar:
        new_file.write(';'.join(line.values()) + '\n')
    new_file.close()


def str_maker(old_ar: list) -> list:
    '''Change integer number to string'''
    for row in old_ar:
        row['cnt_workers'] = str(row['cnt_workers'])
        row['avg_salary'] = str(row['avg_salary'])
    return old_ar


if __name__ == '__main__':
    start()
