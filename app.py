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

# --- DICCIONARIO DE LOS 18 BIENES Y SUS DESCRIPCIONES COMPLETAS ---
CATALOGO_BIENES_DESCRIPCIONES = {
    "SILLA PARA ANALISTA BRAZO COMPLETO": "Color: negro. Descripción: Respaldo en polipropileno, tapizado en malla, con soporte lumbar, asiento con espuma tapizado en tela, base de nylon con ruedas, respaldo de 0.42 metros de altura (+- 3 centímetros), mecanismo de palanca para activar pistón y bloqueo de reclinamiento.",
    "SILLA EJECUTIVA NEGRA": "Color: negro. Descripción: Asiento tapizado en tela color negro, respaldo ergonómico en malla e incluye un soporte lumbar ajustable tanto en altura como en profundidad, base en nylon, con 5 ruedas. Respaldo con altura de 0.53 metros (+- 3 centímetros). Mecanismo de palanca para activar el pistón y bloquear el reclinamiento. Pistón con rebosador de base; brazos de polipropileno con ajuste de altura. Cabecera tapizada en malla y ajustable en altura y ángulo.",
    "SILLA EJECUTIVA GRIS": "Color: Gris con negro Descripción: Cabecera ajustable, respaldo alto tapizado en malla gris, inclinacion y soporte lumbar ajustable, asiento ajustable, tapizado en tela gris, base de aluminio y 5 ruedas. Mecanismo  con perillas de autoequilibrio y ajuste de tension, palancas para ajuste de altura, ajuste de reclinamiento, brazos con altura ajustable y coderas de poliurertano con ajustes de apertura.",
    "SILLA PARA ANALISTA BRAZO AJUSTABLE": "Color: negro. Descripción: respaldo tapizado en malla con almohadilla lumbar, asiento de espuma estándar tapizado en tela, base de nylon con 5 ruedas, Respaldo con una altura de 0.50 metros (+- 3 centímetros). Mecanismo ajustable de altura y bloqueo de reclinamiento, brazos de polipropileno sujetos al respaldo, ajustables en posición vertical como opción para ocultarlos.",
    "BANCA DE RECEPCION": "Color gris. Medidas: 1.75 metros de largo por 0.47 metros de ancho,por 0.78 metros de altura(+-3 centimetros en todas las medidas). Descripcion: De 3 plazas, asiento  y respaldo en ujna sola pieza, de lamina de acero  calibre 14 multiperforada con diseño ergonomico y pintura color gris con doblez en los extremos y esquinas para evitar filos. Estructura: Con soportes laterales, trabe horizontal inferior para  soportar los asientos, fabricada en perfil de acero con placas soldadas para atornillar los soportes del asiento y terminada en pintura color gris. Patas y brazos: Laterales fabricados en lamina y soldadura con acabado cromo, con soporte para recibir los extremos de la trabe sin tornillos visibles.",
    "ARCHIVERO": "Color: beige. Medidas: 0.40 metros de ancho por 0.53 metros de fondo por 0.57 metros de alto (+- 3 centímetros en todas las medidas). Descripción: Metálico de 3 gavetas en lámina calibre 22, corredera embalinada reforzada, con chapa general, 4 ruedas, jaladera troquelada y acabado en pintura color beige.",
    "ARCHIVERO 4 GAVETAS": "Color: beige. Medidas: 1.32 metros de alto x 0.46 metros de ancho x 0.60 metros de fondo (+- 3 centímetros en todas las medidas). Descripción: De 4 gavetas, fabricado en lámina calibre 22, corredera embalinada reforzada, con chapa general, jaladera troquelada y acabado en pintura color beige.",
    "ESCRITORIO RECTO": "Color: café, negro. Medidas: 1.20 metros de largo por 0.60 metros de ancho por 0.75 metros de alto (+- 3 centímetros en todas las medidas). Descripción: Con cubierta de melamina color café con agujero para cableado, estructura color negro totalmente en acero tubular cuadrado de 2\" calibre 18, refuerzo superior en perfil tubular rectangular en calibre 18. En la parte inferior de las 4 patas incluye 4 niveladores de plástico rígido en color negro.",
    "ESCRITORIO EN L 1.50": "Color: café, negro. Medidas: 0.90 metros de largo por 0.50 metros de ancho por 0.75 metros de alto más 1.50 metros de largo por 0.70 metros de ancho por 0.75 metros de alto (+- 3 centímetros en todas las medidas). Descripción: Escritorio con cubierta de melamina color café con agujero para cableado, estructura cuadrada de 2\" calibre 18 color negro, en la parte inferior de las patas incluye niveladores de plástico rígido en color negro.",
    "ESCRITORIO EN L 1.80": "Color: café, negro. Medidas: 1.80 metros de largo por 0.70 metros de ancho por 0.75 metros de alto más 1 metro de largo por 0.45 metros de ancho por 0.75 metros de alto (+- 3 centímetros en todas las medidas). Descripción: Escritorio con cubierta de melamina color café con agujero para cableado, estructura cuadrada de 2\" calibre 18 color negro, en la parte inferior de las patas incluye niveladores de plástico rígido en color negro.",
    "CREDENZA": "Color: café. Medidas: 1.60 metros de largo por 0.46 metros de ancho por 0.73 metros de alto (+- 3 centímetros en todas las medidas). Descripción: De 2 módulos color café, de MDF laminado de 15 milímetros, 2 puertas abatibles con jaladeras metálicas y chapa de seguridad general, 2 repisa divisora en acabado bilaminado. Regatones niveladores de color negro.",
    "MESA DE JUNTAS 3.20": "Color: café, negro. Medidas: 3.20 metros de largo por 1.20 metros de ancho por 0.75 metros de alto (+- 3 centímetros en todas las medidas). Descripción: Estructura metálica color negro, cubierta laminada color café de 30 milimetros, resistente a rayones, refuerzo superior en perfil tubular rectangular de 3\" en calibre 18.",
    "MODULO DE RECEPCION 2.40": "Color: café. Medidas: 2.4 metros de largo por 1.10 metros de alto por 0.60 metros de ancho (+- 3 centímetros en todas las medidas). Descripción: MDF laminado de 18 milímetros, color café, niveladores de polipropileno color negro, cuenta con 1 pedestal mixto, que incluye un cajón archivero y un cajón papelero, con vista de aluminio.",
    "MODULO DE RECEPCION 1.80": "Color: café. Medidas: 1.80 metros de largo por 0.60 metros ancho de  por 1.10 metros de alto  (+- 3 centímetros en todas las medidas). Descripción: MDF laminado de 18 milímetros color café, niveladores de polipropileno color negro, cuenta con 1 pedestal mixto, que incluye un cajón archivero y un cajón papelero, con vista de aluminio brillante color natural.",
    "ESTANTE": "Color: gris. Medidas: 2.10 metros de altura por 0.85 metros de largo por 0.30 metros de ancho (+- 3 centímetros en todas las medidas). Descripción: Tipo esqueleto, con 4 postes metálicos de 2.10 metros en calibre 18 perforados y 5 charolas de 0.85 metros por 0.30 metros en calibre 24, con tornillería para su armado y acabado en pintura color gris.",
    "MESA CIRCULAR": "Color: café. Medidas: 1 metro de diámetro por 0.75 metros de altura (+- 3 centímetros en todas las medidas). Descripción: En cubierta de melamina color café, base en forma de cruz con niveladores de polipropileno color negro",
    "SILLA PERIQUERA": "Color: negro. Medidas: 1.06 metros de alto por 0.36 metros de ancho por 0.36 metros de largo (+- 3 centímetros en todas las medidas) Descripción: asiento tapizado en vinil en tubo cuadrado de 1” calibre 18 y refuerzos en tubo cuadrado de 3/4” color negro, cuenta con 3 soleras en el respaldo para mayor comodidad.",
    "SILLON": "Color: gris. Medidas: 1.93 metros de largo por 0.81 metros de ancho por 0.81 metros de alto (+- 3 centímetros en todas las medidas). Descripción: De 3 plazas, tapizado en tela gris, asientos de espuma."
}

