rm accuracies.txt
# Ami songs
# anyway
printf "****Anyway Test****\n" >> accuracies.txt
python3 ../../Util/split.py ../../Tuffy/DB_Files/anyway.db ../DB_Files/testr.db ../DB_Files/testl.db
python3 ../Inference/right_annotation.py >> ../Results/anyway.txt
printf "Anyway Test Right:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputr.db ../../Tuffy/DB_Files/anyway.db >> accuracies.txt
python3 ../Inference/left_annotation.py >> ../Results/anyway.txt
printf "Anyway Test Left:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputl.db ../../Tuffy/DB_Files/anyway.db >> accuracies.txt
cat ../Results/outputl.db ../Results/outputr.db > ../Results/anyway_result.db
printf "Anyway Test Overall:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/anyway_result.db ../../Tuffy/DB_Files/anyway.db >> accuracies.txt


# yesterday
printf "\n****Yesterday Test****\n" >> accuracies.txt
python3 ../../Util/split.py ../../Tuffy/DB_Files/yesterday.db ../DB_Files/testr.db ../DB_Files/testl.db
python3 ../Inference/right_annotation.py >> ../Results/yesterday.txt
printf "Yesterday Test Right:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputr.db ../../Tuffy/DB_Files/yesterday.db >> accuracies.txt
python3 ../Inference/left_annotation.py >> ../Results/yesterday.txt
printf "Yesterday Test Left:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputl.db ../../Tuffy/DB_Files/yesterday.db >> accuracies.txt
printf "Yesterday Test Overall:\n" >> accuracies.txt
cat ../Results/outputl.db ../Results/outputr.db > ../Results/yesterday_result.db
python3 ../../Util/accuracy_test.py ../Results/yesterday_result.db ../../Tuffy/DB_Files/yesterday.db >> accuracies.txt

#hey_jude HEY JUDE DB IS CURRENTLY BROKEN
#printf "\n****Hey Jude Test****\n" >> accuracies.txt
#python3 ../../Util/split.py ../../Tuffy/DB_Files/hey_jude.db ../DB_Files/testr.db ../DB_Files/testl.db
#python3 ../Inference/right_annotation.py >> ../Results/hey_jude.txt
#printf "Hey Jude Test Right:\n" >> accuracies.txt
#python3 ../../Util/accuracy_test.py ../Results/outputr.db ../../Tuffy/DB_Files/hey_jude.db >> accuracies.txt
#python3 ../Inference/left_annotation.py >> ../Results/hey_jude.txt
#printf "Hey Jude Test Left:\n" >> accuracies.txt
#cat ../Results/outputl.db > test
#python3 ../../Util/accuracy_test.py ../Results/outputl.db ../../Tuffy/DB_Files/hey_jude.db >> accuracies.txt
#printf "Hey Jude Test Overall:\n" >> accuracies.txt
#cat ../Results/outputl.db ../Results/outputr.db > ../Results/hey_jude_result.db
#python3 ../../Util/accuracy_test.py ../Results/hey_jude_result.db ../../Tuffy/DB_Files/hey_jude.db >> accuracies.txt

#summertime_sadness
printf "\n****Summertime Sadness Test****\n" >> accuracies.txt
python3 ../../Util/split.py ../../Tuffy/DB_Files/summertime_sadness.db ../DB_Files/testr.db ../DB_Files/testl.db
python3 ../Inference/right_annotation.py >> ../Results/summetime_sadness.txt
printf "Summertime Sadness Test Right:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputr.db ../../Tuffy/DB_Files/summertime_sadness.db >> accuracies.txt
python3 ../Inference/left_annotation.py >> ../Results/summertime_sadness.txt
printf "Summertime Sadness Test Left:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputl.db ../../Tuffy/DB_Files/summertime_sadness.db >> accuracies.txt
printf "Summertime Sadness Test Overall:\n" >> accuracies.txt
cat ../Results/outputl.db ../Results/outputr.db > ../Results/summertime_sadness_result.db
python3 ../../Util/accuracy_test.py ../Results/summertime_sadness_result.db ../../Tuffy/DB_Files/summertime_sadness.db >> accuracies.txt

