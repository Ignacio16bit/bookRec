* La aplicación se trata de un sistema de recomendación de libros en base a la entrada de un usuario. Es decir, presentado con un libro el sistema devolverá una lista (o uno sólo) que guarde relación y suponga una experiencia de lectura cercana.

# 1. Arquitectura
La aplicación está diseñada con una arquitectura desacoplada basada en servicios web (con API REST). El backend se construye con Django, que implementa internamente el patrón Modelo-Vista-Plantilla. Aún así en este proyecto se limita a actuar como proveedor de API de datos (modelos y vistas) mediante Django REST Framework (DRF).

El frontend se delega al completo a React con TypeScript en un concepto de SPA, asumiendo el rol de interfaz de usuario.

La separación responde a la necesidad de aislar el tratamiento de datos (mediante un algoritmo de recomendación) de la interfaz, manteniendo la agilidad a lo largo del sistema. Además se simplifica la estructura del proyecto evitando la complejidad de una arquitectura de microservicios.    

## 1.1 Flujo de datos

1. El usuario introducirá en un buscador el libro del que precisa la recomendación. 

2. El front (React) realiza la petición HTTP al back (Django) mediante Axios.

3. El back procesa la solicitud. Consultará la API de libros para verificar o enriquecer la información y, posteriormente, ejecutar el algoritmo de recomendación.

4. El algoritmo contrasta el libro buscado con el sistema de etiquetas. En él, se **cuantifica** la coincidencia de etiquetas mediante un **índice de cercanía**.

5. Django sólo devolverá en la respuesta cualquier libro que cumpla con:
    - x>= 0.75  (En un rango -1/1)

6. Sólo en ese caso se devolverá el JSON con los libros recomendados y se renderizarán en pantalla.
    
## 1.2 Almacenamiento de datos

El sistema no almacena los libros en su base de datos. En su lugar, cada solicitud de recomendación funciona de la siguiente manera:
1. Consulta a la API de Google Books para obtener libro de entrada.

2. Recuperar categoría del libro.

3. Consulta de nuevo a la API para obtener libros potenciales para comparar.

4. Calcular similitud en tiempo real y devolver las recomendaciones.

Se toma esta decisión para mantener la base de datos ligera y garantizar que los datos se mantengan actualizados, a costa de un mayor consumo de la cuota de la API.

A futuro, una vez superado el MVP, se plantea la inclusión de un sistema de caché de manera que guarde resultados durante un periodo de tiempo establecido y cuente con recomendaciones "precalculadas" en las búsquedas que se identifquen como frecuentes con el objetivo de evitar el Rate Limiting o la latencia elevada.
    
## 1.3 Stack tecnológico
* **Backend**: Django 6.0.7 (bajo el lenguaje de programación Python 3.14.4).
* **API REST**: Django REST Framework (DRF) para la creación y gestión de los endpoints.
* **Frontend**: React estructurado con VIte y tipado en TypeScript.
* **Cliente HTTP**: Axios para la comunicación asíncrona entre cliente-servidor
* **Gestor de paquetes**: pnpm; elegido por seguridad, velocidad y gestión eficiente de dependencias con enlaces duros.
    
# 2. Instalación y despliegue
## 2.1 Backend (Django)
Al trabajar con Python es necesario el uso de entornos virtuales para aislar las dependencias:
1. Clonar el repositorio y acceder a la carpeta de backend.

2. Crear y activar el entorno virtual:
    * **UNIX**: `source venv/bin/activate`
    * **Windows**: `venv\Scripts\activate`
    
3. Instalar las dependencias del proyecto.
    * `pip install -r requirements.txt`

4. Crear el archivo .env en la raíz y configurar las variables de entorno. Pueden ser la clave secreta en Django y las API Keys de la API externa.
5. Aplicar las migraciones a la base de datos local
    * `python manage.py migrate`

6. Levantar el servidor de desarrollo
    * `python manage.py runserver`
    
## 2.2 React

1. Acceder a la carpeta de frontend.

2. Instalar el árbol de dependencias con pnpm:
    * `pnpm install`

3. Configurar las variables de entorno necesarias. Por ejemplo, la URL base de la API de Django en un .env.local.

4. Iniciar el servidor locar de Vite
    * `pnpm run dev` (o de forma abreviada `pnpm dev`)
    
# 3. Flujo y lógica de algoritmo de recomendación
Para el sistema de recomendación hay que explicar en primer lugar el algoritmo usado para ello. 
    
## 3.1 Similitud de coseno
El algoritmo de **similitud de coseno** supone una medida de similitud dentro del espacio interno que mide el coseno del ángulo entre dos vectores. Es decir, mide la similitud de n listas de vectores, calculando el coseno del ángulo entre ambos. De esta manera se permite trabajar con los siguientes datos:
* cos 0ª = 1   //   cos 90ª = 0    // cos 180ª = -1

