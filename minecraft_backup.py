import os
import zipfile
import datetime
import argparse
import shutil
import getpass
import platform

class directoriesModel:
  worldFolder: str = ''
  destination: str = ''

class minecraftWorldsModel:
  paths = []
  worldCount: int = 0
  
def parse_args(worldFolder: str, destination: str):
  usage_message='Usage: ' + ' python minecraft_backup.py -w <path to minecraftWorlds> -d <path to backup destination>'
  parser = argparse.ArgumentParser('python minecraft_backup.py', usage=usage_message)
  parser.add_argument('-w', '--world', type=str,
    help='Location of the minecraftWorlds folder to back up. \
      The default location will be specific to Minecraft \
      Windows 10. You will need to specify this argument if you \
      want to use a different location.')
  parser.add_argument('-d', '--destination', type=str,
    help='Destination folder to backup to.')

  args = parser.parse_args()
  model = directoriesModel()
  model.destination = args.destination if args.destination else destination
  model.worldFolder = args.world if args.world else worldFolder

  # TODO: validate that the given path is a valid minecraftWorlds directory
  if not os.path.isdir(model.worldFolder):
    print ('the given worldFolder is not a valid minecraftWorlds directory. exiting...')
    exit()

  if not os.path.isdir(model.destination):
    print ('the given destination is not a valid directory. exiting...')
    exit()

  return model
  
def build_worlds_model(dirName):  # figure out what we are backing up
  model = minecraftWorldsModel()

  for root, directories, files in os.walk(dirName):
    for directory in directories:
      if directory not in ['db', 'texts', 'behavior_packs', 'resource_packs', 'lost']:
        model.worldCount += 1
    for file in files:
      filePath = os.path.join(root, file)
      model.paths.append(filePath)

  return model

def main(directoriesModel: directoriesModel):
  now = str(datetime.datetime.today().date())
  zipBaseName = directoriesModel.worldFolder.split('\\')[-1]
  zipArchive = zipBaseName + '_' + platform.node() + '_' + now + '.zip'
  os.chdir(directoriesModel.worldFolder)
  worldsModel = build_worlds_model('.')

  print('')
  print('zipping', worldsModel.worldCount, 'worlds into ' + zipArchive + '...')
  with zipfile.ZipFile(zipArchive, 'w') as zip_file:
    for file in worldsModel.paths:
      zip_file.write(file)

  print('...zipped!')
  print('')
  print('uploading to backup location...')
  shutil.move(zipArchive, directoriesModel.destination)
  print(zipArchive + ' uploaded to ' + directoriesModel.destination)
  print('')

  # TODO: need to throw away some older ones maybe?

  print('...finished.')

if __name__ == '__main__':
  worldFolder = 'C:\\Users\\' + getpass.getuser() + '\\AppData\\Local\\Packages\\\
Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang\\minecraftWorlds'  # Folder to backup
  destination = ''

  directoriesModel = parse_args(worldFolder, destination)
  main(directoriesModel)