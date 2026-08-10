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

# --- CATÁLOGO MAESTRO DE ÁREAS INSTITUCIONALES (Completas y sin abreviaciones) ---
AREAS_MAESTRAS = [
    "DIRECCION DE GESTION INSTITUCIONAL",
    "ÓRGANO INTERNO DE CONTROL",
    "DIRECCIÓN GENERAL DE ASISTENCIA, ATENCIÓN Y PROTECCIÓN",
    "SUBSECRETARÍA DE INCLUSIÓN Y DESARROLLO",
    "DIRECCIÓN GENERAL DE PROSPECTIVA, PLANEACIÓN Y EVALUACIÓN DE LOS PROGRAMAS SOCIALES",
    "DIRECCIÓN GENERAL DE OPERACIÓN Y LOGÍSTICA DE PROGRAMAS",
    "COORDINACIÓN ADMINISTRATIVA",
    "SUBDIRECCIÓN DE INTEGRACIÓN Y CONTROL DE INFORMACIÓN",
    "DIRECCIÓN DE RECURSOS FINANCIEROS",
    "DIRECCIÓN DE RECURSOS HUMANOS",
    "DIRECCIÓN DE CONTROL Y SEGUIMIENTO DE AUDITORÍA",
    "SUBSECRETARÍA DE PARTICIPACIÓN SOCIAL Y FOMENTO ARTESANAL",
    "DIRECCIÓN GENERAL DE FOMENTO ARTESANAL",
    "SUBSECRETARÍA DE DESARROLLO SOCIAL Y HUMANO",
    "DIRECCIÓN GENERAL DE ATENCIÓN AL MIGRANTE",
    "DIRECCIÓN GENERAL DE INCLUSIÓN PARA LAS PERSONAS CON DISCAPACIDAD",
    "DIRECCIÓN DE RECURSOS MATERIALES",
    "DIRECCIÓN GENERAL DE SERVIDORES DEL PUEBLO",
    "CONTACT CENTER",
    "DIRECCIÓN DE SUBSIDIO AL SERVICIO DE VERIFICACIÓN VEHICULAR",
]

