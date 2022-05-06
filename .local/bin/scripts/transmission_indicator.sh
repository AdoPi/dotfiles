#!/bin/bash
#
# Transmission indicator for polybar.
#
# THIS DOESN'T CURRENTLY WORK
#
# Author: machaerus
# https://gitlab.com/machaerus

source colors.sh

transmission_indicator() {

	TSTATUS=$(tresorit-cli status | head -1 | grep -oE '[^ ]+$')
	[ "$TSTATUS" = "running" ] && RUNNING=1 || RUNNING=0

	if [ "$RUNNING" -eq 1 ]; then
		TTRANSFERS=$(tresorit-cli transfers | grep syncing | wc -l)
		[ "$TTRANSFERS" -gt 0 ] && echo "$bright_yellow$RESET" || echo "$bright_green$RESET"
	else
		echo "$bright_red$RESET"
	fi
}

transmission_indicator
