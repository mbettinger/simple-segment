from matplotlib.pylab import gca, figure, plot, subplot, title, xlabel, ylabel, xlim,show
from matplotlib.lines import Line2D
import segment
import fit
import sys

from numpy import array
def draw_plot(data,plot_title):
    plot(data[:,0],data[:,1],alpha=0.8,color='red')
    title(plot_title)
    xlabel("Samples")
    ylabel("Signal")
    xlim((data[:,0][0],data[:,0][-1]))

def draw_segments(segments,ticks):
    segments=[(x1,y1,x21,y21) for x,(x1,y1),x2,(x21,y21),err in segments]
    ax = gca()
    ax.set_xticklabels(ticks, rotation=20)
    for segment in segments:
        line = Line2D((segment[0],segment[2]),(segment[1],segment[3]))
        ax.add_line(line)

def wrapOrchestration(title, labels, data, segment_algo, create_segment, compute_error, max_error):
    figure()
    segments = segment_algo(data, create_segment, compute_error, max_error)
    draw_plot(data,title)
    draw_segments(segments,labels)
    print(len(segments))
    print(len(data)/len(segments))
    name=title.split()[0][:3]+title.split()[-1][:3]
    with open(f"./output/{name}_{labels[0]}_{labels[-1]}_{max_error}.txt","w") as file:
        for xbeg, (x0,y0), xend, (x1,y1), err in segments:
            file.write(f"{labels[xbeg]}\t{x0}\t{y0}\n")
            file.write(f"{labels[xend]}\t{x1}\t{y1}\t{err}\n")


MIN=int(sys.argv[1]) if len(sys.argv)>1 else 0
MAX=int(sys.argv[2]) if len(sys.argv)>2 else MIN+30
ERROR=float(sys.argv[3]) if len(sys.argv)>3 else 0.1
with open("example_data/bitcoin_2010-8-16_2021-9-8.txt") as f:
    file_lines = f.readlines()

data = [tuple(x.split("\t")[1:3]) for x in file_lines[MIN:MAX]]
labels = [x.split("\t")[0] for x in file_lines[MIN:MAX]]
data = array([(float(x),float(y.strip())/pow(10,14)) for x,y in data])
max_error = ERROR

#sliding window with regression 
wrapOrchestration("Sliding window with regression",labels,data,segment.slidingwindowsegment, fit.regression, fit.sumsquared_error, max_error)
#bottom-up with regression
wrapOrchestration("Bottom-up with regression",labels,data,segment.bottomupsegment,fit.regression, fit.sumsquared_error, max_error)
#top-down with regression
wrapOrchestration("Top-down with regression",labels,data,segment.topdownsegment,fit.regression, fit.sumsquared_error, max_error)

#sliding window with simple interpolation
wrapOrchestration("Sliding window with simple interpolation",labels,data,segment.slidingwindowsegment, fit.interpolate, fit.sumsquared_error, max_error)
#bottom-up with  simple interpolation
wrapOrchestration("Bottom-up with simple interpolation",labels,data,segment.bottomupsegment,fit.interpolate, fit.sumsquared_error, max_error)
#top-down with  simple interpolation
wrapOrchestration("Top-down with simple interpolation",labels,data,segment.topdownsegment,fit.interpolate, fit.sumsquared_error, max_error)

show()

