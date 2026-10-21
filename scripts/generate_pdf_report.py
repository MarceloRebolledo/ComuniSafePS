import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8.5)
        self.setFillColor(colors.HexColor("#718096"))
        
        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(46, 752, "ComuniSafe — Informe de Evaluación de Calidad con SonarQube")
            self.drawRightString(566, 752, "Arquitectura de Software")
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(46, 746, 566, 746)
            
        # Footer
        page_text = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(566, 32, page_text)
        self.drawString(46, 32, "Universidad de La Frontera · Octubre 2026")
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(46, 42, 566, 42)
        self.restoreState()

def create_report(output_filename="Reporte_Calidad_SonarQube_ComuniSafe.pdf"):
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        leftMargin=46,
        rightMargin=46,
        topMargin=46,
        bottomMargin=46
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=6
    )
    h1_style = ParagraphStyle(
        'H1',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=8,
        spaceAfter=5,
        keepWithNext=True
    )
    h2_style = ParagraphStyle(
        'H2',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#2D3748"),
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=4
    )
    bullet_style = ParagraphStyle(
        'Bullet',
        parent=body_style,
        leftIndent=12,
        bulletIndent=4,
        spaceAfter=2
    )
    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=10.5,
        textColor=colors.HexColor("#2D3748")
    )
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.white
    )
    code_style = ParagraphStyle(
        'CodeSnippet',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#1A202C")
    )
    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#718096"),
        alignment=1,
        spaceAfter=6
    )

    story = []

    # ================= PAGE 1 =================
    story.append(Paragraph("Evaluación de Calidad de Código con SonarQube", title_style))
    story.append(Paragraph("<b>Proyecto:</b> ComuniSafe &nbsp;|&nbsp; <b>Asignatura:</b> Arquitectura de Software", subtitle_style))
    story.append(Paragraph("<b>Repositorio Git:</b> <font color='#2B6CB0'><u>https://github.com/MarceloRebolledo/ComuniSafePS.git</u></font>", body_style))
    story.append(Paragraph("<b>Fecha:</b> 21 de Octubre de 2026 &nbsp;|&nbsp; <b>Herramienta:</b> SonarQube 9.9.8 LTS Community &amp; SonarScanner CLI", body_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2B6CB0"), spaceBefore=4, spaceAfter=8))

    story.append(Paragraph("1. Descripción del Proyecto y Arquitectura Tecnológica", h1_style))
    story.append(Paragraph(
        "<b>ComuniSafe</b> es una plataforma integral de gestión colaborativa de seguridad vecinal e incidentes comunitarios. "
        "El sistema facilita a los residentes reportar eventos de riesgo (luminarias defectuosas, baches, microbasurales, emergencias), "
        "georreferenciar situaciones en mapas interactivos, colaborar comunitariamente y gestionar automáticamente la derivación de requerimientos "
        "hacia departamentos municipales correspondientes.",
        body_style
    ))
    story.append(Paragraph("La solución sigue un patrón arquitectónico desacoplado en capas compuesto por:", body_style))
    story.append(Paragraph("• <b>Backend API:</b> Desarrollado en <b>Python 3.11</b> bajo el framework asíncrono <b>FastAPI</b>, persistencia con <b>SQLAlchemy</b> sobre SQLite/PostgreSQL, seguridad criptográfica con tokens JWT (Passlib, Bcrypt, Jose), validación mediante esquemas Pydantic y conjunto de pruebas automatizadas con <b>Pytest</b> y <b>Pytest-Cov</b>.", bullet_style))
    story.append(Paragraph("• <b>Frontend Web:</b> Portal reactivo de administración y monitoreo implementado con <b>Vue 3</b> (Composition API) y <b>TypeScript</b>, empaquetado con <b>Vite</b>, gestión de estado global centralizada mediante <b>Pinia</b> y gráficos con <b>Chart.js</b>.", bullet_style))
    story.append(Paragraph("• <b>Frontend Mobile:</b> Aplicación móvil multiplataforma desarrollada en <b>Flutter (Dart)</b> para la interacción ciudadana en terreno con geolocalización.", bullet_style))
    story.append(Paragraph("• <b>Entorno de Evaluación de Calidad:</b> Contenedor oficial <b>SonarQube Community LTS</b> orquestado con Docker, vinculado a <b>SonarScanner CLI</b> y configurado mediante <code>sonar-project.properties</code>.", bullet_style))

    story.append(Spacer(1, 4))
    story.append(Paragraph("2. Configuración y Ejecución del Primer Análisis (Línea Base)", h1_style))
    story.append(Paragraph(
        "Para establecer la línea base de calidad del software, se ejecutaron las siguientes actividades de configuración:<br/>"
        "1. <b>Despliegue de SonarQube:</b> Ejecución del contenedor local <code>sonarqube:lts-community</code> en el puerto 9000.<br/>"
        "2. <b>Generación de Cobertura de Pruebas:</b> Instrumentación del código backend mediante <code>py -3.11 -m pytest --cov=app --cov-report=xml:coverage.xml tests/</code>, logrando un reporte Cobertura XML con rutas mapeadas hacia el contenedor.<br/>"
        "3. <b>Configuración del Scanner:</b> Creación del archivo <code>sonar-project.properties</code> en la raíz del repositorio, definiendo fuentes en <code>backend/app</code>, <code>backend/main.py</code> y <code>frontend_web/src</code>, exclusiones de dependencias y la vinculación de <code>coverage.xml</code>.<br/>"
        "4. <b>Ejecución del Escaneo Inicial:</b> Lanzamiento de <code>sonar-scanner-cli</code> mediante Docker conectado a la instancia local.",
        body_style
    ))

    # ================= PAGE 2 =================
    story.append(PageBreak())
    story.append(Paragraph("Resultados Iniciales de SonarQube (Línea Base)", h1_style))

    img_baseline_path = os.path.abspath("docs/images/baseline_overall.png")
    if os.path.exists(img_baseline_path):
        story.append(Image(img_baseline_path, width=500, height=175))
        story.append(Paragraph("Figura 1: Captura del Dashboard inicial de SonarQube para ComuniSafe (Pestaña 'Overall Code').", caption_style))

    story.append(Paragraph("<b>Métricas Clave Registradas en el Análisis Inicial:</b>", h2_style))

    initial_metrics_data = [
        [Paragraph("<b>Métrica</b>", table_header_style), Paragraph("<b>Valor</b>", table_header_style), Paragraph("<b>Rating</b>", table_header_style), Paragraph("<b>Interpretación e Impacto en ComuniSafe</b>", table_header_style)],
        [Paragraph("<b>Quality Gate</b>", table_cell_style), Paragraph("Passed (OK)", table_cell_style), Paragraph("—", table_cell_style), Paragraph("El código global cumplió los umbrales estándar iniciales de SonarQube.", table_cell_style)],
        [Paragraph("<b>Bugs</b>", table_cell_style), Paragraph("2", table_cell_style), Paragraph("Rating B", table_cell_style), Paragraph("Tablas de datos HTML en vistas Vue sin etiqueta ni atributo de descripción accesible.", table_cell_style)],
        [Paragraph("<b>Vulnerabilities</b>", table_cell_style), Paragraph("0", table_cell_style), Paragraph("Rating A", table_cell_style), Paragraph("Sin fallas críticas ni riesgos de inyección SQL detectados en los endpoints.", table_cell_style)],
        [Paragraph("<b>Code Smells</b>", table_cell_style), Paragraph("6", table_cell_style), Paragraph("Rating A", table_cell_style), Paragraph("Duplicación de literales en modelos/routers y una función con alta complejidad cognitiva (21).", table_cell_style)],
        [Paragraph("<b>Coverage</b>", table_cell_style), Paragraph("49.9%", table_cell_style), Paragraph("—", table_cell_style), Paragraph("Porcentaje de líneas de backend ejecutadas durante la suite de pruebas automatizadas.", table_cell_style)],
        [Paragraph("<b>Duplications</b>", table_cell_style), Paragraph("2.9%", table_cell_style), Paragraph("—", table_cell_style), Paragraph("Bajo porcentaje de líneas duplicadas en componentes y plantillas (&lt; 3.0%).", table_cell_style)],
        [Paragraph("<b>Deuda Técnica</b>", table_cell_style), Paragraph("53 min", table_cell_style), Paragraph("—", table_cell_style), Paragraph("Esfuerzo estimado por SonarQube para remediar los 8 problemas iniciales.", table_cell_style)],
        [Paragraph("<b>Líneas de Código (NCLOC)</b>", table_cell_style), Paragraph("942", table_cell_style), Paragraph("—", table_cell_style), Paragraph("Volumen de líneas efectivas analizadas (backend Python y frontend Vue/TS).", table_cell_style)]
    ]

    t_initial = Table(initial_metrics_data, colWidths=[100, 70, 75, 275])
    t_initial.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_initial)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Explicación de las Métricas Más Relevantes:</b>", h2_style))
    story.append(Paragraph("• <b>Reliability Rating (B):</b> Refleja la existencia de al menos un bug de severidad menor. En aplicaciones vecinales como ComuniSafe, la fiabilidad garantiza que las interfaces no fallen ni presenten inconsistencias de visualización para usuarios con tecnologías de asistencia.", bullet_style))
    story.append(Paragraph("• <b>Code Smells y Maintainability (A):</b> Aunque la calificación general es A, la existencia de funciones complejas dificulta que nuevos desarrolladores amplíen el sistema sin riesgo de efectos colaterales.", bullet_style))
    story.append(Paragraph("• <b>Coverage (49.9%):</b> La cobertura protege los módulos de negocio principales de incidentes ante refactorizaciones, pero requiere extenderse hacia los flujos de autenticación.", bullet_style))

    # ================= PAGE 3 =================
    story.append(PageBreak())
    story.append(Paragraph("3. Identificación y Análisis de Hallazgos Críticos", h1_style))
    story.append(Paragraph(
        "Se analizaron detalladamente los problemas identificados por SonarQube, seleccionando los 3 hallazgos principales (cubriendo Bugs y Code Smells) "
        "más dos hallazgos adicionales relevantes de mantenibilidad:",
        body_style
    ))

    findings_summary = [
        [Paragraph("<b>ID</b>", table_header_style), Paragraph("<b>Tipo</b>", table_header_style), Paragraph("<b>Componente / Archivo</b>", table_header_style), Paragraph("<b>Problema Identificado</b>", table_header_style), Paragraph("<b>Gravedad</b>", table_header_style), Paragraph("<b>Acción Propuesta</b>", table_header_style)],
        [Paragraph("<b>H01</b>", table_cell_style), Paragraph("Bug", table_cell_style), Paragraph("<code>frontend_web/.../VecinosView.vue</code> (L45) y <code>ReportsView.vue</code>", table_cell_style), Paragraph("Tabla HTML <code>&lt;table&gt;</code> sin descripción accesible (Regla S5256).", table_cell_style), Paragraph("Minor", table_cell_style), Paragraph("Incorporar <code>&lt;caption class='sr-only'&gt;</code>.", table_cell_style)],
        [Paragraph("<b>H02</b>", table_cell_style), Paragraph("Code Smell", table_cell_style), Paragraph("<code>backend/app/routers/reports.py</code> (L247, 283, 326, 344, 426)", table_cell_style), Paragraph("Duplicación de literal <i>'Reporte no encontrado'</i> en 5 ubicaciones.", table_cell_style), Paragraph("Critical", table_cell_style), Paragraph("Definir constante <code>ERROR_REPORT_NOT_FOUND</code>.", table_cell_style)],
        [Paragraph("<b>H03</b>", table_cell_style), Paragraph("Code Smell", table_cell_style), Paragraph("<code>backend/app/routers/reports.py</code> (L412)", table_cell_style), Paragraph("Función <code>update_report_status</code> con Complejidad Cognitiva de 21 (límite 15).", table_cell_style), Paragraph("Critical", table_cell_style), Paragraph("Modularizar mediante extracción de métodos auxiliares.", table_cell_style)],
        [Paragraph("<b>H04</b>", table_cell_style), Paragraph("Code Smell", table_cell_style), Paragraph("<code>backend/app/models.py</code> (L25, 46, 57)", table_cell_style), Paragraph("Duplicación de literales <i>'all, delete-orphan'</i> (6x) y claves foráneas.", table_cell_style), Paragraph("Critical", table_cell_style), Paragraph("Declarar constantes para cascade y foreign keys.", table_cell_style)],
        [Paragraph("<b>H05</b>", table_cell_style), Paragraph("Code Smell", table_cell_style), Paragraph("<code>backend/main.py</code> (L24, 37, 50)", table_cell_style), Paragraph("Duplicación del literal de ubicación <i>'Temuco, Chile'</i> (3x).", table_cell_style), Paragraph("Critical", table_cell_style), Paragraph("Definir constante <code>DEFAULT_MOCK_LOCATION</code>.", table_cell_style)]
    ]

    t_findings = Table(findings_summary, colWidths=[30, 65, 125, 130, 50, 120])
    t_findings.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
    ]))
    story.append(t_findings)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Preguntas de Análisis por Hallazgo:</b>", h2_style))
    story.append(Paragraph("<b>Hallazgo H01 (Bug - Accesibilidad Web en Vistas Vue):</b>", body_style))
    story.append(Paragraph("• <i>¿Por qué es importante corregir el problema?</i> Las directrices WCAG 2.1 exigen que las estructuras tabulares ofrezcan títulos descriptivos. Sin ellos, usuarios que emplean lectores de pantalla pierden el contexto de los listados vecinales.", bullet_style))
    story.append(Paragraph("• <i>¿Cómo afecta al sistema?</i> Degrada el Reliability Rating a nivel 'B' e introduce barreras de inclusión digital en una aplicación comunitaria.", bullet_style))
    story.append(Paragraph("• <i>¿Qué modificación permite resolverlo?</i> Incorporar <code>&lt;caption class='sr-only'&gt;Listado de vecinos...&lt;/caption&gt;</code> en <code>VecinosView.vue</code> y <code>ReportsView.vue</code>.", bullet_style))

    story.append(Paragraph("<b>Hallazgo H02 (Code Smell - Duplicación de Literales en reports.py):</b>", body_style))
    story.append(Paragraph("• <i>¿Por qué es importante corregir el problema?</i> Viola el principio DRY. La duplicación manual de cadenas idénticas es fuente de incoherencias en respuestas de error ante futuras actualizaciones o traducción de la API.", bullet_style))
    story.append(Paragraph("• <i>¿Cómo afecta al sistema?</i> Incrementa la deuda técnica y eleva el costo de mantenimiento.", bullet_style))
    story.append(Paragraph("• <i>¿Qué modificación permite resolverlo?</i> Crear la constante <code>ERROR_REPORT_NOT_FOUND = 'Reporte no encontrado'</code> y sustituir las 5 instancias.", bullet_style))

    story.append(Paragraph("<b>Hallazgo H03 (Code Smell - Complejidad Cognitiva de 21 en update_report_status):</b>", body_style))
    story.append(Paragraph("• <i>¿Por qué es importante corregir el problema?</i> El flujo de la función combinaba autorización, validaciones de cambio de estado, derivación municipal asíncrona y cálculo trigonométrico de notificaciones Haversine en un único método.", bullet_style))
    story.append(Paragraph("• <i>¿Cómo afecta al sistema?</i> Dificulta la lectura del código, entorpece las pruebas unitarias y favorece la introducción de fallos lógicos durante el mantenimiento.", bullet_style))
    story.append(Paragraph("• <i>¿Qué modificación permite resolverlo?</i> Aplicar refactorización por extracción de métodos, delegando la lógica en <code>_validate_status_transition</code> y <code>_notify_status_update</code>.", bullet_style))

    # ================= PAGE 4 =================
    story.append(PageBreak())
    story.append(Paragraph("4. Aplicación de Mejoras y Evidencia de Código", h1_style))
    story.append(Paragraph(
        "Se aplicaron correcciones reales directamente en los archivos afectados, resolviendo el 100% de los Bugs y Code Smells detectados:",
        body_style
    ))

    story.append(Paragraph("<b>Evidencia 1: Corrección de Bug en Tablas Vue (VecinosView.vue & ReportsView.vue)</b>", h2_style))
    diff_vue = (
        "&lt;div class=\"table-container\"&gt;<br/>"
        "&nbsp;&nbsp;&lt;table class=\"data-table\"&gt;<br/>"
        "<font color='#276749'><b>+&nbsp;&nbsp;&nbsp;&lt;caption class=\"sr-only\"&gt;Listado de vecinos registrados en la comunidad&lt;/caption&gt;</b></font><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&lt;thead&gt;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&lt;tr&gt;&lt;th&gt;Nombre del Usuario&lt;/th&gt;&lt;th&gt;Correo Electrónico&lt;/th&gt;...&lt;/tr&gt;<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&lt;/thead&gt;"
    )
    t_c1 = Table([[Paragraph(diff_vue, code_style)]], colWidths=[520])
    t_c1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_c1)
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>Evidencia 2: Extracción de Constante de Error en Router de Reportes (reports.py)</b>", h2_style))
    diff_const = (
        "<font color='#276749'><b>+ ERROR_REPORT_NOT_FOUND = \"Reporte no encontrado\"</b></font><br/><br/>"
        "&nbsp;&nbsp;if not report:<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;raise HTTPException(<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;status_code=status.HTTP_404_NOT_FOUND,<br/>"
        "<font color='#C53030'><b>-&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;detail=\"Reporte no encontrado\"</b></font><br/>"
        "<font color='#276749'><b>+&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;detail=ERROR_REPORT_NOT_FOUND</b></font><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;)"
    )
    t_c2 = Table([[Paragraph(diff_const, code_style)]], colWidths=[520])
    t_c2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_c2)
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>Evidencia 3: Descomposición Modular de update_report_status (reports.py)</b>", h2_style))
    diff_comp = (
        "<font color='#276749'><b>+ def _validate_status_transition(current_user: User, report: Report, new_status: str) -&gt; None:</b></font><br/>"
        "<font color='#276749'><b>+&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if current_user.role != \"admin\" and report.author_id != current_user.id:</b></font><br/>"
        "<font color='#276749'><b>+&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;raise HTTPException(status_code=403, detail=\"No tienes permiso...\")</b></font><br/>"
        "<font color='#276749'><b>+&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if new_status not in [\"abierto\", \"derivado_muni\", \"resuelto\", \"rechazado\"]:</b></font><br/>"
        "<font color='#276749'><b>+&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;raise HTTPException(status_code=400, detail=\"Estado inválido...\")</b></font><br/>"
        "<font color='#276749'><b>+&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if current_user.role != \"admin\" and new_status not in [\"abierto\", \"resuelto\"]:</b></font><br/>"
        "<font color='#276749'><b>+&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;raise HTTPException(status_code=403, detail=\"Los ciudadanos solo pueden cambiar a...\")</b></font><br/><br/>"
        "&nbsp;&nbsp;@router.put(\"/{report_id}/status\", response_model=ReportResponse)<br/>"
        "&nbsp;&nbsp;async def update_report_status(...):<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...<br/>"
        "<font color='#276749'><b>+&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_validate_status_transition(current_user, report, new_status)</b></font><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;report.status = new_status<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;...<br/>"
        "<font color='#276749'><b>+&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;_notify_status_update(db, report, current_user, old_status, new_status)</b></font><br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;invalidate_all_reports_cache()<br/>"
        "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;return ReportResponse(...)"
    )
    t_c3 = Table([[Paragraph(diff_comp, code_style)]], colWidths=[520])
    t_c3.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F7FAFC")),
        ('BOX', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_c3)

    # ================= PAGE 5 =================
    story.append(PageBreak())
    story.append(Paragraph("5. Resultados Posteriores y Comparación de Métricas", h1_style))
    story.append(Paragraph(
        "Se ejecutó un segundo escaneo completo con SonarQube sobre el código refactorizado para cuantificar el impacto de las modificaciones:",
        body_style
    ))

    img_post_path = os.path.abspath("docs/images/posterior_overall.png")
    if os.path.exists(img_post_path):
        story.append(Image(img_post_path, width=500, height=170))
        story.append(Paragraph("Figura 2: Captura del Dashboard de SonarQube tras la aplicación de mejoras (Overall Code).", caption_style))

    story.append(Paragraph("<b>Tabla Comparativa Antes vs. Después de las Mejoras:</b>", h2_style))

    comparison_data = [
        [Paragraph("<b>Métrica</b>", table_header_style), Paragraph("<b>Análisis Inicial</b>", table_header_style), Paragraph("<b>Análisis Posterior</b>", table_header_style), Paragraph("<b>Variación / Impacto</b>", table_header_style)],
        [Paragraph("<b>Bugs</b>", table_cell_style), Paragraph("2", table_cell_style), Paragraph("<font color='#276749'><b>0</b></font>", table_cell_style), Paragraph("<font color='#276749'><b>-2 (100% resueltos)</b></font>. Se eliminaron todas las incidencias de accesibilidad.", table_cell_style)],
        [Paragraph("<b>Reliability Rating</b>", table_cell_style), Paragraph("B (2.0)", table_cell_style), Paragraph("<font color='#276749'><b>A (1.0)</b></font>", table_cell_style), Paragraph("<b>Mejora sustancial:</b> Máxima calificación de confiabilidad alcanzada.", table_cell_style)],
        [Paragraph("<b>Code Smells</b>", table_cell_style), Paragraph("6", table_cell_style), Paragraph("<font color='#276749'><b>0</b></font>", table_cell_style), Paragraph("<font color='#276749'><b>-6 (100% resueltos)</b></font>. Eliminación total de olores de código y deuda técnica.", table_cell_style)],
        [Paragraph("<b>Maintainability Rating</b>", table_cell_style), Paragraph("A (1.0)", table_cell_style), Paragraph("<b>A (1.0)</b>", table_cell_style), Paragraph("Mantiene la calificación máxima de mantenibilidad.", table_cell_style)],
        [Paragraph("<b>Deuda Técnica</b>", table_cell_style), Paragraph("53 min", table_cell_style), Paragraph("<font color='#276749'><b>0 min</b></font>", table_cell_style), Paragraph("<font color='#276749'><b>-53 min</b></font>. Se saldó completamente la deuda técnica identificada.", table_cell_style)],
        [Paragraph("<b>Vulnerabilities</b>", table_cell_style), Paragraph("0", table_cell_style), Paragraph("0", table_cell_style), Paragraph("Sin vulnerabilidades detectadas en ambas evaluaciones.", table_cell_style)],
        [Paragraph("<b>Security Rating</b>", table_cell_style), Paragraph("A (1.0)", table_cell_style), Paragraph("A (1.0)", table_cell_style), Paragraph("Mantiene calificación máxima de seguridad.", table_cell_style)],
        [Paragraph("<b>Coverage (%)</b>", table_cell_style), Paragraph("49.9%", table_cell_style), Paragraph("<b>50.1%</b>", table_cell_style), Paragraph("<font color='#276749'><b>+0.2%</b></font>. Incremento marginal en cobertura de backend.", table_cell_style)],
        [Paragraph("<b>Duplications (%)</b>", table_cell_style), Paragraph("2.9%", table_cell_style), Paragraph("<b>2.8%</b>", table_cell_style), Paragraph("<font color='#276749'><b>-0.1%</b></font>. Ligera disminución en redundancia de código.", table_cell_style)],
        [Paragraph("<b>Quality Gate</b>", table_cell_style), Paragraph("Passed (OK)", table_cell_style), Paragraph("Failed (Error)*", table_cell_style), Paragraph("Falló estrictamente por umbral de <i>New Coverage</i> (55.3% &lt; 80% en nuevas líneas).", table_cell_style)]
    ]

    t_comp = Table(comparison_data, colWidths=[105, 80, 85, 250])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#2B6CB0")),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, colors.HexColor("#F7FAFC")]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "<i>*Nota Técnica sobre el Quality Gate:</i> En el perfil 'Sonar Way', SonarQube evalúa el Quality Gate sobre el bloque de <i>New Code</i> "
        "exigiendo que al menos el 80% de las nuevas líneas contengan pruebas unitarias. Al refactorizar la lógica de estado y accesibilidad (80 líneas netas añadidas) "
        "sin sumar nuevos tests a la suite, la cobertura de ese incremento específico fue de 55.3%, activando la condición de fallo puntual para código nuevo, "
        "a pesar de que el sistema global alcanzó 0 Bugs, 0 Code Smells y Rating A general.",
        caption_style
    ))

    # ================= PAGE 6 =================
    story.append(PageBreak())
    story.append(Paragraph("6. Conclusiones y Respuestas al Cuestionario", h1_style))

    story.append(Paragraph("<b>1. ¿Cuál es el estado general de calidad del código según SonarQube?</b>", h2_style))
    story.append(Paragraph(
        "El estado general de calidad del código de <b>ComuniSafe</b> es <b>excelente</b>. Tras la aplicación de las mejoras, "
        "el sistema alcanzó la máxima calificación (<b>Rating A</b>) en Confiabilidad (Reliability), Seguridad (Security) y Mantenibilidad (Maintainability). "
        "Se erradicaron todos los Bugs y Code Smells reportados, llevando la deuda técnica estimada a cero minutos y manteniendo una tasa de duplicación saludable de 2.8%.",
        body_style
    ))

    story.append(Paragraph("<b>2. ¿Cuáles fueron los problemas más importantes encontrados y por qué?</b>", h2_style))
    story.append(Paragraph(
        "Los problemas principales fueron: (1) <b>Incumplimiento de pautas de accesibilidad HTML5 (WCAG) en vistas Vue.js</b>, calificado como Bug por comprometer el uso del portal con lectores de pantalla; "
        "(2) <b>Alta complejidad cognitiva (21) en la función central de transición de estados de incidentes</b>, que concentraba lógica de autorización, derivación de tickets y notificaciones en un único bloque; "
        "y (3) <b>Duplicación repetitiva de literales clave</b> en modelos SQLAlchemy y routers de FastAPI, que amenazaba la consistencia del sistema ante cambios futuros.",
        body_style
    ))

    story.append(Paragraph("<b>3. ¿Qué cambios realizaron para corregirlos?</b>", h2_style))
    story.append(Paragraph(
        "Se aplicaron tres técnicas estándar de refactorización: (a) Inclusión de etiquetas semánticas <code>&lt;caption class='sr-only'&gt;</code> en las tablas de <code>VecinosView.vue</code> y <code>ReportsView.vue</code>; "
        "(b) Extracción de constantes centralizadas (<code>ERROR_REPORT_NOT_FOUND</code>, <code>CASCADE_ALL_DELETE</code>, <code>FK_USERS_ID</code>, <code>DEFAULT_MOCK_LOCATION</code>); "
        "y (c) Modularización del endpoint <code>update_report_status</code> mediante la delegación en funciones auxiliares <code>_validate_status_transition</code> y <code>_notify_status_update</code>.",
        body_style
    ))

    story.append(Paragraph("<b>4. ¿Qué métricas mejoraron después de aplicar las correcciones?</b>", h2_style))
    story.append(Paragraph(
        "• <b>Bugs:</b> Disminución de 2 a <b>0</b> (100% de bugs eliminados).<br/>"
        "• <b>Reliability Rating:</b> Ascendió de <b>Rating B a Rating A</b>.<br/>"
        "• <b>Code Smells:</b> Reducción de 6 a <b>0</b> (100% de olores resueltos).<br/>"
        "• <b>Deuda Técnica:</b> Reducción de 53 min a <b>0 min</b>.<br/>"
        "• <b>Duplicaciones:</b> Disminución de 2.9% a <b>2.8%</b>.<br/>"
        "• <b>Cobertura Global:</b> Aumento de 49.9% a <b>50.1%</b>.",
        body_style
    ))

    story.append(Paragraph("<b>5. ¿Qué problemas siguen pendientes y qué acciones deberían realizarse en los próximos avances?</b>", h2_style))
    story.append(Paragraph(
        "El área de mejora principal se encuentra en la <b>cobertura de pruebas automatizadas</b>: "
        "(a) Sincronizar y actualizar las pruebas de <code>tests/test_backend.py</code> implementando los endpoints reales de autenticación y registro para superar el 75-80% de cobertura en backend; "
        "(b) Incorporar una suite de pruebas unitarias para el frontend web con Vitest para emitir reportes <code>lcov.info</code> hacia SonarQube; "
        "y (c) Integrar la ejecución de SonarScanner en la canalización de integración continua (CI/CD) para evaluar cada Pull Request automáticamente antes de la integración.",
        body_style
    ))

    story.append(Spacer(1, 6))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#CBD5E0"), spaceAfter=8))
    story.append(Paragraph("7. Enlace al Repositorio e Instrucciones de Reproducción", h1_style))
    story.append(Paragraph(
        "El repositorio con el código fuente refactorizado y las configuraciones de escaneo se encuentra disponible en:<br/>"
        "<b>URL Git:</b> <font color='#2B6CB0'><u>https://github.com/MarceloRebolledo/ComuniSafePS.git</u></font><br/>"
        "Las instrucciones paso a paso para levantar la instancia Docker y reproducir el escaneo de calidad están documentadas en el archivo <code>README.md</code> en la raíz del proyecto.",
        body_style
    ))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Report successfully generated at: {os.path.abspath(output_filename)}")

if __name__ == "__main__":
    create_report()