# --- CATÁLOGO MAESTRO DE ÁREAS INSTITUCIONALES ---
AREAS_MAESTRAS = [
    "DIRECCION DE GESTION INSTITUCIONAL", "ÓRGANO INTERNO DE CONTROL", 
    "DIRECCIÓN GENERAL DE ASISTENCIA, ATENCIÓN Y PROTECCIÓN", "SUBSECRETARÍA DE INCLUSIÓN Y DESARROLLO", 
    "DIRECCIÓN GENERAL DE PROSPECTIVA, PLANEACIÓN Y EVALUACIÓN DE LOS PROGRAMAS SOCIALES", 
    "DIRECCIÓN GENERAL DE OPERACIÓN Y LOGÍSTICA DE PROGRAMAS", "COORDINACIÓN ADMINISTRATIVA", 
    "SUBDIRECCIÓN DE INTEGRACIÓN Y CONTROL DE INFORMACIÓN", "DIRECCIÓN DE RECURSOS FINANCIEROS", 
    "DIRECCIÓN DE RECURSOS HUMANOS", "DIRECCIÓN DE CONTROL Y SEGUIMIENTO DE AUDITORÍA", 
    "SUBSECRETARÍA DE PARTICIPACIÓN SOCIAL Y FOMENTO ARTESANAL", "DIRECCIÓN GENERAL DE FOMENTO ARTESANAL", 
    "SUBSECRETARÍA DE DESARROLLO SOCIAL Y HUMANO", "DIRECCIÓN GENERAL DE ATENCIÓN AL MIGRANTE", 
    "DIRECCIÓN GENERAL DE INCLUSIÓN PARA LAS PERSONAS CON DISCAPACIDAD", "DIRECCIÓN DE RECURSOS MATERIALES", 
    "DIRECCIÓN GENERAL DE SERVIDORES DEL PUEBLO", "CONTACT CENTER", 
    "DIRECCIÓN DE SUBSIDIO AL SERVICIO DE VERIFICACIÓN VEHICULAR"
]

