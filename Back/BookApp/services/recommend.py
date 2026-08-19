#imports
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics.pairwise import cosine_similarity

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

    join_list = [target]+candidates

    mlb = MultiLabelBinarizer()
    join_binaries = mlb.fit_transform(join_list)

    v_target = joinBinaries[0:1]
    v_candidates = joinBinaries[1:]

    similarities = cosine_similarity(v_target, v_candidates)

    #Devolverá tantos índices del vector como comparaciones se realicen
    return similarities


#Normalización entrada
    #Tomar listas como argumentos

    #to lower case

    #devolver las listas normalizadas