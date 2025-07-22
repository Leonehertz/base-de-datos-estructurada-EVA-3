from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime

# --- Configuración de Conexión a MongoDB ---
# IMPORTANTE: Reemplaza esta URI con la de tu cluster de MongoDB Atlas si lo usas.
# Si es local, probablemente sea 'mongodb://localhost:27017/'
MONGO_URI = "mongodb+srv://felipepoblete:Monster@cluster.niexarr.mongodb.net/" # Ejemplo para Atlas: "mongodb+srv://<user>:<password>@clustername.mongodb.net/mi_base_alimentos?retryWrites=true&w=majority"
DB_NAME = "mi_base_alimentos" # Nombre de la base de datos que creaste/usarás
COLLECTION_NAME = "alimentos" # Nombre de la colección que creaste/usarás

# --- Funciones de Utilidad ---
def get_collection():
    """Establece la conexión a MongoDB y devuelve la colección."""
    try:
        client = MongoClient(MONGO_URI)
        db = client[DB_NAME]
        collection = db[COLLECTION_NAME]
        print(f"Conexión exitosa a la colección '{COLLECTION_NAME}' en la base de datos '{DB_NAME}'.")
        return collection
    except Exception as e:
        print(f"Error al conectar a MongoDB: {e}")
        return None

# --- Operaciones CRUD ---

# 1. CREATE (Creación de nuevos documentos)
def crear_alimento(alimento):
    """Inserta un nuevo documento de alimento en la colección."""
    collection = get_collection()
    if collection is not None:
        try:
            if "fecha_creacion" not in alimento:
                alimento["fecha_creacion"] = datetime.now()
            result = collection.insert_one(alimento)
            print(f"Alimento '{alimento['nombre']}' insertado con ID: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            print(f"Error al insertar alimento: {e}")
    return None

def crear_varios_alimentos(alimentos_list):
    """Inserta múltiples documentos de alimentos en la colección."""
    collection = get_collection()
    if collection is not None:
        try:
            for alimento in alimentos_list:
                if "fecha_creacion" not in alimento:
                    alimento["fecha_creacion"] = datetime.now()
            result = collection.insert_many(alimentos_list)
            print(f"Insertados {len(result.inserted_ids)} alimentos.")
            return result.inserted_ids
        except Exception as e:
            print(f"Error al insertar varios alimentos: {e}")
    return None

# 2. READ (Lectura con filtros, operadores lógicos y estructuras anidadas)
def leer_todos_alimentos():
    """Lee y muestra todos los documentos de la colección."""
    collection = get_collection()
    if collection is not None:
        print("\n--- Todos los Alimentos ---")
        alimentos = list(collection.find())
        for alimento in alimentos:
            print(alimento)
        return alimentos
    return []

def buscar_por_nombre(nombre_alimento):
    """Busca y muestra un alimento por su nombre exacto."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Buscando alimento: {nombre_alimento} ---")
        alimento = collection.find_one({"nombre": nombre_alimento})
        if alimento:
            print(alimento)
            return alimento
        else:
            print(f"Alimento '{nombre_alimento}' no encontrado.")
    return None

def buscar_por_rango_calorias(min_calorias, max_calorias):
    """Busca alimentos con porciones dentro de un rango de calorías (Operador de comparación)."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Alimentos con porciones entre {min_calorias} y {max_calorias} calorías ---")
        query = {
            "porciones": {
                "$elemMatch": {
                    "calorias": {"$gte": min_calorias, "$lte": max_calorias}
                }
            }
        }
        alimentos_encontrados = list(collection.find(query))
        if alimentos_encontrados:
            for alimento in alimentos_encontrados:
                print(alimento)
        else:
            print("No se encontraron alimentos en ese rango de calorías.")
        return alimentos_encontrados
    return []

