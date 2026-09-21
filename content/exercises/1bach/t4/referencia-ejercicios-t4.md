# Banco editorial T4 v1 - Rozamiento y aplicaciones de las fuerzas

**Curso:** 1.º de Bachillerato
**Tema:** T4 - Rozamiento y aplicaciones de las fuerzas
**Estado:** referencia editorial completa previa al catálogo JSON
**Fecha:** 21 de septiembre de 2026

## 1. Propósito del banco

T4 se centra en decidir qué modelo físico corresponde antes de calcular: reposo o deslizamiento, límite estático o rozamiento cinético, curva plana o peraltada, y muelle en longitud natural o deformado. Los ejercicios conectan DCL, desigualdades, gráficas experimentales y condiciones límite. El banco contiene **60 ejercicios originales**, todos corregibles de forma estructurada.

| Bloque | IDs | Cantidad |
|---|---:|---:|
| Rozamiento estático y cinético | `t4_r_001`–`t4_r_016` | 16 |
| Planos con rozamiento | `t4_p_001`–`t4_p_012` | 12 |
| Curvas planas y peraltadas | `t4_c_001`–`t4_c_010` | 10 |
| Muelles y ley de Hooke | `t4_m_001`–`t4_m_012` | 12 |
| Experimento, integración y auditoría | `t4_i_001`–`t4_i_010` | 10 |
| **Total** |  | **60** |

## 2. Contrato editorial y técnico

- El rozamiento estático se calcula por equilibrio hasta `f_s,max=μ_sN`; no se sustituye siempre por su máximo.
- El sentido del rozamiento se decide por la tendencia de deslizamiento entre superficies.
- En curvas, “centrípeta” nombra la resultante radial, no una fuerza extra.
- En muelles se declara referencia, signo y longitud natural; `F=-kx` se interpreta vectorialmente.
- Respuestas admitidas: número, vector, función, unidad, selección o texto corto de vocabulario cerrado.
- No habrá pistas, dibujos entregados por el alumno ni explicaciones abiertas.
- Las soluciones posteriores mostrarán el cambio de régimen y comprobarán límites/unidades.

### Metadatos previstos para el JSON

Todos usarán `course: 1bach`, `topic: t4`, `status: draft`, `version: 1`, `response_mode: structured` y origen `original_teacher_bank`. R comienza en dificultad 2; P/M en 3; C e I en 3–4. Cada familia progresa hasta 4 o 5, con tiempos de `7–17 min`. Etiquetas comunes: `friction`, `model_selection`, la familia y el tipo visual; los ajustes experimentales añaden `data_analysis` y las auditorías `model_check`.

## 3. Inventario de ejercicios

### Bloque R - Rozamiento estático y cinético (16)

