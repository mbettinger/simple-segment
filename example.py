from matplotlib.pylab import gca, figure, plot, subplot, title, xlabel, ylabel, xlim,show
from matplotlib.lines import Line2D
import segment
import fit
import sys
def draw_plot(data,plot_title):
    plot(range(len(data)),data,alpha=0.8,color='red')
    title(plot_title)
    xlabel("Samples")
    ylabel("Signal")
    xlim((0,len(data)-1))

def draw_segments(segments):
    ax = gca()
    for segment in segments:
        line = Line2D((segment[0],segment[2]),(segment[1],segment[3]))
        ax.add_line(line)

MIN=int(sys.argv[1]) if len(sys.argv)>1 else 0
MAX=int(sys.argv[2]) if len(sys.argv)>2 else MIN+30
ERROR=float(sys.argv[3]) if len(sys.argv)>3 else 0.1
with open("example_data/bitcoin_2010-8-16_2021-9-8.txt") as f:
    file_lines = f.readlines()

data = [float(x.split("\t")[1].strip())/pow(10,14) for x in file_lines[MIN:MAX]]
print(data)
print(len(data))
max_error = ERROR

#sliding window with regression
figure()
segments = segment.slidingwindowsegment(data, fit.regression, fit.sumsquared_error, max_error)
draw_plot(data,"Sliding window with regression")
draw_segments(segments)
print(len(segments))
print(len(data)/len(segments))
#bottom-up with regression
figure()
segments = segment.bottomupsegment(data, fit.regression, fit.sumsquared_error, max_error)
draw_plot(data,"Bottom-up with regression")
draw_segments(segments)
print(len(segments))
print(len(data)/len(segments))
#top-down with regression
figure()
segments = segment.topdownsegment(data, fit.regression, fit.sumsquared_error, max_error)
draw_plot(data,"Top-down with regression")
draw_segments(segments)
print(len(segments))
print(len(data)/len(segments))


#sliding window with simple interpolation
figure()
segments = segment.slidingwindowsegment(data, fit.interpolate, fit.sumsquared_error, max_error)
draw_plot(data,"Sliding window with simple interpolation")
draw_segments(segments)
print(len(segments))
print(len(data)/len(segments))
#bottom-up with  simple interpolation
figure()
segments = segment.bottomupsegment(data, fit.interpolate, fit.sumsquared_error, max_error)
draw_plot(data,"Bottom-up with simple interpolation")
draw_segments(segments)
print(len(segments))
print(len(data)/len(segments))
#top-down with  simple interpolation
figure()
segments = segment.topdownsegment(data, fit.interpolate, fit.sumsquared_error, max_error)
draw_plot(data,"Top-down with simple interpolation")
draw_segments(segments)
print(len(segments))
print(len(data)/len(segments))

show()