LISTA_RESPONSABLES = [
    "RICARDO GÓMEZ MORENO",
    "MARLEN ELVA ARISTA AMADOR",
    "JOSUÉ RAYMUNDO SÁNCHEZ ÁVALOS",
    "PAUL GIOVANNI SÁNCHEZ NIETO",
    "JUAN ALEXIS GARCÍA GARCÍA",
    "DIANA LAURA FERNÁNDEZ MONROY",
    "JORGE ALBERTO VARGAS ROMERO",
    "EMMANUEL HUERTA MONZALVO",
    "DIVANI SHAIRENE CARDOSO LARA",
    "JOSÉ ANTONIO MENDOZA MEJÍA",
    "ESPERANZA QUEZADA XAXNI",
    "DARIANA OLVERA MENDOZA",
    "SUSANA RUIZ REYES",
    "MISAEL LÓPEZ MACARIO",
    "LUZ MARÍA BECERRA HERNÁNDEZ",
    "KARINA ANAÍ HERNÁNDEZ SOTO",
    "SERGIO EDUARDO RUIZ ARRIAGA",
    "MARIBEL IBARRA CABRERA",
    "MARÍA ANDREA REYES ESCUDERO",
    "MAHALI VÁZQUEZ VEGA",
    "ERICK DAVID GARCÍA VILLAREAL",
    "IRMA GEORGINA CONTRERAS GARCÍA",
    "VERÓNICA SEQUEIRA MONZALVO",
    "ANA GABRIELA GUTIÉRREZ GAMERO",
    "LUIS ENRIQUE LÓPEZ FARIAS",
    "JUAN JAVIER JARAMILLO SÁNCHEZ",
    "SILVIA VÁZQUEZ OLVERA",
    "CLEMENCIA CORTÉS SÁNCHEZ",
    "KARLA SOBERANES SIERRA",
    "MIRNA YADIRA SUÁREZ ZARCO",
    "GUADALUPE TREJO SAN JUAN",
    "DENISSE MALDONADO ORTEGA",
    "IRMA FERNANDA ZUÑIGA VAZQUEZ",
    "CÉSAR ALEJANDRO GARCÍA CANDELARIA",
    "FRANCISCO JAVIER MUÑOZ ARCE",
    "IRIS DIANA GARCÍA ÁNGELES",
    "MIRIAM HERRERA HERNÁNDEZ",
    "ESTEFANI GÓMEZ COLÍN",
    "MARIELA BENÍTEZ BARRERA",
    "UZIEL DE JESÚS ZENIL SALINAS",
    "JUAN CARLOS ROQUE RAMÍREZ",
    "JESÚS OREYA MENDOZA",
    "ALMA ESTELA JIMÉNEZ PÉREZ",
    "YARELI BARRERA FERNÁNDEZ",
    "OSCAR ISIDRO ROLDÁN VARGAS",
    "DAVID ROBLES HERNÁNDEZ",
    "DAVID PEÑA SÁNCHEZ",
    "NORA SUSANA MACÍAS GARCÍA",
    "CELLY FLORA AGUILAR ALVAREZ",
    "MIRIAM MARGARITA LAGUNA LEÓN",
    "LUIS GERARDO ESPARZA CANALES",
    "BEATRIZ ISABEL VÁZQUEZ MARÍN",
    "MANUEL ENRIQUE ARANDA MONTERO",
    "PATRICIA HERNÁNDEZ LÓPEZ",
    "NOÉ CHÁVEZ SALINAS",
    "VÍCTOR HUGO GUERRERO HERNÁNDEZ",
    "VALENTÍN CERÓN PACHECO",
    "MARÍA GUADALUPE PORTILLO GARNICA",
    "CECILIA ARACELI DESTUNIS ---------",
    "OSCAR HERNÁNDEZ JIMÉNEZ",
    "MIGUEL ESNEYDER HERNÁNDEZ LUGO",
    "RAYMUNDO IVÁN GOVEA VILLANUEVA",
    "MA. JUDITH RAMÍREZ VALTIERRA",
    "ALEJANDRO ORDAZ HERRERA",
    "YESSICA YAZMÍN CALLEJAS VEGA",
    "GRINDELIA ESPINOSA FIGUEROA",
    "JOSÉ IVÁN MANZANO TAPIA",
    "WENDY NAYELI ESPINOSA HERNÁNDEZ",
    "ASUCENA VERGARA TÉLLEZ",
    "ALFONSO HAYYIM FLORES BARRERA",
    "EGLAIM DAMARIS ACOSTA VIDAL",
    "VICENTE MORALES ORTEGA",
    "ANA MARIA LARA CASTELLANOS",
    "RUTH TEODORO REYES",
    "ESTEFANIA RODRÍGUEZ CRUZ",
    "KARINA DOMÍNGUEZ FRANCO",
    "LUCERO PÉREZ MORALES",
    "FERNANDO CARBALLO CRUZ",
    "OMAR SAMUEL MEJÍA RODRÍGUEZ",
    "ARELI MAYA MONZALVO",
    "FERNANDO ESTRADA CRUZ",
    "RAÚL LOZANO SÁNCHEZ",
    "ARADI BADILLO CUELLAR",
    "CÉSAR ALONSO ÁNGELES TREJO",
    "KARLA MARITZA HUERTA GUARNEROS",
    "ADÁN MISSAEL HERNÁNDEZ GARRIDO",
    "MARÍN ÁNGELES ZAMORA",
    "MARÍA ELENA ARELLANO MÁRQUEZ",
    "KEVIN MARTÍN LEÓN PALACIOS",
    "ERICK ACOSTA TÉLLEZ",
    "LAURA RAMÍREZ CRUZ",
    "CÉSAR REYES LEÓN",
    "LAURA ESTHER RUIZ GÁLVEZ",
    "GRACIELA VÁZQUEZ MOLINA",
    "NORA AIDHÉ LUCIANO MARTÍNEZ",
    "FLOR NOCHEBUENA MANUEL GUTIÉRREZ",
    "PEDRO FERNANDO MARTÍNEZ CHONG",
    "ARTURO AGUILAR MARTÍNEZ",
    "DANIEL AUSTRIA ZENIL",
    "ITZIA HERNÁNDEZ UREÑA",
    "ADRIANA LABRA GÓMEZ",
    "ROSA HERNÁNDEZ RODRÍGUEZ",
    "MARÍA ORQUÍDEA HERNÁNDEZ BARRERA",
    "IVÁN CRUZ SEGURA",
    "ESMERALDA VARGAS LECHUGA",
    "ESTHER GAYOSSO JOAQUÍN",
    "MARÍA DE LOURDES SÁNCHEZ PEÑA",
    "COLUMBA ORDAZ LÓPEZ",
    "MADELINA SÁNCHEZ PEÑA",
    "KARLA LUCERO VÁZQUEZ LARA",
    "LINDA YAMYLETH MENDOZA LUNA",
    "MARIBEL ORTA MEJÍA",
    "JUAN ROBERTO LAZCANO TREJO",
    "EDGAR MISSAEL MONTOYA RUBIO",
    "LIZETH VARGAS JUÁREZ",
    "ISAURO MÁRQUEZ TREJO",
    "ALFONSO FERNÁNDEZ MORENO",
    "ELIZABETH MARTÍNEZ HERNÁNDEZ",
    "TANIA YERALDIN LARA HERNÁNDEZ",
    "MARLENE JIMÉNEZ RAMÍREZ",
    "DAENA GUADALUPE ACOSTA HERNÁNDEZ",
    "REYNA BAUTISTA GRANADOS",
    "PAOLA GUERRERO ENCISO",
    "ARIADNA RAMÍREZ HERNÁNDEZ",
    "VIRIDIANA BARRAZA CORTÉZ",
    "JULIO CÉSAR GRANADOS COLMENARES",
    "ALEJANDRO SALINAS AYOTITLA",
    "ALEJANDRA CAMACHO CORONADO",
    "CÉSAR LOZANO LÓPEZ",
    "NÉSTOR MARTÍN CASTILLO VENTURA",
    "JUAN ESPINOZA ISLAS",
    "GUILLERMO AYALA PARRA",
    "JAVIER ORTIZ NOCHEBUENA",
    "LUZ JULIANA BAUTISTA DURÁN",
    "LEOPOLDO LAGARDE GONZÁLEZ",
    "MARÍA DE LA LUZ TÉLLEZ SÁNCHEZ",
    "GRISELDA YARELI GUTIÉRREZ CANO",
    "CARLOS ABUNDIO CONTRERAS GONZÁLEZ",
    "AGUSTÍN MISAEL VELÁZQUEZ MONROY",
    "AXEL ARMANDO HUERTA GUARNEROS",
    "DANNA ODEMARIS FUENTES OLGUÍN",
    "MARICELA MARTÍNEZ HERNÁNDEZ",
    "EMMA SHARAÍ MEJÍA GARCÍA",
    "EMA ROZA ROA JIMÉNEZ",
    "ANTONIO DE JESÚS CRUZ ROMERO",
    "ANA MARÍA MARTÍNEZ RUBIO",
    "CARLOS ALBERTO HERNÁNDEZ ACOSTA",
    "ÁNGEL VELASCO ROCHA",
    "MA GUADALUPE URBANO CASTILLO",
    "MARÍA DE LOS ÁNGELES PERCASTEGUI JIMÉNEZ",
    "ROSA LETICIA MUÑOZ CHÁVEZ",
    "ELIZABETH MARGARITA NOGUEZ ROMERO",
    "MARÍA SARA ORTIZ GONZÁLEZ",
    "MINERVA OLGUÍN ÁNGELES",
    "JUAN MOISÉS GÓMEZ AISPURO",
    "ARIANA SALAS LUGO",
    "MARÍA FERNANDA GUZMÁN ESCAMILLA",
    "LIZBETH CASTRO LANDAVERDE",
    "MARTHA PATRICIA BARRAGÁN GARCÍA",
    "LAURA TRINIDAD HERNÁNDEZ DÍAZ",
    "GABRIELA LETICIA MARTÍNEZ PÉREZ",
    "VICTOR HUGO PÉREZ GUATI ROJO",
    "PERLA ALELÍ BARRERA GODÍNEZ",
    "CARLOS RODRIGO ROJAS RUIZ",
    "ANA LUISA BAÑOS CASTRO",
    "MAYTHE MONSERRAT ESCARELA PÉREZ",
    "CRISTHIAN OMAR CORDERO ESTRADA",
    "JOSÉ MANUEL NORIEGA DE LUCIO",
    "ALFONSO GUDIÑO ZAMORA",
    "SANDRA LIZBETH HERNÁNDEZ GARCÍA",
    "ADRIANA ÁVILA FLORES",
    "ARELY LÓPEZ VARGAS",
    "ANA BRISNA CERVANTES HIDALGO",
    "JULIO GIEZI HERNÁNDEZ GRAJEDA",
    "EIRENE LÓPEZ APARICIO",
    "MARY CARMEN LÓPEZ HERNÁNDEZ",
    "RAÚL URIEL OLIVARES RÍOS",
    "JUANITA CHÁVEZ PÉREZ",
    "LIZETH VIDAL CANO",
    "CARLOS CHARGOY RODRÍGUEZ",
    "VIANEY CRISTINA SOLARES MORENO",
    "SUSANA JIMÉNEZ HERNÁNDEZ",
    "FRANCISCO REYES VÁZQUEZ",
    "ABRIL HERNÁNDEZ GUERRERO",
    "LUZ MARÍA LUQUE GÓMEZ",
    "MARÍA ELENA TELLO SÁNCHEZ",
    "MISAEL GUTIÉRREZ ISLAS",
    "ERNESTO MARTÍNEZ AGUILAR",
    "GABRIELA HERNÁNDEZ BUSTOS",
    "JUAN ÁNGEL AGUILAR MENDOZA",
    "GARDENIA CRUZ ESCUDERO",
    "ROBERTO CARLOS LÓPEZ ESTRADA",
    "SARABI VALENTINA DÍAZ TÉLLEZ GIRÓN",
    "JORGE MIGUEL GARCÍA VÁZQUEZ",
    "MARIBEL MOLINA HERNÁNDEZ",
    "ABADI JOSEFINA JURADO GARNICA",
    "ERICK ESPINOSA LORENZO",
    "ROSA MARÍA PÉREZ GARCÍA",
    "KARLA PAOLA MÉNDEZ MORALES",
    "JOSÉ LUIS GONZÁLEZ MARTÍINEZ",
    "IVÁN MERA CURIEL",
    "FRANCISCA HERNÁNDEZ MONROY",
    "SERGIO YAMIR BALDERAS BAUTISTA",
    "LILIANA YAZMIN FRANCO CASTRO",
    "XIMENA NAVA ESCAMILLA",
    "MANUEL ALEJANDRO HERNÁNDEZ RIVERA",
    "SERGIO VERGARA FLORES",
    "SCARLETT OLGUÍN RODRÍGUEZ",
    "AURELIA PATRICIA CASTAÑEDA MONTER",
    "DANIELA PELCASTRE HERNÁNDEZ",
    "ÁNGEL VLADIMIR SÁNCHEZ GARCÍA",
    "PEDRO FUENTES AGUILAR",
    "CARLOS ALEJANDRO SOTO GÓMEZ",
    "MARÍA DE LA LUZ ESPINOSA HERNÁNDEZ",
    "JUANA GUADALUPE HERNÁNDEZ ESPITIA",
    "SAÚL PÉREZ LÓPEZ",
]