| ID | Actividad y datos | Clave estructurada | SVG/gráfica |
|---|---|---|---|
| `t4_r_001` | Caja `10 kg`, `μ_s=0,4`, empuje `20 N`. | Reposo; `f_s=20 N`; `f_s,max=39,2 N`. | DCL y barra de margen estático. |
| `t4_r_002` | Misma caja con empuje `45 N`, `μ_k=0,3`. | Desliza; `f_k=29,4 N`; `a=1,56 m/s²`. | Gráfica fuerza aplicada/rozamiento. |
| `t4_r_003` | Barrido `F` de `0` a `60 N` en caja anterior. | Función por tramos de `f(F)` y umbral `39,2 N`. | Panel `f` frente a `F`. |
| `t4_r_004` | Bloque `5 kg`, tirón `30 N` a `25°`, `μ_k=0,2`. | `N=36,3 N`; `f_k=7,26 N`; `a=4,00 m/s²`. | Fuerza oblicua hacia arriba. |
| `t4_r_005` | Mismos datos empujando `25°` hacia abajo. | `N=61,7 N`; `f_k=12,3 N`; `a=3,00 m/s²`. | Comparación tirar/empujar. |
| `t4_r_006` | Hallar fuerza horizontal mínima para mover `m=12 kg`, `μ_s=0,35`. | `F_min=41,2 N`. | Umbral con bloque aún en reposo. |
| `t4_r_007` | Dos superficies con mismo `μ`, masas `4` y `8 kg`. | Razón `f_k2/f_k1=2`; misma desaceleración `μg`. | Dos bloques y gráfica `v(t)`. |
| `t4_r_008` | Bloque lanzado a `6 m/s`, `μ_k=0,25`. | `a=-2,45 m/s²`; parada `2,45 s`; distancia `7,35 m`. | Trayectoria y panel `v(t)`. |
| `t4_r_009` | Determinar `μ_k` desde parada: `v_0=8 m/s`, `d=10 m`. | `μ_k=0,327`. | Gráfica `v²` frente a distancia. |
| `t4_r_010` | Caja sobre camión acelera `2 m/s²`, `μ_s=0,25`. | No desliza; `f_s=ma`; límite de aceleración `2,45 m/s²`. | Caja/camión y tendencia relativa. |
| `t4_r_011` | Camión frena a `4 m/s²`, `μ_s=0,3`. | Desliza; dirección del rozamiento sobre caja hacia atrás; máximo `2,94 m/s²`. | Dos marcos temporales. |
| `t4_r_012` | Dos bloques apilados, superior `2 kg`, inferior acelerado a `3 m/s²`, `μ_s=0,4`. | `f_s=6 N`; no desliza; umbral `3,92 m/s²`. | DCL separados de ambos bloques. |
| `t4_r_013` | Empuje horizontal sobre pared mantiene bloque `1 kg`, `μ_s=0,5`. | Empuje mínimo `19,6 N`; rozamiento vertical `9,8 N`. | Pared y fuerzas perpendiculares. |
| `t4_r_014` | Comparar área de contacto doble con misma masa/material. | Selección: modelo seco ideal da mismo rozamiento. | Dos bases y fuerzas iguales. |
| `t4_r_015` | Tabla experimental `N-f_k` lineal. | Pendiente `μ_k`; con datos `(20,6),(40,12),(60,18)`, `μ_k=0,30`. | Dispersión por el origen. |
| `t4_r_016` | Auditar solución que usa `μ_sN` aunque el cuerpo está en reposo con fuerza pequeña. | Error seleccionado; valor correcto de `f_s` igual a fuerza aplicada. | Dos curvas y paso erróneo resaltado. |

### Bloque P - Planos con rozamiento (12)

| ID | Actividad y datos | Clave estructurada | SVG/gráfica |
|---|---|---|---|
| `t4_p_001` | Bloque `5 kg`, plano `20°`, `μ_s=0,4`. | Reposo; `f_s=16,8 N`; máximo `18,4 N`. | DCL con tendencia cuesta abajo. |
| `t4_p_002` | Aumentar ángulo hasta inicio de deslizamiento, `μ_s=0,4`. | `θ_c=21,8°`; relación `tanθ_c=μ_s`. | Plano de inclinación variable. |
| `t4_p_003` | Plano `30°`, `μ_k=0,2`, bloque desliza abajo. | `a=3,20 m/s²`; `N=mg cos30°`. | Fuerzas paralelas opuestas. |
| `t4_p_004` | Bloque sube inicialmente por plano anterior. | `a=-6,60 m/s²` con eje arriba; parada desde `v_0=5`: `0,758 s`. | Vectores velocidad/rozamiento. |
| `t4_p_005` | Tras pararse, decidir si vuelve a bajar con `μ_s=0,4`. | Sí, porque `tan30°>0,4`; selección de régimen posterior. | Línea temporal de dos fases. |
| `t4_p_006` | Fuerza paralela mantiene velocidad constante cuesta arriba, `m=8`, `θ=25°`, `μ_k=0,15`. | `F=44,1 N`. | DCL y eje local. |
| `t4_p_007` | Fuerza horizontal `60 N` sobre `m=10 kg`, plano `30°`, `μ_k=0,2`. | `N=114,9 N`; componente paralela `52,0 N`; aceleración `-1,90 m/s²` si arriba positivo. | Descomposición de fuerza horizontal. |
| `t4_p_008` | Bloque en plano unido a masa colgante; incluir rozamiento. `m_1=4`, `m_2=3`, `θ=30°`, `μ_k=0,1`. | Sentido hacia `m_2`; `a=0,915 m/s²`; `T=26,7 N`. | Dos DCL y sentido comprobado. |
| `t4_p_009` | Hallar masa colgante para equilibrio en límite de subir, con `m_1=5 kg`, `θ=25°`, `μ_s=0,30`. | `m_2=m_1(sinθ+μ_s cosθ)=3,47 kg`. | Dos límites, subir/bajar. |
| `t4_p_010` | Rango de masa colgante que permite reposo. | Intervalo estructurado `[m_min;m_max]`. | Banda de equilibrio visual. |
| `t4_p_011` | Comparar un bloque que baja por `θ=30°` con `μ=0` y con `μ_k=0,20`. | `a_0=4,90 m/s²`; `a_μ=3,20 m/s²`; razón `0,653`; función `a(μ)=g(sinθ-μcosθ)`. | Gráfica lineal con corte. |
| `t4_p_012` | Diagnóstico de signo: alumno pone rozamiento siempre cuesta arriba. | Seleccionar caso incorrecto: bloque que sube; dirección correcta cuesta abajo. | Cuatro viñetas de tendencia. |

