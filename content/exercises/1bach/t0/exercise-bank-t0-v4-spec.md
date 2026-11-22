# Banco editorial T0 v4 — rediseño completo de ejercicios

**Curso:** 1.º de Bachillerato

**Tema:** T0 — Herramientas para empezar Física

**Estado:** especificación editorial cerrada para convertir a JSON
**Fecha:** 12 de septiembre de 2026

## 1. Objetivo de esta versión

Este documento sustituye el planteamiento del banco T0 v3. La versión anterior contiene 80 ejercicios, pero demasiados consisten en reconocer una definición o ejecutar una única operación evidente. Además, solo dedica dos ejercicios a medida, error e incertidumbre, aunque ese contenido ocupa un bloque completo de la lección.

La v4 mantiene **80 ejercicios**, pero los redistribuye de acuerdo con los cuatro bloques reales del tema:

| Bloque | IDs | Cantidad |
|---|---:|---:|
| Lenguaje físico, unidades y análisis dimensional | `t0_u_001`–`t0_u_016` | 16 |
| Vectores y elección de ejes | `t0_v_001`–`t0_v_024` | 24 |
| Medida, error, incertidumbre y cifras significativas | `t0_m_001`–`t0_m_020` | 20 |
| Funciones, gráficas, derivadas e integrales | `t0_c_001`–`t0_c_020` | 20 |
| **Total** |  | **80** |

Los IDs antiguos que no aparecen aquí deben quedar retirados del catálogo activo. No se deben reciclar para un contenido de otra familia. Si existen intentos históricos con esos IDs, se conservarán en la base de datos como históricos; no se borrarán ni se reasignarán.

## 2. Criterio general de dificultad

- No habrá ejercicios de dificultad 1 en el catálogo principal. La dificultad 1 puede reservarse en el futuro para un diagnóstico opcional.
- Dificultad 2: aplicación breve, pero con al menos dos decisiones u operaciones.
- Dificultad 3: combinación de conceptos, conversión de unidades o interpretación física.
- Dificultad 4: varios apartados conectados, ambigüedad de signos/ejes o comprobación crítica.
- Dificultad 5: problema integrador o respuesta gráfica/argumentada con más de una estrategia posible.
- La duración estimada debe ser realista. Ningún ejercicio enriquecido debe anunciar 4 minutos si exige dibujo, justificación y cálculo.

## 3. Contrato editorial común

Codex debe trasladar **literalmente** el contenido de este documento al esquema JSON vigente. Puede adaptar la estructura técnica, escapar HTML/TeX y crear los `response_fields`, pero no debe cambiar datos, redondeos, opciones, respuestas, pistas ni razonamientos.

Reglas comunes:

1. Las magnitudes numéricas se corrigen con la unidad indicada. La tolerancia que se da abajo es absoluta salvo que se diga lo contrario.
2. Cuando se piden cifras significativas, una respuesta numéricamente cercana pero con formato incompatible se marca como parcialmente correcta o se deja señalada para feedback; nunca se presenta silenciosamente como idéntica.
3. Los ángulos se dan en grados y se miden desde `+x` en sentido antihorario salvo indicación expresa.
4. Para texto corto se indican las formas aceptadas. Cualquier explicación libre adicional queda `pending_review`.
5. Las soluciones completas solo se muestran después de entregar. Las pistas se revelan progresivamente.
6. Los diagramas exactos se harán como SVG web-native. No usar PNG generados por IA ni gráficos de Matplotlib con grandes márgenes.
7. Cada ejercicio debe tener feedback específico para los errores enumerados; no reutilizar mensajes genéricos como «identifica el método».

---

# BLOQUE U — Lenguaje físico, unidades y análisis dimensional

## T0-U-001 — Rapidez media con conversión doble

- **ID:** `t0_u_001`
- **Dificultad / tiempo:** 2 / 7 min
- **Tipo:** `numeric_multi`
- **Enunciado:** «Una ciclista recorre 12,6 km en 18,0 min. a) Expresa la distancia y el tiempo en unidades SI. b) Calcula la rapidez media en m·s⁻¹. c) Escribe la dimensión física de la rapidez.»
- **Campos:** `distance_m = 12600` m (tol. 1 m); `time_s = 1080` s (tol. 0,5 s); `speed = 11.7` m·s⁻¹ (tol. 0,05; **3 cifras significativas**); `dimension = L T^-1` (aceptar `[L T^-1]`, `L·T^-1`).
- **Pista 1:** Convierte por separado kilómetros a metros y minutos a segundos.
- **Pista 2:** La rapidez media es distancia total dividida entre tiempo total.
- **Solución:** $12,6\,\mathrm{km}=12600\,\mathrm{m}$ y $18,0\,\mathrm{min}=1080\,\mathrm{s}$. Entonces $v=12600/1080=11,666\ldots\,\mathrm{m\,s^{-1}}$, que a 3 cifras significativas es $11,7\,\mathrm{m\,s^{-1}}$. Su dimensión es $LT^{-1}$.
- **Errores a detectar:** dividir antes de convertir; convertir min multiplicando por 60 dos veces; responder 11,666… sin el redondeo pedido; confundir unidad con dimensión.

## T0-U-002 — Densidad y cambio de sistema de unidades

- **ID:** `t0_u_002`
- **Dificultad / tiempo:** 3 / 8 min
- **Tipo:** `numeric_multi`
- **Enunciado:** «Una pieza de metal tiene una masa de 270 g y ocupa 100 cm³. a) Calcula su densidad en g·cm⁻³. b) Conviértela a kg·m⁻³. c) Entre aluminio (2700 kg·m⁻³) y hierro (7870 kg·m⁻³), indica con cuál es compatible.»
- **Campos:** `density_cgs = 2.70` g·cm⁻³ (tol. 0,005; 3 cifras); `density_si = 2700` kg·m⁻³ (tol. 5); `material = aluminium` (opciones `aluminium`, `iron`).
- **Pista 1:** En las unidades dadas, calcula primero $270/100$.
- **Pista 2:** $1\,\mathrm{g\,cm^{-3}}=1000\,\mathrm{kg\,m^{-3}}$.
- **Solución:** $\rho=270/100=2,70\,\mathrm{g\,cm^{-3}}=2700\,\mathrm{kg\,m^{-3}}$. Es compatible con el aluminio.
- **Errores a detectar:** convertir solo gramos pero no cm³; usar $1\,\mathrm{cm^3}=10^{-2}\,\mathrm{m^3}$; elegir por cercanía sin mostrar la conversión.

## T0-U-003 — Constante de una ley de acumulación

- **ID:** `t0_u_003`
- **Dificultad / tiempo:** 3 / 8 min
- **Tipo:** `numeric_multi`
- **Enunciado:** «Una superficie de 0,800 m² recibe 2,40 kJ de energía en 5,00 min y se modela mediante $Q=kAt$. a) Deduce la unidad SI de $k$. b) Calcula $k$. c) Predice la energía recibida por 1,20 m² durante 2,00 min si $k$ no cambia.»
- **Campos:** `unit_k = J m^-2 s^-1`; `k = 10.0` J·m⁻²·s⁻¹ (tol. 0,05; 3 cifras); `predicted_energy = 1440` J (tol. 2; 3 cifras, aceptar `1.44 kJ`).
- **Pista 1:** Despeja $k=Q/(At)$ y convierte kJ y min antes de sustituir.
- **Pista 2:** Para la predicción usa de nuevo $Q=kAt$.
- **Solución:** $[k]=\mathrm{J\,m^{-2}\,s^{-1}}$. Con $Q=2400$ J y $t=300$ s, $k=2400/(0,80\cdot300)=10,0$. Después, $Q=10,0\cdot1,20\cdot120=1440$ J.
- **Errores a detectar:** dejar kJ/min; invertir la fórmula; aplicar el cambio de área o tiempo dos veces.

## T0-U-004 — Constante elástica desde energía

- **ID:** `t0_u_004`
- **Dificultad / tiempo:** 3 / 9 min
- **Tipo:** `numeric_multi`
- **Enunciado:** «La energía almacenada por un muelle se modela como $E=\tfrac12kx^2$. Al deformarlo 6,00 cm almacena 0,360 J. a) Deduce la unidad SI de $k$. b) Calcula $k$. c) Calcula la energía para una deformación de 9,00 cm.»
- **Campos:** `unit_k = N m^-1` (aceptar `J m^-2`); `k = 200` N·m⁻¹ (tol. 1; 3 cifras); `energy_9cm = 0.810` J (tol. 0,002; 3 cifras).
- **Pista 1:** Antes de calcular, convierte centímetros a metros.
- **Pista 2:** $k=2E/x^2$; la energía crece con el cuadrado de la deformación.
- **Solución:** $[k]=\mathrm{J\,m^{-2}}=\mathrm{N\,m^{-1}}$. $k=2(0,360)/(0,060)^2=200\,\mathrm{N\,m^{-1}}$. Para $x=0,090$ m, $E=\tfrac12(200)(0,090)^2=0,810$ J.
- **Errores a detectar:** omitir el factor $1/2$; usar 6 y 9 como metros; suponer que la energía crece linealmente con $x$.

## T0-U-005 — Elegir una ley dimensionalmente posible

- **ID:** `t0_u_005`
- **Dificultad / tiempo:** 3 / 8 min
- **Tipo:** `single_choice_plus_text`
- **Enunciado:** «Se propone modelar el periodo $T$ de un péndulo usando su longitud $L$ y la aceleración gravitatoria $g$. ¿Cuál de estas expresiones puede ser correcta por dimensiones? A) $T=2\pi L/g$; B) $T=2\pi\sqrt{L/g}$; C) $T=2\pi\sqrt{g/L}$; D) $T=2\pi Lg$. Justifica dimensionalmente y calcula $T$ para $L=0,900$ m y $g=9,81$ m·s⁻².»
- **Campos:** `choice = B`; `justification` texto corto obligatorio; `period = 1.90` s (tol. 0,01; 3 cifras).
- **Pista 1:** $[g]=LT^{-2}$; calcula la dimensión de $L/g$.
- **Pista 2:** $L/g$ tiene dimensión $T^2$.
- **Solución:** Solo B produce tiempo: $[\sqrt{L/g}]=\sqrt{L/(LT^{-2})}=T$. $T=2\pi\sqrt{0,900/9,81}=1,90$ s.
- **Errores a detectar:** elegir por recordar la fórmula sin justificar; tratar $2\pi$ como dimensional; invertir $L/g$.

## T0-U-006 — Parámetros de un decaimiento exponencial

- **ID:** `t0_u_006`
- **Dificultad / tiempo:** 4 / 10 min
- **Tipo:** `numeric_multi`
- **Enunciado:** «Una amplitud espacial sigue $y(x)=Ae^{-\lambda x}$. Se mide $y(0)=12,0$ cm y $y(0,800\,\mathrm{m})=4,40$ cm. a) Deduce las unidades de $A$ y $\lambda$. b) Obtén sus valores. c) Explica por qué el exponente no puede tener unidades.»
- **Campos:** `unit_A = cm`; `unit_lambda = m^-1`; `A = 12.0` cm (tol. 0,01); `lambda = 1.25` m⁻¹ (tol. 0,01; 3 cifras); `exponent_reason` texto obligatorio.
- **Pista 1:** En $x=0$, el factor exponencial vale 1.
- **Pista 2:** Divide $4,40/12,0=e^{-0,80\lambda}$ y aplica logaritmos.
- **Solución:** $A=12,0$ cm. El exponente $\lambda x$ debe ser adimensional, así que $[\lambda]=\mathrm{m^{-1}}$. $\lambda=-\ln(4,40/12,0)/0,80=1,25\,\mathrm{m^{-1}}$.
- **Errores a detectar:** asignar a $A$ unidades SI forzosamente aunque $y$ se da en cm; olvidar el signo menos; escribir $\lambda$ en m.

## T0-U-007 — Fase inicial y periodo

