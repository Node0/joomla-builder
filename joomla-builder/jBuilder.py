#!/usr/bin/env python3

import os, sh, shutil

class Jbuilder():
  def __init__(self):
    print("Assuming jBuilder.py is run from the 'joomla-builder' folder, if this is not the case please move jBuilder.py to the 'built-tools' folder and run it again.")
    os.chdir("../")
    self.basePath = os.getcwd()
    self.srcDirs = [ 'components', 'plugins', 'modules', 'libraries' ]
    self.buildsDir = f"{self.basePath}/builds"
    print(f"The base path is: {self.basePath}")
    self.lineSepThick = '==========================================================================='
    self.lineSepThin  = '---------------------------------------------------------------------------'

    # If ANY of the core extension-type source dirs specified in array above do not exist on the filesystem
    # exit with error message, without source folder mappings we cannot reliably populate ./builds with artifacts.
    for srcDir in self.srcDirs:
      if ( os.path.exists( srcDir ) ):
        print( f"Source directory {self.basePath}/{srcDir} exists" )
      else:
        print( f"ERROR The directory {self.basePath}/{srcDir} does not exist, EXITING." )
        exit(1)

    # Create and clean build dir
    if ( not os.path.exists(self.buildsDir) ):
      sh.mkdir("-p", self.buildsDir)
      os.chdir( self.buildsDir )
      print( f"{os.getcwd()} now exists" )
    else:
      os.chdir( self.buildsDir )
      thisDir = os.getcwd()
      for files in os.listdir( thisDir ):
        path = os.path.join( thisDir, files )
        try:
            shutil.rmtree( path )
        except OSError:
            os.remove( path )
      print( f"{os.getcwd()} is now cleaned and ready" )
      print(f"{self.lineSepThick}")


  def listdirs(self, folder):
    return [d for d in os.listdir(folder) if os.path.isdir(os.path.join(folder, d))]

  def removeDsStoreFiles(self):
    findDsStoreFilesStdout = sh.find(f"{self.basePath}", "-type", "f", "-name", ".DS_Store",  _iter=True )
    foundDsStoreFiles = findDsStoreFilesStdout.split('\n')
    foundDsStoreFiles.pop()
    if ( len(foundDsStoreFiles) > 0 ):
      print("Removing .DS_Store files...")
      for dsStoreFile in foundDsStoreFiles:
        sh.rm("-f", dsStoreFile )
        print(f"Removed {dsStoreFile}")

  def packageDirsInSrcDirs(self):
    for srcDir in self.srcDirs:
      if ( os.path.exists( f"{self.basePath}/{srcDir}" ) ):
        os.chdir( f"{self.basePath}/{srcDir}" )
        print(f"{self.lineSepThin}")
        print( f"Working in {os.getcwd()}" )
        # print( self.listdirs( f"{self.basePath}/{srcDir}" ) )
        for extension in self.listdirs( f"{self.basePath}/{srcDir}" ):
          sh.zip( "-r", f"{extension}.zip", f"{extension}" )
          sh.mv( f"{self.basePath}/{srcDir}/{extension}.zip", f"{self.buildsDir}"  )
          print(f"Packaged {extension} -> {extension}.zip and moved to ./builds folder. ")

  def execute(self):
    self.removeDsStoreFiles()
    self.packageDirsInSrcDirs()

JB = Jbuilder()
JB.execute()

