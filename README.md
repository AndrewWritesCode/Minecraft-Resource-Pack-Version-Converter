# How To To Use:
## GUI Use
- Be sure to install PyQt5 before running

1) Run mcrpc_app.py



## Terminal Use
- Note that you must unzip your resource packs before using them in any steps below

1) run fileMapper.py on a resource pack of the version of MC that you want to convert to
- This will create a JSON that describes how the resource pack assets are structured

2) run MinecraftVersionTranslator.py
- This will generate a JSON file based on the root directory of your out-dated resource pack, and will prompt your for the JSON generated in step 1

3) run mcrpc_termional.py
- This will take the JSON from step 2 and form the pack in the same directory as that JSON file
- You will need to change the pack.mcmeta pack format to the proper number (will be automatic soon)
- Zip the pack and it should be ready to work (so far I've only tested vanilla 1.12.2 => 1.16.5)
