#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# (C) 2017 1U Ring LLC - All Rights Reserved
#
#
# LICENSE
# =======
#	https://creativecommons.org/licenses/
#	#
#	# se.flagger.py licensed under CreativeCommons.org BY-NC-ND
#	#
#	https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode
#	-
#	- BY == attribute back to 1U RING LLC
#	- NC == not for your commercial use
#	- ND == no derivative allowed - no forking allowed
#	-
#
#
# se.flagger.py -b	# check body contents	== crashes from driver.get(url) ??
# se.flagger.py -t	# check title
#
#
# Default tests
# -------------
#	se.flagger.py -d -d -d -c 5 -l fresno     -u d/search/bpa  -t -b -f -q
#	se.flagger.py -d -d -d -c 5 -l sacramento -u /d/search/cps -t -b -f -q		# computer services
#
#
# 30-Dec-17 amo Date-of-Birth
# 10-Jan-18 amo Use postbot.se.flagger.py
# 11-Jan-18 amo Remove un-necessary Account(), user/password and use CL urls
# 12-Jan-18 amo Added fixed -b check body, -t check title, -c limit number of posts to check, -l location
# 15-Jan-18 amo Use Title[] and Body[] to save and compare hash for flagging
# 16-Jan-18 amo Exclude unique non-critical stuff in html that makes it unique in duplicate posts
# 17-Jan-18 amo Rename from postbot.se.flagger to se.flagger, fix driver = Browser(), added quantumrandom() info
# 22-Jan-18 amo Skip calculating (slow) body hash - but href still required
#
#
# Flag Duplicate Posts:
# ====================
#
#	- same MD5 of body content
#	- ignore posting dates in content
#	- ignore craigslist management info in content
#	- same Title
#
#	# these other "duplicate ad" detection NOT implemented yet
#	- turn off pictures -- reduce bandwidth usage - not interested in pictures
#	- not alphanumeric characters
#
#	- check for reordered words
#	- check for changed words
#	- also check for 1 character differences
#	- also check for 1 line differences
#
#	- NOT prohibited if OVER 48 hrs
#
#	- same ad posted more than once in 48hr period
#	- prohibited items posts
#
#	- use proxy
#	- click ad with spoof'd addresses
#	- remove cookies and flag it again
#
#
# Different Browser incompatibilities
# Different Language incompatibilities	- search for text
#
#
import os
import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')
#
import random
from random import *	# randint()
#
import time		# time.sleep(x)
from time import sleep
#
import string
#
import hashlib
#
import urllib2 		# webUrl = urllib2.urlopen( url )
#
# import subprocess	# subprocess.popen()
# from subprocess import Popen, PIPE
#
#
from selenium import webdriver
#
from selenium.webdriver.chrome.options import Options	# duh
#
import re
#
# import argparse
import getopt
from optparse import OptionParser
#
#
# locale -a
#	LANG="en_US.UTF-8"
#	LC_ALL="en_US.UTF-8"
#
#
# me = "postbot.se.flagger"
Name = "se.flagger"
Version = "2018.0122"
#
#

"""
  --------------------------
  Initialize global variable
  --------------------------
"""
fname = "/tmp/postbot.se.flagger.html"
#
# ---------
# Save hash
# ---------
Title = []		# title hash
TitleStr = []		# title
#
Body = []		# content hash
BodyURL = []		# href
#
Duplicate = []		# list of duplicate title or duplicate body


