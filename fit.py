from wrappers import leastsquareslinefit
import math
# compute_error functions

def sumsquared_error(sequence, segment):
    """Return the sum of squared errors for a least squares line fit of one segment of a sequence"""
    x0,(xa0,ya0),x1,(xa1,ya1), err = segment
    datapoints=sequence[x0:x1+1]
    progress=[(x,(x-xa0)/(xa1-xa0)) for x,y in datapoints]
    approxPoints=[(x,(1-prog)*ya0+prog*ya1) for x,prog in progress]
    assert(len(datapoints)==len(approxPoints))
    error=math.sqrt(sum([(ya-datapoints[index][1])**2 for index,(xa,ya) in enumerate(approxPoints)]))
    #p, error = leastsquareslinefit(sequence,(x0,x1))
    return error
    
# create_segment functions

def regression(sequence, seq_range):
    """Return (x0,y0,x1,y1) of a line fit to a segment of a sequence using linear regression"""
    p, error = leastsquareslinefit(sequence,seq_range)
    y0 = p[0]*sequence[seq_range[0]][0] + p[1]
    y1 = p[0]*sequence[seq_range[1]][0] + p[1]
    return (seq_range[0],(sequence[seq_range[0]][0],y0),seq_range[1],(sequence[seq_range[1]][0],y1), error)
    
def interpolate(sequence, seq_range):
    """Return (x0,y0,x1,y1) of a line fit to a segment using a simple interpolation"""
    segment=(seq_range[0], sequence[seq_range[0]], seq_range[1], sequence[seq_range[1]], 0)
    segment = (*segment[:4],sumsquared_error(sequence,segment))
    return segment
