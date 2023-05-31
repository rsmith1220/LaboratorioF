import procesador
archivo1='lex1.yalp' #YALP

archivo2=''

inside_block_comment = False

with open(archivo1,'r') as file:
    content=file.read()


# Buscar %% en el file 
try:
    tokens,productos = content.split('%%')
    
except:
    print("El operador %% no esta en el arachivo")
    exit()

tokenList=[]
lineas  = content.split('\n')
for line in lineas:
    if line.startswith("%token"):
        line_tokens = line[len("%token"):].strip().split(' ')
        tokens.extend(line_tokens)
    elif not line.startswith('IGNORE') and not line.startswith('/*'):
        print("error a la  hora de definir tokens ")

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

procesador.lectorL(content)