import json
from datetime import datetime
# Importa la librería Pandas para análisis y manipulación de datos
try:
    import pandas as pd
except ImportError:
    print("ADVERTENCIA: La librería 'pandas' no está instalada. Ejecuta 'pip install pandas'")
    pd = None

# Importa el conector de MySQL (Deberás instalarlo: pip install mysql-connector-python)
# try:
#     import mysql.connector
#     # Descomenta esta línea para que el módulo esté disponible
#     # mysql_connector = mysql.connector 
# except ImportError:
#     print("ADVERTENCIA: La librería 'mysql-connector-python' no está instalada.")
#     mysql_connector = None


# --- CONFIGURACIÓN DE LA BASE DE DATOS (PERSONALIZAR) ---
DB_CONFIG = {
    "host": "localhost",
    "user": "tu_usuario_mysql",
    "password": "tu_contraseña",
    "database": "pos_mypime"
}

# Nombres de Tablas y Columnas (PERSONALIZAR SEGÚN TU DISEÑO ER)
TABLES = {
    "ventas": "ventas",
    "detalles_venta": "detalles_venta",
    "productos": "productos",
    "usuarios": "usuarios",
    "inventario": "inventario",
    "categorias": "categorias"
}

# --- FUNCIONES UTILITARIAS ---

def _parse_date(date_str, end_of_day=False):
    """Convierte una cadena de fecha (YYYY-MM-DD) a un objeto datetime, 
    ajustando la hora a inicio (00:00:00) o fin (23:59:59) del día."""
    if not date_str:
        return None
    try:
        # Si es el final del día, añade la hora máxima
        time_str = " 23:59:59" if end_of_day else " 00:00:00"
        # Intenta parsear la fecha
        return pd.to_datetime(f"{date_str}{time_str}")
    except Exception as e:
        print(f"Error al parsear la fecha '{date_str}': {e}")
        return None


# --- FUNCIÓN PRINCIPAL DE CONEXIÓN A DB ---

def get_db_connection():
    """
    Función para establecer la conexión a la base de datos MySQL.
    Se debe descomentar y ajustar una vez se tenga el conector instalado.
    """
    # if mysql_connector is None:
    #     print("SIMULACIÓN: Conexión a la DB establecida (Falta el conector).")
    #     return "SIMULATED_DB_CONNECTION"
        
    # try:
    #     conn = mysql_connector.connect(**DB_CONFIG)
    #     print("Conexión a la DB establecida.")
    #     return conn
    # except Exception as e:
    #     print(f"ERROR DE CONEXIÓN A DB: {e}")
    #     return None
    
    # Por ahora, solo simulación
    print("SIMULACIÓN: Conexión a la DB establecida.")
    return "SIMULATED_DB_CONNECTION"

# --- FUNCIONES INTERNAS DE GENERACIÓN DE DATOS (POR TIPO DE REPORTE) ---

