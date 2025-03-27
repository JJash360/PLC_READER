# PLC_READER
Interfaz gráfica en Python con PyQt5 para comunicarse con PLC Siemens usando Snap7. Permite leer y escribir datos en la memoria del PLC de forma sencilla y eficiente.

## Características
- Interfaz gráfica interactiva con PyQt5.
- Conexión con PLC Siemens mediante Snap7.
- Lectura y escritura de datos en la memoria del PLC.
- Fácil integración y escalabilidad.

## Instalación
Asegúrate de tener Python 3.8+ instalado y luego ejecuta:

```bash
pip install PyQt5 snap7
```

Para Raspberry Pi, puedes instalar PyQt5 con:

```bash
sudo apt install python3-pyqt5
```

## Uso
Ejecuta el script principal para iniciar la interfaz gráfica:

```bash
python main.py
```

## Licencia
Este proyecto está licenciado bajo la licencia **MIT**. Para más detalles, consulta el archivo `LICENSE` en este repositorio.

## Dependencias y Licencias
Este software usa las siguientes bibliotecas de terceros:

- Snap7 - Licencia EUPL [(ver aquí)](https://github.com/klemenzagar/snap7)  
- PyQt5 - Licencia GPL [(ver aquí)](https://riverbankcomputing.com/software/pyqt/license)  

📌 **Nota sobre PyQt5:** PyQt5 usa la licencia GPL, lo que significa que si distribuyes un binario de este software, **debes compartir el código fuente**. Si deseas evitar esta restricción, considera usar PySide6, que está bajo licencia LGPL.

## Autores
- **Jashua Jafet Solon Aquino**
- **Jeremy Lorenzo Calderon Alvarado**


