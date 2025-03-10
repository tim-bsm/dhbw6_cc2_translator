# ----- IMPORTS -----

from azure_translator import get_language_names, azure_translate_text
from constants import site_languages
from strings import ALERTS, CONTENT

from flask import Flask, render_template, redirect, request, url_for, jsonify
import json



# ----- SOURCE -----

app = Flask(__name__)
translator_languages = get_language_names(app.logger)


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
    if not translate_from or ( translate_from not in translator_languages and translate_from != "Detect Language" ):
        app.logger.error("Invalid source language provided in the request")
        return {
            "error": "Invalid source language provided in the request"
        }, 400
    
    # Get the target language from the data
    translate_to = data["translate_to"]
    
    # Check if the target language is valid
    if not translate_to or translate_to not in translator_languages:
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
            strings=CONTENT,
            site_languages=site_languages,
            translator_languages=translator_languages,
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
                        "message": ALERTS.INVALID_LANGUAGE.message
                    },
                ],
            }
            
            # Log and redirect
            app.logger.debug(f"Invalid language provided: %s, redirecting to default /?lang=%s" % (lang, default_lang))
            return redirect(url_for("index", lang="en", data=json.dumps(data)))

def translate_text(text: str, src: str, dest: str) -> tuple[str, str, str]:
    """
    Checks in db if text was already translated into the given language. If not,
    it translates the given text from the source language to the destination language.
    
    :param str text: The text to be translated
    :param str src: The source language
    :param dest: The destination language
    
    :return translated_text (str): The translated text
    :return src (str): The source language
    :return dest (str): The destination language
    """
    
    # Translate the text
    translated_text, src, dest = azure_translate_text(app.logger, [text], [dest], src if src != "Detect Language" else None)
    
    return translated_text[0], src, dest[0]
