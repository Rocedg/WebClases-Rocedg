# Banco editorial T6 v1 - Momento lineal, impulso y choques

**Curso:** 1.º de Bachillerato
**Tema:** T6 - Momento lineal, impulso y choques
**Estado:** referencia editorial completa previa al catálogo JSON
**Fecha:** 21 de septiembre de 2026

## 1. Propósito del banco

T6 debe hacer visible qué se conserva, durante qué intervalo y para qué sistema. Los ejercicios conectan vectores de momento, áreas bajo `F(t)`, fuerzas internas/externas, separaciones y distintos tipos de choque. Se comprueba el momento antes y después y se usa la energía cinética como diagnóstico, no como conservación automática. El banco contiene **60 ejercicios originales** y estructurados.

| Bloque | IDs | Cantidad |
|---|---:|---:|
| Momento e impulso | `t6_i_001`–`t6_i_012` | 12 |
| Sistemas y conservación | `t6_s_001`–`t6_s_010` | 10 |
| Separaciones y retroceso | `t6_x_001`–`t6_x_008` | 8 |
| Choques y restitución | `t6_c_001`–`t6_c_018` | 18 |
| Integración, gráficas y auditoría | `t6_a_001`–`t6_a_012` | 12 |
| **Total** |  | **60** |

## 2. Contrato editorial y técnico

- Se declara el sistema y el eje antes de escribir conservación.
- El momento es vectorial; los signos codifican sentidos y no se sustituyen por módulos.
- El impulso es área con signo bajo `F(t)` y equivale al cambio de momento.
- Solo se conserva el momento del sistema si el impulso externo es despreciable en el intervalo.
- Se distingue choque elástico, inelástico y perfectamente inelástico mediante momento, restitución y energía.
- Respuestas: número, vector, función, selección, unidad o texto corto cerrado. No habrá redacción libre ni pistas.
- Los diagramas mostrarán líneas temporales antes/durante/después, fronteras, vectores y gráficas fuerza-tiempo.

### Metadatos previstos para el JSON

Todos usarán `course: 1bach`, `topic: t6`, `status: draft`, `version: 1`, `response_mode: structured` y origen `original_teacher_bank`. I/S empiezan en dificultad 2 (`6–11 min`), X/C en 3 (`8–15 min`) y A en 4–5 (`12–18 min`). Etiquetas comunes: `momentum`, la familia, `system_boundary` y la representación visual; las comprobaciones energéticas añaden `collision_classification` y las auditorías `model_check`.

## 3. Inventario de ejercicios

### Bloque I - Momento e impulso (12)

| ID | Actividad y datos | Clave estructurada | SVG/gráfica |
|---|---|---|---|
| `t6_i_001` | Pelota `0,4 kg` a `5 m/s` hacia `+x`. | `p=+2 kg·m/s`. | Vector sobre eje. |
| `t6_i_002` | Dos objetos: `2 kg` a `3 m/s`, `1 kg` a `-4 m/s`. | Momentos `6`, `-4`; total `+2 kg·m/s`. | Barras/vector suma. |
| `t6_i_003` | Cambiar velocidad de `-2` a `+6 m/s`, `m=0,5`. | `J=+4 N·s`. | Antes/después. |
| `t6_i_004` | Fuerza constante `20 N` durante `0,3 s`. | Impulso `6 N·s`. | Rectángulo `F-t`. |
| `t6_i_005` | Pulso triangular, pico `100 N`, duración `0,04 s`. | Impulso `2 N·s`; fuerza media `50 N`. | Triángulo `F-t`. |
| `t6_i_006` | Fuerza cambia de signo en dos tramos. | Áreas positiva/negativa y neta. | `F-t` bicolor. |
| `t6_i_007` | Misma variación de momento con `0,02` y `0,10 s`. | Razón de fuerzas medias `5`. | Dos pulsos con igual área. |
| `t6_i_008` | Airbag alarga impacto de `0,03` a `0,15 s`. | Fuerza media se reduce a `1/5`; impulso igual. | Pulsos ancho/alto. |
| `t6_i_009` | Pelota llega a pared a `+8` y sale a `-6 m/s`, `m=0,2`. | `Δp=-2,8`; impulso sobre pared `+2,8 N·s`. | Pares de impulso. |
| `t6_i_010` | Hallar velocidad final desde impulso `-12 N·s`, `m=3`, `v_i=5`. | `v_f=1 m/s`. | Línea temporal. |
| `t6_i_011` | Fuerza `F(t)=6t`, `0–2 s`, cuerpo `2 kg` desde reposo. | `J=12 N·s`; `v_f=6 m/s`. | Curva `F-t` y área. |
| `t6_i_012` | Auditar impulso=`F/t` para `F=40 N` durante `0,15 s`. | Seleccionar `J=FΔt`; unidad `N·s`; resultado `6 N·s`. | Tarjetas dimensionales. |

