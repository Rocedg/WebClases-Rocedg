# Banco editorial T3 v1 - Leyes de Newton

**Curso:** 1.º de Bachillerato
**Tema:** T3 - Leyes de Newton
**Estado:** referencia editorial completa previa al catálogo JSON
**Fecha:** 21 de septiembre de 2026

## 1. Propósito del banco

T3 debe enseñar a modelizar interacciones, no a buscar una fórmula por palabras clave. Cada ejercicio obliga a decidir el sistema, reconocer fuerzas reales, dibujar el diagrama de cuerpo libre, elegir ejes y relacionar la resultante con la aceleración. Los SVG serán instrumentos de razonamiento: cuerpos aislados, pares de interacción, ejes locales, poleas y vectores radiales.

El banco previsto contiene **60 ejercicios originales**. Ninguno requiere texto libre, fotografía o corrección manual.

| Bloque | IDs | Cantidad |
|---|---:|---:|
| Fuerzas e interacciones | `t3_f_001`–`t3_f_012` | 12 |
| Resultante y leyes de Newton | `t3_n_001`–`t3_n_012` | 12 |
| Planos, cuerdas y sistemas enlazados | `t3_p_001`–`t3_p_014` | 14 |
| Dinámica circular | `t3_c_001`–`t3_c_010` | 10 |
| Integración, diagnóstico y modelización | `t3_i_001`–`t3_i_012` | 12 |
| **Total** |  | **60** |

## 2. Contrato editorial y técnico

1. Todo enunciado declara sistema, ejes y situación cinemática. La solución empieza por el diagrama, aunque la respuesta sea numérica.
2. No se dibujan como fuerzas la velocidad, la aceleración, la “resultante” ni la fuerza centrípeta como fuerza adicional.
3. Acción y reacción aparecen sobre cuerpos distintos. La normal se determina con Newton; no se fija automáticamente igual al peso.
4. Las respuestas serán `numeric`, `vector`, `single_choice`, `function`, `unit_expression` o `short_text` con conjunto cerrado verificable.
5. Cada campo queda asociado a `(a)`, `(b)`, etc. Las unidades visibles no se escriben dentro del valor.
6. No habrá pistas. La solución posterior incluirá ecuaciones por ejes, signos, unidades y una comprobación física.
7. Todo SVG será responsive y resoluble junto al texto: la imagen aclara relaciones espaciales, pero no guarda datos exclusivos.
8. Los distractores representarán errores reales: pares acción-reacción mal emparejados, normal igual al peso, tensión duplicada o centrípeta añadida.

### Metadatos previstos para el JSON

Todos usarán `course: 1bach`, `topic: t3`, `status: draft`, `version: 1`, `response_mode: structured` y origen `original_teacher_bank`. Las familias F/N parten de dificultad 2 y llegan a 4 (`6–11 min`); P/C parten de 3 y llegan a 5 (`8–15 min`); I será 4–5 (`12–18 min`). Etiquetas comunes: `newton`, `dcl`, la familia y la representación visual. Los ejercicios de auditoría añaden `model_check`.

## 3. Inventario de ejercicios

### Bloque F - Fuerzas e interacciones (12)

| ID | Núcleo del enunciado | Respuestas estructuradas y clave | SVG imprescindible |
|---|---|---|---|
| `t3_f_001` | Libro en reposo sobre mesa: identificar interacciones Tierra-libro y mesa-libro. | Selección múltiple cerrada: peso y normal; resultante `0 N`. | Libro aislado y diagrama de interacciones separado. |
| `t3_f_002` | Lámpara colgada de un cable vertical, `m=3 kg`, `g=9,8`. | `T=29,4 N`; par de reacción de la tensión: lámpara sobre cable. | Lámpara, cable y dos DCL alternativos. |
| `t3_f_003` | Caja empujada horizontalmente sin rozamiento con `F=18 N`, `m=6 kg`. | Fuerzas: peso, normal y empuje; `a=3 m/s²`. | Caja y flechas con ejes. |
| `t3_f_004` | Ascensor que sube a velocidad constante con persona de `60 kg`. | `N=588 N`; selección: aceleración nula aunque se mueve. | Persona aislada dentro del ascensor. |
| `t3_f_005` | Ascensor acelera hacia arriba a `1,5 m/s²`, persona `60 kg`. | `N=678 N`; vector resultante `(0;90) N`. | Comparación visual `N>P`. |
| `t3_f_006` | Misma persona con aceleración descendente `2 m/s²`. | `N=468 N`; selección `N<P`. | Comparación con el caso anterior. |
| `t3_f_007` | Bloque sobre plano de `30°`, sin rozamiento. | Componentes del peso: paralela `24,5 N`, normal `42,4 N` para `m=5 kg`. | Peso y ejes rotados, sin fuerzas ficticias. |
| `t3_f_008` | Dos patinadores se empujan con `80 N`. | Fuerzas mutuas `80 N` y sentidos opuestos; selección del par correcto. | Dos cuerpos y pares coloreados. |
| `t3_f_009` | Caballo tira de carro: distinguir par acción-reacción y fuerza que acelera el sistema. | Selección: suelo sobre caballo; par cuerda-carro/carro-cuerda. | Diagrama de interacciones de tres sistemas. |
| `t3_f_010` | Pelota ascendiendo tras abandonar la mano, sin aire. | Selección: solo peso; aceleración `(0;-9,8) m/s²`. | Tres DCL, dos con fuerzas inventadas. |
| `t3_f_011` | Satélite ideal en órbita: fuerza y velocidad en un punto. | Selección: fuerza radial, velocidad tangente, perpendiculares. | Órbita con cuatro pares vectoriales candidatos. |
| `t3_f_012` | Auditar un DCL con “fuerza del movimiento” y resultante añadida. | Selección de dos flechas que deben eliminarse; número de fuerzas reales `2`. | DCL deliberadamente incorrecto y versión numerada. |

