# Checklist antes de subir a producción

> **Esqueleto.** Los pasos concretos saldrán del recorrido completo de la web
> como alumno y como profesor (tarea 2.1 de la limpieza del 22/11/2026). Hasta
> entonces, cada sección solo dice qué debe cubrir.

Objetivo: un recorrido de unos 15 minutos en local, antes de cada merge a
`main` que cambie la interfaz, las rutas o el contenido.

## 0. Preparación

- [ ] `python -m pytest` pasa.
- [ ] Si se han tocado ejercicios: validadores de
      [exercise-workflow.md](exercise-workflow.md).
- [ ] Web arrancada en local con una base de prueba (no la de Neon).

## 1. Acceso

- [ ] _Por definir: login de alumno, login de profesor, logout, rutas que
      requieren login (incluida `/exams`), cambio de contraseña._

## 2. Alumno: estudiar

- [ ] _Por definir: Apuntes, visor de PDF, descarga, resúmenes._

## 3. Alumno: practicar

- [ ] _Por definir: catálogo y filtros, abrir un ejercicio, empezar, guardar
      borrador, entregar, ver la solución, siguiente ejercicio, historial._

## 4. Alumno: progreso

- [ ] _Por definir: página de progreso y continuidad ("seguir donde lo
      dejaste")._

## 5. Profesor

- [ ] _Por definir: resumen de alumnos, ficha de un alumno, intento con
      respuestas, cuentas (crear, cambiar contraseña, desactivar)._

## 6. Móvil

- [ ] _Por definir: qué páginas se revisan con ancho de móvil._

## 7. Después de desplegar

- [ ] Ver [deployment.md](deployment.md#después-de-desplegar).
