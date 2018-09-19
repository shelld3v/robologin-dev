# TODO LIST
---
## Little things
- BaseController
- Raise Choice Actions?
- WebSession
    - Vars to set
    - self.delay = False
    - self.dest_ip_address = None
    - self.dns_cache = True
    - self._dns_cache = {}
    - self.proxy_handler = None
    - self.user_agent_handler = None
    - Mask Exceptions
    - Finish parameter binding
    - Test retries
    - CDN check (-b issue in dirsearch)
- GUI
    - port dirsearch style
    - Control+C (port from dirsearch)
    - Set colors
    - Logging library (Developer mode)
- detect if 401 is the incorrect status code (some tomcats drops 403)
- Worker
    - thread monitor
    - check false positives?

---

## HTML parsing 
- Radio buttons
- Checkboxes
- textareas
- selects
- Iframes  (follow redirects?)
    - Ask Index forms?
    - Ask follow redirects?
    - Add Referer to follow redirects   

---

## Stealthing
Multiple UserAgents?
?????

---

## Wordlist Processing

**Wordlist char detection**
- chardet in FileUtils.get_lines()
- check split lines

**Command line Arguments**
- --usernames-wordlist path
- --add-username user1,user2
- --add-single-username 'full username'
- --password-wordlist path
- --add-wordlist path
- --wordlist-field-separator (default :)
- --wordlist-row-separator   (default line separator)

---
## Plugins (this is looong)
AppPlugin 
- PluginType
    - CodePlugin (Python)
    - JsonPlugin
    - Other? (Ini, XML)
- PluginComponents
    - login-detect (help detect login form)
    - find-backend (find backend from front page)
    - default-credentials (all default creds)
    - username-getter (username disclosure)
    - password-getter (password disclosure ??)
- PluginLoader 
- FuzzerBuilder (inherits from lib.model.core.BaseFuzzer)

---
## CSRF Token detection (this is hard, need help)
### Manual
Arguments
- --csrf-token-field-name
- --csrf-token-regexp
### Detect token
- Links
    - http://blog.dkbza.org/2007/05/scanning-data-for-entropy-anomalies.html
    - https://github.com/rrenaud/Gibberish-Detector
    - http://blog.guif.re/2012/10/anti-csrf-token-detection-for-fun-and.html
- for each param, the xpath ('lib/model/parser/FormData.py : xpath_soup() )
- entropy of token
- Multiple tests to look token changes
---

### Detection Behaviour?

1. First request get the params
2. Send testing requests
3. Drop cookies
4. request, using previous creds, get all setted params (hidden, radio, etc),
5. Evaluation
- If any setted_params changes, there is a possible csrf token
- If not setted_params changes
    - more requests for testing
    - get setted_params size and entropy
    - string_size > 16 AND entropy > X -> csrf value


### CSRF Handler 
- Should CSRF Handler Object be assigned to FormData object?
- CSRF Handler Object (and Cookie) should be different for every thread?
- Token could be identified using xpath_soup function ('lib/model/parser/FormData.py : xpath_soup() )
- Tokens can change by time, usage, how to identify (assume X tries, X time) ?
