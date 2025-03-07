# Proyecto de Automatización de Pruebas con Selenium para MercadoLibre - Rafael Emilio Abreu Valdez

Este proyecto demuestra la automatización de pruebas utilizando Selenium WebDriver para evaluar la funcionalidad del sitio web de MercadoLibre.

## Objetivo del Proyecto

El objetivo principal es crear una suite de pruebas automatizadas que permita verificar las funcionalidades básicas del sitio web de MercadoLibre, incluyendo:

- Navegación a la página principal
- Selección de país
- Búsqueda de productos
- Filtrado de resultados
- Acceso a detalles de productos

## Configuración del Entorno

### Requisitos Previos

- Python 3.7 o superior
- Pip (gestor de paquetes de Python)
- Navegador Chrome instalado

### Instalación

1. Clonar este repositorio:

   ```
   git clone https://github.com/usuario/selenium-mercadolibre-test.git
   cd selenium-mercadolibre-test
   ```

2. Crear un entorno virtual (opcional pero recomendado):

   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. Instalar las dependencias:
   ```
   pip install -r requirements.txt
   ```

## Estructura del Proyecto

```
selenium-mercadolibre-test/
├── main.py   # Archivo principal de pruebas
├── requirements.txt       # Dependencias del proyecto
├── README.md              # Documentación del proyecto
└── logs/                  # Directorio para archivos de registro
```

## Escenarios de Prueba

El proyecto automatiza los siguientes escenarios:

1. **Navegación a la página principal**: Verifica que se pueda acceder a la página de inicio de MercadoLibre.
2. **Selección de país**: Comprueba que se pueda seleccionar un país específico (México).
3. **Búsqueda de productos**: Valida que funcione correctamente la búsqueda de productos.
4. **Filtrado por condición**: Verifica que se puedan aplicar filtros a los resultados de búsqueda.
5. **Ver detalle de producto**: Comprueba que se pueda acceder a la página de detalle de un producto.

## Implementación de las Pruebas

Las pruebas están implementadas utilizando:

- **Selenium WebDriver**: Para interactuar con el navegador y la interfaz de usuario.
- **unittest**: Framework de pruebas unitarias de Python.
- **Webdriver Manager**: Para la gestión automática del controlador de Chrome.
- **Logging**: Para registrar información detallada de la ejecución de las pruebas.

### Buenas Prácticas Implementadas

- **Page Object Model (POM)**: Aunque no implementado completamente, el código sigue la estructura básica del patrón POM.
- **Esperas explícitas**: Se utilizan para garantizar que los elementos estén disponibles antes de interactuar con ellos.
- **Logging**: Registro detallado de acciones y resultados.
- **Screenshots en caso de error**: Se guardan capturas de pantalla cuando ocurren errores para facilitar el diagnóstico.

## Ejecución de Pruebas

Para ejecutar todas las pruebas:

```
python -m unittest main.py
```

Para ejecutar una prueba específica:

```
python -m unittest main.MercadoLibreTest.test_01_navegar_a_mercadolibre
```

## Informes de Pruebas

Los informes se generan automáticamente en forma de registros en el directorio `logs/`. Cada ejecución crea un archivo de registro con fecha y hora.

También se generan capturas de pantalla en caso de error, que se guardan en el mismo directorio.
