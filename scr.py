class AnalizadorSintactico:
    tabla_predictiva = {
        'P': {
            'INICIO': ['INICIO','se_sent', "FIN"]
            
        },
        "se_sent": {
            'id': ['sent',';','se_sent'],
            'write': ['sent',';','se_sent'],  # Caso de vacío
            'Tdato': ['sent',';','se_sent'],  # Caso de vacío
            'FIN': [],  # Caso de vacío
            ';': ['sent',';','se_sent'],  # Caso de vacío
        },
        'sent': {
            'id': ['id','=','exp'], 
            'write': ['write', '(', 'exp','l2' ')'],
            'Tdato': ['de_var'],
            ';': ['de_var'],
        },
        'de_var': {
            'Tdato': ['de_renglon',';''de_var'],
            ';': [],
        },
        'l': {
            ',': ['id', 'l'],
            ';': []
        },
        'l2': {
            ',': ['exp', 'l2'],
            ';': []
        },
        
        'de_renglon': {
            'Tdato': ['Tdato''id', 's1']
        },
        
        's1': {
            ',': ['l'],
            '=': ['exp'],
            ';':['l']
        },
        
        'exp': {
            'id': ['=', 'exp'],
            '(': ['exp','s2']
        },
        's2': {
            ',': [],
            ')': [],
            'OA': ['OA','exp'],
            ';': []
        }
        
    
        
        
    }

    def obtener_produccion(cls,no_terminal, siguiente_simbolo):
        return cls.tabla_predictiva[no_terminal][siguiente_simbolo]



    def validar_cadena(cls, cadena):
        
        caracteres_especiales = ['id', '+', '*', '(', ')','INICIO','write', 'Tdato',',', '=','FIN','OA', ';']
        for caracter in caracteres_especiales:
            cadena = cadena.replace(caracter, caracter + ' ')
        
        cadena_tokens = [token for token in cadena.split() if token != ''] + ['$']
        pila = ['$', 'P']
        indice = 0

        print("Cadena de entrada:", ' '.join(cadena_tokens))  

        while len(pila) > 0:
            simbolo_pila = pila.pop()
            
            # Manejar caso de fin de cadena
            if indice >= len(cadena_tokens):
                simbolo_actual = '$'
            else:
                simbolo_actual = cadena_tokens[indice]

            if simbolo_pila == simbolo_actual:
                indice += 1
            else:
                if simbolo_pila in cls.tabla_predictiva and simbolo_actual in cls.tabla_predictiva[simbolo_pila]:
                    produccion = cls.tabla_predictiva[simbolo_pila][simbolo_actual]
                    if produccion:
                        pila.extend(reversed(produccion))
                    else:
                        continue

            print("Pila:", pila)
            print("Cadena de entrada actual:", ' '.join(cadena_tokens[indice:]))  

        if simbolo_pila == '$' and simbolo_actual == '$':
            return "La cadena es válida."
        else:
            return "La cadena no es válida."


    def validar_archivo(cls, nombre_archivo):
            todas_validas = True  

            with open(nombre_archivo, 'r') as archivo:
                
                for linea in archivo:
                    
                    cadena_validar = linea.strip()
                    resultado = cls.validar_cadena(cadena_validar)
                    print(f"La cadena '{cadena_validar}' es: {resultado}")

                    if resultado == "La cadena no es válida.":
                        todas_validas = False  # Si alguna cadena es inválida, actualiza la bandera

           
            if todas_validas:
                print("El código fuente es correcto, todas las cadenas son válidas.")
            else:
                print("El código fuente contiene errores.")