#the_greatest
printf "\n****The Greatest Test****\n" >> accuracies.txt
python3 ../../Util/split.py ../../Tuffy/DB_Files/the_greatest.db ../DB_Files/testr.db ../DB_Files/testl.db
python3 ../Inference/right_annotation.py >> ../Results/summertime_sadness.txt
printf "The Greatest Test Right:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputr.db ../../Tuffy/DB_Files/the_greatest.db >> accuracies.txt
python3 ../Inference/left_annotation.py >> ../Results/summertime_sadness.txt
printf "The Greatest Test Left:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputl.db ../../Tuffy/DB_Files/the_greatest.db >> accuracies.txt
printf "The Greatest Test Overall:\n" >> accuracies.txt
cat ../Results/outputl.db ../Results/outputr.db > ../Results/the_greatest_result.db
python3 ../../Util/accuracy_test.py ../Results/the_greatest_result.db ../../Tuffy/DB_Files/the_greatest.db >> accuracies.txt

#standin in the rain
#printf "\n****Standin in the Rain Test****\n" >> accuracies.txt
#python3 ../../Util/split.py ../../Tuffy/DB_Files/standin_in_the_rain.db ../DB_Files/testr.db ../DB_Files/testl.db
#python3 ../Inference/right_annotation.py >> ../Results/standin_in_the_rain.txt
#printf "Standin in the Rain Test Right:\n" >> accuracies.txt
#python3 ../../Util/accuracy_test.py ../Results/outputr.db ../../Tuffy/DB_Files/standin_in_the_rain.db >> accuracies.txt
#python3 ../Inference/left_annotation.py >> ../Results/standin_in_the_rain.txt
#printf "Standin in the Rain Test Left:\n" >> accuracies.txt
#python3 ../../Util/accuracy_test.py ../Results/outputl.db ../../Tuffy/DB_Files/standin_in_the_rain.db >> accuracies.txt
#printf "Standin in the Rain Test Overall:\n" >> accuracies.txt
#cat ../Results/outputl.db ../Results/outputr.db > ../Results/standin_in_the_rain_result.db
#python3 ../../Util/accuracy_test.py ../Results/standin_in_the_rain_result.db ../../Tuffy/DB_Files/standin_in_the_rain.db >> accuracies.txt

#daydreaming Broken like
printf "\n****Daydreaming Test****\n" >> accuracies.txt
python3 ../../Util/split.py ../../Tuffy/DB_Files/daydreaming.db ../DB_Files/testr.db ../DB_Files/testl.db
python3 ../Inference/right_annotation.py >> ../Results/daydreaming.txt
printf "Daydreaming Test Right:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputr.db ../../Tuffy/DB_Files/daydreaming.db >> accuracies.txt
python3 ../Inference/left_annotation.py >> ../Results/daydreaming.txt
printf "Daydreaming Test Left:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputl.db ../../Tuffy/DB_Files/daydreaming.db >> accuracies.txt
printf "Daydreaming Test Overall:\n" >> accuracies.txt
cat ../Results/outputl.db ../Results/outputr.db > ../Results/daydreaming_result.db
python3 ../../Util/accuracy_test.py ../Results/daydreaming_result.db ../../Tuffy/DB_Files/daydreaming.db >> accuracies.txt

#Kristen songs:
# Lady madonna
printf "\n****Lady Madonna Test****\n" >> accuracies.txt
python3 ../../Util/split.py ../../Tuffy/DB_Files/lady_madonna.db ../DB_Files/testr.db ../DB_Files/testl.db
python3 ../Inference/right_annotation.py >> ../Results/lady_madonna.txt
printf "Lady Madonna Test Right:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputr.db ../../Tuffy/DB_Files/lady_madonna.db >> accuracies.txt
python3 ../Inference/left_annotation.py >> ../Results/lady_madonna.txt
printf "Lady Madonna Test Left:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputl.db ../../Tuffy/DB_Files/lady_madonna.db >> accuracies.txt
printf "Lady Madonna Test Overall:\n" >> accuracies.txt
cat ../Results/outputl.db ../Results/outputr.db > ../Results/lady_madonna_result.db
python3 ../../Util/accuracy_test.py ../Results/lady_madonna_result.db ../../Tuffy/DB_Files/lady_madonna.db >> accuracies.txt