LISTA_RESPONSABLES = [
    "RICARDO GÓMEZ MORENO", "MARLEN ELVA ARISTA AMADOR", "JOSUÉ RAYMUNDO SÁNCHEZ ÁVALOS",
    "PAUL GIOVANNI SÁNCHEZ NIETO", "JUAN ALEXIS GARCÍA GARCÍA", "DIANA LAURA FERNÁNDEZ MONROY",
    "JORGE ALBERTO VARGAS ROMERO", "EMMANUEL HUERTA MONZALVO", "DIVANI SHAIRENE CARDOSO LARA",
    "JOSÉ ANTONIO MENDOZA MEJÍA", "ESPERANZA QUEZADA XAXNI", "DARIANA OLVERA MENDOZA",
    "SUSANA RUIZ REYES", "MISAEL LÓPEZ MACARIO", "LUZ MARÍA BECERRA HERNÁNDEZ",
    "KARINA ANAÍ HERNÁNDEZ SOTO", "SERGIO EDUARDO RUIZ ARRIAGA", "MARIBEL IBARRA CABRERA",
    "MARÍA ANDREA REYES ESCUDERO", "MAHALI VÁZQUEZ VEGA", "ERICK DAVID GARCÍA VILLAREAL",
    "IRMA GEORGINA CONTRERAS GARCÍA", "VERÓNICA SEQUEIRA MONZALVO", "ANA GABRIELA GUTIÉRREZ GAMERO",
    "LUIS ENRIQUE LÓPEZ FARIAS", "JUAN JAVIER JARAMILLO SÁNCHEZ", "SILVIA VÁZQUEZ OLVERA",
    "CLEMENCIA CORTÉS SÁNCHEZ", "KARLA SOBERANES SIERRA", "MIRNA YADIRA SUÁREZ ZARCO",
    "GUADALUPE TREJO SAN JUAN", "DENISSE MALDONADO ORTEGA", "IRMA FERNANDA ZUÑIGA VAZQUEZ",
    "CÉSAR ALEJANDRO GARCÍA CANDELARIA", "FRANCISCO JAVIER MUÑOZ ARCE", "IRIS DIANA GARCÍA ÁNGELES",
    "MIRIAM HERRERA HERNÁNDEZ", "ESTEFANI GÓMEZ COLÍN", "MARIELA BENÍTEZ BARRERA",
    "UZIEL DE JESÚS ZENIL SALINAS", "JUAN CARLOS ROQUE RAMÍREZ", "JESÚS OREYA MENDOZA",
    "ALMA ESTELA JIMÉNEZ PÉREZ", "YARELI BARRERA FERNÁNDEZ", "OSCAR ISIDRO ROLDÁN VARGAS",
    "DAVID ROBLES HERNÁNDEZ", "DAVID PEÑA SÁNCHEZ", "NORA SUSANA MACÍAS GARCÍA",
    "CELLY FLORA AGUILAR ALVAREZ", "MIRIAM MARGARITA LAGUNA LEÓN", "LUIS GERARDO ESPARZA CANALES",
    "BEATRIZ ISABEL VÁZQUEZ MARÍN", "MANUEL ENRIQUE ARANDA MONTERO", "PATRICIA HERNÁNDEZ LÓPEZ",
    "NOÉ CHÁVEZ SALINAS", "VÍCTOR HUGO GUERRERO HERNÁNDEZ", "VALENTÍN CERÓN PACHECO",
    "MARÍA GUADALUPE PORTILLO GARNICA", "CECILIA ARACELI DESTUNIS ---------", "OSCAR HERNÁNDEZ JIMÉNEZ",
    "MIGUEL ESNEYDER HERNÁNDEZ LUGO", "RAYMUNDO IVÁN GOVEA VILLANUEVA", "MA. JUDITH RAMÍREZ VALTIERRA",
    "ALEJANDRO ORDAZ HERRERA", "YESSICA YAZMÍN CALLEJAS VEGA", "GRINDELIA ESPINOSA FIGUEROA",
    "JOSÉ IVÁN MANZANO TAPIA", "WENDY NAYELI ESPINOSA HERNÁNDEZ", "ASUCENA VERGARA TÉLLEZ",
    "ALFONSO HAYYIM FLORES BARRERA", "EGLAIM DAMARIS ACOSTA VIDAL", "VICENTE MORALES ORTEGA",
    "ANA MARIA LARA CASTELLANOS", "RUTH TEODORO REYES", "ESTEFANIA RODRÍGUEZ CRUZ",
    "KARINA DOMÍNGUEZ FRANCO", "LUCERO PÉREZ MORALES", "FERNANDO CARBALLO CRUZ",
    "OMAR SAMUEL MEJÍA RODRÍGUEZ", "ARELI MAYA MONZALVO", "FERNANDO ESTRADA CRUZ",
    "RAÚL LOZANO SÁNCHEZ", "ARADI BADILLO CUELLAR", "CÉSAR ALONSO ÁNGELES TREJO",
    "KARLA MARITZA HUERTA GUARNEROS", "ADÁN MISSAEL HERNÁNDEZ GARRIDO", "MARÍN ÁNGELES ZAMORA",
    "MARÍA ELENA ARELLANO MÁRQUEZ", "KEVIN MARTÍN LEÓN PALACIOS", "ERICK ACOSTA TÉLLEZ",
    "LAURA RAMÍREZ CRUZ", "CÉSAR REYES LEÓN", "LAURA ESTHER RUIZ GÁLVEZ",
    "GRACIELA VÁZQUEZ MOLINA", "NORA AIDHÉ LUCIANO MARTÍNEZ", "FLOR NOCHEBUENA MANUEL GUTIÉRREZ",
    "PEDRO FERNANDO MARTÍNEZ CHONG", "ARTURO AGUILAR MARTÍNEZ", "DANIEL AUSTRIA ZENIL",
    "ITZIA HERNÁNDEZ UREÑA", "ADRIANA LABRA GÓMEZ", "ROSA HERNÁNDEZ RODRÍGUEZ",
    "MARÍA ORQUÍDEA HERNÁNDEZ BARRERA", "IVÁN CRUZ SEGURA", "ESMERALDA VARGAS LECHUGA",
    "ESTHER GAYOSSO JOAQUÍN", "MARÍA DE LOURDES SÁNCHEZ PEÑA", "COLUMBA ORDAZ LÓPEZ",
    "MADELINA SÁNCHEZ PEÑA", "KARLA LUCERO VÁZQUEZ LARA", "LINDA YAMYLETH MENDOZA LUNA",
    "MARIBEL ORTA MEJÍA", "JUAN ROBERTO LAZCANO TREJO", "EDGAR MISSAEL MONTOYA RUBIO",
    "LIZETH VARGAS JUÁREZ", "ISAURO MÁRQUEZ TREJO", "ALFONSO FERNÁNDEZ MORENO",
    "ELIZABETH MARTÍNEZ HERNÁNDEZ", "TANIA YERALDIN LARA HERNÁNDEZ", "MARLENE JIMÉNEZ RAMÍREZ",
    "DAENA GUADALUPE ACOSTA HERNÁNDEZ", "REYNA BAUTISTA GRANADOS", "PAOLA GUERRERO ENCISO",
    "ARIADNA RAMÍREZ HERNÁNDEZ", "VIRIDIANA BARRAZA CORTÉZ", "JULIO CÉSAR GRANADOS COLMENARES",
    "ALEJANDRO SALINAS AYOTITLA", "ALEJANDRA CAMACHO CORONADO", "CÉSAR LOZANO LÓPEZ",
    "NÉSTOR MARTÍN CASTILLO VENTURA", "JUAN ESPINOZA ISLAS", "GUILLERMO AYALA PARRA",
    "JAVIER ORTIZ NOCHEBUENA", "LUZ JULIANA BAUTISTA DURÁN", "LEOPOLDO LAGARDE GONZÁLEZ",
    "MARÍA DE LA LUZ TÉLLEZ SÁNCHEZ", "GRISELDA YARELI GUTIÉRREZ CANO", "CARLOS ABUNDIO CONTRERAS GONZÁLEZ",
    "AGUSTÍN MISAEL VELÁZQUEZ MONROY", "AXEL ARMANDO HUERTA GUARNEROS", "DANNA ODEMARIS FUENTES OLGUÍN",
    "MARICELA MARTÍNEZ HERNÁNDEZ", "EMMA SHARAÍ MEJÍA GARCÍA", "EMA ROZA ROA JIMÉNEZ",
    "ANTONIO DE JESÚS CRUZ ROMERO", "ANA MARÍA MARTÍNEZ RUBIO", "CARLOS ALBERTO HERNÁNDEZ ACOSTA",
    "ÁNGEL VELASCO ROCHA", "MA GUADALUPE URBANO CASTILLO", "MARÍA DE LOS ÁNGELES PERCASTEGUI JIMÉNEZ",
    "ROSA LETICIA MUÑOZ CHÁVEZ", "ELIZABETH MARGARITA NOGUEZ ROMERO", "MARÍA SARA ORTIZ GONZÁLEZ",
    "MINERVA OLGUÍN ÁNGELES", "JUAN MOISÉS GÓMEZ AISPURO", "ARIANA SALAS LUGO",
    "MARÍA FERNANDA GUZMÁN ESCAMILLA", "LIZBETH CASTRO LANDAVERDE", "MARTHA PATRICIA BARRAGÁN GARCÍA",
    "LAURA TRINIDAD HERNÁNDEZ DÍAZ", "GABRIELA LETICIA MARTÍNEZ PÉREZ", "VICTOR HUGO PÉREZ GUATI ROJO",
    "PERLA ALELÍ BARRERA GODÍNEZ", "CARLOS RODRIGO ROJAS RUIZ", "ANA LUISA BAÑOS CASTRO",
    "MAYTHE MONSERRAT ESCARELA PÉREZ", "CRISTHIAN OMAR CORDERO ESTRADA", "JOSÉ MANUEL NORIEGA DE LUCIO",
    "ALFONSO GUDIÑO ZAMORA", "SANDRA LIZBETH HERNÁNDEZ GARCÍA", "ADRIANA ÁVILA FLORES",
    "ARELY LÓPEZ VARGAS", "ANA BRISNA CERVANTES HIDALGO", "JULIO GIEZI HERNÁNDEZ GRAJEDA",
    "EIRENE LÓPEZ APARICIO", "MARY CARMEN LÓPEZ HERNÁNDEZ", "RAÚL URIEL OLIVARES RÍOS",
    "JUANITA CHÁVEZ PÉREZ", "LIZETH VIDAL CANO", "CARLOS CHARGOY RODRÍGUEZ",
    "VIANEY CRISTINA SOLARES MORENO", "SUSANA JIMÉNEZ HERNÁNDEZ", "FRANCISCO REYES VÁZQUEZ",
    "ABRIL HERNÁNDEZ GUERRERO", "LUZ MARÍA LUQUE GÓMEZ", "MARÍA ELENA TELLO SÁNCHEZ",
    "MISAEL GUTIÉRREZ ISLAS", "ERNESTO MARTÍNEZ AGUILAR", "GABRIELA HERNÁNDEZ BUSTOS",
    "JUAN ÁNGEL AGUILAR MENDOZA", "GARDENIA CRUZ ESCUDERO", "ROBERTO CARLOS LÓPEZ ESTRADA",
    "SARABI VALENTINA DÍAZ TÉLLEZ GIRÓN", "JORGE MIGUEL GARCÍA VÁZQUEZ", "MARIBEL MOLINA HERNÁNDEZ",
    "ABADI JOSEFINA JURADO GARNICA", "ERICK ESPINOSA LORENZO", "ROSA MARÍA PÉREZ GARCÍA",
    "KARLA PAOLA MÉNDEZ MORALES", "JOSÉ LUIS GONZÁLEZ MARTÍINEZ", "IVÁN MERA CURIEL",
    "FRANCISCA HERNÁNDEZ MONROY", "SERGIO YAMIR BALDERAS BAUTISTA", "LILIANA YAZMIN FRANCO CASTRO",
    "XIMENA NAVA ESCAMILLA", "MANUEL ALEJANDRO HERNÁNDEZ RIVERA", "SERGIO VERGARA FLORES",
    "SCARLETT OLGUÍN RODRÍGUEZ", "AURELIA PATRICIA CASTAÑEDA MONTER", "DANIELA PELCASTRE HERNÁNDEZ",
    "ÁNGEL VLADIMIR SÁNCHEZ GARCÍA", "PEDRO FUENTES AGUILAR", "CARLOS ALEJANDRO SOTO GÓMEZ",
    "MARÍA DE LA LUZ ESPINOSA HERNÁNDEZ", "JUANA GUADALUPE HERNÁNDEZ ESPITIA", "SAÚL PÉREZ LÓPEZ"
]

