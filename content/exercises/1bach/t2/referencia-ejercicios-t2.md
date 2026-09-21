# Banco editorial T2 v1 - Movimiento en el plano

**Curso:** 1.º de Bachillerato  
**Tema:** T2 - Movimiento en el plano  
**Estado:** referencia editorial para construir el catálogo JSON  
**Fecha:** 14 de septiembre de 2026

## 1. Propósito del banco

T2 debe usar intensamente las herramientas vectoriales de T0 y el trabajo funcional de T1. El alumno no solo calcula un alcance: modela el movimiento mediante componentes, interpreta trayectorias y conecta diagramas del plano `x-y` con funciones temporales `x(t)`, `y(t)`, `v_x(t)` y `v_y(t)`.

Se esperan más diagramas que en T1. Cada situación bidimensional necesita al menos un esquema claro de ejes, origen, vectores y datos angulares. Los problemas largos deben exigir una representación vectorial antes de operar.

El catálogo inicial contiene **60 ejercicios**.

| Bloque | IDs | Cantidad |
|---|---:|---:|
| Posición, velocidad y aceleración vectoriales | `t2_v_001`-`t2_v_010` | 10 |
| Funciones paramétricas y gráficas por componentes | `t2_f_001`-`t2_f_010` | 10 |
| Tiro horizontal | `t2_h_001`-`t2_h_010` | 10 |
| Tiro parabólico oblicuo | `t2_p_001`-`t2_p_014` | 14 |
| Movimiento circular | `t2_c_001`-`t2_c_008` | 8 |
| Problemas integradores y referencias PAU | `t2_i_001`-`t2_i_008` | 8 |
| **Total** |  | **60** |

Si la versión final de la lección T2 no incluye formalmente movimiento circular, los ocho ejercicios `t2_c_*` se sustituyen por ocho ejercicios adicionales de composición vectorial, movimiento relativo en dos dimensiones y lectura de funciones paramétricas. Los IDs no se reciclan para otro contenido una vez haya intentos históricos.

## 2. Contrato editorial común

1. Se declaran origen, ejes y convención de signos antes de toda ecuación. Por defecto, `+x` hacia la derecha y `+y` hacia arriba.
2. La aceleración gravitatoria se escribe como `a_y=-g` cuando se usa esa convención.
3. Se distingue siempre entre vector, módulo y componente. No se acepta una dirección sin sentido ni una magnitud sin unidad cuando proceda.
4. En tiro parabólico se separan explícitamente las ecuaciones horizontal y vertical. No se permite resolverlo como una única ecuación escalar.
5. Las gráficas `x(t)`, `y(t)`, `v_x(t)` y `v_y(t)` deben compartir escala temporal o declarar claramente su intervalo.
6. Los diagramas serán SVG responsive en la implementación. Deben mostrar los datos necesarios, pero el enunciado conserva todos los valores por escrito para seguir siendo resoluble sin la imagen.
7. Las soluciones incluyen una comprobación cualitativa: signo, cuadrante, altura, alcance, orden de magnitud o concordancia con la trayectoria.
8. Las respuestas escritas indican si se exige un diagrama de fuerzas o de movimiento, las componentes, las ecuaciones y una conclusión final.

## 3. Tipos de respuesta previstos

| Tipo | Uso | Formato obligatorio |
|---|---|---|
| `numeric_multi` | Componentes, tiempos, alcance, altura, módulo y periodo | Campo separado por magnitud, unidad, tolerancia y redondeo |
| `vector_components` | Vectores posición, velocidad o aceleración | Orden explícito `x; y`, con signos y unidades |
| `function_expression` | Funciones paramétricas o dependencias temporales | Variables, unidades y expresiones equivalentes aceptadas |
| `graph_selection` | Elegir gráfica compatible con una trayectoria o función | Justificación por componente, pendiente o área |
| `written_upload` | Problemas de tiro, circular o PAU | Ejes, diagrama, modelo vectorial, cálculos y respuesta física |