"""
  ==========================
  Define CraigsList Location - aka sfbayarea, etc
  ==========================
"""
def DefineLocation( CmdOpt ):
  #
  # Location.craigslist.org/d/wanted/search/waa
  #
  # should use 2D array: [state][city]
  #
  # should keep equal number of cities for 2D array
  #
  # SC = [[]]	# define a 2 dimensional array
  #	IndexError: list assignment index out of range
  #
  # -- or --
  #
  #	range(len(a))		# i == state
  #	range(len(a[i]))	# j == city
  #
  state_count = 2
  city_count = 23
  #
  # Pre-Define a 2-dimensional array == 2 states x 3 cities
  #
  SC = [[0 for j in range(city_count)] for i in range(state_count)]	# initialize
  #
  # [0] == California
  SC[0][0] = ("bakersfield")
  SC[0][1] = ("chico")
  SC[0][2] = ("fresno")
  SC[0][3] = ("hanford")
  SC[0][4] = ("humboldt")
  #
  SC[0][5] = ("losangeles")
  SC[0][6] = ("mendocino")
  SC[0][7] = ("merced")
  SC[0][8] = ("modesto")
  SC[0][9] = ("monterey")
  #
  # 10
  SC[0][10] = ("redding")
  SC[0][11] = ("sacramento")
  SC[0][12] = ("sandiego")
  SC[0][13] = ("slo")		# san luis obispo
  SC[0][14] = ("santabarbara")
  #
  SC[0][15] = ("santamaria")
  SC[0][16] = ("sfbayarea")
  SC[0][17] = ("siskiyou")
  SC[0][18] = ("stockton")
  SC[0][19] = ("susanville")
  #
  # 20
  SC[0][20] = ("ventura")
  # [0][  ] = ("visilia")	# visilia.CL.org doesn't seem to exist -- fix non-existent SC[][]
  SC[0][21] = ("yubasutter")
  #
  # [1] == Oregon
  SC[1][0] = "bend"
  SC[1][1] = "corvallis"
  SC[1][2] = "eugene"
  SC[1][3] = "klamath"
  SC[1][4] = "medford"
  #
  SC[1][5] = "oregoncoast"
  SC[1][6] = "portland"
  SC[1][7] = "salem"
  #
  # generate ONE random integer between 0 and ( 1states or 2cities )
  #
  #	range(len(a))		# i == state
  #	range(len(a[i]))	# j == city
  #
  sID = randint(0,1)	# StateID
  #
  # sID = 1	# force testing of Oregon
  #
  c = 7	# oregon cities
  if ( sID == 0 ):
    c = 21	# california cities
  #
  # pip install quantumrandom
  # qrandom --int --min 5 --max 15
  # quantumrandom.randint(0, 20)
  #
  cID = randint(0,c)	# CityID	== max depends on StateID
  #
  # ---------------
  # use random City
  # ---------------
  location = SC[sID][cID]
  #
  # -------------------------------------------------------------------
  # Your craigslist URL
  # -------------------
  # location = "sfbayarea."
  # url = "/d/antiques/search/ata"	# defined later
  # -------------------------------------------------------------------
  #
#x config.location = location
#x config.category = "/d/antiques/search/ata"	# initialize to something
#x config.type =
  #
  CmdOpt.location = location
  #
  if ( CmdOpt.DEBUG >= 2 ):
    prMsg ( "# .. [sID][cID]=[%d][%d]=%s=craigslist.org..\n", sID, cID, CmdOpt.location )
  #
  # end DefineLocation():


"""
  ============================
  Random URLs for Testing
  ============================
"""
def DefineURL( CmdOpt ):
  #
  URL = []
  URL.append( "d/computer-gigs/search/cpg" )
  URL.append( "d/computer-services/search/cps" )
  #
  URL.append( "d/search/pts" )		# auto parts by owner
  URL.append( "d/search/bip" )		# bikes parts by dealer and owner
  URL.append( "d/search/bpa" )		# boats by dealer and owner
  #
  #
  uid = randint( 0, len(URL)-1 )
  #
  url = URL[uid]
  #
  CmdOpt.url = url
  #
  if ( CmdOpt.DEBUG >= 2 ):
    prMsg ( "# .. URL[%d].. %s.craigslist.org/%s..\n", uid, CmdOpt.location, CmdOpt.url )
  #
  # end DefineURL


"""
  --------------------
  Fire up the Browser
  --------------------
"""
def Browser():
  #
  chrome_path="/usr/local/bin/chromedriver"
  #
  chrome_options = Options()
  chrome_options.add_argument("--no-sandbox")		# allow root to startup chromium-browser
  chrome_options.add_argument("--window-position=150,50")	# no negative numbers
  chrome_options.add_argument("--window-size=1030,890")	# width,height
  #
  driver = webdriver.Chrome( chrome_options=chrome_options, executable_path=chrome_path )
  #
  return ( driver )

