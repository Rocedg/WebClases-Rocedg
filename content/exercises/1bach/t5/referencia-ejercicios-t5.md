# Banco editorial T5 v1 - Energía y trabajo

**Curso:** 1.º de Bachillerato
**Tema:** T5 - Energía y trabajo
**Estado:** referencia editorial completa previa al catálogo JSON
**Fecha:** 21 de septiembre de 2026

## 1. Propósito del banco

T5 enseña a resolver procesos por estados y transferencias. El alumno debe escoger sistema, reconocer qué trabajos cruzan su frontera, leer áreas bajo `F(x)`, usar el teorema cinético y construir balances con energía potencial, muelles y disipación. El banco contiene **60 ejercicios originales**, sin respuestas abiertas ni pistas.

| Bloque | IDs | Cantidad |
|---|---:|---:|
| Trabajo y fuerzas variables | `t5_w_001`–`t5_w_014` | 14 |
| Energía cinética y potencia | `t5_k_001`–`t5_k_012` | 12 |
| Energía potencial gravitatoria | `t5_g_001`–`t5_g_010` | 10 |
| Energía elástica | `t5_e_001`–`t5_e_010` | 10 |
| Balances, disipación e integración | `t5_b_001`–`t5_b_014` | 14 |
| **Total** |  | **60** |

## 2. Contrato editorial y técnico

- Cada problema declara estado inicial/final y frontera del sistema.
- Trabajo es transferencia; energía cinética y potencial son estados. El signo se vincula con la dirección y el proceso.
- En `F(x)`, el trabajo es área con signo. En potencia se distingue media de instantánea.
- La referencia de energía potencial es libre, pero las diferencias deben coincidir.
- Respuestas: número, función, vector, selección, unidad o texto corto cerrado. No se pedirán demostraciones ni redacciones.
- Los SVG usarán barras de energía, trayectorias con niveles, gráficas fuerza-desplazamiento y diagramas de flujo.

### Metadatos previstos para el JSON

Todos usarán `course: 1bach`, `topic: t5`, `status: draft`, `version: 1`, `response_mode: structured` y origen `original_teacher_bank`. W/K/G comienzan en dificultad 2 (`6–11 min`), E en 3 (`8–13 min`) y B en 3–5 (`10–18 min`). Etiquetas comunes: `work_energy`, la familia, `system_boundary` cuando proceda y la representación visual. Las auditorías añaden `energy_accounting`.

## 3. Inventario de ejercicios

### Bloque W - Trabajo y fuerzas variables (14)

| ID | Actividad y datos | Clave estructurada | SVG/gráfica |
|---|---|---|---|
| `t5_w_001` | Fuerza `20 N` paralela durante `5 m`. | `W=100 J`; selección signo positivo. | Fuerza y desplazamiento. |
| `t5_w_002` | Fuerza `30 N` a `60°`, desplazamiento `4 m`. | `W=60 J`. | Triángulo y proyección útil. |
| `t5_w_003` | Rozamiento `12 N` opuesto durante `7 m`. | `W=-84 J`. | Flechas opuestas y barra de transferencia. |
| `t5_w_004` | Peso en desplazamiento horizontal. | `W_P=0 J`; selección por perpendicularidad. | Ángulo `90°`. |
| `t5_w_005` | Elevar `3 kg` verticalmente `2 m` a velocidad constante. | `W_P=-58,8 J`; `W_ap=+58,8 J`; neto `0`. | Estados inicial/final. |
| `t5_w_006` | Fuerza constante vectorial `(4;3) N`, desplazamiento `(5;-2) m`. | Producto escalar `14 J`. | Vectores en plano. |
| `t5_w_007` | Gráfica rectangular `F=10 N`, `0–3 m`. | Área/trabajo `30 J`. | `F-x` sombreada. |
| `t5_w_008` | Fuerza crece linealmente `0→12 N` en `4 m`. | Trabajo `24 J`; fuerza media `6 N`. | Triángulo bajo `F-x`. |
| `t5_w_009` | `F-x` cruza eje: `+8 N` dos metros y `-4 N` tres metros. | Trabajos `16`, `-12`; neto `4 J`. | Áreas con colores de signo. |
| `t5_w_010` | Función `F(x)=3x²`, `0≤x≤2`. | `W=8 J`; unidad del coeficiente `N/m²`. | Curva y área. |
| `t5_w_011` | Fuerza por tramos triangular-trapezoidal. | Tres áreas y suma numérica. | Panel con vértices etiquetados. |
| `t5_w_012` | Comparar dos caminos bajo fuerza uniforme gravitatoria entre mismas alturas. | Selección: mismo trabajo; valor `-mgΔh`. | Dos trayectorias. |
| `t5_w_013` | Fuerza radial en movimiento circular uniforme. | Trabajo instantáneo/total `0 J`. | Tangente y radio perpendiculares. |
| `t5_w_014` | Auditar `W=Fd` para `F=50 N`, `d=3 m` y `60°` entre ambos. | Seleccionar `W=Fd cosθ`; resultado `75 J`. | Resolución ficticia y proyección. |

