
def me():
    # ВАЖНО! некоторые переменные называются нелогично, например cheap_node, хотя по логике он next_node,
    # это потому что я взял почти всю логику из своего решения траспортной задачи методом минимальной стоимости

    # Закомменченые данные - тестовые, более удобные для тестирование кода(вместо input'ов)
    # На счет ввода данных я не заморачивался и сгенерировал его нейронкой


    # graph = {}
    # graph["M1"] = {}
    # graph["M1"]["1"] = 1
    # graph["M1"]["2"] = 3
    # graph["M1"]["3"] = 5
    # graph["M1"]["4"] = 7
    # graph["M2"] = {}
    # graph["M2"]["1"] = 2
    # graph["M2"]["2"] = 2
    # graph["M2"]["3"] = 2
    # graph["M2"]["4"] = 4
    #
    # print(graph)
    #
    # need = {}
    # need["M1"] = 100
    # need["M2"] = 100
    #
    #
    # stash = {}
    # stash["1"] = 70
    # stash["2"] = 30
    # stash["3"] = 50
    # stash["4"] = 50
    #
    # total_sums = {}
    # total_sums["M1"] = 0
    # total_sums["M2"] = 0
    #
    # total_need = sum(need.values())

    graph = {}
    need = {}
    stash = {}
    total_sums = {}

    while True:
        try:
            num_m = int(input("Количество пунктов спроса (M): "))
            if num_m <= 0:
                raise ValueError
            break
        except ValueError:
            print("Ошибка: введите положительное целое число!")

    m_list = []
    for i in range(num_m):
        m_name = input(f"Имя пункта спроса {i + 1} (например, M{i + 1}): ").strip()
        if not m_name or m_name in m_list:
            print("Ошибка: имя должно быть уникальным и не пустым!")
            i -= 1  # Повторить ввод
            continue
        m_list.append(m_name)
        while True:
            try:
                need[m_name] = int(input(f"Сколько необходимо {m_name}? (целое число): "))
                if need[m_name] < 0:
                    raise ValueError
                break
            except ValueError:
                print("Ошибка: введите положительное целое число!")

    # Ввод количества и имён поставщиков
    print("\nВведите данные для поставщиков (узлов):")
    while True:
        try:
            num_nodes = int(input("Количество поставщиков (узлов): "))
            if num_nodes <= 0:
                raise ValueError
            break
        except ValueError:
            print("Ошибка: введите положительное целое число!")

    node_list = []
    for i in range(num_nodes):
        node_name = input(f"Имя поставщика {i + 1} (например, {i + 1}): ").strip()
        if not node_name or node_name in node_list:
            print("Ошибка: имя должно быть уникальным и не пустым!")
            i -= 1  # Повторить ввод
            continue
        node_list.append(node_name)
        while True:
            try:
                stash[node_name] = int(input(f"Сколько есть у {node_name} поставщика? (целое число): "))
                if stash[node_name] < 0:
                    raise ValueError
                break
            except ValueError:
                print("Ошибка: введите положительное целое число!")

    # Ввод graph: для каждого M вводим стоимости к каждому узлу
    print("\nВведите стоимости в graph (от M к узлам):")
    for m in m_list:
        graph[m] = {}
        for node in node_list:
            while True:
                try:
                    graph[m][node] = int(input(f"Стоимость от от {node} поставщика к {m}(целое число): "))
                    if graph[m][node] < 0:
                        raise ValueError
                    break
                except ValueError:
                    print("Ошибка: введите положительное целое число!")

    total_need = sum(need.values())
    total_stash = sum(stash.values())
    penalty = 0  # Стоимость для dummy

    if total_need > total_stash:
        # Добавляем фиктивный поставщик (dummy_node)
        dummy_node = "dummy_supply"
        while dummy_node in node_list:  # Уникальное имя
            dummy_node += "_"
        node_list.append(dummy_node)
        stash[dummy_node] = total_need - total_stash
        for m in m_list:
            graph[m][dummy_node] = penalty  # 0 или штраф
        print(f"Добавлен dummy_supply '{dummy_node}' с stash={stash[dummy_node]} для баланса (need > stash)")

    for m in need:
        total_sums[m] = 0

    processed = []
    print(f"START: need: {need}, stash: {stash}, total_sums: {total_sums}, \n"
          f"graph: {graph}")


    def find_next_node(spisok):
        next_node = None
        local_graph = spisok
        local_m = None
        for m, nodes in local_graph.items():
            if m in processed:
                continue
            for node, cost in nodes.items():
                if node not in processed:
                    next_node = node
                    local_m = m
                    return next_node, local_m
        return None, None

    def counting(spisok):
        print("def counting started")
        while total_need > 0:
            print("cycle started")
            cheap_node, m = find_next_node(spisok)
            print(f"I gave m: {m}")
            if m is None:
                break
            local_need = need[m]
            total_cost = 0
            print(f"I gave cheap_node: {cheap_node}")
            if local_need >= stash[cheap_node]:
                how_many = stash[cheap_node]
            else:
                how_many = local_need
            print(f"how_many: {how_many}")
            total_cost += spisok[m][cheap_node] * how_many
            stash[cheap_node] -= how_many
            need[m] -= how_many
            total_sums[m] += total_cost
            if need[m]  <= 0:
                processed.append(m)
            if stash[cheap_node] <= 0:
                processed.append(cheap_node)
                print(f"I appended cheap_node: {cheap_node}")
            print(
                f"total_cost:{total_cost}, stash:{stash}, need:{need}, processed:{processed}, total_sums:{total_sums}")
        print(f"total_cost:{total_cost}, stash:{stash}, need:{need}, processed:{processed}, total_sums:{total_sums}")

        leftovers = []
        if sum(stash.values()) > 0:
            print("В результате работы алгоритма были выявлены остатки:")
            for x, y in stash.items():
                if y > 0:
                    print(f"На складе {x}: {y}")

        otvet = sum(total_sums.values())
        print(f"Ответ: {otvet}")


    counting(graph)

me()