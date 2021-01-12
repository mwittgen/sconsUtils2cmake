# -*- python -*-

import importlib.util
import builtins
import importlib.machinery
import yaml
from pathlib import Path


global_config=dict()
global_config["libs"]=list()

class lsst:
    class sconsUtils:
        class Configuration:
            def __init__(self,cfgFile, headers=(), libs=None, hasSwigFiles=True,
                 includeFileDirs=["include"], libFileDirs=["lib"],
                 hasDoxygenInclude=False, hasDoxygenTag=True, eupsProduct=None):
                self.cfgFile=cfgFile
                self.headers=headers
                self.libs=libs
                self.hasSwigFiles=hasSwigFiles
                self.includeFileDirs=includeFileDirs
                self.libFileDirs=libFileDirs
                self.hasDoxygenInclude=hasDoxygenInclude
                self.hasDoxygenTag=hasDoxygenTag
                self.eupsProduct=eupsProduct
        class targets:
            pass
        class env:
            pass
        class scripts:
            class BasicSConscript:
                @staticmethod
                def lib(libName=None, src=None, libs="self", noBuildList=None):
                    d=dict()
                    d["libName"]=libName
                    d["src"]=src
                    d["libs"]=libs
                    d["noBuildList"]=noBuildList
                    if libName is None:
                        d["libName"] = global_config["packageName"]              
                    if src is None:
                        d["src"] = [str(p) for p in Path('src').glob('**/*.cc')]                 
                    global_config["libs"].append(d)
                @staticmethod
                def shebang(src=None):
                    self.src=src
                @staticmethod
                def python(module=None, src=None, extra=(), libs="main python"):
                    self.module=module
                    self.src=src
                    self.extra=extra
                    self.libs=libs
                @staticmethod
                def pybind11(nameList=[], libs="main python", extraSrc=None, addUnderscore=True):
                    self.nameList=nameList
                    self.libs=libs
                    self.extraSrc=extraSrc
                    self.addUnderscore=addUnderscore
                @staticmethod
                def doc(config="doxygen.conf.in", projectName=None, projectNumber=None, **kwargs):
                    self.config=config
                    self.projectName=projectName
                    self.projectNumber=projectNumber
                @staticmethod
                def tests(pyList=None, ccList=None, swigNameList=None, swigSrc=None,
                          ignoreList=None, noBuildList=None, pySingles=None,
                          args=None):
                    self.pyList=pyList
                    self.ccList=ccList
                    self.swigNameList=swigNameList
                    self.swigSrc=swigSrc
                    self.ignoreList=ignoreList
                    self.noBuildList=noBuildList
                    self.pySingles=noBuildList       
                    self.args=args
                @staticmethod
                def examples(ccList=None, swigNameList=None, swigSrc=None):
                    self.ccList=ccList
                    self.swigNameList=swigNameList
                    self.swigSrc=swigSrc
            class BasicSConstruct:
                def __init__(self,packageName):
                    global_config["packageName"]=packageName

                

realimp = builtins.__import__
def cmake_import(name, globals={}, locals={}, fromlist=[],level=-1):
  print(name,fromlist)
  if(name.startswith("lsst.sconsUtils")):
      if(fromlist is None):
          return lsst
      else:
          return lsst.sconsUtils
  return realimp(name, globals, locals, fromlist)
builtins.__import__ = cmake_import

def load(namespace,filename):
    loader = importlib.machinery.SourceFileLoader(namespace,filename)
    mod = loader.load_module()
    return mod


project=load("project","SConstruct")
config=load("ups_config",'ups/afw.cfg')
lib=load("lib","lib/SConscript")
global_config["config"]=config.config
global_config["dependencies"]=config.dependencies

for file_path in Path('.').glob('**/SConscript'):
    print(file_path)

print(yaml.dump(global_config))





