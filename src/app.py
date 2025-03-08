# ----- IMPORTS -----

from constants import languages
from strings import ALERTS, CONTENT

from flask import Flask, render_template, redirect, request, url_for
import json



# ----- SOURCE -----

app = Flask(__name__)


@app.route("/")
def index():
    """
    Defines the only route of the application and renders the template based on the
    language provided in the arguments. If no or an invalid language is provided, it
    will redirect to the default page /?lang=en.
    """
    
    lang = request.args.get("lang")
        
    # Check if the language is valid
    if lang in languages:
        data = json.loads(request.args.get("data")) if request.args.get("data") else {}
        bs_alerts = data["bs_alerts"] if "bs_alerts" in data else []
        
        return render_template(
            "index.html",
            bs_alerts=bs_alerts,
            strings=CONTENT,
            languages=languages,
        )
    # Else redirect to default /?lang=en
    else:
        # Redirect to default /?lang=en if no language is provided
        if not lang:
            return redirect(url_for("index", lang="en"))
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
            
            return redirect(url_for("index", lang="en", data=json.dumps(data)))
        