### Bloque S - Sistemas y conservación (10)

| ID | Actividad y datos | Clave estructurada | SVG/gráfica |
|---|---|---|---|
| `t6_s_001` | Dos patinadores se empujan desde reposo. | Momento total inicial/final `0`; relación `m_1v_1=-m_2v_2`. | Frontera conjunta. |
| `t6_s_002` | Elegir sistema para choque de dos carros durante `0,05 s`. | Selección conjunto de carros; impulso externo despreciable. | Fronteras candidatas. |
| `t6_s_003` | Persona camina dentro de barca inicialmente en reposo. | Centro de masas fijo; velocidades opuestas con relación de masas. | Persona/barca y orilla. |
| `t6_s_004` | Dos masas con fuerza interna variable. | Momento total constante; momentos individuales cambian. | Gráficas `p_1`, `p_2`, `p_total`. |
| `t6_s_005` | Carro de `2 kg` tiene `p_i=4 kg·m/s` y recibe `J_ext=-1,5 N·s`. | `p_f=2,5 kg·m/s`; `v_f=1,25 m/s`. | Frontera y flecha externa. |
| `t6_s_006` | Explosión durante caída: componente horizontal. | `p_x` se conserva; `p_y` cambia por gravedad. | Vectores 2D y gravedad. |
| `t6_s_007` | Comparar intervalo muy corto y largo bajo el mismo peso. | Selección cuándo despreciar impulso externo; valores de `mgΔt`. | Dos escalas temporales. |
| `t6_s_008` | Carros de `2` y `3 kg` llevan velocidades `4` y `-1 m/s` antes de interactuar. | `p_total=5 kg·m/s`; `v_CM=1 m/s`, igual antes y después. | Eje y marcador CM. |
| `t6_s_009` | Sistema abierto expulsa masa de forma discreta. | Balance de momento para dos fragmentos, no fórmula continua. | Antes/después con frontera. |
| `t6_s_010` | Auditar conservación aplicada a un solo objeto durante choque. | Sistema correcto seleccionado; fuerza interna identificada. | Dos soluciones paralelas. |

### Bloque X - Separaciones y retroceso (8)