- **ID:** `t0_u_007`
- **Dificultad / tiempo:** 4 / 11 min
- **Tipo:** `numeric_multi`
- **Enunciado:** «Una oscilación se describe por $y(t)=4,00\sin(3,00t+\phi)$ cm, con $t$ en segundos. En $t=0$, $y=2,00$ cm y la partícula se mueve en el sentido positivo de $y$. a) Indica las unidades de $3,00$ y de $\phi$. b) Determina $\phi$ en el intervalo $[0,2\pi)$. c) Calcula el periodo.»
- **Campos:** `unit_omega = s^-1` (aceptar `rad s^-1`); `unit_phi = dimensionless` (aceptar `rad`); `phi = 0.524` rad (tol. 0,005; aceptar `pi/6`); `period = 2.09` s (tol. 0,01).
- **Pista 1:** De $2,0=4,0\sin\phi$ salen dos ángulos; usa el signo de la velocidad para escoger.
- **Pista 2:** $dy/dt=12,0\cos(3,0t+\phi)$ cm·s⁻¹ debe ser positivo en $t=0$.
- **Solución:** $3,0$ tiene unidad s⁻¹ y $\phi$ es adimensional (se expresa en rad). $\sin\phi=0,5$ da $\phi=\pi/6$ o $5\pi/6$, pero solo $\pi/6$ tiene $\cos\phi>0$. $T=2\pi/3,0=2,09$ s.
- **Errores a detectar:** aceptar ambas fases ignorando el sentido; dar grados sin indicarlo; calcular $T=1/3$.

## T0-U-008 — Exponentes desconocidos por análisis dimensional

- **ID:** `t0_u_008`
- **Dificultad / tiempo:** 4 / 10 min
- **Tipo:** `numeric_multi`
- **Enunciado:** «Sin conocer la fórmula del péndulo, se supone $T=C L^a g^b$, donde $C$ es adimensional. Determina $a$ y $b$ imponiendo compatibilidad dimensional. Después indica cómo cambia $T$ si la longitud se cuadruplica.»
- **Campos:** `a = 0.5` (tol. 0.001); `b = -0.5` (tol. 0.001); `factor = 2.0` (tol. 0.001).
- **Pista 1:** Sustituye $[T]=T$, $[L]=L$ y $[g]=LT^{-2}$.
- **Pista 2:** Iguala por separado los exponentes de $L$ y de $T$.
- **Solución:** $T=L^{a+b}T^{-2b}$. Por tanto $a+b=0$ y $-2b=1$, de donde $b=-1/2$ y $a=1/2$. Como $T\propto\sqrt L$, al cuadruplicar $L$ el periodo se duplica.
- **Errores a detectar:** igualar los exponentes sin separar magnitudes; obtener $b=+1/2$; afirmar que el periodo se cuadruplica.

## T0-U-009 — Constante gravitatoria en unidades básicas

- **ID:** `t0_u_009`
- **Dificultad / tiempo:** 3 / 9 min
- **Tipo:** `short_text_plus_numeric`
- **Enunciado:** «La ley $F=Gm_1m_2/r^2$ usa $F$ en N, masas en kg y distancia en m. a) Deduce $[G]$ usando N. b) Exprésala solo con kg, m y s. c) Si ambas masas se duplican y la distancia se triplica, ¿por qué factor cambia la fuerza?»
- **Campos:** `unit_derived = N m^2 kg^-2`; `unit_base = m^3 kg^-1 s^-2`; `force_factor = 4/9` (aceptar 0,444; tol. 0,002).
- **Pista 1:** $G=Fr^2/(m_1m_2)$ y $1\,\mathrm N=1\,\mathrm{kg\,m\,s^{-2}}$.
- **Pista 2:** En el cociente de fuerzas, $G$ se cancela.
- **Solución:** $[G]=\mathrm{N\,m^2\,kg^{-2}}=\mathrm{m^3\,kg^{-1}\,s^{-2}}$. El numerador aumenta por 4 y $r^2$ por 9, de modo que $F'/F=4/9$.
- **Errores a detectar:** conservar kg² en la unidad básica; cambiar $G$ al modificar el sistema; olvidar que la distancia está al cuadrado.

## T0-U-010 — Exponente radial en una ley de Coulomb

- **ID:** `t0_u_010`
- **Dificultad / tiempo:** 4 / 9 min
- **Tipo:** `numeric_multi`
- **Enunciado:** «Una ley se escribe $F=kq_1q_2/r^n$. La constante tiene unidades N·m²·C⁻². a) Determina $n$ por dimensiones. b) Si la distancia pasa de $r$ a $3r$ sin cambiar las cargas, calcula $F'/F$. c) Explica por qué el análisis dimensional fija el exponente, pero no el valor numérico de $k$.»
- **Campos:** `n = 2`; `ratio = 0.1111` (tol. 0,0005; aceptar `1/9`); `explanation` texto obligatorio.
- **Pista 1:** Las unidades de $kq_1q_2/r^n$ deben reducirse a N.
- **Pista 2:** Sustituye $r'=3r$ en la misma ley.
- **Solución:** Para cancelar m² debe cumplirse $n=2$. Así, $F'/F=(r/3r)^2=1/9$. Las dimensiones no contienen información sobre factores adimensionales ni sobre el valor experimental de una constante.
- **Errores a detectar:** deducir $n=1$; decir que la fuerza se divide entre 3; afirmar que las unidades determinan el valor de $k$.

## T0-U-011 — Resistividad de un hilo real

- **ID:** `t0_u_011`
- **Dificultad / tiempo:** 4 / 12 min
- **Tipo:** `numeric_multi`
- **Enunciado:** «Un hilo cilíndrico de longitud 2,40 m, diámetro 0,60 mm y resistencia 0,85 Ω cumple $R=\rho L/A$. a) Deduce la unidad SI de $\rho$. b) Calcula el área de la sección. c) Obtén la resistividad con 2 cifras significativas.»
- **Campos:** `unit_rho = ohm m`; `area = 2.83e-7` m² (tol. `0.01e-7`; 3 cifras); `rho = 1.0e-7` Ω·m (tol. `0.03e-7`; **2 cifras significativas**, mostrar `1,0×10^-7`).
- **Pista 1:** El radio es la mitad del diámetro y debe convertirse de mm a m.
- **Pista 2:** $A=\pi r^2$ y $\rho=RA/L$.
- **Solución:** $[\rho]=\Omega\,\mathrm m$. $r=3,0\times10^{-4}$ m y $A=\pi r^2=2,83\times10^{-7}$ m². $\rho=0,85A/2,40=1,001\times10^{-7}\,\Omega\,\mathrm m\approx1,0\times10^{-7}\,\Omega\,\mathrm m$.
- **Errores a detectar:** usar el diámetro como radio; convertir mm a m con $10^{-2}$; redondear a `1×10^-7` perdiendo las 2 cifras pedidas.

## T0-U-012 — Ley cúbica y sensibilidad a la velocidad

- **ID:** `t0_u_012`
- **Dificultad / tiempo:** 3 / 9 min
- **Tipo:** `numeric_multi`
- **Enunciado:** «La potencia necesaria para vencer cierto arrastre se aproxima por $P=kAv^3$. Para $P=1,20$ kW, $A=0,500$ m² y $v=10,0$ m·s⁻¹: a) deduce la unidad de $k$; b) calcula $k$; c) determina por qué factor cambia $P$ si $v$ se duplica.»
- **Campos:** `unit_k = kg m^-3`; `k = 2.40` kg·m⁻³ (tol. 0,01; 3 cifras); `power_factor = 8`.
- **Pista 1:** Usa $1\,\mathrm W=1\,\mathrm{kg\,m^2\,s^{-3}}$.
- **Pista 2:** En una proporcionalidad cúbica, sustituir $v$ por $2v$ introduce $2^3$.
- **Solución:** $[k]=\mathrm{W}/[\mathrm{m^2(m\,s^{-1})^3}]=\mathrm{kg\,m^{-3}}$. $k=1200/(0,500\cdot10,0^3)=2,40\,\mathrm{kg\,m^{-3}}$. Al duplicar $v$, la potencia se multiplica por 8.
- **Errores a detectar:** no convertir kW; tratar la ley como lineal; perder potencias de m o s al reducir unidades.

## T0-U-013 — Coherencia dimensional de van der Waals

- **ID:** `t0_u_013`
- **Dificultad / tiempo:** 5 / 14 min
- **Tipo:** `short_text_multi`
- **Enunciado:** «En $(P+a n^2/V^2)(V-nb)=nRT$, $P$ está en Pa, $V$ en m³, $n$ en mol y $T$ en K. a) Deduce las unidades de $a$, $b$ y $R$. b) Explica qué dos sumas/restas obligan a esas unidades. c) Comprueba que ambos miembros tienen unidad de energía.»
- **Campos:** `unit_a = Pa m^6 mol^-2`; `unit_b = m^3 mol^-1`; `unit_R = J mol^-1 K^-1`; `compatibility_explanation` texto obligatorio.
- **Pista 1:** En una suma, cada término debe tener la misma dimensión: $P$ y $an^2/V^2$; $V$ y $nb$.
- **Pista 2:** $\mathrm{Pa\,m^3}=\mathrm J$.
- **Solución:** $[a]=\mathrm{Pa\,m^6\,mol^{-2}}$ para que $an^2/V^2$ sea presión. $[b]=\mathrm{m^3\,mol^{-1}}$ para que $nb$ sea volumen. El primer paréntesis es presión y el segundo volumen, por lo que su producto es Pa·m³ = J. Entonces $[R]=\mathrm{J\,mol^{-1}\,K^{-1}}$.
- **Errores a detectar:** multiplicar unidades dentro de una suma; asignar a $b$ unidad de volumen sin dividir por mol; no comprobar el miembro derecho.

## T0-U-014 — Bernoulli: unidades y orden de magnitud

- **ID:** `t0_u_014`
- **Dificultad / tiempo:** 4 / 12 min
- **Tipo:** `numeric_multi`
- **Enunciado:** «En un punto de una corriente de agua, $P=120,0$ kPa, $\rho=1000$ kg·m⁻³, $h=2,50$ m y $v=3,00$ m·s⁻¹. Con $g=9,81$ m·s⁻², usa $C=P+\rho gh+\tfrac12\rho v^2$. a) Demuestra que los tres términos tienen unidades de presión. b) Calcula cada contribución y $C$. c) Indica cuál domina numéricamente.»
- **Campos:** `pressure_term = 120000` Pa (tol. 50); `height_term = 24525` Pa (tol. 30); `kinetic_term = 4500` Pa (tol. 10); `C = 149025` Pa (tol. 100; 3 cifras); `dominant = pressure`.
- **Pista 1:** Convierte kPa a Pa y reduce $\rho gh$ a unidades básicas.
- **Pista 2:** Compara los tres números antes de sumarlos.
- **Solución:** $P=120000$ Pa, $\rho gh=24525\approx24500$ Pa y $\tfrac12\rho v^2=4500$ Pa. Los dos últimos reducen a kg·m⁻¹·s⁻² = Pa. $C=149025$ Pa $\approx$ 149 kPa. Domina el término de presión estática.
- **Errores a detectar:** sumar 120 como si fueran Pa; omitir $1/2$; afirmar compatibilidad sin reducir unidades.

## T0-U-015 — Oscilación amortiguada y tiempo característico

- **ID:** `t0_u_015`
- **Dificultad / tiempo:** 4 / 11 min
- **Tipo:** `numeric_multi`
- **Enunciado:** «$x(t)=A e^{-0,350t}\cos(4,20t+0,400)$ describe una posición en metros con $t$ en segundos. a) Da las unidades de los números 0,350; 4,20 y 0,400. b) Calcula el tiempo en que la amplitud se reduce a la mitad. c) Calcula el periodo de la oscilación.»
- **Campos:** `unit_gamma = s^-1`; `unit_omega = s^-1` (aceptar rad·s⁻¹); `unit_phase = dimensionless` (aceptar rad); `half_time = 1.98` s (tol. 0,01); `period = 1.50` s (tol. 0,01).
- **Pista 1:** Para la semiamplitud resuelve $e^{-0,35t}=1/2$.
- **Pista 2:** El periodo depende de 4,2 mediante $T=2\pi/\omega$.
- **Solución:** 0,35 y 4,2 tienen unidad s⁻¹; 0,40 es una fase adimensional. $t_{1/2}=\ln2/0,35=1,98$ s. $T=2\pi/4,2=1,50$ s.
- **Errores a detectar:** confundir periodo con tiempo de semiamplitud; asignar segundos a la fase; olvidar el logaritmo.

## T0-U-016 — Suma bajo una raíz

