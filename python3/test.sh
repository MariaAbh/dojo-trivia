#!/bin/bash

do_test () {
	seed=${1}
	orig="tests/${seed}.start.txt"
	now="tests/${seed}.now.txt"

	timeout 5 python3 ./trivia.py "${seed}" > "${now}"
	if [ "$?" = "124" ]
	then
		echo "${seed}	TIMEOUT"
	elif diff "${orig}" "${now}" > /dev/null 2>/dev/null
	then
		echo "${seed}	OK"
	else
		echo "${seed}	FAILED"
	fi
}

all_test () {
	for i in $(seq 255)
	do
		do_test ${i} &
	done
	wait
}
if [ $# != 0 ]
then
	while [ $# != 0 ]
	do
		do_test ${1}
		diff tests/${1}.start.txt tests/${1}.now.txt
		shift
	done
	exit
fi
all_test | tee outtest.txt

sort -n outtest.txt | tee ordered.txt

grep -v 'OK' ordered.txt > failed.txt
nfailed=$(cat failed.txt | wc -l)
if [ "${nfailed}" != 0 ]
then
	echo
	echo FAILED
	cat failed.txt

	echo "${nfailed} failed tests"
fi

rm outtest.txt
rm ordered.txt
rm failed.txt