| ID | Actividad y datos | Clave estructurada | SVG/gráfica |
|---|---|---|---|
| `t6_x_001` | Patinadores `50` y `75 kg`; primero sale a `3 m/s`. | Segundo `-2 m/s`. | Antes/después. |
| `t6_x_002` | Cañón `500 kg`, proyectil `5 kg` a `100 m/s`. | Retroceso `-1 m/s`. | Vectores de distinto tamaño/escala. |
| `t6_x_003` | Carro `6 kg` se divide en `2` y `4 kg`; fragmento ligero `+8`. | Fragmento pesado `-4 m/s`. | Separación en eje. |
| `t6_x_004` | Objeto en movimiento `M=10`, `v=4` se separa en `4` y `6 kg`; uno queda en reposo. | Otro `6,67 m/s`. | Momento inicial y final. |
| `t6_x_005` | Dos fragmentos salen perpendiculares desde reposo imposible sin tercero. | Selección: momento vectorial no suma cero; vector tercero requerido. | Polígono de momentos. |
| `t6_x_006` | Explosión 2D: `p_1=(6;0)`, `p_2=(0;8)`, inicial cero. | `p_3=(-6;-8)`; módulo `10`. | Triángulo cerrado. |
| `t6_x_007` | Energía aumenta en separación desde reposo. | Selección: energía interna se transforma; `ΔK` numérico. | Barras de energía y momento. |
| `t6_x_008` | Auditar signos de retroceso cuando ambos resultados se dan positivos. | Velocidad con signo corregida y comprobación de suma cero. | Eje y tabla de signos. |

### Bloque C - Choques y restitución (18)

| ID | Actividad y datos | Clave estructurada | SVG/gráfica |
|---|---|---|---|
| `t6_c_001` | Choque perfectamente inelástico: `2 kg·3 m/s` alcanza `1 kg` en reposo. | Velocidad conjunta `2 m/s`; pérdida `3 J`. | Secuencia antes/después. |
| `t6_c_002` | Choque frontal: `1 kg` a `4`, `1 kg` a `-2`, se pegan. | `v_f=1 m/s`; pérdida `9 J`. | Eje con signos. |
| `t6_c_003` | Bala-bloque: `0,01 kg` a `300`, bloque `1,49` en reposo. | Velocidad conjunta `2 m/s`. | Escalas separadas antes/después. |
| `t6_c_004` | Masa `2 kg` choca con otra de `3 kg` en reposo y quedan juntas a `2 m/s`. | Velocidad incidente `5 m/s`. | Línea temporal. |
| `t6_c_005` | Choque elástico de masas iguales, una en reposo. | Intercambio de velocidades seleccionado y calculado. | Cuatro opciones vectoriales. |
| `t6_c_006` | Elástico 1D `m_1=1`, `m_2=3`, `u_1=4`, `u_2=0`. | `v_1=-2`, `v_2=2 m/s`. | Antes/después. |
| `t6_c_007` | Elástico con masas `3` y `1`, mismo `u_1=4`. | `v_1=2`, `v_2=6 m/s`. | Comparación con el anterior. |
| `t6_c_008` | Comprobar elasticidad desde velocidades medidas. | Momento antes/después y razón `K_f/K_i=1`. | Barras dobles. |
| `t6_c_009` | Choque conserva momento pero pierde `40%` de `K`. | Clasificación inelástico; energía perdida numérica. | Diagrama `p` constante/`K` decrece. |
| `t6_c_010` | Coeficiente de restitución con velocidades dadas. | `e=|v_2-v_1|/|u_1-u_2|`; valor cerrado. | Velocidades relativas. |
| `t6_c_011` | `e=0`: interpretar y calcular velocidad común. | Perfectamente inelástico; `v_f`. | Objetos unidos. |
| `t6_c_012` | `e=1`: resolver junto con momento. | Dos velocidades finales. | Sistema de dos ecuaciones visual. |
| `t6_c_013` | `e=0,5`, masas iguales, una en reposo, `u=6`. | `v_1=1,5`, `v_2=4,5 m/s`. | Separación relativa. |
| `t6_c_014` | Pelota rebota en suelo: `u_y=-10`, `e=0,8`. | `v_y=+8`; porcentaje de energía vertical `64%`. | Impacto vertical. |
| `t6_c_015` | Dos cuerpos se mueven juntos: determinar si puede saberse que fue inelástico. | Selección: estado final común implica perfectamente inelástico en 1D. | Fotogramas. |
| `t6_c_016` | Choque 2D con objeto inicialmente en reposo y vectores finales perpendiculares. | Vector momento inicial y una velocidad desconocida por componentes. | Triángulo de momentos. |
| `t6_c_017` | Billar ideal, masas iguales, una en reposo; finales perpendiculares. | Relación pitagórica de velocidades y ángulos. | Vista superior. |
| `t6_c_018` | Auditar solución que conserva energía cinética en choque pegajoso. | Paso erróneo seleccionado; velocidad correcta y pérdida. | Dos balances contrapuestos. |