LISTA_AVALA = [
    "ING. ARIANA SALAS LUGO", "ING. DAVID ROBLES HERNANDEZ", "ING. JUAN ANGEL AGULAR MENDOZA",
    "L.A.P. JORGE MIGUEL GARCIA VAZQUEZ", "LD. LUIS ENRIQUE LOPEZ FARIAS", "LIC. ANA KAREN CERON MARTINEZ",
    "LIC. ARELI MAYA MONZALVO", "LIC. JULIO CESAR GONZALEZ GARCIA", "LIC. KARLA SOBERANES SIERRA",
    "LIC. LIZETH VIDAL CANO", "LIC. LUIS GERARDO MALDONADO REYES", "LIC. LUZ MARIA LUQUE GOMEZ",
    "LIC. MA. GUADALUPE PINEDA GONZALEZ", "LIC. MANUEL ALEJANDRO HERNANDEZ RIVERA", "LIC. MANUEL ENRIQUE ARANDA MONTERO",
    "LIC. MARIELA BENITEZ BARRERA", "LIC. MARLEN ELVA ARISTA AMADOR", "LIC. NORA AIDHE LUCIANO MARTINEZ",
    "LIC. VICTOR HUGO PEREZ GUATI ROJO", "MTRA. ANA BRISNA CERVANTES HIDALGO", "MTRA. ROSA LETICIA MUÑOZ CHAVEZ",
    "MTRO. ALEJANDRO SALINAS AYOTITLA", "MTRO. ALFONSO HAYYIM FLORES BARRERA", "MTRO. JUAN ROBERTO LAZCANO TREJO",
    "MTRO. RICARDO GOMEZ MORENO"
]

