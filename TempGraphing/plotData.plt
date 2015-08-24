reset 
set datafile separator ","
set term png
set xdata time
set timefmt "%Y-%m-%d %H:%M:%S"
set format x "%b %d %H:%M"
set xtics rotate by -45
set xlabel ""
set ylabel "Temperature (C)"
set ytics nomirror
set output "dataTemp.png"
set key left

plot "tempLog.dat" using 1:3 title "Room Temperature" with lines axes x1y1
