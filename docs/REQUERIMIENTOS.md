# Portal para comerciales — borrador de requerimientos

Documento derivado del prompt inicial. **Faltan definiciones** (marcadas como TBD); este texto sirve para alinear con TI, comerciales y seguridad.

---

## 1. Objetivo

Herramienta web ligera para **equipos comerciales** (internos y externos corporativos) que permita:

- Ver **gráficas** e indicadores de ventas / productos / cartera.
- Navegar por **secciones** (botones o menú) sin cambiar de aplicación.
- **Buscar** clientes, productos u oportunidades.
- **Capturar notas o consultas** (texto libre o formularios simples) según el perfil.

Entrega prevista: algo desplegable en red corporativa (y acceso controlado para externos).

---

## 2. Usuarios y acceso

| Perfil | Quién es | Acceso |
|--------|----------|--------|
| **Interno** | Empleados de áreas comerciales, gerencia, operaciones de venta en casa matriz/sucursales. | Datos amplios: márgenes, inventario sensible, todos los productos, reportes históricos completos. |
| **Externo corporativo** | Fuerza de venta o partners que **ofrecen productos a clientes** pero pertenen al esquema corporativo (misma marca, contrato, capacitación). | Catálogo y precios **autorizados**, clientes **asignados**, sin datos financieros internos ni productos restringidos. |

**TBD (pendiente de negocio):**

- ¿Autenticación? (Entra ID / Azure AD, VPN, SSO existente).
- ¿Externos = misma tenant M365 con licencia distinta o app con login propio + lista blanca?
- Auditoría: quién vio qué y exportaciones.

---

## 3. Funcionalidad mínima (MVP)

### 3.1 Visualización

- Gráficas: ventas por periodo, por producto, por región/comercial (según datos disponibles).
- Filtros por fechas y categoría.
- Actualización: manual (carga de CSV/Excel) o conexión a API/BD (**TBD**).

### 3.2 Navegación

- Botones o pestañas: p. ej. **Resumen**, **Productos**, **Clientes**, **Mis notas**.
- Al cambiar sección, cambian gráficas y tablas (misma sesión).

### 3.3 Búsqueda y escritura

- Campo de **búsqueda** global o por sección (texto parcial).
- **Notas** o **comentarios** por cliente/oportunidad (interno: todas; externo: solo su cartera) — **TBD** persistencia (SharePoint, SQL, etc.).

### 3.4 Distribución a comerciales

- URL interna + guía de uso corta.
- Opcional: exportar PDF o captura de tablero (**TBD**).
- Capacitación: qué ve cada perfil.

---

## 4. No funcionales

- Idioma: español (i18n **TBD**).
- Responsive básico (tablet en visita a cliente).
- Rendimiento: respuesta &lt; 3 s con volumen acordado (**TBD**).
- Cumplimiento: datos personales de clientes según política corporativa.

---

## 5. Stack sugerido (alineado al prototipo)

| Capa | Opción MVP | Producción posible |
|------|------------|-------------------|
| UI + gráficas | **Streamlit** o **Dash** (Python) | Mismo o migrar a web React + API |
| Datos | CSV / Excel / Parquet en servidor | SQL Server, Dataverse, Power BI semantic model |
| Auth | Simulación por perfil en MVP | Microsoft Entra ID, grupos `Comercial-Interno` / `Comercial-Externo` |
| Hosting | VM interna o Azure App Service | Red corporativa + WAF |

---

## 6. Criterios de aceptación (borrador)

1. Usuario **interno** inicia sesión (o selecciona perfil en demo) y ve gráficas completas y catálogo sin restricciones de demo.
2. Usuario **externo** ve solo productos permitidos y sin columnas confidenciales.
3. Búsqueda devuelve resultados en &lt; 2 s sobre dataset de prueba acordado.
4. Al menos **tres secciones** navegables por botones con contenido distinto.
5. Documentación de despliegue para equipo que envía el enlace a comerciales.

---

## 7. Preguntas abiertas para la siguiente iteración

1. ¿Fuente única de verdad? (ERP, CRM, Excel de comerciales).
2. ¿Qué debe poder **escribir** el comercial? (solo notas vs. crear pedido/cotización).
3. ¿Offline o solo online?
4. ¿Marca visual (logo, colores)?
5. ¿Integración con Teams / correo para notificar?

---

*Prototipo de referencia en la raíz del repo: `app.py` (Streamlit).*
