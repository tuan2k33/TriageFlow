#!/bin/sh
# Proposed actions for numpy/numpy. Review report.md, then remove the leading '# ' from the lines you agree with.

# --- Open issues already marked as duplicates (10)
# gh issue close 4217 -R numpy/numpy --reason "not planned" --comment "Duplicate of #9208"   # 1.00
# gh issue close 8352 -R numpy/numpy --reason "not planned" --comment "Duplicate of #16785"   # 1.00
# gh issue close 8734 -R numpy/numpy --reason "not planned" --comment "Duplicate of #16384"   # 1.00
# gh issue close 8969 -R numpy/numpy --reason "not planned" --comment "Duplicate of #11681"   # 1.00
# gh issue close 8969 -R numpy/numpy --reason "not planned" --comment "Duplicate of #12725"   # 1.00
# gh issue close 10374 -R numpy/numpy --reason "not planned" --comment "Duplicate of #17021"   # 1.00
# gh issue close 13878 -R numpy/numpy --reason "not planned" --comment "Duplicate of #14427"   # 1.00
# gh issue close 14402 -R numpy/numpy --reason "not planned" --comment "Duplicate of #18000"   # 1.00
# gh issue close 15581 -R numpy/numpy --reason "not planned" --comment "Duplicate of #28097"   # 1.00
# gh issue close 15981 -R numpy/numpy --reason "not planned" --comment "Duplicate of #19168"   # 1.00

# --- Open issues whose closing PR is merged (9)
# gh issue close 4043 -R numpy/numpy --reason completed --comment "Closed by #4045"   # 0.99
# gh issue close 4959 -R numpy/numpy --reason completed --comment "Closed by #16022"   # 0.99
# gh issue close 8720 -R numpy/numpy --reason completed --comment "Closed by #9986"   # 0.99
# gh issue close 12974 -R numpy/numpy --reason completed --comment "Closed by #13305"   # 0.99
# gh issue close 13088 -R numpy/numpy --reason completed --comment "Closed by #13397"   # 0.99
# gh issue close 15200 -R numpy/numpy --reason completed --comment "Closed by #16022"   # 0.99
# gh issue close 21213 -R numpy/numpy --reason completed --comment "Closed by #21218"   # 0.99
# gh issue close 29524 -R numpy/numpy --reason completed --comment "Closed by #29539"   # 0.99
# gh issue close 30440 -R numpy/numpy --reason completed --comment "Closed by #31113"   # 0.99

# --- Likely duplicates of an older open issue (48)
# gh issue close 20022 -R numpy/numpy --reason "not planned" --comment "Duplicate of #6661"   # 0.97
# gh issue close 6083 -R numpy/numpy --reason "not planned" --comment "Duplicate of #6082"   # 0.95
# gh issue close 17310 -R numpy/numpy --reason "not planned" --comment "Duplicate of #12283"   # 0.95
# gh issue close 21147 -R numpy/numpy --reason "not planned" --comment "Duplicate of #15499"   # 0.94
# gh issue close 21944 -R numpy/numpy --reason "not planned" --comment "Duplicate of #4332"   # 0.94
# gh issue close 23187 -R numpy/numpy --reason "not planned" --comment "Duplicate of #18881"   # 0.94
# gh issue close 23273 -R numpy/numpy --reason "not planned" --comment "Duplicate of #20351"   # 0.94
# gh issue close 28795 -R numpy/numpy --reason "not planned" --comment "Duplicate of #5976"   # 0.94
# gh issue close 30258 -R numpy/numpy --reason "not planned" --comment "Duplicate of #14624"   # 0.94
# gh issue close 30342 -R numpy/numpy --reason "not planned" --comment "Duplicate of #8207"   # 0.94
# gh issue close 30985 -R numpy/numpy --reason "not planned" --comment "Duplicate of #29201"   # 0.94
# gh issue close 6070 -R numpy/numpy --reason "not planned" --comment "Duplicate of #5353"   # 0.93
# gh issue close 14277 -R numpy/numpy --reason "not planned" --comment "Duplicate of #8875"   # 0.93
# gh issue close 16380 -R numpy/numpy --reason "not planned" --comment "Duplicate of #4554"   # 0.93
# gh issue close 17744 -R numpy/numpy --reason "not planned" --comment "Duplicate of #6051"   # 0.93
# gh issue close 18519 -R numpy/numpy --reason "not planned" --comment "Duplicate of #5236"   # 0.93
# gh issue close 20226 -R numpy/numpy --reason "not planned" --comment "Duplicate of #2457"   # 0.93
# gh issue close 21539 -R numpy/numpy --reason "not planned" --comment "Duplicate of #9023"   # 0.93
# gh issue close 22141 -R numpy/numpy --reason "not planned" --comment "Duplicate of #5613"   # 0.93
# gh issue close 22881 -R numpy/numpy --reason "not planned" --comment "Duplicate of #9450"   # 0.93
# gh issue close 24897 -R numpy/numpy --reason "not planned" --comment "Duplicate of #13105"   # 0.93
# gh issue close 28602 -R numpy/numpy --reason "not planned" --comment "Duplicate of #9009"   # 0.93
# gh issue close 28946 -R numpy/numpy --reason "not planned" --comment "Duplicate of #15770"   # 0.93
# gh issue close 29071 -R numpy/numpy --reason "not planned" --comment "Duplicate of #11686"   # 0.93
# gh issue close 30171 -R numpy/numpy --reason "not planned" --comment "Duplicate of #29071"   # 0.93
# gh issue close 30349 -R numpy/numpy --reason "not planned" --comment "Duplicate of #10926"   # 0.93
# gh issue close 33219 -R numpy/numpy --reason "not planned" --comment "Duplicate of #21944"   # 0.93
# gh issue close 7730 -R numpy/numpy --reason "not planned" --comment "Duplicate of #6971"   # 0.92
# gh issue close 9023 -R numpy/numpy --reason "not planned" --comment "Duplicate of #6661"   # 0.92
# gh issue close 13683 -R numpy/numpy --reason "not planned" --comment "Duplicate of #5972"   # 0.92
# gh issue close 16159 -R numpy/numpy --reason "not planned" --comment "Duplicate of #13349"   # 0.92
# gh issue close 17408 -R numpy/numpy --reason "not planned" --comment "Duplicate of #4440"   # 0.92
# gh issue close 19039 -R numpy/numpy --reason "not planned" --comment "Duplicate of #9331"   # 0.92
# gh issue close 20586 -R numpy/numpy --reason "not planned" --comment "Duplicate of #15601"   # 0.92
# gh issue close 21787 -R numpy/numpy --reason "not planned" --comment "Duplicate of #4965"   # 0.92
# gh issue close 22182 -R numpy/numpy --reason "not planned" --comment "Duplicate of #14804"   # 0.92
# gh issue close 23574 -R numpy/numpy --reason "not planned" --comment "Duplicate of #14396"   # 0.92
# gh issue close 24689 -R numpy/numpy --reason "not planned" --comment "Duplicate of #8352"   # 0.92
# gh issue close 25235 -R numpy/numpy --reason "not planned" --comment "Duplicate of #11723"   # 0.92
# gh issue close 25363 -R numpy/numpy --reason "not planned" --comment "Duplicate of #15726"   # 0.92
# gh issue close 26145 -R numpy/numpy --reason "not planned" --comment "Duplicate of #5657"   # 0.92
# gh issue close 26177 -R numpy/numpy --reason "not planned" --comment "Duplicate of #8449"   # 0.92
# gh issue close 26779 -R numpy/numpy --reason "not planned" --comment "Duplicate of #23694"   # 0.92
# gh issue close 27588 -R numpy/numpy --reason "not planned" --comment "Duplicate of #20850"   # 0.92
# gh issue close 29117 -R numpy/numpy --reason "not planned" --comment "Duplicate of #17310"   # 0.92
# gh issue close 31868 -R numpy/numpy --reason "not planned" --comment "Duplicate of #27258"   # 0.92
# gh issue close 32372 -R numpy/numpy --reason "not planned" --comment "Duplicate of #8775"   # 0.92
# gh issue close 33203 -R numpy/numpy --reason "not planned" --comment "Duplicate of #6854"   # 0.92