def _generate_sales_report(filters):
    """Genera el Reporte de Ventas Detallado."""
    print(f"Lógica de Ventas activada. Filtros: {filters}")

    if pd is None:
        return {"error": "Pandas no está instalado. Instálalo para usar el procesamiento de datos."}

    # --- INICIO DE LÓGICA REAL (Descomentar y Ajustar SQL) ---
    # conn = get_db_connection()
    # if conn == "SIMULATED_DB_CONNECTION":
    #     # Si la conexión es de simulación, usa datos simulados.
    #     pass 
    # else:
    #     # Aquí iría tu consulta SQL real
    #     query = f"""
    #         SELECT v.id, v.fecha_venta, p.nombre, dv.cantidad, u.id AS cajero_id, dv.monto_total 
    #         FROM {TABLES['ventas']} v
    #         JOIN {TABLES['detalles_venta']} dv ON v.id = dv.venta_id
    #         JOIN {TABLES['productos']} p ON dv.producto_id = p.id
    #         JOIN {TABLES['usuarios']} u ON v.usuario_id = u.id
    #         WHERE v.fecha_venta >= '{filters['startDate']}' AND v.fecha_venta <= '{filters['endDate']}'
    #         {'AND u.id = ' + filters['userId'] if filters.get('userId') else ''}
    #     """
    #     df = pd.read_sql(query, conn)
    #     conn.close()
    # --- FIN DE LÓGICA REAL ---
    
    # SIMULACIÓN DE DATOS DE VENTAS
    data = {
        'ID Venta': [1001, 1002, 1003, 1004, 1005, 1006],
        'Fecha': ['2025-11-08 10:30', '2025-11-08 11:15', '2025-11-08 14:00', '2025-11-09 09:00', '2025-11-09 12:45', '2025-11-09 15:00'],
        'Producto': ['Café Especial', 'Tarta de Queso', 'Bebida Energética', 'Pan Integral', 'Chocolate Caliente', 'Café Especial'],
        'Cantidad': [2, 1, 5, 3, 4, 3],
        'Cajero ID': ['101', '102', '101', '103', '102', '101'],
        'Monto Total': [60.00, 35.50, 100.00, 45.75, 80.00, 90.00]
    }
    df = pd.DataFrame(data)
    
    # 1. Aplicar filtro de fecha (SIMULACIÓN)
    df['Fecha'] = pd.to_datetime(df['Fecha'])
    start_date_dt = _parse_date(filters.get('startDate'))
    end_date_dt = _parse_date(filters.get('endDate'), end_of_day=True)

    if start_date_dt:
        df = df[df['Fecha'] >= start_date_dt]
    if end_date_dt:
        df = df[df['Fecha'] <= end_date_dt]

    # 2. Aplicar filtro de usuario simulado
    if filters.get('userId'):
        df = df[df['Cajero ID'] == filters['userId']]

    # 3. Procesamiento de Métricas
    summary = {
        # Si no hay filas, sum() devuelve 0.0, lo cual es correcto.
        "total_ventas": df['Monto Total'].sum(), 
        "transacciones": len(df),
        "producto_estrella": df.groupby('Producto')['Cantidad'].sum().idxmax() if len(df) > 0 else "N/A",
    }
    
    # Formato de Salida
    return {
        "metadata": {
            "title": "Reporte de Ventas Detallado",
            "startDate": filters['startDate'],
            "endDate": filters['endDate'],
            "filterUser": filters['userId'] if filters.get('userId') else "Todos",
        },
        "summary": summary,
        "columns": df.columns.tolist(),
        "data": df.values.tolist(),
    }


def _generate_inventory_report(filters):
    """Genera el Reporte de Inventario/Stock."""
    print(f"Lógica de Inventario activada. Filtros: {filters}")
    if pd is None:
        return {"error": "Pandas no está instalado. Instálalo para usar el procesamiento de datos."}

    # SIMULACIÓN DE DATOS DE INVENTARIO
    data = {
        'ID Producto': ["A101", "B202", "C303", "D404"],
        'Nombre': ["Café Grano", "Leche Entera", "Muffin de Arándano", "Jugo Naranja"],
        'Stock Actual': [250, 120, 45, 80],
        'Unidad': ["Bolsas", "Litros", "Unidades", "Botellas"],
        'Fecha Vencimiento': ["2026-06-01", "2025-11-30", "2025-12-15", "2026-01-20"]
    }
    df = pd.DataFrame(data)

    # Procesamiento de Métricas (Ajustadas para Inventario)
    total_stock = df['Stock Actual'].sum()
    summary = {
        "total_stock_unidades": total_stock,
        "productos_diferentes": len(df),
        "producto_bajo_stock": df.iloc[df['Stock Actual'].idxmin()]['Nombre'] if len(df) > 0 else "N/A", # Producto con menor stock
    }

    return {
        "metadata": {
            "title": "Reporte de Inventario Actual",
            "startDate": "N/A",
            "endDate": "N/A",
            "filterCategory": filters['category'] if filters.get('category') else "Todas las categorías",
        },
        "summary": summary,
        "columns": df.columns.tolist(),
        "data": df.values.tolist(),
    }

