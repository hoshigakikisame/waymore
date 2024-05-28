#!/bin/bash

cat $1 | urldedupe | tee "$2/urldedupe.$1" && rm -rf $1
