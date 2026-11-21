# Reglas de desarrollo

- Cada inicio de un spec debe crear una feature mediante el plugin Git de Speckit.
- Una feature permanece abierta hasta que el usuario solicite explícitamente su cierre. No ejecutar `feature finish` automáticamente.
- Si al iniciar una acción existen archivos sin guardar, hacer primero su commit y continuar desde ese estado.
- Las acciones `analyze`, `specify`, `plan`, `tasks` e `implement` deben crear un commit propio al finalizar. Aplicar la misma regla a las demás acciones de Speckit habilitadas por los hooks.
- Mantener activos todos los plugins Git de Speckit: `initialize`, `feature`, `commit`, `remote` y `validate`.
- La versión de `pyproject.toml` debe seguir `yyyy.mayor.minor.micro`; usar el año actual de desarrollo y controlar `mayor`, `minor` y `micro`. Cada cambio debe actualizar la versión.
- Realizar cambios mínimos, cubrir exactamente lo definido por la especificación y no agregar trabajo extra. El desarrollo debe ser únicamente funcional.
- Antes de hacer commit de cambios que no haya realizado el agente, mostrar al usuario el diff correspondiente y solicitar confirmación explícita. Los cambios realizados por el agente pueden hacerse commit directamente sin solicitar confirmación.
