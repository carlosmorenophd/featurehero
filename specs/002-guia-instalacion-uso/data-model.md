# Data Model: Guía de instalación y uso para principiantes

Esta feature no modifica el modelo de datos de ejecución de Feature Hero. El
modelo siguiente describe las entidades documentales que deben mantenerse
consistentes durante la implementación.

## Guía de usuario

- **Purpose**: Documento principal para instalar y ejecutar Feature Hero por primera vez.
- **Fields**: título, alcance, requisitos, navegación, recorridos de plataforma,
  inicio rápido, solución de problemas y referencias técnicas.
- **Validation**: debe existir como Markdown independiente, ser enlazable desde
  `README.md` y cubrir FR-001–FR-014.

## Recorrido de plataforma

- **Purpose**: Secuencia de pasos para preparar, instalar y verificar el paquete.
- **Fields**: plataforma, requisitos, comandos, activación del entorno, señal de
  éxito, recuperación y límites de soporte.
- **Instances**: Windows PowerShell, Windows CMD, macOS, Ubuntu/Debian y orientación
  general para otras distribuciones Linux.
- **Validation**: cada acción debe tener una señal observable de éxito o un siguiente
  paso de recuperación.

## Inicio rápido

- **Purpose**: Ejemplo reproducible desde una instalación verificada hasta una primera ejecución.
- **Fields**: archivo de entrada, columna objetivo o columnas transformadas,
  comando, salida esperada y criterios de interpretación.
- **Relationships**: usa un Recorrido de plataforma completado y enlaza con el Contrato CLI.
- **Validation**: debe ejecutarse con datos pequeños y no depender de una ruta inexistente.

## Problema frecuente

- **Purpose**: Entrada de recuperación para un fallo que un principiante puede encontrar.
- **Fields**: síntoma, causa probable, acción correctiva, verificación y cuándo solicitar ayuda.
- **Instances**: Python no encontrado, comando no reconocido, permisos, entorno no
  activado, ruta incorrecta, formato no soportado y columnas inválidas.

## Referencia técnica

- **Purpose**: Enlace al README o a la ayuda del CLI para detalles avanzados.
- **Relationship**: complementa la Guía de usuario sin duplicar ni contradecir sus instrucciones básicas.

## Índice bilingüe

- **Purpose**: Tabla de contenidos navegable para un idioma específico dentro de
  `README.md` o `INSTALLATION_GUIDE.md`.
- **Fields**: idioma, título visible, destino interno, sección equivalente en el
  otro idioma y enlace al otro documento.
- **Instances**: Índice español e índice inglés en cada documento.
- **Validation**: cada destino debe existir, llevar a la sección correcta y
  permitir llegar al documento relacionado sin perder el idioma seleccionado.
