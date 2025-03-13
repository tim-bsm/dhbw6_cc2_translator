# ----- IMPORTS -----

from logging import Logger
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from pymongo.database import Database
import os



# ----- SOURCE -----

def connect_to_db(logger: Logger, language_codes: list[str]) -> Database:
    """
    Connects to the database using the connection string from
    an environment variable.

    :param logger (Logger): The logger object
    :param language_codes (list[str]): The list of language codes
    :return db (Database): The MongoDB database object
    """

    # Connect to the MongoDB database
    client = MongoClient(os.environ["TRANSLATOR_MONGODB_URI"], server_api=ServerApi('1'))
    db = client.get_database("translations")

    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        logger.info("Connected to MongoDB")
        
    except Exception as e:
        logger.error("Failed to connect to MongoDB: %s" % e)
        return None

    # Create the collections if they do not exist
    logger.debug("Checking for collections in the database")
    for lang in language_codes:
        if lang not in db.list_collection_names():
            db.create_collection(lang)
            logger.debug("Created collection for language: %s" % lang)
    logger.debug("Collections are ready")
    
    # Return the database object
    return db

def write_text_to_db(db: Database, logger: Logger, language: str, text: str, translation: str) -> bool:
    """
    Writes the text and its translation to the database.

    :param db (Database): The MongoDB database object
    :param logger (Logger): The logger object
    :param language (str): The language code
    :param text (str): The original text
    :param translation (str): The translated text
    :return success (bool): True if the write operation was successful, False otherwise
    """

    # Get the collection for the specified language
    collection = db[language]

    # Create a document with the text and its translation
    document = {
        "text": text,
        "translation": translation
    }

    # Insert the document into the collection
    try:
        collection.insert_one(document)
        logger.debug("Inserted entry into database: %s" % document)
        return True

    except Exception as e:
        logger.error("Failed to write text to database: %s" % e)
        return False

def read_text_from_db(db: Database, logger: Logger, language: str, text: str) -> str:
    """
    Reads the translation of the text from the database.

    :param db (Database): The MongoDB database object
    :param logger (Logger): The logger object
    :param language (str): The language code
    :param text (str): The original text
    :return translation (str): The translated text if found, an empty string otherwise
    """ 
    print(language)
    # Get the collection for the specified language
    collection = db[language]

    # Search for the document with the specified text
    document = collection.find_one({"text": text})

    # Return the translation if found
    if document:
        logger.debug("Found translation in database: %s" % document)
        return document["translation"]

    else:
        logger.debug("Translation not found in database")
        return None
