from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
from scipy.stats import poisson
from tabulate import tabulate
import time

# Configuración de Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# URL de la página web
url = "https://www.flashscore.co/partido/neXWQux2/#/h2h/overall"
driver.get(url)

# Obtener el HTML de la página
html = driver.page_source

# Crear un objeto BeautifulSoup para analizar el HTML
soup = BeautifulSoup(html, "html.parser")

# Encontrar los elementos que contienen los nombres de los equipos
equipo_local_element = soup.find("div", class_="duelParticipant__home")
equipo_visitante_element = soup.find("div", class_="duelParticipant__away")

# Extraer los nombres de los equipos
lista_equipos=[]
nombre_equipo_local = equipo_local_element.find("a", class_="participant__participantName").text
nombre_equipo_visitante = equipo_visitante_element.find("a", class_="participant__participantName").text

# Imprimir los nombres de los equipos
print("Equipo Local:", nombre_equipo_local)
print("Equipo Visitante:", nombre_equipo_visitante)
# Esperar hasta que los elementos de la primera tabla sean visibles
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "h2h__section")))

# Obtener el botón "Mostrar más partidos"
show_more_button = driver.find_element(By.CLASS_NAME, "showMore")

# Hacer clic en el botón "Mostrar más partidos" tres veces usando JavaScript
for _ in range(6):
    driver.execute_script("arguments[0].click();", show_more_button)
    # Esperar un breve momento para que se carguen los datos
    time.sleep(2)

# Encontrar los elementos de la primera tabla
partidos_equipo1 = driver.find_elements(By.CSS_SELECTOR, ".h2h__section:nth-child(1) .h2h__row")

# Crear una lista de tuplas para los datos del primer equipo
datos_tabla1 = []
for partido in partidos_equipo1:
    nombres_element = partido.find_elements(By.CSS_SELECTOR, ".h2h__participantInner")
    resultados_element = partido.find_element(By.CSS_SELECTOR, ".h2h__result")
    
    equipo_local = nombres_element[0].text
    equipo_visitante = nombres_element[1].text
    resultado_local = resultados_element.find_elements(By.TAG_NAME, "span")[0].text
    resultado_visitante = resultados_element.find_elements(By.TAG_NAME, "span")[1].text
    
    if equipo_local == nombre_equipo_local or equipo_visitante == nombre_equipo_local:
        datos_tabla1.append((equipo_local, resultado_local, resultado_visitante, equipo_visitante))

# Mostrar la tabla del primer equipo
tabla_equipo1 = tabulate(datos_tabla1, headers=["Equipo Local", "Goles Local", "Goles Visitante", "Equipo Visitante"])
print("Tabla Primer Equipo (Filtrada):")
print(tabla_equipo1)

# Obtener el elemento del botón "Mostrar más partidos" de la segunda tabla
show_more_button = driver.find_element(By.CSS_SELECTOR, ".h2h__section:nth-child(2) .showMore.showMore")

# Desplazar la página hacia abajo para asegurarse de que el botón esté en la parte superior de la vista
driver.execute_script("arguments[0].scrollIntoView();", show_more_button)

# Hacer clic en el botón "Mostrar más partidos" tres veces usando JavaScript
for _ in range(6):
    driver.execute_script("arguments[0].click();", show_more_button)
    # Esperar un breve momento para que se carguen los datos
    time.sleep(2)

# Esperar a que se carguen los nuevos partidos en la segunda tabla
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".h2h__section:nth-child(2) .h2h__row"))
)

# Encontrar los elementos de la segunda tabla
partidos_equipo2 = driver.find_elements(By.CSS_SELECTOR, ".h2h__section:nth-child(2) .h2h__row")

# Crear una lista de tuplas para los datos del segundo equipo
datos_tabla2 = []
for partido in partidos_equipo2:
    nombres_element = partido.find_elements(By.CSS_SELECTOR, ".h2h__participantInner")
    resultados_element = partido.find_element(By.CSS_SELECTOR, ".h2h__result")
    
    equipo_local = nombres_element[0].text
    equipo_visitante = nombres_element[1].text
    resultado_local = resultados_element.find_elements(By.TAG_NAME, "span")[0].text
    resultado_visitante = resultados_element.find_elements(By.TAG_NAME, "span")[1].text
    
    datos_tabla2.append((equipo_local, resultado_local, resultado_visitante, equipo_visitante))

# Mostrar la tabla del segundo equipo
tabla_equipo2 = tabulate(datos_tabla2, headers=["Equipo Local", "Goles Local", "Goles Visitante", "Equipo Visitante"])
print("Tabla Segundo Equipo (Filtrada):")
print(tabla_equipo2)

# ...

# Encontrar los elementos de la segunda tabla
partidos_equipo3 = driver.find_elements(By.CSS_SELECTOR, ".h2h__section:nth-child(3) .h2h__row")

# Crear una lista de tuplas para los datos de la tercera tabla (máximo 3 resultados)
datos_equipo3 = []

