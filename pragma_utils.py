import re
from solc_compiler import SolcCompiler
from packaging import version

class Pragma: 
    # injects Solc Compiler
    def __init__(self, solc: SolcCompiler) -> None:
        self.solc_compiler = solc

    # finds first matched version (pragma solidity >=0.6.12 <0.6.10) 
    def get_version(self, pragma_version: str)-> str | None:
        version_regex = '\d{1,2}\.\d{1}\.\d{1,2}'
        versions = re.findall(version_regex, pragma_version)
        if len(versions) > 0:
            return versions[0] 
        else:
            return None

    def get_higher_version(self, pragma_version: str, installed_versions: list) -> str:
        for v in installed_versions:
            if version.parse(v) > version.parse(pragma_version):
                return v


    def find_correct_version(self, pragma_version: str) -> str:
        file_pragma_version = self.get_version(pragma_version)

        installed_solc_versions = self.solc_compiler.get_installed_solc_versions()
        version_exists = file_pragma_version in installed_solc_versions

        if not version_exists:
            return self.get_higher_version(file_pragma_version, installed_solc_versions)
        else:
            return file_pragma_version