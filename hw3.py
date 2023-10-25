# При старте программы выводится меню, которое состоит из 3-х пунктов:
# Вывести в понятном виде иерархию команд, т.е. департамент и все команды, которые входят в него
# Вывести сводный отчёт по департаментам: название, численность, "вилка" зарплат в виде мин – макс, среднюю зарплату
# Сохранить сводный отчёт из предыдущего пункта в виде csv-файла. При этом необязательно вызывать сначала команду из п.2
# Пользователь выбирает пункт меню, вводя соответствующее число.

# Условия:
# Используем только встроенные модули (без pandas и т.д.)
# Весь скрипт разбит на функции
# Каждая функция содержит докстринги
# Бонус: все параметры аннотированы типами

def start():
    '''Just start this program'''
    option = 0
    options = [1, 2, 3]
    print(
        'Программа может выполнить три команды:\n',
        '1) Вывести иерархию команд, т.е. департамент и все команды, которые входят в него\n',
        '2) Вывести сводный отчёт по департаментам: название, численность,',
        'вилка зарплат в виде мин – макс, среднюю зарплату\n',
        '3) Сохранить сводный отчёт из предыдущего пункта в виде csv-файла.'
    )
    while option not in options:
        print('Выберите: команда {}, {} или {}'.format(*options))
        option = int(input())
    if option == 1:
        dep_hierarchy()
    elif option == 2:
        consolidated_report_printer()
    else:
        csv_maker()


def file_opener() -> list:
    '''This hepls to open the file'''
    lines_ar = []
    with open('Corp_Summary.csv', encoding="utf-8") as f:
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
    print(dep_ar)


def consolidated_report_printer():
    '''Just print this report'''
    print(*consolidated_report())


def consolidated_report() -> list:
    '''Make 2d list of info for second task'''
    file = file_opener()
    dep_ar = {}
    for row in file:
        dep_name = row[1]
        salary = row[5]
        if dep_name in dep_ar:
            dep_ar[dep_name].append(n_remover(salary))
        else:
            dep_ar[dep_name] = [n_remover(salary)]
    dep_ar_new = dict_changer(dep_ar)
    return dep_ar_new


def n_remover(salary: str) -> int:
    '''Put any number with \n and this function change it to integer'''
    salary = int(salary[:-1])
    return salary


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


def dict_changer(dep_ar: dict) -> list:
    '''Convert dict to list'''
    dep_ar_new = []
    for dep_name, dep_sal in dep_ar.items():
        dep_ar_new.append([dep_name, count_workers(dep_sal), salary_fork(dep_sal), avg_salary(dep_sal)])
    return dep_ar_new


def csv_maker():
    '''Write data in a new csv file'''
    final_ar = str_maker(consolidated_report())
    new_file = open('Corp_Summary_New.csv', 'w', encoding="utf-8")
    new_file.write('Название;Численность;Вилка зарплат;Средняя зарплата\n')
    for line in final_ar:
        new_file.write(';'.join(line) + '\n')
    new_file.close()


def str_maker(old_ar: list) -> list:
    '''Change integer number to string'''
    for row in old_ar:
        row[1], row[3] = str(row[1]), str(row[3])
    return old_ar


if __name__ == '__main__':
    start()
