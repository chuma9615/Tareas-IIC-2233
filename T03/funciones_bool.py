from funciones_numericas import LEN, PROM, VAR, MEDIAN, DESV
from errores_personalizados import ImposibleProcesar


def comparar_columna(col1, simbolo, comando, columna2):
    func = {"LEN": LEN, "PROM": PROM, "VAR": VAR, "MEDIAN": MEDIAN, "DESV": DESV}
    simb = ["<", ">", "==", ">=", "<=", "!="]
    if simbolo not in simb:
        raise ValueError("No se puede procesar ")
    try:
        if comando in func and isinstance(comando, str):
            a = func[comando].__call__(list(col1))
            b = func[comando].__call__(list(columna2))
            if simbolo == ">=":
                if a >= b:
                    return True
                return False

            if simbolo == "<=":
                if a <= b:
                    return True
                return False

            if simbolo == "==":
                if a == b:
                    return True
                return False

            if simbolo == "<":
                if a < b:
                    return True
                return False

            if simbolo == ">":
                if a > b:
                    return True
                return False
    except TypeError:
        raise ImposibleProcesar("Imposible procesar")


def comparar(a, simbolo, b):
    simb = ["<", ">", "==", ">=", "<=", "!="]
    if simbolo not in simb:
        raise ValueError("No se puede procesar ")
    if simbolo == ">=":
        if a >= b:
            return True
        return False

    if simbolo == "<=":
        if a <= b:
            return True
        return False

    if simbolo == "==":
        if a == b:
            return True
        return False

    if simbolo == "<":
        if a < b:
            return True
        return False

    if simbolo == ">":
        if a > b:
            return True
        return False
