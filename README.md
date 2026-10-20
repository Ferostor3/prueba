# Portal comerciales (prototipo)

Demo en Python para alinear requerimientos con equipos comerciales (acceso interno y externo corporativo).

## Requerimientos

Ver [docs/REQUERIMIENTOS.md](docs/REQUERIMIENTOS.md).

## Ejecutar

```bash
cd ~/Projects/portal-comerciales
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

Abre la URL local (por defecto `http://localhost:8501`).

## Qué demuestra

- Gráficas (Plotly): ventas por mes, región y producto.
- Botones en barra lateral: Resumen, Productos, Clientes, Notas.
- Búsqueda global y por sección.
- Perfil **Interno** vs **Externo** (catálogo y clientes filtrados; sin margen para externos).

## Próximos pasos sugeridos

- Entra ID y grupos de seguridad.
- Conectar ERP/CRM o Power BI.
- Persistir notas y auditoría.
- Despliegue interno (Azure App Service, VM, etc.).
