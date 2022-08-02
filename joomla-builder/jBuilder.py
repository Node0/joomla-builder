#!/usr/bin/env python3

import os, sh, shutil

# A utility class for safely dealing with files
class Fileaccess():
  import traceback
  def __init__(self, file_name, mode = 'r'):
    if (os.path.exists(file_name)):
      self.file_name = file_name
    else:
      raise Exception(f"Filename parameter must be a valid file path")
    # mode can be r = read, w = write, a = append
    if (mode in [ 'r', 'w', 'a' ] ):
      self.mode = mode
    else:
      raise Exception(f"Passed mode must be one of r = read, w = write, a = append, instead found: {mode}")

  def __enter__(self):
    self.file = open(self.file_name, self.mode)
    return self.file

  def __exit__(self, exc_type, exc_value, traceback):
    self.file.close()
    if exc_type is not None:
      self.traceback.print_exception(exc_type, exc_value, traceback)
      return False

class Jbuilder():
  def __init__(self):
    print("Assuming jBuilder.py is run from the 'joomla-builder' folder, if this is not the case please move jBuilder.py to the 'built-tools' folder and run it again.")
    os.chdir("../")
    self.folderPermissions = "0755"
    self.filePermissions = "0644"
    self.basePath = os.getcwd()
    self.srcDirs = [ 'components', 'plugins', 'modules', 'libraries' ]
    self.buildsDir = f"{self.basePath}/builds"
    print(f"The base path is: {self.basePath}")
    self.lineSepThick = '==========================================================================='
    self.lineSepThin  = '---------------------------------------------------------------------------'
    self.lineDotted   = '...........................................................................'

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


  # Folder asset, file asset, and writer function helper
  def createFile(self, assetType = "f", targetPath = None, fileContents = None):
    filePerms = self.filePermissions if self.filePermissions else "0644"
    folderPerms = self.folderPermissions if self.folderPermissions else "0755"
    fileAsset = None
    directoryAsset = None

    if( assetType == "d" and targetPath == None):
      print("""You have chosen to create a directory WITHOUT providing a target path.\nPlease provide: createFileAndWriteContents(targetPath = "/path/of/desired/asset" """)
    elif ( assetType == "f" and targetPath == None):
      print("""You have chosen to create a file WITHOUT providing a target path.\nPlease provide: createFileAndWriteContents(targetPath = "/path/of/desired/asset" """)
    elif ( assetType == "f" and targetPath != None and type(targetPath) == str):
      fileAsset = targetPath
    elif ( assetType == "d" and targetPath != None and type(targetPath) == str):
      directoryAsset = targetPath

    # Create directory if not exists ("mkdir -p" will silently desist if dir exists)
    if ( type(directoryAsset) == str ):
      sh.mkdir("-p", f"{directoryAsset}")
      sh.chmod(folderPerms, directoryAsset)

      if ( os.path.exists(directoryAsset) ):
        print( f"Created dir: {directoryAsset}, with 755 permissions" )
      else:
        print( f"ERROR encountered in creating dir: {directoryAsset}" )
      return

    if ( type(fileAsset) == str ):

      # Create containing dir for file first
      targetPathArray = fileAsset.split("/")
      targetPathArray.pop()
      fileAssetContainingDir = "/".join(targetPathArray)
      sh.mkdir("-p", f"{fileAssetContainingDir}")

      # Create file and set perms to 644
      sh.touch(f"{fileAsset}")
      sh.chmod(filePerms, fileAsset)
      if ( os.path.exists(fileAsset) and fileContents != None ):
        with Fileaccess(fileAsset, 'w') as fileHandle:
          fileHandle.write(fileContents)

      if ( os.path.exists(fileAsset) ):
        if ( fileContents == None and os.path.getsize(fileAsset) == 0 ):
          print( f"Created file: {fileAsset}, with 644 permissions" )
        elif ( fileContents == None and os.path.getsize(fileAsset) != 0  ):
          print(f"ERROR empty file creation specified, but {fileAsset} is not empty, please verify")
        elif ( fileContents != None and os.path.getsize(fileAsset) > 0 ):
          print( f"""Created file: {fileAsset}, with 644 permissions, and wrote contents:{fileContents[0:85]}...""" )
          return

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
        if ( srcDir == 'libraries' ):
          for library in self.listdirs( f"{self.basePath}/{srcDir}" ):
            os.chdir( f"{self.basePath}/{srcDir}/{library}" )
            print( f"Working in {os.getcwd()}" )
            print( f"Compiling Core include file for {library}")
            print( f"{self.lineSepThin}")
            phpFileName = f"""{library}RequireHub.php"""
            phpFileNameFullPath = f"{self.basePath}/{srcDir}/{library}/{phpFileName}"
            phpFileContents = """<?php\n"""
            phpFileListStr = sh.find(".", "-type", "f", "-name", "*.php")
            phpFileList = phpFileListStr.split('\n')[0:-1]
            if ( len(phpFileList) > 0 ):
              phpFileContents += f"""/* Require Hub for the {library} library */\n"""
              for phpFilePath in phpFileList:
                if( phpFileName not in phpFilePath ):
                  phpFileContents += f"""require_once( dirname(__FILE__) . "/{phpFilePath.replace('./', '')}");\n"""
              # Done with concat loop, time to write the resulting string to our requireHub.php file.
              self.createFile(assetType = "f", targetPath = phpFileNameFullPath, fileContents = phpFileContents)
        # Step back OUT of this this specific library folder.
        os.chdir( f"{self.basePath}/{srcDir}" )

        # Done with special library auto-wiring, proceed as normal for other extension types.
        for extension in self.listdirs( f"{self.basePath}/{srcDir}" ):
          if ( srcDir == 'libraries' ):
            libExtension = f"lib_{extension}"
            sh.zip( "-r", f"{libExtension}.zip", f"{extension}" )
            sh.mv( f"{self.basePath}/{srcDir}/{libExtension}.zip", f"{self.buildsDir}"  )
            print(f"Packaged {extension} -> {libExtension}.zip and moved to ./builds folder. ")
          else:
            sh.zip( "-r", f"{extension}.zip", f"{extension}" )
            sh.mv( f"{self.basePath}/{srcDir}/{extension}.zip", f"{self.buildsDir}"  )
            print(f"Packaged {extension} -> {extension}.zip and moved to ./builds folder. ")

  def execute(self):
    self.removeDsStoreFiles()
    self.packageDirsInSrcDirs()

JB = Jbuilder()
JB.execute()

