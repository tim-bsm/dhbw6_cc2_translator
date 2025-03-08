(() => {
'use strict'

// Remove the query string from the URL
const params = new URLSearchParams(window.location.search);
params.delete('data');
window.history.replaceState({}, document.title, window.location.pathname + '?' + params);


const showActiveLang = (lang, focus=false) => {
    const langSwitcher = document.querySelector('#lang')

    if (!langSwitcher) {
        return
    }

    const langSwitcherText = document.querySelector('#lang-text')
    const activeThemeIcon = document.querySelector('.lang-icon-active i')
    const btnToActive = document.querySelector(`[data-lang-value="${lang}"]`)
    const iconOfActiveBtn = btnToActive.querySelector('span i').getAttribute('class')
    const spanCheck = btnToActive.querySelector('span:nth-child(2)')

    document.querySelectorAll('[data-lang-value]').forEach(element => {
        element.classList.remove('active')
        element.querySelector('span:nth-child(2)').classList.add('d-none')
        element.setAttribute('aria-pressed', 'false')
    })

    btnToActive.classList.add('active')
    btnToActive.setAttribute('aria-pressed', 'true')
    activeThemeIcon.setAttribute('class', iconOfActiveBtn)
    const themeSwitcherLabel = `${langSwitcherText.textContent} (${btnToActive.dataset.langValue})`
    langSwitcher.setAttribute('aria-label', themeSwitcherLabel)
    spanCheck.classList.remove('d-none')

    if (focus) {
        langSwitcher.focus()
    }
}

window.addEventListener('DOMContentLoaded', () => {
    showActiveLang(params.get('lang') || 'en')

    document.querySelectorAll('[data-lang-value]')
        .forEach(toggle => {
            toggle.addEventListener('click', () => {
                const lang = toggle.getAttribute('data-lang-value')
                showActiveLang(lang, true)
            })
        })
})
})()