### Bloque C - Curvas planas y peraltadas (10)

| ID | Actividad y datos | Clave estructurada | SVG/gráfica |
|---|---|---|---|
| `t4_c_001` | Coche `1000 kg`, curva plana `r=50 m`, `v=10 m/s`. | Rozamiento requerido `2000 N`; `μ_s,min=0,204`. | Vista superior y DCL lateral. |
| `t4_c_002` | Velocidad máxima en curva plana `r=80 m`, `μ_s=0,5`. | `v_max=19,8 m/s`. | Curva y vector radial. |
| `t4_c_003` | Lluvia reduce `μ_s` de `0,6` a `0,3`. | Razón de velocidades máximas `√0,5=0,707`. | Dos arcos con zonas seca/mojada. |
| `t4_c_004` | Curva peraltada sin rozamiento `r=100 m`, `θ=12°`. | `v=14,4 m/s`. | Sección transversal y componentes de `N`. |
| `t4_c_005` | Hallar peralte para `v=20 m/s`, `r=120 m`. | `θ=18,8°`. | Triángulo de la carretera. |
| `t4_c_006` | Elegir sentido del rozamiento si velocidad es menor que la de diseño. | Selección: hacia arriba del peralte. | Tres DCL candidatos. |
| `t4_c_007` | Elegir sentido si velocidad es mayor que diseño. | Selección: hacia abajo del peralte. | Continuación del anterior. |
| `t4_c_008` | Ciclista inclinado en curva plana, `v=8`, `r=20`. | `tanφ=v²/(rg)`; `φ=18,1°`. | Bicicleta y resultante de contacto. |
| `t4_c_009` | Curva con rapidez variable: comparar fuerza radial en `v` y `2v`. | Razón `4`; gráfica cuadrática seleccionada. | `F_r(v)` con distractores. |
| `t4_c_010` | Auditar “normal + peso + centrípeta = ma”. | Eliminar centrípeta; elegir componentes que producen resultante radial. | DCL erróneo en curva peraltada. |

### Bloque M - Muelles y ley de Hooke (12)

| ID | Actividad y datos | Clave estructurada | SVG/gráfica |
|---|---|---|---|
| `t4_m_001` | Muelle `k=200 N/m` estirado `3 cm`. | Fuerza `6 N` hacia el equilibrio. | Escala longitud natural/deformada. |
| `t4_m_002` | Compresión `5 cm`, eje positivo a la derecha. | `x=-0,05 m`; `F=+10 N` para `k=200`. | Eje y signos. |
| `t4_m_003` | Masa colgada `0,5 kg`, `k=100 N/m`. | Alargamiento de equilibrio `0,049 m`. | Dos referencias: natural y equilibrio. |
| `t4_m_004` | Añadir `0,2 kg` a la masa anterior. | Incremento de alargamiento `0,0196 m`; total `0,0686 m`. | Regla vertical con dos posiciones. |
| `t4_m_005` | Gráfica `F-x` experimental. | Pendiente `k=150 N/m`; función `F=-150x`. | Puntos con signos y recta. |
| `t4_m_006` | Dos muelles en paralelo `k_1=100`, `k_2=150`. | `k_eq=250 N/m`; reparto para `x=0,04`: `4 N`, `6 N`. | Dos muelles paralelos. |
| `t4_m_007` | Dos muelles en serie con mismos valores. | `k_eq=60 N/m`; alargamientos con `F=6 N`: `0,06`, `0,04 m`. | Serie y tensión común. |
| `t4_m_008` | Bloque horizontal unido a muelle, posición `x=0,08`, `k=75`, sin rozamiento. | Fuerza `-6 N`; aceleración para `m=2`: `-3 m/s²`. | Bloque, origen y vector restaurador. |
| `t4_m_009` | Muelle vertical: rapidez instantánea no determina equilibrio. | Selección de DCL por encima/debajo del equilibrio; fuerzas numéricas. | Tres alturas del bloque. |
| `t4_m_010` | Calibrar dinamómetro con masas `0,1–0,5 kg`. | Función `x=(g/k)m`; obtener `k` desde pendiente. | Tabla y ajuste lineal. |
| `t4_m_011` | Muelle real deja de ser lineal tras `8 cm`. | Seleccionar rango de Hooke y punto que debe excluirse del ajuste. | Curva experimental con cambio de pendiente. |
| `t4_m_012` | Auditar confusión entre longitud `L` y deformación `x=L-L_0`. | `x` y fuerza correctas con `L_0=20 cm`, `L=27 cm`, `k=80`: `5,6 N`. | Dos medidas etiquetadas. |

