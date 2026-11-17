#!/bin/sh
# Proposed actions for opencv/opencv. Review report.md, then remove the leading '# ' from the lines you agree with.

# --- Open issues already marked as duplicates (5)
# gh issue close 4269 -R opencv/opencv --reason "not planned" --comment "Duplicate of #17892"   # 1.00
# gh issue close 7479 -R opencv/opencv --reason "not planned" --comment "Duplicate of #16850"   # 1.00
# gh issue close 9477 -R opencv/opencv --reason "not planned" --comment "Duplicate of #20531"   # 1.00
# gh issue close 12001 -R opencv/opencv --reason "not planned" --comment "Duplicate of #17445"   # 1.00
# gh issue close 15352 -R opencv/opencv --reason "not planned" --comment "Duplicate of #17257"   # 1.00

# --- Open issues whose closing PR is merged (42)
# gh issue close 4235 -R opencv/opencv --reason completed --comment "Closed by #7966"   # 0.99
# gh issue close 7276 -R opencv/opencv --reason completed --comment "Closed by #30086"   # 0.99
# gh issue close 7606 -R opencv/opencv --reason completed --comment "Closed by #7913"   # 0.99
# gh issue close 9179 -R opencv/opencv --reason completed --comment "Closed by #14092"   # 0.99
# gh issue close 9477 -R opencv/opencv --reason completed --comment "Closed by #9479"   # 0.99
# gh issue close 9575 -R opencv/opencv --reason completed --comment "Closed by #10834"   # 0.99
# gh issue close 9908 -R opencv/opencv --reason completed --comment "Closed by #10497"   # 0.99
# gh issue close 10158 -R opencv/opencv --reason completed --comment "Closed by #20618"   # 0.99
# gh issue close 12077 -R opencv/opencv --reason completed --comment "Closed by #15100"   # 0.99
# gh issue close 12343 -R opencv/opencv --reason completed --comment "Closed by #30823"   # 0.99
# gh issue close 13523 -R opencv/opencv --reason completed --comment "Closed by #16006"   # 0.99
# gh issue close 13822 -R opencv/opencv --reason completed --comment "Closed by #16165"   # 0.99
# gh issue close 16394 -R opencv/opencv --reason completed --comment "Closed by #19721"   # 0.99
# gh issue close 16940 -R opencv/opencv --reason completed --comment "Closed by #16947"   # 0.99
# gh issue close 17094 -R opencv/opencv --reason completed --comment "Closed by #17256"   # 0.99
# gh issue close 19587 -R opencv/opencv --reason completed --comment "Closed by #29927"   # 0.99
# gh issue close 20305 -R opencv/opencv --reason completed --comment "Closed by #29943"   # 0.99
# gh issue close 20979 -R opencv/opencv --reason completed --comment "Closed by #30597"   # 0.99
# gh issue close 21055 -R opencv/opencv --reason completed --comment "Closed by #30508"   # 0.99
# gh issue close 21120 -R opencv/opencv --reason completed --comment "Closed by #30130"   # 0.99
# gh issue close 21175 -R opencv/opencv --reason completed --comment "Closed by #21182"   # 0.99
# gh issue close 21983 -R opencv/opencv --reason completed --comment "Closed by #22164"   # 0.99
# gh issue close 22243 -R opencv/opencv --reason completed --comment "Closed by #29913"   # 0.99
# gh issue close 22746 -R opencv/opencv --reason completed --comment "Closed by #29077"   # 0.99
# gh issue close 22763 -R opencv/opencv --reason completed --comment "Closed by #30389"   # 0.99
# gh issue close 23906 -R opencv/opencv --reason completed --comment "Closed by #25809"   # 0.99
# gh issue close 24914 -R opencv/opencv --reason completed --comment "Closed by #29093"   # 0.99
# gh issue close 25320 -R opencv/opencv --reason completed --comment "Closed by #25321"   # 0.99
# gh issue close 25367 -R opencv/opencv --reason completed --comment "Closed by #30316"   # 0.99
# gh issue close 25904 -R opencv/opencv --reason completed --comment "Closed by #28275"   # 0.99
# gh issue close 26407 -R opencv/opencv --reason completed --comment "Closed by #30727"   # 0.99
# gh issue close 26519 -R opencv/opencv --reason completed --comment "Closed by #30435"   # 0.99
# gh issue close 26552 -R opencv/opencv --reason completed --comment "Closed by #26559"   # 0.99
# gh issue close 26642 -R opencv/opencv --reason completed --comment "Closed by #26650"   # 0.99
# gh issue close 26952 -R opencv/opencv --reason completed --comment "Closed by #29714"   # 0.99
# gh issue close 28904 -R opencv/opencv --reason completed --comment "Closed by #28914"   # 0.99
# gh issue close 28910 -R opencv/opencv --reason completed --comment "Closed by #29878"   # 0.99
# gh issue close 29419 -R opencv/opencv --reason completed --comment "Closed by #29425"   # 0.99
# gh issue close 29454 -R opencv/opencv --reason completed --comment "Closed by #29493"   # 0.99
# gh issue close 30338 -R opencv/opencv --reason completed --comment "Closed by #30351"   # 0.99
# gh issue close 30744 -R opencv/opencv --reason completed --comment "Closed by #30797"   # 0.99
# gh issue close 30857 -R opencv/opencv --reason completed --comment "Closed by #30860"   # 0.99

# --- Likely duplicates of an older open issue (32)
# gh issue close 29869 -R opencv/opencv --reason "not planned" --comment "Duplicate of #29845"   # 0.99
# gh issue close 17002 -R opencv/opencv --reason "not planned" --comment "Duplicate of #4322"   # 0.98
# gh issue close 27281 -R opencv/opencv --reason "not planned" --comment "Duplicate of #27279"   # 0.97
# gh issue close 21457 -R opencv/opencv --reason "not planned" --comment "Duplicate of #12969"   # 0.96
# gh issue close 21930 -R opencv/opencv --reason "not planned" --comment "Duplicate of #21928"   # 0.96
# gh issue close 13414 -R opencv/opencv --reason "not planned" --comment "Duplicate of #11797"   # 0.94
# gh issue close 25223 -R opencv/opencv --reason "not planned" --comment "Duplicate of #23864"   # 0.94
# gh issue close 28948 -R opencv/opencv --reason "not planned" --comment "Duplicate of #28913"   # 0.94
# gh issue close 21443 -R opencv/opencv --reason "not planned" --comment "Duplicate of #21419"   # 0.93
# gh issue close 23316 -R opencv/opencv --reason "not planned" --comment "Duplicate of #23314"   # 0.93
# gh issue close 25104 -R opencv/opencv --reason "not planned" --comment "Duplicate of #8782"   # 0.93
# gh issue close 30384 -R opencv/opencv --reason "not planned" --comment "Duplicate of #4728"   # 0.93
# gh issue close 11779 -R opencv/opencv --reason "not planned" --comment "Duplicate of #11778"   # 0.92
# gh issue close 19262 -R opencv/opencv --reason "not planned" --comment "Duplicate of #19261"   # 0.92
# gh issue close 20214 -R opencv/opencv --reason "not planned" --comment "Duplicate of #18893"   # 0.92
# gh issue close 22582 -R opencv/opencv --reason "not planned" --comment "Duplicate of #18654"   # 0.92
# gh issue close 24924 -R opencv/opencv --reason "not planned" --comment "Duplicate of #23425"   # 0.92
# gh issue close 25850 -R opencv/opencv --reason "not planned" --comment "Duplicate of #23873"   # 0.92
# gh issue close 27215 -R opencv/opencv --reason "not planned" --comment "Duplicate of #5688"   # 0.92
# gh issue close 27306 -R opencv/opencv --reason "not planned" --comment "Duplicate of #25742"   # 0.92
# gh issue close 29590 -R opencv/opencv --reason "not planned" --comment "Duplicate of #29588"   # 0.92
# gh issue close 4691 -R opencv/opencv --reason "not planned" --comment "Duplicate of #4640"   # 0.91
# gh issue close 8052 -R opencv/opencv --reason "not planned" --comment "Duplicate of #4502"   # 0.91
# gh issue close 11383 -R opencv/opencv --reason "not planned" --comment "Duplicate of #8672"   # 0.91
# gh issue close 13819 -R opencv/opencv --reason "not planned" --comment "Duplicate of #7938"   # 0.91
# gh issue close 22532 -R opencv/opencv --reason "not planned" --comment "Duplicate of #19457"   # 0.91
# gh issue close 23385 -R opencv/opencv --reason "not planned" --comment "Duplicate of #23384"   # 0.91
# gh issue close 23738 -R opencv/opencv --reason "not planned" --comment "Duplicate of #23385"   # 0.91
# gh issue close 23826 -R opencv/opencv --reason "not planned" --comment "Duplicate of #23212"   # 0.91
# gh issue close 25121 -R opencv/opencv --reason "not planned" --comment "Duplicate of #23864"   # 0.91
# gh issue close 26360 -R opencv/opencv --reason "not planned" --comment "Duplicate of #26078"   # 0.91
# gh issue close 30862 -R opencv/opencv --reason "not planned" --comment "Duplicate of #30861"   # 0.91

# --- Open issues very similar to an older closed one (came back, or a duplicate of something settled?) (89)
# gh issue view 6520 -R opencv/opencv; gh issue view 7480 -R opencv/opencv   # 0.99
# gh issue view 8261 -R opencv/opencv; gh issue view 8262 -R opencv/opencv   # 0.99
# gh issue view 7570 -R opencv/opencv; gh issue view 8351 -R opencv/opencv   # 0.99
# gh issue view 27197 -R opencv/opencv; gh issue view 27198 -R opencv/opencv   # 0.98
# gh issue view 4329 -R opencv/opencv; gh issue view 5078 -R opencv/opencv   # 0.97
# gh issue view 9739 -R opencv/opencv; gh issue view 11834 -R opencv/opencv   # 0.97
# gh issue view 24455 -R opencv/opencv; gh issue view 24489 -R opencv/opencv   # 0.97
# gh issue view 23199 -R opencv/opencv; gh issue view 24937 -R opencv/opencv   # 0.97
# gh issue view 25570 -R opencv/opencv; gh issue view 25571 -R opencv/opencv   # 0.97
# gh issue view 19118 -R opencv/opencv; gh issue view 19119 -R opencv/opencv   # 0.96
# gh issue view 26502 -R opencv/opencv; gh issue view 27034 -R opencv/opencv   # 0.96
# gh issue view 11487 -R opencv/opencv; gh issue view 11510 -R opencv/opencv   # 0.95
# gh issue view 14536 -R opencv/opencv; gh issue view 17597 -R opencv/opencv   # 0.95
# gh issue view 16380 -R opencv/opencv; gh issue view 21774 -R opencv/opencv   # 0.95
# gh issue view 22622 -R opencv/opencv; gh issue view 22768 -R opencv/opencv   # 0.95
# gh issue view 26609 -R opencv/opencv; gh issue view 26718 -R opencv/opencv   # 0.95
# gh issue view 4890 -R opencv/opencv; gh issue view 9053 -R opencv/opencv   # 0.94
# gh issue view 10614 -R opencv/opencv; gh issue view 10615 -R opencv/opencv   # 0.94
# gh issue view 6500 -R opencv/opencv; gh issue view 13205 -R opencv/opencv   # 0.94
# gh issue view 21634 -R opencv/opencv; gh issue view 23058 -R opencv/opencv   # 0.94
# gh issue view 23205 -R opencv/opencv; gh issue view 23207 -R opencv/opencv   # 0.94
# gh issue view 13015 -R opencv/opencv; gh issue view 26341 -R opencv/opencv   # 0.94
# gh issue view 11480 -R opencv/opencv; gh issue view 17169 -R opencv/opencv   # 0.93
# gh issue view 14123 -R opencv/opencv; gh issue view 20093 -R opencv/opencv   # 0.93
# gh issue view 16449 -R opencv/opencv; gh issue view 20319 -R opencv/opencv   # 0.93
# gh issue view 13276 -R opencv/opencv; gh issue view 20552 -R opencv/opencv   # 0.93
# gh issue view 16879 -R opencv/opencv; gh issue view 21842 -R opencv/opencv   # 0.93
# gh issue view 19574 -R opencv/opencv; gh issue view 21906 -R opencv/opencv   # 0.93
# gh issue view 17661 -R opencv/opencv; gh issue view 22379 -R opencv/opencv   # 0.93
# gh issue view 25562 -R opencv/opencv; gh issue view 26064 -R opencv/opencv   # 0.93
# gh issue view 30158 -R opencv/opencv; gh issue view 30413 -R opencv/opencv   # 0.93
# gh issue view 30684 -R opencv/opencv; gh issue view 30697 -R opencv/opencv   # 0.93
# gh issue view 4530 -R opencv/opencv; gh issue view 4591 -R opencv/opencv   # 0.92
# gh issue view 6585 -R opencv/opencv; gh issue view 6587 -R opencv/opencv   # 0.92
# gh issue view 4428 -R opencv/opencv; gh issue view 6630 -R opencv/opencv   # 0.92
# gh issue view 6781 -R opencv/opencv; gh issue view 6897 -R opencv/opencv   # 0.92
# gh issue view 7591 -R opencv/opencv; gh issue view 8904 -R opencv/opencv   # 0.92
# gh issue view 7407 -R opencv/opencv; gh issue view 9685 -R opencv/opencv   # 0.92
# gh issue view 9096 -R opencv/opencv; gh issue view 10146 -R opencv/opencv   # 0.92
# gh issue view 5031 -R opencv/opencv; gh issue view 11359 -R opencv/opencv   # 0.92
# gh issue view 7974 -R opencv/opencv; gh issue view 15533 -R opencv/opencv   # 0.92
# gh issue view 13759 -R opencv/opencv; gh issue view 18654 -R opencv/opencv   # 0.92
# gh issue view 15129 -R opencv/opencv; gh issue view 19366 -R opencv/opencv   # 0.92
# gh issue view 18728 -R opencv/opencv; gh issue view 20997 -R opencv/opencv   # 0.92
# gh issue view 21810 -R opencv/opencv; gh issue view 21814 -R opencv/opencv   # 0.92
# gh issue view 21149 -R opencv/opencv; gh issue view 22011 -R opencv/opencv   # 0.92
# gh issue view 21080 -R opencv/opencv; gh issue view 22152 -R opencv/opencv   # 0.92
# gh issue view 7045 -R opencv/opencv; gh issue view 22157 -R opencv/opencv   # 0.92
# gh issue view 22487 -R opencv/opencv; gh issue view 22590 -R opencv/opencv   # 0.92
# gh issue view 10739 -R opencv/opencv; gh issue view 22658 -R opencv/opencv   # 0.92
# gh issue view 17107 -R opencv/opencv; gh issue view 22881 -R opencv/opencv   # 0.92
# gh issue view 9745 -R opencv/opencv; gh issue view 23252 -R opencv/opencv   # 0.92
# gh issue view 22631 -R opencv/opencv; gh issue view 23298 -R opencv/opencv   # 0.92
# gh issue view 19888 -R opencv/opencv; gh issue view 23428 -R opencv/opencv   # 0.92
# gh issue view 10671 -R opencv/opencv; gh issue view 23430 -R opencv/opencv   # 0.92
# gh issue view 17291 -R opencv/opencv; gh issue view 23507 -R opencv/opencv   # 0.92
# gh issue view 12646 -R opencv/opencv; gh issue view 23593 -R opencv/opencv   # 0.92
# gh issue view 18735 -R opencv/opencv; gh issue view 24110 -R opencv/opencv   # 0.92
# gh issue view 22304 -R opencv/opencv; gh issue view 24430 -R opencv/opencv   # 0.92
# gh issue view 20863 -R opencv/opencv; gh issue view 24506 -R opencv/opencv   # 0.92
# gh issue view 18543 -R opencv/opencv; gh issue view 25929 -R opencv/opencv   # 0.92
# gh issue view 24000 -R opencv/opencv; gh issue view 26250 -R opencv/opencv   # 0.92
# gh issue view 27159 -R opencv/opencv; gh issue view 27200 -R opencv/opencv   # 0.92
# gh issue view 28597 -R opencv/opencv; gh issue view 29238 -R opencv/opencv   # 0.92
# gh issue view 23791 -R opencv/opencv; gh issue view 29419 -R opencv/opencv   # 0.92
# gh issue view 29279 -R opencv/opencv; gh issue view 30459 -R opencv/opencv   # 0.92
# gh issue view 4518 -R opencv/opencv; gh issue view 5060 -R opencv/opencv   # 0.91
# gh issue view 6749 -R opencv/opencv; gh issue view 11277 -R opencv/opencv   # 0.91
# gh issue view 7652 -R opencv/opencv; gh issue view 18041 -R opencv/opencv   # 0.91
# gh issue view 14527 -R opencv/opencv; gh issue view 18183 -R opencv/opencv   # 0.91
# gh issue view 11452 -R opencv/opencv; gh issue view 18759 -R opencv/opencv   # 0.91
# gh issue view 13255 -R opencv/opencv; gh issue view 19737 -R opencv/opencv   # 0.91
# gh issue view 14527 -R opencv/opencv; gh issue view 20907 -R opencv/opencv   # 0.91
# gh issue view 21395 -R opencv/opencv; gh issue view 21396 -R opencv/opencv   # 0.91
# gh issue view 16397 -R opencv/opencv; gh issue view 21419 -R opencv/opencv   # 0.91
# gh issue view 12646 -R opencv/opencv; gh issue view 21571 -R opencv/opencv   # 0.91
# gh issue view 6093 -R opencv/opencv; gh issue view 22984 -R opencv/opencv   # 0.91
# gh issue view 16029 -R opencv/opencv; gh issue view 23097 -R opencv/opencv   # 0.91
# gh issue view 8625 -R opencv/opencv; gh issue view 23212 -R opencv/opencv   # 0.91
# gh issue view 16323 -R opencv/opencv; gh issue view 23297 -R opencv/opencv   # 0.91
# gh issue view 10363 -R opencv/opencv; gh issue view 23396 -R opencv/opencv   # 0.91
# gh issue view 12646 -R opencv/opencv; gh issue view 23548 -R opencv/opencv   # 0.91
# gh issue view 7332 -R opencv/opencv; gh issue view 24831 -R opencv/opencv   # 0.91
# gh issue view 24964 -R opencv/opencv; gh issue view 24971 -R opencv/opencv   # 0.91
# gh issue view 14706 -R opencv/opencv; gh issue view 25614 -R opencv/opencv   # 0.91
# gh issue view 18382 -R opencv/opencv; gh issue view 25744 -R opencv/opencv   # 0.91
# gh issue view 18209 -R opencv/opencv; gh issue view 26674 -R opencv/opencv   # 0.91
# gh issue view 15712 -R opencv/opencv; gh issue view 27885 -R opencv/opencv   # 0.91
# gh issue view 9150 -R opencv/opencv; gh issue view 29692 -R opencv/opencv   # 0.91

