def read_function_table() -> {float: float}:
    function_table = {}
    while True:
        # filename = input("Введите имя файла для загрузки исходных данных "
        #                  "или пустую строку, чтобы ввести вручную: ")
        filename = "test.txt"

        if filename == '':
            while True:
                line = input()
                if line == '':
                    if len(function_table) < 8:
                        print('(!) Необходимо не менее 8 точек')
                        continue
                    else:
                        break
                try:
                    if len(line.split()) != 2:
                        print(' Нужно ввести два числа, через пробел')
                        continue
                    x, y = map(float, line.split())
                    function_table[x] = y
                except ValueError:
                    print('Вы ввели не число')
            break
        else:
            try:
                f = open(filename, "r")
                for line in f.readlines():
                    try:
                        if len(line.split()) != 2:
                            continue
                        x, y = map(float, line.split())
                        function_table[x] = y
                    except ValueError:
                        continue
                if len(function_table) < 6:
                    print('(!) В файле менее 8 корректных точек')
                    continue
                break
            except FileNotFoundError:
                print('(!) Файл для загрузки исходных данных не найден.')

    return function_table
