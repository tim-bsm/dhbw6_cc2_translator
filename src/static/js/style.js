// https://getbootstrap.com/docs/5.3/customize/color-modes/#javascript
/*!
 * Color mode toggler for Bootstrap's docs (https://getbootstrap.com/)
 * Copyright 2011-2024 The Bootstrap Authors
 * Licensed under the Creative Commons Attribution 3.0 Unported License.
 */

(() => {
'use strict'

// Remove the query string from the URL
const params = new URLSearchParams(window.location.search);
params.delete('data');
window.history.replaceState({}, document.title, window.location.pathname + '?' + params);


const getStoredTheme = () => localStorage.getItem('theme')
const setStoredTheme = theme => localStorage.setItem('theme', theme)

const getPreferredTheme = () => {
  const storedTheme = getStoredTheme()
  if (storedTheme) {
    return storedTheme
  }

  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

const setTheme = theme => {
  if (theme === 'auto') {
    document.documentElement.setAttribute('data-bs-theme', (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'))
  } else {
    document.documentElement.setAttribute('data-bs-theme', theme)
  }
}

setTheme(getPreferredTheme())

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
  const storedTheme = getStoredTheme()
  if (storedTheme !== 'light' && storedTheme !== 'dark') {
    setTheme(getPreferredTheme())
  }
})

window.addEventListener('DOMContentLoaded', () => {
  showActiveIcon(params.get('lang') || 'en', 'lang')
  addIconEventListeners('lang')
  
  showActiveIcon(getPreferredTheme(), 'bs-theme')
  addIconEventListeners('bs-theme')
  
  showActiveText('Detect Language', 'transl-from')
  addTextEventListeners('transl-from')

  showActiveText('English', 'transl-to')
  addTextEventListeners('transl-to')
})

})()


// Function to change the active icon of dropdowns
const showActiveIcon = (value, id, focus=false) => {
  // Create an alternate id with the first letter of each word capitalized and without hyphens
  const alternateId = id.replace(/(-)(\S)/g, s=>s.toUpperCase()).replace('-', '')
  const switcher = document.querySelector('#'+id)


  if (!switcher) {
    return
  }

  const switcherText = document.querySelector('#'+id+'-text')
  const activeIcon = document.querySelector('.'+id+'-icon-active i')
  const btnToActive = document.querySelector(`[data-`+id+`-value="${value}"]`)
  const iconOfActiveBtn = btnToActive.querySelector('span i').getAttribute('class')
  const spanCheck = btnToActive.querySelector('span:nth-child(2)')

  document.querySelectorAll('[data-'+id+'-value]').forEach(element => {
    element.classList.remove('active')
    element.querySelector('span:nth-child(2)').classList.add('d-none')
    element.setAttribute('aria-pressed', 'false')
  })

  btnToActive.classList.add('active')
  btnToActive.setAttribute('aria-pressed', 'true')
  activeIcon.setAttribute('class', iconOfActiveBtn)
  const themeSwitcherLabel = `${switcherText.textContent} (${btnToActive.dataset[alternateId+'Value']})`
  switcherText.setAttribute('aria-label', themeSwitcherLabel)
  spanCheck.classList.remove('d-none')

  if (focus) {
    switcherText.focus()
  }
}
const addIconEventListeners = (id) => {
  document.querySelectorAll('[data-'+id+'-value]')
    .forEach(toggle => {
      toggle.addEventListener('click', () => {
        const value = toggle.getAttribute('data-'+id+'-value')
        if (id == 'bs-theme') {
          setStoredTheme(value)
          setTheme(value)
        }
        showActiveIcon(value, id, true)
      })
    })
}

// Function to change the active text of dropdowns
const showActiveText = (value, id, focus=false) => {
  // Create an alternate id with the first letter of each word capitalized and without hyphens
  const alternateId = id.replace(/(-)(\S)/g, s=>s.toUpperCase()).replace('-', '')
  const switcher = document.querySelector('#'+id)


  if (!switcher) {
    return
  }

  const switcherText = document.querySelector('#'+id+'-text')
  const activeText = document.querySelector('.'+id+'-text-active')
  const btnToActive = document.querySelector(`[data-`+id+`-value="${value}"]`)
  const textOfActiveBtn = btnToActive.textContent || btnToActive.innerText
  const spanCheck = btnToActive.querySelector('span')

  document.querySelectorAll('[data-'+id+'-value]').forEach(element => {
    element.classList.remove('active')
    element.querySelector('span').classList.add('d-none')
    element.setAttribute('aria-pressed', 'false')
  })

  btnToActive.classList.add('active')
  btnToActive.setAttribute('aria-pressed', 'true')
  activeText.textContent = textOfActiveBtn
  const themeSwitcherLabel = `${switcherText.textContent} (${btnToActive.dataset[alternateId+'Value']})`
  switcherText.setAttribute('aria-label', themeSwitcherLabel)
  spanCheck.classList.remove('d-none')

  if (focus) {
    switcherText.focus()
  }
}
const addTextEventListeners = (id) => {
  document.querySelectorAll('[data-'+id+'-value]')
    .forEach(toggle => {
      toggle.addEventListener('click', () => {
        const value = toggle.getAttribute('data-'+id+'-value')
        showActiveText(value, id, false)
      })
    })
}