- **ID:** `t0_u_016`
- **Dificultad / tiempo:** 5 / 13 min
- **Tipo:** `numeric_multi`
- **Enunciado:** «Una magnitud se define como $S=\sqrt{\alpha x^2+\beta y}/t$, con $S$ en m·s⁻¹, $x$ e $y$ en m y $t$ en s. a) Deduce las unidades de $\alpha$ y $\beta$. b) Justifica por qué los dos términos dentro de la raíz deben tener la misma dimensión. c) Calcula $S$ para $\alpha=0,50$, $\beta=4,0$ m, $x=3,0$ m, $y=2,0$ m y $t=2,0$ s.»
- **Campos:** `unit_alpha = dimensionless`; `unit_beta = m`; `calculator_S = 1.768` m·s⁻¹ (tol. 0,002); `reported_S = 1.8` m·s⁻¹ (tol. 0,05; **2 cifras significativas**); `sum_reason` texto obligatorio.
- **Pista 1:** Para que $S$ sea m·s⁻¹, el contenido de la raíz debe ser m².
- **Pista 2:** Calcula $0,50(3,0)^2+(4,0)(2,0)$ antes de extraer la raíz.
- **Solución:** $\alpha x^2$ exige $[\alpha]=1$ y $\beta y$ exige $[\beta]=\mathrm m$; ambos términos son m² y se pueden sumar. El valor de calculadora es $S=\sqrt{4,5+8,0}/2,0=1,768\ldots\,\mathrm{m\,s^{-1}}$ y se informa $1,8\,\mathrm{m\,s^{-1}}$ por los datos de 2 cifras significativas.
- **Errores a detectar:** sumar términos de dimensiones distintas; sacar la raíz por separado de una suma; olvidar dividir entre $t$.

---

# BLOQUE V — Vectores y elección de ejes

## T0-V-001 — Escalar y vector en un trayecto

- **ID:** `t0_v_001`; **dificultad / tiempo:** 2 / 7 min; **tipo:** `single_choice_multi`.
- **Enunciado:** «Una alumna camina 300 m al este y después 400 m al norte en 10 min. a) Clasifica como escalares o vectoriales: tiempo, distancia recorrida, rapidez media, desplazamiento y velocidad media. b) Calcula la distancia y el módulo del desplazamiento. c) Explica por qué no son intercambiables.»
- **Respuesta:** escalares = tiempo, distancia, rapidez; vectoriales = desplazamiento, velocidad. `distance = 700 m`; `displacement_magnitude = 500 m` (tol. 0,5). Texto justificativo obligatorio.
- **Pistas:** la distancia suma el camino; el desplazamiento une origen y final. Usa Pitágoras para el módulo.
- **Solución:** recorre 700 m, pero se desplaza $(300,400)$ m, cuyo módulo es 500 m. La distancia no tiene dirección; el desplazamiento sí.
- **Errores:** clasificar rapidez como vector; responder 700 m como desplazamiento; definir vector solo como «algo con flecha» sin referirse a módulo, dirección y sentido.

## T0-V-002 — Módulo, unitario y dirección

- **ID:** `t0_v_002`; **dificultad / tiempo:** 3 / 9 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Para $\vec a=(4,-3)$ m: a) calcula su módulo; b) construye el vector unitario de su dirección; c) da su ángulo en $[0,360^\circ)$; d) comprueba que el unitario tiene módulo 1.»
- **Campos:** `magnitude = 5.00 m` (tol. 0,01); `ux = 0.800`, `uy = -0.600` (tol. 0,002); `angle = 323.1°` (tol. 0,2); `unit_check = 1.000` (tol. 0,002).
- **Pistas:** divide cada componente por el módulo; el vector está en el cuarto cuadrante.
- **Solución:** $|a|=5$, $\hat a=(0,8,-0,6)$ y $\theta=360^\circ-\arctan(3/4)=323,1^\circ$.
- **Errores:** dar $-36,9^\circ$ sin ajustarse al intervalo; dividir por una componente; perder el signo de $y$.

## T0-V-003 — Fuerza con dirección prescrita

- **ID:** `t0_v_003`; **dificultad / tiempo:** 3 / 8 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Construye una fuerza de 15,0 N paralela y del mismo sentido que $(6,8)$. Da sus componentes, comprueba el módulo y escribe la fuerza opuesta.»
- **Campos:** `Fx = 9.00 N`, `Fy = 12.0 N` (tol. 0,02); `magnitude = 15.0 N` (tol. 0,02); `opposite_x = -9.00 N`, `opposite_y = -12.0 N`.
- **Pistas:** primero normaliza $(6,8)$; el opuesto cambia ambos signos, no intercambia componentes.
- **Solución:** el unitario es $(0,6,0,8)$; por tanto $\vec F=(9,12)$ N, $|F|=15$ N y $-\vec F=(-9,-12)$ N.
- **Errores:** multiplicar directamente $(6,8)$ por 15; construir un perpendicular; cambiar solo un signo.

## T0-V-004 — Tres representaciones del mismo vector

- **ID:** `t0_v_004`; **dificultad / tiempo:** 3 / 9 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Un desplazamiento tiene módulo 20,0 m y dirección $150^\circ$. a) Escríbelo en componentes cartesianas. b) Escríbelo con $\vec i,\vec j$. c) Indica su cuadrante y reconstruye módulo y ángulo desde las componentes.»
- **Campos:** `x = -17.3 m`, `y = 10.0 m` (tol. 0,05; 3 cifras); `quadrant = II`; reconstrucción `magnitude = 20.0 m`, `angle = 150°`.
- **Pistas:** $x=R\cos\theta$, $y=R\sin\theta$; comprueba los signos antes de calcular.
- **Solución:** $\vec R=(-17,3\,\vec i+10,0\,\vec j)$ m. Está en el segundo cuadrante y las componentes recuperan 20,0 m y $150^\circ$.
- **Errores:** usar seno para $x$ sin justificar otra convención; devolver ambas componentes positivas; confundir vector con su módulo.

## T0-V-005 — Componente desconocida y dos direcciones posibles

- **ID:** `t0_v_005`; **dificultad / tiempo:** 4 / 11 min; **tipo:** `numeric_multi`.
- **Enunciado:** «$\vec u=(a,12)$ tiene módulo 13. a) Calcula todos los valores posibles de $a$. b) Da el ángulo de cada vector desde $+x$. c) Explica por qué el módulo no determina una dirección única.»
- **Campos:** `a_positive = 5`, `a_negative = -5`; `angle_positive = 67.4°`, `angle_negative = 112.6°` (tol. 0,2); explicación obligatoria.
- **Pistas:** $a^2+12^2=13^2$; al extraer una raíz aparecen dos signos.
- **Solución:** $a^2=25$, luego $a=\pm5$. Los vectores están en los cuadrantes I y II, con $67,4^\circ$ y $112,6^\circ$.
- **Errores:** quedarse solo con $a=5$; usar el mismo ángulo para ambos; resolver $a+12=13$.

## T0-V-006 — Relaciones entre pares de vectores

- **ID:** `t0_v_006`; **dificultad / tiempo:** 3 / 9 min; **tipo:** `short_text_multi`.
- **Enunciado:** «Clasifica y justifica: A=$(2,-1)$ y B=$(2,-1)$; C=$(3,0)$ y D=$(-6,0)$; E=$(1,2)$ y F=$(2,-1)$. Para cada par indica si son iguales, paralelos, opuestos o perpendiculares. Usa proporcionalidad o producto escalar, no solo el dibujo.»
- **Respuesta:** A–B iguales; C–D paralelos de sentido opuesto y $D=-2C$ (no son vectores opuestos en sentido estricto si se reserva “opuesto” para $-C$); E–F perpendiculares porque $E\cdot F=0$.
- **Pistas:** igualdad exige mismas componentes; paralelismo permite un factor; perpendicularidad se prueba con producto escalar cero.
- **Errores:** llamar iguales a C y D; afirmar que longitudes distintas impiden paralelismo; decidir perpendicularidad por apariencia.

## T0-V-007 — Suma, resta y significado geométrico

- **ID:** `t0_v_007`; **dificultad / tiempo:** 3 / 10 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Sean $A=(5,-2)$ m y $B=(-1,7)$ m. a) Calcula $A+B$ y $A-B$. b) Obtén módulo y ángulo de $A+B$. c) Interpreta $A-B$ como el vector que debe sumarse a B para llegar a A.»
- **Campos:** suma `(4,5) m`; resta `(6,-9) m`; `sum_magnitude = 6.40 m` (tol. 0,02); `sum_angle = 51.3°` (tol. 0,2).
- **Pistas:** opera componente a componente; usa `atan2(y,x)` o razona el cuadrante.
- **Solución:** $A+B=(4,5)$ m, $A-B=(6,-9)$ m, $|A+B|=\sqrt{41}=6,40$ m y $\theta=51,3^\circ$.
- **Errores:** sumar módulos; calcular $B-A$; obtener un ángulo del cuadrante incorrecto.

## T0-V-008 — Combinación lineal y vector equilibrante

- **ID:** `t0_v_008`; **dificultad / tiempo:** 4 / 10 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Con $A=(1,-4)$ N y $B=(-2,3)$ N: a) calcula $R=2A-3B$; b) encuentra $C$ para que $2A-3B+C=0$; c) verifica la igualdad por componentes.»
- **Campos:** `Rx = 8 N`, `Ry = -17 N`; `Cx = -8 N`, `Cy = 17 N`; verificación escrita breve.
- **Pistas:** distribuye primero los escalares; el equilibrante es $-R$.
- **Solución:** $2A=(2,-8)$ y $3B=(-6,9)$, así que $R=(8,-17)$ N. Debe ser $C=(-8,17)$ N.
- **Errores:** interpretar $-3B$ como $(-3,-3)+B$; olvidar cambiar ambos signos en $C$; sumar módulos.

## T0-V-009 — Tres desplazamientos y dirección final

- **ID:** `t0_v_009`; **dificultad / tiempo:** 3 / 10 min; **tipo:** `numeric_multi`.
- **Enunciado:** «$A=(2,1)$ cm, $B=(-3,4)$ cm y $C=(5,-2)$ cm. Calcula $R=A+2B-C$, su módulo y su dirección desde $+x$. Sitúa el resultado en el cuadrante correcto antes de usar la calculadora.»
- **Campos:** `Rx = -9 cm`, `Ry = 11 cm`; `magnitude = 14.2 cm` (tol. 0,05); `angle = 129.3°` (tol. 0,2); `quadrant = II`.
- **Pistas:** calcula componentes antes del módulo; $x<0$, $y>0$.
- **Solución:** $R=(-9,11)$ cm, $|R|=\sqrt{202}=14,2$ cm y $\theta=129,3^\circ$.
- **Errores:** restar solo el módulo de C; aceptar $-50,7^\circ$ sin corregir el cuadrante.

## T0-V-010 — Combinación en tres dimensiones

- **ID:** `t0_v_010`; **dificultad / tiempo:** 4 / 11 min; **tipo:** `numeric_multi`.
- **Enunciado:** «$A=(1,0,3)$, $B=(-2,4,1)$ y $C=(0,-1,5)$. a) Calcula $R=A-2B+C$. b) Obtén $|R|$. c) Calcula el coseno director respecto a $+z$, $R_z/|R|$.»
- **Campos:** `Rx = 5`, `Ry = -9`, `Rz = 6`; `magnitude = 11.92` (tol. 0,02); `cos_z = 0.503` (tol. 0,003).
- **Pistas:** conserva el orden x-y-z; el coseno director no es un ángulo.
- **Solución:** $R=(5,-9,6)$, $|R|=\sqrt{142}=11,92$ y $R_z/|R|=0,503$.
- **Errores:** perder el signo al calcular $-2B$; aplicar Pitágoras solo a dos componentes; dar grados en el campo del coseno.

## T0-V-011 — Ecuación vectorial con comprobación

- **ID:** `t0_v_011`; **dificultad / tiempo:** 3 / 9 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Resuelve $2X+A=B$ para $A=(4,-6)$ y $B=(-2,8)$. Después sustituye tu resultado en la ecuación y calcula el módulo de X.»
- **Campos:** `Xx = -3`, `Xy = 7`; `magnitude = 7.62` (tol. 0,02); comprobación `2X+A=(-2,8)`.
- **Pistas:** despeja simbólicamente $X=(B-A)/2$ antes de operar.
- **Solución:** $B-A=(-6,14)$, por tanto $X=(-3,7)$ y $|X|=\sqrt{58}=7,62$. La sustitución recupera B.
- **Errores:** usar $(A-B)/2$; dividir solo una componente; no comprobar.

## T0-V-012 — Construcción punta-cola