def buscar_por_categoria_y_proyectar(categoria, campos_a_proyectar):
    """Busca alimentos por categoría y muestra solo los campos especificados (Proyección)."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Alimentos en categoría '{categoria}' (solo {', '.join(campos_a_proyectar)}) ---")
        projection = {"_id": 0} # Excluir _id por defecto
        for campo in campos_a_proyectar:
            projection[campo] = 1 # Incluir los campos solicitados

        alimentos_encontrados = list(collection.find({"categoria": categoria}, projection))
        if alimentos_encontrados:
            for alimento in alimentos_encontrados:
                print(alimento)
        else:
            print(f"No se encontraron alimentos en la categoría '{categoria}'.")
        return alimentos_encontrados
    return []

def buscar_alimentos_con_micronutriente(nombre_micronutriente):
    """Busca alimentos que contengan un micronutriente específico (Filtro en estructura anidada)."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Alimentos con '{nombre_micronutriente}' ---")
        query = {"micronutrientes.nombre": nombre_micronutriente}
        alimentos_encontrados = list(collection.find(query))
        if alimentos_encontrados:
            for alimento in alimentos_encontrados:
                print(alimento)
        else:
            print(f"No se encontraron alimentos con '{nombre_micronutriente}'.")
        return alimentos_encontrados
    return []

def buscar_por_alergenos(alergia):
    """Busca alimentos que contengan un alergeno específico (Filtro en array)."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Alimentos que contienen el alergeno '{alergia}' ---")
        query = {"alergenos": alergia} # Busca si el valor existe en el array
        alimentos_encontrados = list(collection.find(query))
        if alimentos_encontrados:
            for alimento in alimentos_encontrados:
                print(alimento)
        else:
            print(f"No se encontraron alimentos con el alergeno '{alergia}'.")
        return alimentos_encontrados
    return []


# 3. UPDATE (Actualización de documentos o campos internos)
def actualizar_calorias_por_nombre(nombre_alimento, nueva_caloria_por_unidad, unidad_porciones="unidad"):
    """Actualiza las calorías de una porción específica de un alimento."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Actualizando calorías de '{nombre_alimento}' (unidad: {unidad_porciones}) ---")
        result = collection.update_one(
            {"nombre": nombre_alimento, "porciones.unidad": unidad_porciones},
            {"$set": {"porciones.$[elem].calorias": nueva_caloria_por_unidad}},
            array_filters=[{"elem.unidad": unidad_porciones}]
        )
        if result.matched_count > 0:
            print(f"Alimento '{nombre_alimento}' actualizado. Documentos modificados: {result.modified_count}")
        else:
            print(f"Alimento '{nombre_alimento}' o unidad '{unidad_porciones}' no encontrado para actualizar.")
        return result

def agregar_o_actualizar_micronutriente(nombre_alimento, nombre_micronutriente, cantidad_mg):
    """Agrega o actualiza un micronutriente para un alimento."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Agregando/Actualizando '{nombre_micronutriente}' para '{nombre_alimento}' ---")
        # Intenta actualizar si el micronutriente ya existe
        result = collection.update_one(
            {"nombre": nombre_alimento, "micronutrientes.nombre": nombre_micronutriente},
            {"$set": {"micronutrientes.$.cantidad_mg": cantidad_mg}}
        )
        if result.matched_count > 0:
            print(f"Micronutriente '{nombre_micronutriente}' actualizado para '{nombre_alimento}'.")
        else:
            # Si no existe, lo agrega con $push
            result = collection.update_one(
                {"nombre": nombre_alimento},
                {"$push": {"micronutrientes": {"nombre": nombre_micronutriente, "cantidad_mg": cantidad_mg}}}
            )
            if result.matched_count > 0:
                print(f"Micronutriente '{nombre_micronutriente}' agregado a '{nombre_alimento}'.")
            else:
                print(f"Alimento '{nombre_alimento}' no encontrado para agregar/actualizar micronutriente.")
        return result

def actualizar_campo_directo(nombre_alimento, campo, nuevo_valor):
    """Actualiza un campo directo (no anidado ni array) de un alimento."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Actualizando '{campo}' de '{nombre_alimento}' a '{nuevo_valor}' ---")
        result = collection.update_one(
            {"nombre": nombre_alimento},
            {"$set": {campo: nuevo_valor}}
        )
        if result.matched_count > 0:
            print(f"Campo '{campo}' de '{nombre_alimento}' actualizado. Documentos modificados: {result.modified_count}")
        else:
            print(f"Alimento '{nombre_alimento}' no encontrado.")
        return result


