def get_terminales_no_terminales(productions):
    non_terminals = set(productions.keys())
    symbols = {symbol for production in productions.values() for sequence in production for symbol in sequence}
    terminals = symbols - non_terminals

    return terminals, non_terminals



def primeros(productions):
    non_terminals, terminals = get_terminales_no_terminales(productions)
    first = {nt: set() for nt in non_terminals}
    visited = {nt: False for nt in non_terminals}

    def compute_first(symbol):
        if symbol in terminals:
            return {symbol}
        elif first[symbol] is None:
            first[symbol] = set()
            if symbol in productions:  # Add this line
                for production in productions[symbol]:
                    for symbol_in_prod in production:
                        first[symbol].update(compute_first(symbol_in_prod))
                        if None not in first[symbol_in_prod]:
                            break
                    else:
                        first[symbol].add(None)
        return first[symbol]


    # Compute FIRST sets for all non-terminals
    for non_terminal in non_terminals:
        compute_first(non_terminal)

    return first



def siguientes(productions, primeros):
    _, non_terminals = get_terminales_no_terminales(productions)
    follow = {non_terminal: set() for non_terminal in non_terminals}
    follow[next(iter(non_terminals))].add('$')  # start symbol

    while True:
        # Make a deep copy of the follow sets to check if any changes are made in the loop
        old_follow = {key: val.copy() for key, val in follow.items()}
        for non_terminal in non_terminals:
            for production in productions[non_terminal]:
                for i in range(len(production)):
                    if production[i] in non_terminals:
                        if i+1 < len(production):
                            next_symbol = production[i+1]
                            # If the next symbol is a non terminal, then add its first to the current non terminal's follow
                            if next_symbol in non_terminals:
                                follow[production[i]] = follow[production[i]].union(primeros[next_symbol] - {None})
                            else:
                                # If the next symbol is a terminal then add it to the current non terminal's follow
                                follow[production[i]].add(next_symbol)
                        else:
                            # If the current non terminal is the last symbol then add the follow of the LHS non terminal to its follow
                            follow[production[i]] = follow[production[i]].union(follow[non_terminal])
        
        # If no changes were made in the last loop, then stop
        if old_follow == follow:
            break

    return follow