- **ID:** `t0_v_012`; **dificultad / tiempo:** 4 / 13 min; **tipo:** `written_upload_plus_numeric`.
- **Enunciado:** «Dibuja a escala $A=(3,1)$ y $B=(1,4)$. Construye por punta-cola $A+B$ y $A-B$, y comprueba ambos por componentes. El dibujo debe distinguir el vector trasladado de su posición original.»
- **Campos:** archivo/dibujo obligatorio `pending_review`; suma `(4,5)`; resta `(2,-3)`.
- **Pistas:** para $A-B$ usa $A+(-B)$; trasladar un vector no cambia sus componentes.
- **Solución:** $A+B=(4,5)$ y $A-B=(2,-3)$. El SVG de solución mostrará ambas construcciones en paneles separados.
- **Activo SVG obligatorio:** dos paneles con `viewBox` ajustado; ejes finos; A azul, B verde, resultado coral; cabezas de flecha de 8–10 px; etiquetas sin solaparse; sin el enorme espacio vacío ni las flechas negras de la versión anterior.
- **Errores:** dibujar B desde el origen en vez de desde la punta de A; usar B en lugar de $-B$ en la resta; evaluar solo estética sin comprobar componentes.

## T0-V-013 — Componentes y proyección horizontal

- **ID:** `t0_v_013`; **dificultad / tiempo:** 3 / 9 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Una fuerza de 10,0 N forma $30,0^\circ$ sobre $+x$. a) Calcula sus componentes. b) Calcula qué fracción de su módulo representa la componente horizontal. c) Reconstruye el módulo desde las componentes.»
- **Campos:** `Fx = 8.66 N`, `Fy = 5.00 N` (tol. 0,02; 3 cifras); `horizontal_fraction = 0.866` (tol. 0,002); `reconstructed = 10.0 N`.
- **Pistas:** coseno acompaña al cateto adyacente al ángulo; la fracción es $F_x/F$.
- **Solución:** $(F_x,F_y)=(10\cos30^\circ,10\sin30^\circ)=(8,66,5,00)$ N; $F_x/F=0,866$ y Pitágoras devuelve 10,0 N.
- **Errores:** intercambiar seno y coseno; dar porcentajes sin aclararlo; redondear tan pronto que falle la comprobación.

## T0-V-014 — Dos cuadrantes y una resultante

- **ID:** `t0_v_014`; **dificultad / tiempo:** 4 / 12 min; **tipo:** `numeric_multi`.
- **Enunciado:** «$A$ tiene módulo 12,0 y ángulo $210^\circ$; $B$ tiene módulo 8,00 y ángulo $315^\circ$. a) Calcula sus componentes. b) Calcula $R=A+B$. c) Da módulo y dirección de R.»
- **Campos:** `Ax=-10.39`, `Ay=-6.00`, `Bx=5.66`, `By=-5.66`; `Rx=-4.74`, `Ry=-11.66` (tol. 0,03); `Rmag=12.58` (tol. 0,03); `Rangle=247.9°` (tol. 0,3).
- **Pistas:** predice signos por cuadrante; R queda en el tercer cuadrante.
- **Solución:** $A=(-10,39,-6,00)$, $B=(5,66,-5,66)$ y $R=(-4,74,-11,66)$. $|R|=12,58$ y $\theta=247,9^\circ$.
- **Errores:** introducir grados como radianes; ignorar signos; usar el ángulo principal de la arctangente sin cuadrante.

## T0-V-015 — Ángulo medido desde el eje y

- **ID:** `t0_v_015`; **dificultad / tiempo:** 3 / 9 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Una fuerza de 50,0 N forma $40,0^\circ$ con $+y$ hacia $+x$. a) Haz un croquis mínimo. b) Calcula sus componentes. c) Expresa el ángulo equivalente medido desde $+x$.»
- **Campos:** dibujo opcional; `Fx=32.1 N`, `Fy=38.3 N` (tol. 0,1; 3 cifras); `angle_from_x=50.0°`.
- **Pistas:** el ángulo con $+x$ es complementario; respecto al ángulo dado, $F_y$ es la componente adyacente.
- **Solución:** $\theta_x=90^\circ-40^\circ=50^\circ$. $F_x=50\sin40^\circ=32,1$ N y $F_y=50\cos40^\circ=38,3$ N.
- **Errores:** tratar los 40° como medidos desde x; intercambiar componentes; poner un signo negativo sin razón.

## T0-V-016 — La ambigüedad de la arctangente

- **ID:** `t0_v_016`; **dificultad / tiempo:** 4 / 10 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Un vector tiene componentes $(-6,-8)$. Una calculadora muestra $\arctan(y/x)=53,1^\circ$. a) Calcula el módulo. b) Explica por qué 53,1° no es la dirección del vector. c) Da el ángulo correcto en $[0,360^\circ)$ y otro ángulo equivalente.»
- **Campos:** `magnitude=10.0`; `angle=233.1°` (tol. 0,2); `equivalent=-126.9°` (tol. 0,2); explicación obligatoria.
- **Pistas:** ambas componentes son negativas; usa `atan2` o suma 180°.
- **Solución:** el vector está en el tercer cuadrante. $|v|=10$ y la dirección es $53,1^\circ+180^\circ=233,1^\circ$, equivalente a $-126,9^\circ$.
- **Errores:** aceptar 53,1°; sumar 360° al ángulo agudo; creer que ángulos negativos son siempre inválidos.

## T0-V-017 — Cambio a ejes girados

- **ID:** `t0_v_017`; **dificultad / tiempo:** 5 / 14 min; **tipo:** `written_upload_plus_numeric`.
- **Enunciado:** «El vector $A=(10,0)$ N se describe en unos ejes $x',y'$ girados $30^\circ$ antihorario respecto a $x,y$. a) Dibuja ambos sistemas. b) Calcula $A_{x'}$ y $A_{y'}$. c) Reconstruye A en los ejes originales y explica el signo de $A_{y'}$.»
- **Campos:** dibujo `pending_review`; `Ax_prime=8.66 N`, `Ay_prime=-5.00 N` (tol. 0,02); reconstrucción escrita.
- **Pistas:** el vector queda 30° por debajo de $+x'$; cambiar ejes no cambia el vector físico.
- **Solución:** $A_{x'}=10\cos30^\circ=8,66$ N y $A_{y'}=-10\sin30^\circ=-5,00$ N. Al proyectar de vuelta se obtiene $(10,0)$ N.
- **Activo SVG obligatorio:** ejes originales grises, ejes girados discontinuos azules, arco de 30°, vector coral; etiquetas fuera de las flechas.
- **Errores:** girar el vector junto con los ejes; poner $A_{y'}>0$; confundir transformación activa y cambio de base.

## T0-V-018 — Peso en un plano inclinado

- **ID:** `t0_v_018`; **dificultad / tiempo:** 4 / 12 min; **tipo:** `written_upload_plus_numeric`.
- **Enunciado:** «Un bloque de 6,00 kg reposa sobre un plano de $25,0^\circ$. Toma $+x$ hacia arriba por la rampa y $+y$ normal hacia fuera. a) Dibuja el peso y los ejes. b) Calcula sus componentes con $g=9,81$ m·s⁻². c) Indica qué componente equilibra la normal si no hay otras fuerzas perpendiculares.»
- **Campos:** dibujo; `Px=-24.9 N`, `Py=-53.3 N` (tol. 0,1; 3 cifras); `normal=53.3 N`.
- **Pistas:** el peso total es $mg=58,8$ N vertical; ambos componentes son negativos con los ejes elegidos.
- **Solución:** $P_x=-mg\sin25^\circ=-24,9$ N y $P_y=-mg\cos25^\circ=-53,3$ N. En equilibrio perpendicular, $N=53,3$ N hacia $+y$.
- **Activo SVG obligatorio:** plano compacto, bloque, ejes locales y peso vertical; sin decorar con texturas; ángulo marcado una sola vez.
- **Errores:** poner una componente positiva; intercambiar seno/coseno; dibujar el peso perpendicular a la rampa.

## T0-V-019 — Distancia recorrida y desplazamiento

- **ID:** `t0_v_019`; **dificultad / tiempo:** 3 / 9 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Una persona camina 3,0 km al este, 2,0 km al norte y 5,0 km al oeste. a) Calcula la distancia total. b) Obtén las componentes, módulo y dirección del desplazamiento. c) Calcula la rapidez media y el módulo de la velocidad media si tarda 2,0 h.»
- **Campos:** `distance=10.0 km`; `Rx=-2.0 km`, `Ry=2.0 km`; `Rmag=2.83 km`; `Rangle=135°`; `average_speed=5.00 km/h`; `average_velocity_magnitude=1.41 km/h`.
- **Pistas:** la distancia suma longitudes; la velocidad media usa desplazamiento/tiempo.
- **Solución:** distancia 10,0 km; $R=(-2,2)$ km, $|R|=2,83$ km a 135°. Rapidez media 5,00 km/h y módulo de velocidad media 1,41 km/h.
- **Errores:** dividir el mismo numerador en ambos promedios; dar solo el módulo del desplazamiento; omitir dirección.

## T0-V-020 — Resultante y fuerza equilibrante

- **ID:** `t0_v_020`; **dificultad / tiempo:** 4 / 12 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Tres personas tiran de una anilla: 40,0 N a $0^\circ$, 30,0 N a $120^\circ$ y 25,0 N a $240^\circ$. a) Calcula la resultante. b) Da módulo y dirección. c) Determina la cuarta fuerza que produciría equilibrio.»
- **Campos:** `Rx=12.50 N`, `Ry=4.33 N`; `Rmag=13.23 N` (tol. 0,03); `Rangle=19.1°` (tol. 0,2); equilibrante `(-12.50,-4.33) N`, `199.1°`.
- **Pistas:** descompón las tres fuerzas antes de sumar; la equilibrante es exactamente $-R$.
- **Solución:** $R=(12,50,4,33)$ N, $|R|=13,23$ N, $\theta=19,1^\circ$. La cuarta fuerza es $(-12,50,-4,33)$ N, a $199,1^\circ$.
- **Errores:** sumar módulos; confundir equilibrante con una fuerza perpendicular; cambiar el módulo al invertir el sentido.

## T0-V-021 — Barca que quiere cruzar sin deriva

- **ID:** `t0_v_021`; **dificultad / tiempo:** 5 / 14 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Una barca puede navegar a 4,00 m·s⁻¹ respecto al agua. El río fluye a 1,50 m·s⁻¹ hacia el este y tiene 180 m de ancho. La barca quiere llegar justo enfrente. a) Determina el ángulo al oeste del norte con que debe apuntar. b) Calcula su velocidad respecto a la orilla. c) Calcula el tiempo de cruce.»
- **Campos:** `heading=22.0° west of north` (tol. 0,2); velocidad orilla `(0,3.71) m/s`; `crossing_time=48.5 s` (tol. 0,2).
- **Pistas:** la componente oeste de la barca debe cancelar 1,50 m/s; el módulo de la velocidad propia sigue siendo 4,00.
- **Solución:** $4\sin\alpha=1,5$, luego $\alpha=22,0^\circ$. La componente norte es $\sqrt{4^2-1,5^2}=3,71$ m/s y $t=180/3,71=48,5$ s.
- **Activo SVG recomendado:** suma vectorial de velocidad respecto al agua y corriente, más una vista superior del río; no usar flechas gigantes.
- **Errores:** sumar 4 y 1,5 como escalares; usar la resultante de deriva libre; dividir el ancho entre 4,00.

## T0-V-022 — Desplazamiento de un dron

- **ID:** `t0_v_022`; **dificultad / tiempo:** 4 / 11 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Un dron se desplaza 12,0 m al este, 7,0 m al sur y después 5,0 m a $60^\circ$ sobre el eje oeste. a) Traduce el tercer tramo a un ángulo desde $+x$. b) Calcula el desplazamiento total y su módulo. c) Compara con la distancia recorrida.»
- **Campos:** `third_angle=120°`; `Rx=9.50 m`, `Ry=-2.67 m`; `Rmag=9.87 m` (tol. 0,03); `path_length=24.0 m`.
- **Pistas:** «60° sobre el oeste» equivale a 120° desde $+x$; distancia y desplazamiento no se suman del mismo modo.
- **Solución:** tercer tramo $=(-2,50,4,33)$ m. El total es $(9,50,-2,67)$ m, módulo 9,87 m. La distancia recorrida es 24,0 m.
- **Errores:** usar 60° desde +x; sumar 5 al componente x; responder 24 m como desplazamiento.

## T0-V-023 — Producto escalar y proyección

