import os
import pandas as pd
from fpdf import FPDF
import streamlit as st
from datetime import datetime

# Configuración inicial de la página
st.set_page_config(
    page_title="Sistema de Inventarios - SEBISO", layout="wide"
)

st.markdown(
    """
    <h2 style='text-align: center; color: #b38f00;'>SECRETARÍA DE BIENESTAR E INCLUSIÓN SOCIAL</h2>
    <h4 style='text-align: center; color: #555;'>Sistema de Control de Bienes Muebles y Generación de Resguardos</h4>
""",
    unsafe_allow_html=True,
)

# --- CATÁLOGO MAESTRO DE ÁREAS INSTITUCIONALES ---
AREAS_MAESTRAS = [
    "DIRECCION DE GESTION INSTITUCIONAL",
    "DIRECCION GENERAL DE FOMENTO ARTESANAL",
    "DIRRECION GENERAL DE ATENCION AL MIGRANTE",
    "SUBSECRETARIA DE INCLUSION Y DESARROLLO",
    "SUBSECRETARIA DE DESARROLLO SOCIAL Y HUMANO",
    (
        "DIRECCION GENERAL DE PROSPECTIVA, PLANEACION Y EVALUACION DE LOS"
        " PROGRAMAS SOCIALES"
    ),
    "DIRECCION GENERAL DE OPERACIÓN Y LOGISTICA DE PROGRAMAS",
    "INSTITUTO HIDALGUENSE DE LA JUVENTUD",
    "COORDINACION ADMINISTRATIVA -DIRECCION DE RECURSOS MATERIALES",
    "COORDINACION ADMINISTRATIVA-DIRECCION DE RECURSOS HUMANOS",
    "COORDINACION ADMINISTRATIVA-INFORMATICA",
    (
        "COORDINACION ADMINISTRATIVA-SUBDIRECCION DE INTEGRACION Y CONTROL DE"
        " INFORMACION"
    ),
    "DIRECCION GENERAL DE SERVIDORES DEL PUEBLO",
    "DIRECCIÓN DE RECURSOS FINANCIEROS",
    "DIRECCION DE CONTROL Y SEGUIMINTO DE AUDITORIA",
    "COORDINACIÓN ADMINISTRATIVA",
    "DIRECCION GENERAL  DE ASISTENCIA, ATENCION Y PROTECCION",
    "DIRECCIÓN DE SUBSIDIO AL SERVICIO DE VERIFICACION VEHICULAR",
    "ORGANO INTERNO DE CONTROL",
    "MOBILIARIO PARA PRESTAMO",
]

# --- 1. SELECCIÓN DE BASE DE DATOS ---
st.sidebar.header("📁 Base de Datos")
opcion_bd = st.sidebar.selectbox(
    "Selecciona la Base de Datos:", ["archiveros.xlsx", "SEBISOO.xlsx"]
)

# Creamos las dos pestañas principales solicitadas
tab_original, tab_edicion = st.tabs(
    ["📄 Vista Original Completa (Excel)", "✏️ Panel de Control y Edición"]
)

# ==========================================
# PESTAÑA 1: VISTA ORIGINAL COMPLETA
# ==========================================
with tab_original:
  st.subheader(f"Vista íntegra del archivo original: {opcion_bd}")
  st.markdown(
      "Este apartado muestra el archivo tal como se encuentra en su origen,"
      " conservando su estructura completa y portada original."
  )
  if os.path.exists(opcion_bd):
    try:
      xls = pd.ExcelFile(opcion_bd)
      df_raw_view = pd.read_excel(
          opcion_bd, sheet_name=xls.sheet_names[0], header=None, dtype=str
      )
      df_raw_view = df_raw_view.fillna("")
      if "SEBISOO" in opcion_bd:
        df_raw_view = df_raw_view.iloc[:, :14]
      st.dataframe(
          df_raw_view, use_container_width=True, height=650, hide_index=True
      )
    except Exception as e:
      st.error(f"Error al cargar la vista original: {e}")
  else:
    st.warning(f"No se encontró el archivo {opcion_bd} en el directorio.")

