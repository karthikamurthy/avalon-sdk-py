#!/usr/bin/env python

# Copyright 2020 Intel Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import sys
import subprocess
import re


from setuptools import setup, find_packages, Extension

include_dirs = [ "common/enums/proxy"]
setup(name='avalon_sdk_fabric',
      version='0.0.4',
      description='Avalon SDK ',
      author='Hyperledger Avalon ',
      author_email="karthika.murthy@intel.com",                                               
      url='https://github.com/hyperledger/avalon_sdk_py',       
      package_dir = {'enums' : 'common/enums',
                     'enums.proxy' : 'common/enums/proxy',
                     'handler' : 'internal/handler/proxy',
                     'interfaces' : 'common/interfaces',
                     'exceptions' : 'internal/exceptions',
                     'exceptions.proxy' : 'internal/exceptions/proxy',
                     'validation' : 'internal/validation',
                     'validation.proxy' : 'internal/validation/proxy',
                     'utility' : 'common/utility',
                     'avalon_sdk_fabric' : 'avalon_sdk_proxy/fabric'
                     
                    }, 
      
      packages=['enums',
                'enums.proxy',
                'handler', 
                'interfaces',
                'exceptions',
                'exceptions.proxy',
                'validation',
                'validation.proxy',
                'utility',
                'avalon_sdk_fabric'
               ],
        
      package_data={'validation': ['data/*.json'],
                    'avalon_sdk_fabric': ['fabric_chaincode/order/go/*.go',
                                          'fabric_chaincode/receipt/go/*.go',
                                          'fabric_chaincode/registry/go/*.go',
                                          'fabric_chaincode/worker/go/*.go',
                                          'fabric_chaincode/order/go/go.mod',
                                          'fabric_chaincode/receipt/go/go.mod',
                                          'fabric_chaincode/registry/go/go.mod',
                                          'fabric_chaincode/worker/go/go.mod']},
      data_files=[('/avalon_sdk', ['avalon_sdk_proxy/fabric/network.json','avalon_sdk_proxy/fabric/methods.json',])],
      include_dirs = include_dirs,
      include_package_data=True,
      install_requires=['fabric-sdk-py'],
      entry_points={})