# 4. DELETE (Eliminación controlada de registros)
def eliminar_alimento_por_nombre(nombre_alimento):
    """Elimina un alimento por su nombre."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Eliminando alimento: {nombre_alimento} ---")
        result = collection.delete_one({"nombre": nombre_alimento})
        if result.deleted_count > 0:
            print(f"Alimento '{nombre_alimento}' eliminado exitosamente.")
        else:
            print(f"Alimento '{nombre_alimento}' no encontrado para eliminar.")
        return result

def eliminar_alimentos_por_categoria(categoria):
    """Elimina todos los alimentos de una categoría específica."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Eliminando alimentos de la categoría: {categoria} ---")
        result = collection.delete_many({"categoria": categoria})
        if result.deleted_count > 0:
            print(f"Eliminados {result.deleted_count} alimentos de la categoría '{categoria}'.")
        else:
            print(f"No se encontraron alimentos en la categoría '{categoria}' para eliminar.")
        return result

def eliminar_micronutriente_de_alimento(nombre_alimento, nombre_micronutriente):
    """Elimina un micronutriente específico del array de un alimento."""
    collection = get_collection()
    if collection is not None:
        print(f"\n--- Eliminando '{nombre_micronutriente}' de '{nombre_alimento}' ---")
        result = collection.update_one(
            {"nombre": nombre_alimento},
            {"$pull": {"micronutrientes": {"nombre": nombre_micronutriente}}}
        )
        if result.matched_count > 0 and result.modified_count > 0:
            print(f"Micronutriente '{nombre_micronutriente}' eliminado de '{nombre_alimento}'.")
        else:
            print(f"Alimento '{nombre_alimento}' o micronutriente '{nombre_micronutriente}' no encontrado.")
        return result

# --- Bloque de Ejecución Principal de la Aplicación ---
if __name__ == "__main__":
    

    # --- Inserción Adicional (Opcional) ---
    # Por si se necesita agregar algun alimento mas adelante
    # crear_alimento({
    #     "nombre": "Nuevo Alimento Extra", "categoria": "Snack",
    #     "porciones": [{ "unidad": "unidad", "cantidad": 1, "gramos": 50, "calorias": 200 }],
    #     "macros": { "proteinas_g": 5.0, "carbohidratos_g": 20.0, "grasas_g": 10.0 },
    #     "micronutrientes": [], "fibra_g": 2.0, "azucar_g": 10.0, "alergenos": []
    # })

    # 2. Leer (Consultar) diferentes tipos de datos
    print("\n=== LECTURA / CONSULTAS ===")
    leer_todos_alimentos() # Mostrará los 99 alimentos que se agregaron (o los que queden)
    buscar_por_nombre("Snickers")
    buscar_por_rango_calorias(80, 200)
    buscar_por_categoria_y_proyectar("Fruta", ["nombre", "porciones.calorias"])
    buscar_alimentos_con_micronutriente("Vitamina C")
    buscar_por_alergenos("gluten")

    # 3. Actualizar datos
    print("\n=== ACTUALIZACIONES ===")
    actualizar_calorias_por_nombre("Manzana Roja", 100, "unidad")
    actualizar_campo_directo("Naranja", "categoria", "Cítrico")
    agregar_o_actualizar_micronutriente("Plátano", "Vitamina A", 0.05)
    actualizar_campo_directo("Brownie NutraBien", "macros.grasas_g", 10.0)

    # Verificación después de actualizaciones
    print("\n--- VERIFICANDO ACTUALIZACIONES ---")
    buscar_por_nombre("Manzana Roja")
    buscar_por_nombre("Naranja")
    buscar_por_nombre("Plátano")
    buscar_por_nombre("Brownie NutraBien")

    # 4. Eliminar datos
    print("\n=== ELIMINACIONES ===")
    eliminar_alimento_por_nombre("Espinaca (cocida)")
    eliminar_alimentos_por_categoria("Bebida Alcohólica")
    eliminar_micronutriente_de_alimento("Manzana Roja", "Potasio")

    # Verificación después de eliminaciones
    print("\n--- VERIFICANDO ELIMINACIONES ---")
    leer_todos_alimentos()

    print("\n=== Todas las operaciones CRUD han sido demostradas. ===")