import os.path
import urllib2
import urllib
import sys
from optparse import OptionParser
import base64

# This script fetches thermostat setpoint (temperature to be achieved) and publishes
# it to a virtual temp Domoticz device
#
#
#
# Change variables here, depending on your local install
#
# Enable debugging to console output. Dumps responses of queries and responses
# to stdout
debug = 0
# Username and password for tado.com
tadoUsername = "username@goes.here"
tadoPassword = "passw0rd"
# Your Domoticz installation (usually localhost:8080, without http://)
domoticzURL = "localhost:8080"
# the IDX from the Temp dummy device in Domoticz
domoticzIDX = "nn"
# the username / password of your Domoticz installation (optional, if you
# enabled authentication, currently does not work!)
domoticzusername = "xxxxx"
domoticzpassword = "xxxxx"
#
# Location of the stored cookies, used for API calls
COOKIEFILE = '/tmp/tadocookies.lwp'
# ----- End user input, following is only code -----

cj = None
cookielib = None

try:
    import cookielib
except ImportError:
    print "Cannot find cookielib. Bailing"
    sys.exit(-1)

else:
    urlopen = urllib2.urlopen
    Request = urllib2.Request
    cj = cookielib.LWPCookieJar()

if cj is not None:

    if os.path.isfile(COOKIEFILE):
        cj.load(COOKIEFILE)

    if cookielib is not None:
        opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
        urllib2.install_opener(opener)

    else:
        opener = ClientCookie.build_opener(ClientCookie.HTTPCookieProcessor(cj))
        ClientCookie.install_opener(opener)

getyourcookies = 'https://my.tado.com/j_spring_security_check?j_password=' + tadoPassword + '&j_username=' + tadoUsername
data = {}

try:
    req = Request(getyourcookies, data)
    handle = urlopen(req)

except IOError, e:
    print 'We failed to open "%s".' % getyourcookies
    if hasattr(e, 'code'):
        print 'We failed with error code - %s.' % e.code
    elif hasattr(e, 'reason'):
        print "The error object has the following 'reason' attribute :"
        print e.reason
    sys.exit()

# OK, so we have the cookies. Let's get some data.
tadomeurl = 'https://my.tado.com/api/v1/me'

try:
  req = Request(tadomeurl)
  req.add_header('Referer', 'https://my.tado.com')
  res = urlopen(req).read()

except IOError, e:
  print "Couldnt request home ID"
  sys.exit(-1)

else:
  try:
    import json
  except ImportError:
    try:
       import simplejson as json
    except ImportError:
       print "No json library available. I recommend installing either python-json"
       print "or simpejson."
       sys.exit(-1)

  res = json.loads(res)
  if debug:
    print "Retrieved Home info:"
    print json.dumps(res, indent=4)

  tadohomeId = res["homeId"]

# Lets get HVAC data and send it to Domoticz
tadohvacurl = 'https://my.tado.com/api/v1/home/' + str(tadohomeId) + '/hvacState'

try:
  req = Request(tadohvacurl)
  req.add_header('Referer', 'https://my.tado.com')
  res = urlopen(req).read()

except IOError, e:
  print "Couldnt request HVAC data"
  sys.exit(-1)

else:

  res = json.loads(res)
  if debug:
    print "Retrieved HVAC info:"
    print json.dumps(res, indent=4)

  tadosetpoint = res["setting"]["temperature"]["celsius"]

domoticzurl = ("http://" + domoticzURL + "/json.htm?type=command&param=udevice&idx=" + domoticzIDX + "&nvalue=0&svalue=" + str(tadosetpoint))

if debug:
  print "Complete URL for submission to Domoticz"
  print domoticzurl

request = urllib2.Request(domoticzurl)
res = urllib2.urlopen(request)