# --- Open issues very similar to an older closed one (came back, or a duplicate of something settled?) (67)
# gh issue view 32270 -R numpy/numpy; gh issue view 32272 -R numpy/numpy   # 0.97
# gh issue view 9769 -R numpy/numpy; gh issue view 9775 -R numpy/numpy   # 0.96
# gh issue view 19307 -R numpy/numpy; gh issue view 19308 -R numpy/numpy   # 0.96
# gh issue view 17697 -R numpy/numpy; gh issue view 25677 -R numpy/numpy   # 0.95
# gh issue view 26387 -R numpy/numpy; gh issue view 27250 -R numpy/numpy   # 0.95
# gh issue view 8192 -R numpy/numpy; gh issue view 28920 -R numpy/numpy   # 0.95
# gh issue view 31686 -R numpy/numpy; gh issue view 31926 -R numpy/numpy   # 0.95
# gh issue view 8192 -R numpy/numpy; gh issue view 9331 -R numpy/numpy   # 0.94
# gh issue view 7622 -R numpy/numpy; gh issue view 15726 -R numpy/numpy   # 0.94
# gh issue view 15041 -R numpy/numpy; gh issue view 17224 -R numpy/numpy   # 0.94
# gh issue view 8878 -R numpy/numpy; gh issue view 21791 -R numpy/numpy   # 0.94
# gh issue view 13983 -R numpy/numpy; gh issue view 22217 -R numpy/numpy   # 0.94
# gh issue view 3887 -R numpy/numpy; gh issue view 24050 -R numpy/numpy   # 0.94
# gh issue view 3508 -R numpy/numpy; gh issue view 28839 -R numpy/numpy   # 0.94
# gh issue view 26254 -R numpy/numpy; gh issue view 31210 -R numpy/numpy   # 0.94
# gh issue view 4903 -R numpy/numpy; gh issue view 5041 -R numpy/numpy   # 0.93
# gh issue view 1989 -R numpy/numpy; gh issue view 7329 -R numpy/numpy   # 0.93
# gh issue view 4445 -R numpy/numpy; gh issue view 7330 -R numpy/numpy   # 0.93
# gh issue view 6040 -R numpy/numpy; gh issue view 9465 -R numpy/numpy   # 0.93
# gh issue view 7462 -R numpy/numpy; gh issue view 10004 -R numpy/numpy   # 0.93
# gh issue view 5903 -R numpy/numpy; gh issue view 11881 -R numpy/numpy   # 0.93
# gh issue view 8323 -R numpy/numpy; gh issue view 12098 -R numpy/numpy   # 0.93
# gh issue view 8769 -R numpy/numpy; gh issue view 13011 -R numpy/numpy   # 0.93
# gh issue view 7225 -R numpy/numpy; gh issue view 14828 -R numpy/numpy   # 0.93
# gh issue view 10118 -R numpy/numpy; gh issue view 16499 -R numpy/numpy   # 0.93
# gh issue view 8316 -R numpy/numpy; gh issue view 16665 -R numpy/numpy   # 0.93
# gh issue view 3207 -R numpy/numpy; gh issue view 17118 -R numpy/numpy   # 0.93
# gh issue view 2612 -R numpy/numpy; gh issue view 17305 -R numpy/numpy   # 0.93
# gh issue view 15199 -R numpy/numpy; gh issue view 18147 -R numpy/numpy   # 0.93
# gh issue view 7944 -R numpy/numpy; gh issue view 19205 -R numpy/numpy   # 0.93
# gh issue view 12738 -R numpy/numpy; gh issue view 19472 -R numpy/numpy   # 0.93
# gh issue view 7355 -R numpy/numpy; gh issue view 20514 -R numpy/numpy   # 0.93
# gh issue view 16208 -R numpy/numpy; gh issue view 21065 -R numpy/numpy   # 0.93
# gh issue view 18442 -R numpy/numpy; gh issue view 23500 -R numpy/numpy   # 0.93
# gh issue view 22985 -R numpy/numpy; gh issue view 23546 -R numpy/numpy   # 0.93
# gh issue view 3927 -R numpy/numpy; gh issue view 25548 -R numpy/numpy   # 0.93
# gh issue view 6078 -R numpy/numpy; gh issue view 25623 -R numpy/numpy   # 0.93
# gh issue view 24660 -R numpy/numpy; gh issue view 26078 -R numpy/numpy   # 0.93
# gh issue view 21782 -R numpy/numpy; gh issue view 26401 -R numpy/numpy   # 0.93
# gh issue view 26596 -R numpy/numpy; gh issue view 26761 -R numpy/numpy   # 0.93
# gh issue view 17038 -R numpy/numpy; gh issue view 27498 -R numpy/numpy   # 0.93
# gh issue view 19552 -R numpy/numpy; gh issue view 27985 -R numpy/numpy   # 0.93
# gh issue view 4107 -R numpy/numpy; gh issue view 28104 -R numpy/numpy   # 0.93
# gh issue view 18748 -R numpy/numpy; gh issue view 28371 -R numpy/numpy   # 0.93
# gh issue view 3213 -R numpy/numpy; gh issue view 5613 -R numpy/numpy   # 0.92
# gh issue view 6753 -R numpy/numpy; gh issue view 8987 -R numpy/numpy   # 0.92
# gh issue view 5775 -R numpy/numpy; gh issue view 10496 -R numpy/numpy   # 0.92
# gh issue view 5110 -R numpy/numpy; gh issue view 10520 -R numpy/numpy   # 0.92
# gh issue view 8664 -R numpy/numpy; gh issue view 14804 -R numpy/numpy   # 0.92
# gh issue view 10092 -R numpy/numpy; gh issue view 15978 -R numpy/numpy   # 0.92
# gh issue view 14659 -R numpy/numpy; gh issue view 18700 -R numpy/numpy   # 0.92
# gh issue view 14883 -R numpy/numpy; gh issue view 19146 -R numpy/numpy   # 0.92
# gh issue view 9393 -R numpy/numpy; gh issue view 20684 -R numpy/numpy   # 0.92
# gh issue view 3502 -R numpy/numpy; gh issue view 21280 -R numpy/numpy   # 0.92
# gh issue view 8546 -R numpy/numpy; gh issue view 22197 -R numpy/numpy   # 0.92
# gh issue view 21105 -R numpy/numpy; gh issue view 22609 -R numpy/numpy   # 0.92
# gh issue view 5681 -R numpy/numpy; gh issue view 22956 -R numpy/numpy   # 0.92
# gh issue view 18294 -R numpy/numpy; gh issue view 23305 -R numpy/numpy   # 0.92
# gh issue view 11142 -R numpy/numpy; gh issue view 24836 -R numpy/numpy   # 0.92
# gh issue view 16609 -R numpy/numpy; gh issue view 24976 -R numpy/numpy   # 0.92
# gh issue view 5819 -R numpy/numpy; gh issue view 25606 -R numpy/numpy   # 0.92
# gh issue view 24430 -R numpy/numpy; gh issue view 26861 -R numpy/numpy   # 0.92
# gh issue view 28438 -R numpy/numpy; gh issue view 29125 -R numpy/numpy   # 0.92
# gh issue view 23286 -R numpy/numpy; gh issue view 29336 -R numpy/numpy   # 0.92
# gh issue view 27325 -R numpy/numpy; gh issue view 31037 -R numpy/numpy   # 0.92
# gh issue view 11361 -R numpy/numpy; gh issue view 31485 -R numpy/numpy   # 0.92
# gh issue view 32414 -R numpy/numpy; gh issue view 32431 -R numpy/numpy   # 0.92

# --- Open issues that a later merged PR seems to fix (69)
# gh issue close 24568 -R numpy/numpy --reason completed --comment "Looks fixed by #24745"   # 0.95
# gh issue close 28205 -R numpy/numpy --reason completed --comment "Looks fixed by #28221"   # 0.95
# gh issue close 33240 -R numpy/numpy --reason completed --comment "Looks fixed by #33241"   # 0.95
# gh issue close 14624 -R numpy/numpy --reason completed --comment "Looks fixed by #30617"   # 0.94
# gh issue close 15726 -R numpy/numpy --reason completed --comment "Looks fixed by #32640"   # 0.94
# gh issue close 17310 -R numpy/numpy --reason completed --comment "Looks fixed by #31069"   # 0.94
# gh issue close 29349 -R numpy/numpy --reason completed --comment "Looks fixed by #30855"   # 0.94
# gh issue close 9394 -R numpy/numpy --reason completed --comment "Looks fixed by #21977"   # 0.93
# gh issue close 14225 -R numpy/numpy --reason completed --comment "Looks fixed by #14252"   # 0.93
# gh issue close 21070 -R numpy/numpy --reason completed --comment "Looks fixed by #21567"   # 0.93
# gh issue close 28046 -R numpy/numpy --reason completed --comment "Looks fixed by #29394"   # 0.93
# gh issue close 4422 -R numpy/numpy --reason completed --comment "Looks fixed by #8364"   # 0.92
# gh issue close 15978 -R numpy/numpy --reason completed --comment "Looks fixed by #21812"   # 0.92
# gh issue close 23180 -R numpy/numpy --reason completed --comment "Looks fixed by #31755"   # 0.92
# gh issue close 28463 -R numpy/numpy --reason completed --comment "Looks fixed by #28524"   # 0.92
# gh issue close 29336 -R numpy/numpy --reason completed --comment "Looks fixed by #29372"   # 0.92
# gh issue close 32063 -R numpy/numpy --reason completed --comment "Looks fixed by #33225"   # 0.92
# gh issue close 4301 -R numpy/numpy --reason completed --comment "Looks fixed by #10658"   # 0.91
# gh issue close 4560 -R numpy/numpy --reason completed --comment "Looks fixed by #30163"   # 0.91
# gh issue close 9818 -R numpy/numpy --reason completed --comment "Looks fixed by #26292"   # 0.91
# gh issue close 13831 -R numpy/numpy --reason completed --comment "Looks fixed by #14170"   # 0.91
# gh issue close 15692 -R numpy/numpy --reason completed --comment "Looks fixed by #24981"   # 0.91
# gh issue close 25134 -R numpy/numpy --reason completed --comment "Looks fixed by #26706"   # 0.91
# gh issue close 25936 -R numpy/numpy --reason completed --comment "Looks fixed by #26136"   # 0.91
# gh issue close 31030 -R numpy/numpy --reason completed --comment "Looks fixed by #31045"   # 0.91
# gh issue close 2494 -R numpy/numpy --reason completed --comment "Looks fixed by #9458"   # 0.90
# gh issue close 5617 -R numpy/numpy --reason completed --comment "Looks fixed by #12609"   # 0.90
# gh issue close 5669 -R numpy/numpy --reason completed --comment "Looks fixed by #31271"   # 0.90
# gh issue close 5976 -R numpy/numpy --reason completed --comment "Looks fixed by #7987"   # 0.90
# gh issue close 8994 -R numpy/numpy --reason completed --comment "Looks fixed by #23240"   # 0.90
# gh issue close 10003 -R numpy/numpy --reason completed --comment "Looks fixed by #29534"   # 0.90
# gh issue close 11569 -R numpy/numpy --reason completed --comment "Looks fixed by #18183"   # 0.90
# gh issue close 18244 -R numpy/numpy --reason completed --comment "Looks fixed by #30992"   # 0.90
# gh issue close 19205 -R numpy/numpy --reason completed --comment "Looks fixed by #30879"   # 0.90
# gh issue close 22217 -R numpy/numpy --reason completed --comment "Looks fixed by #27335"   # 0.90
# gh issue close 24084 -R numpy/numpy --reason completed --comment "Looks fixed by #24138"   # 0.90
# gh issue close 24345 -R numpy/numpy --reason completed --comment "Looks fixed by #29819"   # 0.90
# gh issue close 25606 -R numpy/numpy --reason completed --comment "Looks fixed by #27807"   # 0.90
# gh issue close 27038 -R numpy/numpy --reason completed --comment "Looks fixed by #32798"   # 0.90
# gh issue close 28596 -R numpy/numpy --reason completed --comment "Looks fixed by #29557"   # 0.90
# gh issue close 29125 -R numpy/numpy --reason completed --comment "Looks fixed by #29212"   # 0.90
# gh issue close 29703 -R numpy/numpy --reason completed --comment "Looks fixed by #29704"   # 0.90
# gh issue close 31866 -R numpy/numpy --reason completed --comment "Looks fixed by #32041"   # 0.90
# gh issue close 33276 -R numpy/numpy --reason completed --comment "Looks fixed by #33303"   # 0.90
# gh issue close 4983 -R numpy/numpy --reason completed --comment "Looks fixed by #11694"   # 0.89
# gh issue close 7588 -R numpy/numpy --reason completed --comment "Looks fixed by #7823"   # 0.89
# gh issue close 8987 -R numpy/numpy --reason completed --comment "Looks fixed by #9961"   # 0.89
# gh issue close 15128 -R numpy/numpy --reason completed --comment "Looks fixed by #31659"   # 0.89
# gh issue close 15846 -R numpy/numpy --reason completed --comment "Looks fixed by #32673"   # 0.89
# gh issue close 18434 -R numpy/numpy --reason completed --comment "Looks fixed by #22540"   # 0.89
# gh issue close 18926 -R numpy/numpy --reason completed --comment "Looks fixed by #19581"   # 0.89
# gh issue close 20705 -R numpy/numpy --reason completed --comment "Looks fixed by #20722"   # 0.89
# gh issue close 21280 -R numpy/numpy --reason completed --comment "Looks fixed by #27117"   # 0.89
# gh issue close 23014 -R numpy/numpy --reason completed --comment "Looks fixed by #27504"   # 0.89
# gh issue close 24976 -R numpy/numpy --reason completed --comment "Looks fixed by #32320"   # 0.89
# gh issue close 25640 -R numpy/numpy --reason completed --comment "Looks fixed by #26261"   # 0.89
# gh issue close 27542 -R numpy/numpy --reason completed --comment "Looks fixed by #29811"   # 0.89
# gh issue close 28428 -R numpy/numpy --reason completed --comment "Looks fixed by #29905"   # 0.89
# gh issue close 31764 -R numpy/numpy --reason completed --comment "Looks fixed by #31771"   # 0.89
# gh issue close 31930 -R numpy/numpy --reason completed --comment "Looks fixed by #31992"   # 0.89
# gh issue close 5098 -R numpy/numpy --reason completed --comment "Looks fixed by #9306"   # 0.88
# gh issue close 7490 -R numpy/numpy --reason completed --comment "Looks fixed by #23087"   # 0.88
# gh issue close 10989 -R numpy/numpy --reason completed --comment "Looks fixed by #25541"   # 0.88
# gh issue close 13357 -R numpy/numpy --reason completed --comment "Looks fixed by #13710"   # 0.88
# gh issue close 15488 -R numpy/numpy --reason completed --comment "Looks fixed by #33042"   # 0.88
# gh issue close 17744 -R numpy/numpy --reason completed --comment "Looks fixed by #18965"   # 0.88
# gh issue close 21787 -R numpy/numpy --reason completed --comment "Looks fixed by #25230"   # 0.88
# gh issue close 26059 -R numpy/numpy --reason completed --comment "Looks fixed by #33312"   # 0.88
# gh issue close 26761 -R numpy/numpy --reason completed --comment "Looks fixed by #33213"   # 0.88

