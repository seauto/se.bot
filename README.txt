#
#
# se.auto-bot.README.txt		== README.txt
#
#
# 18-Jan-18 amo Date-of-Birth
#
#
# se.auto-bot Requirements
# ------------------------
#	se.auto-bot.Install-HOWTO.txt	== Intall-HOWTO.txt
#
#	- Selenium
#	- Browser Driver
#
#	- Your CraigsList login credentials ( email and password ) is required for CraigsList management
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
# =========================================================================
# se.bot is tentatively released under CreativeCommons4.0 by-nc-nd license
# =========================================================================
#
#	https://CreativeCommons.org/licenses
#	https://CreativeCommons.org/licenses/by-nc-nd/4.0/legalcode	# or newer
#
#		- by	give appropriate credit to 1U Ring LLC
#		- nc	not for commercial products -- consulting is okay ??
#		- nd	not for your fork.. lets combine our time, resources, energy, expertise
#
# se.bot.auto-post.py	- post all ads listed under Listing directory
# -------------------
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
#
# se.bot.auto-renew.py	- automatically renew all posts already posted to CL requiring renewal
# --------------------
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