"""
  --------------------
  Print debug messages
  --------------------
"""
def prMsg(format, *args):
  sys.stdout.write(format % args)       # import sys
  #
  #

"""
  -------------------------
  Standard Usage
  -------------------------
"""
def usage():
  print "#"
  print "# usage: %prog [options] args"
  print "# -h --help"
  print "# -V --Version"
  print "#"
  print "# -d --debug	# -d -d -d == Debug level == 3"
  print "#"
  print "# -l --location # location.CraigsList.org "
  print "# -u --url     #  xxx.CraigsList.org/URL "
  print "#"
  print "# -c --cnt xx  # check first cc posts "
  print "#"
  print "# -f --flag    # manually      flag the duplicates "
  print "# -F --FLAG    # automatically flag the duplicates "
  print "#"
  print "# -t --title   # check for duplicate based on title "
  print "# -b --body    # check for duplicate based on body contents "
  print "#"
  print "# -q --quit    # quit the browser "
  print "#"
  #
  #

"""
  ========================
  Get Line Command Options
  ========================
"""
def GetCmdOptions():
  #
  parser = OptionParser()
  #
  #
  # option -xx not recognized if NOT in list
  # -------------------------
  try:
    opts, args = getopt.getopt(sys.argv[1:], "c:dhqfFbl:tu:V", ["help", "Version"])
    #   -c xx requires ':'
    #   --category xx requires '='
    #
  except getopt.GetoptError as err:
    print(err)
    sys.exit(2)
  #
  parser.DEBUG = 0
  parser.location = ""
  parser.url = ""
  parser.flag = 0
  parser.body  = 0
  parser.title  = 0
  parser.cnt = int(12)		# check first 12 posts
  parser.quit  = 0
  #
  for o, a in opts:
    #
    if o in ("-d", "--debug"):
      parser.DEBUG += 1         # increment debug level per -d option
      #
      if ( parser.DEBUG == 3 ):
        print "#"
      #
    elif o in ("-V", "--Version"):
      #
      print "# " +Name + "-" + Version + ".py\n#"
      exit(1)
      #
    elif o in ("-h", "--help"):
      #
      usage()
      sys.exit(2)
      #
    elif o in ("-l", "--location"):
      #
      parser.location = a
      #
      if ( parser.DEBUG >= 4 ):
 	print "# .. CmdOpt: Use location=" + parser.location
      #
    elif o in ("-u", "--url"):
      #
      parser.url = a
      #
      if ( parser.DEBUG >= 4 ):
 	print "# .. CmdOpt: url=" + parser.url
      #
    elif o in ("-c", "--cnt"):
      #
      parser.cnt = a
      #
      if ( parser.DEBUG >= 4 ):
 	print "# .. CmdOpt: Check first " + parser.cnt + " CL postings for duplicates.."
      #
    elif o in ("-f", "--flag"):
      #
      parser.flag = 1
      #
      if ( parser.DEBUG >= 4 ):
 	print "# .. CmdOpt: Manually Flag duplicate CL postings.."
      #
    elif o in ("-F", "--FLAG"):
      #
      parser.flag = 2
      #
      if ( parser.DEBUG >= 4 ):
 	print "# .. CmdOpt: Automatically Flag duplicate CL postings.."
      #
    elif o in ("-b", "--body"):
      #
      parser.body = 1
      #
      if ( parser.DEBUG >= 4 ):
 	print "# .. CmdOpt: check body contents.."
      #
    elif o in ("-t", "--title"):
      #
      parser.title = 1
      #
      if ( parser.DEBUG >= 4 ):
 	print "# .. CmdOpt: check title.."
      #
    elif o in ("-q", "--quit"):
      #
      parser.quit = 1
      #
      if ( parser.DEBUG >= 4 ):
	print "# .. CmdOpt: quit = Close the browser.."
      #
    else:
      print "# Un-supported: o=" +o + "..arg=" +a + ".."
      #
  #
  return parser
#
# End GetCmdOptions

#
# ------------------------------------------------------
# Ignore non-critical body content that makes it unique
# ------------------------------------------------------
# 
def IgnoreBodyStr ( cmdopt, str ):
  #
  if ( cmdopt.DEBUG >= 4 ):
    prMsg ( "# .. ignore str=%s..\n", str )

