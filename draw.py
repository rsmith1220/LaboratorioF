from graphviz import Digraph


def automara(states, transitions):
    dot = Digraph()
    dot.attr('node', shape='rectangle')

    for i, state in enumerate(states):
        parte1 = []
        derivados = []
        for item in state:
            if item.derivados:
                derivados.append(str(item))
            else:
                parte1.append(str(item))

        label = 'I ' + str(i) + '\n<---------------->\n'
        label += '\n'.join(parte1) + \
            '\n<---------------->\n' + '\n'.join(derivados)

        dot.node(str(i), label=label)

    for t in transitions:
        dot.edge(str(t[0]), str(t[2]), label=t[1])

    dot.render("automata", cleanup=True)