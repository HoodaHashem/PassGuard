from os import getenv
storage_type = getenv("PASSGUARD_STORAGE_TYPE")

if storage_type == "db":
    from models.Store_engine.DB_Storage import DB_Storage
    storage = DB_Storage()
else:
    from models.Store_engine.File_Storge import File_Storage
    storage = File_Storage()
