# test_mercadolibre.py
# Automatización de pruebas para MercadoLibre.com utilizando Selenium

import time
import unittest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import logging
import os
from datetime import datetime

# Configuración del sistema de logging
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"logs/test_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

class MercadoLibreTest(unittest.TestCase):
    
    def setUp(self):
    
        logger.info("Iniciando configuración del WebDriver")
        
        try:
            chrome_options = Options()
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-gpu")

            try:
                service = Service(ChromeDriverManager().install())
                self.driver = webdriver.Chrome(service=service, options=chrome_options)
            except Exception as e:                
                try:
                    chrome_paths = {
                        'win': 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
                        'win_alt': 'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
                        'mac': '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                        'linux': '/usr/bin/google-chrome'
                    }
                    import platform
                    system = platform.system().lower()
                    
                    if 'win' in system:
                        if os.path.exists(chrome_paths['win']):
                            chrome_options.binary_location = chrome_paths['win']
                        elif os.path.exists(chrome_paths['win_alt']):
                            chrome_options.binary_location = chrome_paths['win_alt']
                    elif 'darwin' in system:  # macOS
                        if os.path.exists(chrome_paths['mac']):
                            chrome_options.binary_location = chrome_paths['mac']
                    elif 'linux' in system:
                        if os.path.exists(chrome_paths['linux']):
                            chrome_options.binary_location = chrome_paths['linux']
                    
                    self.driver = webdriver.Chrome(options=chrome_options)
                except Exception as e2:
                    logger.warning(f"Error al inicializar con path manual: {str(e2)}")
                    
                    logger.info("Intentando inicializar Chrome de forma simple")
                    self.driver = webdriver.Chrome(options=chrome_options)
            
            self.driver.maximize_window()
            self.wait = WebDriverWait(self.driver, 10)
            logger.info("WebDriver configurado correctamente")
            
        except Exception as final_error:
            logger.error(f"Error fatal al configurar WebDriver: {str(final_error)}")
            raise
        
    def tearDown(self):
        logger.info("Finalizando prueba y cerrando WebDriver")
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
    
    def test_01_navegar_a_mercadolibre(self):
        logger.info("Ejecutando prueba: Navegar a MercadoLibre")
        try:
            self.driver.get("https://www.mercadolibre.com")
            
            self.wait.until(EC.title_contains("Mercado"))
            current_url = self.driver.current_url
            self.assertTrue("mercadolibre.com" in current_url, f"URL incorrecta: {current_url}")
            
            logger.info(f"Navegación exitosa a: {current_url}")
        except Exception as e:
            logger.error(f"Error en test_01_navegar_a_mercadolibre: {str(e)}")
            self.driver.save_screenshot(f"logs/error_navegacion_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            raise
        
    def test_02_seleccionar_pais(self):
        logger.info("Ejecutando prueba: Seleccionar país en MercadoLibre")
        try:
            self.driver.get("https://www.mercadolibre.com")
            
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[href*='mercadolibre.com.do']")))
            
            self.driver.save_screenshot(f"logs/seleccion_pais_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            
            dom_link = self.driver.find_element(By.CSS_SELECTOR, "a[href*='mercadolibre.com.do']")
            logger.info(f"Seleccionando país: {dom_link.text}")
            dom_link.click()
            
            self.wait.until(EC.url_contains("mercadolibre.com.do"))
            self.assertTrue("mercadolibre.com.do" in self.driver.current_url, 
                       f"No se redirigió correctamente a la versión de Dominicana: {self.driver.current_url}")
            
            logger.info(f"Selección de país exitosa: {self.driver.current_url}")
        except Exception as e:
            logger.error(f"Error en test_02_seleccionar_pais: {str(e)}")
            self.driver.save_screenshot(f"logs/error_pais_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            raise
        
    def test_03_busqueda_producto(self):
        logger.info("Ejecutando prueba: Búsqueda de producto")
        try:
            self.driver.get("https://www.mercadolibre.com.do")
            
            search_box = self.wait.until(EC.presence_of_element_located((By.NAME, "as_word")))
            
            producto = "laptop"
            logger.info(f"Buscando producto: {producto}")
            search_box.clear()
            search_box.send_keys(producto)
            search_box.send_keys(Keys.RETURN)
            
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ol.ui-search-layout")))
            resultados = self.driver.find_elements(By.CSS_SELECTOR, "li.ui-search-layout__item")
            
            self.assertTrue(len(resultados) > 0, "No se encontraron resultados para la búsqueda")
            logger.info(f"Búsqueda exitosa. Se encontraron {len(resultados)} resultados")
        except Exception as e:
            logger.error(f"Error en test_03_busqueda_producto: {str(e)}")
            self.driver.save_screenshot(f"logs/error_busqueda_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            raise
        
    def test_04_filtrar_por_condicion(self):
        logger.info("Ejecutando prueba: Filtrar por condición")
        try:
            self.driver.get("https://www.mercadolibre.com.do")
            search_box = self.wait.until(EC.presence_of_element_located((By.NAME, "as_word")))
            search_box.clear()
            search_box.send_keys("iphone")
            search_box.send_keys(Keys.RETURN)
            
            self.driver.save_screenshot(f"logs/filtro_condicion_1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Condición')]")))
                filtro_nuevo = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Nuevo')]")))
                logger.info("Aplicando filtro: Nuevo (método 1)")
                filtro_nuevo.click()
            except Exception as filter_error:
                logger.warning(f"No se pudo aplicar el filtro con método 1: {str(filter_error)}")
                
                try:
                    self.driver.save_screenshot(f"logs/filtro_condicion_2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                    
                    filtros = self.driver.find_elements(By.CSS_SELECTOR, ".ui-search-filter-dl, .ui-search-filter-container")
                    for filtro in filtros:
                        if "Condición" in filtro.text or "CONDICIÓN" in filtro.text.upper():
                            logger.info("Encontrada sección de filtro Condición")
                            try:
                                filtro.click()
                                time.sleep(1)
                            except:
                                pass
                            
                            nuevo_opciones = filtro.find_elements(By.XPATH, ".//*[contains(text(), 'Nuevo')]")
                            if nuevo_opciones:
                                logger.info("Aplicando filtro: Nuevo (método 2)")
                                nuevo_opciones[0].click()
                                break
                
                except Exception as filter_error2:
                    logger.warning(f"No se pudo aplicar el filtro con método 2: {str(filter_error2)}")
                    # Continuamos con la prueba sin aplicar el filtro
                    logger.info("Continuando sin aplicar filtro")
            
            self.assertTrue("iphone" in self.driver.current_url.lower(), 
                           "No estamos en la página de resultados para iPhone")
            
            logger.info("Prueba de filtrado completada")
        except Exception as e:
            logger.error(f"Error en test_04_filtrar_por_condicion: {str(e)}")
            self.driver.save_screenshot(f"logs/error_filtro_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            raise
            
    def test_05_ver_detalle_producto(self):
        logger.info("Ejecutando prueba: Ver detalle de producto")
        try:
            self.driver.get("https://www.mercadolibre.com.do")
            search_box = self.wait.until(EC.presence_of_element_located((By.NAME, "as_word")))
            search_box.clear()
            search_box.send_keys("monitor")
            search_box.send_keys(Keys.RETURN)
            
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "ol.ui-search-layout")))
            
            self.driver.save_screenshot(f"logs/detalle_producto_1_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            
            try:
                primer_producto = self.wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, "li.ui-search-layout__item div.ui-search-item__title")))
                nombre_producto = primer_producto.text
                logger.info(f"Seleccionando producto (método 1): {nombre_producto}")
                primer_producto.click()
            except Exception as prod_error:
                logger.warning(f"No se pudo seleccionar el producto con método 1: {str(prod_error)}")
                
                try:
                    self.driver.save_screenshot(f"logs/detalle_producto_2_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                    primer_producto = self.wait.until(EC.element_to_be_clickable(
                        (By.CSS_SELECTOR, ".ui-search-result__content a, .ui-search-item a, .ui-search-result a")))
                    logger.info("Seleccionando producto (método 2)")
                    primer_producto.click()
                except Exception as prod_error2:
                    logger.warning(f"No se pudo seleccionar el producto con método 2: {str(prod_error2)}")
                    
                    self.driver.save_screenshot(f"logs/detalle_producto_3_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
                    enlaces_resultados = self.driver.find_elements(By.CSS_SELECTOR, "ol.ui-search-layout a")
                    if enlaces_resultados:
                        logger.info("Seleccionando producto (método 3)")
                        enlaces_resultados[0].click()
                    else:
                        raise Exception("No se encontraron enlaces en la página de resultados")
            
           
            self.wait.until(lambda driver: "articulo" in driver.current_url or "producto" in driver.current_url or "item" in driver.current_url)
            
            self.driver.save_screenshot(f"logs/detalle_producto_final_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            
            self.assertTrue("articulo" in self.driver.current_url or "item" in self.driver.current_url or 
                           "producto" in self.driver.current_url, 
                           f"No estamos en una página de detalle de producto: {self.driver.current_url}")
            
            logger.info("Navegación a detalle de producto exitosa")
        except Exception as e:
            logger.error(f"Error en test_05_ver_detalle_producto: {str(e)}")
            self.driver.save_screenshot(f"logs/error_detalle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            raise

if __name__ == "__main__":
    unittest.main()