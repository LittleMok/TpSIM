from scipy.stats import chi2
from Modulos.Constantes import ResultadosChi2

def EstadisticoChi2(frec_obs, frec_esp):
    ''' 
    La funcion devuelve el valor del estadistico Chi^2 para los valores de frecuencia esperada y observada
    Parametros: frec_obs : int Frecuencia observada para un intervalo
                frec_esp : int Frecuencia esperada para un intervalo
    '''
    return ((frec_obs - frec_esp) ** 2) / frec_esp

def EstadisticoChi2Acumulado(frec_obs, frec_esp=None,):
    '''
    La funcion calcula el valor acumulado para el estadistico Chi^2 segun una lista de frecuencias observadas
    Parametros: frec_obs : List<int> Lista de valores de frecuencias observadas
                frec_esp : List<int> Parametro opcional, contiene los valores de frecuencias esperadas para cada intervalo
    
    Retorno: grados_libertad : int Grados de libertad calculados para la cantidad de intervalos dados
             chi2_acu : float Valor acumulado para el estadistico chi^2
             chi2_valores : Lista de valores del estadistico chi^2 para cada intervalo
    '''
    chi2_valores = []
    chi2_acu = 0
    grados_libertad = len(frec_obs) - 1
    if frec_esp is None:
        val = sum(frec_obs) / len(frec_obs)
        frec_esp = list([val for i in range(len(frec_obs))])

    for i in range(len(frec_obs)):
        ci = EstadisticoChi2(frec_obs[i],frec_esp[i])
        chi2_acu += ci
        chi2_valores.append(round(ci,2))
    return grados_libertad, round(chi2_acu,2), chi2_valores

def ContarFrecuencias(lista_valores, intervalos):
    ''' La funcion devuelve la cantidad de valores de la lista que se ajustan a cada intervalo
        Parametros: lista_valores : List<float> Lista de valores sobre la que se va a trabajar
                    intervalos : Dict<str, extremos_intervalo> Diccionario que contiene la representacion como string del intervalo como clave
                                                                y una lista de dos elementos extremos como valor 
                    extremos_intervalo: [extremo_inferior, extremo_superior] Parametro implicito contenido dentro del diccionario
        Retorno: Dict<str,int> Diccionario que contiene la cantidad de elementos encontrados para cada intervalo
    '''
    contador_intervalos = {k:0 for k in intervalos.keys()} #Inicializa los contadores utilizando las claves del diccionario pasado como parametro como claves propias
    
    for k,v in intervalos.items(): #Se itera sobre todos los intervalos pasados como parametro
        contador_intervalos[k] = len(list(
            filter(lambda x: v[0] <= x and x < v[1], lista_valores) #Se filtra la cantidad de elementos de lista_valores que esta contenido en un intervalo dado
        ))
    return contador_intervalos

def CrearLimitesIntervalos(cantidad_intervalos):
    '''
    La funcion crea una lista auxiliar utilizada para contener los extremos de los intervalos
    '''
    amplitud_intervalo = round(1 / cantidad_intervalos, 4)
    limites_intervalos = [0.0] * (cantidad_intervalos + 1)
    for i in range(len(limites_intervalos) - 1):
        limites_intervalos[i + 1] = round(limites_intervalos[i] + amplitud_intervalo, 3)
    return limites_intervalos

def CrearIntervalos(limites_intervalos):
    '''
    La funcion crea el diccionario de intervalos que se utilizara para contabilizar los valores por cada uno de ellos
    Parametros: limites_intervalos : List<Float> contiene los valores extremos de los intervalos a crear
    Retorno: intervalos Dict<str, extremos> Diccionario que utiliza como clave la representacion del intervalo. Su valor es una lista con los valores extremos del mismo
             extremos [extremo_inferior, extremo_superior] Retorno implicito dentro del diccionario. Tiene dos elementos, cada uno representando un extremo del intervalo
    '''
    intervalos = {
        str(limites_intervalos[i]) + " - " + str(limites_intervalos[i+1]): [limites_intervalos[i], limites_intervalos[i + 1]] 
        for i in range(len(limites_intervalos) - 1)
        } #Se utiliza comprension de listas para generar el diccionario
    return intervalos

