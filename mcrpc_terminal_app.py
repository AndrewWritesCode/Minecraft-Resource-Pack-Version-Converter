import json2pack
from minecraft_version_translator import MinecraftVersionTranslator
from minecraft_version_translator import setup
import os


input_pack_data, reference_pack_data, reference_pack_path, input_pack_path, packname = setup()
MinecraftVersionTranslator(input_pack_data, reference_pack_data, input_pack_path, packname, reference_pack_path=reference_pack_path, mode='terminal')

print('You will need a .json file generated from minecraft_version_translator.py before running this script')
print('You will also need to be sure there is not a folder with the same name as your.json file in the same directory')
json2pack_path = input('What is the path of your .json file? ')

pack_path_root = json2pack_path.replace(os.path.basename(json2pack_path), '')
pack_folder = os.path.basename(json2pack_path)
pack_folder = os.path.splitext(pack_folder)[0]
pack_path_root = os.path.join(pack_path_root, pack_folder)

json2pack.json2pack('terminal', json2pack_path, pack_path_root)
