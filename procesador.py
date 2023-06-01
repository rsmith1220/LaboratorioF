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
        if line[:6] == "%token":
            line_tokens = line[7:].strip().split(' ')
            tokens += line_tokens
        if line[:6] != "%token" and line[:6] != "IGNORE" and line[:2] != "/*" and line.strip():
            print("\nThe tokens are not properly defined.")
            exit()
    return tokens


def yalp(content,tokens,producciones):
    content = content
    seccTokens, seccProd = tokens,producciones
    tokens = tokensFunction(seccTokens)
    productions = lectorLe(seccProd)
    return tokens, productions

def convertir(productions):
        converted_productions = {}
        for key, value in productions.items():
            converted_productions[key] = [prod.split() for prod in value]
        return converted_productions