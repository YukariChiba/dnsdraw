#!/bin/bash

process_file() {
  sed -i 's/[,，]//g' $1
}
export -f process_file

find data/*.txt | xargs -I @ bash -c "process_file @"