def _generate_top_selling_report(filters):
    """Genera el Reporte de Productos Más Vendidos."""
    print(f"Lógica de Productos Más Vendidos activada. Filtros: {filters}")
    if pd is None:
        return {"error": "Pandas no está instalado. Instálalo para usar el procesamiento de datos."}

    # SIMULACIÓN DE DATOS DE PRODUCTOS VENDIDOS (Agregados)
    data = {
        'Ranking': [1, 2, 3, 4],
        'Nombre Producto': ['Café Especial', 'Tarta de Queso', 'Bebida Energética', 'Pan Integral'],
        'Total Cantidad Vendida': [1200, 850, 720, 510],
        'Total Ingreso': [36000.00, 30175.00, 14400.00, 13770.00]
    }
    df = pd.DataFrame(data)

    summary = {
        "total_ingreso": df['Total Ingreso'].sum(),
        "total_unidades_vendidas": df['Total Cantidad Vendida'].sum(),
        "producto_estrella": df.iloc[0]['Nombre Producto'] if len(df) > 0 else "N/A",
    }
    
    return {
        "metadata": {
            "title": "Reporte de Productos Más Vendidos (Top 4)",
            "startDate": filters['startDate'],
            "endDate": filters['endDate'],
            "filterCategory": filters.get('category') if filters.get('category') else "Todas las categorías",
        },
        "summary": summary,
        "columns": df.columns.tolist(),
        "data": df.values.tolist(),
    }


def _generate_profit_report(filters):
    """Genera el Reporte de Utilidad Bruta."""
    print(f"Lógica de Utilidad Bruta activada. Filtros: {filters}")
    if pd is None:
        return {"error": "Pandas no está instalado. Instálalo para usar el procesamiento de datos."}

    # SIMULACIÓN DE DATOS DE UTILIDAD (Generalmente por período)
    data = {
        'Mes': ['Oct-25', 'Sep-25', 'Ago-25'],
        'Ingresos Netos': [25000.00, 22000.00, 19500.00],
        'Costo de Venta (COGS)': [8000.00, 7000.00, 6200.00],
        'Utilidad Bruta': [17000.00, 15000.00, 13300.00],
        'Margen (%)': [68.0, 68.2, 68.2]
    }
    df = pd.DataFrame(data)

    summary = {
        "total_ingresos": df['Ingresos Netos'].sum(),
        "utilidad_total": df['Utilidad Bruta'].sum(),
        "margen_promedio": f"{df['Margen (%)'].mean():.1f}%",
    }
    
    return {
        "metadata": {
            "title": "Reporte de Utilidad Bruta Mensual",
            "startDate": filters['startDate'],
            "endDate": filters['endDate'],
            "filterUser": "General",
        },
        "summary": summary,
        "columns": df.columns.tolist(),
        "data": df.values.tolist(),
    }


# --- FUNCIÓN PRINCIPAL DE DISTRIBUCIÓN ---

def generate_report_data(filters):
    """
    Función principal llamada desde el HTML/Frontend para generar los datos del reporte.
    Distribuye la llamada a la función interna correspondiente.
    
    :param filters: Diccionario con filtros (reportType, startDate, endDate, userId, category)
    :return: Diccionario JSON con los datos del reporte.
    """
    report_type = filters.get('reportType')
    
    # Simulación de manejo de conexión (Descomentar para uso real)
    # conn = get_db_connection() 
    
    if report_type == 'ventas':
        result = _generate_sales_report(filters)
        
    elif report_type == 'inventario':
        result = _generate_inventory_report(filters)
        
    elif report_type == 'productos_vendidos':
        result = _generate_top_selling_report(filters)
        
    elif report_type == 'utilidad':
        result = _generate_profit_report(filters)
        
    else:
        result = {"error": f"Tipo de reporte no válido o no implementado: {report_type}"}

    # if conn != "SIMULATED_DB_CONNECTION":
    #    conn.close() # Cerrar conexión real

    return result

