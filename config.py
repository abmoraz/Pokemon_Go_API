import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

#urls
api_url='https://pgorelease.nianticlabs.com/plfe/rpc'
login_url='https://sso.pokemon.com/sso/oauth2.0/authorize?client_id=mobile-app_pokemon-go&redirect_uri=https%3A%2F%2Fwww.nianticlabs.com%2Fpokemongo%2Ferror'
login_oauth='https://sso.pokemon.com/sso/oauth2.0/accessToken'
#urls end

#values
use_proxy=False
debug=False
#distance=0
steps=0.000095
walk_time=14 #median seconds between updating the server with location
google=True
pub=None
#pub=True
earned_xp=0
use_powerball=False
#values end

#session
proxies = {
  'http': 'http://127.0.0.1:8888',
  'https': 'http://127.0.0.1:8888',
}
s=requests.session()
if use_proxy:
	s.proxies.update(proxies)
	s.verify=False
s.headers.update({'User-Agent':'Niantic App'})
#session end
###########################################################################################
#public
API_URL = 'https://pgorelease.nianticlabs.com/plfe/rpc'
LOGIN_URL = 'https://sso.pokemon.com/sso/login?service=https%3A%2F%2Fsso.pokemon.com%2Fsso%2Foauth2.0%2FcallbackAuthorize'
LOGIN_OAUTH = 'https://sso.pokemon.com/sso/oauth2.0/accessToken'
PTC_CLIENT_SECRET = 'w8ScCUXJQc6kXKw8FiOhd8Fixzht18Dq3PEVkUCP5ZPxtgyWsbTvWHFLm2wNY0JR'

SESSION = requests.session()
SESSION.headers.update({'User-Agent': 'Niantic App'})
if use_proxy:
	SESSION.proxies.update(proxies)
	SESSION.verify = False
DEBUG = True
###########################################################################################