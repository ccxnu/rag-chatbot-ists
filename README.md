# RAG Chatbot ISTS

Este repositorio contiene un chatbot basado en Retrieval-Augmented Generation (RAG)
desarrollado como parte de un proyecto del [ISTS](https://tecnologicosudamericano.edu.ec/).
El chatbot utiliza técnicas de recuperación de información y generación de lenguaje
natural para proporcionar respuestas basadas en la información disponible en una base de datos.

## Características

- **Retrieval-Augmented Generation (RAG)**: Combina modelos de lenguaje preentrenados
con técnicas de recuperación de documentos para mejorar la precisión y relevancia de las respuestas.
- **Integración con fuentes de datos**: Recupera información relevante de una base
de datos para enriquecer las respuestas del chatbot.
- **Modelo de lenguaje avanzado**: Basado en modelos de lenguaje de última generación
para la generación de respuestas coherentes y contextuales.

## Requisitos

Antes de ejecutar el proyecto, asegúrate de tener instaladas las siguientes dependencias:

- [Python 3.8+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [Ollama](https://ollama.com/library/llama3.1)
- [Langchain](https://python.langchain.com/v0.2/docs/introduction/)
- Otros requisitos mencionados en `requirements.txt`

## Instalación

1. Clona este repositorio en tu máquina local:

   ```bash
   git clone https://github.com/ccxnu/rag-chatbot-ists.git
   ```

2. Navega al directorio del proyecto:

   ```bash
   cd rag-chatbot-ists
   ```

3. Instala las dependencias necesarias:

   ```bash
   pip install -r requirements.txt
   ```

## Uso

Para ejecutar el chatbot, puedes usar el siguiente comando:

```bash
python app.py
```

Esto iniciará el servidor del chatbot que estará listo para recibir consultas y proporcionar respuestas basadas en la información recuperada.
Asegurate de tener ollama server corriendo.

## Estructura del Proyecto

- `main.py`: Archivo principal para iniciar el chatbot.
- `requirements.txt`: Lista de dependencias del proyecto.
- `chroma/`: Directorio donde se almacenan los datos utilizados para la recuperación de información.
- `pdf_files/`: Contiene los archivos pdf que se suben.

## Contribuciones

Si deseas contribuir al proyecto, por favor sigue los siguientes pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y realiza commits descriptivos.
4. Envía un pull request detallado para revisión.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contacto

Para cualquier pregunta o comentario, puedes contactarme a través de correo electrónico [Pablo Cuenca](mailto:pacuencac@ists.edu.ec).
