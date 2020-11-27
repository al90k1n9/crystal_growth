
plot "w_vs_t_(80,200,100)" u ($1/80**alpha):($2/80**alpha) title "L=80"
replot "w_vs_t_(90,200,100)" u ($1/90**alpha):($2/90**alpha) title "L=90"
replot "w_vs_t_(100,200,100)" u ($1/100**alpha):($2/100**alpha) title "L=100"
replot "w_vs_t_(120,300,100)" u ($1/120**alpha):($2/120**alpha) title "L=120"
replot "w_vs_t_(150,200,100)" u ($1/150**alpha):($2/150**alpha) title "L=150"
set logscale xy
set title "Width vs time for different dimensions L"
set xlabel "t"
set ylabel "w"
set term png size 1200,900
set output "/home/algoking/Documents/M2/Crystal_growth/results/comp.png"
rep
