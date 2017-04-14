README


EJERCICIO 1


Ejercicio 2: Modelo de n-gramas                         LISTO!

Implementa un modelo de n-gramas con conteo de apariciones. Se agregan
marcadores de inicio y fin de oración para evitar underflow en el cálculo de
probabilidades.
Para el cálculo de prob_cond se contempló el caso de división por cero, mientras
que para sent_prob se agregan marcadores de inicio y fin de oración, cuando
necesario, para encontrar coincidencia con el diccionario de counts.
Las probabilidad sent_log_prob es muy parecida a sent_prob, solo que consiste
en una suma de logaritmos.
Una primera implementación (chancha), disponible en commints viejos, pasaba los
tests (tests/test_ngram.py) pero al probar con n > 2 no funcionaba. Se volvió
a pensar la estructura casi desde cero, y quedó código mas legible.
Los tests dados requerían de estructuras fijas que debieron ser copiadas. Sirvió
de mucho en mi caso (a pesar de las no menores dificultades para comprender
la idea) el pedir una estructura fija.


Ejercicio 3: Generación de Texto        FALTA GENERACION DE PALARAS con 1,2,3,4

Para NGramGenerator se optó por NO guardar la lista de sentencias, ya que se
trata de un duplicado innecesario en memoria del texto crudo.
Se intentó implementar NGramGenerator como clase hija de NGram.
Pudo haber sido el caso, sin embargo, era muy útil contar con la lista completa
de sentencias para ser procesadas y sacar, por ejemplo, las primeras palabras
de cada oración en el modelo. Luego de eso (y un poco por falta de tiempo), se
dejó la implementación como estaba a sabiendas que se pueden hacer mejoras,
pendientes a futuro.
Una explicación del algoritmo para construir el diccionario de probabilidades
está disponible en los comentarios de ngram.py. Y con respecto a sorted_probs
es una simple transformación de los values del diccionario probs a lista, y un
ordenamiento
Se encuentran más notas explicativas en el código de ngram.py (de nuevo, un poco
mezclado) y en scripts/generate.py


Ejercicio 4: Suavizado "add-one"        FALTA guardar los modelos resultantes para varios valores de n (1, 2, 3 y 4).

La implementación de AddOneNGram sí es bastante más acertada que la de
NGramGenerator. En ella se hizo herencia de forma correcta. Se sobreescribió
la función cond_prob, por la diferencia en el cálculo que, notemos, no puede
ser rehusada (esto debido a que dado el resultado de un cociente no se pueden
realizar operaciones aritméticas para sumar constantes tanto al numerador
como al denominador).
Queda sin embargo el cálculo del tamaño del alfabeto implementado en la clase
padre (i. e. NGram). Ésto debido a que para dicho cálculo es mucho más práctico
el procesamiento del texto crudo.
