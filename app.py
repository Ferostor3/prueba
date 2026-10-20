"""Portal comercial — prototipo Streamlit (interno / externo corporativo)."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

DATA_DIR = Path(__file__).resolve().parent / "data"

PERFIL_INTERNO = "Interno (corporativo)"
PERFIL_EXTERNO = "Externo (comercial de campo)"


@st.cache_data
def load_tables() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    productos = pd.read_csv(DATA_DIR / "productos.csv")
    ventas = pd.read_csv(DATA_DIR / "ventas.csv")
    clientes = pd.read_csv(DATA_DIR / "clientes.csv")
    return productos, ventas, clientes


def filtrar_productos(productos: pd.DataFrame, es_interno: bool) -> pd.DataFrame:
    if es_interno:
        return productos.copy()
    return productos[productos["visible_externo"]].copy()


def filtrar_clientes(
    clientes: pd.DataFrame, es_interno: bool, comercial: str | None
) -> pd.DataFrame:
    if es_interno:
        return clientes.copy()
    if not comercial:
        return clientes.iloc[0:0].copy()
    return clientes[clientes["comercial_asignado"] == comercial].copy()


def aplicar_busqueda(df: pd.DataFrame, query: str, columnas: list[str]) -> pd.DataFrame:
    q = query.strip().lower()
    if not q:
        return df
    mask = pd.Series(False, index=df.index)
    for col in columnas:
        if col in df.columns:
            mask |= df[col].astype(str).str.lower().str.contains(q, na=False)
    return df[mask]


def init_session() -> None:
    if "notas" not in st.session_state:
        st.session_state.notas = []
    if "seccion" not in st.session_state:
        st.session_state.seccion = "Resumen"


def main() -> None:
    st.set_page_config(
        page_title="Portal comerciales",
        page_icon="📊",
        layout="wide",
    )
    init_session()

    productos, ventas, clientes = load_tables()

    with st.sidebar:
        st.title("Acceso")
        perfil = st.radio(
            "Perfil",
            [PERFIL_INTERNO, PERFIL_EXTERNO],
            help="En producción esto vendría de Entra ID / grupos de seguridad.",
        )
        es_interno = perfil == PERFIL_INTERNO

        comercial_externo: str | None = None
        if not es_interno:
            comerciales = sorted(clientes["comercial_asignado"].unique())
            comercial_externo = st.selectbox("Comercial (simulación login)", comerciales)

        st.divider()
        st.caption("Secciones")
        for label, key in [
            ("📈 Resumen", "Resumen"),
            ("📦 Productos", "Productos"),
            ("👥 Clientes", "Clientes"),
            ("📝 Notas", "Notas"),
        ]:
            if st.button(label, use_container_width=True):
                st.session_state.seccion = key

        st.divider()
        busqueda_global = st.text_input(
            "Búsqueda rápida",
            placeholder="Cliente, producto, SKU…",
        )

    st.header("Portal para comerciales")
    st.caption(
        "Prototipo: gráficas, botones, búsqueda y perfiles interno/externo. "
        "Datos de ejemplo en `data/`."
    )

    if not es_interno:
        st.info(
            "Vista **externa**: solo productos autorizados, clientes de tu cartera "
            "y sin márgenes internos."
        )

    seccion = st.session_state.seccion
    prod_v = filtrar_productos(productos, es_interno)
    cli_v = filtrar_clientes(clientes, es_interno, comercial_externo)

    if busqueda_global:
        prod_v = aplicar_busqueda(prod_v, busqueda_global, ["sku", "nombre", "categoria"])
        cli_v = aplicar_busqueda(
            cli_v, busqueda_global, ["id_cliente", "nombre", "region", "comercial_asignado"]
        )

    if seccion == "Resumen":
        render_resumen(ventas, prod_v, es_interno)
    elif seccion == "Productos":
        render_productos(prod_v, es_interno)
    elif seccion == "Clientes":
        render_clientes(cli_v)
    else:
        render_notas(es_interno, comercial_externo)


def render_resumen(ventas: pd.DataFrame, productos: pd.DataFrame, es_interno: bool) -> None:
    st.subheader("Resumen de ventas")

    skus_visibles = set(productos["sku"])
    v = ventas[ventas["sku"].isin(skus_visibles)]

    col1, col2, col3 = st.columns(3)
    col1.metric("Ventas (demo)", f"${v['monto'].sum():,.0f} MXN")
    col2.metric("Operaciones", len(v))
    col3.metric("Productos en catálogo", len(productos))

    fig_mes = px.bar(
        v.groupby("mes", as_index=False)["monto"].sum(),
        x="mes",
        y="monto",
        title="Ventas por mes",
        labels={"monto": "Monto", "mes": "Mes"},
    )
    st.plotly_chart(fig_mes, use_container_width=True)

    c1, c2 = st.columns(2)
    with c1:
        fig_reg = px.pie(
            v.groupby("region", as_index=False)["monto"].sum(),
            names="region",
            values="monto",
            title="Por región",
        )
        st.plotly_chart(fig_reg, use_container_width=True)
    with c2:
        fig_prod = px.bar(
            v.groupby("sku", as_index=False)["monto"].sum().merge(
                productos[["sku", "nombre"]], on="sku", how="left"
            ),
            x="nombre",
            y="monto",
            title="Por producto",
            labels={"monto": "Monto", "nombre": "Producto"},
        )
        st.plotly_chart(fig_prod, use_container_width=True)

    if es_interno:
        st.markdown("#### Detalle (solo interno)")
        st.dataframe(v, use_container_width=True, hide_index=True)


def render_productos(productos: pd.DataFrame, es_interno: bool) -> None:
    st.subheader("Catálogo")
    filtro = st.text_input("Buscar en productos", key="buscar_prod")
    df = aplicar_busqueda(productos, filtro, ["sku", "nombre", "categoria"])

    columnas = ["sku", "nombre", "categoria", "precio_lista"]
    if es_interno:
        columnas.append("margen_pct")
    else:
        df = df.drop(columns=["margen_pct"], errors="ignore")

    st.dataframe(df[columnas], use_container_width=True, hide_index=True)

    fig = px.scatter(
        df,
        x="precio_lista",
        y="categoria",
        size=[40] * len(df),
        hover_data=["sku", "nombre"],
        title="Precio de lista por categoría",
    )
    st.plotly_chart(fig, use_container_width=True)


def render_clientes(clientes: pd.DataFrame) -> None:
    st.subheader("Cartera de clientes")
    filtro = st.text_input("Buscar en clientes", key="buscar_cli")
    df = aplicar_busqueda(
        clientes, filtro, ["id_cliente", "nombre", "region", "estatus"]
    )

    st.dataframe(df, use_container_width=True, hide_index=True)

    consulta = st.text_area(
        "Consulta o comentario para seguimiento (demo, no se guarda en BD)",
        placeholder="Ej.: Cliente pide cotización Plan Empresa Plus…",
    )
    if st.button("Registrar nota rápida (demo)") and consulta.strip():
        st.session_state.notas.append({"origen": "Clientes", "texto": consulta.strip()})
        st.success("Nota agregada en esta sesión (ver sección Notas).")


def render_notas(es_interno: bool, comercial: str | None) -> None:
    st.subheader("Notas de la sesión")
    st.caption("En producción: guardar en CRM, SharePoint o SQL con usuario y fecha.")

    nueva = st.text_area("Nueva nota", key="nota_nueva")
    if st.button("Guardar nota") and nueva.strip():
        autor = "Interno" if es_interno else (comercial or "Externo")
        st.session_state.notas.append({"origen": autor, "texto": nueva.strip()})

    if not st.session_state.notas:
        st.write("Sin notas aún.")
        return

    for i, nota in enumerate(reversed(st.session_state.notas), start=1):
        st.markdown(f"**{nota['origen']}** — {nota['texto']}")


if __name__ == "__main__":
    main()