# --- Open issues that a later merged PR seems to fix (64)
# gh issue close 27452 -R opencv/opencv --reason completed --comment "Looks fixed by #27453"   # 0.96
# gh issue close 29150 -R opencv/opencv --reason completed --comment "Looks fixed by #29151"   # 0.96
# gh issue close 19648 -R opencv/opencv --reason completed --comment "Looks fixed by #28087"   # 0.94
# gh issue close 30569 -R opencv/opencv --reason completed --comment "Looks fixed by #30570"   # 0.94
# gh issue close 14461 -R opencv/opencv --reason completed --comment "Looks fixed by #30509"   # 0.93
# gh issue close 19587 -R opencv/opencv --reason completed --comment "Looks fixed by #27959"   # 0.93
# gh issue close 22093 -R opencv/opencv --reason completed --comment "Looks fixed by #29506"   # 0.93
# gh issue close 22573 -R opencv/opencv --reason completed --comment "Looks fixed by #24782"   # 0.93
# gh issue close 28222 -R opencv/opencv --reason completed --comment "Looks fixed by #28227"   # 0.93
# gh issue close 18546 -R opencv/opencv --reason completed --comment "Looks fixed by #18547"   # 0.92
# gh issue close 21880 -R opencv/opencv --reason completed --comment "Looks fixed by #24949"   # 0.92
# gh issue close 23326 -R opencv/opencv --reason completed --comment "Looks fixed by #24153"   # 0.92
# gh issue close 23624 -R opencv/opencv --reason completed --comment "Looks fixed by #23985"   # 0.92
# gh issue close 23930 -R opencv/opencv --reason completed --comment "Looks fixed by #25603"   # 0.92
# gh issue close 7386 -R opencv/opencv --reason completed --comment "Looks fixed by #29856"   # 0.91
# gh issue close 11003 -R opencv/opencv --reason completed --comment "Looks fixed by #13909"   # 0.91
# gh issue close 25547 -R opencv/opencv --reason completed --comment "Looks fixed by #26580"   # 0.91
# gh issue close 25904 -R opencv/opencv --reason completed --comment "Looks fixed by #29255"   # 0.91
# gh issue close 27967 -R opencv/opencv --reason completed --comment "Looks fixed by #28018"   # 0.91
# gh issue close 4269 -R opencv/opencv --reason completed --comment "Looks fixed by #29843"   # 0.90
# gh issue close 4304 -R opencv/opencv --reason completed --comment "Looks fixed by #21407"   # 0.90
# gh issue close 9529 -R opencv/opencv --reason completed --comment "Looks fixed by #12829"   # 0.90
# gh issue close 18625 -R opencv/opencv --reason completed --comment "Looks fixed by #24142"   # 0.90
# gh issue close 22835 -R opencv/opencv --reason completed --comment "Looks fixed by #22836"   # 0.90
# gh issue close 25155 -R opencv/opencv --reason completed --comment "Looks fixed by #27823"   # 0.90
# gh issue close 26407 -R opencv/opencv --reason completed --comment "Looks fixed by #30121"   # 0.90
# gh issue close 30067 -R opencv/opencv --reason completed --comment "Looks fixed by #30072"   # 0.90
# gh issue close 30630 -R opencv/opencv --reason completed --comment "Looks fixed by #30755"   # 0.90
# gh issue close 4249 -R opencv/opencv --reason completed --comment "Looks fixed by #22460"   # 0.89
# gh issue close 4270 -R opencv/opencv --reason completed --comment "Looks fixed by #10569"   # 0.89
# gh issue close 4371 -R opencv/opencv --reason completed --comment "Looks fixed by #20012"   # 0.89
# gh issue close 4426 -R opencv/opencv --reason completed --comment "Looks fixed by #5484"   # 0.89
# gh issue close 4574 -R opencv/opencv --reason completed --comment "Looks fixed by #26366"   # 0.89
# gh issue close 4914 -R opencv/opencv --reason completed --comment "Looks fixed by #26831"   # 0.89
# gh issue close 15647 -R opencv/opencv --reason completed --comment "Looks fixed by #18371"   # 0.89
# gh issue close 26963 -R opencv/opencv --reason completed --comment "Looks fixed by #27949"   # 0.89
# gh issue close 30211 -R opencv/opencv --reason completed --comment "Looks fixed by #30213"   # 0.89
# gh issue close 4598 -R opencv/opencv --reason completed --comment "Looks fixed by #14015"   # 0.88
# gh issue close 5012 -R opencv/opencv --reason completed --comment "Looks fixed by #8044"   # 0.88
# gh issue close 5688 -R opencv/opencv --reason completed --comment "Looks fixed by #12916"   # 0.88
# gh issue close 6117 -R opencv/opencv --reason completed --comment "Looks fixed by #14362"   # 0.88
# gh issue close 6630 -R opencv/opencv --reason completed --comment "Looks fixed by #7887"   # 0.88
# gh issue close 9643 -R opencv/opencv --reason completed --comment "Looks fixed by #19780"   # 0.88
# gh issue close 11039 -R opencv/opencv --reason completed --comment "Looks fixed by #12827"   # 0.88
# gh issue close 13121 -R opencv/opencv --reason completed --comment "Looks fixed by #13124"   # 0.88
# gh issue close 16433 -R opencv/opencv --reason completed --comment "Looks fixed by #23913"   # 0.88
# gh issue close 17491 -R opencv/opencv --reason completed --comment "Looks fixed by #18073"   # 0.88
# gh issue close 19678 -R opencv/opencv --reason completed --comment "Looks fixed by #29754"   # 0.88
# gh issue close 20527 -R opencv/opencv --reason completed --comment "Looks fixed by #29926"   # 0.88
# gh issue close 23066 -R opencv/opencv --reason completed --comment "Looks fixed by #25611"   # 0.88
# gh issue close 23116 -R opencv/opencv --reason completed --comment "Looks fixed by #24243"   # 0.88
# gh issue close 23845 -R opencv/opencv --reason completed --comment "Looks fixed by #25035"   # 0.88
# gh issue close 24891 -R opencv/opencv --reason completed --comment "Looks fixed by #24893"   # 0.88
# gh issue close 24902 -R opencv/opencv --reason completed --comment "Looks fixed by #24903"   # 0.88
# gh issue close 25895 -R opencv/opencv --reason completed --comment "Looks fixed by #27573"   # 0.88
# gh issue close 26574 -R opencv/opencv --reason completed --comment "Looks fixed by #26625"   # 0.88
# gh issue close 27276 -R opencv/opencv --reason completed --comment "Looks fixed by #27443"   # 0.88
# gh issue close 27515 -R opencv/opencv --reason completed --comment "Looks fixed by #29928"   # 0.88
# gh issue close 28608 -R opencv/opencv --reason completed --comment "Looks fixed by #28611"   # 0.88
# gh issue close 4651 -R opencv/opencv --reason completed --comment "Looks fixed by #7754"   # 0.87
# gh issue close 13549 -R opencv/opencv --reason completed --comment "Looks fixed by #17208"   # 0.87
# gh issue close 15315 -R opencv/opencv --reason completed --comment "Looks fixed by #15425"   # 0.87
# gh issue close 23471 -R opencv/opencv --reason completed --comment "Looks fixed by #28735"   # 0.87
# gh issue close 25853 -R opencv/opencv --reason completed --comment "Looks fixed by #25898"   # 0.87

# --- Open PRs after the same thing (13)
# gh pr view 28037 -R opencv/opencv; gh pr view 28623 -R opencv/opencv   # 0.99
# gh pr view 28037 -R opencv/opencv; gh pr view 28736 -R opencv/opencv   # 0.99
# gh pr view 28623 -R opencv/opencv; gh pr view 28736 -R opencv/opencv   # 0.99
# gh pr view 29775 -R opencv/opencv; gh pr view 29959 -R opencv/opencv   # 0.99
# gh pr view 29863 -R opencv/opencv; gh pr view 29873 -R opencv/opencv   # 0.99
# gh pr view 29980 -R opencv/opencv; gh pr view 29992 -R opencv/opencv   # 0.99
# gh pr view 30377 -R opencv/opencv; gh pr view 30378 -R opencv/opencv   # 0.99
# gh pr view 29285 -R opencv/opencv; gh pr view 29527 -R opencv/opencv   # 0.96
# gh pr view 27155 -R opencv/opencv; gh pr view 27554 -R opencv/opencv   # 0.94
# gh pr view 28942 -R opencv/opencv; gh pr view 29136 -R opencv/opencv   # 0.94
# gh pr view 29746 -R opencv/opencv; gh pr view 30179 -R opencv/opencv   # 0.94
# gh pr view 30788 -R opencv/opencv; gh pr view 30880 -R opencv/opencv   # 0.93
# gh pr view 30665 -R opencv/opencv; gh pr view 30767 -R opencv/opencv   # 0.91