# ------------------
# Save the HTML page
# ------------------
def SavePage( cmdopt, url ):
  #
  # prMsg ( "# .. SavePage: %s..\n", url )
  #
  # -----------------------------------
  # now have access to all CL postings
  # -----------------------------------
  #xx driver.get( url )
  #
  # # has too much info
  # htmlpage = driver.page_source
  #
  # ----------------------------------------------------
  # want just the Title of the Ad and the body of the ad
  #	- get rid of "prohibited" ... "posted xx days ago" jibberish
  #	- get rid of everything after "post id"
  #	- get rid of blank lines
  # ----------------------------------------------------
  #xx htmlpage = driver.find_element_by_xpath("/html/body").text
  #
  #
  # define encoding=utf8
  # --------------------
  # import sys
  reload( sys )
  sys.setdefaultencoding( 'utf8' )
  #
  # browser.open('http://somewebpage')
  # html = br.response().readlines()
  # for line in html:
  #   print line
  #
  # =================================
  # Save the Current CraigsList posts
  # =================================
  #
  # import urllib2
  webUrl = urllib2.urlopen( url )
  webUrl.getcode()
  data = webUrl.read()
  # print data
  # 
  # ----------------------
  # Save the Modified HTML
  # ----------------------
  file = open ( fname, 'w' )		# encoding='utf-8'
  #
  for line in data.split( '\n' ):
    #
    # ignore non-critical body-content lines in HTML that makes it unique especially for Duplicate postings
    #
    if   line.find( '<title>' ) >= 0 :
      IgnoreBodyStr ( cmdopt, line )
      #
    elif line.find( '<link rel=' ) >= 0 :
      IgnoreBodyStr ( cmdopt, line )
      #
    elif line.find( '<meta name=' ) >= 0 :
      IgnoreBodyStr ( cmdopt, line )
      #
    elif line.find( '<meta property=' ) >= 0 :
      IgnoreBodyStr ( cmdopt, line )
      #
    elif line.find( '<a id="replylink" ' ) >= 0 :
      IgnoreBodyStr ( cmdopt, line )
      #
    elif line.find( ' class="lastLink" ' ) >= 0 :
      IgnoreBodyStr ( cmdopt, line )
      #
    elif line.find( ' class="lastTitle" ' ) >= 0 :
      IgnoreBodyStr ( cmdopt, line )
      #
    elif line.find( ' class="flaglink" ' ) >= 0 :
      IgnoreBodyStr ( cmdopt, line )
      #
    elif line.find( '<time class="date timeago" ' ) >= 0 :
      IgnoreBodyStr ( cmdopt, line )
      #
    elif line.find( '<span id="titletextonly"' ) >= 0 :
      IgnoreBodyStr ( cmdopt, line )
      #
    elif line.find( 'https://images.craigslist.org' ) >= 0 :
      IgnoreBodyStr ( cmdopt, line )
      #
    elif line.find( 'https://maps.google.com' ) >= 0 :
      IgnoreBodyStr ( cmdopt, line )
      #
    elif line.find( ' data-location=' ) >= 0 :
      IgnoreBodyStr ( cmdopt, line )
      #
    elif line.find( 'show contact info' ) >= 0 :
      IgnoreBodyStr ( cmdopt, line )
      #
    # if line.find( '<p class="postinginfo reveal" ' ) >= 0 :
    elif line.find( '<p class="postinginfo"' ) >= 0 :
      IgnoreBodyStr ( cmdopt, line )
      #
    #
    # this timestamp entry is gonna be problematic --- use command line 
    #
    elif line.find( '  2018-' ) >= 0 :
      IgnoreBodyStr ( cmdopt, line )
      #
    elif line.find( 'postingID=' ) >= 0 :
      IgnoreBodyStr ( cmdopt, line )
      #
    elif line.find( 'var pID = ' ) >= 0 :
      IgnoreBodyStr ( cmdopt, line )
      #
    elif line.find( 'var repost_of=' ) >= 0 :
      IgnoreBodyStr ( cmdopt, line )
      #
    else:
      #
      # Remove wierd chars -- or just flag it
      # line = ''.join( [i if ord(i) < 128 else '' for i in line] )
      #
      file.write( line )
      file.write( '\n' )
  #
  #
  #xx  file.write( data )
  #xx  file.write( htmlpage )
  #
  #  f.write( htmlpage.encode("utf-8") )
  file.close()
  #
  #xx driver.back()		# return back from driver.get(url) above
  time.sleep ( 2 )	# wait a little for page to load
  #