- **ID:** `t0_v_023`; **dificultad / tiempo:** 5 / 14 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Sean $A=(2,-1,3)$ y $B=(4,5,-2)$. a) Calcula $A\cdot B$. b) Obtén el ángulo entre ellos. Además, para $d=(6,2)$ m y la dirección $u=(3,4)$, c) calcula la proyección escalar de d sobre u y d) el vector proyectado.»
- **Campos:** `dot=-3`; `angle=96.9°` (tol. 0,2); `scalar_projection=5.20 m` (tol. 0,02); `projection_x=3.12 m`, `projection_y=4.16 m`.
- **Pistas:** $\cos\theta=(A\cdot B)/(|A||B|)$; normaliza u antes de proyectar.
- **Solución:** $A\cdot B=-3$, de donde $\theta=96,9^\circ$. $\hat u=(0,6,0,8)$, $d\cdot\hat u=5,20$ m y $\operatorname{proj}_u d=5,20\hat u=(3,12,4,16)$ m.
- **Errores:** multiplicar módulos en lugar de componentes; proyectar sobre u sin normalizar; no interpretar el producto negativo como ángulo obtuso.

## T0-V-024 — Producto vectorial y carga negativa

- **ID:** `t0_v_024`; **dificultad / tiempo:** 5 / 13 min; **tipo:** `short_text_plus_numeric`.
- **Enunciado:** «$A=3\,\vec i$ y $B=4\,\vec j$. a) Calcula $A\times B$ y $B\times A$, indicando módulo y sentido. b) Interpreta $|A\times B|$ como área. c) Una carga negativa se mueve hacia $+x$ en un campo hacia $+y$: determina el sentido de $\vec v\times\vec B$ y de $q\vec v\times\vec B$.»
- **Campos:** `A_cross_B = +12 k`; `B_cross_A = -12 k`; `area=12`; `v_cross_B = out_of_page`; `force = into_page`.
- **Pistas:** usa la regla de la mano derecha para el producto; después invierte el sentido por ser $q<0$.
- **Solución:** $A\times B=12\vec k$ sale del papel y $B\times A=-12\vec k$ entra. El paralelogramo tiene área 12. Para la carga, $v\times B$ sale, pero la fuerza entra.
- **Activo SVG obligatorio:** símbolos ⊙ y ⊗ con leyenda, ejes x-y y una mano derecha esquemática opcional; nunca representar «entra/sale» con una flecha 2D ambigua.
- **Errores:** considerar conmutativo el producto vectorial; volver a multiplicar por el módulo de q cuando solo se pide sentido; olvidar invertir por carga negativa.

---

# BLOQUE M — Medida, error, incertidumbre y cifras significativas

## T0-M-001 — Error absoluto, relativo y signo

- **ID:** `t0_m_001`; **dificultad / tiempo:** 2 / 7 min; **tipo:** `numeric_multi`.
- **Enunciado:** «La longitud de referencia de una mesa es 120,0 cm y una alumna mide 118,6 cm. Calcula: a) error firmado $x_m-x_r$; b) error absoluto; c) error relativo porcentual; d) indica si sobreestima o subestima.»
- **Campos:** `signed_error=-1.4 cm`; `absolute_error=1.4 cm`; `relative_error=1.17 %` (tol. 0,01; 3 cifras); `direction=underestimate`.
- **Pistas:** el error absoluto nunca lleva signo; el relativo se divide entre el valor de referencia.
- **Solución:** error firmado $-1,4$ cm; absoluto $1,4$ cm; relativo $1,4/120,0\times100=1,17\%$; la medida subestima.
- **Errores:** dividir por la medida obtenida; dar error absoluto negativo; confundir 0,0117 con 1,17 %.

## T0-M-002 — Mismo porcentaje, distinto error absoluto

- **ID:** `t0_m_002`; **dificultad / tiempo:** 3 / 8 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Medición A: 49 g frente a 50 g. Medición B: 980 g frente a 1000 g. Calcula los errores absolutos y relativos porcentuales. Decide cuál es mejor en términos relativos y cuál se desvía más en gramos.»
- **Campos:** `abs_A=1 g`, `rel_A=2.00 %`; `abs_B=20 g`, `rel_B=2.00 %`; `relative_comparison=equal`; `larger_absolute=B`.
- **Pistas:** no compares solo los gramos cuando las escalas son distintas.
- **Solución:** A se desvía 1 g y B 20 g, pero ambas tienen error relativo del 2,00 %. Son igualmente buenas en términos relativos; B tiene mayor error absoluto.
- **Errores:** declarar A mejor sin especificar criterio; usar 49 o 980 como denominador de referencia; olvidar el porcentaje.

## T0-M-003 — Multiplicación y cifras significativas

- **ID:** `t0_m_003`; **dificultad / tiempo:** 3 / 8 min; **tipo:** `numeric_with_format`.
- **Enunciado:** «Evalúa $R=(12,4\times3,25)/0,80$. a) Da el valor de calculadora. b) Da el resultado que debe publicarse aplicando la regla de cifras significativas. c) Indica qué dato limita la precisión.»
- **Campos:** `calculator=50.375` (tol. 0,001); `reported=5.0e1` (**formato exigido:** `5,0×10^1`, 2 cifras); `limiting=0.80`.
- **Pistas:** en productos y cocientes manda el dato con menos cifras significativas; escribir solo `50` no deja claro si hay una o dos cifras.
- **Solución:** el valor bruto es 50,375. Como 0,80 tiene 2 cifras, se informa $5,0\times10^1$.
- **Errores:** redondear a 50,4 por decimales; escribir 50 sin marcar dos cifras; tomar 12,4 como limitante.

## T0-M-004 — Suma y posición decimal

- **ID:** `t0_m_004`; **dificultad / tiempo:** 2 / 7 min; **tipo:** `numeric_with_format`.
- **Enunciado:** «Suma 12,37 cm + 0,8 cm + 3,142 cm. a) Conserva el resultado de calculadora. b) Informa el resultado correctamente. c) Explica por qué aquí no se usa directamente el número de cifras significativas.»
- **Campos:** `calculator=16.312 cm`; `reported=16.3 cm` (tol. 0,001; **1 decimal**); explicación obligatoria.
- **Pistas:** en sumas manda la posición decimal menos precisa.
- **Solución:** $16,312$ cm se redondea a $16,3$ cm porque 0,8 solo llega a décimas.
- **Errores:** responder 16 cm por tener 1 cifra significativa en 0,8; conservar todas las cifras; redondear cada sumando antes de sumar.

## T0-M-005 — Serie de medidas y semidispersión

- **ID:** `t0_m_005`; **dificultad / tiempo:** 3 / 10 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Se mide cinco veces una longitud: 10,2; 10,4; 10,3; 10,5; 10,1 cm. Usa como incertidumbre la semidispersión $(x_{max}-x_{min})/2$. Calcula media, incertidumbre, resultado final y incertidumbre relativa.»
- **Campos:** `mean=10.3 cm` (tol. 0,01); `uncertainty=0.2 cm`; resultado textual `(10.3 ± 0.2) cm`; `relative=1.9 %` (tol. 0,05; 2 cifras).
- **Pistas:** la media usa las cinco medidas; la semidispersión solo máximo y mínimo.
- **Solución:** $\bar x=10,3$ cm, $u=(10,5-10,1)/2=0,2$ cm y $u_r=0,2/10,3\times100=1,94\%\approx1,9\%$.
- **Errores:** usar el rango completo 0,4; escribir más decimales en la media que en la incertidumbre; dividir la incertidumbre entre 100.

## T0-M-006 — Resolución de dos instrumentos

- **ID:** `t0_m_006`; **dificultad / tiempo:** 3 / 9 min; **tipo:** `single_choice_plus_numeric`.
- **Enunciado:** «Una regla analógica tiene divisiones de 1 mm y un calibre digital muestra centésimas de cm. Adoptando media división como incertidumbre instrumental: a) calcula la incertidumbre de cada uno en mm; b) decide cuál tiene mejor resolución; c) indica si “digital” basta por sí solo para justificar la elección.»
- **Campos:** `u_ruler=0.5 mm`; `u_caliper=0.05 mm`; `better=caliper`; respuesta conceptual: no, debe compararse resolución.
- **Pistas:** 0,01 cm = 0,1 mm; la incertidumbre asumida es la mitad del salto mínimo.
- **Solución:** regla ±0,5 mm; calibre ±0,05 mm. El calibre resuelve diez veces mejor, pero no por ser digital, sino por su incremento de 0,1 mm.
- **Errores:** convertir 0,01 cm en 1 mm; comparar pantallas y no escalas; usar la división completa pese al convenio dado.

## T0-M-007 — Precisión y exactitud no son sinónimos

- **ID:** `t0_m_007`; **dificultad / tiempo:** 4 / 11 min; **tipo:** `classification_multi`.
- **Enunciado:** «El valor de referencia es 10,00 cm. Tres grupos obtienen: A = 9,99; 10,00; 10,01. B = 10,48; 10,50; 10,49. C = 9,70; 10,30; 10,00. Clasifica cada serie en precisión alta/baja y exactitud de su promedio alta/baja. Justifica con dispersión y cercanía al valor de referencia.»
- **Respuesta:** A alta precisión y alta exactitud; B alta precisión y baja exactitud; C baja precisión pero promedio 10,00, por tanto alta exactitud del promedio. Justificación obligatoria.
- **Pistas:** precisión mira agrupamiento; exactitud mira cercanía al valor verdadero.
- **Solución:** A está agrupada y centrada; B agrupada pero desplazada ≈0,49 cm; C muy dispersa aunque su media coincide con 10,00 cm.
- **Errores:** llamar exacta a B por ser consistente; llamar precisa a C porque contiene un dato exacto; valorar datos aislados y no la serie.

## T0-M-008 — Corrección de error de cero

- **ID:** `t0_m_008`; **dificultad / tiempo:** 3 / 8 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Una balanza marca +0,6 g cuando está vacía. Al colocar una muestra indica 125,4 g. a) Identifica el tipo de error. b) Corrige la masa. c) Si la resolución es 0,1 g, informa el resultado con incertidumbre instrumental de media división.»
- **Campos:** `error_type=systematic_zero`; `corrected_mass=124.8 g`; `uncertainty=0.05 g`; formato `(124.80 ± 0.05) g`.
- **Pistas:** la lectura incluye el desplazamiento de cero; réstalo a todas las medidas.
- **Solución:** es un error sistemático de cero. $m=125,4-0,6=124,8$ g; con el convenio, $(124,80\pm0,05)$ g.
- **Errores:** sumar la corrección; llamarlo aleatorio; informar 124,8 ± 0,05 mezclando posiciones decimales.

## T0-M-009 — Diferencia de longitudes con incertidumbre

- **ID:** `t0_m_009`; **dificultad / tiempo:** 3 / 9 min; **tipo:** `numeric_multi`.
- **Enunciado:** «$L_1=(12,4\pm0,1)$ cm y $L_2=(8,7\pm0,1)$ cm. Usando suma lineal de incertidumbres máximas para suma/resta, calcula $D=L_1-L_2$ e informa el resultado. Indica los extremos mínimo y máximo compatibles.»
- **Campos:** `D=3.7 cm`; `u_D=0.2 cm`; `min=3.5 cm`; `max=3.9 cm`; formato `(3.7 ± 0.2) cm`.
- **Pistas:** el valor central se resta, pero las incertidumbres máximas se suman.
- **Solución:** $D=3,7$ cm y $u_D=0,1+0,1=0,2$ cm. Intervalo $[3,5,3,9]$ cm.
- **Errores:** restar incertidumbres; confundir extremos al restar intervalos; conservar centésimas inexistentes.

## T0-M-010 — Área e incertidumbre relativa

- **ID:** `t0_m_010`; **dificultad / tiempo:** 4 / 11 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Un rectángulo mide $(12,0\pm0,1)$ cm por $(5,0\pm0,1)$ cm. Usando para productos la suma de incertidumbres relativas: a) calcula el área; b) su incertidumbre relativa; c) su incertidumbre absoluta; d) informa el resultado.»
- **Campos:** `area=60.0 cm^2`; `relative=2.83 %` (tol. 0,02); `absolute=1.7 cm^2` (tol. 0,05); formato `(60.0 ± 1.7) cm^2`.
- **Pistas:** $u_A/A=u_L/L+u_W/W$; después $u_A=A(u_A/A)$.
- **Solución:** $A=60,0$ cm². $u_A/A=0,1/12,0+0,1/5,0=0,0283$; $u_A=1,7$ cm². Resultado $(60,0\pm1,7)$ cm².
- **Errores:** sumar 0,1+0,1 directamente al área; expresar 0,0283 como 0,0283 %; cuadrar la incertidumbre.

## T0-M-011 — Densidad con incertidumbre

