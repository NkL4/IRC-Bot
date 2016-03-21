from twython import Twython
import irclib
import ircbot
import commands
import time

chan = "leflood"
authaut = ['xxx','xxx','xxxxx',...]

APP_KEY = 'XX'
APP_SECRET = 'XX'
OAUTH_TOKEN = 'XX'
OAUTH_TOKEN_SECRET = 'XX'


class Bot(ircbot.SingleServerIRCBot):
  #  chan = "channel name"

    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(self, [("irc.server", port)],
                                           "Bot name", "Bot desc.")
    def on_welcome(self, serv, ev):
        serv.join("#"+chan)
    def on_pubmsg(self, serv, ev):
        message = ev.arguments()[0]
        auteur = irclib.nm_to_n(ev.source())

        if "!meteo" in message[:6]:
		i=1
		while i<=7:
			u=commands.getoutput('curl --silent wttr.in/'+message[7:]+' | sed -n '+str(i)+'p')
			serv.privmsg("#"+chan,u)
			i+=1
	
	if "choupinette" in message:
		gmtime = time.gmtime()
		localtime = time.localtime()

		if localtime.tm_hour >= 12:
			serv.privmsg("#"+chan, "OK, CHOUPINETTES !!!")
		else:
			serv.privmsg("#"+chan, "Non non, il est encore trop tot !")

	if "!twtr" in message[:5] and auteur in authaut:
		# Requires Authentication as of Twitter API v1.1
		twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

	        if len(message[6:]) > 140:
	            serv.privmsg("#"+chan, 'Too many characters :/')
		else:
	 		    try:
				    twitter.update_status(status=message[6:])
				    serv.privmsg("#"+chan, 'Twitter update successfull !')
			    except TwythonError as e:
		    		    print e
			    	    serv.privmsg("#"+chan, 'Twitter update failed : '+e)

	elif "!twtr" in message[:5] and auteur not in authaut:
		    serv.privmsg("#"+chan, 'User not authorized !')

	if "!help" in message:
		serv.privmsg("#"+chan,' HELP : !cafe | !meteo <City or DNS> | !twtr <msg> #for auth users')


	if "!cafe" in message:
	        serv.privmsg("#"+chan, 'Hop, c[_] pour ' + auteur)
	if "!mate" in message:
		serv.privmsg('#'+chan, 'Et un club mate pour ' + auteur '. Un mate et ça repart')

if __name__ == "__main__":
    Bot().start()
