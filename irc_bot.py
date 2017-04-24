from twython import Twython
import irclib
import ircbot
import commands
import time
import shutil

chan = "chan"
authaut = ['xxx','xxx','xxxxx',...]

APP_KEY = 'XX'
APP_SECRET = 'XX'
OAUTH_TOKEN = 'XX'
OAUTH_TOKEN_SECRET = 'XX'


class Bot(ircbot.SingleServerIRCBot):
  #  chan = "TestIRCbotLA"
	def __init__(self):
		ircbot.SingleServerIRCBot.__init__(self, [("irc.freenode.com", 6667)],
										   "DaneelOliwav", "Je suis partout, tout le temps.")
	def on_welcome(self, serv, ev):
		serv.join("#"+chan)
	def on_pubmsg(self, serv, ev):
		message = ev.arguments()[0]
		auteur = irclib.nm_to_n(ev.source())

		if "choupinette" in message.lower():
			gmtime = time.gmtime()
			localtime = time.localtime()

			if localtime.tm_hour >= 12:
				serv.privmsg("#"+chan, "OK, CHOUPINETTES " + auteur + " !!!")
			else:
				serv.privmsg("#"+chan, "Non non, il est encore trop tot !")

		elif "!twtr" in message[:5] and auteur in authaut:
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
		elif "!help" in message:
			serv.privmsg("#"+chan," HELP : !cafe | !mate | !datalove | !meteo <City or DNS> | !twtr <msg> #for auth users | !wcmd <command & result> #write new bot's command | !dcmd <command> #delete bot's command | !botrespond #list bot's commands")
		elif "!datalove" in message:
			serv.privmsg("#"+chan, '(:~ #Datalove for you ' + auteur + ' ~:)')
		elif "!cafe" in message:
			serv.privmsg("#"+chan, 'Hop, c[_] pour ' + auteur)
		elif "!mate" in message:
			serv.privmsg('#'+chan, 'Et un club mate pour ' + auteur + '. Un mate et ca repart.')
		elif "!wcmd" in message[:5]:
			if len(message[6:]) >0:
				wcmd = open("cmd", "a")
				cmd = message[6:].split()
				command = cmd[0] + ' ' + ' '.join(cmd[1:])
				wcmd.write(command+"\n")
				wcmd.close()
				serv.privmsg("#"+chan, "Command : [*] " + command + " [*] updated !")
			else:
				serv.privmsg("#"+chan, "Tu n'aurais pas oublié un truc "+ auteur +" ?")
			#debug
			#print(cmd[0] + ' ' + ' '.join(cmd[1:]))
		elif "!dcmd" in message[:5]:
			if  len(message[6:]) >0:
				oldfile = "cmd"
				newfile = "cmd1"

				emailDomains = message[6:]

				serv.privmsg("#"+chan,"[*] This script will remove records that contain the following strings: " + emailDomains)

				linecounter = 0

				with open(oldfile) as oFile, open(newfile, 'w') as nFile:
					for line in oFile:
						if emailDomains not in line:
							nFile.write(line)
							linecounter = linecounter + 1
							#debug
							#print '[*] - {%s} Writing verified record to %s ---{ %s' % (linecounter, newfile, line)

				nFile.close()
				oFile.close()
				serv.privmsg("#"+chan,'[*] There are %s records in your saved file.' % linecounter)
				shutil.copy("cmd1","cmd")
			else:
				serv.privmsg("#"+chan, "Tu n'aurais pas oublié un truc "+ auteur +" ?")
		else:
			cmds = open("./cmd", "r")
			CMD = cmds.readlines()
			cmds.close()
			#debug
			#print(CMD)
			for action in CMD:
				actionResponse = action.split()
				if actionResponse[0] in message:
					serv.privmsg("#"+chan, ' '.join(actionResponse[1:]))
					time.sleep(1) # delays for 1 seconds

			if "!test" in message and "!test" in CMD:
				serv.privmsg('#'+chan, 'Yeaaah, it works ' + auteur)

			if "!botrespond" in message:
				if len(CMD) == 0:
					serv.privmsg("#"+chan, "Oh, no command available :(")
				else:
					serv.privmsg("#"+chan, "Commands availables : ")
					for action in CMD:
						serv.privmsg("#"+chan,action)
						time.sleep(1) # delays for 1 seconds
						#debug
						#print(len(action))

	# pi.py clone !
		if "!meteo" in message[:6]:
			i=1
			while i<=7:
				u=commands.getoutput('curl --silent wttr.in/'+message[7:]+' | sed -n '+str(i)+'p')
				serv.privmsg("#"+chan,u)
				i+=1


if __name__ == "__main__":
    Bot().start()
