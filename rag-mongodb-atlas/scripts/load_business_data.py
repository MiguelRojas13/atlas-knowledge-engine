"""
Script para cargar datos de negocio a MongoDB
"""
import json
import asyncio
from pathlib import Path
from datetime import datetime
from config.database import mongodb
from config.settings import settings

async def load_business_data():
    """Cargar datos de negocio (clientes, productos, ventas)"""

    # Conectar a MongoDB
    mongodb.connect_sync()
    db = mongodb.sync_db

    # Rutas a los archivos de datos
    base_path = Path(__file__).parent.parent / "data" / "raw" / "business"

    # 1. Cargar clientes
    print("📊 Cargando clientes...")
    clientes_path = base_path / "clientes.json"
    if clientes_path.exists():
        with open(clientes_path, 'r', encoding='utf-8') as f:
            clientes = json.load(f)

        # Limpiar colección existente
        db['clientes'].delete_many({})

        # Agregar timestamps
        for cliente in clientes:
            cliente['created_at'] = datetime.utcnow()
            cliente['updated_at'] = datetime.utcnow()

        # Insertar datos
        result = db['clientes'].insert_many(clientes)
        print(f"✅ {len(result.inserted_ids)} clientes cargados")
    else:
        print(f"❌ Archivo no encontrado: {clientes_path}")

    # 2. Cargar productos
    print("\n📦 Cargando productos...")
    productos_path = base_path / "productos.json"
    if productos_path.exists():
        with open(productos_path, 'r', encoding='utf-8') as f:
            productos = json.load(f)

        # Limpiar colección existente
        db['productos'].delete_many({})

        # Agregar timestamps
        for producto in productos:
            producto['created_at'] = datetime.utcnow()
            producto['updated_at'] = datetime.utcnow()

        # Insertar datos
        result = db['productos'].insert_many(productos)
        print(f"✅ {len(result.inserted_ids)} productos cargados")
    else:
        print(f"❌ Archivo no encontrado: {productos_path}")

    # 3. Cargar ventas
    print("\n💰 Cargando ventas...")
    ventas_path = base_path / "ventas.json"
    if ventas_path.exists():
        with open(ventas_path, 'r', encoding='utf-8') as f:
            ventas = json.load(f)

        # Limpiar colección existente
        db['ventas'].delete_many({})

        # Agregar timestamps
        for venta in ventas:
            venta['created_at'] = datetime.utcnow()
            venta['updated_at'] = datetime.utcnow()

        # Insertar datos
        result = db['ventas'].insert_many(ventas)
        print(f"✅ {len(result.inserted_ids)} ventas cargadas")
    else:
        print(f"❌ Archivo no encontrado: {ventas_path}")

    # Mostrar resumen
    print("\n" + "="*70)
    print("📊 RESUMEN DE DATOS CARGADOS")
    print("="*70)
    print(f"  • Clientes: {db['clientes'].count_documents({})}")
    print(f"  • Productos: {db['productos'].count_documents({})}")
    print(f"  • Ventas: {db['ventas'].count_documents({})}")
    print("="*70)

    # Ejemplos de consultas
    print("\n💡 Ejemplos de consultas que puedes hacer:")
    print("  • ¿Cuántos clientes tengo activos?")
    print("  • Muéstrame los productos con bajo stock")
    print("  • ¿Cuál es el total de ventas del mes de marzo?")
    print("  • ¿Qué cliente tiene más compras?")
    print("  • Lista los productos de la categoría hardware")
    print("  • ¿Cuántas ventas están pendientes?")
    print("  • Muéstrame las ventas de TechCorp Solutions")
    print("  • ¿Qué productos son de tipo suscripción?")

    # Cerrar conexión
    mongodb.disconnect_sync()

if __name__ == "__main__":
    asyncio.run(load_business_data())