## 4. Progresión y familias

### Bloque V - Posición, velocidad y aceleración vectoriales (10)

| ID | Actividad | Visual imprescindible | Resultado principal |
|---|---|---|---|
| `t2_v_001` | Posición en el plano desde coordenadas | Ejes y puntos | Vector posición y módulo |
| `t2_v_002` | Desplazamiento entre dos posiciones | Dos puntos y flecha | `Delta r`, módulo y dirección |
| `t2_v_003` | Velocidad media vectorial | Dos posiciones con intervalo de tiempo | Componentes y módulo |
| `t2_v_004` | Aceleración media desde dos velocidades | Vectores velocidad punta-cola | `Delta v/Delta t` |
| `t2_v_005` | Comparar rapidez media y módulo de velocidad media | Trayectoria no recta | Explicación de por qué difieren |
| `t2_v_006` | Construir un vector de velocidad con módulo y ángulo | Triángulo de componentes | `v_x`, `v_y` |
| `t2_v_007` | Reconocer dirección de velocidad y aceleración en una trayectoria | Curva con varios puntos | Vectores tangente y aceleración cualitativa |
| `t2_v_008` | Movimiento relativo de una barca o dron | Dos vectores de velocidad | Suma vectorial y dirección final |
| `t2_v_009` | Elegir ejes más útiles para un problema en plano | Tres propuestas de ejes | Justificación del sistema elegido |
| `t2_v_010` | Problema inverso: hallar vector desconocido | Paralelogramo con datos | Componentes y verificación gráfica |

### Bloque F - Funciones paramétricas y gráficas por componentes (10)

| ID | Actividad | Funciones/gráficas obligatorias |
|---|---|---|
| `t2_f_001` | Evaluar una posición vectorial `r(t)` | `x(t)`, `y(t)` y punto `x-y` |
| `t2_f_002` | Derivar `r(t)` para obtener `v(t)` y `a(t)` | Componentes y unidades |
| `t2_f_003` | Construir `r(t)` desde `x(t)` e `y(t)` | Forma vectorial y trayectoria |
| `t2_f_004` | Identificar una trayectoria lineal desde funciones | `x(t)`, `y(t)` y plano |
| `t2_f_005` | Eliminar el parámetro para obtener `y(x)` | Trayectoria y dominio físico |
| `t2_f_006` | Relacionar una parábola con sus funciones temporales | `x(t)` lineal y `y(t)` cuadrática |
| `t2_f_007` | Comparar dos movimientos con igual trayectoria y diferente ritmo | Dos parametrizaciones de la misma curva |
| `t2_f_008` | Leer componentes desde gráficas temporales | `v_x(t)` y `v_y(t)` |
| `t2_f_009` | Determinar instante de cruce de una condición espacial | Funciones y recta/altura objetivo |
| `t2_f_010` | Detectar una parametrización incompatible con un dibujo | Trayectoria, signos y valores iniciales |

### Bloque H - Tiro horizontal (10)

| ID | Actividad | Partes mínimas | Diagrama requerido |
|---|---|---|---|
| `t2_h_001` | Lanzamiento horizontal desde altura conocida | Tiempo de caída, alcance y velocidad de impacto | Borde, ejes y `v_0` horizontal |
| `t2_h_002` | Hallar velocidad inicial para alcanzar una distancia | Modelo por componentes e incógnita | Trayectoria con objetivo |
| `t2_h_003` | Determinar altura desde una fotografía/datos de alcance | Eliminar tiempo; comprobación | Plano y datos |
| `t2_h_004` | Comparar dos lanzamientos con distinta velocidad | Proporcionalidad y gráficas | Dos trayectorias |
| `t2_h_005` | Comparar dos lanzamientos con distinta altura | Tiempo de caída y alcance | Dos plataformas |
| `t2_h_006` | Construir `x(t)`, `y(t)`, `v_x(t)` y `v_y(t)` | Cuatro funciones | Panel de gráficos temporales |
| `t2_h_007` | Elegir la trayectoria y gráficos correctos | Justificación por independencia de componentes | Opciones gráficas |
| `t2_h_008` | Impacto sobre una rampa o superficie a altura conocida | Condición geométrica y tiempo físico | Rampa y trayectoria |
| `t2_h_009` | Lanzamiento desde vehículo en MRU | Velocidad respecto a suelo y plataforma | Referencia doble |
| `t2_h_010` | Problema largo de laboratorio simulado | Datos con incertidumbre simple; ajuste y conclusión | Fotograma/diagrama propio |