### Bloque K - Energía cinética y potencia (12)

| ID | Actividad y datos | Clave estructurada | SVG/gráfica |
|---|---|---|---|
| `t5_k_001` | `m=2 kg`, rapidez `3 m/s`. | `K=9 J`. | Barra de energía cinética. |
| `t5_k_002` | Duplicar rapidez con masa fija. | Razón `K_2/K_1=4`. | Barras comparativas. |
| `t5_k_003` | Trabajo neto `50 J` desde reposo, `m=4 kg`. | `v=5 m/s`. | Flujo trabajo→cinética. |
| `t5_k_004` | `m=1000 kg`, `v_i=20`, `v_f=10 m/s`. | Trabajo neto `-150 kJ`. | Estados y barras `K`. |
| `t5_k_005` | Frenada con fuerza constante `6000 N` del coche anterior. | Distancia `25 m`. | Trayectoria de frenada. |
| `t5_k_006` | Fuerza neta variable dada por `F-x`; partir con `v_0=2`. | Trabajo por área y rapidez final. | Gráfica más estados. |
| `t5_k_007` | Máquina hace `12 kJ` en `8 s`. | Potencia media `1,5 kW`. | Línea temporal. |
| `t5_k_008` | Elevador `500 kg` sube a `2 m/s` constante. | Potencia `9,8 kW`. | Ascensor y flujo energético. |
| `t5_k_009` | Vehículo `F=800 N` a `v=15 m/s`. | Potencia instantánea `12 kW`. | Vectores paralelos. |
| `t5_k_010` | Fuerza a `60°` respecto de `v`, `F=100`, `v=4`. | `P=200 W`. | Ángulo fuerza-velocidad. |
| `t5_k_011` | Gráfica `P(t)` escalonada. | Energía transferida por áreas; resultado en J. | `P-t` con áreas. |
| `t5_k_012` | Elegir gráfica `K(v)` y `P(v)` para fuerza constante. | Opciones correctas: cuadrática y lineal. | Cuatro pares de curvas. |

### Bloque G - Energía potencial gravitatoria (10)

| ID | Actividad y datos | Clave estructurada | SVG/gráfica |
|---|---|---|---|
| `t5_g_001` | `m=3 kg`, subir `5 m`. | `ΔU_g=147 J`; trabajo del peso `-147 J`. | Dos niveles. |
| `t5_g_002` | Cambiar referencia de suelo a mesa. | Dos valores absolutos, misma `ΔU`. | Ejes de energía con ceros distintos. |
| `t5_g_003` | Caída desde `20 m`, sin aire. | Rapidez `19,8 m/s`; barras inicial/final. | Torre y energía. |
| `t5_g_004` | Rampa sin rozamiento con desnivel `3 m`. | Rapidez final `7,67 m/s`, independiente de forma. | Dos rampas. |
| `t5_g_005` | Lanzamiento vertical `v_0=14 m/s`. | Altura adicional `10 m`. | Estados salida/cima. |
| `t5_g_006` | Montaña rusa: alturas `20→5 m`, parte del reposo. | `v=17,1 m/s`. | Perfil con niveles. |
| `t5_g_007` | Velocidad mínima para superar colina de `8 m`. | `v_min=12,5 m/s`. | Perfil y punto de retorno. |
| `t5_g_008` | Elegir gráfico `U_g(h)` para varios ceros. | Pendiente `mg`; opciones equivalentes por constante. | Tres rectas paralelas. |
| `t5_g_009` | Plano inclinado: relacionar recorrido `s` y altura `s sinθ`. | Función `U(s)=mg s sinθ+C`. | Geometría de rampa. |
| `t5_g_010` | Auditar afirmación “la energía potencial pertenece al objeto”. | Selección: pertenece al sistema de interacción; `ΔU` numérico. | Fronteras objeto/Tierra. |

### Bloque E - Energía elástica (10)