- **ID:** `t0_m_011`; **dificultad / tiempo:** 4 / 12 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Una muestra tiene $m=(84,2\pm0,1)$ g y $V=(10,0\pm0,2)$ cm³. Para $\rho=m/V$, suma las incertidumbres relativas máximas. Calcula densidad, incertidumbre relativa, absoluta y resultado final.»
- **Campos:** `rho=8.42 g cm^-3`; `relative=2.12 %` (tol. 0,02); `absolute=0.18 g cm^-3` (tol. 0,01); formato `(8.42 ± 0.18) g cm^-3`.
- **Pistas:** en un cociente también se suman las incertidumbres relativas bajo este convenio.
- **Solución:** $\rho=8,42$. $u_r=0,1/84,2+0,2/10,0=0,0212$; $u_\rho=8,42(0,0212)=0,178\approx0,18$. Resultado $(8,42\pm0,18)$ g·cm⁻³.
- **Errores:** restar errores relativos por tratarse de un cociente; usar porcentajes como factores sin dividir entre 100; sobre-redondear el valor central.

## T0-M-012 — Elegir el instrumento adecuado

- **ID:** `t0_m_012`; **dificultad / tiempo:** 3 / 9 min; **tipo:** `single_choice_multi`.
- **Enunciado:** «Se quiere medir el grosor aproximado de una lámina de 0,80 mm con error relativo instrumental menor del 5 %. Hay tres instrumentos con resolución 1 mm, 0,1 mm y 0,01 mm. Suponiendo incertidumbre de media división, calcula el porcentaje esperado para cada uno y elige todos los que cumplen.»
- **Campos:** `p_1mm=62.5 %`; `p_0_1mm=6.25 %`; `p_0_01mm=0.625 %`; elección correcta: solo resolución 0,01 mm.
- **Pistas:** divide media resolución entre 0,80 mm y multiplica por 100.
- **Solución:** porcentajes 62,5 %, 6,25 % y 0,625 %. Solo el instrumento de 0,01 mm cumple <5 %.
- **Errores:** comparar resolución absoluta con 5 sin porcentaje; escoger 0,1 mm por parecer “una décima”; usar la resolución completa.

## T0-M-013 — Dato atípico en una serie

- **ID:** `t0_m_013`; **dificultad / tiempo:** 4 / 11 min; **tipo:** `numeric_plus_text`.
- **Enunciado:** «Los tiempos de una oscilación son 1,82; 1,79; 1,81; 2,46; 1,80 s. a) Identifica el dato sospechoso. b) Explica por qué no debe borrarse sin investigar. c) Si se confirma un fallo de cronometraje y se excluye, calcula media y semidispersión de los cuatro restantes e informa el resultado.»
- **Campos:** `suspect=2.46 s`; justificación obligatoria; `mean=1.805 s` (tol. 0,001); `half_range=0.015 s`; formato final `(1.81 ± 0.02) s`.
- **Pistas:** compara la separación del dato con la dispersión del grupo; redondea incertidumbre y valor al mismo decimal.
- **Solución:** 2,46 s es claramente discordante, pero primero se revisa la causa. Sin él, media 1,805 s y semidispersión 0,015 s; al informar, $(1,81\pm0,02)$ s.
- **Errores:** borrar el dato solo porque molesta; incluirlo después de declararlo fallo confirmado; escribir 1,805 ± 0,015 como resultado final sin criterio de redondeo.

## T0-M-014 — Pendiente experimental y unidades

- **ID:** `t0_m_014`; **dificultad / tiempo:** 4 / 12 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Una gráfica $y$ frente a $x$ contiene los puntos (0,0 m; 1,0 N), (2,0 m; 5,1 N) y (4,0 m; 9,0 N). a) Estima pendiente e intercepto usando los extremos. b) Escribe la ley lineal aproximada con unidades. c) Predice y para $x=3,0$ m.»
- **Campos:** `slope=2.00 N m^-1` (tol. 0,02); `intercept=1.00 N` (tol. 0,02); `prediction=7.00 N` (tol. 0,05); ley `y≈(2.00 N m^-1)x+1.00 N`.
- **Pistas:** la pendiente lleva unidades de variable vertical dividida por horizontal.
- **Solución:** $m=(9,0-1,0)/(4,0-0)=2,00$ N·m⁻¹; $b=1,00$ N; $y(3,0)\approx7,00$ N.
- **Activo SVG recomendado:** nube de tres puntos y recta aproximada; ejes rotulados con magnitud y unidad; límites ajustados a datos.
- **Errores:** omitir unidades de pendiente; forzar paso por origen; intercambiar x e y.

## T0-M-015 — Incertidumbre de una potencia

- **ID:** `t0_m_015`; **dificultad / tiempo:** 4 / 12 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Se calcula el volumen de una esfera con $V=\tfrac43\pi r^3$ y $r=(2,50\pm0,02)$ cm. Usa $u_V/V=3u_r/r$. Calcula volumen, incertidumbre relativa, incertidumbre absoluta y resultado final.»
- **Campos:** `volume=65.45 cm^3` (tol. 0,02); `relative=2.40 %`; `absolute=1.6 cm^3` (tol. 0,05); formato `(65.4 ± 1.6) cm^3`.
- **Pistas:** el exponente 3 multiplica la incertidumbre relativa; no eleves 0,02 al cubo.
- **Solución:** $V=65,45$ cm³, $u_V/V=3(0,02/2,50)=0,0240$, $u_V=1,57\approx1,6$ cm³. Se informa $(65,4\pm1,6)$ cm³.
- **Errores:** usar $3u_r$ sin dividir por r; cubicar la incertidumbre; informar más decimales en V que en u.

## T0-M-016 — Escritura correcta de un resultado

- **ID:** `t0_m_016`; **dificultad / tiempo:** 3 / 8 min; **tipo:** `single_choice_plus_text`.
- **Enunciado:** «Un cálculo produce $x=2,3764$ m y $u=0,083$ m. Usando una cifra significativa en la incertidumbre, elige y justifica: A) $(2,3764\pm0,083)$ m; B) $(2,4\pm0,08)$ m; C) $(2,38\pm0,08)$ m; D) $(2,376\pm0,1)$ m.»
- **Campos:** `choice=C`; justificación: $u\to0,08$ y x se redondea a centésimas.
- **Pistas:** primero redondea la incertidumbre; después iguala la posición decimal del valor.
- **Solución:** C, $(2,38\pm0,08)$ m.
- **Errores:** elegir A por “más precisión”; elegir B redondeando x a décimas; redondear x antes de u.

## T0-M-017 — Conversión de una medida con incertidumbre

- **ID:** `t0_m_017`; **dificultad / tiempo:** 3 / 9 min; **tipo:** `numeric_with_format`.
- **Enunciado:** «Convierte $(72,0\pm0,5)$ km·h⁻¹ a m·s⁻¹. Aplica el mismo factor tanto al valor como a la incertidumbre e informa ambos con posiciones decimales coherentes.»
- **Campos:** `value=20.00 m s^-1` (tol. 0,005); `uncertainty=0.14 m s^-1` (tol. 0,005); formato `(20.00 ± 0.14) m s^-1`.
- **Pistas:** divide ambos números entre 3,6.
- **Solución:** $72,0/3,6=20,00$ y $0,5/3,6=0,1389\approx0,14$. Resultado $(20,00\pm0,14)$ m·s⁻¹.
- **Errores:** convertir solo el valor central; multiplicar por 3,6; informar 20 ± 0,14.

## T0-M-018 — Calibración lineal de un termómetro

- **ID:** `t0_m_018`; **dificultad / tiempo:** 5 / 14 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Un termómetro marca 0,4 °C en el punto real 0,0 °C y 101,2 °C en el punto real 100,0 °C. Supón una relación lineal $T_{lec}=aT_{real}+b$. a) Halla a y b. b) Corrige una lectura de 37,0 °C. c) Indica por qué restar simplemente 0,4 °C no corrige por completo la escala.»
- **Campos:** `a=1.008` (tol. 0,0005); `b=0.4 °C`; `corrected=36.3 °C` (tol. 0,05); explicación obligatoria.
- **Pistas:** usa los dos puntos de calibración; despeja $T_{real}=(T_{lec}-b)/a$.
- **Solución:** $b=0,4$ y $a=(101,2-0,4)/100=1,008$. Para 37,0 °C, $T_{real}=(37,0-0,4)/1,008=36,31\approx36,3$ °C. Hay error de cero y de escala.
- **Errores:** corregir solo el cero; invertir a; usar grados Celsius como factor multiplicativo con unidades en a.

## T0-M-019 — Compatibilidad de dos medidas

- **ID:** `t0_m_019`; **dificultad / tiempo:** 4 / 10 min; **tipo:** `short_text_plus_numeric`.
- **Enunciado:** «Dos métodos dan $A=(9,8\pm0,2)$ y $B=(10,1\pm0,1)$ en la misma unidad. a) Escribe los intervalos compatibles. b) Decide si son compatibles bajo el criterio “los intervalos se solapan o tocan”. c) Calcula la diferencia entre valores centrales.»
- **Campos:** intervalo A `[9.6,10.0]`; B `[10.0,10.2]`; `compatible=yes_at_boundary`; `difference=0.3`.
- **Pistas:** forma $[x-u,x+u]$ para cada resultado.
- **Solución:** A admite [9,6;10,0] y B [10,0;10,2]. Tocan en 10,0, así que son compatibles justo en el límite del criterio dado. Los centros difieren 0,3.
- **Errores:** comparar solo centros; exigir solapamiento de anchura positiva pese al criterio; sumar incertidumbres al centro incorrecto.

## T0-M-020 — Medir varias oscilaciones

- **ID:** `t0_m_020`; **dificultad / tiempo:** 5 / 13 min; **tipo:** `numeric_multi_plus_text`.
- **Enunciado:** «Un cronómetro tiene una incertidumbre de reacción de ±0,2 s por medida. a) Si una oscilación se cronometra como 1,9 s, informa T. b) Si 10 oscilaciones duran 18,6 s, calcula T y su incertidumbre suponiendo que ±0,2 s afecta al tiempo total. c) Cuantifica el factor de mejora en incertidumbre absoluta y explica por qué conviene medir varios periodos.»
- **Campos:** método 1 `(1.9 ± 0.2) s`; método 10 `T=1.86 s`, `u_T=0.02 s`, formato `(1.86 ± 0.02) s`; `improvement_factor=10`; explicación obligatoria.
- **Pistas:** al dividir el tiempo total entre 10, divide también su incertidumbre absoluta entre 10.
- **Solución:** una oscilación da $(1,9\pm0,2)$ s. Diez dan $T=18,6/10=1,86$ s y $u_T=0,2/10=0,02$ s. La incertidumbre absoluta se reduce por un factor 10.
- **Errores:** mantener ±0,2 después de dividir; dividir la incertidumbre entre $\sqrt{10}$ pese al modelo explícito; decir que el valor 1,86 es más exacto solo por tener más decimales.

---

# BLOQUE C — Funciones, gráficas, derivadas e integrales

## T0-C-001 — De posición a velocidad y aceleración

- **ID:** `t0_c_001`; **dificultad / tiempo:** 3 / 10 min; **tipo:** `short_text_plus_numeric`.
- **Enunciado:** «La posición de una partícula es $x(t)=7-3t+2t^4$ m, con t en s. a) Obtén $v(t)$ y $a(t)$ con unidades. b) Calcula ambas en $t=1,00$ s. c) Explica el significado del signo de v en ese instante.»
- **Campos:** `v_expression=-3+8t^3` m·s⁻¹; `a_expression=24t^2` m·s⁻²; `v_1=5.00 m s^-1`; `a_1=24.0 m s^-2`; explicación: se mueve hacia +x.
- **Pistas:** deriva respecto al tiempo dos veces; el signo de velocidad indica sentido, no rapidez negativa.
- **Solución:** $v=-3+8t^3$ y $a=24t^2$. En 1,00 s, $v=5,00$ m·s⁻¹ y $a=24,0$ m·s⁻²; el movimiento instantáneo es hacia +x.
- **Errores:** olvidar derivar la constante; escribir unidades de posición en v/a; decir que velocidad positiva implica necesariamente aceleración positiva en todo instante.

## T0-C-002 — Potencias negativas y tasa local

