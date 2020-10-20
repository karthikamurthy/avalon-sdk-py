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

WHEEL_FILE=dist/avalon_sdk-linux_x86_64.whl

all :
	python3 setup.py sdist bdist_wheel

clean:
	if [ -f $(WHEEL_FILE) ] ; then pip3 uninstall --yes $(WHEEL_FILE); fi
	rm -rf build deps dist *.egg-info
	find . -iname '*.pyc' -delete
	find . -iname '__pycache__' -delete

.PHONY : all
.PHONY : clean
.PHONY : install

