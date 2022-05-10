#!/usr/bin/env python3

import os, sh, shutil
# Please ensure sh library is installed: pip3 install sh

class JBuilder():
  def __init__(self):
    print("Running with assumption that jBuilder.py is run from the 'joomla-builder' folder.\nif this is not the case please move jBuilder.py to the 'joomla-builder' folder and run it again.")
    os.chdir("../")
    self.basePath = os.getcwd()
    self.srcDirs = [ 'components', 'plugins', 'modules', 'libraries' ]
    self.buildsDir = f"{self.basePath}/builds"
    print(f"The base path is: {self.basePath}")
    self.lineSepThick = '==========================================================================='
    self.lineSepThin  = '---------------------------------------------------------------------------'

    # Ensure that all dirs listed in srcDirs actually exist, else exit with error
    for srcDir in self.srcDirs:
      if ( os.path.exists( srcDir ) ):
        print( f"Source directory {self.basePath}/{srcDir} exists" )
      else:
        print( f"ERROR The directory {self.basePath}/{srcDir} does not exist, EXITING." )
        exit(1)



  # Returns a list of folders one level deep from location where it's called
  def getTopLevelDirs(self, folder):
    return [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

  def packageDirsInSrcDirs(self):
    # For each extension folder type listed in self.srcDirs array
    for srcDir in self.srcDirs:
      if ( os.path.exists( f"{self.basePath}/{srcDir}" ) ):
        os.chdir( f"{self.basePath}/{srcDir}" )
        print(f"{self.lineSepThin}")
        print( f"Working in {os.getcwd()}..." )
        # Check for folders in this extension folder type (one level deep, assume each folder is a separate extension)
        for extension in self.getTopLevelDirs( f"{self.basePath}/{srcDir}" ):
          sh.zip( "-r", f"{extension}.zip", f"{extension}" )
          sh.mv( f"{self.basePath}/{srcDir}/{extension}.zip", f"{self.buildsDir}"  )
          print(f"Built {extension} as {extension}.zip, you can find it in the ./builds folder.")

  def execute(self):
    self.packageDirsInSrcDirs()

JB = JBuilder()
JB.execute()

