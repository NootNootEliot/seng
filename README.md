# Seng
Seng is a Discord Bot which currently helps, in particular, the Astra Nova
Network.

### Installation for Development
1. Clone this repository to your local machine.
2. Install `poetry`, the dependency manager that Seng uses.
    - To install `poetry`, check their [documentation](https://python-poetry.org/).
3. `cd` into this project's main directory.
4. Run `poetry install`.
5. Run `poetry shell`.
6. See Set-Up instructions below.

### Set-Up: General
 - To test locally, you will need to create a 'Bot' application within the
 [Discord Developer Portal](https://discord.com/developers/docs/intro).
 - To use any encryption/decryption features, please install
 [age](https://github.com/FiloSottile/age) onto your local machine. For more
 info, please see the **Using Encryption/Decryption features** section.

### Set-Up: Without a data pack
 - If you do not have a data pack, then you may want to consider using
 `config/load_template_files` which will load template files into the seng
 directory. Following this, please edit the template files with the correct
 data.
 - You can run `config/file_check.py` for a check that files are in the right
 places, amongst other things. This is handy for checking that the template
 files have been correctly filled out.

### Set-Up: With a data pack
 - If you have a data pack, it should be encrypted. Please place it at
 `seng/data_pack.tar.gz.age`.
 - Please check the **Encryption/Decryption features** section for where to
 place the private key.
 - Then run `config/load_data_pack.py` to load its files into the seng 
 directory.
 - Then run`config/file_check.py` for a check that files are in the right
 places, amongst other things.

### Using Encryption/Decryption features
 - If you would like to use Encryption/Decryption features of Seng, which are
 just for exporting and importing `data_pack`s (which are files that an
 instance of Seng stores), then please place `key.txt` (which should be the 
 private key from `age` key generation) within the `private` directory, as well
 as placing `public_key.txt` (which is a copy-and-paste of the public key from
 the `age` key generation) in the `private` directory too.
 - `config/create_data_pack.py` can be used to create an encrypted data pack.

 ### Contribution Info
 - Thank you for taking an interest in contributing to Seng!
 - Please read `CONTRIBUTING.md` for more information on how to contribute.
