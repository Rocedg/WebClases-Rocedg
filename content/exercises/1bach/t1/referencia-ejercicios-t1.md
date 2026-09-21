# Banco editorial T1 v1 - Movimiento rectilíneo

**Curso:** 1.º de Bachillerato  
**Tema:** T1 - Movimiento rectilíneo  
**Estado:** referencia editorial para construir el catálogo JSON  
**Fecha:** 14 de septiembre de 2026

## 1. Propósito del banco

T1 transforma las herramientas de T0 en lectura física de un movimiento sobre una recta. El banco no debe limitarse a sustituir datos en una fórmula: el alumno debe poder elegir un sistema de referencia, construir o interpretar funciones de tiempo y pasar entre las cuatro representaciones de un mismo movimiento:

1. descripción verbal o diagrama de la recta;
2. tabla de datos;
3. función o ecuación;
4. gráficas `x(t)`, `v(t)` y `a(t)`.

El catálogo inicial contiene **60 ejercicios**, con más problemas de varios apartados que T0. Los ejercicios largos deben parecerse a pequeñas investigaciones: extraer información, representar, calcular y comprobar coherencia.

| Bloque | IDs | Cantidad |
|---|---:|---:|
| Referencia, posición y representaciones | `t1_r_001`-`t1_r_008` | 8 |
| MRU, encuentros y movimiento relativo | `t1_u_001`-`t1_u_012` | 12 |
| MRUA y movimiento vertical rectilíneo | `t1_a_001`-`t1_a_014` | 14 |
| Funciones y gráficas temporales | `t1_g_001`-`t1_g_016` | 16 |
| Problemas integradores y fuentes PAU | `t1_i_001`-`t1_i_010` | 10 |
| **Total** |  | **60** |

## 2. Contrato editorial común

1. La dirección positiva de la recta se declara antes de usar signos. Si se toma hacia el este, derecha o arriba, debe quedar escrito en el enunciado y reflejado en el diagrama.
2. Posición, desplazamiento, distancia recorrida, rapidez, velocidad y aceleración no son intercambiables. Las soluciones deben nombrar la magnitud que calculan.
3. Las gráficas deben tener ejes, unidades, escala y tramo temporal explícitos. Un gráfico no puede ser decorativo ni contener información que el texto no permita recuperar.
4. Los problemas con varios apartados siguen una secuencia didáctica: representar -> modelar -> calcular -> interpretar/comprobar.
5. Las respuestas numéricas indican unidad, redondeo y tolerancia. Una respuesta de función indica una forma canónica aceptada y las variantes equivalentes.
6. En una respuesta escrita, se especifica qué debe verse: referencia/ejes, ecuaciones, signos, unidades y conclusión física.
7. Los diagramas se implementarán más adelante como SVG responsive. Esta especificación describe qué información debe contener cada uno; no usar capturas, PNG generados por IA ni gráficas con márgenes innecesarios.
8. Las soluciones completas se liberan tras entregar; las pistas se revelan de menor a mayor ayuda.

## 3. Tipos de respuesta previstos

| Tipo | Cuándo usarlo | Requisito editorial |
|---|---|---|
| `numeric_multi` | Valores, tiempos, velocidades, aceleraciones y áreas | Un campo por magnitud; unidad y tolerancia definidas |
| `function_expression` | `x(t)`, `v(t)` o `a(t)` | Declarar variables, unidades y formas algebraicas equivalentes aceptadas |
| `single_choice_plus_text` | Elegir una gráfica, una afirmación o una conclusión | La justificación corta debe señalar pendiente, área o signo relevante |
| `graph_selection` | Relacionar representaciones del mismo movimiento | Cada opción debe ser físicamente distinta, no solo estéticamente distinta |
| `written_upload` | Problemas largos, gráficas construidas o razonamientos | Lista precisa de elementos que se deben mostrar en la foto |

## 4. Progresión y familias

### Bloque R - Referencia, posición y representaciones (8)

| ID | Actividad | Representación/diagrama obligatorio | Resultado principal |
|---|---|---|---|
| `t1_r_001` | Elegir origen y sentido para una recta ferroviaria | Vía, estación de origen y puntos a ambos lados | Posiciones con signo |
| `t1_r_002` | Distinguir posición, desplazamiento y distancia en un recorrido con vuelta | Recta con tres posiciones sucesivas | `x_i`, `x_f`, `Delta x` y distancia |
| `t1_r_003` | Traducir una tabla a `x(t)` lineal | Tabla con unidades SI | Función y gráfica |
| `t1_r_004` | Leer una función lineal y completar tabla | Recta `x(t)` | Posición, instante y velocidad |
| `t1_r_005` | Comparar dos sistemas de referencia | Dos orígenes sobre la misma recta | Cambio de coordenada sin cambiar el movimiento |
| `t1_r_006` | Identificar signos de posición, velocidad y aceleración | Esquema de varios móviles | Clasificación razonada |
| `t1_r_007` | Completar una representación ausente | Descripción, tabla y gráfica parciales | Forma faltante coherente |
| `t1_r_008` | Detectar una incoherencia entre texto y gráfica | Dos representaciones deliberadamente contradictorias | Explicación del error |