#
# End SavePage


"""
  -----------------------------------------
  Calculate MD5 Hash for Title and Body
  -----------------------------------------
"""
def CalcHash( id, url ):
  #
  # prMsg ( "# CalcMD5..\n" )
  #
  # ---------------------------------
  # Calculate the MD5 of the HTMLpage
  # ---------------------------------
  #
  # https://gist.github.com/Zireael-N/ed36997fd1a967d78cb2
  #
  with open( fname, 'rb') as f:
    contents = f.read()
    #
    # ----------------------------------------------------
    # Exclude unique identifiers from hash of body content
    # ----------------------------------------------------
    #	<title> ..
    #	<link rel=..
    #	<meta name=
    #	<meta property=
    #   ... body starts here ...
    #	<input type="hidden" class="lastLink"
    #	<input type="hidden" class="lastTitle"
    #	<a id="replylink" href="/unique-url" ...
    #	<a class="flaglink" data-flag ..
    #	<time class="date timeago"
    #   <span id="titletextonly" .. modified titles or identical tities ..
    #	<div .. data-location=https://"unique-url"
    #	<a href="/unique-url" .... show contact info
    #	<p class="postinginfo reveal" .. "date timeago"
    #	postingID=...uniqueID.. abcdefg...
    #
    sha = hashlib.sha1(contents).hexdigest()
    #
    # print("SHA1: %s" % hashlib.sha1(contents).hexdigest())
    # print("SHA256: %s" % hashlib.sha256(contents).hexdigest())
    #
    # md5 = hashlib.md5()
    # for i in range(0, len(contents), 8192):
    #   md5.update(contents[i:i+8192])
    #
    # print("MD5: %s" % md5.hexdigest())
    #
    # print ( "# .. CalcSHA1[%d]: %s url=%s" % ( id, sha, url ))
    #
    return ( sha )
#
# End CalcHash


"""
  ------------------------
  Find the duplicate posts 
  ------------------------
"""
def FindDuplicateAds( driver, cmdopt ):
  #
  id = 0
  cnt = 0
  fnd = 0
  #
  flag = cmdopt.flag 
  #
  if cmdopt.DEBUG >= 1 :
    if cmdopt.flag >= 1 :
      prMsg ( "# .. FindDuplicateAds: Found '-f' option.. you have 5 seconds manually Set/Click the Prohibit flag on the 1 duplicate ads..\n" )
      #
    else:
      prMsg ( "# .. FindDuplicateAds: Just search for duplicate ads.. \n" )
  #
  posts = driver.find_elements_by_xpath( "//*[ @class='result-title hdrlnk' ]" )
  #	Message: stale element reference: element is not attached to the page document
  #
  prohibit = ""
  #
  # pcnt = len( posts )		# 120 posts
  pcnt = len( driver.find_elements_by_xpath( "//*[ @class='result-title hdrlnk' ]" ))
  #
  for id in range( 0, pcnt):
    #
    dup = Duplicate[id]
    #
    if cmdopt.DEBUG >= 3 :
      prMsg ( "# .. Duplicate[%d]=%d..\n", id, dup )
    #
    # ------------------
    # Process Duplicates
    # ------------------
    if dup >= 1 :
      fnd += 1
      if cmdopt.DEBUG >= 2 :
	prMsg ( "# .. Duplicate[%d]: %s.. %s..\n", id, BodyURL[id], TitleStr[id] )
      #
      if flag >= 1 :
	#
	# prMsg ( "# .... driver.get.. href=%s..\n", BodyURL[id] )
	#
	driver.get ( BodyURL[id] )
	#
	# <a class="flaglink" data-flag="28" href="https://post.craigslist.org/flag?flagCode=28&amp;postingID=6460872210&amp;cat=bpo&amp;area=fre"
	#  title="flag as prohibited / spam / miscategorized">
	#  <span class="flag">x</span>
	#  <span class="flagtext">prohibited</span></a>
	#  <sup>[<a href="http://www.craigslist.org/about/prohibited">?</a>]</sup> </aside>
	#
        if cmdopt.flag >= 2 :
	  #
  	  driver.find_elements_by_xpath( "//*[ @title=\"flag as prohibited \" ]" ).click()	# xpath(...)[].click()
	  #
  	  # driver.find_elements_by_xpath( "//*[ @class='flaglink' ]" ).click()	# xpath(...)[].click()
	  #	=======================================
	  #	 'list' object has no attribute 'click'
	  #	IndexError: list index out of range
	  #	=======================================
	else:
	  #
  	  # driver.find_elements_by_xpath( "//*[ @class='flaglink' ]" )
	  #
	  time.sleep ( 5 )	# allow enough time to manually click prohibit
  	  #
	driver.back	# undo driver.get()
	#
    #
    # -----------------------------
    # just check the first few URLs 
    # -----------------------------
    cnt += 1
    if cnt >= int(cmdopt.cnt) :
      break
    #
  if cmdopt.DEBUG >= 1 :
    prMsg ( "#\n" )
    #
    if fnd > 0 :
      prMsg ( "# .. FindDuplicateAds: Found %d duplicate ads.. Found '-f' option .. you have 5 seconds manually Set/Click the Prohibit flag on the %d duplicate ads..\n", fnd, fnd )
    else :
      prMsg ( "# .. No duplicate posts found for the first %s posts\n", cmdopt.cnt )
  #
  return ( fnd )
  #
  # FindDuplicateAds()


