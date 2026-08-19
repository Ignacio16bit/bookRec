#imports
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity
import re

#Normalización entrada
def normalize(subject_list):
    if not subject_list:
        return []
    
    normalized =[]
    
    for item in subject_list:
        item_str = str(item)

        #Eliminar caracteres y espacios
        item_str = item_str.lower()
        item_str = re.sub(r'[^a-z0-9\sáéíóúüñ]','',item_str)
        item_str= re.sub(r'\s+',' ', item_str).strip()
        
        if item_str:
            normalized.append(item_str)

    return normalized

#Vectorización
def vectorizer(target, candidates):
    '''
    Covierte las listas de género en vectores binarios para calcular sus similitudes (de coseno) sobre un plano de n dimensiones

    Parámetros:
        target: list -> Temas del libro buscado
        candidates: list of lists -> Temas de los libros candidatos (obtenidos por API)

    Devuelve:
        Matriz de similitudes de tamaño (1, len(candidates))
        Cada valor es la similitud del coseno entre target y ese candidato
    '''

    if not target or len(target) == 0:
        print('No existe un libro de referencia.')
        return None

    if not candidates or len(candidates) ==0:
        print('No se  encontraron libros para comparar. Pruebe de nuevo')
        return None

    norm_target = normalize(target)
    norm_candidates = [normalize(c) for c in candidates]

    join_list = [norm_target]+norm_candidates

    mlb = MultiLabelBinarizer()
    join_binaries = mlb.fit_transform(join_list)

    v_target = join_binaries[0:1]
    v_candidates = join_binaries[1:]

    similarities = cosine_similarity(v_target, v_candidates)

    #Devolverá tantos índices del vector como comparaciones se realicen
    return similarities [0]