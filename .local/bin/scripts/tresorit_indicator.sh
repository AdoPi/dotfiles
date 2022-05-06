#!/bin/bash
# 
# Custom Tresorit indicator for polybar.
#
# Author: machaerus
# https://gitlab.com/machaerus

source colors.sh

tresorit_indicator() {
	TSTATUS=$(tresorit-cli status | head -1 | grep -oE '[^ ]+$')
	[ "$TSTATUS" = "running" ] && RUNNING=1 || RUNNING=0

	if [ "$RUNNING" -eq 1 ]; then
		TTRANSFERS=$(tresorit-cli transfers | grep syncing | wc -l)
		[ "$TTRANSFERS" -gt 0 ] && echo "$faded_yellow$RESET" || echo "$faded_green$RESET"
	else
		echo "$faded_red$RESET"
	fi
}

# tresorit_indicator