### Bloque N - Resultante y leyes de Newton (12)

| ID | Núcleo del enunciado | Respuestas estructuradas y clave | SVG imprescindible |
|---|---|---|---|
| `t3_n_001` | Fuerzas horizontales `14 N` derecha y `8 N` izquierda sobre `2 kg`. | `F_R=6 N`; `a=3 m/s²`, derecha. | Recta, fuerzas y vector resultante a completar. |
| `t3_n_002` | Fuerzas perpendiculares `6 N` y `8 N` sobre `5 kg`. | Resultante `(6;8) N`; módulo `10 N`; `a=2 m/s²`. | Paralelogramo vectorial. |
| `t3_n_003` | Carrito pasa de `2` a `8 m/s` en `3 s`, `m=4 kg`. | `a=2 m/s²`; `F_R=8 N`. | Panel `v(t)` y DCL incompleto. |
| `t3_n_004` | Resultante constante `-12 N`, `m=3 kg`, `v_0=10 m/s`. | `a=-4 m/s²`; parada `2,5 s`; selección del sentido antes de parar. | Vectores `v` y `a` opuestos. |
| `t3_n_005` | Dos cuerpos reciben la misma resultante; masas `2` y `5 kg`. | Razón `a_1/a_2=2,5`; elección de la gráfica `a(F)` correcta. | Dos carros y gráfica comparativa. |
| `t3_n_006` | Experimento `F-a`: puntos `(2,0,5)`, `(4,1)`, `(6,1,5)`. | Pendiente/masa `4 kg`; función `F=4a`. | Dispersión lineal con origen. |
| `t3_n_007` | Velocidad constante pese a motor de `500 N`. | Fuerza resistiva `500 N`; resultante `0 N`. | Vehículo con fuerzas horizontales equilibradas. |
| `t3_n_008` | Trineo `20 kg`, fuerza `(60;0) N`, aceleración `(2;0)`. | Resistencia `20 N` opuesta; resultante `(40;0) N`. | DCL con fuerza desconocida. |
| `t3_n_009` | Cuerpo con `a=(2;-1) m/s²`, `m=3 kg`. | Resultante `(6;-3) N`; módulo `6,71 N`. | Plano cartesiano de aceleración/resultante. |
| `t3_n_010` | Elegir gráfica de aceleración cuando la fuerza neta cambia de signo. | Opción exacta `a(t)=F(t)/m`; valores `2,0,-1 m/s²`. | Paneles escalonados `F(t)` y opciones `a(t)`. |
| `t3_n_011` | Báscula en ascensor registra `735 N` para `m=70 kg`. | `a=0,7 m/s²` hacia arriba. | Báscula y DCL con lectura `N`. |
| `t3_n_012` | Error: “si la resultante es cero, el objeto está parado”. | Selección contraejemplo: MRU; velocidad compatible `cualquier constante`. | Dos gráficas `x(t)` candidatas. |

### Bloque P - Planos, cuerdas y sistemas enlazados (14)