opcion_bd = "SEBISOO.xlsx"

tab_original, tab_edicion = st.tabs(
    ["📄 Vista Original Completa (Excel)", "✏️ Panel de Control y Edición"]
)

with tab_original:
  st.subheader(f"Vista íntegra del archivo original: {opcion_bd}")
  if os.path.exists(opcion_bd):
    try:
      xls = pd.ExcelFile(opcion_bd)
      df_raw_view = pd.read_excel(
          opcion_bd, sheet_name=xls.sheet_names[0], header=None, dtype=str
      ).fillna("")
      st.dataframe(df_raw_view.iloc[:, :14], use_container_width=True, height=650, hide_index=True)
    except Exception as e:
      st.error(f"Error: {e}")

with tab_edicion:
  @st.cache_data(ttl=1)
  def cargar_datos(archivo):
    if os.path.exists(archivo):
      try:
        xls = pd.ExcelFile(archivo)
        df_temp = pd.read_excel(archivo, sheet_name=xls.sheet_names[0], header=None)
        header_idx = 29
        for idx, row in df_temp.iterrows():
          if "inventario" in str(row.values).lower() and "no" in str(row.values).lower():
            header_idx = idx
            break

        df = pd.read_excel(archivo, sheet_name=xls.sheet_names[0], header=header_idx, dtype=str)
        df = df.dropna(subset=[col for col in df.columns if "Inventario" in str(col)]).reset_index(drop=True)

        renombres = {}
        for col in df.columns:
          c_lower = str(col).lower().strip()
          if "no." in c_lower and "inventario" not in c_lower: renombres[col] = "NO."
          elif "inventario" in c_lower: renombres[col] = "INVENTARIO"
          elif "nombre" in c_lower and "usuario" not in c_lower and "servidor" not in c_lower: renombres[col] = "DESCRIPCION"
          elif "marc" in c_lower: renombres[col] = "MARCA"
          elif "modelo" in c_lower: renombres[col] = "MODELO"
          elif "serie" in c_lower: renombres[col] = "SERIE"
          elif "descripción" in c_lower or "caracteristicas" in c_lower: renombres[col] = "CARACTERISTICAS"

        df.rename(columns=renombres, inplace=True)
        df = df.loc[:, ~df.columns.duplicated()]
        df = df.loc[:, ~df.columns.astype(str).str.contains("^Unnamed", case=False)]

        if "AREA" not in df.columns: df["AREA"] = "DIRECCIÓN DE RECURSOS MATERIALES"
        if "NOMBRE DEL USUARIO" not in df.columns: df["NOMBRE DEL USUARIO"] = ""
        if "OBSERVACIONES" in df.columns and "OBSERVACION" not in df.columns:
          df.rename(columns={"OBSERVACIONES": "OBSERVACION"}, inplace=True)
        if "OBSERVACION" not in df.columns: df["OBSERVACION"] = ""

        columnas_deseadas = ["NO.", "INVENTARIO", "DESCRIPCION", "MARCA", "MODELO", "SERIE", "CARACTERISTICAS", "AREA", "NOMBRE DEL USUARIO", "OBSERVACION"]
        for c in columnas_deseadas:
          if c not in df.columns: df[c] = ""
        return df[columnas_deseadas].fillna("")
      except Exception as e:
        st.error(f"Error al leer: {e}")
        return pd.DataFrame()
    return pd.DataFrame()

  df = cargar_datos(opcion_bd)

  if not df.empty:
    columna_area = "AREA"
    areas_en_archivo = df[columna_area].dropna().astype(str).str.strip().tolist()
    todas_las_areas = sorted(list(set(AREAS_MAESTRAS + areas_en_archivo)))

    st.sidebar.markdown("---")
    st.sidebar.header("🔍 Filtros de Área")
    area_seleccionada = st.sidebar.selectbox("Selecciona el Área para el Resguardo:", ["Todas"] + todas_las_areas)

    if area_seleccionada != "Todas":
      df_filtrado = df[df[columna_area].astype(str).str.strip().str.upper() == area_seleccionada.strip().upper()].copy()
    else:
      df_filtrado = df.copy()

    with st.expander("➕ Registrar Nuevo Bien / Asignar Área", expanded=False):
      st.markdown(f"Agrega un bien directamente en **{opcion_bd}**:")
      
      c1, c2, c3 = st.columns(3)
      with c1:
        nuevo_inv = st.text_input("Inventario")
        lista_nombres_bienes = list(CATALOGO_BIENES_DESCRIPCIONES.keys())
        nuevo_desc = st.selectbox("Descripción (Bien)", lista_nombres_bienes)
        nuevo_marca = st.text_input("Marca", "SIN MARCA")
      with c2:
        nuevo_modelo = st.text_input("Modelo", "SIN MODELO")
        nuevo_serie = st.text_input("Serie", "S/S")
        caracteristica_automatica = CATALOGO_BIENES_DESCRIPCIONES.get(nuevo_desc, "")
        nuevo_carac = st.text_area("Características (Automática)", value=caracteristica_automatica, height=100)
      with c3:
        nuevo_usuario = st.selectbox("Nombre del Servidor Público / Usuario", LISTA_RESPONSABLES)
        nueva_area_reg = st.selectbox("Área de Adscripción", todas_las_areas)
        nuevo_obs = st.text_input("Observaciones", "")

      if st.button("Guardar Bien en la Base de Datos", type="primary"):
        nuevo_registro = {
            "NO.": str(len(df) + 1),
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
        df = pd.concat([df, pd.DataFrame([nuevo_registro])], ignore_index=True)
        df.to_excel(opcion_bd, index=False)
        st.success("¡Bien registrado correctamente!")
        st.rerun()

    st.subheader(f"Visualizando registros de: {opcion_bd} (Área: {area_seleccionada})")
    st.markdown(f"Total de bienes en esta vista: **{len(df_filtrado)}**")

    df_editado = st.data_editor(df_filtrado, num_rows="dynamic", use_container_width=True, key="editor_principal")

    if st.button("💾 Guardar Cambios en Excel"):
      try:
        df.update(df_editado.astype(str))
        df.to_excel(opcion_bd, index=False)
        st.success("¡Cambios guardados en el archivo de Excel con éxito!")
      except Exception as e:
        st.error(f"Error al guardar: {e}")

    # --- GENERACIÓN DE PDF OPTIMIZADA (SIN ESPACIOS EN BLANCO EXCESIVOS) ---
    st.markdown("---")
    st.subheader("📄 Generación de Resguardo PDF Exclusivo de esta Área")
    col_f1, col_f2 = st.columns(2)
    with col_f1:
      firmante_responsable = st.selectbox("Firma del Servidor Público Responsable:", LISTA_RESPONSABLES)
    with col_f2:
      firmante_avala = st.selectbox("Selecciona quién AVALA:", LISTA_AVALA)

    if st.button("📥 Generar PDF de Resguardo (Solo esta Área)"):
      if area_seleccionada == "Todas":
        st.warning("Por favor selecciona un **Área específica** en la barra lateral para generar su resguardo individual.")
      else:
        try:
          pdf = FPDF(orientation="L", unit="mm", format="letter")
          pdf.set_margins(left=6, top=8, right=6)
          pdf.add_page()
          # Desactivamos el auto page break predeterminado para controlarlo nosotros con precisión
          pdf.set_auto_page_break(auto=False, margin=6)

          def imprimir_encabezado():
            if os.path.exists("BIENESTAR8.png"):
              pdf.image("BIENESTAR8.png", x=6, y=6, w=55)
            pdf.set_font("Arial", "B", 9)
            pdf.cell(0, 5, "SECRETARÍA DE BIENESTAR E INCLUSIÓN SOCIAL", 0, 1, "C")
            pdf.set_font("Arial", "B", 7.5)
            pdf.cell(0, 3.5, "COORDINACIÓN ADMINISTRATIVA", 0, 1, "C")
            pdf.cell(0, 3.5, "INVENTARIO DE BIENES MUEBLES 2026", 0, 1, "C")
            pdf.cell(0, 3.5, "RESGUARDO INDIVIDUAL INTERNO", 0, 1, "C")
            pdf.ln(2)

            fecha_hoy = datetime.now().strftime("%d/%m/%Y")
            pdf.set_font("Arial", "B", 7.5)
            pdf.cell(15, 5, "AREA:", 0, 0, "L")
            pdf.set_font("Arial", "", 7.5)
            pdf.cell(150, 5, area_seleccionada, 0, 0, "L")
            pdf.set_font("Arial", "B", 7.5)
            pdf.cell(20, 5, "FECHA:", 0, 0, "R")
            pdf.set_font("Arial", "", 7.5)
            pdf.cell(42, 5, fecha_hoy, 0, 1, "R")
            pdf.ln(1)

            # Cabecera de la tabla
            global headers, widths
            pdf.set_font("Arial", "B", 6)
            for i, h in enumerate(headers):
              pdf.cell(widths[i], 4.5, h, 1, 0, "C")
            pdf.ln()

          headers = ["No.", "INVENTARIO", "DESCRIPCION", "MARCA", "MODELO", "SERIE", "CARACTERISTICAS", "NOMBRE DEL USUARIO"]
          widths = [8, 26, 42, 18, 18, 14, 75, 66]

          imprimir_encabezado()
          pdf.set_font("Arial", "", 5.5)

          for idx, (_, row) in enumerate(df_filtrado.iterrows(), start=1):
            cell_data = [
                str(idx),
                str(row.get("INVENTARIO", "")),
                str(row.get("DESCRIPCION", "")),
                str(row.get("MARCA", "SIN MARCA")),
                str(row.get("MODELO", "SIN MODELO")),
                str(row.get("SERIE", "S/S")),
                str(row.get("CARACTERISTICAS", "")),
                str(row.get("NOMBRE DEL USUARIO", ""))
            ]

            line_h = 3.0
            max_lines = 1
            for i, text in enumerate(cell_data):
              if widths[i] > 0 and len(text) > 0:
                chars_per_line = max(4, int(widths[i] / 1.6))
                lines = max(1, int(len(text) / chars_per_line) + (1 if len(text) % chars_per_line > 0 else 0))
                if lines > max_lines: max_lines = lines

            row_height = max(4.5, max_lines * line_h + 1.0)

            # ESPACIO MÍNIMO NECESARIO ANTES DE SALTO DE PÁGINA (Tabla + Nota + Firmas = ~50mm requeridos al final)
            espacio_footer_necesario = 45
            if pdf.get_y() + row_height > (215 - espacio_footer_necesario):
              pdf.add_page()
              imprimir_encabezado()
              pdf.set_font("Arial", "", 5.5)

            x_start, y_start = pdf.get_x(), pdf.get_y()
            for i, text in enumerate(cell_data):
              current_x, current_y = pdf.get_x(), pdf.get_y()
              pdf.rect(current_x, current_y, widths[i], row_height)
              pdf.set_xy(current_x + 0.8, current_y + 0.5)
              pdf.multi_cell(widths[i] - 1.6, line_h, text, 0, "L")
              pdf.set_xy(current_x + widths[i], current_y)

            pdf.set_xy(x_start, y_start + row_height)

          # --- BLOQUE DE CIERRE (NOTA LEGAL Y FIRMAS) ---
          # Si no hay espacio suficiente para la nota y las firmas en esta página, salta limpio a una nueva
          if pdf.get_y() > 155:
            pdf.add_page()
            imprimir_encabezado()

          pdf.ln(2.5)
          pdf.set_font("Arial", "", 4.5)
          nota_legal = "CON FUNDAMENTO EN LO DISPUESTO POR LOS ARTÍCULOS 149 V EN FRACCIÓN II DE LA CONSTITUCIÓN POLÍTICA DEL ESTADO DE HIDALGO; 7 FRACCIÓN III DE LA LEY GENERAL DE RESPONSABILIDADES ADMINISTRATIVAS; 2 PÁRRAFO ÚNICO DE LA LEY ORGÁNICA DE LA ADMINISTRACIÓN PÚBLICA DEL ESTADO DE HIDALGO; 4 FRACCIÓN VI, 6 FRACCIÓN IV Y 45 SÉPTIMO Y OCTAVO PÁRRAFO DE LAS NORMAS GENERALES PARA ADMINISTRAR Y CONTROLAR LOS BIENES MUEBLES... RECIBÍ DE COMPLETA CONFORMIDAD LOS BIENES MUEBLES ANTES LISTADOS."
          
          y_nota = pdf.get_y()
          pdf.rect(6, y_nota, 267, 10)
          pdf.set_xy(7.5, y_nota + 1.0)
          pdf.multi_cell(264, 2.5, nota_legal, 0, "J")
          pdf.ln(3.5)

          y_firma = pdf.get_y()
          pdf.rect(6, y_firma, 88, 18)
          pdf.rect(95, y_firma, 88, 18)
          pdf.rect(184, y_firma, 89, 18)

          pdf.set_font("Arial", "B", 5)
          pdf.set_xy(6, y_firma + 1.5); pdf.cell(88, 2.5, "FIRMA DEL SERVIDOR PÚBLICO RESPONSABLE", 0, 0, "C")
          pdf.set_xy(95, y_firma + 1.5); pdf.cell(88, 2.5, "AVALA", 0, 0, "C")
          pdf.set_xy(184, y_firma + 1.5); pdf.cell(89, 2.5, "Vo.Bo.", 0, 1, "C")

          pdf.set_font("Arial", "", 5.5)
          pdf.set_xy(10, y_firma + 7.5); pdf.cell(80, 2, "_" * 42, 0, 0, "C")
          pdf.set_xy(99, y_firma + 7.5); pdf.cell(80, 2, "_" * 42, 0, 0, "C")
          pdf.set_xy(188, y_firma + 7.5); pdf.cell(81, 2, "_" * 42, 0, 1, "C")

          pdf.set_font("Arial", "B", 5)
          pdf.set_xy(6, y_firma + 11.0); pdf.cell(88, 2.5, firmante_responsable, 0, 0, "C")
          pdf.set_xy(95, y_firma + 11.0); pdf.cell(88, 2.5, firmante_avala, 0, 0, "C")
          pdf.set_xy(184, y_firma + 11.0); pdf.cell(89, 2.5, "MTRA. ROSA LETICIA MUÑOZ CHÁVEZ", 0, 1, "C")

          pdf.set_font("Arial", "", 4.5)
          pdf.set_xy(184, y_firma + 14.0); pdf.cell(89, 2.5, "COORDINADORA ADMINISTRATIVA", 0, 1, "C")

          output_pdf = "resguardo_area.pdf"
          pdf.output(output_pdf)

          with open(output_pdf, "rb") as f:
            st.download_button("📥 Descargar Resguardo PDF", f, file_name="Resguardo_Area.pdf", mime="application/pdf")
          st.success("¡PDF generado exitosamente!")
        except Exception as e:
          st.error(f"Error al generar PDF: {e}")