# --- FUNCIÓN DE EXPORTACIÓN (Requisito 2) ---

def export_to_file(report_data, format_type):
    """
    Gestiona la exportación del reporte a PDF o Excel.
    
    :param report_data: El diccionario de datos del reporte (generado por generate_report_data).
    :param format_type: 'pdf' o 'excel'.
    :return: Ruta del archivo generado o un mensaje de error.
    """
    if pd is None:
        return "ERROR: Pandas no está instalado. No se puede exportar."
        
    # Extraer el título del reporte
    report_title = report_data.get('metadata', {}).get('title', 'Reporte')
    
    # Crear DataFrame a partir de los datos
    try:
        # Asegurarse de que tanto 'columns' como 'data' existan y no estén vacíos
        if report_data.get('columns') and report_data.get('data'):
            df = pd.DataFrame(report_data['data'], columns=report_data['columns'])
        else:
            df = pd.DataFrame()
    except Exception as e:
        print(f"ADVERTENCIA: Fallo al crear DataFrame, usando vacío: {e}")
        df = pd.DataFrame()
    
    if df.empty:
        return "ADVERTENCIA: No hay datos para exportar."
        
    # Normalizar el nombre del archivo
    filename = f"{report_title.replace(' ', '_').replace('/', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    if format_type == 'excel':
        # Librería recomendada: openpyxl (pip install openpyxl)
        filename_ext = f"{filename}.xlsx"
        try:
            df.to_excel(filename_ext, index=False)
            return f"Archivo Excel generado en: {filename_ext}"
        except Exception as e:
            # Aquí puede fallar si openpyxl no está instalado
            return f"ERROR al exportar a Excel. Asegúrate de tener 'openpyxl' instalado: {e}"
            
    elif format_type == 'pdf':
        # La generación de PDF es compleja y requiere librerías adicionales.
        filename_ext = f"{filename}.pdf"
        
        # Lógica de generación de PDF...
        
        return f"SIMULACIÓN: Archivo PDF generado con éxito en la ruta: {filename_ext}. Requiere librerías como WeasyPrint o fpdf2 para la generación real."
        
    return "Formato de exportación no soportado."

# --- EJEMPLO DE USO (Para probar el script directamente) ---

if __name__ == '__main__':
    # Simulación de filtros que vienen desde la interfaz HTML
    test_filters = {
        'reportType': 'ventas',
        'startDate': '2025-11-08', # Fecha de inicio para probar el filtro
        'endDate': '2025-11-08', # Fecha de fin para probar el filtro
        'userId': '101', # Filtro por cajero
        'category': 'alimentos'
    }
    
    print("--- PRUEBA 1: REPORTE DE VENTAS (FILTRO 11-08 y Cajero 101) ---")
    reporte_ventas = generate_report_data(test_filters)
    print(json.dumps(reporte_ventas, indent=4))
    print(export_to_file(reporte_ventas, 'excel'))

    # Restablecer filtros de fecha para otras pruebas si fuera necesario
    test_filters['startDate'] = '2025-01-01'
    test_filters['endDate'] = '2025-11-09'
    test_filters['userId'] = '' # Quitar filtro de usuario

    print("\n--- PRUEBA 2: REPORTE DE INVENTARIO ---")
    test_filters['reportType'] = 'inventario'
    reporte_inventario = generate_report_data(test_filters)
    print(json.dumps(reporte_inventario, indent=4))

    print("\n--- PRUEBA 3: PRODUCTOS MÁS VENDIDOS ---")
    test_filters['reportType'] = 'productos_vendidos'
    reporte_top = generate_report_data(test_filters)
    print(json.dumps(reporte_top, indent=4))
    
    print("\n--- PRUEBA 4: REPORTE DE UTILIDAD BRUTA ---")
    test_filters['reportType'] = 'utilidad'
    reporte_utilidad = generate_report_data(test_filters)
    print(json.dumps(reporte_utilidad, indent=4))