"""
  ============================================
  List of CL URLs ==== duplicates get flagged
  ============================================
"""
def CheckAds( driver, cmdopt, hash ):
  #
  id = 0
  cnt = 0
  #
  href = ""
  md5 = ""
  #
  if cmdopt.DEBUG >= 1 :
    if (( cmdopt.title == 1 ) and ( hash == "title" )):
      #
      prMsg ( "# .. CheckAds: Calculate Title hash..\n" )
      #
    else :
      if cmdopt.body == 1 :
 	prMsg ( "# .. CheckAds: Calculate Body hash..\n" )
	#
      else :
 	prMsg ( "# .. CheckAds: Skipping calculating body hash .. relatively slow..\n" )
      #
  #
  posts = driver.find_elements_by_xpath( "//*[ @class='result-title hdrlnk' ]" )
  #
  pcnt = len( posts )
  #
  # initialize array of duplicate title/body
  #
  for id in range( 0, pcnt):
    Duplicate.append( 0 )	# initialize to 0
    #
  #
  for id in range( 0, pcnt):
    #
    link = posts[id]
    #		<selenium.webdriver .... (session="92efdae39b183b351449252c0e1512e9", element="0.9943303958795735-1")>
    #
    # prMsg ( "# .. Check[%s]: url[%d]=%s.. %s..\n", id, href )
    #
    if ( hash == "title" ):
      #
      title = link.text
      #
      # Remove wierd chars -- or just flag it
      #
      title = ''.join( [i if ord(i) < 128 else '' for i in title] )
      #
      # -----------------------------------------------
      # Calculate the Hash - flag the newest ads on top
      # -----------------------------------------------
      md5 = hashlib.sha1( title ).hexdigest()
      #
      dup = 0
      for tid in range( 0, len(Title) ):
 	#
        if Title[tid] == md5 :
	  dup += 1
	  Duplicate[tid]= id
 	  if ( cmdopt.DEBUG >= 3 ):
	    prMsg ( "# .. title[%d] == older original ---- found %d newer duplicate at title[%d]..\n", id, dup, tid )	# prev duplicate
	  #
      #
      # ------------
      # Avoid Errors == save required data now
      #		Message: stale element reference: element is not attached to the page document
      #		index out of range errors
      # ------------
      Title.append( md5 )	# assign the hash in sequence
      TitleStr.append( title )
      #
      if ( cmdopt.DEBUG >= 3 ):
 	prMsg ( "# .. title[%d]=%s.. %s..\n", cnt, Title[id], TitleStr[id] )
      #
      #
    else :
      #
      href = link.get_attribute( "href" )
      #
      # Speed things up ... don't calculate body hash
      # =============================================
      if ( cmdopt.body == 1 ):
	#
	# ---------------------------------------------
	# Save the content of the url to calculate hash
	# ---------------------------------------------
	SavePage( cmdopt, href )
	#
	# ------------------------------------------
	# Calculate the Hash - flag the newest ads on top
	# ------------------------------------------
	md5 = CalcHash( cnt, href )
	#
	dup = 0
	for bid in range( 0, len(Body) ):
	  #
	  if Body[bid] == md5 :
	    dup += 1
	    Duplicate[bid]= id
 	    if ( cmdopt.DEBUG >= 3 ):
	      prMsg ( "# .. body[%d] == older original ---- found %d newer duplicate at body[%d]..\n", id, dup, bid )	# prev duplicate
	  #
	  # duplicate body
	# skip body hash 
 	#
      else :
	#
 	# Create unique random bodyHash filler
	#
	md5 = hashlib.sha1( href ).hexdigest()	 # craigslist href=//.../xxx.html is already unique 
	#
      # ----------------------
      # Save Body Hash and href
      # ----------------------
      Body.append( md5 )	# assign the hash in sequence
      BodyURL.append ( href )
      #
      if ( cmdopt.DEBUG >= 3 ):
        prMsg ( "# .. body[%d]=%s.. %s..\n", cnt, Body[id], BodyURL[id] )
	#
      #
    # -----------------------------
    # just check the first few URLs 
    # -----------------------------
    cnt += 1
    if cnt >= int(cmdopt.cnt) :
      break
    #
  return cnt
  #
  # CheckAds


