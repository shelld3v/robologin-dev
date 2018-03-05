BaseController
    raise Choice 
WebSession
    Variables a setear
        self.delay = False
        self.dest_ip_address = None
        self.dns_cache = True
        self._dns_cache = {}
        self.proxy_handler = None
        self.user_agent_handler = None
    Enmascarar excepciones
    Bindear parametros del WebSession a ArgParser y DefaultConfig
WebForm
    --csrf-token-field-name
    --csrf-token-regexp
    CSRF Handling
        http://blog.guif.re/2012/10/anti-csrf-token-detection-for-fun-and.html
        entropy of token
        Detectar Token Present
        Si existe multiples pruebas para ver si cambia        
    Handlear 
        Radio
        Checkbox
        textarea
        select
        Handlear iframes (cono follow redirects)
    Multiples UserAgents
    Preguntar por el index del form
    Preguntar si seguir redirects
    Agregar Referer a request    
    
    
    
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
    

    
