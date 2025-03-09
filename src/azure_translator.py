# ----- IMPORTS -----

from azure.ai.translation.text import TextTranslationClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError
from logging import Logger
import os



# ----- SOURCE -----

# https://github.com/Azure/azure-sdk-for-python/blob/azure-ai-translation-text_1.0.1/sdk/translation/azure-ai-translation-text/samples/sample_text_translation_client.py
def __create_text_translation_client_with_credential() -> TextTranslationClient:
    """
    Creates a Text Translation client using the Azure SDK for Python.
    
    :return client (TextTranslationClient):
    """
    
    apikey = os.environ["TRANSLATOR_AZURE_TEXT_TRANSLATION_APIKEY"]
    region = os.environ["TRANSLATOR_AZURE_TEXT_TRANSLATION_REGION"]
    
    credential = AzureKeyCredential(apikey)
    text_translator = TextTranslationClient(credential=credential, region=region)
    
    return text_translator

# Define the global variables
text_translator = __create_text_translation_client_with_credential()
languages = None


# https://learn.microsoft.com/en-us/python/api/overview/azure/ai-translation-text-readme?view=azure-python
def __get_languages(logger: Logger) -> dict:
    """
    Gets the supported languages for the Azure Text Translator API.
    
    :param Flask app: The Flask application instance.
    :return languages (dict):
    """
    
    global languages
    
    try:
        response = text_translator.get_supported_languages()
        
        # Log the supported languages
        if response.translation is not None:
            logger.info("Got following translation languages: %s" % response.translation)
        languages = response.translation
        return response.translation
    
    except HttpResponseError as exception:
        if exception.error is not None:
            logger.error("HTTP error occurred: %s" % exception.error)
            logger.error("Message: %s" % exception.error.message)
        raise

def get_language_names(logger: Logger) -> list[str]:
    """
    Returns the names of the languages from the dictionary.
    
    :param dict languages: The dictionary of languages
    :return language_names (list):
    """
    
    global languages
    languages = languages or __get_languages(logger)
    language_names = []
    
    # Iterate over the languages and get only the names
    for language in list(languages.values()):
        language_names.append(language["name"])
        
    return sorted(language_names)

def get_language_code_of_name(logger: Logger, language_name: list[str]) -> list[str]:
    """
    Returns the language code for a given language name.
    
    :param str language_name: The name of the language
    :return language_code (str):
    """
    
    global languages
    languages = languages or __get_languages(logger)
    codes = []
    
    # Iterate over the languages and get the code for the given language name
    for code, language in languages.items():
        if language["name"] in language_name:
            codes.append(code)
            
    return codes if codes else None

def get_language_name_of_code(logger: Logger, language_code: list[str]) -> list[str]:
    """
    Returns the language name for a given language code.
    
    :param str language_code: The code of the language
    :return language_name (str):
    """
    
    global languages
    languages = languages or __get_languages(logger)
    names = []
    
    # Iterate over the languages and get the name for the given language code
    for code, language in languages.items():
        if code in language_code:
            names.append(language["name"])
            
    return names if names else None    

def azure_translate_text(logger: Logger, text: list[str], target_language: list[str], source_language: str = None) -> tuple[list[str], str, list[str]]:
    """
    Translates a given text from a source language to a destination language.
    
    :param list[str] text: The text to be translated
    :param list[str] target_language: The language to translate the text to
    :param str source_language: The language of the text to be translated
    :return translated (str):
    """
    try:
        response = text_translator.translate(
            body=text,
            from_language=get_language_code_of_name(logger, [source_language])[0] if source_language else None,
            to_language=get_language_code_of_name(logger, target_language),
            include_sentence_length=True
        )
        translation = response[0] if response else None

        if translation:
            # If no language was given as input, detect the language
            detected_language = translation.detected_language
            if detected_language:
                logger.info("Detected languages of the input text: %s with score: %s." % (detected_language.language, detected_language.score) )
            
            # Log the translated text and add it to the list
            translated_text_list = []
            for translated_text in translation.translations:
                logger.info("Text was translated to: '%s' and the result is: '%s'." % (translated_text.to, translated_text.text) )
                translated_text_list.append(translated_text.text)
                if translated_text.sent_len:
                    logger.debug("Source Sentence length: %s" % translated_text.sent_len.src_sent_len)
                    logger.debug("Translated Sentence length: %s" % translated_text.sent_len.trans_sent_len)
        
        source_language = get_language_name_of_code(logger, detected_language.language)[0] if source_language is None else source_language
        return translated_text_list, source_language, target_language

    except HttpResponseError as exception:
        if exception.error is not None:
            logger.error("HTTP error occurred: %s" % exception.error)
            logger.error("Message: %s" % exception.error.message)