for i, partido in enumerate(partidos_equipo3):
    if i >= 4:  # Limitar a 3 resultados
        break
    
    # Obtener la fecha del partido
    fecha = partido.find_element(By.CLASS_NAME, "h2h__date").text

    # Obtener los nombres de los equipos local y visitante
    equipo_local_element = partido.find_element(By.CLASS_NAME, "h2h__homeParticipant")
    equipo_visitante_element = partido.find_element(By.CLASS_NAME, "h2h__awayParticipant")
    equipo_local = equipo_local_element.find_element(By.CLASS_NAME, "h2h__participantInner").text
    equipo_visitante = equipo_visitante_element.find_element(By.CLASS_NAME, "h2h__participantInner").text

    # Obtener los resultados del partido
    resultado_element = partido.find_element(By.CLASS_NAME, "h2h__result")
    resultado_local = resultado_element.find_elements(By.TAG_NAME, "span")[0].text
    resultado_visitante = resultado_element.find_elements(By.TAG_NAME, "span")[1].text

    datos_equipo3.append((fecha, equipo_local, resultado_local, resultado_visitante, equipo_visitante))

# Mostrar la tabla del tercer apartado (máximo 3 resultados)
tabla_equipo3 = tabulate(datos_equipo3, headers=["Fecha", "Equipo Local", "Goles Local", "Goles Visitante", "Equipo Visitante"])
print("Tabla Tercer Apartado:")
print(tabla_equipo3)

# Cerrar el navegador
driver.quit()


# Crear un diccionario para almacenar los datos de los equipos y sus pruebas de Poisson
datos_equipos = {}

# Obtener la lista de equipos
lista_equipos = [nombre_equipo_local, nombre_equipo_visitante]

# Calcular la cantidad promedio de goles de cada equipo
for equipo in lista_equipos:
    datos_local_equipo = [(_, resultado_local, _, nombre_local) for _, resultado_local, _, nombre_local in datos_tabla1 if equipo == nombre_local]
    datos_visitante_equipo = [(_, _, resultado_visitante, nombre_visitante) for _, _, resultado_visitante, nombre_visitante in datos_tabla2 if equipo == nombre_visitante]

    goles_promedio_local = sum(int(resultado_local) for _, resultado_local, _, _ in datos_local_equipo) / 10
    
    if datos_visitante_equipo:
        goles_promedio_visitante = sum(int(resultado_visitante) for _, _, resultado_visitante, _ in datos_visitante_equipo) / 10
    else:
        goles_promedio_visitante = 0  # Asignar 0 si no hay datos de visitantes
    
    datos_equipos[equipo] = {
        "goles_promedio_local": goles_promedio_local,
        "goles_promedio_visitante": goles_promedio_visitante
    }

# Crear una tabla para mostrar los resultados de las probabilidades
print("Tabla de Probabilidades:")
print("{:<30} {:<20} {:<20} {:<20} {:<20}".format("Equipo", "1 Gol", "2 Goles", "3 Goles", "Más de 3 Goles"))
print("="*110)

for equipo, datos in datos_equipos.items():
    datos_local_equipo = [(_, resultado_local, _, nombre_local) for _, resultado_local, _, nombre_local in datos_tabla1 if equipo == nombre_local]
    datos_visitante_equipo = [(_, _, resultado_visitante, nombre_visitante) for _, _, resultado_visitante, nombre_visitante in datos_tabla2 if equipo == nombre_visitante]
    
    goles_reales_local = int(datos_local_equipo[0][1]) if datos_local_equipo else 0
    goles_reales_visitante = int(datos_visitante_equipo[0][2]) if datos_visitante_equipo else 0
    
    media_poisson_local = datos["goles_promedio_local"]
    media_poisson_visitante = datos["goles_promedio_visitante"]
    
    probabilidad_1_gol_local = poisson.pmf(1, media_poisson_local)
    probabilidad_2_goles_local = poisson.pmf(2, media_poisson_local)
    probabilidad_3_goles_local = poisson.pmf(3, media_poisson_local)
    probabilidad_mas_3_goles_local = 1 - poisson.cdf(3, media_poisson_local)
    
    probabilidad_1_gol_visitante = poisson.pmf(1, media_poisson_visitante)
    probabilidad_2_goles_visitante = poisson.pmf(2, media_poisson_visitante)
    probabilidad_3_goles_visitante = poisson.pmf(3, media_poisson_visitante)
    probabilidad_mas_3_goles_visitante = 1 - poisson.cdf(3, media_poisson_visitante)
    
    print("{:<30} {:<20.4f} {:<20.4f} {:<20.4f} {:<20.4f}".format(equipo, probabilidad_1_gol_local, probabilidad_2_goles_local, probabilidad_3_goles_local, probabilidad_mas_3_goles_local))
    print("{:<30} {:<20.4f} {:<20.4f} {:<20.4f} {:<20.4f}".format(equipo, probabilidad_1_gol_visitante, probabilidad_2_goles_visitante, probabilidad_3_goles_visitante, probabilidad_mas_3_goles_visitante))
    print("-"*110)

# Cerrar el navegador
driver.quit()