| ID | Núcleo del enunciado | Respuestas estructuradas y clave | SVG imprescindible |
|---|---|---|---|
| `t3_p_001` | Bloque `4 kg` en plano `30°` sin rozamiento. | `a=4,9 m/s²` cuesta abajo; `N=33,9 N`. | Plano y DCL con ejes locales. |
| `t3_p_002` | Fuerza paralela de `30 N` sube el bloque anterior. | Resultante paralela `10,4 N`; `a=2,6 m/s²` arriba. | Comparación de fuerzas paralelas. |
| `t3_p_003` | Fuerza horizontal `40 N` sobre bloque `5 kg` en plano `30°`. | Componentes locales `34,6 N` y `-20 N`; `N=62,4 N`. | Descomposición de una fuerza no alineada. |
| `t3_p_004` | Masa colgante `3 kg` en equilibrio sostenida por dos cuerdas simétricas a `45°`. | Cada tensión `20,8 N`. | Nudo con ángulos y fuerzas concurrentes. |
| `t3_p_005` | Nudo con cable horizontal y cable a `30°`, carga `100 N`. | Cable inclinado `200 N`; horizontal `173,2 N`. | Diagrama de nudo, no de la carga completa. |
| `t3_p_006` | Dos bloques `2` y `3 kg` unidos, tirados con `20 N`, mesa ideal. | `a=4 m/s²`; tensión `12 N`. | Dos DCL alineados. |
| `t3_p_007` | Misma cadena tirada desde el bloque de `2 kg`. | `a=4 m/s²`; tensión `8 N`; selección: tensión cambia. | Comparación de extremos de aplicación. |
| `t3_p_008` | Máquina de Atwood ideal `m_1=2`, `m_2=3 kg`. | `a=1,96 m/s²`; `T=23,5 N`. | Polea y dos ejes verticales coherentes. |
| `t3_p_009` | Atwood con masas iguales y velocidad inicial no nula. | `a=0`; selección: mantiene velocidad, no se detiene necesariamente. | Flechas de velocidad y fuerzas equilibradas. |
| `t3_p_010` | Bloque `4 kg` en mesa unido a masa colgante `1 kg`. | `a=1,96 m/s²`; `T=7,84 N`. | Dos DCL y cuerda ideal. |
| `t3_p_011` | Bloque `3 kg` en plano `30°` unido a colgante `2 kg`. | `a=0,98 m/s²` hacia el colgante; `T=17,6 N`. | Plano-polea-colgante con sentidos supuestos. |
| `t3_p_012` | Tres bloques `1,2,3 kg` tirados por `24 N`. | `a=4 m/s²`; tensiones `T_12=4 N`, `T_23=12 N`. | Tres DCL o mapa de cortes de cuerda. |
| `t3_p_013` | Polea móvil ideal que sostiene una carga de `200 N`. | Tensión por tramo `100 N`; fuerza aplicada `100 N`. | Polea móvil y dos tramos portantes. |
| `t3_p_014` | Auditar solución que usa una única ecuación para dos cuerpos y obtiene tensión incorrecta. | Selección del sistema para `a`; ecuación individual correcta; `T=12 N` para datos de `p_006`. | Solución ficticia anotada por pasos. |

### Bloque C - Dinámica circular (10)

| ID | Núcleo del enunciado | Respuestas estructuradas y clave | SVG imprescindible |
|---|---|---|---|
| `t3_c_001` | Piedra `0,5 kg`, radio `2 m`, rapidez `4 m/s`, plano horizontal ideal. | `a_c=8 m/s²`; resultante radial `4 N`. | Trayectoria, tangente y radio. |
| `t3_c_002` | Elegir DCL correcto de coche en curva plana sin rozamiento modelizado aún. | Selección: peso/normal verticales; falta interacción horizontal para curvar. | Vista superior y lateral coordinadas. |
| `t3_c_003` | Masa en cuerda horizontal ideal, `m=0,2`, `r=0,8`, `v=6`. | `T=9 N`. | Círculo y tensión hacia el centro. |
| `t3_c_004` | Círculo vertical, punto inferior, `m=1`, `r=2`, `v=6`. | `T=27,8 N`. | DCL inferior con `T` y `P` opuestos. |
| `t3_c_005` | Mismo sistema en punto superior. | `T=8,2 N`. | DCL superior con ambas fuerzas radiales. |
| `t3_c_006` | Rapidez mínima para cuerda tensa arriba, `r=1,5 m`. | `v_min=3,83 m/s`; `T=0` en el límite. | Caso límite en la cima. |
| `t3_c_007` | Pasajero en curva vertical inferior, `m=60`, `r=10`, `v=12`. | `N=1452 N`; factor aparente `2,47`. | Asiento y centro de curvatura. |
| `t3_c_008` | Péndulo cónico `L=1,2 m`, `θ=30°`, `m=0,5`. | `T=5,66 N`; radio `0,6 m`; `v=1,84 m/s`. | Cono, componentes de tensión. |
| `t3_c_009` | Gráfica de rapidez creciente en círculo de radio fijo. | Selección: `a_c∝v²`; razón al duplicar `v`: `4`. | Curvas candidatas `a_c(v)`. |
| `t3_c_010` | Auditar un DCL que añade “fuerza centrípeta” a tensión y peso. | Flecha a eliminar: centrípeta; ecuación radial correcta seleccionada. | DCL incorrecto numerado. |

