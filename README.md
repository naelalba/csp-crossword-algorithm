# Crossword Solver CSP 🧩

Motor algorítmico diseñado para la generación y resolución automática de crucigramas, modelado matemáticamente como un Problema de Satisfacción de Restricciones (CSP)[cite: 7]. 

## 📌 Contexto del Proyecto
Este repositorio contiene el código desarrollado para la asignatura de Sistemas Inteligentes del Grado en Ingeniería Informática de la Universidad de Alicante (Curso 2026/2027)[cite: 7]. 

El proyecto parte de un entorno gráfico base proporcionado por la universidad[cite: 7]. **El trabajo central y de autoría propia de este repositorio radica exclusivamente en la arquitectura lógica y la implementación del motor de resolución**, encargado de encontrar combinaciones de palabras válidas sin repeticiones[cite: 10]. Las palabras introducidas tanto en horizontal como en vertical deben contener el mismo carácter exacto en su punto de intersección[cite: 7].

## ⚙️ Motor Algorítmico Implementado

El núcleo del software incluye la implementación desde cero de tres algoritmos fundamentales de satisfacción de restricciones:

*   **Algoritmo AC-3 (Arc Consistency):** Sistema de preprocesamiento que evalúa las variables del tablero para reducir sus dominios iniciales y eliminar inconsistencias de arista antes de iniciar los procesos de búsqueda profunda[cite: 12].
*   **Forward Checking (FC):** Algoritmo predictivo que, al asignar un valor a una variable actual, comprueba la viabilidad frente a las variables futuras (huecos del crucigrama sin instanciar) que comparten restricciones, eliminando de sus dominios las opciones incompatibles[cite: 11].
*   **Backtracking (BK):** Sistema de búsqueda recursiva que explora combinaciones de palabras y retrocede a estados anteriores (desasignando variables) en el momento que detecta una ruta inconsistente sin solución[cite: 10].

*(Opcional: Si implementaste Backjumping, añade esta línea)*
*   **Backjumping (BJ):** Optimización de la búsqueda que evita el sobreprocesamiento (*trashing*) saltando directamente al origen estructural del conflicto algorítmico, en lugar de retroceder cronológicamente[cite: 13, 14].

## 🚀 Despliegue y Ejecución

El software admite la carga de diccionarios de palabras personalizados y configuraciones de tablero mediante ficheros de texto[cite: 8]. 

Para lanzar el entorno, ejecuta el script principal indicando los parámetros requeridos:

```bash
# Ejecución estableciendo dimensiones manuales y fichero de diccionario
python main.py --filas 5 --columnas 6 --dic diccionario.txt

# Ejecución cargando una plantilla de tablero predefinida
python main.py --plantilla tablero.txt --dic diccionario.txt
```

Al iniciar la interfaz gráfica, el panel lateral permite ejecutar a demanda la reducción de dominios (AC3) o la resolución completa mediante los motores de búsqueda (BK o FC)[cite: 8].