### Bloque U - MRU, encuentros y movimiento relativo (12)

| ID | Actividad | Partes mínimas | Visual requerido |
|---|---|---|---|
| `t1_u_001` | MRU desde datos iniciales | Construir `x(t)`; calcular posición posterior; invertir para hallar instante | Recta y eje temporal |
| `t1_u_002` | MRU desde gráfica `x-t` | Leer pendiente; escribir función; extrapolar | Gráfica con escala |
| `t1_u_003` | Dos móviles que se encuentran | Dos funciones; resolver igualdad; comprobar posición | Dos rectas `x(t)` |
| `t1_u_004` | Alcance con salida retardada | Funciones por tramos; instante de alcance; distancia | Línea temporal y posiciones iniciales |
| `t1_u_005` | Dos ciclistas en sentidos opuestos | Convención de signo; tiempo de cruce; posición | Recta con flechas |
| `t1_u_006` | Velocidad relativa como diferencia de funciones | Comparar sistemas; interpretar signo | Tabla de dos velocidades |
| `t1_u_007` | Diseñar la hora de salida para llegar a tiempo | Ecuación de posición y condición final | Horario/línea temporal |
| `t1_u_008` | MRU con conversión de unidades integrada | Conversión; función; resultado realista | Sin visual obligatorio |
| `t1_u_009` | Tren y andén: longitud recorrida por ambos extremos | Posición de extremo delantero y trasero; condición de salida completa | Tren, andén y referencia |
| `t1_u_010` | Construir una gráfica `x-t` desde una narración de MRU con parada | Tres tramos; identificar reposo | Gráfica construida por el alumno |
| `t1_u_011` | Decidir si un encuentro puede ocurrir | Comparar posiciones iniciales y velocidades; justificar | Recta `x(t)` o diagrama |
| `t1_u_012` | Problema inverso: hallar velocidad inicial necesaria | Traducir condición de encuentro a ecuación | Esquema de dos móviles |

### Bloque A - MRUA y movimiento vertical rectilíneo (14)

| ID | Actividad | Aspecto que debe evitarse | Partes mínimas |
|---|---|---|---|
| `t1_a_001` | MRUA desde `x_0`, `v_0` y `a` | Sustitución ciega | Función `x(t)`, velocidad y posición en un instante |
| `t1_a_002` | Hallar aceleración desde dos velocidades y tiempo | Confundir aceleración con velocidad | Signo y unidad |
| `t1_a_003` | Frenada uniforme | Usar aceleración positiva por costumbre | Tiempo, distancia y comprobación física |
| `t1_a_004` | Arranque desde reposo | Suponer distancia lineal en tiempo | Comparar dos instantes |
| `t1_a_005` | Cambio de sentido | Ignorar el instante con `v=0` | Instante, posición y sentido antes/después |
| `t1_a_006` | Determinar `v_0` a partir de condición final | Elegir fórmula sin condición | Despeje y validación |
| `t1_a_007` | Movimiento vertical de caída libre | Tratar `g` sin signo | Eje vertical, posición y velocidad de impacto |
| `t1_a_008` | Lanzamiento vertical hacia arriba | Confundir altura máxima con distancia total | Tiempo de subida, altura y velocidad |
| `t1_a_009` | Dos objetos verticales con salida diferida | Mezclar sus relojes | Función de cada objeto y encuentro |
| `t1_a_010` | Ascensor: aceleración, velocidad y posición | Concluir "reposo" solo porque `a=0` | Interpretación por tramos |
| `t1_a_011` | Deducir parámetros desde una función cuadrática | Perder dimensiones de coeficientes | `x_0`, `v_0`, `a` |
| `t1_a_012` | Elegir el modelo correcto de cuatro opciones | Mirar solo los números | Justificación dimensional y física |
| `t1_a_013` | Tiempo de reacción más distancia de frenado | Mezclar dos modelos en una sola ecuación | Diagrama temporal y distancia total |
| `t1_a_014` | Problema inverso con velocidad máxima permitida | Omitir una condición de seguridad | Ecuación, resultado y decisión razonada |

### Bloque G - Funciones y gráficas temporales (16)