### Bloque A - Integración, gráficas y auditoría (12)

| ID | Actividad y datos | Clave estructurada | SVG/gráfica |
|---|---|---|---|
| `t6_a_001` | Reconstruir velocidad desde sensor `F(t)` de impacto y masa conocida. | Área, `Δp`, velocidad final. | Pulso experimental suavizado. |
| `t6_a_002` | Comparar dos cascos con igual impulso y picos distintos. | Selección del menor pico/mayor duración; áreas iguales. | Pulsos superpuestos. |
| `t6_a_003` | Choque pegajoso seguido de frenada por rozamiento. | Etapa 1 momento; etapa 2 energía/cinemática; distancia final. | Línea temporal en dos modelos. |
| `t6_a_004` | Bala-bloque-péndulo: impacto y ascenso. | Velocidad conjunta por altura; velocidad de bala por momento. | Péndulo balístico en dos etapas. |
| `t6_a_005` | Carro `1 kg` a `6 m/s` se pega a otro de `2 kg`; después comprimen un muelle `k=300 N/m` sin rozamiento. | Velocidad conjunta `2 m/s`; energía elástica `6 J`; compresión máxima `0,20 m`. | Choque→muelle comprimido. |
| `t6_a_006` | Elegir sistema y ley para cinco fases de una interacción. | Secuencia cerrada: impulso, momento, energía. | Diagrama de decisiones. |
| `t6_a_007` | Gráficas de fuerzas mutuas durante choque. | `F_12(t)=-F_21(t)`; impulsos opuestos. | Dos pulsos especulares. |
| `t6_a_008` | Datos con incertidumbre: decidir si momento se conserva dentro de tolerancia. | Diferencia relativa y selección sí/no por umbral. | Barras con intervalos. |
| `t6_a_009` | Hallar masa desconocida desde choque y velocidades medidas. | Ecuación de momento y masa positiva. | Fotogramas con velocidades. |
| `t6_a_010` | Detectar datos físicamente incompatibles (`e>1` sin aporte energético declarado). | `e` calculado y opción “superelástico/no compatible con modelo pasivo”. | Velocidades relativas. |
| `t6_a_011` | Movimiento 2D: explosión y caída posterior. | Momento horizontal en explosión; alcance de fragmento con cinemática. | Secuencia vectorial y trayectorias. |
| `t6_a_012` | Miniinvestigación cerrada de choque: clasificar, calcular `e`, pérdida y seleccionar gráfico. | Cuatro campos numéricos/cerrados. | Antes/después, barras y gráfica `F(t)`. |

## 4. Sistema visual

Se prevén **al menos 44 SVG**. Habrá secuencias antes/durante/después, fronteras de sistema, polígonos de momento, pulsos `F-t`, barras comparativas de momento y energía, y trayectorias 2D. La escala de flechas debe ser coherente o declararse cualitativa.

## 5. Criterios de aceptación antes del JSON

1. Los 60 ejercicios declaran eje, sistema e intervalo de interacción.
2. Cada choque comprueba momento; la energía cinética solo se conserva cuando el modelo lo autoriza.
3. Los resultados vectoriales mantienen signos y unidades coherentes.
4. Las preguntas de comprensión son selecciones verificables basadas en sistema, impulso, restitución o energía.
5. Las soluciones por etapas no mezclan las leyes aplicables al choque con las del movimiento posterior.
6. No se añaden fuentes externas ni PAU en esta fase.
