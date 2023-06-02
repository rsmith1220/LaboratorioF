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
    follow[next(iter(non_terminals))].add('$')

    changed = True
    while changed:
        changed = False
        for non_terminal in non_terminals:
            for production in productions[non_terminal]:
                for i, symbol in enumerate(production):
                    if symbol in non_terminals:
                        # Si no es el último símbolo de la producción, añadir el conjunto first del siguiente símbolo
                        if i + 1 < len(production):
                            next_symbol = production[i + 1]
                            if next_symbol in non_terminals:
                                added = len(follow[symbol])
                                follow[symbol].update(
                                    primeros[next_symbol] - {None})
                                if len(follow[symbol]) != added:
                                    changed = True
                            # Si el siguiente símbolo es un terminal, añadirlo al conjunto follow
                            else:
                                if next_symbol not in follow[symbol]:
                                    follow[symbol].add(next_symbol)
                                    changed = True
                        # Si es el último símbolo de la producción, añadir el conjunto follow del no terminal actual
                        else:
                            added = len(follow[symbol])
                            follow[symbol].update(follow[non_terminal])
                            if len(follow[symbol]) != added:
                                changed = True

    return follow