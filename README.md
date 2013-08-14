About
=====

This is a plugin that creates a new channel in Plex Media Server to view content from the website KissAnime.com. It is currently under development and as such, should be considered alpha software and potentially unstable. If you try it and it works for you (or if it not!) please let me know. 

**Note:** the author of this plugin has no affiliation with KissAnime.com or the owners of the content that it hosts.

System Requirements
===================

- **Plex Media Server Version 0.9.8.4 or newer:**
	
	- Tested Working:
		- Windows
		
	- Not Tested:
		- Mac OSX
		- Linux & NAS

- **Plex Clients:**

	- Tested Working:
		- Plex Media Centre / Home Theater for Windows
		- Android
		
	- Tested NOT Working:
		- Plex/Web
		
	- Not Tested:
		- Plex Media Centre / Home Theater for Mac OSX
		- Windows 8 app
		- Roku
		- iOS
		- Windows Phone
		- LG, Samsung Google Smart TV

How To Install
==============

- [Download](https://github.com/TehCrucible/KissAnime.bundle/archive/master.zip) the latest version of the plugin.

- Unzip and rename folder to "KissAnime.bundle"

- Copy KissAnime.bundle into the PMS plugins directory under your user account:
	- Windows 7, Vista, or Server 2008: C:\Users[Your Username]\AppData\Local\Plex Media Server\Plug-ins
	- Windows XP, Server 2003, or Home Server: C:\Documents and Settings[Your Username]\Local Settings\Application Data\Plex Media Server\Plug-ins
	- Mac/Linux: ~/Library/Application Support/Plex Media Server/Plug-ins

- Restart PMS

Known Issues
============

- Initial loading of show list can be slow.
- Season/Episode numbers listed are not the actual Season/Episode division of the show. Refer to the title of the video for the actual episode number.
- All shows have rating of 10. (Because all anime is awesome!)
- Unwatched counts will be always unwatched.  Nothing I can do about this one, its a bug with the Plex framework.

Roadmap
=======

- Favourites list
- Movies return MovieObject not TVShowObject (Cosmetic)
- More complete meta-data (Cosmetic)

Changelog
=========

**0.03** - 14/08/13 - Added search function. Confirmed Android support.

**0.02** - 14/08/13 - Cleaned & commented code

**0.01** - 14/08/13 - Initial version