- **ID:** `t0_c_002`; **dificultad / tiempo:** 3 / 9 min; **tipo:** `short_text_plus_numeric`.
- **Enunciado:** «Para $g(x)=5x^{-1}-2x^{-3}$, $x\ne0$: a) calcula $g'(x)$; b) evalúa $g'(2)$; c) indica en qué dos intervalos está definido el modelo.»
- **Campos:** `derivative=-5x^-2+6x^-4`; `value=-0.875` (tol. 0,002); dominio `(-∞,0)∪(0,∞)`.
- **Pistas:** $d(x^n)/dx=nx^{n-1}$ también para exponentes negativos.
- **Solución:** $g'=-5x^{-2}+6x^{-4}$ y $g'(2)=-5/4+6/16=-0,875$. El dominio excluye x=0.
- **Errores:** convertir $x^{-1}$ en $-x$; perder el signo de la segunda derivada; incluir cero.

## T0-C-003 — Raíces como potencias

- **ID:** `t0_c_003`; **dificultad / tiempo:** 3 / 9 min; **tipo:** `short_text_plus_numeric`.
- **Enunciado:** «Reescribe $h(x)=3\sqrt{x}-4/\sqrt{x}$ como potencias, deriva para $x>0$ y calcula la pendiente en $x=4$.»
- **Campos:** reescritura `3x^(1/2)-4x^(-1/2)`; derivada `(3/2)x^(-1/2)+2x^(-3/2)`; `slope=1.00` (tol. 0,005).
- **Pistas:** $1/\sqrt x=x^{-1/2}$; cuidado con el doble signo en el segundo término.
- **Solución:** $h'=\tfrac32x^{-1/2}+2x^{-3/2}$. En x=4: $3/4+1/4=1$.
- **Errores:** derivar la raíz como $x^{-1/2}$ sin factor 1/2; mantener signo negativo en el segundo término; evaluar antes de derivar.

## T0-C-004 — Parámetros y unidades en una función física

- **ID:** `t0_c_004`; **dificultad / tiempo:** 4 / 11 min; **tipo:** `short_text_multi`.
- **Enunciado:** «$x(t)=at^3-bt+c$ representa una posición en m y t se mide en s. a) Da las unidades de a, b y c. b) Obtén velocidad y aceleración. c) Comprueba dimensionalmente cada término de v y a.»
- **Respuesta:** `[a]=m s^-3`, `[b]=m s^-1`, `[c]=m`; $v=3at^2-b$ en m·s⁻¹; $a_x=6at$ en m·s⁻²; comprobación escrita.
- **Pistas:** todos los términos que se suman en x deben ser metros; derivar divide efectivamente por una unidad de tiempo.
- **Errores:** confundir el parámetro a con aceleración; dar las mismas unidades a los tres coeficientes; comprobar solo la fórmula original.

## T0-C-005 — Cambio medio e instantáneo

- **ID:** `t0_c_005`; **dificultad / tiempo:** 4 / 11 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Una posición viene dada por $x(t)=t^3-4t$ m. a) Calcula la velocidad media entre 1,0 s y 2,0 s. b) Calcula la velocidad instantánea y la aceleración en 2,0 s. c) Explica por qué la velocidad media no coincide con la instantánea.»
- **Campos:** `average_velocity=3.00 m s^-1`; `instant_velocity=8.00 m s^-1`; `acceleration=12.0 m s^-2`; explicación obligatoria.
- **Pistas:** $x(1)=-3$ y $x(2)=0$; la instantánea sale de la derivada.
- **Solución:** $v_{med}=[0-(-3)]/(2-1)=3$ m/s. $v=3t^2-4$, luego $v(2)=8$ m/s; $a=6t$, luego $a(2)=12$ m/s².
- **Errores:** promediar $v(1)$ y $v(2)$ sin justificar; dividir posición final por tiempo final; confundir v con a.

## T0-C-006 — Puntos estacionarios y clasificación

- **ID:** `t0_c_006`; **dificultad / tiempo:** 4 / 12 min; **tipo:** `numeric_multi_plus_text`.
- **Enunciado:** «Para $f(x)=x^3-3x^2$: a) localiza los puntos donde $f'=0$; b) calcula sus coordenadas; c) clasifícalos como máximo o mínimo usando el signo de $f'$ o $f''$.»
- **Campos:** `x1=0`, `f1=0`, tipo `local_max`; `x2=2`, `f2=-4`, tipo `local_min`; justificación obligatoria.
- **Pistas:** $f'=3x(x-2)$; $f''=6x-6$.
- **Solución:** en x=0, $f''=-6<0$, máximo local (0,0). En x=2, $f''=6>0$, mínimo local (2,-4).
- **Errores:** resolver solo x=2; llamar extremos a las raíces de f; clasificar sin comprobar cambio o segunda derivada.

## T0-C-007 — Misma velocidad, distinta posición

- **ID:** `t0_c_007`; **dificultad / tiempo:** 3 / 9 min; **tipo:** `short_text_multi`.
- **Enunciado:** «Dos móviles tienen $x_1(t)=2t^2+3$ m y $x_2(t)=2t^2-5$ m. a) Compara sus velocidades y aceleraciones. b) Calcula su separación con signo $x_1-x_2$. c) Explica físicamente qué representa la constante que desaparece al derivar.»
- **Respuesta:** ambas velocidades $4t$ m/s y aceleraciones $4$ m/s²; separación constante 8 m; constantes representan posiciones iniciales.
- **Pistas:** deriva, pero también resta las funciones originales.
- **Errores:** concluir que ocupan el mismo lugar porque tienen la misma derivada; decir que la constante “no importa”; restar 3−5.

## T0-C-008 — De aceleración a velocidad con condición inicial

- **ID:** `t0_c_008`; **dificultad / tiempo:** 3 / 10 min; **tipo:** `short_text_plus_numeric`.
- **Enunciado:** «Una partícula tiene $a(t)=4+3t^2$ m·s⁻² y $v(0)=-2$ m·s⁻¹. a) Obtén v(t). b) Calcula v(2,0 s). c) Indica si basta con una primitiva sin constante.»
- **Campos:** `v_expression=4t+t^3-2` m·s⁻¹; `v_2=14.0 m s^-1`; conceptual: no, la condición fija C=-2.
- **Pistas:** integra a y usa v(0).
- **Solución:** una primitiva es $4t+t^3+C$; v(0)=-2 da C=-2. Así v(2)=8+8-2=14 m/s.
- **Errores:** olvidar C; usar C=0 automáticamente; derivar en lugar de integrar.

## T0-C-009 — Cambio de velocidad acumulado

- **ID:** `t0_c_009`; **dificultad / tiempo:** 4 / 11 min; **tipo:** `short_text_plus_numeric`.
- **Enunciado:** «$a(t)=6t^2-4t+1$ m·s⁻² y $v(0)=3$ m·s⁻¹. a) Halla v(t). b) Calcula el cambio de velocidad entre 0 y 2 s mediante una integral definida. c) Comprueba que coincide con v(2)-v(0).»
- **Campos:** `v_expression=2t^3-2t^2+t+3`; `delta_v=10.0 m s^-1`; `v_2=13.0 m s^-1`; comprobación obligatoria.
- **Pistas:** $\Delta v=\int_0^2 a(t)dt$.
- **Solución:** $v=2t^3-2t^2+t+3$. La integral vale $[2t^3-2t^2+t]_0^2=10$ m/s y 13−3=10.
- **Errores:** sumar v(0) dentro de $\Delta v$; omitir límites; perder el término lineal.

## T0-C-010 — Área bajo v(t)

- **ID:** `t0_c_010`; **dificultad / tiempo:** 3 / 9 min; **tipo:** `numeric_multi`.
- **Enunciado:** «La velocidad es $v(t)=2t+1$ m·s⁻¹. Entre t=1 s y t=3 s: a) calcula el desplazamiento por integración; b) calcula la velocidad media; c) comprueba el desplazamiento como área de un trapecio.»
- **Campos:** `displacement=10.0 m`; `average_velocity=5.00 m s^-1`; área trapecio `10.0 m`.
- **Pistas:** $v(1)=3$ y $v(3)=7$; el intervalo dura 2 s.
- **Solución:** $\int_1^3(2t+1)dt=10$ m. $v_{med}=10/2=5$ m/s. Trapecio: $(3+7)2/2=10$ m.
- **Errores:** calcular el área desde t=0; confundir área con velocidad; dividir entre 3 s y no entre 2 s.

## T0-C-011 — Desplazamiento cero, distancia no nula

- **ID:** `t0_c_011`; **dificultad / tiempo:** 4 / 12 min; **tipo:** `numeric_multi_plus_text`.
- **Enunciado:** «Un móvil tiene $v(t)=t^3$ m·s⁻¹ entre −2 s y 2 s. a) Calcula el desplazamiento. b) Calcula la distancia recorrida. c) Explica la diferencia usando el signo de v.»
- **Campos:** `displacement=0 m`; `distance=8.00 m`; explicación: v negativa antes de 0 y positiva después.
- **Pistas:** para distancia integra $|v|$ o separa en t=0.
- **Solución:** la función impar integra 0 en límites simétricos. Distancia $=\int_{-2}^0(-t^3)dt+\int_0^2t^3dt=4+4=8$ m.
- **Errores:** concluir que no se mueve; usar la integral con signo como distancia; tomar valor absoluto solo al final.

## T0-C-012 — Signo antes de calcular

- **ID:** `t0_c_012`; **dificultad / tiempo:** 2 / 7 min; **tipo:** `single_choice_plus_numeric`.
- **Enunciado:** «Sin hallar primero una primitiva, predice el signo de $I=\int_0^2-(x+1)dx$ y justifica desde la gráfica. Después calcula I exactamente.»
- **Campos:** `sign=negative`; `I=-4.00`; justificación: función bajo eje x en todo [0,2].
- **Pistas:** observa el signo del integrando; luego integra para comprobar.
- **Solución:** el integrando es siempre negativo, por lo que I<0. $I=-[x^2/2+x]_0^2=-4$.
- **Errores:** predecir positivo porque el área geométrica es positiva; cambiar límites; omitir el signo exterior.

## T0-C-013 — Movimiento a velocidad constante por tramos

- **ID:** `t0_c_013`; **dificultad / tiempo:** 4 / 12 min; **tipo:** `numeric_multi`.
- **Enunciado:** «$v=2,0$ m/s entre 0 y 3 s y $v=-1,0$ m/s entre 3 y 7 s. Si $x(0)=5,0$ m: a) calcula desplazamiento; b) distancia; c) posición final; d) instante en que vuelve a x=5,0 m, si ocurre.»
- **Campos:** `displacement=2.0 m`; `distance=10.0 m`; `final_position=7.0 m`; `return_within_interval = no`; `hypothetical_return_time = 9.0 s` si se prolonga el segundo tramo.
- **Pistas:** primer tramo aporta +6 m; después retrocede a 1 m/s.
- **Solución:** $\Delta x=6-4=2$ m; distancia $6+4=10$ m; $x_f=7$ m. Desde x=11 m en t=3 necesita retroceder 6 m, por lo que vuelve a x=5 en t=9 s, **fuera del intervalo descrito**. Por tanto, dentro de [0,7] no vuelve.
- **Errores:** afirmar t=6 s contando desde cero en el segundo tramo; sumar velocidades; confundir posición final y desplazamiento.

## T0-C-014 — Recta experimental por dos puntos

- **ID:** `t0_c_014`; **dificultad / tiempo:** 3 / 9 min; **tipo:** `short_text_multi`.
- **Enunciado:** «Una calibración lineal relaciona entrada x (V) y salida y (mA) y pasa por (1,0 V; 2,0 mA) y (5,0 V; 10,0 mA). Obtén la ecuación, las unidades de pendiente e intercepto y predice y para 3,5 V.»
- **Campos:** `slope=2.0 mA V^-1`; `intercept=0 mA`; ecuación `y=(2.0 mA V^-1)x`; `prediction=7.0 mA`.
- **Pistas:** calcula pendiente y usa un punto para b; no borres unidades en la ecuación física.
- **Solución:** pendiente $(10-2)/(5-1)=2$ mA/V y b=0; para 3,5 V, y=7,0 mA.
- **Errores:** hallar pendiente 1/2; escribir y=2x sin aclarar unidades; suponer b=0 sin comprobar.

## T0-C-015 — Recta, cortes e interpretación

