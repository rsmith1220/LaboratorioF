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
        #si no se esta en un comentario, se agrega a la lista
        filtered_lines.append(line)

for i in filtered_lines:
    if i.startswith("%token"):
        line_tokens = i[len("%token"):].strip().split(' ')
        tokenList.extend(line_tokens)
    elif i.startswith(''):
        pass
    elif not i.startswith('IGNORE') and not i.startswith('/*'):
        print("error a la  hora de definir tokens ")


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


if len(tokenList)== len(tokensYal):
    estados, transiciones = leftRight.coleccion_canonica(productsConve)
    print("Estados")
    for i, estados in enumerate(estados):
        print(f'{i}: {estados}')
        
    print('\nTransiciones:')
    for transition in transiciones:
        print(f'{str(transition[0])} - \'{transition[1]}\' to {str(transition[2])}')
        

    estados, transiciones = leftRight.coleccion_canonica(productsConve)    
    draw.automara(estados,transiciones)   

    converted_prod = procesador.convertir(dictProductos)
    first = firstFollow.primeros(converted_prod)
    follow = firstFollow.siguientes(converted_prod, first)
    


    print("\n-----Firsts-----")
    for noTermilal, firSet in first.items():
        print(f"{noTermilal}: {firSet}")

    print("\n-----Follow-----")
    for noTermilal, follows in follow.items():
        print(f"{noTermilal}: {follows}")


#Convertir los sets en listas para que pandas entienda
terminals, no_terminals = firstFollow.get_terminales_no_terminales(productsConve)
terminals = list(terminals)
no_terminals = list(no_terminals)


action_table, goto_table, production_list, error_list = tabla.generate_slr_tables(estados, transiciones, productsConve, follow, no_terminals, terminals)

# concatenated_table = pd.concat([action_table, goto_table], axis=1, keys=['Accion', 'Goto'])
action_df = pd.DataFrame(action_table)
goto_df = pd.DataFrame(goto_table)
concatenated_table = pd.concat([action_df, goto_df], axis=1, keys=['Accion', 'Goto'])


concatenated_table = concatenated_table.fillna('-')

#Tabla y errores
print('\nTabla SLR')
print(concatenated_table,'\t')
if len(error_list) > 0:
    print("\nErrores encontrados:")
    for error in error_list:
        print(error)
else:
    pass
