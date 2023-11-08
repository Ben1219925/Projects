#!/usr/bin/env -S gnuplot -persist
set key top right
plot '../test/data.csv' with lines linetype 1, '../build/data_a.out' with lines linetype 2, '../build/data_b.out' with lines linetype 3