LISTA_AVALA = [
    "ING. ARIANA SALAS LUGO",
    "ING. DAVID ROBLES HERNANDEZ",
    "ING. JUAN ANGEL AGULAR MENDOZA",
    "L.A.P. JORGE MIGUEL GARCIA VAZQUEZ",
    "LD. LUIS ENRIQUE LOPEZ FARIAS",
    "LIC. ANA KAREN CERON MARTINEZ",
    "LIC. ARELI MAYA MONZALVO",
    "LIC. JULIO CESAR GONZALEZ GARCIA",
    "LIC. KARLA SOBERANES SIERRA",
    "LIC. LIZETH VIDAL CANO",
    "LIC. LUIS GERARDO MALDONADO REYES",
    "LIC. LUZ MARIA LUQUE GOMEZ",
    "LIC. MA. GUADALUPE PINEDA GONZALEZ",
    "LIC. MANUEL ALEJANDRO HERNANDEZ RIVERA",
    "LIC. MANUEL ENRIQUE ARANDA MONTERO",
    "LIC. MARIELA BENITEZ BARRERA",
    "LIC. MARLEN ELVA ARISTA AMADOR",
    "LIC. NORA AIDHE LUCIANO MARTINEZ",
    "LIC. VICTOR HUGO PEREZ GUATI ROJO",
    "MTRA. ANA BRISNA CERVANTES HIDALGO",
    "MTRA. ROSA LETICIA MUÑOZ CHAVEZ",
    "MTRO. ALEJANDRO SALINAS AYOTITLA",
    "MTRO. ALFONSO HAYYIM FLORES BARRERA",
    "MTRO. JUAN ROBERTO LAZCANO TREJO",
    "MTRO. RICARDO GOMEZ MORENO",
]