### Bloque P - Tiro parabólico oblicuo (14)

| ID | Actividad | Competencia central | Diagrama/funciones |
|---|---|---|---|
| `t2_p_001` | Descomponer velocidad inicial en dos componentes | Trigonometría y signos | Triángulo de `v_0` |
| `t2_p_002` | Ecuaciones paramétricas desde datos iniciales | Modelo completo | Ejes y trayectoria |
| `t2_p_003` | Tiempo de vuelo a misma altura | Raíces y selección física | `y(t)` |
| `t2_p_004` | Alcance horizontal | Sustituir tiempo físico | Trayectoria y suelo |
| `t2_p_005` | Altura máxima | Condición `v_y=0` | `v_y(t)` |
| `t2_p_006` | Velocidad y ángulo de impacto | Componentes, módulo y dirección | Vectores en impacto |
| `t2_p_007` | Lanzamiento desde altura no nula | Dos raíces y condición temporal | Plataforma y suelo |
| `t2_p_008` | Alcanzar una diana a altura dada | Resolver `y(x)` y elegir solución | Diana y dos posibles ángulos |
| `t2_p_009` | Comparar ángulos complementarios | Mismo alcance, distinta altura/tiempo | Dos trayectorias |
| `t2_p_010` | Encontrar ángulo o velocidad inicial bajo una condición | Problema inverso | Diagrama etiquetado |
| `t2_p_011` | Distinguir componentes independientes en opciones | Razonamiento conceptual con cálculo breve | Gráficas `v_x`, `v_y` |
| `t2_p_012` | Proyecto de gráfico: dibujar funciones temporales | Pasar de trayectoria a cuatro gráficas | Panel temporal |
| `t2_p_013` | Tiro contra plano inclinado simple | Intersección trayectoria-recta | Rampa y ejes |
| `t2_p_014` | Auditoría de una resolución con errores | Detectar signo, raíz o unidad incorrecta | Enunciado y solución ficticia |

### Bloque C - Movimiento circular (8)

Usar este bloque solo si figura en la lección T2 final.

| ID | Actividad | Elementos a comprobar |
|---|---|---|
| `t2_c_001` | Periodo, frecuencia y velocidad angular | Unidades y conversiones completas |
| `t2_c_002` | Radio, velocidad lineal y vueltas | Diferenciar `v` de `omega` |
| `t2_c_003` | Vector velocidad tangente | Dirección en cuatro puntos de la circunferencia |
| `t2_c_004` | Aceleración centrípeta | Dirección al centro y módulo |
| `t2_c_005` | Funciones paramétricas de MCU | `x(t)`, `y(t)` y trayectoria circular |
| `t2_c_006` | Gráficas temporales de componentes | Seno/coseno, fase y periodo |
| `t2_c_007` | Comparar dos movimientos circulares | Proporcionalidades al cambiar radio o periodo |
| `t2_c_008` | Problema integrador de rueda o satélite idealizado | Diagrama, funciones y vectores en un punto |

### Bloque I - Problemas integradores y referencia PAU (8)

Todos son `written_upload`. La entrega debe mostrar ejes, diagrama, ecuaciones de componentes, cálculo, unidad y una conclusión física explícita.

