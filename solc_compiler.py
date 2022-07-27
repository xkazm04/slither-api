
import os
import subprocess


# class for encapsulatin solc compiler related functs
class SolcCompiler:
    # get all available solc versions to install then on server bootsrap
    def get_solc_versions(self):
        proc = subprocess.Popen(['solc-select', 'install'], stdout=subprocess.PIPE)

        versions = []
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            version = line.decode('utf-8').rstrip('b').rstrip()
            versions.append(version)

        # filters versions where it does not start with integer
        filtered_versions = filter(lambda x: x[0].isdigit(), versions)
        return list(filtered_versions)
    
    # installes same solc version as pragma version
    def install_solc_version(self,pragma_version:str):
        os.system(f"solc-select install {pragma_version}")
    
    # switches solc compiler to same version as pragmra version
    def switch_solc_to_version(self,pragma_version: str):
        os.system(f"solc-select use {pragma_version}")
    
    def install_solc_versions(self,versions: list):
        for version in versions:
            os.system(f"solc-select install {version}")
    
    # switches solc compiler to same version as pragmra version
    def switch_solc_to_version(self,pragma_version: str):
        os.system(f"solc-select use {pragma_version}")




