class ALERTS:
    """
    Class to store alert messages
    """
    
    class INVALID_LANGUAGE:
        message = "The language you tried is either invalid or not supported."

class CONTENT:
    """
    Class to store messages that contain words on the website
    """
    
    class APP_NAME:
        message = "Translator"
    
    class LANGUAGE:
        class TOGGLE:
            message = "Toggle language"
    
    class THEME:        
        class TOGGLE:
            message = "Toggle theme"
            
        class LIGHT:
            message = "Light"
        
        class DARK:
            message = "Dark"
            
        class AUTO:
            message = "Auto"
    
    class TRANSLATE_FROM:
        class TOGGLE:
            message = "Toggle translate from"
        
        class TEXT_FIELD:
            message = "Original text"
        
        class PLACEHOLDER:
            message = "Please insert text here..."
    
    class TRANSLATE_TO:
        class TOGGLE:
            message = "Toggle translate to"
        
        class TEXT_FIELD:
            message = "Translated text"
            
        class PLACEHOLDER:
            message = "Your text translates to..."
    
    class SUBMIT:
        message = "Translate"