### Bloque I - Integración, diagnóstico y modelización (12)

| ID | Núcleo del enunciado | Respuestas estructuradas y clave | SVG imprescindible |
|---|---|---|---|
| `t3_i_001` | Elegir sistema útil: dos bloques y cuerda sobre mesa ideal. | Selección sistema conjunto para `a`, cuerpo individual para `T`; valores de `p_006`. | Capas de sistema resaltables. |
| `t3_i_002` | Del vídeo `x(t)=0,75t²` de un carro `2 kg`, inferir fuerza neta. | `a=1,5 m/s²`; `F_R=3 N`. | Trayectoria y gráfica `x(t)`. |
| `t3_i_003` | Datos de `F` y `a` con una medida atípica. | Masa por ajuste `2 kg`; seleccionar punto atípico `(8 N,2 m/s²)`. | Dispersión experimental. |
| `t3_i_004` | Caja en camión que acelera: identificar interacción que acelera la caja. | Selección rozamiento estático hacia delante; mínimo requerido `ma`. | Caja y camión, dos referencias. |
| `t3_i_005` | Globo en coche acelerado como diagnóstico conceptual. | Selección de inclinación hacia delante; dirección del gradiente de presión. | Habitáculo con aire y globo. |
| `t3_i_006` | Persona de `60 kg` sobre una báscula tira de una cuerda que pasa por una polea fija; la tensión es `100 N`. | Relación `N+T=mg`; lectura `N=488 N`. | Persona-báscula-cuerda con sistema señalado. |
| `t3_i_007` | Comparar bajar y subir el mismo plano con igual rapidez instantánea. | Aceleración idéntica cuesta abajo `g sinθ`; elección de signos según eje. | Dos fotogramas, mismo DCL. |
| `t3_i_008` | Para `m=4 kg`, `a(t)` vale `1 m/s²` entre `0–2 s`, `-0,5 m/s²` entre `2–4 s` y `0` después. | `F_R(t)` por tramos: `4 N`, `-2 N`, `0 N`. | Panel `a(t)`/`F(t)`. |
| `t3_i_009` | Diseñar fuerza para que un bloque recorra `8 m` desde reposo en `4 s`, `m=5 kg`. | `a=1 m/s²`; `F_R=5 N`. | Línea temporal y DCL. |
| `t3_i_010` | Diagrama de interacción de libro-mesa-Tierra y selección de pares de tercera ley. | Tres pares correctos en selección cerrada. | Mapa de nodos con interacciones. |
| `t3_i_011` | Caso mixto plano-polea: decidir primero el sentido sin asumirlo por la masa mayor. | Comparar `m_2g` con `m_1g sinθ`; selección del sentido y aceleración numérica. | Barras comparativas de fuerzas motrices. |
| `t3_i_012` | Miniinvestigación cerrada: cuatro DCL candidatos para un péndulo cónico y tres resultados. | Elegir DCL; `T`, `v` y periodo con tolerancias. | Péndulo, vista lateral y superior. |

## 4. Sistema visual

- Colores constantes por interacción: gravedad, contacto, cuerda y fuerza aplicada; nunca por “tipo de resultado”.
- Los DCL aíslan un solo sistema y se separan del dibujo contextual.
- Los sistemas enlazados incluyen una versión global y DCL individuales cuando la tensión sea incógnita.
- Los movimientos circulares combinan vista contextual, dirección radial y vector tangente sin revelar el resultado numérico.
- Al menos 36 ejercicios tendrán SVG; los demás usarán paneles `F(t)`, `a(t)` o selección gráfica cuando el visual aporte razonamiento.

## 5. Criterios de aceptación antes del JSON

1. Los 60 IDs son únicos, consecutivos dentro de cada familia y no se reutilizan.
2. Todos los resultados numéricos se recalculan con `g=9,8 m/s²` y tolerancia explícita.
3. Cada ejercicio tiene entre dos y cinco campos verificables o una selección inequívoca.
4. No quedan explicaciones abiertas; la comprensión se evalúa mediante selección conceptual, clasificación cerrada, vector, función o número.
5. Cada SVG tiene guion propio, texto alternativo y datos duplicados en el enunciado.
6. No se incorporan fuentes externas ni referencias PAU sin una revisión posterior de fuente primaria.
