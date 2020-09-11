#!/bin/bash

python3 -c "from datablox import datablox_agent; da = datablox_agent('dylan', db_directory = '/tmp/datablox'); da.serve();";