# ==========================================
# PESTAÑA 2: PANEL DE CONTROL Y EDICIÓN
# ==========================================
with tab_edicion:

  # Carga inteligente y flexible de archivos
  @st.cache_data(ttl=1)
  def cargar_datos(archivo):
    if os.path.exists(archivo):
      try:
        if "SEBISOO" in archivo:
          xls = pd.ExcelFile(archivo)
          primera_pestana = xls.sheet_names[0]
          df = pd.read_excel(archivo, sheet_name=primera_pestana, header=29)

          df = df.dropna(
              subset=[col for col in df.columns if "Inventario" in str(col)]
          ).reset_index(drop=True)

          if "Nombre " in df.columns:
            df.rename(columns={"Nombre ": "DESCRIPCION"}, inplace=True)
          if "Marc " in df.columns:
            df.rename(columns={"Marc ": "MARCA"}, inplace=True)
          if "Modelo " in df.columns:
            df.rename(columns={"Modelo ": "MODELO"}, inplace=True)
          if "Serie " in df.columns:
            df.rename(columns={"Serie ": "SERIE"}, inplace=True)
          if "Descripción" in df.columns:
            df.rename(columns={"Descripción": "CARACTERISTICAS"}, inplace=True)

          if "AREA" not in df.columns:
            df["AREA"] = "DIRECCION DE RECURSOS MATERIALES"
          if "NOMBRE DEL USUARIO" not in df.columns:
            df["NOMBRE DEL USUARIO"] = ""
          return df
        else:
          df = pd.read_excel(archivo)
          if "NOMBRE DEL USUARIO" not in df.columns:
            df["NOMBRE DEL USUARIO"] = ""
          return df
      except Exception as e:
        st.error(f"Error al leer el archivo {archivo}: {e}")
        return pd.DataFrame()
    else:
      return pd.DataFrame()

  df = cargar_datos(opcion_bd)

  if not df.empty:
    columna_area = None
    for col in df.columns:
      if "area" in str(col).lower() or "dirección" in str(col).lower():
        columna_area = col
        break

    if not columna_area:
      df["AREA"] = "DIRECCION DE RECURSOS MATERIALES"
      columna_area = "AREA"

    areas_en_archivo = (
        df[columna_area].dropna().astype(str).str.strip().tolist()
    )
    todas_las_areas = sorted(list(set(AREAS_MAESTRAS + areas_en_archivo)))

    # --- 2. FILTROS DE ÁREA EN BARRA LATERAL ---
    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Filtros de Área")

    area_seleccionada = st.sidebar.selectbox(
        "Selecciona el Área para el Resguardo:", ["Todas"] + todas_las_areas
    )

    if area_seleccionada != "Todas":
      df_filtrado = df[
          df[columna_area].astype(str).str.strip() == area_seleccionada
      ].copy()
    else:
      df_filtrado = df.copy()

    # --- 3. PANEL DE REGISTRO RÁPIDO ---
    with st.expander("➕ Registrar Nuevo Bien / Asignar Área", expanded=False):
      st.markdown(
          "Agrega un bien directamente y asígnale su área correspondiente en"
          f" **{opcion_bd}**:"
      )
      with st.form("form_nuevo_bien"):
        c1, c2, c3 = st.columns(3)
        with c1:
          nuevo_inv = st.text_input("No. Inventario")
          nuevo_desc = st.text_input("Descripción", "SILLA PLEGABLE")
          nuevo_marca = st.text_input("Marca", "SIN MARCA")
        with c2:
          nuevo_modelo = st.text_input("Modelo", "SIN MODELO")
          nuevo_serie = st.text_input("Serie", "S/S")
          nuevo_carac = st.text_input(
              "Características", "REFORZADA CON ASIENTO Y RESPALDO"
          )
        with c3:
          nuevo_usuario = st.text_input(
              "Nombre del Servidor Público / Usuario", ""
          )
          nueva_area_reg = st.selectbox("Área de Adscripción", todas_las_areas)
          nueva_obs = st.text_input("Observaciones", "")

        btn_agregar = st.form_submit_button("Guardar Bien en la Base de Datos")

        if btn_agregar:
          nuevo_registro = {
              (
                  "INVENTARIO"
                  if "INVENTARIO" in df.columns
                  else "No. Inventario"
              ): nuevo_inv,
              (
                  "DESCRIPCION" if "DESCRIPCION" in df.columns else "Nombre "
              ): nuevo_desc,
              "MARCA" if "MARCA" in df.columns else "Marc ": nuevo_marca,
              "MODELO" if "MODELO" in df.columns else "Modelo ": nuevo_modelo,
              "SERIE" if "SERIE" in df.columns else "Serie ": nuevo_serie,
              (
                  "CARACTERISTICAS"
                  if "CARACTERISTICAS" in df.columns
                  else "Descripción"
              ): nuevo_carac,
              "NOMBRE DEL USUARIO": nuevo_usuario,
              columna_area: nueva_area_reg,
          }
          df = pd.concat(
              [df, pd.DataFrame([nuevo_registro])], ignore_index=True
          )
          df.to_excel(opcion_bd, index=False)
          st.success("¡Bien registrado correctamente!")
          st.rerun()

    # --- 4. PANEL PRINCIPAL: TABLA EDITABLE ---
    st.subheader(
        f"Visualizando registros de: {opcion_bd} (Área: {area_seleccionada})"
    )
    st.markdown(f"Total de bienes en esta vista: **{len(df_filtrado)}**")

    df_editado = st.data_editor(
        df_filtrado,
        num_rows="dynamic",
        use_container_width=True,
        key="editor_principal",
    )

    if st.button("💾 Guardar Cambios en Excel"):
      try:
        df.update(df_editado)
        df.to_excel(opcion_bd, index=False)
        st.success("¡Cambios guardados en el archivo de Excel con éxito!")
      except Exception as e:
        st.error(f"Error al guardar: {e}")

    # --- 5. GENERACIÓN DEL PDF EXCLUSIVO DEL ÁREA ---
    st.markdown("---")
    st.subheader("📄 Generación de Resguardo PDF Exclusivo de esta Área")

    if st.button("📥 Generar PDF de Resguardo (Solo esta Área)"):
      if df_editado.empty:
        st.warning(
            "No hay bienes registrados para generar el PDF con este filtro."
        )
      elif area_seleccionada == "Todas":
        st.warning(
            "Por favor selecciona un **Área específica** en la barra lateral"
            " para generar su resguardo individual."
        )
      else:
        try:
          pdf = FPDF(orientation="L", unit="mm", format="letter")
          pdf.add_page()
          pdf.set_auto_page_break(auto=True, margin=10)

          # --- LOGOTIPO INSTITUCIONAL ---
          if os.path.exists("BIENESTAR8.png"):
            # Coloca la imagen en la parte superior izquierda (x=10, y=8, ancho=45mm)
            pdf.image("BIENESTAR8.png", x=10, y=8, w=45)

          # Encabezado institucional
          pdf.set_font("Arial", "B", 10)
          pdf.cell(
              0,
              6,
              "SECRETARÍA DE BIENESTAR E INCLUSIÓN SOCIAL",
              0,
              1,
              "C",
          )
          pdf.set_font("Arial", "B", 8)
          pdf.cell(0, 4, "COORDINACIÓN ADMINISTRATIVA", 0, 1, "C")
          pdf.cell(0, 4, "INVENTARIO DE BIENES MUEBLES 2026", 0, 1, "C")
          pdf.cell(0, 4, "RESGUARDO INDIVIDUAL INTERNO", 0, 1, "C")
          pdf.ln(5)

          # Datos de Área y Fecha
          fecha_hoy = datetime.now().strftime("%d/%m/%Y")
          pdf.set_font("Arial", "B", 8)
          pdf.cell(15, 6, "AREA:", 0, 0, "L")
          pdf.set_font("Arial", "", 8)
          pdf.cell(140, 6, area_seleccionada, 0, 0, "L")
          pdf.set_font("Arial", "B", 8)
          pdf.cell(20, 6, "FECHA:", 0, 0, "R")
          pdf.set_font("Arial", "", 8)
          pdf.cell(30, 6, fecha_hoy, 0, 1, "R")
          pdf.ln(2)

          # Configuración de columnas (Ancho total exacto = 257 mm)
          headers = [
              "No.",
              "INVENTARIO",
              "DESCRIPCION",
              "MARCA",
              "MODELO",
              "SERIE",
              "CARACTERISTICAS",
              "NOMBRE DEL USUARIO",
              "OBSERVACION",
          ]
          widths = [8, 24, 42, 18, 18, 15, 52, 48, 32]

          pdf.set_font("Arial", "B", 6.5)
          for i, h in enumerate(headers):
            pdf.cell(widths[i], 5, h, 1, 0, "C")
          pdf.ln()

          # Filas con manejo limpio de altura automática por celda multilínea
          pdf.set_font("Arial", "", 6)
          for idx, (_, row) in enumerate(df_editado.iterrows(), start=1):
            inv_val = str(
                row.get(
                    "INVENTARIO",
                    row.get(
                        "No. Inventario",
                        row.get("NO. INTERNO DE INVENTARIO", ""),
                    ),
                )
            )
            desc_val = str(row.get("DESCRIPCION", row.get("Nombre ", "")))
            marca_val = str(row.get("MARCA", row.get("Marc ", "SIN MARCA")))
            modelo_val = str(row.get("MODELO", row.get("Modelo ", "SIN MODELO")))
            serie_val = str(row.get("SERIE", row.get("Serie ", "S/S")))
            carac_val = str(
                row.get("CARACTERISTICAS", row.get("Descripción", ""))
            )
            usu_val = str(row.get("NOMBRE DEL USUARIO", ""))
            obs_val = str(
                row.get("OBSERVACIONES", row.get("OBSERVACION", ""))
            )

            cell_data = [
                str(idx),
                inv_val,
                desc_val,
                marca_val,
                modelo_val,
                serie_val,
                carac_val,
                usu_val,
                obs_val,
            ]

            line_h = 3.5
            max_lines = 1
            for i, text in enumerate(cell_data):
              if widths[i] > 0 and len(str(text)) > 0:
                chars_per_line = max(4, int(widths[i] / 1.8))
                lines = max(
                    1,
                    int(len(str(text)) / chars_per_line)
                    + (1 if len(str(text)) % chars_per_line > 0 else 0),
                )
                if lines > max_lines:
                  max_lines = lines

            row_height = max(5, max_lines * line_h + 1.5)

            x_start = pdf.get_x()
            y_start = pdf.get_y()

            for i, text in enumerate(cell_data):
              current_x = pdf.get_x()
              current_y = pdf.get_y()
              pdf.rect(current_x, current_y, widths[i], row_height)
              pdf.set_xy(current_x + 1, current_y + 0.8)
              pdf.multi_cell(
                  widths[i] - 2, line_h, str(text), 0, "L"
              )
              pdf.set_xy(current_x + widths[i], current_y)

            pdf.set_xy(x_start, y_start + row_height)

          # Nota al pie y firmas institucionales
          pdf.ln(4)
          pdf.set_font("Arial", "", 5)
          nota_legal = (
              "CON FUNDAMENTO EN LO DISPUESTO POR LOS ARTÍCULOS 149 V EN"
              " FRACCIÓN II DE LA CONSTITUCIÓN POLÍTICA DEL ESTADO DE HIDALGO;"
              " 7 FRACCIÓN III DE LA LEY GENERAL DE RESPONSABILIDADES"
              " ADMINISTRATIVAS; 2 PÁRRAFO ÚNICO DE LA LEY ORGÁNICA DE LA"
              " ADMINISTRACIÓN PÚBLICA DEL ESTADO DE HIDALGO; 4"
              " FRACCIÓN VI, 6 FRACCIÓN IV Y 45 SÉPTIMO Y OCTAVO PÁRRAFO DE LAS"
              " NORMAS GENERALES PARA ADMINISTRAR Y CONTROLAR LOS BIENES"
              " MUEBLES... RECIBÍ DE COMPLETA CONFORMIDAD LOS BIENES MUEBLES"
              " ANTES LISTADOS."
          )
          pdf.multi_cell(0, 3, nota_legal, 0, "J")
          pdf.ln(8)

          # Cuadros de Firmas
          y_firma = pdf.get_y()
          pdf.rect(10, y_firma, 85, 15)
          pdf.rect(98, y_firma, 85, 15)
          pdf.rect(186, y_firma, 84, 15)

          pdf.set_xy(10, y_firma + 11)
          pdf.cell(
              85, 3, "FIRMA DEL SERVIDOR PÚBLICO RESPONSABLE", 0, 0, "C"
          )
          pdf.set_xy(98, y_firma + 11)
          pdf.cell(85, 3, "AVALA", 0, 0, "C")
          pdf.set_xy(186, y_firma + 11)
          pdf.cell(84, 3, "Vo.Bo.", 0, 1, "C")

          output_pdf = "resguardo_area.pdf"
          pdf.output(output_pdf)

          with open(output_pdf, "rb") as f:
            st.download_button(
                label=(
                    "📥 Descargar Resguardo PDF"
                    f" ({area_seleccionada[:15]})"
                ),
                data=f,
                file_name=(
                    f"Resguardo_{area_seleccionada.replace(' ', '_')[:25]}.pdf"
                ),
                mime="application/pdf",
            )
          st.success("¡PDF exclusivo de esta área generado exitosamente!")

        except Exception as e:
          st.error(f"Error al generar el PDF: {e}")

  else:
    st.warning(
        "No se encontraron registros válidos en la base de datos seleccionada."
    )