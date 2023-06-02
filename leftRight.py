class AutoItem:
    def __init__(self, producciones, position, derived=False):
        self.producciones = (producciones[0], tuple(producciones[1]))
        self.position = position
        self.derived = derived

    def __repr__(self):
        before_dot = " ".join(self.producciones[1][:self.position])
        after_dot = " ".join(self.producciones[1][self.position:])
        return f'{self.producciones[0]} -> {before_dot} • {after_dot}'


    def __eq__(self, other):
        return self.producciones == other.producciones and self.position == other.position

    def __hash__(self):
        return hash((self.producciones, self.position))


def cerra(items, produccioness):
    new_items = set(items)
    changed = True
    while changed:
        changed = False
        for item in list(new_items):
            if item.position < len(item.producciones[1]) and item.producciones[1][item.position] in produccioness:
                non_terminal = item.producciones[1][item.position]
                for producciones in produccioness[non_terminal]:
                    new_item = AutoItem((non_terminal, producciones), 0, True)
                    if new_item not in new_items:
                        new_items.add(new_item)
                        changed = True
    return new_items


def goto(items, symbol, producciones):
    next_items = set()
    for item in items:
        if item.position < len(item.producciones[1]) and item.producciones[1][item.position] == symbol:
            next_items.add(AutoItem(item.producciones, item.position + 1))
    return cerra(next_items, producciones)


def CC(producciones):
    initial_key = list(producciones.keys())[0]
    initial_item = AutoItem((initial_key + '\'', [initial_key]), 0)
    initial_state = cerra({initial_item}, producciones)
    
    states = [initial_state]
    transitions = []
    
    stack = [initial_state]

    while stack:
        current_state = stack.pop()
        symbols = set(sym for item in current_state for sym in item.producciones[1][item.position:item.position + 1])
        
        for symbol in symbols:
            next_state = goto(current_state, symbol, producciones)
            if not next_state:
                continue

            if next_state not in states:
                states.append(next_state)
                stack.append(next_state)
            
            transitions.append((states.index(current_state), symbol, states.index(next_state)))

    accept_state = len(states)
    for i, state in enumerate(states):
        for item in state:
            if item.producciones[0] == initial_key + '\'' and item.position == len(item.producciones[1]) and item.derived == False:
                transitions.append((i, '$', accept_state))
                break

    states.append(set())
    
    return states, transitions
