(() => {
'use strict'

const submitTranslation = () => {
    // Get the value of the active button
    const origText = document.getElementById('origText')
    const translatedText = document.getElementById('translatedText')
    const fromText = document.querySelector('.transl-from-text-active')
    const toText = document.querySelector('.transl-to-text-active')

    const data = {
        text: origText.value,
        translate_from: removeNewlineAndSpaces(fromText.textContent) || removeNewlineAndSpaces(fromText.innerText),
        translate_to: removeNewlineAndSpaces(toText.textContent) || removeNewlineAndSpaces(toText.innerText),
    }
    const headers = {
        "Content-type": "application/json; charset=UTF-8"
    }

    console.log("seding following translate request to api: ", data)
    fetch('/api', {
        method: 'POST',
        body: JSON.stringify(data),
        headers: headers,
    })
        .then(response => response.json())
        .then(data => {
            console.log("received following response from api: ", data)
            translatedText.textContent = data.translated_text
            showActiveText(data.translate_from, 'transl-from')
        })
}

window.addEventListener('DOMContentLoaded', () => {
    document.getElementById('submit-btn')
        .addEventListener('click', () => {
            submitTranslation()
        })
})

const removeNewlineAndSpaces = (text) => {
    text = text.replace(/(\r\n|\n|\r)/gm, "") // remove newlines
    text = text.trim() // remove leading and trailing spaces
    return text
}
  
})()