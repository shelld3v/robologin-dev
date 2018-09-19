BaseController
    raise Choice 
WebSession
    * Variables a setear
        * self.delay = False
        * self.dest_ip_address = None
        * self.dns_cache = True
        * self._dns_cache = {}
        * self.proxy_handler = None
        * self.user_agent_handler = None
    * Enmascarar excepciones
    * Bindear parametros del WebSession a ArgParser y DefaultConfig




WebForm
    --csrf-token-field-name
    --csrf-token-regexp
    CSRF Handling
        agregar por cada param, el xpath
        http://blog.dkbza.org/2007/05/scanning-data-for-entropy-anomalies.html
        https://github.com/rrenaud/Gibberish-Detector
        http://blog.guif.re/2012/10/anti-csrf-token-detection-for-fun-and.html
        entropy of token
        Detectar Token Present
        Si existe multiples pruebas para ver si cambia

    COMO PROBAR
        1 request obtiene los parametros con xpath
        2 envia test de creds
        3 drop cookies
        4 request, con las mismas creds, obtiene los setted params,
            1 si cambia alguno de los (ratio_check) setted_params, posible csrf token
            2 si no cambians los setted_params
                1 mas requests con pruebas
                2 tamano del value del setted_param y medir entropia
                    si el value es > 16 y entropy > X
                    -> csrf value
        
        Se genera el CSRFHandler
            1 se asigna el csrf handler al formData
            2 cuando se pide la data , por cada param se preguntra al csrfhandler si es un token
            3 Por cada thread, y por cada cred, le pasa todos los params (get y post)
                si no es un token, no hace nada
                    agrega sin modificar al result
                ei es un token
                    1 chequea si tiene registrado el thread
                        1 si no, lo crea
                        2 pide la url y registra la cookie
                    2 pide la url con la cookie correspondiente
                    3 con el xpath recupera el valor del token
                    4 agrega el token al result
                
   
    Handlear 
        Radio
        Checkbox
        textarea
        select
        Handlear iframes (cono follow redirects)
    Preguntar por el index del form
    Preguntar si seguir redirects
    Agregar Referer a request    
    
 
Stealthing
    Multiples UserAgents
    
    
    
Wordlist Processing
    Wordlist char detection
        chardet in FileUtils.get_lines()
        checkear split lines
    Arguments
        --usernames-wordlist path
        --add-username user1,user2
        --add-single-username 'full username'
        --password-wordlist path
        --add-wordlist path
        --wordlist-field-separator (default :)
        --wordlist-row-separator   (default line separator)
Controller:
    Fatal errors
    Control+C
Logger
    Setear colores en Logger
    Crear Log en carpeta Logs
GUI
    port dirsearch gui
HttpAuthScanner
    detectar si al fallar tira 401 o otro status

AppPlugin 
    PluginType
        CodePlugin
        JsonPlugin
    PluginComponents
        login-detect
        find-backend
        default-credentials
        username-getter
        password-getter 
    PluginLoader
    FuzzerBuilder
Worker
    thread monitor de actividad
    
    chequear falsos positivos
    

    