| ID | Actividad y datos | Clave estructurada | SVG/gráfica |
|---|---|---|---|
| `t5_e_001` | Muelle `k=200`, deformación `0,10 m`. | `U_e=1 J`. | Longitud natural/deformada. |
| `t5_e_002` | Duplicar deformación. | Razón de energías `4`. | Parábola `U(x)`. |
| `t5_e_003` | Trabajo del muelle de `x=0,12` a `0`. `k=100`. | `+0,72 J`. | Área triangular `F-x`. |
| `t5_e_004` | Trabajo externo cuasiestático al comprimir `0→0,08`, `k=250`. | `0,8 J`. | Fuerza aplicada creciente. |
| `t5_e_005` | Muelle lanza bloque `0,5 kg`, `k=200`, `x=0,10`, sin rozamiento. | `v=2 m/s`. | Estado comprimido/salida. |
| `t5_e_006` | Muelle vertical: comparar referencia natural y equilibrio. | `x_eq=mg/k`; energía total con ambas referencias. | Dos ceros geométricos. |
| `t5_e_007` | Dos muelles en paralelo almacenan energía. | `U=½(k_1+k_2)x²`. | Montaje paralelo y barras. |
| `t5_e_008` | Muelles en serie `k_1=100`, `k_2=200 N/m` sometidos a `F=10 N`. | Deformaciones `0,10`, `0,05 m`; energías `0,50`, `0,25 J`; total `0,75 J`. | Deformaciones separadas. |
| `t5_e_009` | La curva da `U=0,90 J` cuando `x=0,15 m`. | `k=2U/x²=80 N/m`. | Datos `U-x`. |
| `t5_e_010` | Auditar `U=kx` para `k=120 N/m`, `x=0,10 m`. | Seleccionar `U=½kx²`; unidad `J`; resultado `0,60 J`. | Tarjetas de fórmulas dimensionales. |

### Bloque B - Balances, disipación e integración (14)

| ID | Actividad y datos | Clave estructurada | SVG/gráfica |
|---|---|---|---|
| `t5_b_001` | Bloque baja `4 m` de altura con rozamiento que hace `-30 J`, `m=2`. | `K_f=48,4 J`; `v=6,96 m/s`. | Barras `U`, térmica y `K`. |
| `t5_b_002` | Rampa rugosa, hallar `μ_k` desde rapidez final. | Balance cerrado y `μ_k` numérico. | Perfil y frontera del sistema. |
| `t5_b_003` | Muelle impulsa bloque por zona rugosa hasta detenerse. | Distancia `d=kx²/(2μmg)`. | Muelle-zona rugosa. |
| `t5_b_004` | Bloque cae sobre muelle vertical: compresión máxima. | Ecuación cuadrática y raíz física seleccionada. | Tres estados verticales. |
| `t5_b_005` | Montaña rusa con bucle: energía + condición dinámica mínima arriba. | `v_top=√(gr)` y altura inicial `2,5r`. | Bucle y barras por estado. |
| `t5_b_006` | Péndulo soltado desde ángulo `60°`, longitud `1 m`. | Rapidez abajo `3,13 m/s`. | Arco y niveles. |
| `t5_b_007` | Columpio pierde `15%` de energía por oscilación. | Factor de altura `0,85`; tras 3, `0,85³`. | Barras decrecientes. |
| `t5_b_008` | Motor sube carga con rendimiento `80%`. | Potencia de entrada `P_útil/0,8`. | Diagrama de Sankey simple. |
| `t5_b_009` | Comparar tres sistemas para el mismo descenso con rozamiento. | Selección de términos internos/externos. | Fronteras superpuestas. |
| `t5_b_010` | Gráfica de energía potencial `U(x)` con mínimos y máximos. | Equilibrios, estabilidad y fuerza por pendiente seleccionados. | Paisaje energético. |
| `t5_b_011` | Dada energía total horizontal, hallar regiones permitidas. | Intervalo de `x` donde `E≥U(x)`. | `U(x)` y línea `E`. |
| `t5_b_012` | Fuerza conservativa desde `U(x)=2x²-4x`. | `F(x)=-4x+4`; equilibrio `x=1`. | Panel `U`/`F`. |
| `t5_b_013` | Auditoría de balance que suma simultáneamente trabajo del peso y `ΔU_g`. | Seleccionar doble conteo; ecuación corregida. | Libro mayor de energía. |
| `t5_b_014` | Investigación cerrada de carrito: datos de altura/rapidez estiman pérdida y eficiencia. | `E_i`, `E_f`, pérdida y porcentaje. | Datos, perfil y barras. |

## 4. Sistema visual

Se prevén **al menos 40 SVG**: áreas `F-x` y `P-t`, diagramas de estados, barras de energía alineadas, perfiles de trayectoria, fronteras del sistema, paisajes `U(x)` y flujos tipo Sankey sencillos. Ninguna barra mostrará el valor desconocido antes de responder.

## 5. Criterios de aceptación antes del JSON

1. Los 60 ejercicios declaran sistema y estados cuando el balance lo necesita.
2. Todos los signos y áreas se verifican analítica y gráficamente.
3. Las respuestas conceptuales usan opciones físicamente distintas y unívocas.
4. No hay doble conteo de trabajo conservativo y cambio de potencial.
5. Los resultados incluyen unidades, tolerancia y raíz/intervalo físico.
6. No se añaden fuentes externas en esta fase.