# Martha my dear
printf "\n****Martha My Dear Test****\n" >> accuracies.txt
python3 ../../Util/split.py ../../Tuffy/DB_Files/martha_my_dear.db ../DB_Files/testr.db ../DB_Files/testl.db
python3 ../Inference/right_annotation.py >> ../Results/martha_my_dear.txt
printf "Lady Madonna Test Right:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputr.db ../../Tuffy/DB_Files/martha_my_dear.db >> accuracies.txt
python3 ../Inference/left_annotation.py >> ../Results/martha_my_dear.txt
printf "Lady Madonna Test Left:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputl.db ../../Tuffy/DB_Files/martha_my_dear.db >> accuracies.txt
printf "Lady Madonna Test Overall:\n" >> accuracies.txt
cat ../Results/outputl.db ../Results/outputr.db > ../Results/martha_my_dear_result.db
python3 ../../Util/accuracy_test.py ../Results/martha_my_dear_result.db ../../Tuffy/DB_Files/martha_my_dear.db >> accuracies.txt

# moonchild
printf "\n****Moonchild Test****\n" >> accuracies.txt
python3 ../../Util/split.py ../../Tuffy/DB_Files/moonchild.db ../DB_Files/testr.db ../DB_Files/testl.db
python3 ../Inference/right_annotation.py >> ../Results/moonchild.txt
printf "Moonchild Test Right:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputr.db ../../Tuffy/DB_Files/moonchild.db >> accuracies.txt
python3 ../Inference/left_annotation.py >> ../Results/moonchild.txt
printf "Moonchild Test Left:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputl.db ../../Tuffy/DB_Files/moonchild.db >> accuracies.txt
printf "Moonchild Test Overall:\n" >> accuracies.txt
cat ../Results/outputl.db ../Results/outputr.db > ../Results/moonchild_result.db
python3 ../../Util/accuracy_test.py ../Results/moonchild_result.db ../../Tuffy/DB_Files/moonchild.db >> accuracies.txt

# strange_magic
printf "\n****Strange Magic Test****\n" >> accuracies.txt
python3 ../../Util/split.py ../../Tuffy/DB_Files/strange_magic.db ../DB_Files/testr.db ../DB_Files/testl.db
python3 ../Inference/right_annotation.py >> ../Results/strange_magic.txt
printf "Strange Magic Test Right:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputr.db ../../Tuffy/DB_Files/strange_magic.db >> accuracies.txt
python3 ../Inference/left_annotation.py >> ../Results/strange_magic.txt
printf "Strange Magic Test Left:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputl.db ../../Tuffy/DB_Files/strange_magic.db >> accuracies.txt
printf "Strange Magic Test Overall:\n" >> accuracies.txt
cat ../Results/outputl.db ../Results/outputr.db > ../Results/strange_magic_result.db
python3 ../../Util/accuracy_test.py ../Results/strange_magic_result.db ../../Tuffy/DB_Files/strange_magic.db >> accuracies.txt

# Robin
# paint it black
printf "\n****Paint it Black Test****\n" >> accuracies.txt
python3 ../../Util/split.py ../../Tuffy/DB_Files/paint_it_black.db ../DB_Files/testr.db ../DB_Files/testl.db
python3 ../Inference/right_annotation.py >> ../Results/paint_it_black.txt
printf "Paint it Black Test Right:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputr.db ../../Tuffy/DB_Files/paint_it_black.db >> accuracies.txt
python3 ../Inference/left_annotation.py >> ../Results/paint_it_black.txt
printf "Paint it Black Test Left:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputl.db ../../Tuffy/DB_Files/paint_it_black.db >> accuracies.txt
printf "Paint it Black Test Overall:\n" >> accuracies.txt
cat ../Results/outputl.db ../Results/outputr.db > ../Results/paint_it_black_result.db
python3 ../../Util/accuracy_test.py ../Results/paint_it_black_result.db ../../Tuffy/DB_Files/paint_it_black.db >> accuracies.txt

# westworld
printf "\n****Westworld Test****\n" >> accuracies.txt
python3 ../../Util/split.py ../../Tuffy/DB_Files/westworld.db ../DB_Files/testr.db ../DB_Files/testl.db
python3 ../Inference/right_annotation.py >> ../Results/westworld.txt
printf "Westworld Test Right:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputr.db ../../Tuffy/DB_Files/westworld.db >> accuracies.txt
python3 ../Inference/left_annotation.py >> ../Results/westworld.txt
printf "Westworld Test Left:\n" >> accuracies.txt
python3 ../../Util/accuracy_test.py ../Results/outputl.db ../../Tuffy/DB_Files/westworld.db >> accuracies.txt
printf "Westworld Test Overall:\n" >> accuracies.txt
cat ../Results/outputl.db ../Results/outputr.db > ../Results/westworld_result.db
python3 ../../Util/accuracy_test.py ../Results/westworld_result.db ../../Tuffy/DB_Files/westworld.db >> accuracies.txt


