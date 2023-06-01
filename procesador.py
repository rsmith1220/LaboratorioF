def lectorLe(content):
    reglas = {}
    lines = content.split('\n')
    current_production = None
    prodrules = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.endswith(':'):
            if current_production:
                reglas[current_production] = prodrules
                prodrules = []
            current_production = line[:-1]
        elif line.startswith("/*"):
            pass
        elif line.endswith(';'):
            line = line[:-1]
            if line != "":
                prodrules.append(line)
            reglas[current_production] = prodrules
            prodrules = []
            current_production = None
        else:
            if (line.startswith('|') or line.startswith('->')) and current_production:
                line = line.strip().split('|')
                for item in line:
                    if item.strip() != "":
                        prodrules.append(item.strip())

            elif ('|' in line) and current_production:
                line = line.strip()
                prodrules.extend(line.split('|'))
            else:
                prodrules.append(line)
    return reglas

def tokensFunction(content):
    tokens = []
    lines = content.split('\n')
    for line in lines:
        if line.startswith("%token"):
            line_tokens = line[len("%token"):].strip().split(' ')
            tokens.extend(line_tokens)
        if not line.startswith("%token") and not line.startswith("IGNORE") and not line.startswith("/*") and line.strip():
            print("\nLos tokens no estan bien definidos.")
            exit()
    return tokens

def yalp(content,tokens,producciones):
    content = content
    tokens_section, productions_section = tokens,producciones
    tokens = tokensFunction(tokens_section)
    productions = lectorLe(productions_section)
    return tokens, productions