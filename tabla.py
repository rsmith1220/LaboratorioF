from collections import defaultdict

def create_table(states, symbols):
    return defaultdict(lambda: defaultdict(lambda: None), {i: {} for i in range(len(states))})

def add_production(productions):
    production_list = []
    production_index = {}
    for key in productions.keys():
        for value in productions[key]:
            prod = (key, tuple(value))
            production_index[prod] = len(production_list)
            production_list.append(prod)
    return production_list, production_index

def handle_conflict(table, state, symbol, action, existing_actions):
    if symbol in table[state] and symbol != '$':
        existing_action = table[state][symbol]
        existing_actions.append(
            f'Conflict in state {state}, symbol {symbol}: Multiple actions ({existing_action}, {action})')
    else:
        table[state][symbol] = action

def generate_slr_tables(states, transitions, productions, follow_sets, non_terminals, terminals):
    start_symbol = list(productions.keys())[0]
    action_table = create_table(states, terminals)
    goto_table = create_table(states, non_terminals)
    production_list, production_index = add_production(productions)
    existing_actions = []

    for state in range(len(states)):
        for item in states[state]:
            if item.producciones[0] == start_symbol + "'" and item.position == len(item.producciones[1]):
                action_table[state]['$'] = "ACC"

            elif item.position == len(item.producciones[1]):
                for symbol in follow_sets.get(item.producciones[0], []):
                    prod = (item.producciones[0], tuple(item.producciones[1]))
                    handle_conflict(action_table, state, symbol,
                                    f"R{production_index.get(prod, -1)}", existing_actions)
        for trans in transitions:
            if trans[0] == state:
                if trans[1] in terminals:  
                    handle_conflict(action_table, state,
                                    trans[1], f"S{trans[2]}", existing_actions)
                elif trans[1] in non_terminals:  
                    goto_table[state][trans[1]] = trans[2]
                    
    return action_table, goto_table, production_list, existing_actions
