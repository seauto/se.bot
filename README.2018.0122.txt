#
#
# se.auto-bot.README.txt		== README.txt
#
#	se.auto-bot
#
#	research project to demonstrate how to automatically manage craigsList posting
#	- automatically post new ads
#	- automatically renew ads
#	- automatically flag other folks' (duplicate) posts in blatant abuse of CL Terms of Use
#
#
# Original
# --------
#	GitHub.com/seauto
#
#
# 18-Jan-18 amo Date-of-Birth
# 22-Jan-18 amo Added more comments
#
#
# se.auto-bot Requirements
# ------------------------
#	#
#	# Tested on Cent-7.4 64bit
#	#
#	se.auto-bot.Install-HOWTO.txt	== Install-HOWTO.txt
#
#		pypi.python.org/pypi/pip	# Install pip == Python Installer 
#			wget https://bootstrap.pypa.io/get-pip.py	# Download pip
#			python get-pip.py				# Install pip
#
#		pip install -U pip		# update pip
#		pip install selenium
#		pip install pyvirtualdisplay
#		pip install spintax ?
#
#	- python --version	# 2.7.5, 2.7.13+	# Python-3.x is incompatible with Python-2.x syntax
#
#	- Selenium		# http://www.seleniumhq.org/download
#				# https://github.com/SeleniumHQ
#
#	- Browser Driver 	# https://chromedriver.storage.googleapis.com/2.34/chromedriver_linux64.zip
#	# requires 64bit OS	#	unzip chromedriver_linux64.zip
#				#	mv chromedriver /usr/local/bin/chromedriver
#				
#	- Your CraigsList login credentials ( email and password ) is required 
#	  for automated CraigsList management: autopost and autorenew
#
#
# ------------------------------------------
# Pre-Release Proof-of-Concept ( PoC ) Code
# ------------------------------------------
#	#
#	# se.auto-bot.2018.mmdd.tgz
#	#
#	#
#	# please email me at: 	gigEnn.Sales@gMail.com
#	# --------------------------------------------
#	#
#	# Pre-Release PoC are functional
#	# Pre-Release PoC has random Location used in https://Location.CraigsLists.org
#	# Pre-Release PoC has random URLs used in https://Location.CraigsLists.org/Random-URL
#	#
#
#	- auto post classified ads to CraigsLists
#	- auto renew CL ads requiring renewals
#	- auto flag posted CL ads in violation of CL Terms of Use
#
#
# Future Updates
# ----------------
#	auto post to Ebay, Amazon, other online classifieds
#
#
# CraigsLists Info
# ----------------
#	https://www.craigslist.org/about/terms.of.use
#	https://www.craigslist.org/about/prohibited
#
#	http://www.craigslist.org/about/bulk_posting_interface
#
# =========================================================================
# se.bot is tentatively released under CreativeCommons-4.0 by-nc-nd license
# =========================================================================
#
#	https://CreativeCommons.org/licenses
#	https://CreativeCommons.org/licenses/by-nc-nd/4.0/legalcode	# or newer
#
#		- by	give appropriate credit to 1U Ring LLC - Linux-Consulting.com - et.al.
#		- nc	not for commercial products -- consulting is okay ??
#		- nd	not for your fork.. let's combine our time, resources, energy, expertise
#
#	You agree to imdemnify everybody for your actions and inactions
#	when you use this ( se.auto-bot.* ) research Proof of Concept software
#
#	You agree that you will be held liable for ALL of your actions and inactions
#
#
# se.bot.auto-post.py	- post all ads listed under Listing directory
# -------------------
#			#
#			# your CL login credentials required
#			#
#			-H /home/www/html	# Top of Listing Ad-Tree
#			-H /usr/local/SomeDir
#
#			-L Listings	# post all items ( subdirectories )
#			-e Item2	# only post Item2
#
#			# apache/html/se.auto-bot.post/Listings/
#			# apache/html/se.auto-bot.post/Listings/Item1
#			# apache/html/se.auto-bot.post/Listings/Item2
#			# apache/html/se.auto-bot.post/Listings/Item3
#			#
#			# your various CL posts
#			# /usr/local/CListings
#			# /usr/local/CListings/JobsOffered
#			# /usr/local/CListings/ForSaleItem1
#			# /usr/local/CListings/ItemsWanted
#
#
# se.bot.auto-renew.py	- automatically renew all posts already posted to CL requiring renewal
# --------------------
#			# your CL login credentials required
#			-r rr		# renew the first "rr" ads scheduled for renewal
#
#
# se.bot.auto-flag.py	- automatically flag craigslists posts that violate CL terms and conditions
# -------------------
#			-f	flag all duplicate CL postings
#
#			-t 	duplicates defined as "same title" used in CL posting
#			-b	duplicates defined as "same HTML body content"
#
#
# End of file
