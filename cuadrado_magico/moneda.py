import random

def lanzar_moneda():
  resultado = random.choice(["Águila", "Sol"])
  return resultado

resultado_lanzamiento = lanzar_moneda()
print(resultado_lanzamiento)
