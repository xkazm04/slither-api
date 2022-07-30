
import os
import subprocess
from packaging import version


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

    def get_installed_solc_versions(self):
        proc = subprocess.Popen(['solc-select', 'versions'], stdout=subprocess.PIPE)

        versions = []
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            solc_version = line.decode('utf-8').rstrip('b').rstrip()
            version_without_description = solc_version.split(' ')[0]
            versions.append(version_without_description)

        # filters versions where it does not start with integer
        versions = filter(lambda x: x[0].isdigit(), versions)
        versions = sorted(versions, key=lambda x: version.Version(x))
        return list(versions) 
    
    # installes same solc version as pragma version
    def install_solc_version(self,pragma_version:str):
        os.system(f"solc-select install {pragma_version}")
    
    # switches solc compiler to same version as pragmra version
    def switch_solc_to_version(self,pragma_version: str):
        os.system(f"solc-select use {pragma_version}")
    
    # isntalls multiple versions
    def install_solc_versions(self,versions: list):
        for version in versions:
            os.system(f"solc-select install {version}")
    
    # switches solc compiler to same version as pragmra version
    def switch_solc_to_version(self,pragma_version: str):
        os.system(f"solc-select use {pragma_version}")

compiler_helpers = SolcCompiler()


