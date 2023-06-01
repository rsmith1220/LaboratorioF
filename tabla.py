import pandas as pd
import pickle
import firstFollow

def generate_slr_tables(states, transitions, productions, follow_sets, non_terminals, terminals):
    start_symbol = list(productions.keys())[0]  # simbolo inicial
    # inicializar action y goto tables
    action_table = pd.DataFrame(index=range(
        len(states)), columns=terminals, dtype=object)
    goto_table = pd.DataFrame(index=range(len(
        states)), columns=non_terminals, dtype=object)  # Quitar el símbolo de dolar ($)
    # Crear una lista de producciones y un diccionario para mapear las producciones a su índice correspondiente
    production_list = []
    production_index = {}
    for key in productions.keys():
        for value in productions[key]:
            prod = (key, tuple(value))
            production_index[prod] = len(production_list)
            production_list.append(prod)
    # Lista para almacenar los errores
    error_list = []
    def handle_conflict(table, row, col, value):
        try:
            if pd.notna(table.loc[row, col]) and col != '$':
                existing_value = table.loc[row, col]
                error_list.append(
                    f'Conflict in [{row}, {col}]: Multiple actions ({existing_value}, {value})')
            else:
                table.loc[row, col] = value
        except KeyError:
            error_list.append(
                f'Invalid column key: {col} in [{row}, {col}]')
    # llenar las tablas
    for i, state in enumerate(states):
        for item in state:
            # caso especial para la reducción [S' -> S·]
            if item.production[0] == start_symbol + "'" and item.position == len(item.production[1]):
                action_table.loc[i, '$'] = "ACC"
            # caso para [A -> α·]
            elif item.position == len(item.production[1]):
                for symbol in follow_sets.get(item.production[0], []):
                    prod = (item.production[0], tuple(item.production[1]))
                    handle_conflict(action_table, i, symbol,
                                    f"R{production_index.get(prod, -1)}")
        for trans in transitions:
            if trans[0] == i:
                if trans[1] in terminals:  # caso para [A → α·aβ]
                    handle_conflict(action_table, i,
                                    trans[1], f"S{trans[2]}")
                elif trans[1] in non_terminals:  # caso para go to
                    goto_table.loc[i, trans[1]] = trans[2]
    return action_table, goto_table, production_list, error_list
terminals, no_terminals = firstFollow.get_terminales_no_terminales(
    converted_productions)
# Obtener las tablas de análisis SLR
action_table, goto_table, production_list, error_list = generate_slr_tables(
    states, transitions, converted_productions, follow, no_terminals, terminals)
# Concatenamos las tablas para su impresion
concatenated_table = pd.concat(
    [action_table, goto_table], axis=1, keys=['ACTION', 'GOTO'])
# remplazamos NaN con "-"
concatenated_table = concatenated_table.fillna('-')
# imprimimos la tabla
print('\nTABLA DE PARSEO SLR')
print(concatenated_table)
if len(error_list) > 0:
    print("\nInforme de Errores:")
    for error in error_list:
        print(error)
else:
    print("\nNo hay errores, se prosigue con la ejecución")
# convertir objetos a bytes
action_table_bytes = pickle.dumps(action_table)
goto_table_bytes = pickle.dumps(goto_table)
production_list_bytes = pickle.dumps(production_list)
# guardar bytes en archivos binarios
with open('action_table.pkl', 'wb') as f:
    f.write(action_table_bytes)
with open('goto_table.pkl', 'wb') as f:
    f.write(goto_table_bytes)
with open('production_list.pkl', 'wb') as f:
    f.write(production_list_bytes)