# --- Open PRs after the same thing (10)
# gh pr view 22611 -R numpy/numpy; gh pr view 26798 -R numpy/numpy   # 0.99
# gh pr view 30117 -R numpy/numpy; gh pr view 33323 -R numpy/numpy   # 0.99
# gh pr view 30281 -R numpy/numpy; gh pr view 30496 -R numpy/numpy   # 0.99
# gh pr view 31015 -R numpy/numpy; gh pr view 31022 -R numpy/numpy   # 0.99
# gh pr view 32790 -R numpy/numpy; gh pr view 33140 -R numpy/numpy   # 0.99
# gh pr view 28567 -R numpy/numpy; gh pr view 31871 -R numpy/numpy   # 0.93
# gh pr view 31871 -R numpy/numpy; gh pr view 33253 -R numpy/numpy   # 0.93
# gh pr view 26650 -R numpy/numpy; gh pr view 31495 -R numpy/numpy   # 0.92
# gh pr view 28608 -R numpy/numpy; gh pr view 28718 -R numpy/numpy   # 0.92
# gh pr view 28608 -R numpy/numpy; gh pr view 28815 -R numpy/numpy   # 0.92

# --- Labels to add (1164)
# gh issue edit 7644 -R numpy/numpy --add-label '00 - Bug'   # 0.99
# gh issue edit 9438 -R numpy/numpy --add-label '00 - Bug'   # 0.99
# gh issue edit 11283 -R numpy/numpy --add-label '00 - Bug'   # 0.99
# gh issue edit 11659 -R numpy/numpy --add-label '00 - Bug'   # 0.99
# gh issue edit 11990 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.99
# gh issue edit 12183 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.99
# gh issue edit 12906 -R numpy/numpy --add-label '00 - Bug'   # 0.99
# gh issue edit 19308 -R numpy/numpy --add-label '00 - Bug'   # 0.99
# gh issue edit 19397 -R numpy/numpy --add-label '00 - Bug'   # 0.99
# gh issue edit 19532 -R numpy/numpy --add-label '00 - Bug'   # 0.99
# gh issue edit 19685 -R numpy/numpy --add-label '00 - Bug'   # 0.99
# gh issue edit 22049 -R numpy/numpy --add-label '00 - Bug'   # 0.99
# gh pr edit 27071 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.99
# gh issue edit 28366 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.99
# gh issue edit 32605 -R numpy/numpy --add-label 'component: numpy.fft'   # 0.99
# gh issue edit 4560 -R numpy/numpy --add-label '04 - Documentation'   # 0.98
# gh issue edit 10167 -R numpy/numpy --add-label '04 - Documentation'   # 0.98
# gh issue edit 20733 -R numpy/numpy --add-label '04 - Documentation'   # 0.98
# gh issue edit 23271 -R numpy/numpy --add-label '04 - Documentation'   # 0.98
# gh issue edit 27871 -R numpy/numpy --add-label '04 - Documentation'   # 0.98
# gh issue edit 28010 -R numpy/numpy --add-label '04 - Documentation'   # 0.98
# gh pr edit 31523 -R numpy/numpy --add-label '04 - Documentation'   # 0.98
# gh pr edit 31544 -R numpy/numpy --add-label '04 - Documentation'   # 0.98
# gh pr edit 31639 -R numpy/numpy --add-label '04 - Documentation'   # 0.98
# gh issue edit 11960 -R numpy/numpy --add-label '03 - Maintenance'   # 0.97
# gh issue edit 17359 -R numpy/numpy --add-label '03 - Maintenance'   # 0.97
# gh issue edit 19544 -R numpy/numpy --add-label '03 - Maintenance'   # 0.97
# gh issue edit 19604 -R numpy/numpy --add-label '03 - Maintenance'   # 0.97
# gh issue edit 21672 -R numpy/numpy --add-label '03 - Maintenance'   # 0.97
# gh issue edit 21672 -R numpy/numpy --add-label 'component: numpy.f2py'   # 0.97
# gh issue edit 25179 -R numpy/numpy --add-label '03 - Maintenance'   # 0.97
# gh issue edit 25415 -R numpy/numpy --add-label '03 - Maintenance'   # 0.97
# gh issue edit 26078 -R numpy/numpy --add-label '05 - Testing'   # 0.97
# gh issue edit 26176 -R numpy/numpy --add-label '03 - Maintenance'   # 0.97
# gh issue edit 28016 -R numpy/numpy --add-label 'component: numpy.f2py'   # 0.97
# gh issue edit 28018 -R numpy/numpy --add-label '03 - Maintenance'   # 0.97
# gh pr edit 28646 -R numpy/numpy --add-label 'component: numpy.f2py'   # 0.97
# gh issue edit 30260 -R numpy/numpy --add-label 'component: numpy.f2py'   # 0.97
# gh issue edit 30358 -R numpy/numpy --add-label '03 - Maintenance'   # 0.97
# gh pr edit 30988 -R numpy/numpy --add-label '05 - Testing'   # 0.97
# gh pr edit 31200 -R numpy/numpy --add-label 'component: numpy.f2py'   # 0.97
# gh pr edit 31333 -R numpy/numpy --add-label '05 - Testing'   # 0.97
# gh issue edit 31409 -R numpy/numpy --add-label 'component: numpy.f2py'   # 0.97
# gh pr edit 31523 -R numpy/numpy --add-label 'component: numpy.f2py'   # 0.97
# gh pr edit 31599 -R numpy/numpy --add-label 'component: numpy.f2py'   # 0.97
# gh pr edit 31624 -R numpy/numpy --add-label 'component: numpy.f2py'   # 0.97
# gh issue edit 31958 -R numpy/numpy --add-label 'component: numpy.f2py'   # 0.97
# gh issue edit 32148 -R numpy/numpy --add-label 'component: numpy.f2py'   # 0.97
# gh issue edit 32275 -R numpy/numpy --add-label '05 - Testing'   # 0.97
# gh issue edit 32360 -R numpy/numpy --add-label 'component: numpy.f2py'   # 0.97
# gh issue edit 32461 -R numpy/numpy --add-label '05 - Testing'   # 0.97
# gh pr edit 33236 -R numpy/numpy --add-label 'component: numpy.f2py'   # 0.97
# gh issue edit 4554 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.96
# gh issue edit 4829 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.96
# gh issue edit 10215 -R numpy/numpy --add-label 'component: numpy.random'   # 0.96
# gh issue edit 12313 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.96
# gh issue edit 13121 -R numpy/numpy --add-label 'component: numpy.random'   # 0.96
# gh issue edit 13189 -R numpy/numpy --add-label 'component: numpy.random'   # 0.96
# gh issue edit 17269 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.96
# gh issue edit 19057 -R numpy/numpy --add-label 'component: numpy.random'   # 0.96
# gh issue edit 19382 -R numpy/numpy --add-label 'component: numpy.random'   # 0.96
# gh issue edit 20022 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.96
# gh pr edit 20551 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.96
# gh issue edit 20860 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.96
# gh pr edit 20889 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.96
# gh issue edit 21358 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.96
# gh pr edit 21814 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.96
# gh issue edit 21947 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.96
# gh issue edit 21961 -R numpy/numpy --add-label 'component: numpy.random'   # 0.96
# gh issue edit 22459 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.96
# gh issue edit 23353 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.96
# gh issue edit 23531 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.96
# gh issue edit 24699 -R numpy/numpy --add-label '07 - Deprecation'   # 0.96
# gh issue edit 25304 -R numpy/numpy --add-label '07 - Deprecation'   # 0.96
# gh issue edit 25306 -R numpy/numpy --add-label '07 - Deprecation'   # 0.96
# gh issue edit 25589 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.96
# gh issue edit 25612 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.96
# gh issue edit 25724 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.96
# gh pr edit 25960 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.96
# gh issue edit 26401 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.96
# gh issue edit 26491 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.96
# gh issue edit 26617 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.96
# gh pr edit 27584 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.96
# gh issue edit 28378 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.96
# gh issue edit 29680 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.96
# gh pr edit 30330 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.96
# gh pr edit 31739 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.96
# gh issue edit 31868 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.96
# gh pr edit 32525 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.96
# gh pr edit 32807 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.96
# gh pr edit 33132 -R numpy/numpy --add-label 'component: numpy.random'   # 0.96
# gh pr edit 33146 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.96
# gh pr edit 33152 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.96
# gh pr edit 33162 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.96
# gh pr edit 22913 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.95
# gh issue edit 4715 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 4829 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 5221 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 5412 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 5933 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 5972 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 6027 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 6081 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 6082 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 6083 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 6282 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 6364 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 8000 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 8161 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 8207 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 8275 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 8581 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 8765 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 8773 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 9313 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 9370 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 9465 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 9954 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 10318 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 10436 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 11541 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 11548 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 11622 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 12367 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 12550 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 12936 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 13011 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 13100 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 13121 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 13408 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 14254 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 15200 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 16157 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 17335 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 17839 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 18198 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 18385 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 18494 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 18512 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 18516 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 18672 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 18700 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 19020 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 19146 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 19472 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 19473 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 19511 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 19532 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 19861 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 20044 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 20053 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 20233 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 20461 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 20545 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 20880 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 20995 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 21136 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 21160 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 21161 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 21219 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 21220 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 21357 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 21379 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 21396 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 21435 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 21655 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 21713 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 21758 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 21780 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 21787 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 21941 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 21947 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 22025 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 22098 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 22188 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 22217 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 22471 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 22590 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 22710 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 22739 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 22898 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 22995 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 23014 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 23040 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 23068 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 23146 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 23176 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 23180 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 23353 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 23398 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 23434 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 23478 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 23540 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 23582 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 23622 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 23625 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 23671 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 23807 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 23816 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 23849 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 23899 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 23934 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 24084 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 24145 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 24345 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 24368 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 24394 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 24859 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 24897 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 24976 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 25007 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 25235 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 25496 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 25498 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 25622 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 25623 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 25637 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 25640 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 25698 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 25766 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 25823 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 25835 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 25859 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 25872 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 26032 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 26104 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 26206 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 26220 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 26401 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 26448 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 26615 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 26783 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 26819 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 26819 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 26916 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 27109 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 27374 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh pr edit 27402 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 27409 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 27494 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 27530 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 27533 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 27542 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh pr edit 27591 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 27600 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 27629 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 27671 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 27701 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 27785 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 27844 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 27865 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 27968 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 27987 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 28016 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 28024 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 28098 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 28099 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 28119 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 28318 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 28389 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 28549 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 28642 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh pr edit 28686 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 28829 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 29262 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 29527 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 29528 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh pr edit 29567 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 29675 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 29710 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 29752 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 29881 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 30046 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 30089 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 30171 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh pr edit 30299 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh pr edit 30330 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh pr edit 30380 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 30413 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 30699 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 30766 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 30866 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 30916 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh pr edit 31015 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh pr edit 31022 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 31024 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 31086 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 31239 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh pr edit 31247 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 31279 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 31292 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 31301 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh pr edit 31321 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh pr edit 31348 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh pr edit 31598 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh pr edit 31599 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh pr edit 31817 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh pr edit 31854 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 31866 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 31958 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh pr edit 32199 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 32307 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 32372 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh issue edit 32439 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 32970 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 33081 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 33161 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 33161 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.94
# gh pr edit 33165 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 33270 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 33319 -R numpy/numpy --add-label '00 - Bug'   # 0.94
# gh issue edit 33321 -R numpy/numpy --add-label '01 - Enhancement'   # 0.94
# gh issue edit 9546 -R numpy/numpy --add-label '00 - Bug'   # 0.93
# gh issue edit 17328 -R numpy/numpy --add-label '04 - Documentation'   # 0.93
# gh issue edit 27533 -R numpy/numpy --add-label 'component: SIMD'   # 0.93
# gh pr edit 29211 -R numpy/numpy --add-label 'component: SIMD'   # 0.93
# gh pr edit 29263 -R numpy/numpy --add-label 'component: SIMD'   # 0.93
# gh pr edit 29549 -R numpy/numpy --add-label 'component: SIMD'   # 0.93
# gh issue edit 30172 -R numpy/numpy --add-label 'component: SIMD'   # 0.93
# gh pr edit 30449 -R numpy/numpy --add-label 'component: SIMD'   # 0.93
# gh pr edit 31236 -R numpy/numpy --add-label 'component: SIMD'   # 0.93
# gh issue edit 31424 -R numpy/numpy --add-label '01 - Enhancement'   # 0.93
# gh pr edit 32163 -R numpy/numpy --add-label 'component: SIMD'   # 0.93
# gh issue edit 32307 -R numpy/numpy --add-label 'component: SIMD'   # 0.93
# gh pr edit 33268 -R numpy/numpy --add-label 'component: SIMD'   # 0.93
# gh pr edit 33349 -R numpy/numpy --add-label 'component: SIMD'   # 0.93
# gh issue edit 7461 -R numpy/numpy --add-label '00 - Bug'   # 0.92
# gh issue edit 13088 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.92
# gh issue edit 14103 -R numpy/numpy --add-label '00 - Bug'   # 0.92
# gh issue edit 17612 -R numpy/numpy --add-label '00 - Bug'   # 0.92
# gh pr edit 24446 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.92
# gh issue edit 26746 -R numpy/numpy --add-label '00 - Bug'   # 0.92
# gh issue edit 27042 -R numpy/numpy --add-label '01 - Enhancement'   # 0.92
# gh pr edit 27642 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.92
# gh pr edit 31215 -R numpy/numpy --add-label 'component: numpy.random'   # 0.92
# gh pr edit 32973 -R numpy/numpy --add-label 'component: numpy.fft'   # 0.92
# gh issue edit 13189 -R numpy/numpy --add-label '00 - Bug'   # 0.91
# gh issue edit 14412 -R numpy/numpy --add-label '00 - Bug'   # 0.91
# gh issue edit 16876 -R numpy/numpy --add-label '00 - Bug'   # 0.91
# gh issue edit 17752 -R numpy/numpy --add-label '00 - Bug'   # 0.91
# gh issue edit 23821 -R numpy/numpy --add-label 'component: CI'   # 0.91
# gh issue edit 26704 -R numpy/numpy --add-label '00 - Bug'   # 0.91
# gh issue edit 28227 -R numpy/numpy --add-label 'component: CI'   # 0.91
# gh issue edit 29524 -R numpy/numpy --add-label 'component: CI'   # 0.91
# gh issue edit 33172 -R numpy/numpy --add-label 'component: CI'   # 0.91
# gh pr edit 33254 -R numpy/numpy --add-label '00 - Bug'   # 0.91
# gh issue edit 6471 -R numpy/numpy --add-label '00 - Bug'   # 0.90
# gh issue edit 9921 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.90
# gh issue edit 18069 -R numpy/numpy --add-label '00 - Bug'   # 0.90
# gh issue edit 29644 -R numpy/numpy --add-label '01 - Enhancement'   # 0.90
# gh issue edit 11079 -R numpy/numpy --add-label 'component: numpy._core'   # 0.89
# gh issue edit 11887 -R numpy/numpy --add-label '00 - Bug'   # 0.89
# gh issue edit 12283 -R numpy/numpy --add-label '00 - Bug'   # 0.89
# gh issue edit 17305 -R numpy/numpy --add-label '00 - Bug'   # 0.89
# gh issue edit 18586 -R numpy/numpy --add-label '00 - Bug'   # 0.89
# gh issue edit 19162 -R numpy/numpy --add-label '00 - Bug'   # 0.89
# gh issue edit 19410 -R numpy/numpy --add-label '00 - Bug'   # 0.89
# gh issue edit 8627 -R numpy/numpy --add-label '00 - Bug'   # 0.88
# gh issue edit 14225 -R numpy/numpy --add-label '00 - Bug'   # 0.88
# gh issue edit 7780 -R numpy/numpy --add-label '01 - Enhancement'   # 0.87
# gh issue edit 9659 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.87
# gh issue edit 12966 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.87
# gh pr edit 27631 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.87
# gh pr edit 27635 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.87
# gh pr edit 29627 -R numpy/numpy --add-label '00 - Bug'   # 0.87
# gh issue edit 31423 -R numpy/numpy --add-label '01 - Enhancement'   # 0.87
# gh pr edit 31544 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.87
# gh pr edit 32315 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.87
# gh issue edit 4979 -R numpy/numpy --add-label 'component: numpy._core'   # 0.86
# gh issue edit 6951 -R numpy/numpy --add-label '01 - Enhancement'   # 0.86
# gh issue edit 10705 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.86
# gh issue edit 11918 -R numpy/numpy --add-label 'component: numpy.fft'   # 0.86
# gh issue edit 12183 -R numpy/numpy --add-label '00 - Bug'   # 0.86
# gh issue edit 12283 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.86
# gh issue edit 16881 -R numpy/numpy --add-label 'component: numpy._core'   # 0.86
# gh issue edit 17850 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.86
# gh issue edit 20850 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.86
# gh issue edit 23479 -R numpy/numpy --add-label 'component: numpy._core'   # 0.86
# gh issue edit 27987 -R numpy/numpy --add-label 'component: numpy.fft'   # 0.86
# gh issue edit 31590 -R numpy/numpy --add-label 'component: numpy._core'   # 0.86
# gh issue edit 5098 -R numpy/numpy --add-label '00 - Bug'   # 0.85
# gh issue edit 10954 -R numpy/numpy --add-label '00 - Bug'   # 0.85
# gh issue edit 20785 -R numpy/numpy --add-label 'component: benchmarks'   # 0.85
# gh issue edit 27258 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.85
# gh issue edit 29644 -R numpy/numpy --add-label 'component: benchmarks'   # 0.85
# gh issue edit 9128 -R numpy/numpy --add-label '00 - Bug'   # 0.84
# gh issue edit 13733 -R numpy/numpy --add-label '00 - Bug'   # 0.84
# gh issue edit 20596 -R numpy/numpy --add-label '00 - Bug'   # 0.84
# gh issue edit 23362 -R numpy/numpy --add-label '01 - Enhancement'   # 0.84
# gh pr edit 33193 -R numpy/numpy --add-label '04 - Documentation'   # 0.84
# gh issue edit 10446 -R numpy/numpy --add-label '01 - Enhancement'   # 0.83
# gh issue edit 17554 -R numpy/numpy --add-label '00 - Bug'   # 0.83
# gh pr edit 31066 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.83
# gh pr edit 32787 -R numpy/numpy --add-label 'component: numpy.random'   # 0.83
# gh pr edit 33017 -R numpy/numpy --add-label 'component: numpy._core'   # 0.83
# gh issue edit 5894 -R numpy/numpy --add-label '00 - Bug'   # 0.82
# gh issue edit 6286 -R numpy/numpy --add-label '00 - Bug'   # 0.82
# gh issue edit 6318 -R numpy/numpy --add-label '00 - Bug'   # 0.82
# gh issue edit 9287 -R numpy/numpy --add-label '00 - Bug'   # 0.82
# gh issue edit 9436 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.82
# gh issue edit 9642 -R numpy/numpy --add-label '00 - Bug'   # 0.82
# gh issue edit 11387 -R numpy/numpy --add-label '00 - Bug'   # 0.82
# gh issue edit 12282 -R numpy/numpy --add-label '00 - Bug'   # 0.82
# gh issue edit 16152 -R numpy/numpy --add-label '00 - Bug'   # 0.82
# gh issue edit 16726 -R numpy/numpy --add-label '00 - Bug'   # 0.82
# gh issue edit 17202 -R numpy/numpy --add-label '00 - Bug'   # 0.82
# gh issue edit 18604 -R numpy/numpy --add-label '00 - Bug'   # 0.82
# gh issue edit 33299 -R numpy/numpy --add-label '00 - Bug'   # 0.82
# gh issue edit 5150 -R numpy/numpy --add-label '00 - Bug'   # 0.81
# gh issue edit 6316 -R numpy/numpy --add-label '00 - Bug'   # 0.81
# gh issue edit 11938 -R numpy/numpy --add-label '00 - Bug'   # 0.81
# gh issue edit 18986 -R numpy/numpy --add-label '00 - Bug'   # 0.81
# gh issue edit 27422 -R numpy/numpy --add-label '00 - Bug'   # 0.81
# gh issue edit 8361 -R numpy/numpy --add-label '00 - Bug'   # 0.80
# gh issue edit 9659 -R numpy/numpy --add-label '00 - Bug'   # 0.80
# gh issue edit 13285 -R numpy/numpy --add-label '00 - Bug'   # 0.80
# gh issue edit 14066 -R numpy/numpy --add-label '00 - Bug'   # 0.80
# gh issue edit 17118 -R numpy/numpy --add-label '00 - Bug'   # 0.80
# gh issue edit 4979 -R numpy/numpy --add-label '00 - Bug'   # 0.79
# gh issue edit 7874 -R numpy/numpy --add-label '01 - Enhancement'   # 0.79
# gh issue edit 10493 -R numpy/numpy --add-label '01 - Enhancement'   # 0.79
# gh issue edit 31060 -R numpy/numpy --add-label '07 - Deprecation'   # 0.79
# gh pr edit 33183 -R numpy/numpy --add-label '00 - Bug'   # 0.79
# gh issue edit 33352 -R numpy/numpy --add-label '00 - Bug'   # 0.79
# gh issue edit 7277 -R numpy/numpy --add-label '00 - Bug'   # 0.78
# gh issue edit 9923 -R numpy/numpy --add-label '00 - Bug'   # 0.78
# gh issue edit 14239 -R numpy/numpy --add-label '00 - Bug'   # 0.78
# gh issue edit 24428 -R numpy/numpy --add-label '00 - Bug'   # 0.78
# gh issue edit 33318 -R numpy/numpy --add-label 'component: numpy.random'   # 0.78
# gh issue edit 5782 -R numpy/numpy --add-label '00 - Bug'   # 0.77
# gh issue edit 9044 -R numpy/numpy --add-label '00 - Bug'   # 0.77
# gh issue edit 9644 -R numpy/numpy --add-label '00 - Bug'   # 0.77
# gh issue edit 10010 -R numpy/numpy --add-label '00 - Bug'   # 0.77
# gh issue edit 15140 -R numpy/numpy --add-label '00 - Bug'   # 0.77
# gh issue edit 15712 -R numpy/numpy --add-label '00 - Bug'   # 0.77
# gh pr edit 20529 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.77
# gh issue edit 31969 -R numpy/numpy --add-label '01 - Enhancement'   # 0.77
# gh issue edit 12208 -R numpy/numpy --add-label '00 - Bug'   # 0.76
# gh issue edit 16377 -R numpy/numpy --add-label '00 - Bug'   # 0.76
# gh issue edit 24736 -R numpy/numpy --add-label '04 - Documentation'   # 0.76
# gh issue edit 5193 -R numpy/numpy --add-label '00 - Bug'   # 0.75
# gh issue edit 9631 -R numpy/numpy --add-label '00 - Bug'   # 0.75
# gh issue edit 10144 -R numpy/numpy --add-label 'component: numpy._core'   # 0.75
# gh issue edit 13319 -R numpy/numpy --add-label 'component: numpy._core'   # 0.75
# gh issue edit 14225 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.75
# gh issue edit 16665 -R numpy/numpy --add-label 'component: numpy._core'   # 0.75
# gh issue edit 20351 -R numpy/numpy --add-label 'component: numpy.datetime64'   # 0.75
# gh issue edit 22197 -R numpy/numpy --add-label 'component: numpy.datetime64'   # 0.75
# gh issue edit 24050 -R numpy/numpy --add-label 'component: numpy.testing'   # 0.75
# gh issue edit 25677 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.75
# gh issue edit 27380 -R numpy/numpy --add-label 'component: numpy.random'   # 0.75
# gh issue edit 27600 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.75
# gh pr edit 31023 -R numpy/numpy --add-label 'component: numpy.datetime64'   # 0.75
# gh pr edit 31216 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.75
# gh pr edit 31984 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.75
# gh issue edit 11925 -R numpy/numpy --add-label '00 - Bug'   # 0.74
# gh issue edit 12076 -R numpy/numpy --add-label '00 - Bug'   # 0.74
# gh issue edit 12313 -R numpy/numpy --add-label '00 - Bug'   # 0.74
# gh issue edit 12444 -R numpy/numpy --add-label '00 - Bug'   # 0.74
# gh issue edit 17835 -R numpy/numpy --add-label '00 - Bug'   # 0.74
# gh issue edit 5069 -R numpy/numpy --add-label '00 - Bug'   # 0.73
# gh issue edit 6364 -R numpy/numpy --add-label '00 - Bug'   # 0.73
# gh issue edit 7210 -R numpy/numpy --add-label '00 - Bug'   # 0.73
# gh issue edit 14716 -R numpy/numpy --add-label '00 - Bug'   # 0.73
# gh issue edit 15123 -R numpy/numpy --add-label '01 - Enhancement'   # 0.73
# gh issue edit 15569 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.73
# gh issue edit 18632 -R numpy/numpy --add-label '00 - Bug'   # 0.73
# gh issue edit 7797 -R numpy/numpy --add-label 'component: numpy._core'   # 0.72
# gh issue edit 8855 -R numpy/numpy --add-label '00 - Bug'   # 0.72
# gh issue edit 10155 -R numpy/numpy --add-label '00 - Bug'   # 0.72
# gh issue edit 10700 -R numpy/numpy --add-label '00 - Bug'   # 0.72
# gh issue edit 11498 -R numpy/numpy --add-label '00 - Bug'   # 0.72
# gh issue edit 19157 -R numpy/numpy --add-label '00 - Bug'   # 0.72
# gh issue edit 19891 -R numpy/numpy --add-label '04 - Documentation'   # 0.72
# gh issue edit 29801 -R numpy/numpy --add-label '00 - Bug'   # 0.72
# gh issue edit 5718 -R numpy/numpy --add-label 'component: numpy._core'   # 0.71
# gh issue edit 5735 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.71
# gh issue edit 5782 -R numpy/numpy --add-label 'component: numpy._core'   # 0.71
# gh issue edit 7236 -R numpy/numpy --add-label 'component: numpy.testing'   # 0.71
# gh issue edit 7784 -R numpy/numpy --add-label '00 - Bug'   # 0.71
# gh issue edit 7993 -R numpy/numpy --add-label '01 - Enhancement'   # 0.71
# gh issue edit 8502 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.71
# gh issue edit 8855 -R numpy/numpy --add-label 'component: numpy.fft'   # 0.71
# gh issue edit 9032 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.71
# gh issue edit 10581 -R numpy/numpy --add-label '00 - Bug'   # 0.71
# gh issue edit 10582 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.71
# gh issue edit 10866 -R numpy/numpy --add-label 'component: numpy._core'   # 0.71
# gh issue edit 12695 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.71
# gh issue edit 13408 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.71
# gh issue edit 15488 -R numpy/numpy --add-label '00 - Bug'   # 0.71
# gh issue edit 16983 -R numpy/numpy --add-label '01 - Enhancement'   # 0.71
# gh issue edit 17567 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.71
# gh issue edit 18696 -R numpy/numpy --add-label 'component: numpy._core'   # 0.71
# gh issue edit 18744 -R numpy/numpy --add-label '00 - Bug'   # 0.71
# gh issue edit 18898 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.71
# gh issue edit 23849 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.71
# gh issue edit 24428 -R numpy/numpy --add-label 'component: numpy._core'   # 0.71
# gh issue edit 25197 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.71
# gh issue edit 25548 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.71
# gh issue edit 27374 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.71
# gh issue edit 28318 -R numpy/numpy --add-label 'component: numpy._core'   # 0.71
# gh issue edit 28463 -R numpy/numpy --add-label 'component: CI'   # 0.71
# gh issue edit 28642 -R numpy/numpy --add-label 'component: CI'   # 0.71
# gh issue edit 29527 -R numpy/numpy --add-label 'component: numpy._core'   # 0.71
# gh issue edit 31280 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.71
# gh issue edit 31478 -R numpy/numpy --add-label 'component: SIMD'   # 0.71
# gh pr edit 31496 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.71
# gh pr edit 32526 -R numpy/numpy --add-label 'component: numpy.datetime64'   # 0.71
# gh pr edit 33188 -R numpy/numpy --add-label 'component: numpy._core'   # 0.71
# gh issue edit 7212 -R numpy/numpy --add-label '00 - Bug'   # 0.70
# gh issue edit 7713 -R numpy/numpy --add-label '00 - Bug'   # 0.70
# gh issue edit 8089 -R numpy/numpy --add-label '00 - Bug'   # 0.70
# gh issue edit 9032 -R numpy/numpy --add-label '01 - Enhancement'   # 0.70
# gh issue edit 10574 -R numpy/numpy --add-label '00 - Bug'   # 0.70
# gh issue edit 11990 -R numpy/numpy --add-label '00 - Bug'   # 0.70
# gh issue edit 13232 -R numpy/numpy --add-label '00 - Bug'   # 0.70
# gh issue edit 17305 -R numpy/numpy --add-label 'component: numpy._core'   # 0.70
# gh issue edit 17676 -R numpy/numpy --add-label '01 - Enhancement'   # 0.70
# gh issue edit 18388 -R numpy/numpy --add-label '00 - Bug'   # 0.70
# gh pr edit 28490 -R numpy/numpy --add-label 'component: SIMD'   # 0.70
# gh issue edit 28704 -R numpy/numpy --add-label '00 - Bug'   # 0.70
# gh pr edit 33348 -R numpy/numpy --add-label '01 - Enhancement'   # 0.70
# gh issue edit 6132 -R numpy/numpy --add-label '00 - Bug'   # 0.69
# gh issue edit 9448 -R numpy/numpy --add-label '01 - Enhancement'   # 0.69
# gh issue edit 10579 -R numpy/numpy --add-label '00 - Bug'   # 0.69
# gh issue edit 11674 -R numpy/numpy --add-label '00 - Bug'   # 0.69
# gh issue edit 12309 -R numpy/numpy --add-label 'component: numpy._core'   # 0.69
# gh issue edit 12735 -R numpy/numpy --add-label '00 - Bug'   # 0.69
# gh issue edit 13846 -R numpy/numpy --add-label '00 - Bug'   # 0.69
# gh issue edit 15219 -R numpy/numpy --add-label '00 - Bug'   # 0.69
# gh issue edit 18898 -R numpy/numpy --add-label '00 - Bug'   # 0.69
# gh issue edit 25290 -R numpy/numpy --add-label '00 - Bug'   # 0.69
# gh pr edit 32661 -R numpy/numpy --add-label 'component: numpy.testing'   # 0.69
# gh issue edit 5735 -R numpy/numpy --add-label '00 - Bug'   # 0.68
# gh issue edit 8460 -R numpy/numpy --add-label '00 - Bug'   # 0.68
# gh issue edit 8513 -R numpy/numpy --add-label '01 - Enhancement'   # 0.68
# gh issue edit 10937 -R numpy/numpy --add-label '01 - Enhancement'   # 0.68
# gh issue edit 11308 -R numpy/numpy --add-label '00 - Bug'   # 0.68
# gh issue edit 12540 -R numpy/numpy --add-label '04 - Documentation'   # 0.68
# gh issue edit 13553 -R numpy/numpy --add-label '00 - Bug'   # 0.68
# gh issue edit 17593 -R numpy/numpy --add-label '00 - Bug'   # 0.68
# gh issue edit 18028 -R numpy/numpy --add-label '01 - Enhancement'   # 0.68
# gh issue edit 26038 -R numpy/numpy --add-label '00 - Bug'   # 0.68
# gh issue edit 29941 -R numpy/numpy --add-label '04 - Documentation'   # 0.68
# gh issue edit 5412 -R numpy/numpy --add-label 'component: numpy._core'   # 0.67
# gh issue edit 7189 -R numpy/numpy --add-label '00 - Bug'   # 0.67
# gh issue edit 7713 -R numpy/numpy --add-label 'component: numpy._core'   # 0.67
# gh issue edit 8306 -R numpy/numpy --add-label 'component: numpy._core'   # 0.67
# gh issue edit 9509 -R numpy/numpy --add-label 'component: numpy._core'   # 0.67
# gh issue edit 11683 -R numpy/numpy --add-label '00 - Bug'   # 0.67
# gh issue edit 12368 -R numpy/numpy --add-label '01 - Enhancement'   # 0.67
# gh issue edit 12613 -R numpy/numpy --add-label '00 - Bug'   # 0.67
# gh issue edit 12974 -R numpy/numpy --add-label '01 - Enhancement'   # 0.67
# gh issue edit 13100 -R numpy/numpy --add-label 'component: numpy._core'   # 0.67
# gh issue edit 18387 -R numpy/numpy --add-label '00 - Bug'   # 0.67
# gh issue edit 19382 -R numpy/numpy --add-label '01 - Enhancement'   # 0.67
# gh issue edit 19852 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.67
# gh issue edit 23350 -R numpy/numpy --add-label 'component: numpy._core'   # 0.67
# gh pr edit 25703 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.67
# gh issue edit 27588 -R numpy/numpy --add-label '00 - Bug'   # 0.67
# gh pr edit 32340 -R numpy/numpy --add-label 'component: numpy.fft'   # 0.67
# gh pr edit 33253 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.67
# gh issue edit 7380 -R numpy/numpy --add-label '00 - Bug'   # 0.66
# gh issue edit 8003 -R numpy/numpy --add-label '00 - Bug'   # 0.66
# gh issue edit 10270 -R numpy/numpy --add-label '00 - Bug'   # 0.66
# gh issue edit 15332 -R numpy/numpy --add-label '00 - Bug'   # 0.66
# gh issue edit 19267 -R numpy/numpy --add-label '00 - Bug'   # 0.66
# gh issue edit 31485 -R numpy/numpy --add-label '17 - Task'   # 0.66
# gh issue edit 4915 -R numpy/numpy --add-label '00 - Bug'   # 0.65
# gh issue edit 8519 -R numpy/numpy --add-label 'component: numpy._core'   # 0.65
# gh issue edit 9565 -R numpy/numpy --add-label '00 - Bug'   # 0.65
# gh issue edit 13190 -R numpy/numpy --add-label '00 - Bug'   # 0.65
# gh issue edit 13918 -R numpy/numpy --add-label '00 - Bug'   # 0.65
# gh issue edit 17347 -R numpy/numpy --add-label 'component: build'   # 0.65
# gh pr edit 32895 -R numpy/numpy --add-label '01 - Enhancement'   # 0.65
# gh issue edit 5657 -R numpy/numpy --add-label 'component: numpy._core'   # 0.64
# gh issue edit 5721 -R numpy/numpy --add-label 'component: numpy._core'   # 0.64
# gh issue edit 6765 -R numpy/numpy --add-label '00 - Bug'   # 0.64
# gh issue edit 8773 -R numpy/numpy --add-label 'component: numpy._core'   # 0.64
# gh issue edit 15978 -R numpy/numpy --add-label '00 - Bug'   # 0.64
# gh issue edit 17839 -R numpy/numpy --add-label 'component: numpy.fft'   # 0.64
# gh issue edit 18774 -R numpy/numpy --add-label '00 - Bug'   # 0.64
# gh issue edit 19623 -R numpy/numpy --add-label '00 - Bug'   # 0.64
# gh issue edit 19970 -R numpy/numpy --add-label '00 - Bug'   # 0.64
# gh issue edit 24157 -R numpy/numpy --add-label '03 - Maintenance'   # 0.64
# gh issue edit 5657 -R numpy/numpy --add-label '00 - Bug'   # 0.63
# gh issue edit 9474 -R numpy/numpy --add-label '00 - Bug'   # 0.63
# gh issue edit 10645 -R numpy/numpy --add-label '00 - Bug'   # 0.63
# gh issue edit 13510 -R numpy/numpy --add-label '01 - Enhancement'   # 0.63
# gh issue edit 17495 -R numpy/numpy --add-label '00 - Bug'   # 0.63
# gh issue edit 19473 -R numpy/numpy --add-label '00 - Bug'   # 0.63
# gh pr edit 32163 -R numpy/numpy --add-label '01 - Enhancement'   # 0.63
# gh issue edit 2802 -R numpy/numpy --add-label 'component: numpy._core'   # 0.62
# gh issue edit 5543 -R numpy/numpy --add-label 'component: numpy._core'   # 0.62
# gh issue edit 5652 -R numpy/numpy --add-label '00 - Bug'   # 0.62
# gh issue edit 6231 -R numpy/numpy --add-label 'component: numpy._core'   # 0.62
# gh issue edit 6854 -R numpy/numpy --add-label '00 - Bug'   # 0.62
# gh issue edit 7541 -R numpy/numpy --add-label '00 - Bug'   # 0.62
# gh issue edit 7852 -R numpy/numpy --add-label 'component: numpy._core'   # 0.62
# gh issue edit 8780 -R numpy/numpy --add-label '00 - Bug'   # 0.62
# gh issue edit 9252 -R numpy/numpy --add-label 'component: numpy._core'   # 0.62
# gh issue edit 9465 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.62
# gh issue edit 9476 -R numpy/numpy --add-label 'component: numpy._core'   # 0.62
# gh issue edit 10047 -R numpy/numpy --add-label 'component: numpy.distutils'   # 0.62
# gh issue edit 10989 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.62
# gh issue edit 11270 -R numpy/numpy --add-label 'component: numpy._core'   # 0.62
# gh issue edit 12426 -R numpy/numpy --add-label 'component: numpy._core'   # 0.62
# gh issue edit 14837 -R numpy/numpy --add-label 'component: numpy._core'   # 0.62
# gh issue edit 15690 -R numpy/numpy --add-label 'component: numpy._core'   # 0.62
# gh issue edit 15965 -R numpy/numpy --add-label '00 - Bug'   # 0.62
# gh issue edit 16983 -R numpy/numpy --add-label 'component: numpy._core'   # 0.62
# gh issue edit 18112 -R numpy/numpy --add-label '00 - Bug'   # 0.62
# gh issue edit 22029 -R numpy/numpy --add-label 'component: numpy._core'   # 0.62
# gh issue edit 22248 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.62
# gh issue edit 22471 -R numpy/numpy --add-label 'component: numpy._core'   # 0.62
# gh issue edit 27918 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.62
# gh issue edit 28639 -R numpy/numpy --add-label 'component: numpy._core'   # 0.62
# gh pr edit 29102 -R numpy/numpy --add-label 'component: SIMD'   # 0.62
# gh pr edit 29746 -R numpy/numpy --add-label 'component: numpy._core'   # 0.62
# gh issue edit 30037 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.62
# gh issue edit 30337 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.62
# gh issue edit 30809 -R numpy/numpy --add-label 'component: numpy.f2py'   # 0.62
# gh pr edit 31228 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.62
# gh issue edit 32599 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.62
# gh pr edit 32788 -R numpy/numpy --add-label 'component: numpy.random'   # 0.62
# gh issue edit 33081 -R numpy/numpy --add-label 'component: numpy._core'   # 0.62
# gh pr edit 33323 -R numpy/numpy --add-label '01 - Enhancement'   # 0.62
# gh issue edit 3437 -R numpy/numpy --add-label '00 - Bug'   # 0.61
# gh issue edit 9631 -R numpy/numpy --add-label 'component: numpy._core'   # 0.61
# gh issue edit 9637 -R numpy/numpy --add-label '00 - Bug'   # 0.61
# gh issue edit 10288 -R numpy/numpy --add-label '00 - Bug'   # 0.61
# gh issue edit 12817 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.61
# gh issue edit 17605 -R numpy/numpy --add-label '00 - Bug'   # 0.61
# gh issue edit 17665 -R numpy/numpy --add-label '00 - Bug'   # 0.61
# gh issue edit 28598 -R numpy/numpy --add-label '00 - Bug'   # 0.61
# gh issue edit 32170 -R numpy/numpy --add-label '00 - Bug'   # 0.61
# gh issue edit 32747 -R numpy/numpy --add-label '01 - Enhancement'   # 0.61
# gh issue edit 5142 -R numpy/numpy --add-label '00 - Bug'   # 0.60
# gh issue edit 9052 -R numpy/numpy --add-label '01 - Enhancement'   # 0.60
# gh issue edit 9311 -R numpy/numpy --add-label '00 - Bug'   # 0.60
# gh issue edit 9397 -R numpy/numpy --add-label '01 - Enhancement'   # 0.60
# gh issue edit 9443 -R numpy/numpy --add-label 'component: numpy._core'   # 0.60
# gh issue edit 10436 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.60
# gh issue edit 11680 -R numpy/numpy --add-label '00 - Bug'   # 0.60
# gh pr edit 26315 -R numpy/numpy --add-label '03 - Maintenance'   # 0.60
# gh issue edit 28714 -R numpy/numpy --add-label 'component: SIMD'   # 0.60
# gh issue edit 31764 -R numpy/numpy --add-label '00 - Bug'   # 0.60
# gh issue edit 6192 -R numpy/numpy --add-label '00 - Bug'   # 0.59
# gh issue edit 7588 -R numpy/numpy --add-label '00 - Bug'   # 0.59
# gh issue edit 8513 -R numpy/numpy --add-label 'component: numpy._core'   # 0.59
# gh issue edit 8521 -R numpy/numpy --add-label '00 - Bug'   # 0.59
# gh issue edit 9225 -R numpy/numpy --add-label '00 - Bug'   # 0.59
# gh issue edit 9265 -R numpy/numpy --add-label '00 - Bug'   # 0.59
# gh issue edit 9541 -R numpy/numpy --add-label '00 - Bug'   # 0.59
# gh issue edit 9948 -R numpy/numpy --add-label '00 - Bug'   # 0.59
# gh issue edit 10799 -R numpy/numpy --add-label '00 - Bug'   # 0.59
# gh issue edit 13356 -R numpy/numpy --add-label '00 - Bug'   # 0.59
# gh issue edit 13572 -R numpy/numpy --add-label '00 - Bug'   # 0.59
# gh issue edit 14090 -R numpy/numpy --add-label '00 - Bug'   # 0.59
# gh issue edit 16585 -R numpy/numpy --add-label '00 - Bug'   # 0.59
# gh issue edit 29357 -R numpy/numpy --add-label '00 - Bug'   # 0.59
# gh issue edit 31913 -R numpy/numpy --add-label '01 - Enhancement'   # 0.59
# gh issue edit 4198 -R numpy/numpy --add-label '00 - Bug'   # 0.58
# gh issue edit 5976 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.58
# gh issue edit 7449 -R numpy/numpy --add-label 'component: numpy._core'   # 0.58
# gh issue edit 9775 -R numpy/numpy --add-label '00 - Bug'   # 0.58
# gh issue edit 10289 -R numpy/numpy --add-label '00 - Bug'   # 0.58
# gh issue edit 12101 -R numpy/numpy --add-label '00 - Bug'   # 0.58
# gh issue edit 18894 -R numpy/numpy --add-label '01 - Enhancement'   # 0.58
# gh issue edit 19690 -R numpy/numpy --add-label '00 - Bug'   # 0.58
# gh pr edit 24189 -R numpy/numpy --add-label 'component: numpy.ufunc'   # 0.58
# gh issue edit 29315 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.58
# gh pr edit 29507 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.58
# gh pr edit 33140 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.58
# gh issue edit 4966 -R numpy/numpy --add-label '00 - Bug'   # 0.57
# gh issue edit 5236 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 5894 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 6282 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.57
# gh issue edit 7523 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.57
# gh issue edit 7615 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.57
# gh issue edit 7969 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 9698 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 10289 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 10521 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 10574 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 10590 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 10709 -R numpy/numpy --add-label '00 - Bug'   # 0.57
# gh issue edit 11123 -R numpy/numpy --add-label '00 - Bug'   # 0.57
# gh issue edit 11387 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 11498 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.57
# gh issue edit 11938 -R numpy/numpy --add-label 'component: numpy.einsum'   # 0.57
# gh issue edit 12481 -R numpy/numpy --add-label '04 - Documentation'   # 0.57
# gh issue edit 12495 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 13166 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.57
# gh issue edit 13373 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 13470 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 14018 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 14397 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 15495 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 16638 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 17803 -R numpy/numpy --add-label '00 - Bug'   # 0.57
# gh issue edit 18071 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.57
# gh issue edit 18484 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.57
# gh issue edit 19464 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 20114 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.57
# gh issue edit 20705 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 21014 -R numpy/numpy --add-label 'component: build'   # 0.57
# gh issue edit 21280 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 21357 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.57
# gh issue edit 21631 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 21758 -R numpy/numpy --add-label 'component: CI'   # 0.57
# gh issue edit 21804 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.57
# gh pr edit 22176 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.57
# gh issue edit 23273 -R numpy/numpy --add-label 'component: numpy.datetime64'   # 0.57
# gh issue edit 23478 -R numpy/numpy --add-label 'component: numpy.fft'   # 0.57
# gh issue edit 23518 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 23781 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.57
# gh issue edit 24032 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.57
# gh issue edit 24355 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 24368 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.57
# gh issue edit 24689 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.57
# gh pr edit 24944 -R numpy/numpy --add-label '00 - Bug'   # 0.57
# gh issue edit 25647 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 26019 -R numpy/numpy --add-label '04 - Documentation'   # 0.57
# gh issue edit 26206 -R numpy/numpy --add-label 'component: numpy.random'   # 0.57
# gh issue edit 27172 -R numpy/numpy --add-label 'component: numpy.strings'   # 0.57
# gh issue edit 27212 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 27528 -R numpy/numpy --add-label 'component: numpy.strings'   # 0.57
# gh pr edit 27649 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh pr edit 27717 -R numpy/numpy --add-label 'component: numpy.fft'   # 0.57
# gh issue edit 28636 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh pr edit 28640 -R numpy/numpy --add-label 'component: CI'   # 0.57
# gh issue edit 29720 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 30038 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.57
# gh issue edit 30046 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.57
# gh pr edit 31015 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.57
# gh issue edit 31279 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh pr edit 31321 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 31340 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.57
# gh issue edit 31436 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.57
# gh pr edit 31689 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 31866 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 32309 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.57
# gh pr edit 32364 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.57
# gh pr edit 32895 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh pr edit 33027 -R numpy/numpy --add-label 'component: SIMD'   # 0.57
# gh pr edit 33040 -R numpy/numpy --add-label 'component: SIMD'   # 0.57
# gh pr edit 33112 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh pr edit 33115 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.57
# gh pr edit 33174 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.57
# gh pr edit 33271 -R numpy/numpy --add-label 'component: numpy._core'   # 0.57
# gh issue edit 7556 -R numpy/numpy --add-label '01 - Enhancement'   # 0.56
# gh issue edit 8275 -R numpy/numpy --add-label 'component: numpy._core'   # 0.56
# gh issue edit 8300 -R numpy/numpy --add-label 'component: numpy._core'   # 0.56
# gh issue edit 8735 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.56
# gh issue edit 10047 -R numpy/numpy --add-label '00 - Bug'   # 0.56
# gh issue edit 10179 -R numpy/numpy --add-label 'component: numpy._core'   # 0.56
# gh issue edit 10520 -R numpy/numpy --add-label '00 - Bug'   # 0.56
# gh issue edit 10954 -R numpy/numpy --add-label 'component: numpy._core'   # 0.56
# gh issue edit 13569 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.56
# gh issue edit 16923 -R numpy/numpy --add-label '01 - Enhancement'   # 0.56
# gh issue edit 18484 -R numpy/numpy --add-label '00 - Bug'   # 0.56
# gh issue edit 24345 -R numpy/numpy --add-label 'component: numpy._core'   # 0.56
# gh issue edit 25737 -R numpy/numpy --add-label 'component: build'   # 0.56
# gh issue edit 28310 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.56
# gh issue edit 30813 -R numpy/numpy --add-label 'component: numpy._core'   # 0.56
# gh pr edit 31261 -R numpy/numpy --add-label 'component: numpy._core'   # 0.56
# gh issue edit 31930 -R numpy/numpy --add-label '03 - Maintenance'   # 0.56
# gh issue edit 3659 -R numpy/numpy --add-label '00 - Bug'   # 0.55
# gh issue edit 3817 -R numpy/numpy --add-label '01 - Enhancement'   # 0.55
# gh issue edit 9270 -R numpy/numpy --add-label '00 - Bug'   # 0.55
# gh issue edit 9974 -R numpy/numpy --add-label '00 - Bug'   # 0.55
# gh issue edit 9987 -R numpy/numpy --add-label 'component: numpy._core'   # 0.55
# gh issue edit 11309 -R numpy/numpy --add-label '00 - Bug'   # 0.55
# gh issue edit 17335 -R numpy/numpy --add-label '00 - Bug'   # 0.55
# gh pr edit 31871 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.55
# gh pr edit 32541 -R numpy/numpy --add-label '01 - Enhancement'   # 0.55
# gh issue edit 32865 -R numpy/numpy --add-label '00 - Bug'   # 0.55
# gh issue edit 7829 -R numpy/numpy --add-label '00 - Bug'   # 0.54
# gh issue edit 9397 -R numpy/numpy --add-label 'component: numpy._core'   # 0.54
# gh issue edit 10446 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.54
# gh issue edit 11940 -R numpy/numpy --add-label '00 - Bug'   # 0.54
# gh issue edit 12914 -R numpy/numpy --add-label '00 - Bug'   # 0.54
# gh issue edit 17136 -R numpy/numpy --add-label 'component: numpy._core'   # 0.54
# gh issue edit 18298 -R numpy/numpy --add-label '00 - Bug'   # 0.54
# gh issue edit 27701 -R numpy/numpy --add-label 'component: numpy.strings'   # 0.54
# gh issue edit 30280 -R numpy/numpy --add-label 'component: numpy._core'   # 0.54
# gh issue edit 30353 -R numpy/numpy --add-label '04 - Documentation'   # 0.54
# gh issue edit 3762 -R numpy/numpy --add-label '00 - Bug'   # 0.53
# gh issue edit 4945 -R numpy/numpy --add-label '01 - Enhancement'   # 0.53
# gh issue edit 6555 -R numpy/numpy --add-label '00 - Bug'   # 0.53
# gh issue edit 8097 -R numpy/numpy --add-label '00 - Bug'   # 0.53
# gh issue edit 9921 -R numpy/numpy --add-label '01 - Enhancement'   # 0.53
# gh issue edit 12293 -R numpy/numpy --add-label '00 - Bug'   # 0.53
# gh issue edit 12755 -R numpy/numpy --add-label '01 - Enhancement'   # 0.53
# gh issue edit 15934 -R numpy/numpy --add-label '00 - Bug'   # 0.53
# gh issue edit 17228 -R numpy/numpy --add-label '00 - Bug'   # 0.53
# gh issue edit 19057 -R numpy/numpy --add-label '00 - Bug'   # 0.53
# gh issue edit 19579 -R numpy/numpy --add-label '00 - Bug'   # 0.53
# gh issue edit 19825 -R numpy/numpy --add-label '03 - Maintenance'   # 0.53
# gh pr edit 21843 -R numpy/numpy --add-label '01 - Enhancement'   # 0.53
# gh pr edit 22568 -R numpy/numpy --add-label '00 - Bug'   # 0.53
# gh issue edit 25612 -R numpy/numpy --add-label '01 - Enhancement'   # 0.53
# gh issue edit 32451 -R numpy/numpy --add-label '01 - Enhancement'   # 0.53
# gh issue edit 5261 -R numpy/numpy --add-label '04 - Documentation'   # 0.52
# gh issue edit 5671 -R numpy/numpy --add-label '00 - Bug'   # 0.52
# gh issue edit 10685 -R numpy/numpy --add-label '00 - Bug'   # 0.52
# gh issue edit 11060 -R numpy/numpy --add-label '00 - Bug'   # 0.52
# gh issue edit 11228 -R numpy/numpy --add-label '01 - Enhancement'   # 0.52
# gh issue edit 12701 -R numpy/numpy --add-label '00 - Bug'   # 0.52
# gh issue edit 13284 -R numpy/numpy --add-label '00 - Bug'   # 0.52
# gh issue edit 16741 -R numpy/numpy --add-label '00 - Bug'   # 0.52
# gh issue edit 19113 -R numpy/numpy --add-label '00 - Bug'   # 0.52
# gh pr edit 26708 -R numpy/numpy --add-label '05 - Testing'   # 0.52
# gh issue edit 31409 -R numpy/numpy --add-label '00 - Bug'   # 0.52
# gh pr edit 33202 -R numpy/numpy --add-label '01 - Enhancement'   # 0.52
# gh issue edit 8875 -R numpy/numpy --add-label '00 - Bug'   # 0.51
# gh issue edit 9650 -R numpy/numpy --add-label '00 - Bug'   # 0.51
# gh issue edit 10496 -R numpy/numpy --add-label '00 - Bug'   # 0.51
# gh issue edit 11918 -R numpy/numpy --add-label '00 - Bug'   # 0.51
# gh issue edit 12075 -R numpy/numpy --add-label '00 - Bug'   # 0.51
# gh issue edit 16425 -R numpy/numpy --add-label '03 - Maintenance'   # 0.51
# gh issue edit 18519 -R numpy/numpy --add-label '00 - Bug'   # 0.51
# gh issue edit 30109 -R numpy/numpy --add-label '00 - Bug'   # 0.51
# gh issue edit 5193 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.50
# gh issue edit 5353 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 5867 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 5933 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 5972 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 6555 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 7380 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 7993 -R numpy/numpy --add-label 'component: numpy.ufunc'   # 0.50
# gh issue edit 8509 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 9442 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 10010 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 10179 -R numpy/numpy --add-label '00 - Bug'   # 0.50
# gh issue edit 10513 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 10579 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 11622 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 11881 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 12208 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 12282 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.50
# gh issue edit 12322 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.50
# gh issue edit 12368 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 12900 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 13510 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 14103 -R numpy/numpy --add-label 'component: numpy.testing'   # 0.50
# gh issue edit 14478 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.50
# gh issue edit 17085 -R numpy/numpy --add-label 'component: numpy.random'   # 0.50
# gh issue edit 18700 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 19755 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.50
# gh issue edit 20044 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 20226 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 20859 -R numpy/numpy --add-label 'component: numpy.datetime64'   # 0.50
# gh issue edit 21933 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 21958 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 21990 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.50
# gh issue edit 22059 -R numpy/numpy --add-label 'component: SIMD'   # 0.50
# gh issue edit 22609 -R numpy/numpy --add-label 'component: numpy.ufunc'   # 0.50
# gh issue edit 23203 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 23305 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 24155 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.50
# gh issue edit 24397 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.50
# gh issue edit 24424 -R numpy/numpy --add-label '03 - Maintenance'   # 0.50
# gh issue edit 24900 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.50
# gh issue edit 27577 -R numpy/numpy --add-label 'component: swig'   # 0.50
# gh issue edit 28602 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh pr edit 29260 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh pr edit 30182 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.50
# gh pr edit 30205 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 31292 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh pr edit 31534 -R numpy/numpy --add-label 'component: SIMD'   # 0.50
# gh pr edit 31979 -R numpy/numpy --add-label 'component: numpy.datetime64'   # 0.50
# gh issue edit 32272 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.50
# gh pr edit 32790 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.50
# gh pr edit 32916 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 33016 -R numpy/numpy --add-label 'component: SIMD'   # 0.50
# gh issue edit 33173 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.50
# gh pr edit 33183 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.50
# gh pr edit 33243 -R numpy/numpy --add-label 'component: numpy._core'   # 0.50
# gh issue edit 23899 -R numpy/numpy --add-label 'component: numpy.strings'   # 0.46
# gh issue edit 30440 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.46
# gh pr edit 30449 -R numpy/numpy --add-label 'component: numpy._core'   # 0.46
# gh issue edit 32765 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.46
# gh issue edit 5407 -R numpy/numpy --add-label 'component: numpy._core'   # 0.45
# gh issue edit 8581 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.44
# gh issue edit 9265 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.44
# gh issue edit 9401 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.44
# gh issue edit 9885 -R numpy/numpy --add-label 'component: numpy._core'   # 0.44
# gh issue edit 11569 -R numpy/numpy --add-label 'component: numpy._core'   # 0.44
# gh issue edit 14801 -R numpy/numpy --add-label 'component: numpy._core'   # 0.44
# gh issue edit 16004 -R numpy/numpy --add-label 'component: numpy._core'   # 0.44
# gh issue edit 17554 -R numpy/numpy --add-label 'component: numpy._core'   # 0.44
# gh issue edit 19113 -R numpy/numpy --add-label 'component: numpy._core'   # 0.44
# gh issue edit 20905 -R numpy/numpy --add-label 'component: numpy._core'   # 0.44
# gh issue edit 23523 -R numpy/numpy --add-label 'component: SIMD'   # 0.44
# gh issue edit 25637 -R numpy/numpy --add-label 'component: numpy.ufunc'   # 0.44
# gh pr edit 26650 -R numpy/numpy --add-label 'component: numpy._core'   # 0.44
# gh issue edit 28801 -R numpy/numpy --add-label 'component: benchmarks'   # 0.44
# gh issue edit 29229 -R numpy/numpy --add-label 'component: numpy._core'   # 0.44
# gh pr edit 31175 -R numpy/numpy --add-label 'component: CI'   # 0.44
# gh issue edit 33051 -R numpy/numpy --add-label 'component: numpy._core'   # 0.44
# gh issue edit 4581 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 5150 -R numpy/numpy --add-label 'component: numpy.ufunc'   # 0.43
# gh issue edit 5669 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 6316 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 7383 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh issue edit 7490 -R numpy/numpy --add-label 'component: numpy.testing'   # 0.43
# gh issue edit 7647 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 7730 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 7784 -R numpy/numpy --add-label 'component: numpy.testing'   # 0.43
# gh issue edit 7811 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh issue edit 7811 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 7831 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 7989 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 8151 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 8378 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh issue edit 8378 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.43
# gh issue edit 9128 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 9441 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 9456 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 9526 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh issue edit 9871 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh issue edit 9923 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 9984 -R numpy/numpy --add-label 'component: numpy.einsum'   # 0.43
# gh issue edit 10155 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh issue edit 10469 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 10520 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 10700 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.43
# gh issue edit 10709 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 11214 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh issue edit 11334 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 11701 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 12075 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 12076 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 12258 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 12293 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh issue edit 12444 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 12761 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 12914 -R numpy/numpy --add-label 'component: numpy.fft'   # 0.43
# gh issue edit 13307 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 13527 -R numpy/numpy --add-label 'component: CI'   # 0.43
# gh issue edit 13826 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh issue edit 14119 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 14208 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 14294 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 15625 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 16299 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 16726 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 16985 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 17202 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.43
# gh issue edit 17324 -R numpy/numpy --add-label 'component: numpy.ufunc'   # 0.43
# gh issue edit 17471 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 18020 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh issue edit 18279 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 18279 -R numpy/numpy --add-label 'component: numpy.datetime64'   # 0.43
# gh issue edit 18894 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.43
# gh issue edit 19398 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 19511 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 19623 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh issue edit 19690 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 19970 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh issue edit 20028 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh issue edit 20167 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 20259 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 20566 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 20684 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 20755 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh issue edit 20802 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 20802 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.43
# gh issue edit 21012 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 21375 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.43
# gh issue edit 21780 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.43
# gh issue edit 21791 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 21918 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 21969 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.43
# gh issue edit 22018 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 22133 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 22497 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 22516 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.43
# gh pr edit 22568 -R numpy/numpy --add-label 'component: numpy.datetime64'   # 0.43
# gh issue edit 22682 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 22682 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.43
# gh issue edit 22860 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 22870 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 22977 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 23014 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 23062 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 23107 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 23146 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 23146 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.43
# gh issue edit 23187 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 23330 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 23434 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 23574 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 23576 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 23807 -R numpy/numpy --add-label 'component: build'   # 0.43
# gh issue edit 24339 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 24774 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 24841 -R numpy/numpy --add-label 'component: numpy.distutils'   # 0.43
# gh issue edit 24926 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 24989 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 25872 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.43
# gh issue edit 26177 -R numpy/numpy --add-label 'component: numpy.datetime64'   # 0.43
# gh pr edit 26508 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh issue edit 26818 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 27007 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 27382 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 27435 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 27494 -R numpy/numpy --add-label 'component: numpy.testing'   # 0.43
# gh issue edit 27966 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 28099 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.43
# gh issue edit 28104 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh pr edit 28476 -R numpy/numpy --add-label 'component: CI'   # 0.43
# gh pr edit 28722 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh pr edit 28781 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh pr edit 28802 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh issue edit 29201 -R numpy/numpy --add-label 'component: numpy.datetime64'   # 0.43
# gh issue edit 29393 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.43
# gh issue edit 29664 -R numpy/numpy --add-label 'component: numpy.datetime64'   # 0.43
# gh issue edit 29881 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 30109 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 30116 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh pr edit 30144 -R numpy/numpy --add-label 'component: SIMD'   # 0.43
# gh issue edit 30349 -R numpy/numpy --add-label 'component: numpy.einsum'   # 0.43
# gh pr edit 30372 -R numpy/numpy --add-label 'component: SIMD'   # 0.43
# gh issue edit 30699 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.43
# gh issue edit 30768 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.43
# gh pr edit 30815 -R numpy/numpy --add-label 'component: SIMD'   # 0.43
# gh pr edit 30859 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 30959 -R numpy/numpy --add-label 'component: numpy.datetime64'   # 0.43
# gh issue edit 31083 -R numpy/numpy --add-label 'component: numpy.ufunc'   # 0.43
# gh issue edit 31086 -R numpy/numpy --add-label 'component: numpy.datetime64'   # 0.43
# gh pr edit 31102 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh pr edit 31194 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 31243 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.43
# gh pr edit 31291 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.43
# gh pr edit 31333 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh pr edit 31575 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh pr edit 31595 -R numpy/numpy --add-label 'component: SIMD'   # 0.43
# gh pr edit 31940 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 32126 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.43
# gh pr edit 32157 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh pr edit 32184 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh pr edit 32500 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh pr edit 32504 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 32522 -R numpy/numpy --add-label 'component: numpy.datetime64'   # 0.43
# gh pr edit 32523 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh pr edit 32777 -R numpy/numpy --add-label 'component: numpy.datetime64'   # 0.43
# gh pr edit 32873 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh pr edit 33084 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 33154 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.43
# gh pr edit 33195 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 33203 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh pr edit 33331 -R numpy/numpy --add-label 'component: numpy.random'   # 0.43
# gh pr edit 33342 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh pr edit 33345 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.43
# gh pr edit 33348 -R numpy/numpy --add-label 'component: numpy._core'   # 0.43
# gh issue edit 33352 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.43
# gh pr edit 32239 -R numpy/numpy --add-label 'component: numpy.datetime64'   # 0.42
# gh pr edit 32499 -R numpy/numpy --add-label 'component: numpy._core'   # 0.42
# gh issue edit 5261 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.40
# gh issue edit 6051 -R numpy/numpy --add-label 'component: numpy._core'   # 0.40
# gh issue edit 7967 -R numpy/numpy --add-label 'component: numpy._core'   # 0.40
# gh issue edit 10405 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.40
# gh issue edit 11308 -R numpy/numpy --add-label 'component: numpy._core'   # 0.40
# gh issue edit 16945 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.40
# gh pr edit 30660 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.40
# gh issue edit 5933 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.39
# gh issue edit 18700 -R numpy/numpy --add-label 'component: numpy.ufunc'   # 0.39
# gh issue edit 4829 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 6471 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.38
# gh issue edit 8765 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.38
# gh issue edit 9397 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.38
# gh issue edit 9637 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 9974 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 10799 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 11686 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 11925 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 11940 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 12101 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 12336 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 12900 -R numpy/numpy --add-label 'component: numpy.ufunc'   # 0.38
# gh issue edit 13189 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 13733 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 13768 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 14239 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.38
# gh issue edit 15965 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 17704 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 18516 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 19579 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 20514 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 20596 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 21147 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh pr edit 21843 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.38
# gh issue edit 23362 -R numpy/numpy --add-label 'component: SIMD'   # 0.38
# gh issue edit 23379 -R numpy/numpy --add-label 'component: build'   # 0.38
# gh issue edit 23582 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 24755 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 25363 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 25693 -R numpy/numpy --add-label 'component: numpy.strings'   # 0.38
# gh issue edit 25787 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.38
# gh issue edit 26620 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh issue edit 28165 -R numpy/numpy --add-label 'component: numpy.strings'   # 0.38
# gh issue edit 28397 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh pr edit 30449 -R numpy/numpy --add-label 'component: numpy.ufunc'   # 0.38
# gh pr edit 31559 -R numpy/numpy --add-label 'component: numpy.dtype'   # 0.38
# gh pr edit 32026 -R numpy/numpy --add-label 'component: numpy.random'   # 0.38
# gh pr edit 32732 -R numpy/numpy --add-label 'component: numpy._core'   # 0.38
# gh pr edit 33216 -R numpy/numpy --add-label 'component: numpy.ma'   # 0.38
# gh issue edit 6081 -R numpy/numpy --add-label 'component: npy_math'   # 0.36
# gh issue edit 20785 -R numpy/numpy --add-label 'component: SIMD'   # 0.36
# gh issue edit 23176 -R numpy/numpy --add-label 'component: numpy.ufunc'   # 0.36
# gh issue edit 26289 -R numpy/numpy --add-label 'component: build'   # 0.36
# gh issue edit 28839 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.36
# gh issue edit 30216 -R numpy/numpy --add-label 'component: CI'   # 0.36
# gh issue edit 5842 -R numpy/numpy --add-label 'component: numpy._core'   # 0.33
# gh issue edit 6951 -R numpy/numpy --add-label 'component: numpy._core'   # 0.33
# gh issue edit 7265 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.33
# gh issue edit 8581 -R numpy/numpy --add-label 'component: numpy._core'   # 0.33
# gh issue edit 9450 -R numpy/numpy --add-label 'component: numpy._core'   # 0.33
# gh issue edit 10954 -R numpy/numpy --add-label 'component: npy_math'   # 0.33
# gh issue edit 12935 -R numpy/numpy --add-label 'component: numpy._core'   # 0.33
# gh issue edit 13375 -R numpy/numpy --add-label 'component: numpy._core'   # 0.33
# gh issue edit 13569 -R numpy/numpy --add-label 'component: numpy._core'   # 0.33
# gh issue edit 14020 -R numpy/numpy --add-label 'component: numpy._core'   # 0.33
# gh issue edit 17744 -R numpy/numpy --add-label 'component: numpy._core'   # 0.33
# gh pr edit 24467 -R numpy/numpy --add-label 'component: numpy.polynomial'   # 0.33
# gh issue edit 25306 -R numpy/numpy --add-label 'component: numpy._core'   # 0.33
# gh issue edit 26940 -R numpy/numpy --add-label 'component: SIMD'   # 0.33
# gh issue edit 29229 -R numpy/numpy --add-label 'component: numpy.strings'   # 0.33
# gh issue edit 29485 -R numpy/numpy --add-label 'component: numpy.datetime64'   # 0.33
# gh issue edit 30171 -R numpy/numpy --add-label 'component: numpy.einsum'   # 0.33
# gh issue edit 31030 -R numpy/numpy --add-label 'component: numpy.ufunc'   # 0.33
# gh issue edit 31259 -R numpy/numpy --add-label 'component: numpy._core'   # 0.33
# gh issue edit 31926 -R numpy/numpy --add-label 'component: numpy.datetime64'   # 0.33
# gh issue edit 32071 -R numpy/numpy --add-label 'component: numpy._core'   # 0.33
# gh issue edit 32482 -R numpy/numpy --add-label 'component: npy_math'   # 0.33
# gh pr edit 32622 -R numpy/numpy --add-label 'component: numpy._core'   # 0.33
# gh issue edit 8513 -R numpy/numpy --add-label 'component: numpy.ufunc'   # 0.32
# gh issue edit 17012 -R numpy/numpy --add-label 'component: numpy._core'   # 0.31
# gh issue edit 8518 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.30
# gh issue edit 9516 -R numpy/numpy --add-label 'component: numpy.linalg'   # 0.30
# gh issue edit 10405 -R numpy/numpy --add-label 'component: numpy._core'   # 0.30
# gh issue edit 12481 -R numpy/numpy --add-label 'component: numpy._core'   # 0.30
# gh issue edit 14412 -R numpy/numpy --add-label 'component: numpy._core'   # 0.30
# gh issue edit 16945 -R numpy/numpy --add-label 'component: numpy._core'   # 0.30
# gh pr edit 19550 -R numpy/numpy --add-label 'component: numpy._core'   # 0.30
# gh issue edit 27785 -R numpy/numpy --add-label 'component: numpy.random'   # 0.30
# gh issue edit 33336 -R numpy/numpy --add-label 'component: CI'   # 0.30
# gh issue edit 13105 -R numpy/numpy --add-label 'component: numpy._core'   # 0.29
# gh issue edit 8773 -R numpy/numpy --add-label 'component: numpy.ufunc'   # 0.27
# gh issue edit 11092 -R numpy/numpy --add-label 'component: numpy.lib'   # 0.27
# gh issue edit 11092 -R numpy/numpy --add-label 'component: numpy._core'   # 0.27
# gh issue edit 22318 -R numpy/numpy --add-label 'component: CI'   # 0.27
# gh issue edit 22318 -R numpy/numpy --add-label 'component: distribution'   # 0.27
# gh issue edit 30216 -R numpy/numpy --add-label 'component: distribution'   # 0.27
# gh issue edit 9631 -R numpy/numpy --add-label 'component: numpy.ufunc'   # 0.25
# gh issue edit 11622 -R numpy/numpy --add-label 'component: numpy.ufunc'   # 0.25
# gh pr edit 24189 -R numpy/numpy --add-label 'component: numpy._core'   # 0.25
# gh pr edit 25703 -R numpy/numpy --add-label 'component: numpy._core'   # 0.25
# gh issue edit 10446 -R numpy/numpy --add-label 'component: numpy._core'   # 0.23
# gh issue edit 25693 -R numpy/numpy --add-label 'component: numpy._core'   # 0.23
# gh issue edit 32765 -R numpy/numpy --add-label 'component: numpy.strings'   # 0.23