def PruebaChiCuadrado(lista_valores, cantidad_intervalos, nivel_significancia):
    '''
    La funcion realiza la prueba de Chi^2 sobre una lista de valores dados
    Parametros: lista_valores List<float> lista de valores sobre los cuales se desea realizar la prueba
                cantidad_intervalos int : Cantidad de intervalos que se utilizaran para clasificar los datos de prueba
                nivel_significancia float : Define como la probabilidad de tomar la decisión de rechazar la hipótesis nula cuando ésta es verdadera
    Retorno: ResultadosChi2 : Constante que define el resultado de la prueba
             chi2_inter Dict<str,float> : Diccionario que contiene el valor calculado de Chi^2 para cada intervalo
             grados_libertad int : Grados de libertad calculados para la cantidad dada de intervalos
             contador_intervalos Dict<str,int> : Diccionario con la frecuencia observada para cada intervalo
             chi2_ac float : Valor acumulado del estadistico chi^2 utilizado para la decision respecto a la H0

    '''
    limites_intervalos = CrearLimitesIntervalos(cantidad_intervalos)
    intervalos = CrearIntervalos(limites_intervalos)
    contador_intervalos = ContarFrecuencias(lista_valores,intervalos)  
    grados_libertad, chi2_ac, chi2_lista = EstadisticoChi2Acumulado(list(contador_intervalos.values()))
    valor_critico = chi2.ppf(1 - nivel_significancia, grados_libertad)
    chi2_inter = {list(contador_intervalos.keys())[i]:chi2_lista[i] for i in range(len(contador_intervalos.keys()))}

    if chi2_ac < valor_critico:
        return ResultadosChi2.H0_NO_RECHAZABLE, chi2_inter, grados_libertad,contador_intervalos, chi2_ac
    else:
        return ResultadosChi2.H0_RECHAZADA, chi2_inter, grados_libertad,contador_intervalos, chi2_ac

def testEstadisticoChi2Acumulado():
    '''
    Metodo de prueba utilizado para comprobar el buen funcionamiento del modulo
    Utiliza valores constantes obtenidos de los apuntes para verificar si el resultado obtenido de la prueba es correcto

    '''
    print("*****************************************")
    print("Metodo de prueba")
    print("Utiliza los valores dados en el apunte para verificar el funcionamiento del metodo de calculo de la prueba de Chi^2")
    obs_dict = [8,7,5,4,6] #Cada elemento de la lista representa la frecuencia observada de un intervalo
    grados_libertad,valor_chi2,chi2_lista = EstadisticoChi2Acumulado(obs_dict)

    print("Los grados de libertad son: ", grados_libertad)
    print("El estadistico calculado es: ",valor_chi2)
    print("Los valores calculados de chi2 son: ", chi2_lista)
    nivel_significancia = float(input("Ingrese el nivel de significancia: "))
    
    nivel_confianza = 1 - nivel_significancia

    valor_critico = chi2.ppf(nivel_confianza,grados_libertad)
    if valor_chi2 < valor_critico:
        print("No se puede rechazar la hipotesis nula...")
    else:
        print("Se rechaza la hipotesis nula...")

def testPruebaChi2():
    '''
    La funcion utiliza los valores dados en el apunte de la catedra para verificar el comportamiento de la prueba Chi^2
    '''
    arr = [0.15,0.22,0.41,0.65,0.84,0.81,0.62,0.45,0.32,0.07,0.11,0.29,0.58,0.73,0.93,0.97,0.79,0.55,0.35,0.09,0.99,0.51,0.35,0.02,0.19,0.24,0.98,0.10,0.31,0.17]
    nivel_significancia = 0.5
    cantidad_intervalos = 5
    resultado,lista_chi2,grados_libertad,dict_intervalos,valor_chi2 = PruebaChiCuadrado(arr,cantidad_intervalos,nivel_significancia)
    if resultado == ResultadosChi2.H0_RECHAZADA:
        print("La funcion no se comporta de manera esperada")        
    else:
        print("La funcion se comporta correctamente")
        print(resultado)
        print(lista_chi2)
        print(grados_libertad)
        print(dict_intervalos)
        print(valor_chi2)

if __name__ == "__main__":
    testEstadisticoChi2Acumulado()
    testPruebaChi2()