| ID | Escenario | Estructura | Fuente prevista |
|---|---|---|---|
| `t2_i_001` | Dron con velocidad propia y viento | Suma vectorial; trayectoria; llegada a punto objetivo | Original |
| `t2_i_002` | Pelota lanzada desde una grada | Componentes; tiempo; impacto; velocidad final | Original |
| `t2_i_003` | Tiro a una diana elevada | Dos posibles soluciones; criterio físico | Original |
| `t2_i_004` | Lanzamiento horizontal hacia rampa | Ecuación de trayectoria e intersección | Original |
| `t2_i_005` | Movimiento descrito por funciones paramétricas | Derivar, interpretar trayectoria y dibujar vectores | Original |
| `t2_i_006` | Adaptación de cuestión PAU de tiro/parábola | Enunciado, figura y solución propios; nivel ajustado | Adaptado de PAU verificada |
| `t2_i_007` | Adaptación de cuestión PAU de vector/circular | Varios apartados y comprobación gráfica | Adaptado de PAU verificada |
| `t2_i_008` | Cuestión oficial o simulacro breve T2 | Referencia exacta solo si se verifica fuente primaria | PAU oficial verificada u original |

## 5. Reglas de diagramas y gráficas

T2 debe ser el tema con mayor densidad visual del proyecto. Los siguientes requisitos son obligatorios en la producción posterior:

- Todo tiro muestra origen, suelo/objetivo, `+x`, `+y`, vector inicial, ángulo y variables dadas.
- Si hay altura inicial, se diferencia visualmente el origen de coordenadas del nivel del suelo.
- Las trayectorias no deben sugerir que la velocidad sea tangente incorrectamente ni que la aceleración apunte siguiendo la curva.
- Los vectores de velocidad son tangentes; la aceleración gravitatoria apunta verticalmente hacia abajo; la centrípeta apunta al centro.
- Las gráficas temporales llevan unidades y usan el mismo intervalo temporal que el problema.
- Una trayectoria `x-y` no sustituye a las gráficas temporales cuando el ejercicio pide componentes.
- Las imágenes no pueden ser el único lugar donde aparezcan valores numéricos, condiciones iniciales o unidades.

## 6. Política de fuentes PAU

No inventar referencias ni reproducir sin verificar materiales externos. Cada ejercicio PAU sigue uno de estos modelos:

```json
{
  "kind": "original_teacher_bank | adapted_from_pau | official_pau",
  "reference": {
    "community": "",
    "year": 0,
    "session": "ordinaria | extraordinaria",
    "question": "",
    "source_url": "",
    "source_page": 0
  },
  "adaptation_note": ""
}
```

- En `adapted_from_pau`, el alumno recibe texto, números, diagrama y solución propios; la referencia es trazabilidad y atribución.
- En `official_pau`, se conserva la atribución completa y se comprueba que el nivel encaja con T2.
- Para T2, buscar cuestiones sobre vectores, composición de movimientos, tiro horizontal/parabólico, trayectorias, funciones temporales o movimiento circular si forma parte del currículo.
- No forzar una referencia PAU si introduce campos, energía, dinámica u otro contenido aún no trabajado.

## 7. Criterios de aceptación

Antes de convertir el documento a JSON:

1. todos los ejercicios tienen objetivo concreto, dificultad, tiempo, tipo de respuesta, solución y errores frecuentes;
2. se verifican independientemente las componentes, raíces temporales, ángulos y unidades;
3. los problemas de tiro separan explícitamente `x` e `y`;
4. los ejercicios gráficos pueden resolverse aunque el SVG no cargue;
5. no hay ejercicios que sean meras variaciones numéricas de otro;
6. las referencias PAU solo se completan con fuentes primarias comprobadas;
7. se confirma si el bloque circular pertenece a la lección antes de activar sus IDs.