"""
  ---------------
  List of Ads
  ---------------
"""
def ListofAds( cmdopt, driver ):
  #
  url = "https://" + str(cmdopt.location) + ".craigslist.org/" + str(cmdopt.url)
  #
  prMsg ( "# ListofAds: Checking %d ads out of total: %s..\n", int(cmdopt.cnt), url )
  #
  # ---------------------
  # load the CL postings
  # ---------------------
  driver.get( url )
  #
  # List of md5 for Title
  cnt = CheckAds( driver, cmdopt, "title" )	# save title hash
  if ( cmdopt.DEBUG >= 3 ):
    print "#"
  #
  # List of md5 for Body content
  cnt = CheckAds( driver, cmdopt, "body" )	# save body hash
  if ( cmdopt.DEBUG >= 3 ):
    print "#"
  #
  # Flag the Duplicate Postings
  # ---------------------------
  cnt = FindDuplicateAds( driver, cmdopt )
  #
  # List of Ads
#
# End of ListofAds()

"""
  -----------------------------
  Done Checking for Duplicates
  -----------------------------
"""
def TearDown( driver, CmdOpt ):
  #
  if ( CmdOpt.quit ):
    #
    if ( CmdOpt.DEBUG >= 1 ):
      prMsg( "# All done: Browser properly exiting..\n#\n" )
    #
    # driver.delete_all_cookies()
    #
    driver.quit()	# kills the browser -- leave it up to go backward

"""
  =======================================
  Main - process all URLs or specific URL
  =======================================
"""
def main():
  #
  # --------------
  # Default config
  # --------------
  #
  # CommandLine over-rides system defaults
  CmdOpt = GetCmdOptions()
  #
  #
  if ( len( CmdOpt.location ) == 0 ):
    DefineLocation( CmdOpt )
  #
  if ( len( CmdOpt.url ) == 0 ):
    DefineURL( CmdOpt )
  #
  # -----------------
  # Start the Browser
  # -----------------
  driver = Browser()
  #
  #
  print "#"
  #
  ListofAds( CmdOpt, driver )
  #
  print "#"
  #
  #
  # ------------------------------
  # Cleanup any chromium jibberish after exiting chromium
  # ------------------------------
  TearDown ( driver, CmdOpt )
#
#
if __name__ == "__main__":
  main()
#
#
# End of file