Así en 0ª la coincidencia entre ambos vectoras será la **mayor coincidencia** y 90ª la **menor coincidencia**.

Por incidir, supone recoger los datos (géneros de un libro) y una vez encapsulados en un vector (array) este se representará en un gráfico de tantas dimensiones como vectores precisemos. Así permite comparar la orientación de los vectores en el espacio con independencia de su magnitud. Se logra mediante su norma, calculada a través del producto punto consigo mismo. De esta manera, dos libros con diferentes números de categorías pueden compararse de manera justa, ya que lo que importa en la proporción de categorías compartidas, no su cantidad absoluta.
    
## 3.2 Algoritmo

El objetivo así, es contar con un índice de recomendación que venga dado por la similitud de los cosenos, y así poder establecer un rango aceptable de recomendación. En este caso se establece un umbral de similitud de **0.75**. Sólo se consideraran como recomendaciones válidas aquellos libros cuyo coseno de similitud sea mayor o igual a ese índice. Garantiza que las recomendaciones tengan una coindicencia significativa evitando sugerencias más divergentes.
    
## 3.3 Observaciones
Hay que tener en cuenta el *error aceptable*. Se plantea sobre todo en base a la pregunta de "¿Cómo se recomienda algo?"; no es siempre en base a un género o unas etiquetas clave, suele ser una opinión más guiada por sensaciones y la experiencia. Obviamente, es difícil establecer un rango entonces de recomendación, cuantos más datos recojan los vectores más cercanas podrán ser las recomendaciones pero también más centradas en un campo dadas las cardinalidades y los sesgos.

La solución no es, por tanto, un algoritmo más complejo, si no un buen etiquetado de los libros que atienda a campos más diversos que el género.

Es una tarea que en esta situación es inabarcable como solo-dev, no sólo por el tiempo necesario sino también por los propios sesgos personales. Sería necesario un equipo dedicado a encontrar la manera de acertar más exactamente con un campo más universal. Mientras tanto, el algoritmo se plantea como un mínimo entregable que se centrará en **recomendar en base al género**; con la idea de mejorar el sistema en futuras actualizaciones mediante enriquecimiento de los vectores.
    
## 3.4 Futuras mejoras
- Análisis semánticos de sinopsis. Procesamiento de Lenguaje Natural para extracción de temas, conceptos y entidades.

- Factor autor. Cuantificar la similitud entre autores como criterio adicional.

- Filtrado colaborativo. Inclusión de otro algoritmo adicional para incorporar valoraciones y comportamientos de usuarios.
   
# 4. API externa de los libros
Se usará la API de Google Books para la obtención de los datos precisados. Se valoró el uso de Open Library de código abierto, plantea sin embargo, un problema de gran calado para el proyecto actual.

Al ser de código abierto y de libre edición el endpoint que se usaría (`/subjects`) no daría resultados consistentes ya que cada usuario puede haber completado ese campo con una terminología distinta. Por ejemplificar:
- ROMANCE =/= romance      (No son tratadas como la misma categoría)

Frente a ello se opta por la API de Google al contar con un sistema estandarizado de temáticas bajo el endpoint `/volumes` con el campo `categories` en `volumeInfo`.
    
## 4.1 Conexión
### 4.1.1 Autenticación y autorización
Desde la documentación de Google Books se aclara el proceso de acceso, aquí se recogen a continuación aclaraciones respecto al proyecto.
- No se usará OAuth 2.0 al no ser necesario el acceso a datos privados, en su lugar se usará simplemente la clave API en la URL de la solicitud.
- Se usará una clave API pese a poder lanzar solicitudes sin ella. Se debe a que la cuota sin claves o sin autenticar es más limitada.

### 4.1.2 Obtención de API Key
Se siguen los pasos necesarios y detallados en la documentación.
1. Creación de proyecto en Google Cloud Console.

2. Activación de Books API en APIs y servicios.

3. Generación de clave API en "Create credentials".
    
### 4.1.3 Uso de clave API
La clave se añadirá como parámetro de consulta en las solicitudes a la API, es decir:
- `GET https://www.googleapis.com/books/v1/volumes?q={título}&key=API_KEY`

La clave (de acuerdo a la documentación) puede incrustarse de forma segura en las URLs sin codificación adicional.
    
### 4.1.4 Endpoints relevantes
- `/volumes` -> Búsqueda de libros / q (consulta de búsqueda), maxResults.

- `/volumes/{volumeId}` -> Obtención de libro específico / volumeId (identificador único).
    
## 4.2 Implementación en Django
La conexión a la API de Google se implementará en una vista de Django REST Framework, que usará la librería `requests` para realizar peticiones HTTP.