- **ID:** `t0_c_015`; **dificultad / tiempo:** 3 / 9 min; **tipo:** `numeric_multi`.
- **Enunciado:** «Construye la recta de pendiente −3 que pasa por (2,5). a) Escríbela como $y=mx+b$. b) Calcula sus cortes con ambos ejes. c) Comprueba el punto dado.»
- **Campos:** ecuación `y=-3x+11`; `y_intercept=11`; `x_intercept=11/3` (aceptar 3,667; tol. 0,002); comprobación `y(2)=5`.
- **Pistas:** usa $y-5=-3(x-2)$.
- **Solución:** $y=-3x+11$; cortes (0,11) y (11/3,0). Al sustituir x=2 se obtiene 5.
- **Errores:** usar b=5; cambiar el signo al desarrollar; redondear 11/3 demasiado pronto.

## T0-C-016 — Función por tramos y continuidad

- **ID:** `t0_c_016`; **dificultad / tiempo:** 4 / 13 min; **tipo:** `written_upload_plus_text`.
- **Enunciado:** «Construye y dibuja $f(x)$: vale 1 de x=0 a 2; crece linealmente hasta valer 5 en x=4; permanece en 5 hasta x=6. a) Escribe la función por tramos con intervalos. b) Comprueba continuidad en 2 y 4. c) Da la pendiente de cada tramo.»
- **Respuesta:** $f=1$ en [0,2]; $f=2x-3$ en (2,4]; $f=5$ en (4,6]; pendientes 0,2,0; continua en uniones. Dibujo `pending_review`.
- **Activo SVG obligatorio para solución:** ejes con límites x∈[−0,5;6,5], y∈[0;6], tramos azul/coral/verde, puntos de unión claros, sin cuadrícula dominante.
- **Errores:** usar pendiente 4/2 en lugar de (5−1)/(4−2) aunque aquí coincidan sin justificar; generar saltos por intervalos mal definidos; omitir puntos extremos.

## T0-C-017 — Recuperar una función desde su derivada

- **ID:** `t0_c_017`; **dificultad / tiempo:** 4 / 11 min; **tipo:** `short_text_multi`.
- **Enunciado:** «Se sabe que $f'(x)=6x-4$ y $f(1)=3$. a) Halla la familia de primitivas. b) Usa la condición para obtener f. c) Verifica derivando y evaluando.»
- **Campos:** familia `3x^2-4x+C`; `C=4`; `f=3x^2-4x+4`; verificación obligatoria.
- **Pistas:** una derivada no determina la altura vertical; la condición fija C.
- **Solución:** $f=3x^2-4x+C$. Como $f(1)=3$, $3-4+C=3$, así que C=4.
- **Errores:** omitir C; imponer f(0)=3; comprobar solo una de las dos condiciones.

## T0-C-018 — Construcción con valor y pendiente

- **ID:** `t0_c_018`; **dificultad / tiempo:** 5 / 14 min; **tipo:** `written_solution`.
- **Enunciado:** «Busca el polinomio de grado mínimo que cumple $f(0)=2$, $f(1)=3$ y $f'(1)=0$. a) Justifica por qué una recta no basta. b) Determina el polinomio. c) Explica si las tres condiciones harían única una función sin restringir el grado.»
- **Respuesta esperada:** grado mínimo 2; $f(x)=-x^2+2x+2$; una recta no puede tener pendiente 0 y cambiar de 2 a 3; sin limitar grado no es única. Corrección manual/parcial por pasos.
- **Pistas:** prueba $f=ax^2+bx+c$; las condiciones dan c=2, a+b=1 y 2a+b=0.
- **Errores:** dar una solución válida de grado mayor sin atender «grado mínimo»; afirmar unicidad entre todas las funciones; no verificar.

## T0-C-019 — Leer crecimiento y pendientes de una gráfica

- **ID:** `t0_c_019`; **dificultad / tiempo:** 4 / 12 min; **tipo:** `numeric_multi_plus_text`.
- **Enunciado:** «Una gráfica lineal por tramos une (0,0), (2,4), (4,4) y (6,1). a) Indica dónde crece, es constante y decrece. b) Calcula la pendiente de cada tramo. c) Identifica en qué puntos no existe una derivada única y por qué.»
- **Campos:** intervalos `(0,2)`, `(2,4)`, `(4,6)`; pendientes `2`, `0`, `-1.5`; no derivable en x=2 y x=4 por cambio brusco de pendiente.
- **Pistas:** cada pendiente es $\Delta y/\Delta x$; en una esquina las pendientes laterales difieren.
- **Activo SVG obligatorio:** poligonal exacta con puntos rotulados A–D; ejes compactos; no escribir la respuesta sobre la gráfica.
- **Errores:** incluir las esquinas en intervalos de derivada constante; confundir decrecer con valores negativos; decir que pendiente cero implica y=0.

## T0-C-020 — Área con signo y movimiento en una gráfica v–t

- **ID:** `t0_c_020`; **dificultad / tiempo:** 5 / 16 min; **tipo:** `numeric_multi_plus_text`.
- **Enunciado:** «La gráfica velocidad-tiempo une linealmente (0 s,0 m/s), (2 s,4 m/s), (4 s,4 m/s) y (6 s,−3 m/s). a) Halla el instante exacto en que cambia de sentido en el último tramo. b) Calcula área positiva, área negativa con signo, desplazamiento y distancia total entre 0 y 6 s. c) Explica por qué distancia y desplazamiento difieren.»
- **Campos:** `zero_time=36/7 s = 5.143 s` (tol. 0,003); `positive_area=100/7 m = 14.286 m` (tol. 0,01); `negative_signed=-9/7 m = -1.286 m`; `displacement=13.0 m`; `distance=109/7 m = 15.571 m`.
- **Pistas:** el último segmento cruza v=0 antes de t=6; separa sus dos triángulos. Los primeros tramos aportan 4 m y 8 m.
- **Solución:** en el tramo final $v=4-\tfrac72(t-4)$, así que v=0 en $t=36/7$ s. Área positiva $4+8+16/7=100/7$ m; negativa $-9/7$ m; desplazamiento $91/7=13$ m; distancia $109/7=15,571$ m.
- **Activo SVG obligatorio:** gráfica v–t exacta; regiones positiva y negativa con rellenos suaves distintos; línea v=0 destacada; unidades en ambos ejes; el visor no debe revelar valores de solución antes de entregar.
- **Errores:** tratar todo el último trapecio como positivo o negativo; usar `12` como área positiva ignorando la parte sobre el eje después de t=4; sumar área negativa con signo para la distancia. **Nota:** la respuesta del banco v3 para este gráfico era incorrecta; no reutilizar `12, −3, 9`.

---

# 4. Requisitos de conversión a JSON

## 4.1 Versión e identidad

- El nuevo banco será `version: 4`.
- Los 60 IDs conservados (`u_001…u_016`, `v_001…v_024`, `c_001…c_020`) representan revisiones sustanciales: cada ejercicio debe llevar `version: 4`.
- Se crean `t0_m_001…t0_m_020` para el bloque de medida.
- Se retiran del catálogo activo `t0_u_017`, `t0_u_018`, `t0_v_025…t0_v_036`, `t0_e_001`, `t0_e_002` y `t0_c_021…t0_c_024`. No se reasignan. El contenido útil de los dos ejercicios `t0_e_*` queda ampliado en `t0_m_001` y `t0_m_002`.
- Antes de retirar IDs, comprobar que el historial tolera ejercicios ausentes. Si no, mantener un pequeño índice de metadatos retirados (ID, título antiguo, versión y estado `retired`) para que el historial siga siendo legible; no mostrar esos ejercicios en `/homework`.

## 4.2 Campos de respuesta

- Cada apartado calculable tendrá su propio `field_id`; no guardar una respuesta multiparte como un único string.
- Los campos numéricos incluirán `expected_value`, unidad, tolerancia absoluta y, cuando corresponda, `significant_figures` o `decimal_places`.
- Las fracciones exactas indicadas se aceptarán además de su decimal.
- Los campos de unidad aceptarán notación equivalente: por ejemplo `N m^-1` y `J m^-2` cuando ambas sean correctas.
- Los campos de selección usarán IDs estables (`A`, `B`, etc.) y nunca inferirán la opción correcta a partir de su posición visual.
- Los dibujos y justificaciones se guardan como `pending_review`; los apartados numéricos del mismo ejercicio sí se autocorrigen.
- Un campo vacío requerido no puede acabar como respuesta correcta por normalización.

## 4.3 Pistas y solución

- Cargar las pistas exactamente en el orden dado, una por nivel.
- No convertir una pista en una mini-solución que revele todos los números.
- La solución guiada debe separar apartados y mostrar unidades en los pasos intermedios.
- Añadir feedback dirigido a cada error listado. Evitar mensajes universales repetidos.
- No mostrar `final_answer`, tolerancias ni metadatos de corrección en el HTML antes de entregar.

## 4.4 Formato matemático y español

- Usar MathJax/TeX real; no dejar `$...$` visible como texto.
- Usar coma decimal en contenido visible y punto decimal en valores internos JSON.
- Usar «1.º de Bachillerato», «versión», «deducción», «módulo», «ángulo», «gráfica» e «incertidumbre» con ortografía correcta.
- Separar valor y unidad con espacio no separable en HTML cuando sea posible.
- No usar `Ohm` como texto visible si puede renderizarse $\Omega$; sí puede mantenerse como forma normalizada interna.

## 4.5 Activos visuales

Solo son obligatorios los SVG mencionados expresamente en:

- `t0_v_012` — suma y resta punta-cola;
- `t0_v_017` — ejes girados;
- `t0_v_018` — plano inclinado;
- `t0_v_024` — entra/sale del papel;
- `t0_c_016` — función por tramos;
- `t0_c_019` — lectura de pendientes;
- `t0_c_020` — áreas en gráfica v–t.

Son recomendados, pero no necesarios para publicar la primera versión, los SVG de `t0_v_021` y `t0_m_014`.

Contrato visual común:

- SVG con `viewBox` compacto y responsivo, sin ancho/alto raster fijos.
- Trazo de ejes 1,5–2 px y vectores 2,5–3 px.
- Cabezas de flecha proporcionadas (aprox. 8–10 px), nunca triángulos gigantes.
- Tipografía heredada de la web para etiquetas; TeX solo si se renderiza de forma consistente.
- Colores semánticos constantes: vector/dato principal azul, segundo vector verde, resultante coral, construcción auxiliar gris.
- Ninguna etiqueta debe cruzar una flecha o quedar recortada.
- `alt` o descripción accesible específica.
- La figura no ocupará más de 520 px de ancho en escritorio salvo que la gráfica necesite más; en móvil se ajusta al contenedor.

# 5. Validación editorial antes de integrar

Codex debe producir un informe de validación y no limitarse a convertir el Markdown:

1. Confirmar 80 IDs únicos y exactamente 16 U + 24 V + 20 M + 20 C.
2. Confirmar que no queda ningún ejercicio de dificultad 1.
3. Verificar matemáticamente todas las soluciones mediante un script independiente del generador.
4. Verificar que cada campo numérico tiene unidad, tolerancia y regla de redondeo cuando aplica.
5. Verificar que cada ejercicio tiene al menos dos acciones cognitivas reales.
6. Comprobar que ninguna solución se expone antes de entregar.
7. Comprobar que las pistas progresivas no son duplicados genéricos.
8. Comprobar que los siete SVG obligatorios existen, son legibles a 390 px y no contienen espacio vacío dominante.
9. Renderizar manualmente una muestra de al menos dos ejercicios por bloque y todos los que tienen SVG.
10. Ejecutar tests completos, `git diff --check` y el validador de catálogo.

# 6. Decisiones que Codex no debe tomar por su cuenta

- No añadir ejercicios adicionales para “rellenar”.
- No rebajar números o eliminar apartados para simplificar el desarrollo.
- No sustituir campos escritos por test si aquí se pide justificación.
- No convertir todos los ejercicios en autocorregibles fingiendo que una explicación abierta puede corregirse con igualdad de strings.
- No generar imágenes con IA ni usar gráficos automáticos sin revisar.
- No restaurar IDs retirados con contenido distinto.
- No cambiar respuestas o tolerancias porque una prueba falle: primero comprobar si el fallo está en el esquema, el parser o el dato.

# 7. Resultado esperado de la siguiente iteración

La implementación debe entregar:

- el JSON v4 completo;
- los SVG obligatorios;
- tests de esquema, unicidad, corrección y no exposición de soluciones;
- un pequeño script de validación matemática/editorial;
- una tabla de migración con IDs conservados, creados y retirados;
- un informe de cualquier incompatibilidad real con el flujo actual de `ExerciseAttempt` / `ExerciseResponse`.

La interfaz y el sistema de intentos no se rediseñan en esta tarea. Primero se cierra y valida el contenido; después se adapta la experiencia web al nuevo banco.