| ID | Actividad | Gráficas/funciones que deben relacionarse |
|---|---|---|
| `t1_g_001` | Pendiente de `x(t)` en tres tramos | `x-t` y velocidad en cada tramo |
| `t1_g_002` | Área bajo `v(t)` para desplazamiento | `v-t` por rectángulos y triángulos |
| `t1_g_003` | Área con signo y distancia recorrida | `v-t` que cruza el eje |
| `t1_g_004` | Área bajo `a(t)` para cambio de velocidad | `a-t` y valores de `v` |
| `t1_g_005` | Construir `v(t)` a partir de `x(t)` por tramos | Dos gráficos alineados temporalmente |
| `t1_g_006` | Construir `a(t)` a partir de `v(t)` | Dos gráficos alineados temporalmente |
| `t1_g_007` | Elegir el trío `x-t`, `v-t`, `a-t` compatible | Tres opciones completas |
| `t1_g_008` | Identificar reposo, avance, retroceso y cambio de sentido | `x-t` y/o `v-t` |
| `t1_g_009` | Ajustar una función lineal a dos puntos experimentales | Tabla y gráfica con dos puntos |
| `t1_g_010` | Ajustar una función cuadrática a condiciones cinemáticas | `x(t)` y condiciones iniciales |
| `t1_g_011` | Detectar un gráfico imposible | Relación pendiente/área contradictoria |
| `t1_g_012` | Interpretar una aceleración negativa sin asociarla siempre a frenada | Signo de `v` y `a` |
| `t1_g_013` | Movimiento por cuatro tramos | `x-t`, `v-t`, `a-t` a completar |
| `t1_g_014` | Inferir parámetros de MRUA desde `v(t)` | Intersección, pendiente y área |
| `t1_g_015` | Resolver un encuentro desde intersección gráfica | Dos rectas `x(t)` |
| `t1_g_016` | Explicar con palabras una gráfica dada | Texto físico preciso, no solo "sube" o "baja" |

### Bloque I - Problemas integradores y referencia PAU (10)

Estos ejercicios son más largos (`written_upload` salvo que se indique otro tipo). Todos deben pedir explícitamente referencia, planteamiento, desarrollo, unidades y conclusión.

| ID | Escenario | Estructura | Fuente prevista |
|---|---|---|---|
| `t1_i_001` | Viaje de tren con arranque, velocidad de crucero y frenada | Funciones por tramo; gráfico `v-t`; distancia total | Original |
| `t1_i_002` | Ciclista y peatón con salida retardada | Dos funciones; encuentro; gráfica conjunta | Original |
| `t1_i_003` | Frenada ante un obstáculo | Reacción + MRUA; decisión de seguridad | Original |
| `t1_i_004` | Lanzamiento vertical desde una azotea | Eje; dos raíces; sentido de impacto | Original |
| `t1_i_005` | Ascensor descrito por `a(t)` | Integrar por tramos; construir `v(t)` y `x(t)` | Original |
| `t1_i_006` | Informe de datos de un sensor de posición | Ajuste lineal/cuadrático; detectar medida incoherente | Original |
| `t1_i_007` | Adaptación de cuestión PAU sobre gráfica temporal | Conservar habilidad; reescribir enunciado y diagrama propios | Adaptado de PAU verificada |
| `t1_i_008` | Adaptación de cuestión PAU sobre frenada o alcance | Varios apartados; datos modificados; solución propia | Adaptado de PAU verificada |
| `t1_i_009` | Cuestión oficial, solo cuando los derechos y nivel sean adecuados | Referencia exacta, visor de fuente y solución propia separada | PAU oficial verificada |
| `t1_i_010` | Simulacro corto T1 | Selección de cuatro microproblemas conectados por una historia | Original |

## 5. Política de fuentes PAU

No se inventará ninguna comunidad, año, sesión, enunciado ni enlace de PAU. Cada fuente se incorpora solo tras comprobar el PDF o repositorio oficial.

Una referencia debe contener:

```json
{
  "kind": "adapted_from_pau | official_pau",
  "community": "",
  "year": 0,
  "session": "ordinaria | extraordinaria",
  "question": "",
  "source_url": "",
  "source_page": 0,
  "adaptation_note": ""
}
```

- Los ejercicios `adapted_from_pau` son nuevos: texto, datos, gráficos y solución propios.
- Los ejercicios `official_pau` mantienen atribución y referencia exacta; no se copian soluciones de terceros.
- El filtro de la web distinguirá original, adaptado y oficial.
- Para T1, priorizar fuentes con interpretación de gráficos, MRU, MRUA, frenada, encuentros o construcción de funciones. Si el ejercicio oficial exige contenido posterior, se adapta o se descarta.

## 6. Criterios de aceptación

Antes de convertir esta referencia a JSON:

1. cada ejercicio tiene objetivo, subtipo, dificultad, tiempo, formato de respuesta, pistas, solución y errores previsibles;
2. las funciones y gráficas emplean las mismas convenciones de signo del enunciado;
3. los resultados se verifican con unidades y, si procede, por una segunda representación;
4. los problemas largos tienen datos suficientes y no ocultan información esencial en el SVG;
5. toda referencia PAU queda vacía hasta que se haya verificado la fuente primaria;
6. el catálogo no contiene variantes que solo cambien números.