# --- Labels to add (1219)
# gh issue edit 13773 -R opencv/opencv --add-label 'category: core'   # 0.99
# gh issue edit 18313 -R opencv/opencv --add-label 'category: calib3d'   # 0.99
# gh issue edit 20563 -R opencv/opencv --add-label 'category: core'   # 0.99
# gh issue edit 22351 -R opencv/opencv --add-label 'category: calib3d'   # 0.99
# gh issue edit 22680 -R opencv/opencv --add-label 'category: videoio'   # 0.99
# gh issue edit 22835 -R opencv/opencv --add-label 'category: build/install'   # 0.99
# gh issue edit 22983 -R opencv/opencv --add-label 'category: build/install'   # 0.99
# gh issue edit 24115 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.99
# gh issue edit 24661 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.99
# gh issue edit 25179 -R opencv/opencv --add-label 'category: core'   # 0.99
# gh issue edit 25462 -R opencv/opencv --add-label 'category: dnn'   # 0.99
# gh issue edit 25783 -R opencv/opencv --add-label 'category: stitching'   # 0.99
# gh issue edit 26244 -R opencv/opencv --add-label test   # 0.99
# gh issue edit 26360 -R opencv/opencv --add-label 'category: imgproc'   # 0.99
# gh issue edit 28658 -R opencv/opencv --add-label 'category: python bindings'   # 0.99
# gh issue edit 29573 -R opencv/opencv --add-label 'category: calib3d'   # 0.99
# gh issue edit 30442 -R opencv/opencv --add-label 'category: core'   # 0.99
# gh pr edit 30462 -R opencv/opencv --add-label optimization   # 0.99
# gh pr edit 30484 -R opencv/opencv --add-label 'category: calib3d'   # 0.99
# gh pr edit 30623 -R opencv/opencv --add-label 'category: core'   # 0.99
# gh pr edit 30647 -R opencv/opencv --add-label bug   # 0.99
# gh pr edit 30702 -R opencv/opencv --add-label 'category: core'   # 0.99
# gh issue edit 30815 -R opencv/opencv --add-label 'category: imgproc'   # 0.99
# gh issue edit 30818 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.99
# gh issue edit 30017 -R opencv/opencv --add-label 'category: videoio'   # 0.94
# gh pr edit 30462 -R opencv/opencv --add-label 'category: dnn'   # 0.94
# gh issue edit 15768 -R opencv/opencv --add-label bug   # 0.93
# gh issue edit 27022 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.93
# gh issue edit 30362 -R opencv/opencv --add-label 'category: imgproc'   # 0.93
# gh issue edit 30858 -R opencv/opencv --add-label bug   # 0.93
# gh issue edit 30861 -R opencv/opencv --add-label bug   # 0.93
# gh issue edit 12229 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.92
# gh issue edit 21155 -R opencv/opencv --add-label 'category: documentation'   # 0.92
# gh issue edit 21184 -R opencv/opencv --add-label 'category: documentation'   # 0.92
# gh issue edit 21515 -R opencv/opencv --add-label 'category: objdetect'   # 0.92
# gh issue edit 21544 -R opencv/opencv --add-label 'category: documentation'   # 0.92
# gh issue edit 24115 -R opencv/opencv --add-label 'category: documentation'   # 0.92
# gh pr edit 28044 -R opencv/opencv --add-label bug   # 0.92
# gh pr edit 29063 -R opencv/opencv --add-label 'category: objdetect'   # 0.92
# gh issue edit 29654 -R opencv/opencv --add-label 'category: imgproc'   # 0.92
# gh pr edit 29889 -R opencv/opencv --add-label 'category: build/install'   # 0.92
# gh pr edit 30478 -R opencv/opencv --add-label bug   # 0.92
# gh issue edit 30563 -R opencv/opencv --add-label 'category: core'   # 0.92
# gh issue edit 30621 -R opencv/opencv --add-label 'category: objdetect'   # 0.92
# gh issue edit 30697 -R opencv/opencv --add-label 'category: core'   # 0.92
# gh pr edit 30878 -R opencv/opencv --add-label bug   # 0.92
# gh pr edit 30887 -R opencv/opencv --add-label 'category: documentation'   # 0.92
# gh issue edit 19307 -R opencv/opencv --add-label feature   # 0.91
# gh issue edit 22379 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.91
# gh issue edit 25418 -R opencv/opencv --add-label 'category: python bindings'   # 0.91
# gh pr edit 29986 -R opencv/opencv --add-label test   # 0.91
# gh issue edit 30783 -R opencv/opencv --add-label 'category: python bindings'   # 0.91
# gh issue edit 27176 -R opencv/opencv --add-label 'category: dnn'   # 0.90
# gh issue edit 30635 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.90
# gh pr edit 30796 -R opencv/opencv --add-label bug   # 0.90
# gh issue edit 30868 -R opencv/opencv --add-label 'category: flann'   # 0.90
# gh pr edit 30869 -R opencv/opencv --add-label bug   # 0.90
# gh pr edit 30481 -R opencv/opencv --add-label 'category: calib3d'   # 0.89
# gh issue edit 30495 -R opencv/opencv --add-label 'category: core'   # 0.89
# gh issue edit 30580 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.89
# gh issue edit 30603 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.89
# gh issue edit 30683 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.89
# gh issue edit 30713 -R opencv/opencv --add-label 'category: core'   # 0.89
# gh issue edit 30833 -R opencv/opencv --add-label 'category: imgproc'   # 0.89
# gh issue edit 30857 -R opencv/opencv --add-label 'category: video'   # 0.89
# gh issue edit 8257 -R opencv/opencv --add-label 'category: ml'   # 0.88
# gh issue edit 13996 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.88
# gh issue edit 23384 -R opencv/opencv --add-label 'category: build/install'   # 0.88
# gh pr edit 28942 -R opencv/opencv --add-label bug   # 0.88
# gh issue edit 29238 -R opencv/opencv --add-label 'category: core'   # 0.88
# gh issue edit 29821 -R opencv/opencv --add-label 'category: video'   # 0.88
# gh pr edit 29951 -R opencv/opencv --add-label test   # 0.88
# gh pr edit 30482 -R opencv/opencv --add-label 'category: calib3d'   # 0.88
# gh pr edit 29063 -R opencv/opencv --add-label feature   # 0.87
# gh issue edit 30376 -R opencv/opencv --add-label 'category: photo'   # 0.87
# gh pr edit 30378 -R opencv/opencv --add-label 'category: photo'   # 0.87
# gh pr edit 30472 -R opencv/opencv --add-label 'category: photo'   # 0.87
# gh issue edit 30502 -R opencv/opencv --add-label bug   # 0.87
# gh pr edit 30613 -R opencv/opencv --add-label bug   # 0.87
# gh issue edit 30833 -R opencv/opencv --add-label 'category: photo'   # 0.87
# gh issue edit 30861 -R opencv/opencv --add-label 'category: photo'   # 0.87
# gh issue edit 30862 -R opencv/opencv --add-label 'category: photo'   # 0.87
# gh pr edit 30863 -R opencv/opencv --add-label 'category: photo'   # 0.87
# gh pr edit 30864 -R opencv/opencv --add-label 'category: photo'   # 0.87
# gh issue edit 6092 -R opencv/opencv --add-label 'category: build/install'   # 0.86
# gh issue edit 7118 -R opencv/opencv --add-label 'category: calib3d'   # 0.86
# gh issue edit 12969 -R opencv/opencv --add-label 'category: imgproc'   # 0.86
# gh issue edit 17348 -R opencv/opencv --add-label 'category: calib3d'   # 0.86
# gh issue edit 17763 -R opencv/opencv --add-label 'category: build/install'   # 0.86
# gh issue edit 18623 -R opencv/opencv --add-label 'category: calib3d'   # 0.86
# gh issue edit 19159 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 19307 -R opencv/opencv --add-label 'category: imgproc'   # 0.86
# gh issue edit 19999 -R opencv/opencv --add-label 'category: videoio'   # 0.86
# gh issue edit 20093 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 20612 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 21396 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 21473 -R opencv/opencv --add-label 'category: imgproc'   # 0.86
# gh issue edit 21671 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 21880 -R opencv/opencv --add-label 'category: javascript (js)'   # 0.86
# gh issue edit 21912 -R opencv/opencv --add-label 'category: imgproc'   # 0.86
# gh issue edit 22039 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 22180 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 22201 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.86
# gh issue edit 22240 -R opencv/opencv --add-label 'category: calib3d'   # 0.86
# gh issue edit 22486 -R opencv/opencv --add-label 'category: imgproc'   # 0.86
# gh issue edit 22658 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 22711 -R opencv/opencv --add-label 'category: calib3d'   # 0.86
# gh issue edit 22812 -R opencv/opencv --add-label 'category: imgproc'   # 0.86
# gh issue edit 23058 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 23273 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 23297 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 23298 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 23324 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.86
# gh issue edit 23693 -R opencv/opencv --add-label 'category: imgproc'   # 0.86
# gh issue edit 24048 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 24050 -R opencv/opencv --add-label 'category: calib3d'   # 0.86
# gh issue edit 24190 -R opencv/opencv --add-label 'category: build/install'   # 0.86
# gh issue edit 24321 -R opencv/opencv --add-label 'category: videoio'   # 0.86
# gh issue edit 24413 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 24541 -R opencv/opencv --add-label 'category: core'   # 0.86
# gh issue edit 25032 -R opencv/opencv --add-label 'category: imgproc'   # 0.86
# gh issue edit 25233 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 25446 -R opencv/opencv --add-label 'category: build/install'   # 0.86
# gh issue edit 25446 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.86
# gh issue edit 25676 -R opencv/opencv --add-label 'category: build/install'   # 0.86
# gh issue edit 25740 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 26393 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 26781 -R opencv/opencv --add-label 'category: features2d'   # 0.86
# gh issue edit 26962 -R opencv/opencv --add-label 'category: imgproc'   # 0.86
# gh issue edit 27143 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.86
# gh issue edit 27198 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 27966 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 27967 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh pr edit 28623 -R opencv/opencv --add-label bug   # 0.86
# gh issue edit 28960 -R opencv/opencv --add-label 'category: videoio'   # 0.86
# gh issue edit 29313 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh pr edit 29319 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh pr edit 29555 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh pr edit 30378 -R opencv/opencv --add-label bug   # 0.86
# gh issue edit 30535 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh pr edit 30555 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 30589 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 30651 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 30806 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 30834 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh issue edit 30865 -R opencv/opencv --add-label 'category: dnn'   # 0.86
# gh pr edit 30875 -R opencv/opencv --add-label 'category: calib3d'   # 0.86
# gh issue edit 8067 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh issue edit 13729 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh issue edit 24313 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh issue edit 25001 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh issue edit 25012 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh issue edit 28599 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh pr edit 28602 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh pr edit 28623 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh pr edit 28736 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh pr edit 29302 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh pr edit 29347 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh pr edit 29349 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh pr edit 29951 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh pr edit 29952 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh pr edit 29975 -R opencv/opencv --add-label test   # 0.85
# gh issue edit 30215 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh issue edit 30278 -R opencv/opencv --add-label 'category: core'   # 0.85
# gh issue edit 30359 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh pr edit 30460 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh issue edit 30528 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh issue edit 30594 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh pr edit 30604 -R opencv/opencv --add-label bug   # 0.85
# gh issue edit 30630 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh issue edit 30649 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh pr edit 30658 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh issue edit 30733 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh pr edit 30817 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh pr edit 30825 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh issue edit 30830 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh issue edit 30848 -R opencv/opencv --add-label 'category: imgproc'   # 0.85
# gh issue edit 30862 -R opencv/opencv --add-label bug   # 0.85
# gh pr edit 28736 -R opencv/opencv --add-label bug   # 0.84
# gh pr edit 30058 -R opencv/opencv --add-label test   # 0.84
# gh issue edit 7770 -R opencv/opencv --add-label bug   # 0.83
# gh issue edit 13541 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.83
# gh issue edit 26118 -R opencv/opencv --add-label 'category: imgproc'   # 0.83
# gh issue edit 29768 -R opencv/opencv --add-label feature   # 0.83
# gh pr edit 29952 -R opencv/opencv --add-label test   # 0.83
# gh issue edit 30664 -R opencv/opencv --add-label 'category: core'   # 0.83
# gh issue edit 30766 -R opencv/opencv --add-label 'category: core'   # 0.83
# gh issue edit 30819 -R opencv/opencv --add-label 'category: imgproc'   # 0.83
# gh issue edit 8650 -R opencv/opencv --add-label bug   # 0.82
# gh issue edit 24924 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.82
# gh issue edit 27645 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.82
# gh pr edit 28872 -R opencv/opencv --add-label bug   # 0.82
# gh pr edit 30279 -R opencv/opencv --add-label bug   # 0.82
# gh issue edit 30376 -R opencv/opencv --add-label bug   # 0.82
# gh issue edit 30766 -R opencv/opencv --add-label bug   # 0.82
# gh issue edit 14703 -R opencv/opencv --add-label bug   # 0.81
# gh issue edit 22098 -R opencv/opencv --add-label 'category: build/install'   # 0.81
# gh issue edit 27625 -R opencv/opencv --add-label 'category: calib3d'   # 0.81
# gh pr edit 30874 -R opencv/opencv --add-label optimization   # 0.81
# gh issue edit 16951 -R opencv/opencv --add-label bug   # 0.80
# gh issue edit 23297 -R opencv/opencv --add-label 'category: dnn (onnx)'   # 0.80
# gh pr edit 29537 -R opencv/opencv --add-label cleanup   # 0.80
# gh issue edit 29654 -R opencv/opencv --add-label feature   # 0.80
# gh issue edit 29781 -R opencv/opencv --add-label 'category: video'   # 0.80
# gh pr edit 30889 -R opencv/opencv --add-label bug   # 0.80
# gh issue edit 10075 -R opencv/opencv --add-label optimization   # 0.79
# gh issue edit 15675 -R opencv/opencv --add-label feature   # 0.79
# gh pr edit 27151 -R opencv/opencv --add-label bug   # 0.79
# gh pr edit 29992 -R opencv/opencv --add-label 'category: documentation'   # 0.79
# gh issue edit 30787 -R opencv/opencv --add-label bug   # 0.79
# gh issue edit 6496 -R opencv/opencv --add-label 'category: build/install'   # 0.78
# gh issue edit 10993 -R opencv/opencv --add-label bug   # 0.78
# gh issue edit 12369 -R opencv/opencv --add-label 'category: build/install'   # 0.78
# gh issue edit 21720 -R opencv/opencv --add-label 'category: imgproc'   # 0.78
# gh issue edit 23385 -R opencv/opencv --add-label 'category: build/install'   # 0.78
# gh issue edit 23537 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.78
# gh issue edit 24637 -R opencv/opencv --add-label 'category: videoio'   # 0.78
# gh issue edit 28962 -R opencv/opencv --add-label 'category: photo'   # 0.78
# gh pr edit 30822 -R opencv/opencv --add-label 'category: core'   # 0.78
# gh issue edit 7245 -R opencv/opencv --add-label bug   # 0.77
# gh issue edit 16587 -R opencv/opencv --add-label bug   # 0.77
# gh issue edit 19999 -R opencv/opencv --add-label bug   # 0.77
# gh issue edit 30733 -R opencv/opencv --add-label bug   # 0.77
# gh issue edit 11915 -R opencv/opencv --add-label bug   # 0.76
# gh issue edit 23720 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.76
# gh issue edit 27215 -R opencv/opencv --add-label bug   # 0.76
# gh issue edit 15224 -R opencv/opencv --add-label bug   # 0.75
# gh issue edit 16298 -R opencv/opencv --add-label 'category: core'   # 0.75
# gh issue edit 17950 -R opencv/opencv --add-label bug   # 0.75
# gh issue edit 18100 -R opencv/opencv --add-label bug   # 0.75
# gh issue edit 21544 -R opencv/opencv --add-label 'category: imgproc'   # 0.75
# gh issue edit 26702 -R opencv/opencv --add-label 'category: imgproc'   # 0.75
# gh issue edit 28940 -R opencv/opencv --add-label 'category: imgproc'   # 0.75
# gh issue edit 29002 -R opencv/opencv --add-label 'category: build/install'   # 0.75
# gh issue edit 29234 -R opencv/opencv --add-label 'category: core'   # 0.75
# gh pr edit 30179 -R opencv/opencv --add-label bug   # 0.75
# gh pr edit 30179 -R opencv/opencv --add-label 'category: video'   # 0.75
# gh issue edit 30605 -R opencv/opencv --add-label 'category: dnn'   # 0.75
# gh pr edit 30613 -R opencv/opencv --add-label 'category: core'   # 0.75
# gh issue edit 30794 -R opencv/opencv --add-label bug   # 0.75
# gh issue edit 7938 -R opencv/opencv --add-label bug   # 0.74
# gh issue edit 21930 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.74
# gh issue edit 23397 -R opencv/opencv --add-label feature   # 0.74
# gh issue edit 29781 -R opencv/opencv --add-label bug   # 0.74
# gh pr edit 30472 -R opencv/opencv --add-label optimization   # 0.74
# gh issue edit 30813 -R opencv/opencv --add-label optimization   # 0.74
# gh pr edit 30825 -R opencv/opencv --add-label bug   # 0.74
# gh issue edit 30882 -R opencv/opencv --add-label optimization   # 0.74
# gh issue edit 5112 -R opencv/opencv --add-label bug   # 0.73
# gh issue edit 15146 -R opencv/opencv --add-label bug   # 0.73
# gh issue edit 16252 -R opencv/opencv --add-label bug   # 0.73
# gh issue edit 17767 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.73
# gh issue edit 20985 -R opencv/opencv --add-label bug   # 0.73
# gh pr edit 30786 -R opencv/opencv --add-label bug   # 0.73
# gh pr edit 30844 -R opencv/opencv --add-label test   # 0.73
# gh issue edit 20214 -R opencv/opencv --add-label feature   # 0.72
# gh pr edit 20389 -R opencv/opencv --add-label 'category: build/install'   # 0.72
# gh issue edit 21155 -R opencv/opencv --add-label 'category: videoio'   # 0.72
# gh issue edit 22235 -R opencv/opencv --add-label bug   # 0.72
# gh issue edit 22252 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.72
# gh issue edit 23298 -R opencv/opencv --add-label 'category: dnn (onnx)'   # 0.72
# gh issue edit 23873 -R opencv/opencv --add-label bug   # 0.72
# gh issue edit 6303 -R opencv/opencv --add-label 'category: core'   # 0.71
# gh issue edit 7479 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.71
# gh issue edit 7519 -R opencv/opencv --add-label bug   # 0.71
# gh issue edit 8223 -R opencv/opencv --add-label 'category: calib3d'   # 0.71
# gh issue edit 8740 -R opencv/opencv --add-label 'category: core'   # 0.71
# gh issue edit 9219 -R opencv/opencv --add-label 'category: ml'   # 0.71
# gh issue edit 9224 -R opencv/opencv --add-label 'category: objdetect'   # 0.71
# gh issue edit 9640 -R opencv/opencv --add-label bug   # 0.71
# gh issue edit 9885 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.71
# gh issue edit 10101 -R opencv/opencv --add-label 'category: ocl'   # 0.71
# gh issue edit 11479 -R opencv/opencv --add-label 'category: calib3d'   # 0.71
# gh issue edit 12276 -R opencv/opencv --add-label 'category: core'   # 0.71
# gh issue edit 13170 -R opencv/opencv --add-label 'category: flann'   # 0.71
# gh issue edit 13470 -R opencv/opencv --add-label 'category: core'   # 0.71
# gh issue edit 13744 -R opencv/opencv --add-label 'category: core'   # 0.71
# gh issue edit 16843 -R opencv/opencv --add-label 'category: imgproc'   # 0.71
# gh issue edit 17826 -R opencv/opencv --add-label 'category: calib3d'   # 0.71
# gh issue edit 18046 -R opencv/opencv --add-label bug   # 0.71
# gh issue edit 18797 -R opencv/opencv --add-label 'category: imgproc'   # 0.71
# gh issue edit 18934 -R opencv/opencv --add-label bug   # 0.71
# gh issue edit 19150 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.71
# gh issue edit 20193 -R opencv/opencv --add-label 'category: videoio'   # 0.71
# gh issue edit 21402 -R opencv/opencv --add-label 'category: stitching'   # 0.71
# gh issue edit 21616 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.71
# gh issue edit 21711 -R opencv/opencv --add-label 'category: build/install'   # 0.71
# gh issue edit 21729 -R opencv/opencv --add-label 'category: imgproc'   # 0.71
# gh issue edit 21774 -R opencv/opencv --add-label 'category: build/install'   # 0.71
# gh issue edit 21814 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.71
# gh issue edit 21881 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.71
# gh issue edit 22055 -R opencv/opencv --add-label 'category: videoio'   # 0.71
# gh issue edit 22120 -R opencv/opencv --add-label feature   # 0.71
# gh issue edit 22342 -R opencv/opencv --add-label 'category: dnn'   # 0.71
# gh issue edit 22620 -R opencv/opencv --add-label 'category: calib3d'   # 0.71
# gh issue edit 22745 -R opencv/opencv --add-label 'category: stitching'   # 0.71
# gh issue edit 23316 -R opencv/opencv --add-label 'category: dnn'   # 0.71
# gh issue edit 23330 -R opencv/opencv --add-label 'category: dnn'   # 0.71
# gh issue edit 23420 -R opencv/opencv --add-label 'category: core'   # 0.71
# gh issue edit 23727 -R opencv/opencv --add-label 'category: calib3d'   # 0.71
# gh issue edit 24183 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.71
# gh issue edit 24208 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.71
# gh issue edit 24722 -R opencv/opencv --add-label 'category: stitching'   # 0.71
# gh issue edit 25114 -R opencv/opencv --add-label 'category: photo'   # 0.71
# gh issue edit 25186 -R opencv/opencv --add-label 'category: build/install'   # 0.71
# gh issue edit 26496 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.71
# gh issue edit 26674 -R opencv/opencv --add-label 'category: dnn'   # 0.71
# gh issue edit 26686 -R opencv/opencv --add-label 'category: objdetect'   # 0.71
# gh issue edit 27215 -R opencv/opencv --add-label 'category: imgproc'   # 0.71
# gh issue edit 28325 -R opencv/opencv --add-label 'category: build/install'   # 0.71
# gh issue edit 28339 -R opencv/opencv --add-label 'category: dnn'   # 0.71
# gh issue edit 28339 -R opencv/opencv --add-label 'category: dnn (onnx)'   # 0.71
# gh pr edit 28492 -R opencv/opencv --add-label bug   # 0.71
# gh issue edit 28594 -R opencv/opencv --add-label 'category: videoio'   # 0.71
# gh pr edit 29319 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.71
# gh pr edit 30047 -R opencv/opencv --add-label bug   # 0.71
# gh pr edit 30229 -R opencv/opencv --add-label bug   # 0.71
# gh pr edit 30229 -R opencv/opencv --add-label 'category: calib3d'   # 0.71
# gh pr edit 30485 -R opencv/opencv --add-label bug   # 0.71
# gh issue edit 30487 -R opencv/opencv --add-label 'category: dnn'   # 0.71
# gh issue edit 30588 -R opencv/opencv --add-label 'category: objdetect'   # 0.71
# gh issue edit 30589 -R opencv/opencv --add-label 'category: dnn (onnx)'   # 0.71
# gh issue edit 30657 -R opencv/opencv --add-label 'category: build/install'   # 0.71
# gh pr edit 30814 -R opencv/opencv --add-label optimization   # 0.71
# gh issue edit 16383 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.70
# gh issue edit 17975 -R opencv/opencv --add-label bug   # 0.70
# gh issue edit 23706 -R opencv/opencv --add-label 'category: imgproc'   # 0.70
# gh issue edit 25798 -R opencv/opencv --add-label bug   # 0.70
# gh pr edit 30016 -R opencv/opencv --add-label 'category: python bindings'   # 0.70
# gh pr edit 30016 -R opencv/opencv --add-label 'category: build/install'   # 0.70
# gh pr edit 30838 -R opencv/opencv --add-label bug   # 0.70
# gh issue edit 8549 -R opencv/opencv --add-label bug   # 0.69
# gh issue edit 8584 -R opencv/opencv --add-label bug   # 0.69
# gh issue edit 11003 -R opencv/opencv --add-label 'category: core'   # 0.69
# gh issue edit 11717 -R opencv/opencv --add-label bug   # 0.69
# gh issue edit 13170 -R opencv/opencv --add-label bug   # 0.69
# gh issue edit 14023 -R opencv/opencv --add-label bug   # 0.69
# gh issue edit 15643 -R opencv/opencv --add-label bug   # 0.69
# gh issue edit 16429 -R opencv/opencv --add-label bug   # 0.69
# gh issue edit 22314 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.69
# gh issue edit 23066 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.69
# gh issue edit 25303 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.69
# gh issue edit 26064 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.69
# gh issue edit 28613 -R opencv/opencv --add-label 'category: imgproc'   # 0.69
# gh pr edit 29199 -R opencv/opencv --add-label bug   # 0.69
# gh pr edit 29233 -R opencv/opencv --add-label bug   # 0.69
# gh pr edit 30465 -R opencv/opencv --add-label 'category: imgproc'   # 0.69
# gh pr edit 30623 -R opencv/opencv --add-label bug   # 0.69
# gh pr edit 30864 -R opencv/opencv --add-label bug   # 0.69
# gh issue edit 21657 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.68
# gh pr edit 28645 -R opencv/opencv --add-label feature   # 0.68
# gh issue edit 30359 -R opencv/opencv --add-label feature   # 0.68
# gh issue edit 8223 -R opencv/opencv --add-label bug   # 0.67
# gh issue edit 9764 -R opencv/opencv --add-label bug   # 0.67
# gh issue edit 11022 -R opencv/opencv --add-label 'category: core'   # 0.67
# gh issue edit 15410 -R opencv/opencv --add-label bug   # 0.67
# gh issue edit 15910 -R opencv/opencv --add-label bug   # 0.67
# gh issue edit 19907 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.67
# gh issue edit 21983 -R opencv/opencv --add-label bug   # 0.67
# gh issue edit 26888 -R opencv/opencv --add-label feature   # 0.67
# gh pr edit 28994 -R opencv/opencv --add-label 'category: python bindings'   # 0.67
# gh pr edit 29136 -R opencv/opencv --add-label 'category: ml'   # 0.67
# gh pr edit 29527 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.67
# gh pr edit 29810 -R opencv/opencv --add-label feature   # 0.67
# gh issue edit 30361 -R opencv/opencv --add-label 'category: imgproc'   # 0.67
# gh pr edit 30485 -R opencv/opencv --add-label 'category: calib3d'   # 0.67
# gh issue edit 30557 -R opencv/opencv --add-label 'category: core'   # 0.67
# gh pr edit 30568 -R opencv/opencv --add-label feature   # 0.67
# gh issue edit 30574 -R opencv/opencv --add-label 'category: core'   # 0.67
# gh issue edit 30744 -R opencv/opencv --add-label 'category: calib3d'   # 0.67
# gh issue edit 30850 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.67
# gh issue edit 30857 -R opencv/opencv --add-label bug   # 0.67
# gh issue edit 30882 -R opencv/opencv --add-label 'category: core'   # 0.67
# gh issue edit 11621 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.66
# gh issue edit 14420 -R opencv/opencv --add-label bug   # 0.66
# gh issue edit 17488 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.66
# gh issue edit 22351 -R opencv/opencv --add-label bug   # 0.66
# gh issue edit 23490 -R opencv/opencv --add-label bug   # 0.66
# gh issue edit 26697 -R opencv/opencv --add-label bug   # 0.66
# gh pr edit 28991 -R opencv/opencv --add-label feature   # 0.66
# gh pr edit 29959 -R opencv/opencv --add-label bug   # 0.66
# gh issue edit 8331 -R opencv/opencv --add-label feature   # 0.65
# gh issue edit 11082 -R opencv/opencv --add-label bug   # 0.65
# gh issue edit 13790 -R opencv/opencv --add-label bug   # 0.65
# gh issue edit 21729 -R opencv/opencv --add-label bug   # 0.65
# gh issue edit 24638 -R opencv/opencv --add-label bug   # 0.65
# gh issue edit 7250 -R opencv/opencv --add-label bug   # 0.64
# gh issue edit 10920 -R opencv/opencv --add-label bug   # 0.64
# gh issue edit 13459 -R opencv/opencv --add-label feature   # 0.64
# gh issue edit 15134 -R opencv/opencv --add-label bug   # 0.64
# gh issue edit 15787 -R opencv/opencv --add-label bug   # 0.64
# gh issue edit 21774 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.64
# gh issue edit 22273 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.64
# gh pr edit 25569 -R opencv/opencv --add-label bug   # 0.64
# gh pr edit 27646 -R opencv/opencv --add-label bug   # 0.64
# gh pr edit 30875 -R opencv/opencv --add-label bug   # 0.64
# gh issue edit 9643 -R opencv/opencv --add-label feature   # 0.63
# gh issue edit 10090 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.63
# gh issue edit 11533 -R opencv/opencv --add-label bug   # 0.63
# gh issue edit 12212 -R opencv/opencv --add-label bug   # 0.63
# gh issue edit 12426 -R opencv/opencv --add-label bug   # 0.63
# gh issue edit 13077 -R opencv/opencv --add-label feature   # 0.63
# gh issue edit 16262 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.63
# gh issue edit 21010 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.63
# gh issue edit 21633 -R opencv/opencv --add-label bug   # 0.63
# gh issue edit 21838 -R opencv/opencv --add-label bug   # 0.63
# gh issue edit 23385 -R opencv/opencv --add-label bug   # 0.63
# gh issue edit 25929 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.63
# gh issue edit 30459 -R opencv/opencv --add-label 'category: imgproc'   # 0.63
# gh issue edit 30502 -R opencv/opencv --add-label 'category: dnn'   # 0.63
# gh pr edit 30845 -R opencv/opencv --add-label feature   # 0.63
# gh issue edit 9809 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.62
# gh issue edit 13996 -R opencv/opencv --add-label 'category: build/install'   # 0.62
# gh issue edit 15647 -R opencv/opencv --add-label feature   # 0.62
# gh issue edit 17656 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.62
# gh issue edit 18565 -R opencv/opencv --add-label bug   # 0.62
# gh issue edit 20256 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.62
# gh issue edit 21457 -R opencv/opencv --add-label 'category: imgproc'   # 0.62
# gh issue edit 21868 -R opencv/opencv --add-label 'category: core'   # 0.62
# gh issue edit 23593 -R opencv/opencv --add-label 'category: build/install'   # 0.62
# gh issue edit 26074 -R opencv/opencv --add-label 'category: imgproc'   # 0.62
# gh issue edit 26085 -R opencv/opencv --add-label 'category: dnn'   # 0.62
# gh issue edit 26961 -R opencv/opencv --add-label 'category: imgproc'   # 0.62
# gh issue edit 28478 -R opencv/opencv --add-label 'category: videoio'   # 0.62
# gh pr edit 29135 -R opencv/opencv --add-label 'category: build/install'   # 0.62
# gh pr edit 29135 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.62
# gh issue edit 29443 -R opencv/opencv --add-label 'category: core'   # 0.62
# gh pr edit 29967 -R opencv/opencv --add-label 'category: core'   # 0.62
# gh issue edit 30384 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.62
# gh pr edit 30447 -R opencv/opencv --add-label 'category: core'   # 0.62
# gh pr edit 30521 -R opencv/opencv --add-label feature   # 0.62
# gh pr edit 30609 -R opencv/opencv --add-label 'category: dnn'   # 0.62
# gh issue edit 30792 -R opencv/opencv --add-label 'category: swift/objc bindings'   # 0.62
# gh issue edit 11149 -R opencv/opencv --add-label bug   # 0.61
# gh issue edit 17991 -R opencv/opencv --add-label bug   # 0.61
# gh issue edit 21352 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.61
# gh issue edit 23360 -R opencv/opencv --add-label bug   # 0.61
# gh issue edit 26860 -R opencv/opencv --add-label feature   # 0.61
# gh issue edit 30865 -R opencv/opencv --add-label bug   # 0.61
# gh issue edit 9639 -R opencv/opencv --add-label bug   # 0.60
# gh issue edit 10325 -R opencv/opencv --add-label bug   # 0.60
# gh issue edit 13968 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.60
# gh issue edit 15109 -R opencv/opencv --add-label bug   # 0.60
# gh issue edit 20378 -R opencv/opencv --add-label bug   # 0.60
# gh issue edit 22049 -R opencv/opencv --add-label bug   # 0.60
# gh issue edit 22587 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.60
# gh issue edit 23741 -R opencv/opencv --add-label bug   # 0.60
# gh issue edit 27556 -R opencv/opencv --add-label bug   # 0.60
# gh pr edit 30722 -R opencv/opencv --add-label 'category: documentation'   # 0.60
# gh pr edit 30817 -R opencv/opencv --add-label optimization   # 0.60
# gh issue edit 5931 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.59
# gh issue edit 6688 -R opencv/opencv --add-label bug   # 0.59
# gh issue edit 7479 -R opencv/opencv --add-label bug   # 0.59
# gh issue edit 8802 -R opencv/opencv --add-label bug   # 0.59
# gh issue edit 16757 -R opencv/opencv --add-label bug   # 0.59
# gh issue edit 16957 -R opencv/opencv --add-label bug   # 0.59
# gh issue edit 23858 -R opencv/opencv --add-label bug   # 0.59
# gh pr edit 29873 -R opencv/opencv --add-label bug   # 0.59
# gh pr edit 30146 -R opencv/opencv --add-label 'category: dnn'   # 0.59
# gh issue edit 30630 -R opencv/opencv --add-label bug   # 0.59
# gh issue edit 9953 -R opencv/opencv --add-label bug   # 0.58
# gh issue edit 11861 -R opencv/opencv --add-label bug   # 0.58
# gh issue edit 13108 -R opencv/opencv --add-label bug   # 0.58
# gh issue edit 14550 -R opencv/opencv --add-label bug   # 0.58
# gh issue edit 16843 -R opencv/opencv --add-label bug   # 0.58
# gh issue edit 17911 -R opencv/opencv --add-label bug   # 0.58
# gh issue edit 18884 -R opencv/opencv --add-label bug   # 0.58
# gh issue edit 23194 -R opencv/opencv --add-label feature   # 0.58
# gh issue edit 24264 -R opencv/opencv --add-label bug   # 0.58
# gh pr edit 30228 -R opencv/opencv --add-label 'category: python bindings'   # 0.58
# gh issue edit 30821 -R opencv/opencv --add-label bug   # 0.58
# gh pr edit 30863 -R opencv/opencv --add-label bug   # 0.58
# gh issue edit 5626 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh issue edit 5814 -R opencv/opencv --add-label 'category: imgproc'   # 0.57
# gh issue edit 7245 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.57
# gh issue edit 7250 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.57
# gh issue edit 7525 -R opencv/opencv --add-label 'category: core'   # 0.57
# gh issue edit 7770 -R opencv/opencv --add-label 'category: objdetect'   # 0.57
# gh issue edit 8300 -R opencv/opencv --add-label bug   # 0.57
# gh issue edit 8584 -R opencv/opencv --add-label 'category: stitching'   # 0.57
# gh issue edit 8689 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh issue edit 9205 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh issue edit 9843 -R opencv/opencv --add-label bug   # 0.57
# gh issue edit 10555 -R opencv/opencv --add-label bug   # 0.57
# gh issue edit 11003 -R opencv/opencv --add-label feature   # 0.57
# gh issue edit 11832 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.57
# gh issue edit 12873 -R opencv/opencv --add-label 'category: calib3d'   # 0.57
# gh issue edit 13077 -R opencv/opencv --add-label 'category: calib3d'   # 0.57
# gh issue edit 13820 -R opencv/opencv --add-label 'category: core'   # 0.57
# gh issue edit 14819 -R opencv/opencv --add-label 'category: ocl'   # 0.57
# gh issue edit 14992 -R opencv/opencv --add-label 'category: stitching'   # 0.57
# gh issue edit 15321 -R opencv/opencv --add-label bug   # 0.57
# gh issue edit 15571 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh issue edit 15897 -R opencv/opencv --add-label feature   # 0.57
# gh issue edit 15914 -R opencv/opencv --add-label 'category: videoio'   # 0.57
# gh issue edit 16730 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.57
# gh issue edit 16939 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh issue edit 17495 -R opencv/opencv --add-label 'category: objdetect'   # 0.57
# gh issue edit 18575 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh issue edit 19930 -R opencv/opencv --add-label bug   # 0.57
# gh issue edit 20042 -R opencv/opencv --add-label 'category: core'   # 0.57
# gh issue edit 20403 -R opencv/opencv --add-label bug   # 0.57
# gh issue edit 20481 -R opencv/opencv --add-label feature   # 0.57
# gh issue edit 21184 -R opencv/opencv --add-label 'category: calib3d'   # 0.57
# gh issue edit 21434 -R opencv/opencv --add-label 'category: videoio'   # 0.57
# gh issue edit 21472 -R opencv/opencv --add-label 'category: imgproc'   # 0.57
# gh issue edit 21774 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.57
# gh issue edit 21880 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh issue edit 21930 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.57
# gh issue edit 22075 -R opencv/opencv --add-label 'category: imgproc'   # 0.57
# gh issue edit 22087 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh issue edit 22098 -R opencv/opencv --add-label bug   # 0.57
# gh issue edit 22120 -R opencv/opencv --add-label 'category: imgproc'   # 0.57
# gh issue edit 22134 -R opencv/opencv --add-label 'category: dnn'   # 0.57
# gh issue edit 22375 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh issue edit 22392 -R opencv/opencv --add-label 'category: objdetect'   # 0.57
# gh issue edit 22550 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.57
# gh issue edit 22579 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh issue edit 22616 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh issue edit 22636 -R opencv/opencv --add-label 'category: dnn'   # 0.57
# gh issue edit 22680 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.57
# gh issue edit 22777 -R opencv/opencv --add-label 'category: imgproc'   # 0.57
# gh issue edit 22984 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh issue edit 23024 -R opencv/opencv --add-label 'category: imgproc'   # 0.57
# gh issue edit 23163 -R opencv/opencv --add-label 'category: documentation'   # 0.57
# gh issue edit 23201 -R opencv/opencv --add-label 'category: core'   # 0.57
# gh issue edit 23312 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.57
# gh issue edit 23314 -R opencv/opencv --add-label 'category: dnn (onnx)'   # 0.57
# gh issue edit 23368 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.57
# gh issue edit 23369 -R opencv/opencv --add-label 'category: core'   # 0.57
# gh issue edit 23421 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.57
# gh issue edit 23426 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh issue edit 23552 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh issue edit 23609 -R opencv/opencv --add-label bug   # 0.57
# gh issue edit 23898 -R opencv/opencv --add-label 'category: imgproc'   # 0.57
# gh issue edit 23906 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.57
# gh issue edit 24033 -R opencv/opencv --add-label 'category: videoio'   # 0.57
# gh issue edit 24088 -R opencv/opencv --add-label 'category: videoio'   # 0.57
# gh issue edit 24091 -R opencv/opencv --add-label 'category: imgproc'   # 0.57
# gh issue edit 24264 -R opencv/opencv --add-label 'category: videoio'   # 0.57
# gh issue edit 24518 -R opencv/opencv --add-label bug   # 0.57
# gh issue edit 24638 -R opencv/opencv --add-label 'category: imgproc'   # 0.57
# gh issue edit 24978 -R opencv/opencv --add-label 'category: imgproc'   # 0.57
# gh issue edit 25121 -R opencv/opencv --add-label 'category: videoio'   # 0.57
# gh issue edit 25222 -R opencv/opencv --add-label 'category: dnn'   # 0.57
# gh issue edit 25251 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.57
# gh issue edit 25290 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.57
# gh issue edit 25315 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh issue edit 25797 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh pr edit 25869 -R opencv/opencv --add-label 'category: core'   # 0.57
# gh issue edit 25871 -R opencv/opencv --add-label 'category: ocl'   # 0.57
# gh issue edit 25993 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh issue edit 26108 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh issue edit 26438 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh issue edit 26494 -R opencv/opencv --add-label 'category: documentation'   # 0.57
# gh issue edit 26783 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh issue edit 26860 -R opencv/opencv --add-label 'category: imgproc'   # 0.57
# gh issue edit 26896 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.57
# gh issue edit 27955 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.57
# gh issue edit 28391 -R opencv/opencv --add-label 'category: documentation'   # 0.57
# gh pr edit 28433 -R opencv/opencv --add-label bug   # 0.57
# gh issue edit 28462 -R opencv/opencv --add-label 'category: calib3d'   # 0.57
# gh pr edit 28492 -R opencv/opencv --add-label 'category: core'   # 0.57
# gh issue edit 28549 -R opencv/opencv --add-label 'category: documentation'   # 0.57
# gh issue edit 28683 -R opencv/opencv --add-label bug   # 0.57
# gh issue edit 28777 -R opencv/opencv --add-label 'category: imgproc'   # 0.57
# gh issue edit 28924 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.57
# gh pr edit 28970 -R opencv/opencv --add-label 'category: core'   # 0.57
# gh pr edit 29147 -R opencv/opencv --add-label optimization   # 0.57
# gh issue edit 29212 -R opencv/opencv --add-label 'category: build/install'   # 0.57
# gh pr edit 29302 -R opencv/opencv --add-label feature   # 0.57
# gh issue edit 29311 -R opencv/opencv --add-label 'category: dnn'   # 0.57
# gh issue edit 29845 -R opencv/opencv --add-label 'category: imgproc'   # 0.57
# gh pr edit 29962 -R opencv/opencv --add-label 'category: imgproc'   # 0.57
# gh issue edit 29990 -R opencv/opencv --add-label 'category: core'   # 0.57
# gh pr edit 30146 -R opencv/opencv --add-label feature   # 0.57
# gh pr edit 30177 -R opencv/opencv --add-label 'category: videoio'   # 0.57
# gh pr edit 30483 -R opencv/opencv --add-label 'category: calib3d'   # 0.57
# gh pr edit 30609 -R opencv/opencv --add-label bug   # 0.57
# gh pr edit 30627 -R opencv/opencv --add-label 'category: dnn'   # 0.57
# gh issue edit 30651 -R opencv/opencv --add-label 'category: core'   # 0.57
# gh issue edit 30734 -R opencv/opencv --add-label 'category: python bindings'   # 0.57
# gh pr edit 30812 -R opencv/opencv --add-label bug   # 0.57
# gh issue edit 30813 -R opencv/opencv --add-label 'category: imgproc'   # 0.57
# gh pr edit 30814 -R opencv/opencv --add-label 'category: core'   # 0.57
# gh issue edit 30821 -R opencv/opencv --add-label 'category: core'   # 0.57
# gh issue edit 9821 -R opencv/opencv --add-label test   # 0.56
# gh issue edit 14988 -R opencv/opencv --add-label bug   # 0.56
# gh issue edit 20024 -R opencv/opencv --add-label bug   # 0.56
# gh issue edit 22132 -R opencv/opencv --add-label 'category: build/install'   # 0.56
# gh issue edit 22734 -R opencv/opencv --add-label 'category: core'   # 0.56
# gh issue edit 23058 -R opencv/opencv --add-label 'category: dnn (onnx)'   # 0.56
# gh issue edit 23428 -R opencv/opencv --add-label 'category: build/install'   # 0.56
# gh issue edit 24135 -R opencv/opencv --add-label 'category: imgproc'   # 0.56
# gh issue edit 24184 -R opencv/opencv --add-label bug   # 0.56
# gh pr edit 24290 -R opencv/opencv --add-label feature   # 0.56
# gh issue edit 24543 -R opencv/opencv --add-label 'category: dnn'   # 0.56
# gh issue edit 26126 -R opencv/opencv --add-label 'category: objdetect'   # 0.56
# gh issue edit 26156 -R opencv/opencv --add-label 'category: dnn (onnx)'   # 0.56
# gh issue edit 28594 -R opencv/opencv --add-label bug   # 0.56
# gh issue edit 29150 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.56
# gh pr edit 29320 -R opencv/opencv --add-label 'category: core'   # 0.56
# gh issue edit 30215 -R opencv/opencv --add-label optimization   # 0.56
# gh pr edit 30228 -R opencv/opencv --add-label bug   # 0.56
# gh issue edit 30361 -R opencv/opencv --add-label feature   # 0.56
# gh pr edit 30788 -R opencv/opencv --add-label bug   # 0.56
# gh issue edit 30834 -R opencv/opencv --add-label 'category: dnn (onnx)'   # 0.56
# gh issue edit 30870 -R opencv/opencv --add-label 'category: features2d'   # 0.56
# gh issue edit 8872 -R opencv/opencv --add-label feature   # 0.55
# gh issue edit 10116 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.55
# gh issue edit 11962 -R opencv/opencv --add-label bug   # 0.55
# gh issue edit 15571 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.55
# gh issue edit 16339 -R opencv/opencv --add-label feature   # 0.55
# gh issue edit 16394 -R opencv/opencv --add-label 'category: videoio'   # 0.55
# gh issue edit 21402 -R opencv/opencv --add-label bug   # 0.55
# gh issue edit 21447 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.55
# gh issue edit 22342 -R opencv/opencv --add-label feature   # 0.55
# gh issue edit 22352 -R opencv/opencv --add-label bug   # 0.55
# gh issue edit 22374 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.55
# gh issue edit 22658 -R opencv/opencv --add-label bug   # 0.55
# gh issue edit 23286 -R opencv/opencv --add-label bug   # 0.55
# gh issue edit 29776 -R opencv/opencv --add-label 'category: video'   # 0.55
# gh pr edit 30826 -R opencv/opencv --add-label bug   # 0.55
# gh issue edit 5819 -R opencv/opencv --add-label bug   # 0.54
# gh issue edit 14908 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.54
# gh issue edit 15707 -R opencv/opencv --add-label bug   # 0.54
# gh issue edit 16607 -R opencv/opencv --add-label bug   # 0.54
# gh issue edit 16973 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.54
# gh issue edit 17217 -R opencv/opencv --add-label feature   # 0.54
# gh issue edit 19246 -R opencv/opencv --add-label test   # 0.54
# gh issue edit 19294 -R opencv/opencv --add-label bug   # 0.54
# gh issue edit 20057 -R opencv/opencv --add-label bug   # 0.54
# gh issue edit 20563 -R opencv/opencv --add-label feature   # 0.54
# gh issue edit 22132 -R opencv/opencv --add-label bug   # 0.54
# gh issue edit 22575 -R opencv/opencv --add-label bug   # 0.54
# gh issue edit 23282 -R opencv/opencv --add-label bug   # 0.54
# gh issue edit 24115 -R opencv/opencv --add-label bug   # 0.54
# gh issue edit 29419 -R opencv/opencv --add-label 'category: dnn'   # 0.54
# gh issue edit 30535 -R opencv/opencv --add-label 'category: dnn (onnx)'   # 0.54
# gh issue edit 6065 -R opencv/opencv --add-label bug   # 0.53
# gh issue edit 7249 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.53
# gh issue edit 8689 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.53
# gh issue edit 15769 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.53
# gh issue edit 17997 -R opencv/opencv --add-label feature   # 0.53
# gh issue edit 19918 -R opencv/opencv --add-label optimization   # 0.53
# gh issue edit 21647 -R opencv/opencv --add-label bug   # 0.53
# gh issue edit 22060 -R opencv/opencv --add-label bug   # 0.53
# gh issue edit 22083 -R opencv/opencv --add-label bug   # 0.53
# gh issue edit 22152 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.53
# gh pr edit 29962 -R opencv/opencv --add-label bug   # 0.53
# gh pr edit 30828 -R opencv/opencv --add-label feature   # 0.53
# gh issue edit 11022 -R opencv/opencv --add-label optimization   # 0.52
# gh issue edit 12109 -R opencv/opencv --add-label bug   # 0.52
# gh issue edit 13004 -R opencv/opencv --add-label bug   # 0.52
# gh issue edit 13567 -R opencv/opencv --add-label bug   # 0.52
# gh issue edit 13729 -R opencv/opencv --add-label bug   # 0.52
# gh issue edit 14884 -R opencv/opencv --add-label bug   # 0.52
# gh issue edit 14896 -R opencv/opencv --add-label bug   # 0.52
# gh issue edit 17730 -R opencv/opencv --add-label bug   # 0.52
# gh issue edit 20109 -R opencv/opencv --add-label bug   # 0.52
# gh issue edit 22277 -R opencv/opencv --add-label bug   # 0.52
# gh issue edit 23273 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.52
# gh issue edit 24063 -R opencv/opencv --add-label bug   # 0.52
# gh pr edit 24564 -R opencv/opencv --add-label bug   # 0.52
# gh issue edit 26696 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.52
# gh pr edit 29388 -R opencv/opencv --add-label bug   # 0.52
# gh pr edit 29889 -R opencv/opencv --add-label bug   # 0.52
# gh pr edit 29986 -R opencv/opencv --add-label 'category: imgproc'   # 0.52
# gh pr edit 30058 -R opencv/opencv --add-label 'category: imgproc'   # 0.52
# gh pr edit 30481 -R opencv/opencv --add-label bug   # 0.52
# gh issue edit 6092 -R opencv/opencv --add-label bug   # 0.51
# gh issue edit 8740 -R opencv/opencv --add-label bug   # 0.51
# gh issue edit 8817 -R opencv/opencv --add-label bug   # 0.51
# gh issue edit 10010 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.51
# gh issue edit 11099 -R opencv/opencv --add-label bug   # 0.51
# gh issue edit 13816 -R opencv/opencv --add-label bug   # 0.51
# gh issue edit 15143 -R opencv/opencv --add-label bug   # 0.51
# gh issue edit 17395 -R opencv/opencv --add-label bug   # 0.51
# gh issue edit 19369 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.51
# gh issue edit 19787 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.51
# gh issue edit 19922 -R opencv/opencv --add-label bug   # 0.51
# gh issue edit 19938 -R opencv/opencv --add-label feature   # 0.51
# gh issue edit 20418 -R opencv/opencv --add-label bug   # 0.51
# gh issue edit 20726 -R opencv/opencv --add-label bug   # 0.51
# gh issue edit 21747 -R opencv/opencv --add-label bug   # 0.51
# gh issue edit 22157 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.51
# gh issue edit 22581 -R opencv/opencv --add-label bug   # 0.51
# gh issue edit 22582 -R opencv/opencv --add-label bug   # 0.51
# gh issue edit 23164 -R opencv/opencv --add-label bug   # 0.51
# gh issue edit 23792 -R opencv/opencv --add-label bug   # 0.51
# gh issue edit 25889 -R opencv/opencv --add-label bug   # 0.51
# gh issue edit 30649 -R opencv/opencv --add-label feature   # 0.51
# gh pr edit 30884 -R opencv/opencv --add-label bug   # 0.51
# gh issue edit 7270 -R opencv/opencv --add-label 'category: imgproc'   # 0.50
# gh issue edit 7298 -R opencv/opencv --add-label 'category: core'   # 0.50
# gh issue edit 7563 -R opencv/opencv --add-label 'category: core'   # 0.50
# gh issue edit 7862 -R opencv/opencv --add-label 'category: imgproc'   # 0.50
# gh issue edit 10458 -R opencv/opencv --add-label bug   # 0.50
# gh issue edit 12597 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.50
# gh issue edit 14357 -R opencv/opencv --add-label 'category: core'   # 0.50
# gh issue edit 14475 -R opencv/opencv --add-label 'category: core'   # 0.50
# gh issue edit 15210 -R opencv/opencv --add-label bug   # 0.50
# gh issue edit 17591 -R opencv/opencv --add-label feature   # 0.50
# gh issue edit 20198 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.50
# gh issue edit 20548 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.50
# gh issue edit 21037 -R opencv/opencv --add-label 'category: core'   # 0.50
# gh issue edit 21411 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.50
# gh issue edit 21623 -R opencv/opencv --add-label bug   # 0.50
# gh issue edit 21682 -R opencv/opencv --add-label bug   # 0.50
# gh issue edit 21727 -R opencv/opencv --add-label 'category: imgproc'   # 0.50
# gh issue edit 21932 -R opencv/opencv --add-label bug   # 0.50
# gh issue edit 22641 -R opencv/opencv --add-label 'category: python bindings'   # 0.50
# gh issue edit 23592 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.50
# gh issue edit 23735 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.50
# gh issue edit 24543 -R opencv/opencv --add-label 'category: dnn (onnx)'   # 0.50
# gh issue edit 25620 -R opencv/opencv --add-label 'category: imgproc'   # 0.50
# gh issue edit 26329 -R opencv/opencv --add-label 'category: calib3d'   # 0.50
# gh pr edit 28433 -R opencv/opencv --add-label 'category: calib3d'   # 0.50
# gh issue edit 28948 -R opencv/opencv --add-label 'category: core'   # 0.50
# gh pr edit 29285 -R opencv/opencv --add-label 'question (invalid tracker)'   # 0.50
# gh issue edit 29768 -R opencv/opencv --add-label 'category: 3d module'   # 0.50
# gh issue edit 29768 -R opencv/opencv --add-label 'category: imgproc'   # 0.50
# gh issue edit 30067 -R opencv/opencv --add-label 'category: core'   # 0.50
# gh pr edit 30564 -R opencv/opencv --add-label bug   # 0.50
# gh issue edit 30683 -R opencv/opencv --add-label bug   # 0.50
# gh issue edit 30691 -R opencv/opencv --add-label 'category: documentation'   # 0.50
# gh issue edit 30733 -R opencv/opencv --add-label 'category: ocl'   # 0.50
# gh issue edit 30806 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.50
# gh pr edit 30864 -R opencv/opencv --add-label 'category: imgproc'   # 0.50
# gh pr edit 30398 -R opencv/opencv --add-label 'category: core'   # 0.48
# gh pr edit 29975 -R opencv/opencv --add-label 'category: core'   # 0.47
# gh pr edit 29975 -R opencv/opencv --add-label 'category: imgproc'   # 0.47
# gh issue edit 29419 -R opencv/opencv --add-label 'category: build/install'   # 0.46
# gh issue edit 24996 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.45
# gh issue edit 26273 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.45
# gh issue edit 26273 -R opencv/opencv --add-label 'category: core'   # 0.45
# gh issue edit 26273 -R opencv/opencv --add-label 'category: ocl'   # 0.45
# gh pr edit 30613 -R opencv/opencv --add-label 'category: ocl'   # 0.45
# gh issue edit 8300 -R opencv/opencv --add-label 'category: imgproc'   # 0.44
# gh issue edit 10562 -R opencv/opencv --add-label 'category: features2d'   # 0.44
# gh issue edit 13472 -R opencv/opencv --add-label 'category: ocl'   # 0.44
# gh issue edit 16339 -R opencv/opencv --add-label 'category: python bindings'   # 0.44
# gh issue edit 22619 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.44
# gh issue edit 23428 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.44
# gh issue edit 24994 -R opencv/opencv --add-label 'category: core'   # 0.44
# gh issue edit 26126 -R opencv/opencv --add-label 'category: calib3d'   # 0.44
# gh issue edit 26156 -R opencv/opencv --add-label 'category: dnn'   # 0.44
# gh issue edit 26574 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.44
# gh issue edit 27011 -R opencv/opencv --add-label 'category: build/install'   # 0.44
# gh pr edit 29372 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.44
# gh issue edit 30602 -R opencv/opencv --add-label 'category: core'   # 0.44
# gh issue edit 30865 -R opencv/opencv --add-label 'category: dnn (onnx)'   # 0.44
# gh pr edit 30889 -R opencv/opencv --add-label 'category: core'   # 0.44
# gh issue edit 4861 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.43
# gh issue edit 5364 -R opencv/opencv --add-label 'category: imgproc'   # 0.43
# gh issue edit 6355 -R opencv/opencv --add-label 'category: documentation'   # 0.43
# gh issue edit 6355 -R opencv/opencv --add-label 'category: flann'   # 0.43
# gh issue edit 6767 -R opencv/opencv --add-label 'category: ocl'   # 0.43
# gh issue edit 7249 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 7250 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 8151 -R opencv/opencv --add-label 'category: videoio'   # 0.43
# gh issue edit 8802 -R opencv/opencv --add-label 'category: imgproc'   # 0.43
# gh issue edit 8879 -R opencv/opencv --add-label 'category: core'   # 0.43
# gh issue edit 9639 -R opencv/opencv --add-label 'category: t-api'   # 0.43
# gh issue edit 9885 -R opencv/opencv --add-label 'category: python bindings'   # 0.43
# gh pr edit 10318 -R opencv/opencv --add-label 'category: dnn'   # 0.43
# gh issue edit 11713 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.43
# gh issue edit 11811 -R opencv/opencv --add-label 'category: imgproc'   # 0.43
# gh issue edit 12733 -R opencv/opencv --add-label 'category: python bindings'   # 0.43
# gh issue edit 14023 -R opencv/opencv --add-label 'category: video'   # 0.43
# gh issue edit 15167 -R opencv/opencv --add-label 'category: dnn'   # 0.43
# gh issue edit 15630 -R opencv/opencv --add-label 'category: javascript (js)'   # 0.43
# gh issue edit 16112 -R opencv/opencv --add-label 'category: python bindings'   # 0.43
# gh issue edit 16112 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 16207 -R opencv/opencv --add-label 'category: photo'   # 0.43
# gh issue edit 16209 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 17240 -R opencv/opencv --add-label 'category: photo'   # 0.43
# gh issue edit 17277 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 18230 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 18623 -R opencv/opencv --add-label 'category: documentation'   # 0.43
# gh issue edit 18799 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 19042 -R opencv/opencv --add-label 'category: imgproc'   # 0.43
# gh issue edit 19250 -R opencv/opencv --add-label 'category: core'   # 0.43
# gh issue edit 19759 -R opencv/opencv --add-label 'category: imgproc'   # 0.43
# gh issue edit 19863 -R opencv/opencv --add-label 'category: calib3d'   # 0.43
# gh issue edit 19912 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.43
# gh issue edit 19964 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 21433 -R opencv/opencv --add-label 'category: videoio'   # 0.43
# gh issue edit 21578 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 21578 -R opencv/opencv --add-label 'category: videoio'   # 0.43
# gh issue edit 21616 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 22044 -R opencv/opencv --add-label 'category: imgproc'   # 0.43
# gh issue edit 22049 -R opencv/opencv --add-label 'category: videoio'   # 0.43
# gh issue edit 22120 -R opencv/opencv --add-label 'category: documentation'   # 0.43
# gh issue edit 22134 -R opencv/opencv --add-label 'category: dnn (onnx)'   # 0.43
# gh issue edit 22151 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 22157 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 22536 -R opencv/opencv --add-label 'category: videoio'   # 0.43
# gh issue edit 22587 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.43
# gh issue edit 22624 -R opencv/opencv --add-label 'category: features2d'   # 0.43
# gh issue edit 22663 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 22677 -R opencv/opencv --add-label 'category: videoio'   # 0.43
# gh issue edit 22688 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 22698 -R opencv/opencv --add-label 'category: core'   # 0.43
# gh issue edit 22745 -R opencv/opencv --add-label 'category: python bindings'   # 0.43
# gh issue edit 23193 -R opencv/opencv --add-label 'category: imgproc'   # 0.43
# gh issue edit 23314 -R opencv/opencv --add-label 'category: dnn'   # 0.43
# gh issue edit 23324 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 23330 -R opencv/opencv --add-label 'category: dnn (onnx)'   # 0.43
# gh issue edit 23346 -R opencv/opencv --add-label 'category: imgproc'   # 0.43
# gh issue edit 23352 -R opencv/opencv --add-label 'category: javascript (js)'   # 0.43
# gh issue edit 23366 -R opencv/opencv --add-label 'category: videoio'   # 0.43
# gh issue edit 23368 -R opencv/opencv --add-label 'category: videoio'   # 0.43
# gh issue edit 23415 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.43
# gh issue edit 23471 -R opencv/opencv --add-label 'category: features2d'   # 0.43
# gh issue edit 23539 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.43
# gh issue edit 23741 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 23741 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.43
# gh issue edit 23803 -R opencv/opencv --add-label 'category: calib3d'   # 0.43
# gh issue edit 23803 -R opencv/opencv --add-label 'category: python bindings'   # 0.43
# gh issue edit 23854 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 23858 -R opencv/opencv --add-label 'category: imgproc'   # 0.43
# gh issue edit 24107 -R opencv/opencv --add-label 'category: imgproc'   # 0.43
# gh issue edit 24389 -R opencv/opencv --add-label 'category: objdetect'   # 0.43
# gh issue edit 24439 -R opencv/opencv --add-label 'category: calib3d'   # 0.43
# gh issue edit 24481 -R opencv/opencv --add-label 'category: calib3d'   # 0.43
# gh issue edit 24682 -R opencv/opencv --add-label 'category: core'   # 0.43
# gh issue edit 24707 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 24787 -R opencv/opencv --add-label 'category: videoio'   # 0.43
# gh issue edit 24886 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 25223 -R opencv/opencv --add-label 'category: videoio'   # 0.43
# gh issue edit 25244 -R opencv/opencv --add-label 'category: core'   # 0.43
# gh issue edit 25316 -R opencv/opencv --add-label 'category: objdetect'   # 0.43
# gh issue edit 25614 -R opencv/opencv --add-label 'category: dnn'   # 0.43
# gh issue edit 25705 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.43
# gh issue edit 25744 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.43
# gh issue edit 25752 -R opencv/opencv --add-label 'category: core'   # 0.43
# gh issue edit 25782 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 25783 -R opencv/opencv --add-label 'category: python bindings'   # 0.43
# gh issue edit 25797 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.43
# gh issue edit 26015 -R opencv/opencv --add-label 'category: python bindings'   # 0.43
# gh issue edit 26064 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 26288 -R opencv/opencv --add-label 'category: documentation'   # 0.43
# gh issue edit 26392 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 26392 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.43
# gh issue edit 26406 -R opencv/opencv --add-label 'category: documentation'   # 0.43
# gh issue edit 26674 -R opencv/opencv --add-label 'category: dnn (onnx)'   # 0.43
# gh issue edit 26896 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh pr edit 26989 -R opencv/opencv --add-label 'category: imgproc'   # 0.43
# gh issue edit 27283 -R opencv/opencv --add-label 'category: calib3d'   # 0.43
# gh issue edit 27618 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 27935 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 27971 -R opencv/opencv --add-label 'category: java bindings'   # 0.43
# gh pr edit 28223 -R opencv/opencv --add-label 'category: dnn'   # 0.43
# gh issue edit 28391 -R opencv/opencv --add-label 'category: samples'   # 0.43
# gh issue edit 28599 -R opencv/opencv --add-label 'category: ocl'   # 0.43
# gh issue edit 28924 -R opencv/opencv --add-label 'category: build/install'   # 0.43
# gh issue edit 28960 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.43
# gh issue edit 29011 -R opencv/opencv --add-label 'category: imgproc'   # 0.43
# gh pr edit 29334 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.43
# gh issue edit 29444 -R opencv/opencv --add-label 'category: documentation'   # 0.43
# gh issue edit 30459 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.43
# gh issue edit 30813 -R opencv/opencv --add-label 'category: core'   # 0.43
# gh pr edit 30826 -R opencv/opencv --add-label 'category: imgproc'   # 0.43
# gh pr edit 30829 -R opencv/opencv --add-label 'category: calib3d'   # 0.43
# gh pr edit 30863 -R opencv/opencv --add-label 'category: core'   # 0.43
# gh issue edit 27467 -R opencv/opencv --add-label 'category: build/install'   # 0.42
# gh issue edit 29002 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.42
# gh pr edit 29951 -R opencv/opencv --add-label 'category: core'   # 0.41
# gh pr edit 29952 -R opencv/opencv --add-label 'category: core'   # 0.41
# gh pr edit 29986 -R opencv/opencv --add-label 'category: core'   # 0.41
# gh pr edit 30058 -R opencv/opencv --add-label 'category: core'   # 0.41
# gh pr edit 30398 -R opencv/opencv --add-label 'category: ocl'   # 0.39
# gh issue edit 11015 -R opencv/opencv --add-label 'category: calib3d'   # 0.38
# gh issue edit 19129 -R opencv/opencv --add-label 'category: build/install'   # 0.38
# gh issue edit 19350 -R opencv/opencv --add-label 'category: build/install'   # 0.38
# gh issue edit 19945 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.38
# gh issue edit 22132 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.38
# gh issue edit 22238 -R opencv/opencv --add-label 'category: python bindings'   # 0.38
# gh issue edit 24470 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.38
# gh issue edit 25303 -R opencv/opencv --add-label 'category: build/install'   # 0.38
# gh issue edit 25332 -R opencv/opencv --add-label 'category: videoio'   # 0.38
# gh issue edit 25620 -R opencv/opencv --add-label 'category: dnn'   # 0.38
# gh issue edit 25795 -R opencv/opencv --add-label 'category: core'   # 0.38
# gh pr edit 29372 -R opencv/opencv --add-label 'category: core'   # 0.38
# gh pr edit 29372 -R opencv/opencv --add-label 'category: ocl'   # 0.38
# gh issue edit 29935 -R opencv/opencv --add-label 'category: core'   # 0.38
# gh issue edit 30384 -R opencv/opencv --add-label 'category: imgproc'   # 0.38
# gh pr edit 30786 -R opencv/opencv --add-label 'category: dnn'   # 0.38
# gh pr edit 25951 -R opencv/opencv --add-label 'category: core'   # 0.36
# gh issue edit 27206 -R opencv/opencv --add-label 'category: photo'   # 0.36
# gh issue edit 24996 -R opencv/opencv --add-label 'category: core'   # 0.34
# gh issue edit 10157 -R opencv/opencv --add-label 'category: videoio'   # 0.33
# gh issue edit 10157 -R opencv/opencv --add-label 'category: build/install'   # 0.33
# gh issue edit 23434 -R opencv/opencv --add-label 'category: core'   # 0.33
# gh issue edit 25011 -R opencv/opencv --add-label 'category: core'   # 0.33
# gh issue edit 25019 -R opencv/opencv --add-label 'category: core'   # 0.33
# gh issue edit 26574 -R opencv/opencv --add-label 'category: imgproc'   # 0.33
# gh issue edit 27011 -R opencv/opencv --add-label 'category: dnn'   # 0.33
# gh pr edit 28994 -R opencv/opencv --add-label 'category: build/install'   # 0.33
# gh pr edit 29320 -R opencv/opencv --add-label 'category: ocl'   # 0.33
# gh issue edit 29712 -R opencv/opencv --add-label 'category: dnn'   # 0.33
# gh pr edit 30228 -R opencv/opencv --add-label 'category: core'   # 0.33
# gh pr edit 30378 -R opencv/opencv --add-label 'category: calib3d'   # 0.33
# gh pr edit 30378 -R opencv/opencv --add-label 'category: core'   # 0.33
# gh issue edit 30870 -R opencv/opencv --add-label 'category: ocl'   # 0.33
# gh issue edit 13407 -R opencv/opencv --add-label 'category: ocl'   # 0.31
# gh issue edit 13472 -R opencv/opencv --add-label 'category: core'   # 0.31
# gh issue edit 13891 -R opencv/opencv --add-label 'category: build/install'   # 0.31
# gh issue edit 15675 -R opencv/opencv --add-label 'category: core'   # 0.31
# gh issue edit 15675 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.31
# gh issue edit 22098 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.31
# gh issue edit 23066 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.31
# gh pr edit 28623 -R opencv/opencv --add-label 'category: ocl'   # 0.31
# gh issue edit 11012 -R opencv/opencv --add-label 'category: imgproc'   # 0.30
# gh issue edit 19008 -R opencv/opencv --add-label 'category: imgproc'   # 0.30
# gh pr edit 29951 -R opencv/opencv --add-label 'category: calib3d'   # 0.30
# gh pr edit 29952 -R opencv/opencv --add-label 'category: calib3d'   # 0.30
# gh pr edit 29986 -R opencv/opencv --add-label 'category: calib3d'   # 0.30
# gh pr edit 30058 -R opencv/opencv --add-label 'category: calib3d'   # 0.30
# gh issue edit 30502 -R opencv/opencv --add-label 'category: features2d'   # 0.30
# gh issue edit 30621 -R opencv/opencv --add-label 'category: ocl'   # 0.30
# gh pr edit 30722 -R opencv/opencv --add-label 'category: calib3d'   # 0.30
# gh issue edit 4469 -R opencv/opencv --add-label 'category: videoio'   # 0.29
# gh issue edit 4479 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.29
# gh issue edit 4659 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 4747 -R opencv/opencv --add-label 'category: samples'   # 0.29
# gh issue edit 4865 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.29
# gh issue edit 4898 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 5220 -R opencv/opencv --add-label 'category: infrastructure'   # 0.29
# gh issue edit 5364 -R opencv/opencv --add-label 'category: ocl'   # 0.29
# gh issue edit 5364 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 6092 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.29
# gh issue edit 6291 -R opencv/opencv --add-label 'category: python bindings'   # 0.29
# gh issue edit 6587 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 6767 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 7124 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh issue edit 7245 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 7479 -R opencv/opencv --add-label 'category: python bindings'   # 0.29
# gh issue edit 7525 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 8022 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 8094 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 8151 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.29
# gh issue edit 8151 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.29
# gh issue edit 8584 -R opencv/opencv --add-label 'category: python bindings'   # 0.29
# gh issue edit 8879 -R opencv/opencv --add-label 'category: python bindings'   # 0.29
# gh issue edit 9065 -R opencv/opencv --add-label 'category: samples'   # 0.29
# gh issue edit 9065 -R opencv/opencv --add-label 'category: documentation'   # 0.29
# gh issue edit 9184 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.29
# gh issue edit 9224 -R opencv/opencv --add-label 'category: documentation'   # 0.29
# gh issue edit 9413 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 9639 -R opencv/opencv --add-label 'category: ocl'   # 0.29
# gh issue edit 10075 -R opencv/opencv --add-label 'category: features2d'   # 0.29
# gh issue edit 10075 -R opencv/opencv --add-label 'category: dnn'   # 0.29
# gh issue edit 10101 -R opencv/opencv --add-label 'category: t-api'   # 0.29
# gh issue edit 10101 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.29
# gh issue edit 10849 -R opencv/opencv --add-label 'category: documentation'   # 0.29
# gh issue edit 10849 -R opencv/opencv --add-label 'category: dnn'   # 0.29
# gh issue edit 12733 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 13077 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 13170 -R opencv/opencv --add-label 'category: t-api'   # 0.29
# gh issue edit 13790 -R opencv/opencv --add-label 'category: python bindings'   # 0.29
# gh issue edit 14023 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh issue edit 14589 -R opencv/opencv --add-label 'category: java bindings'   # 0.29
# gh issue edit 14589 -R opencv/opencv --add-label 'category: javascript (js)'   # 0.29
# gh issue edit 14819 -R opencv/opencv --add-label 'category: dnn'   # 0.29
# gh issue edit 15410 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 15909 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh issue edit 15909 -R opencv/opencv --add-label 'category: calib3d'   # 0.29
# gh issue edit 15914 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.29
# gh issue edit 16303 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 16303 -R opencv/opencv --add-label 'category: dnn'   # 0.29
# gh issue edit 16939 -R opencv/opencv --add-label 'category: python bindings'   # 0.29
# gh issue edit 17491 -R opencv/opencv --add-label 'category: stitching'   # 0.29
# gh issue edit 17491 -R opencv/opencv --add-label 'category: documentation'   # 0.29
# gh issue edit 18147 -R opencv/opencv --add-label 'category: calib3d'   # 0.29
# gh issue edit 18599 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 19150 -R opencv/opencv --add-label 'category: documentation'   # 0.29
# gh issue edit 19437 -R opencv/opencv --add-label 'category: calib3d'   # 0.29
# gh issue edit 19437 -R opencv/opencv --add-label 'category: python bindings'   # 0.29
# gh issue edit 19442 -R opencv/opencv --add-label 'category: videoio'   # 0.29
# gh issue edit 19759 -R opencv/opencv --add-label 'category: documentation'   # 0.29
# gh issue edit 19759 -R opencv/opencv --add-label 'category: video'   # 0.29
# gh issue edit 20193 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.29
# gh issue edit 21396 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh issue edit 21423 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 21434 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.29
# gh issue edit 21464 -R opencv/opencv --add-label 'category: documentation'   # 0.29
# gh issue edit 21464 -R opencv/opencv --add-label 'category: infrastructure'   # 0.29
# gh issue edit 21515 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 21578 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.29
# gh issue edit 21647 -R opencv/opencv --add-label 'category: documentation'   # 0.29
# gh issue edit 21836 -R opencv/opencv --add-label 'category: g-api / gapi'   # 0.29
# gh issue edit 21836 -R opencv/opencv --add-label 'category: javascript (js)'   # 0.29
# gh issue edit 21912 -R opencv/opencv --add-label 'category: documentation'   # 0.29
# gh issue edit 21944 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 22044 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 22044 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 22055 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.29
# gh issue edit 22058 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.29
# gh issue edit 22060 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.29
# gh issue edit 22087 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 22157 -R opencv/opencv --add-label 'category: python bindings'   # 0.29
# gh issue edit 22338 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 22342 -R opencv/opencv --add-label 'category: g-api / gapi'   # 0.29
# gh issue edit 22481 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 22481 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.29
# gh issue edit 22548 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.29
# gh issue edit 22548 -R opencv/opencv --add-label 'category: videoio'   # 0.29
# gh issue edit 22550 -R opencv/opencv --add-label 'category: features2d'   # 0.29
# gh issue edit 22564 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh issue edit 22587 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 22616 -R opencv/opencv --add-label 'category: dnn'   # 0.29
# gh issue edit 22627 -R opencv/opencv --add-label 'category: features2d'   # 0.29
# gh issue edit 22677 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.29
# gh issue edit 22745 -R opencv/opencv --add-label 'category: samples'   # 0.29
# gh issue edit 22817 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh issue edit 22949 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 22983 -R opencv/opencv --add-label 'category: g-api / gapi'   # 0.29
# gh issue edit 22983 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.29
# gh issue edit 23024 -R opencv/opencv --add-label 'category: documentation'   # 0.29
# gh issue edit 23099 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh issue edit 23099 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 23163 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 23208 -R opencv/opencv --add-label 'category: samples'   # 0.29
# gh issue edit 23303 -R opencv/opencv --add-label 'category: calib3d'   # 0.29
# gh issue edit 23312 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh issue edit 23346 -R opencv/opencv --add-label 'category: features2d'   # 0.29
# gh issue edit 23346 -R opencv/opencv --add-label 'category: calib3d'   # 0.29
# gh issue edit 23352 -R opencv/opencv --add-label 'category: python bindings'   # 0.29
# gh issue edit 23369 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 23395 -R opencv/opencv --add-label 'category: photo'   # 0.29
# gh issue edit 23415 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.29
# gh issue edit 23426 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.29
# gh issue edit 23457 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh issue edit 23471 -R opencv/opencv --add-label 'category: ocl'   # 0.29
# gh issue edit 23543 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.29
# gh issue edit 23543 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh issue edit 23623 -R opencv/opencv --add-label 'category: documentation'   # 0.29
# gh issue edit 23640 -R opencv/opencv --add-label 'category: videoio'   # 0.29
# gh issue edit 23640 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.29
# gh issue edit 23726 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 23817 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh issue edit 23858 -R opencv/opencv --add-label 'category: samples'   # 0.29
# gh issue edit 23858 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.29
# gh issue edit 23906 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh issue edit 23995 -R opencv/opencv --add-label 'category: java bindings'   # 0.29
# gh issue edit 23995 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 23995 -R opencv/opencv --add-label 'category: dnn'   # 0.29
# gh issue edit 24007 -R opencv/opencv --add-label 'category: contrib'   # 0.29
# gh issue edit 24088 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.29
# gh issue edit 24088 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.29
# gh issue edit 24192 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh pr edit 24193 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 24389 -R opencv/opencv --add-label 'category: documentation'   # 0.29
# gh issue edit 24439 -R opencv/opencv --add-label 'category: documentation'   # 0.29
# gh issue edit 24439 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh issue edit 24481 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 24514 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 24514 -R opencv/opencv --add-label 'category: documentation'   # 0.29
# gh issue edit 24518 -R opencv/opencv --add-label 'category: java bindings'   # 0.29
# gh issue edit 24518 -R opencv/opencv --add-label 'category: dnn'   # 0.29
# gh issue edit 24541 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.29
# gh issue edit 24571 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.29
# gh issue edit 24571 -R opencv/opencv --add-label 'category: videoio'   # 0.29
# gh issue edit 24682 -R opencv/opencv --add-label 'category: java bindings'   # 0.29
# gh issue edit 24787 -R opencv/opencv --add-label 'category: python bindings'   # 0.29
# gh issue edit 24816 -R opencv/opencv --add-label 'category: calib3d'   # 0.29
# gh issue edit 25013 -R opencv/opencv --add-label 'category: stitching'   # 0.29
# gh issue edit 25032 -R opencv/opencv --add-label 'category: documentation'   # 0.29
# gh issue edit 25136 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh issue edit 25136 -R opencv/opencv --add-label 'category: python bindings'   # 0.29
# gh issue edit 25233 -R opencv/opencv --add-label 'category: dnn (onnx)'   # 0.29
# gh issue edit 25244 -R opencv/opencv --add-label 'category: python bindings'   # 0.29
# gh issue edit 25290 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.29
# gh issue edit 25315 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.29
# gh issue edit 25315 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 25446 -R opencv/opencv --add-label 'category: dnn'   # 0.29
# gh issue edit 25676 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 25705 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.29
# gh issue edit 25744 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 25752 -R opencv/opencv --add-label 'category: ocl'   # 0.29
# gh issue edit 25782 -R opencv/opencv --add-label 'category: swift/objc bindings'   # 0.29
# gh issue edit 25783 -R opencv/opencv --add-label 'category: samples'   # 0.29
# gh issue edit 25871 -R opencv/opencv --add-label 'category: video'   # 0.29
# gh issue edit 25948 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 25977 -R opencv/opencv --add-label 'category: documentation'   # 0.29
# gh issue edit 25977 -R opencv/opencv --add-label 'category: calib3d'   # 0.29
# gh issue edit 25993 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 25993 -R opencv/opencv --add-label 'category: documentation'   # 0.29
# gh issue edit 26015 -R opencv/opencv --add-label 'category: calib3d'   # 0.29
# gh issue edit 26036 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 26064 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.29
# gh issue edit 26089 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.29
# gh issue edit 26089 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh issue edit 26121 -R opencv/opencv --add-label 'category: calib3d'   # 0.29
# gh issue edit 26121 -R opencv/opencv --add-label 'category: objdetect'   # 0.29
# gh issue edit 26305 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.29
# gh issue edit 26305 -R opencv/opencv --add-label 'category: videoio'   # 0.29
# gh issue edit 26419 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 26494 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.29
# gh issue edit 26718 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.29
# gh issue edit 26718 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 26860 -R opencv/opencv --add-label 'category: video'   # 0.29
# gh issue edit 27143 -R opencv/opencv --add-label 'category: dnn'   # 0.29
# gh issue edit 27231 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh issue edit 27308 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 27751 -R opencv/opencv --add-label 'category: videoio(camera)'   # 0.29
# gh issue edit 27751 -R opencv/opencv --add-label 'category: videoio'   # 0.29
# gh issue edit 27901 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 27955 -R opencv/opencv --add-label 'category: video'   # 0.29
# gh issue edit 28280 -R opencv/opencv --add-label 'category: videoio'   # 0.29
# gh issue edit 28335 -R opencv/opencv --add-label 'category: infrastructure'   # 0.29
# gh issue edit 28391 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.29
# gh issue edit 28462 -R opencv/opencv --add-label 'category: python bindings'   # 0.29
# gh pr edit 28492 -R opencv/opencv --add-label 'category: videoio'   # 0.29
# gh pr edit 28492 -R opencv/opencv --add-label 'category: ocl'   # 0.29
# gh issue edit 28514 -R opencv/opencv --add-label 'category: features2d'   # 0.29
# gh issue edit 29015 -R opencv/opencv --add-label 'category: documentation'   # 0.29
# gh issue edit 29212 -R opencv/opencv --add-label 'category: infrastructure'   # 0.29
# gh issue edit 29287 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh issue edit 29287 -R opencv/opencv --add-label 'category: calib3d'   # 0.29
# gh issue edit 29444 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 29454 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 29559 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh issue edit 29869 -R opencv/opencv --add-label 'category: 3d module'   # 0.29
# gh issue edit 29869 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh pr edit 29962 -R opencv/opencv --add-label 'category: build/install'   # 0.29
# gh issue edit 29990 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh pr edit 30074 -R opencv/opencv --add-label 'category: video'   # 0.29
# gh pr edit 30472 -R opencv/opencv --add-label 'category: dnn'   # 0.29
# gh issue edit 30487 -R opencv/opencv --add-label 'category: samples'   # 0.29
# gh pr edit 30627 -R opencv/opencv --add-label 'category: core'   # 0.29
# gh pr edit 30814 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh issue edit 30821 -R opencv/opencv --add-label 'category: python bindings'   # 0.29
# gh pr edit 30826 -R opencv/opencv --add-label 'category: video'   # 0.29
# gh issue edit 30861 -R opencv/opencv --add-label 'category: imgproc'   # 0.29
# gh pr edit 30887 -R opencv/opencv --add-label 'category: g-api / gapi'   # 0.29
# gh issue edit 8300 -R opencv/opencv --add-label 'category: core'   # 0.28
# gh issue edit 11460 -R opencv/opencv --add-label 'category: build/install'   # 0.28
# gh issue edit 30017 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.28
# gh issue edit 7263 -R opencv/opencv --add-label 'category: documentation'   # 0.27
# gh issue edit 25019 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.27
# gh pr edit 25951 -R opencv/opencv --add-label 'category: imgproc'   # 0.27
# gh pr edit 28736 -R opencv/opencv --add-label 'category: ocl'   # 0.27
# gh issue edit 29776 -R opencv/opencv --add-label 'category: imgproc'   # 0.27
# gh pr edit 29975 -R opencv/opencv --add-label 'category: calib3d'   # 0.27
# gh pr edit 30398 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.26
# gh issue edit 7298 -R opencv/opencv --add-label 'category: build/install'   # 0.25
# gh issue edit 9809 -R opencv/opencv --add-label 'category: documentation'   # 0.25
# gh issue edit 14475 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.25
# gh issue edit 16339 -R opencv/opencv --add-label 'category: build/install'   # 0.25
# gh issue edit 16701 -R opencv/opencv --add-label 'category: features2d'   # 0.25
# gh issue edit 17997 -R opencv/opencv --add-label 'category: javascript (js)'   # 0.25
# gh issue edit 19350 -R opencv/opencv --add-label 'category: photo'   # 0.25
# gh issue edit 19945 -R opencv/opencv --add-label 'category: python bindings'   # 0.25
# gh issue edit 19945 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.25
# gh issue edit 20122 -R opencv/opencv --add-label 'category: swift/objc bindings'   # 0.25
# gh issue edit 22238 -R opencv/opencv --add-label 'category: build/install'   # 0.25
# gh issue edit 22619 -R opencv/opencv --add-label 'category: python bindings'   # 0.25
# gh issue edit 22641 -R opencv/opencv --add-label 'category: stitching'   # 0.25
# gh issue edit 22791 -R opencv/opencv --add-label 'category: core'   # 0.25
# gh issue edit 22867 -R opencv/opencv --add-label 'category: build/install'   # 0.25
# gh issue edit 24470 -R opencv/opencv --add-label 'category: documentation'   # 0.25
# gh issue edit 25332 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.25
# gh issue edit 26329 -R opencv/opencv --add-label 'category: imgproc'   # 0.25
# gh issue edit 26961 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.25
# gh issue edit 27467 -R opencv/opencv --add-label 'category: objdetect'   # 0.25
# gh issue edit 27467 -R opencv/opencv --add-label 'category: dnn'   # 0.25
# gh pr edit 28433 -R opencv/opencv --add-label 'category: python bindings'   # 0.25
# gh issue edit 29313 -R opencv/opencv --add-label 'category: core'   # 0.25
# gh issue edit 29318 -R opencv/opencv --add-label 'category: gpu/cuda (contrib)'   # 0.25
# gh issue edit 29705 -R opencv/opencv --add-label 'category: objdetect'   # 0.25
# gh issue edit 29705 -R opencv/opencv --add-label 'category: core'   # 0.25
# gh issue edit 29935 -R opencv/opencv --add-label 'category: highgui-gui'   # 0.25
# gh issue edit 30067 -R opencv/opencv --add-label 'category: ocl'   # 0.25
# gh pr edit 30179 -R opencv/opencv --add-label 'category: dnn'   # 0.25
# gh issue edit 30605 -R opencv/opencv --add-label 'category: dnn (onnx)'   # 0.25
# gh issue edit 30621 -R opencv/opencv --add-label 'category: t-api'   # 0.25
# gh issue edit 30691 -R opencv/opencv --add-label 'category: core'   # 0.25
# gh issue edit 30744 -R opencv/opencv --add-label 'category: python bindings'   # 0.25
# gh issue edit 30787 -R opencv/opencv --add-label 'category: dnn'   # 0.25
# gh issue edit 30787 -R opencv/opencv --add-label 'category: photo'   # 0.25
# gh issue edit 30862 -R opencv/opencv --add-label 'category: imgproc'   # 0.25
# gh pr edit 30146 -R opencv/opencv --add-label 'category: dnn (onnx)'   # 0.23
# gh pr edit 30481 -R opencv/opencv --add-label 'category: documentation'   # 0.23
# gh issue edit 10562 -R opencv/opencv --add-label 'category: python bindings'   # 0.22
# gh issue edit 11023 -R opencv/opencv --add-label 'category: dnn'   # 0.22
# gh issue edit 11460 -R opencv/opencv --add-label 'category: documentation'   # 0.22
# gh issue edit 21720 -R opencv/opencv --add-label 'category: video'   # 0.22
# gh issue edit 25025 -R opencv/opencv --add-label 'category: ocl'   # 0.22
# gh issue edit 26574 -R opencv/opencv --add-label 'category: python bindings'   # 0.22
# gh issue edit 29150 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.22
# gh pr edit 29527 -R opencv/opencv --add-label 'category: build/install'   # 0.22
# gh pr edit 30485 -R opencv/opencv --add-label 'category: imgproc'   # 0.22
# gh issue edit 30806 -R opencv/opencv --add-label 'category: objdetect'   # 0.22
# gh pr edit 30889 -R opencv/opencv --add-label 'category: dnn'   # 0.22
# gh pr edit 29992 -R opencv/opencv --add-label 'category: calib3d'   # 0.21
# gh issue edit 30376 -R opencv/opencv --add-label 'category: imgproc'   # 0.21
# gh issue edit 19008 -R opencv/opencv --add-label 'category: core'   # 0.20
# gh issue edit 25019 -R opencv/opencv --add-label 'category: imgproc'   # 0.20
# gh issue edit 28948 -R opencv/opencv --add-label 'category: imgproc'   # 0.20
# gh issue edit 7263 -R opencv/opencv --add-label 'category: dnn'   # 0.18
# gh issue edit 16394 -R opencv/opencv --add-label 'category: samples'   # 0.18
# gh pr edit 25951 -R opencv/opencv --add-label 'category: 3d module'   # 0.18
# gh pr edit 30146 -R opencv/opencv --add-label 'category: documentation'   # 0.18
# gh pr edit 30146 -R opencv/opencv --add-label 'category: core'   # 0.18
# gh issue edit 30630 -R opencv/opencv --add-label 'category: documentation'   # 0.18
# gh issue edit 29234 -R opencv/opencv --add-label 'category: imgproc'   # 0.17
# gh pr edit 30179 -R opencv/opencv --add-label 'category: ocl'   # 0.17
# gh issue edit 30361 -R opencv/opencv --add-label 'category: documentation'   # 0.17
# gh issue edit 30783 -R opencv/opencv --add-label 'category: core'   # 0.17
# gh issue edit 30819 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.17
# gh issue edit 24996 -R opencv/opencv --add-label 'category: imgproc'   # 0.16
# gh issue edit 15675 -R opencv/opencv --add-label 'category: python bindings'   # 0.15
# gh issue edit 30594 -R opencv/opencv --add-label 'category: 3rdparty'   # 0.15
# gh issue edit 30792 -R opencv/opencv --add-label 'category: flann'   # 0.15
# gh issue edit 8300 -R opencv/opencv --add-label 'category: imgcodecs'   # 0.12
# gh issue edit 24996 -R opencv/opencv --add-label 'category: build/install'   # 0.11
