#!/bin/bash

export PYTHONPATH=`pwd`
pypy ../pox/pox.py --verbose load_flowtab
