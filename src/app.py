# ----- IMPORTS -----

from azure_translator import get_languages, azure_translate_text, get_language_codes_of_names, get_language_names_of_codes
from constants import site_languages, STRINGS
from database import connect_to_db, write_text_to_db, read_text_from_db

from flask import Flask, render_template, redirect, request, url_for, jsonify
import json



# ----- SOURCE -----

app = Flask(__name__)
language_codes, language_names = get_languages(app.logger)
db = connect_to_db(app.logger, language_codes)

# Define the routes
@app.route("/api", methods=['POST'])
def api():
    """
    Defines the API route for the application. It translates the text provided in the
    request to the target language and returns the translated text.
    
    :return resp (flask.Response): The translated text, language_from and language_to in JSON format
    """
    
    # Get the data from the request
    data = request.get_json() if request.is_json else None
    app.logger.debug("Received data: %s" % data)
    
    # Check if the data is valid
    if not data:
        app.logger.error("No data provided in the request")
        return {
            "error": "No data provided in the request"
        }, 400
    
    # Check if the data contains the required fields
    if "text" not in data or "translate_from" not in data or "translate_to" not in data:
        app.logger.error("Invalid data provided in the request")
        return {
            "error": "Invalid data provided in the request"
        }, 400
    
    # Get the source language from the data
    translate_from = data["translate_from"]
    
    # Check if the source language is valid
    if not translate_from or ( translate_from not in language_names and translate_from != "Detect Language" ):
        app.logger.error("Invalid source language provided in the request")
        return {
            "error": "Invalid source language provided in the request"
        }, 400
    
    # Get the target language from the data
    translate_to = data["translate_to"]
    
    # Check if the target language is valid
    if not translate_to or translate_to not in language_names:
        app.logger.error("Invalid target language provided in the request")
        return {
            "error": "Invalid target language provided in the request"
        }, 400
    
    # Get the text to be translated
    text = data["text"]
    
    # Translate the text
    translated_text, translate_from, translate_to = translate_text(text, translate_from, translate_to)
    
    # Return the translated text
    return jsonify({
        "translated_text": translated_text,
        "translate_from": translate_from,
        "translate_to": translate_to,
    })

@app.route("/", methods=['GET'])
def index():
    """
    Defines the only route of the application and renders the template based on the
    language provided in the arguments. If no or an invalid language is provided, it
    will redirect to the default page /?lang=en.
    """
    
    lang = request.args.get("lang")
    default_lang = "en"

    # Check if the language is valid
    if lang in site_languages:
        data = json.loads(request.args.get("data")) if request.args.get("data") else {}
        bs_alerts = data["bs_alerts"] if "bs_alerts" in data else []

        app.logger.debug("Rendering index page with language: %s" % lang)
        return render_template(
            "index.html",
            bs_alerts=bs_alerts,
            STRINGS=translate_strings(lang),
            site_languages=site_languages,
            translator_languages=language_names,
        )
    # Else redirect to default /?lang=en
    else:
        # Redirect to default /?lang=en if no language is provided
        if not lang:
            app.logger.debug("No language provided, redirecting to default /?lang=%s" % default_lang)
            return redirect(url_for("index", lang=default_lang))
        # If an invalid language is provided, redirect to default /?lang=en with an alert
        else:
            # Data
            data = {
                "bs_alerts": [
                    {
                        "type": "warning",
                        "message": STRINGS["ALERTS"]["INVALID_LANGUAGE"],
                    },
                ],
            }
            
            # Log and redirect
            app.logger.debug(f"Invalid language provided: %s, redirecting to default /?lang=%s" % (lang, default_lang))
            return redirect(url_for("index", lang="en", data=json.dumps(data)))


# Helper functions
def translate_strings(lang: str) -> dict[str, str]:
    """
    Translates the strings in the STRINGS constant to the given language.
    
    :param str lang: The language to translate the strings to
    :return new_strings (dict[str, str]): The translated strings
    """
    
    # On default language, return the strings as they are
    if lang == "en": return STRINGS
    
    new_strings = {}
    for category in STRINGS:
        new_strings[category] = {}
        
        # Don't translate alerts
        if category == "ALERTS":
            new_strings[category] = STRINGS[category]
            continue
        
        for entry in STRINGS[category]:
            new_strings[category][entry], _, _ = translate_text(
                STRINGS[category][entry],
                get_language_names_of_codes(app.logger, ["en"])[0],
                get_language_names_of_codes(app.logger, [lang])[0])
    
    return new_strings

def translate_text(text: str, src: str, dest: str) -> tuple[str, str, str]:
    """
    Checks in db if text was already translated into the given language. If not,
    it translates the given text from the source language to the destination language.
    
    :param str text: The text to be translated
    :param str src: The source language name
    :param dest: The destination language name
    
    :return translated_text (str): The translated text
    :return src (str): The source language
    :return dest (str): The destination language
    """
    
    # Check if the text is already in the database
    translation = read_text_from_db(
        db, 
        app.logger, 
        get_language_codes_of_names(app.logger, [dest])[0],
        text)
    if translation:
        return translation, src, dest
    else:
        # Translate the text
        translated_text, src, dest = azure_translate_text(app.logger, [text], [dest], src if src != "Detect Language" else None)
        
        # Write the translation to the database
        write_text_to_db(
            db, 
            app.logger, 
            get_language_codes_of_names(app.logger, dest)[0], 
            text, 
            translated_text[0])
    
    return translated_text[0], src, dest[0]