La vista se esctructura de la siguiente manera:
```python
class GoogleBooksSearchView(APIView):
    def get(self, request):
        #1. Obtener término de búsqueda
        #2. Preparar URL con API Key
        #3. Realizar petición a la API
        #4. Procesar respuesta y extraer categorías
        #5. Ejecutar algoritmo
        #6. Devolver resultados al front
```
### 4.2.2 Configuración de variables de entorno
La API Key se almacena en un archivo .env y se carga en settings.py con python-decouple o django-environ para mantener seguridad.

### 4.2.3 Manejo de errores
Se implementa un manejo de errores que contemple:
- Falta de clave de API configurada
- Fallo de conexión con Google Books
- Límite de cuotas excedidos
- Resultados de búsqueda vacíos

# 5. API interna - Contrato de API
Se opta por un único endpoint para simplificar la interacción cliente-servidor. Esto reduce la latencia y la complejidad del frontend; el backend se encarga de toda la lógica de la búsqueda, obtención de categorías y cálculo del algoritmo en una sola operación. 
    
## 5.1 Endpoints
Recomendaciones de libros

- **Endpoint**: /api/recommendations/
- **Método**: GET
- **Parámetros**: q / String / Obligatorio / Título o término de búsqueda
    - `GET /api/recommendations/?q=el+nombre+del+viento`
- **Response 200 OK**:
    ```JSON
    {
        "input_book":{
            "title": "El nombre del viento",
            "author": ["Rothfuss, Patrick"],
            "categories": ["Fiction", "Fantasy"]
        },
        "recomendations": [{
            "title": "Imperio final",
            "author": ["Sanderson, Brandon"],
            "categories": ["Fiction", "Fantasy"],
            "similarity_cos": 0.92
        }],
        "total":5
    }
    ```
    **Códigos de error**:
    - 400 - Falta parámetro `q` o la búsqueda es inválida.
    - 404 - No se encontró un libro por ese término.
    - 503 - Error al conectar con la API de Google Books.
    
Se persigue una estructura limpia, **RESTful** y escalable. En futuras actualizaciones se permite añadir más funcionalidades (como filtros) extendiendo el endpoint con parámetros adicionales en lugar de crear nuevos.

# 6. Estructura frontend
El frontend se desarrolla como una Single Page Application SPA usando React con TypeScript. La arquitectura está basada en componentes funcionales y hooks, priorizando una interfaz de usuario reactiva y mantenible.

La estructura sigue el principio de separación de responsabilidades, es decir:

    src/
    ├── components/
    ├── pages/
    ├── services/
    ├── hooks/
    ├── types/
    ├── utils/
    └── styles/ 
    
## 6.1 Gestión de estados
Para la gestión del estado de la aplicación se usa el contexto nativo de React (useContext) combinándolo con hooks personalizados. La decisión se da por la simplicidad, el tipado seguro y la mantenibilidad.
    
## 6.2 Comunicación con backend (Axios)
Para la comunicación asíncrona entre frontend y backend se usa la librería Axios, que proporciona una interfaz más robusta que el fetch nativo en React. La instancia centralizada incluye:
```JavaScript
// services/apiClient.ts
import axios from 'axios';
const apiClient = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    },
});
export default apiClient;
```
Por otro lado las llamadas a la API se encapsulan en servicios específicos que devuelven los datos tipados, manteniendo la lógica de comunicación separada de los componentes.
    
## 6.3 Flujo de datos
Sigue un patrón unidireccional (característico de React).
1. El usuario introduce un término de búsqueda en el campo de entrada.
2. Evento de búsqueda al enviar el formulario. Actualiza el estado de carga y llama al servicio de API.
3. El servicio realiza la llamada asíncrona con la petición al backend.
4. Al recibir la respuesta, el estado se actualiza con los datos.
5. Re-renderizado de la interfaz con los resultados o un mensaje de error.

## 6.4 Estados y componentes
El componente principal maneja tres estados fundamentales:
```JavaScript
const [query, setQuery] = useState('');
const [data, setData] = useState<RecommendationResponse | null>(null);
const [loading, setLoading] = useState(false);
const [error, setError] = useState<string | null>(null);
```

Los componentes principales serán:
- SearchBar -> Captura la entrada y dispara la búsqueda con Props de callback para el envío de formulario.
- BookList -> Renderiza el libro de entrada y las recomendaciones. Usa props de array de libros y metadatos de respuestas (BookCard subcomponente).
- BookCard -> Muestra la información de un libro. Usa props para título, autor, categorías, imagen.

# 7. Modelo de datos
Se usa esta estructura para la representación de un libro
```JSON
{    
    "id": "string",
    "title": "string",
    "author": ["string"],
    "categories": ["string"],
    "description": "string",
    "image_url": "string"
}
```
Esta estructura se obtiene de la respuesta de Google Books, y se usará para la visualización en front y para el cálculo del algoritmo de similitud.