### Bloque I - Experimento, integración y auditoría (10)

| ID | Actividad y datos | Clave estructurada | SVG/gráfica |
|---|---|---|---|
| `t4_i_001` | Identificar `μ_s` y `μ_k` desde gráfica fuerza-tiempo al tirar de una caja. | Pico/N y meseta/N; regímenes seleccionados. | `F(t)` con pico y meseta. |
| `t4_i_002` | La recta experimental `f_k(μ)` tiene pendiente `49 N`. | Función `f_k=mgμ`; masa `5,00 kg`. | Familia de rectas. |
| `t4_i_003` | Caja-muelle sobre mesa rugosa: hallar deformación mínima para iniciar movimiento. | `x_min=μ_smg/k`. | Muelle, bloque y umbral. |
| `t4_i_004` | Tras iniciarse el movimiento, un muelle `k=120 N/m` está deformado `0,08 m`; `m=1,5 kg`, `μ_k=0,20`. | `a=(kx-μ_kmg)/m=4,44 m/s²`. | Cambio estático/cinético en una misma escena. |
| `t4_i_005` | Vehículo toma curva y frena a la vez: límite de adherencia. | Composición vectorial; comprobar `sqrt(a_t²+a_r²)≤μ_sg`. | Círculo de adherencia. |
| `t4_i_006` | Seleccionar modelo para cuatro escenas: cinta, pared, plano, curva. | Clasificación cerrada de sentido y régimen. | Cuadrícula de escenas. |
| `t4_i_007` | Ajuste de muelle con intercepto no nulo por precarga. | `F=kx+F_0`; extraer `k` e `F_0`. | Dispersión con intercepto. |
| `t4_i_008` | Comparar trabajo posterior sin calcularlo aún: misma distancia, rozamientos distintos. | Orden cerrado de fuerzas y aceleraciones. | Dos superficies y barras de fuerza. |
| `t4_i_009` | Auditoría completa de curva peraltada con rozamiento mal orientado. | Elegir sentido, ecuaciones correctas y rango de velocidad. | DCL numerado y sección vial. |
| `t4_i_010` | Plano variable con `μ_s=0,30`, `μ_k=0,20`: predecir inicio y calcular al bajar para `20°`, `30°`, `45°`. | `θ_c=16,7°`; aceleraciones `1,51`, `3,20`, `5,54 m/s²`; seleccionar la curva creciente compatible. | Plano articulado y gráfica. |

## 4. Sistema visual

Se prevén **al menos 42 SVG**. Deben alternar DCL, diagramas de régimen, gráficas de umbral, secciones de curvas, montajes de muelles y datos experimentales. Los cambios estático/cinético se mostrarán con estados comparables; ninguna ilustración revelará el valor esperado.

## 5. Criterios de aceptación antes del JSON

1. Los 60 ejercicios distinguen explícitamente régimen, sistema y tendencia de movimiento.
2. Todo valor de rozamiento estático cumple `|f_s|≤μ_sN`; todos los límites se comprueban.
3. Los campos son verificables y los apartados abiertos se sustituyen por decisiones cerradas honestas.
4. Las soluciones incluyen cambio de régimen, signos, unidades y comprobación dimensional.
5. Cada diagrama aporta una decisión física y tiene alternativa textual completa.
6. No se añaden fuentes externas sin una fase editorial separada.
