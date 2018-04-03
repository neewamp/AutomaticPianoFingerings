#!/bin/bash
treble="${1/.db/"_right.db"}"
bass="${1/.db/"_left.db"}"
python3 split.py $1

cat $treble ../fingering.db ../keys.db| grep -v Finger > ../../Test_DB/testr.db
cat $bass ../fingering.db ../keys.db | grep -v Finger > ../../Test_DB/testl.db

rm $treble
rm $bass