# Base de datos única fija y exclusiva
opcion_bd = "SEBISOO.xlsx"

# Pestañas principales
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
      " conservando su estructura completa, portada y formato exacto."
  )
  if os.path.exists(opcion_bd):
    try:
      xls = pd.ExcelFile(opcion_bd)
      df_raw_view = pd.read_excel(
          opcion_bd, sheet_name=xls.sheet_names[0], header=None, dtype=str
      )
      df_raw_view = df_raw_view.fillna("")
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

  @st.cache_data(ttl=1)
  def cargar_datos(archivo):
    if os.path.exists(archivo):
      try:
        xls = pd.ExcelFile(archivo)
        df = pd.read_excel(archivo, sheet_name=xls.sheet_names[0], header=None)
        
        header_idx = 29
        for idx, row in df.iterrows():
          row_str = str(row.values).lower()
          if "inventario" in row_str and "no" in row_str:
            header_idx = idx
            break

        df = pd.read_excel(
            archivo, sheet_name=xls.sheet_names[0], header=header_idx, dtype=str
        )
        df = df.dropna(
            subset=[col for col in df.columns if "Inventario" in str(col)]
        ).reset_index(drop=True)

        # Mapeo y estandarización limpia de columnas exactas
        renombres = {}
        for col in df.columns:
          c_lower = str(col).lower().strip()
          if "no." in c_lower and "inventario" not in c_lower:
            renombres[col] = "NO."
          elif "inventario" in c_lower:
            renombres[col] = "INVENTARIO"
          elif "nombre" in c_lower and "usuario" not in c_lower and "servidor" not in c_lower:
            renombres[col] = "DESCRIPCION"
          elif "marc" in c_lower:
            renombres[col] = "MARCA"
          elif "modelo" in c_lower:
            renombres[col] = "MODELO"
          elif "serie" in c_lower:
            renombres[col] = "SERIE"
          elif "descripción" in c_lower or "caracteristicas" in c_lower:
            renombres[col] = "CARACTERISTICAS"

        df.rename(columns=renombres, inplace=True)
        df = df.loc[:, ~df.columns.duplicated()]
        df = df.loc[:, ~df.columns.astype(str).str.contains("^Unnamed", case=False)]

        if "AREA" not in df.columns:
          df["AREA"] = "DIRECCIÓN DE RECURSOS MATERIALES"
        if "NOMBRE DEL USUARIO" not in df.columns:
          df["NOMBRE DEL USUARIO"] = ""
        if "OBSERVACIONES" in df.columns and "OBSERVACION" not in df.columns:
          df.rename(columns={"OBSERVACIONES": "OBSERVACION"}, inplace=True)
        if "OBSERVACION" not in df.columns:
          df["OBSERVACION"] = ""

        # Selección estricta y ordenada de columnas visibles en la app
        columnas_deseadas = [
            "NO.",
            "INVENTARIO",
            "DESCRIPCION",
            "MARCA",
            "MODELO",
            "SERIE",
            "CARACTERISTICAS",
            "AREA",
            "NOMBRE DEL USUARIO",
            "OBSERVACION",
        ]
        for c in columnas_deseadas:
          if c not in df.columns:
            df[c] = ""
            
        df = df[[c for c in columnas_deseadas if c in df.columns]]

        return df.fillna("")
      except Exception as e:
        st.error(f"Error al leer el archivo {archivo}: {e}")
        return pd.DataFrame()
    else:
      return pd.DataFrame()

  df = cargar_datos(opcion_bd)

  if not df.empty:
    columna_area = "AREA" if "AREA" in df.columns else df.columns[0]

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
          nuevo_inv = st.text_input("Inventario")
          nuevo_desc = st.text_input("Descripción", "SILLA PLEGABLE")
          nuevo_marca = st.text_input("Marca", "SIN MARCA")
        with c2:
          nuevo_modelo = st.text_input("Modelo", "SIN MODELO")
          nuevo_serie = st.text_input("Serie", "S/S")
          nuevo_carac = st.text_input(
              "Características", "REFORZADA CON ASIENTO Y RESPALDO"
          )
        with c3:
          nuevo_usuario = st.selectbox(
              "Nombre del Servidor Público / Usuario", LISTA_RESPONSABLES
          )
          nueva_area_reg = st.selectbox("Área de Adscripción", todas_las_areas)
          nuevo_obs = st.text_input("Observaciones", "")

        btn_agregar = st.form_submit_button("Guardar Bien en la Base de Datos")

        if btn_agregar:
          nuevo_registro = {
              "NO.": len(df) + 1,
              "INVENTARIO": str(nuevo_inv),
              "DESCRIPCION": str(nuevo_desc),
              "MARCA": str(nuevo_marca),
              "MODELO": str(nuevo_modelo),
              "SERIE": str(nuevo_serie),
              "CARACTERISTICAS": str(nuevo_carac),
              "AREA": str(nueva_area_reg),
              "NOMBRE DEL USUARIO": str(nuevo_usuario),
              "OBSERVACION": str(nuevo_obs),
          }
          df_nuevo_row = pd.DataFrame([nuevo_registro])
          for col in df.columns:
            if col not in df_nuevo_row.columns:
              df_nuevo_row[col] = ""

          df = pd.concat(
              [df, df_nuevo_row[df.columns]], ignore_index=True
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
        df.update(df_editado.astype(str))
        df.to_excel(opcion_bd, index=False)
        st.success("¡Cambios guardados en el archivo de Excel con éxito!")
      except Exception as e:
        st.error(f"Error al guardar: {e}")

    # --- 5. GENERACIÓN DEL PDF EXCLUSIVO DEL ÁREA (SIN OBSERVACIONES) ---
    st.markdown("---")
    st.subheader("📄 Generación de Resguardo PDF Exclusivo de esta Área")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
      firmante_responsable = st.selectbox(
          "Selecciona la Firma del Servidor Público Responsable:",
          LISTA_RESPONSABLES,
      )
    with col_f2:
      firmante_avala = st.selectbox("Selecciona quién AVALA:", LISTA_AVALA)

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
            pdf.image("BIENESTAR8.png", x=10, y=8, w=62)

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

          # Columnas del PDF (Sin Observación)
          headers = [
              "No.",
              "INVENTARIO",
              "DESCRIPCION",
              "MARCA",
              "MODELO",
              "SERIE",
              "CARACTERISTICAS",
              "NOMBRE DEL USUARIO",
          ]
          widths = [8, 28, 45, 20, 20, 15, 60, 61]  # Ancho total exacto = 257 mm

          pdf.set_font("Arial", "B", 6.5)
          for i, h in enumerate(headers):
            pdf.cell(widths[i], 5, h, 1, 0, "C")
          pdf.ln()

          pdf.set_font("Arial", "", 6)
          for idx, (_, row) in enumerate(df_editado.iterrows(), start=1):
            inv_val = str(row.get("INVENTARIO", ""))
            desc_val = str(row.get("DESCRIPCION", ""))
            marca_val = str(row.get("MARCA", "SIN MARCA"))
            modelo_val = str(row.get("MODELO", "SIN MODELO"))
            serie_val = str(row.get("SERIE", "S/S"))
            carac_val = str(row.get("CARACTERISTICAS", ""))
            usu_val = str(row.get("NOMBRE DEL USUARIO", ""))

            cell_data = [
                str(idx),
                inv_val,
                desc_val,
                marca_val,
                modelo_val,
                serie_val,
                carac_val,
                usu_val,
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

          # Cuadros de Firmas (con nombres impresos)
          y_firma = pdf.get_y()
          pdf.rect(10, y_firma, 85, 20)
          pdf.rect(98, y_firma, 85, 20)
          pdf.rect(186, y_firma, 84, 20)

          # 1. Títulos en la parte superior de cada recuadro
          pdf.set_font("Arial", "B", 5.5)
          pdf.set_xy(10, y_firma + 2)
          pdf.cell(85, 3, "FIRMA DEL SERVIDOR PÚBLICO RESPONSABLE", 0, 0, "C")
          pdf.set_xy(98, y_firma + 2)
          pdf.cell(85, 3, "AVALA", 0, 0, "C")
          pdf.set_xy(186, y_firma + 2)
          pdf.cell(84, 3, "Vo.Bo.", 0, 1, "C")

          # 2. Línea divisoria de firma en medio
          pdf.set_font("Arial", "", 6)
          pdf.set_xy(15, y_firma + 9)
          pdf.cell(75, 2, "_" * 45, 0, 0, "C")
          pdf.set_xy(103, y_firma + 9)
          pdf.cell(75, 2, "_" * 45, 0, 0, "C")
          pdf.set_xy(191, y_firma + 9)
          pdf.cell(74, 2, "_" * 45, 0, 1, "C")

          # 3. Nombres en la parte inferior de los recuadros
          pdf.set_font("Arial", "B", 5.5)
          pdf.set_xy(10, y_firma + 13)
          pdf.cell(85, 3, firmante_responsable, 0, 0, "C")
          pdf.set_xy(98, y_firma + 13)
          pdf.cell(85, 3, firmante_avala, 0, 0, "C")
          pdf.set_xy(186, y_firma + 13)
          pdf.cell(84, 3, "MTRA. ROSA LETICIA MUÑOZ CHAVEZ", 0, 1, "C")

          # Cargo institucional inferior exclusivo del Vo.Bo.
          pdf.set_font("Arial", "", 5)
          pdf.set_xy(186, y_firma + 16.5)
          pdf.cell(84, 3, "COORDINADORA ADMINISTRATIVA", 0, 1, "C")

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
    st.warning("No se encontraron registros válidos en la base de datos.")