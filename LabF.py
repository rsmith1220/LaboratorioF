import procesador
import re
archivo1='lex1.yalp' #YALP

archivo2='lex1.yal'

inside_block_comment = False

with open(archivo1,'r') as file:
    content=file.read()

with open(archivo2,'r') as file2:
    content2=file2.read()


lineas  = content.split('\n')


# Buscar %% en el file 
try:
    tokens,productos = content.split('%%')
    
except:
    print("El operador %% no esta en el arachivo")
    exit()

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
                pass
tokenList=[]

for line in lineas:
    if line.startswith("%token"):
        line_tokens = line[len("%token"):].strip().split(' ')
        tokenList.extend(line_tokens)
    elif line.startswith(''):
        pass
    elif not line.startswith('IGNORE') and not line.startswith('/*'):
        print("error a la  hora de definir tokens ")



productos = procesador.lectorLe(content)


converted_productions = {}
for key, value in productos.items():
    converted_productions[key] = [rule.split() for rule in value]

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
  

print(tokenList)
print(tokensYal)



