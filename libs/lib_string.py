def lower(line):
    if "--lower" in line:
        line = line.replace(" --lower", "")
        return line.lower()
    else:
        return line

def upper(line):
    if "--upper" in line:
        line = line.replace(" --upper", "")
        return line.upper()
    else:
        return line