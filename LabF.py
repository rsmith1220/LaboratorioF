import procesador
import re
import firstFollow
import leftRight
import draw
import pickle
import tabla
import pandas as pd
archivo1='lex1.yalp' #YALP

archivo2='lex1.yal'

inside_block_comment = False


#YALP
with open(archivo1,'r') as file:
    content=file.read()


#YALEX
with open(archivo2,'r') as file2:
    content2=file2.read()


lineas  = content.split('\n')


# Buscar %% en el file 
try:
    tokens,productos = content.split('%%')
    
except:
    print("El operador %% no esta en el arachivo")
    exit()


tokenList=[]
filtered_lines=[]

for line in lineas:
    if line.startswith("/*"):
        if inside_block_comment:
            #si estamos en un bloque de comentario, revisar si alli termina o sigue
            if '*/' in line and inside_block_comment or '*)' in line and inside_block_comment:
                
                inside_block_comment = False  # found the end of the comment
        else:
            #revisar si comienza el bloque de comentario
            if '/*' in line or '(*' in line:
                inside_block_comment = True  # found the start of a comment
    else:
        #si no se esta en un comentario, continuar
        filtered_lines.append(line)

for i in filtered_lines:
    if i.startswith("%token"):
        line_tokens = i[len("%token"):].strip().split(' ')
        tokenList.extend(line_tokens)
    elif i.startswith(''):
        pass
    elif not i.startswith('IGNORE') and not i.startswith('/*'):
        print("error a la  hora de definir tokens ")




# productos = procesador.lectorLe(content)


lineas = content2.split('\n')
for i, line in enumerate(lineas):
    if re.match(r"^rule tokens = .*?$", line):
        rule_tokens_index = i
        break

tokensYal=[]
if rule_tokens_index is not None:
    for line in lineas[rule_tokens_index + 1:]:
        match = re.search(r"\{\s*(.*?)\s*\}", line)
        if match and match.group(1):  
            tokensYal.append(match.group(1))
  
tokens, dictProductos=procesador.yalp(content,tokens,content)

productsConve ={}
for key,value in dictProductos.items():
    productsConve[key]=[rule.split() for rule in value]

print(tokenList)
print(tokensYal)

def convertidor(productions_dict):
    setConvertido = {}
    for key in productions_dict:
        setConvertido[key] = []
        for rule in productions_dict[key]:
            setConvertido[key].append(rule.split())
    return setConvertido

# setConvertido = convertidor(productos)

if len(tokenList)== len(tokensYal):
    estados, transiciones = leftRight.coleccion_canonica(productsConve)
    print("Estados")
    for i, estados in enumerate(estados):
        print(f'{i}: {estados}')
        
    print('\nTransiciones:')
    for transition in transiciones:
        print(transition)

    estados, transiciones = leftRight.coleccion_canonica(productsConve)    
    draw.automara(estados,transiciones)   
    
    def convert_productions(productions):
        converted_productions = {}
        for key, value in productions.items():
            converted_productions[key] = [prod.split() for prod in value]
        return converted_productions

    converted_prod = convert_productions(dictProductos)
    first = firstFollow.primeros(converted_prod)
    follow = firstFollow.siguientes(converted_prod, first)

    print("\nConjuntos Primeros:")
    for non_terminal, first_set in first.items():
        print(f"{non_terminal}: {first_set}")

    print("\nConjuntos Siguientes:")
    for non_terminal, follow_set in follow.items():
        print(f"{non_terminal}: {follow_set}")





terminals, no_terminals = firstFollow.get_terminales_no_terminales(productsConve)
terminals = list(terminals)
no_terminals = list(no_terminals)
# Obtener las tablas de análisis SLR
action_table, goto_table, production_list, error_list = tabla.generate_slr_tables(estados, transiciones, productsConve, follow, no_terminals, terminals)
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
    pass
# convertir objetos a bytes
action_table_bytes = pickle.dumps(action_table)
goto_table_bytes = pickle.dumps(goto_table)
production_list_bytes = pickle.dumps(production_list)
# guardar bytes en archivos binarios
with open('action_table.txt', 'wb') as f:
    f.write(action_table_bytes)
with open('goto_table.txt', 'wb') as f:
    f.write(goto_table_bytes)
with open('production_list.txt', 'wb') as f:
    f.write(production_list_bytes)