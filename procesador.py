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