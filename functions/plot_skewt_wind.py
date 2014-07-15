# -*- coding: utf-8 -*-
"""
Created on Wed Jul  2 11:49:54 2014

The function takes in pressure, height, temperature, dew point temperature, both u and v wind components and creates a skewt-log(p) plot with wind barbs. 
It does not calculate thermodynamic variables, but is used for quick glimpse at a sounding file or comparison on python. 

edited by mattjohnson & grantmckercher
"""

def plot_skewt(p,h,T,Td,u,v):
    """
    this code adapted from jhelmus
    """
    # This serves as an intensive exercise of matplotlib's transforms
    # and custom projection API. This example produces a so-called
    # SkewT-logP diagram, which is a common plot in meteorology for
    # displaying vertical profiles of temperature. As far as matplotlib is
    # concerned, the complexity comes from having X and Y axes that are
    # not orthogonal. This is handled by including a skew component to the
    # basic Axes transforms. Additional complexity comes in handling the
    # fact that the upper and lower X-axes have different data ranges, which
    # necessitates a bunch of custom classes for ticks,spines, and the axis
    # to handle this.
    from matplotlib.axes import Axes
    import matplotlib.transforms as transforms
    import matplotlib.axis as maxis
    import matplotlib.spines as mspines
    from matplotlib.projections import register_projection
    
    # The sole purpose of this class is to look at the upper, lower, or total
    # interval as appropriate and see what parts of the tick to draw, if any.
    class SkewXTick(maxis.XTick):
        def draw(self, renderer):
            if not self.get_visible(): return
            renderer.open_group(self.__name__)
    
            lower_interval = self.axes.xaxis.lower_interval
            upper_interval = self.axes.xaxis.upper_interval
    
            if self.gridOn and transforms.interval_contains(
                    self.axes.xaxis.get_view_interval(), self.get_loc()):
                self.gridline.draw(renderer)
    
            if transforms.interval_contains(lower_interval, self.get_loc()):
                if self.tick1On:
                    self.tick1line.draw(renderer)
                if self.label1On:
                    self.label1.draw(renderer)
    
            if transforms.interval_contains(upper_interval, self.get_loc()):
                if self.tick2On:
                    self.tick2line.draw(renderer)
                if self.label2On:
                    self.label2.draw(renderer)
    
            renderer.close_group(self.__name__)
    
    
    # This class exists to provide two separate sets of intervals to the tick,
    # as well as create instances of the custom tick
    class SkewXAxis(maxis.XAxis):
        def __init__(self, *args, **kwargs):
            maxis.XAxis.__init__(self, *args, **kwargs)
            self.upper_interval = 0.0, 1.0
    
        def _get_tick(self, major):
            return SkewXTick(self.axes, 0, '', major=major)
    
        @property
        def lower_interval(self):
            return self.axes.viewLim.intervalx
    
        def get_view_interval(self):
            return self.upper_interval[0], self.axes.viewLim.intervalx[1]
    
    
    # This class exists to calculate the separate data range of the
    # upper X-axis and draw the spine there. It also provides this range
    # to the X-axis artist for ticking and gridlines
    class SkewSpine(mspines.Spine):
        def _adjust_location(self):
            trans = self.axes.transDataToAxes.inverted()
            if self.spine_type == 'top':
                yloc = 1.0
            else:
                yloc = 0.0
            left = trans.transform_point((0.0, yloc))[0]
            right = trans.transform_point((1.0, yloc))[0]
    
            pts  = self._path.vertices
            pts[0, 0] = left
            pts[1, 0] = right
            self.axis.upper_interval = (left, right)
    
    
    # This class handles registration of the skew-xaxes as a projection as well
    # as setting up the appropriate transformations. It also overrides standard
    # spines and axes instances as appropriate.
    class SkewXAxes(Axes):
        # The projection must specify a name.  This will be used be the
        # user to select the projection, i.e. ``subplot(111,
        # projection='skewx')``.
        name = 'skewx'
    
        def _init_axis(self):
            #Taken from Axes and modified to use our modified X-axis
            self.xaxis = SkewXAxis(self)
            self.spines['top'].register_axis(self.xaxis)
            self.spines['bottom'].register_axis(self.xaxis)
            self.yaxis = maxis.YAxis(self)
            self.spines['left'].register_axis(self.yaxis)
            self.spines['right'].register_axis(self.yaxis)
    
        def _gen_axes_spines(self):
            spines = {'top':SkewSpine.linear_spine(self, 'top'),
                      'bottom':mspines.Spine.linear_spine(self, 'bottom'),
                      'left':mspines.Spine.linear_spine(self, 'left'),
                      'right':mspines.Spine.linear_spine(self, 'right')}
            return spines
    
        def _set_lim_and_transforms(self):
            """
            This is called once when the plot is created to set up all the
            transforms for the data, text and grids.
            """
            rot = 30
    
            #Get the standard transform setup from the Axes base class
            Axes._set_lim_and_transforms(self)
    
            # Need to put the skew in the middle, after the scale and limits,
            # but before the transAxes. This way, the skew is done in Axes
            # coordinates thus performing the transform around the proper origin
            # We keep the pre-transAxes transform around for other users, like the
            # spines for finding bounds
            self.transDataToAxes = self.transScale + (self.transLimits +
                    transforms.Affine2D().skew_deg(rot, 0))
    
            # Create the full transform from Data to Pixels
            self.transData = self.transDataToAxes + self.transAxes
    
            # Blended transforms like this need to have the skewing applied using
            # both axes, in axes coords like before.
            self._xaxis_transform = (transforms.blended_transform_factory(
                        self.transScale + self.transLimits,
                        transforms.IdentityTransform()) +
                    transforms.Affine2D().skew_deg(rot, 0)) + self.transAxes
    
    # Now register the projection with matplotlib so the user can select
    # it.
    register_projection(SkewXAxes)
    

    # Now make a simple example using the custom projection.
    from matplotlib.ticker import ScalarFormatter, MultipleLocator
    from matplotlib.collections import LineCollection
    import matplotlib.pyplot as plt
    from StringIO import StringIO
    import numpy as np
    import matplotlib.gridspec as gridspec
        
     
    fig = plt.figure(figsize = [20,15])
    gs = gridspec.GridSpec(1, 2,width_ratios=[5,1])
    
    # Temperature Plot    
    #ax1 = fig.add_subplot(121, projection='skewx')
    ax1 = plt.subplot(gs[0],projection='skewx')
    plt.grid(True)
    ax1.semilogy(T, p, 'r')
    ax1.semilogy(Td, p, 'b')
    ax1.yaxis.set_major_formatter(ScalarFormatter())
    ax1.set_yticks(np.linspace(100,1000,10))
    ax1.set_ylim(1050,100)
    ax1.xaxis.set_major_locator(MultipleLocator(10))
    ax1.set_xlim(-50,50)
    ax1.set_xlabel('Temperature (Celsius)', fontsize=18)
    ax1.set_ylabel('Pressure (hPa)', fontsize=18)
    
    # Wind Profile Plot
    pl = HRRR_PS
    #ax2 = fig.add_subplot(122)
    ax2 = plt.subplot(gs[1])
    # Array for x axis
    a = []
    for i in range(40):
        a.append(0)
    # Convert m/s to knots
    u = u*1.9438444924574
    v = v*1.9438444924574
    # Interpolate if it doesn't match the HRRR dimension
    if (u.size != 40):
        # Interpolate u,v wind to hrrr pressure levels
        u2 = np.interp(pl[::-1],p[::-1],u[::-1])
        v2 = np.interp(pl[::-1],p[::-1],v[::-1])
        u2 = u2[::-1]
        v2 = v2[::-1]
    else:
        u2 = u
        v2 = v 
    # Plot pressure from HRRR
    ax2 = plt.gca()
    ax2.set_yscale('log')
    ax2.set_ylim([1100,min(pl)])
    ax2.set_xlim([0,0])
    # x axis
    xmajorLocator = MultipleLocator(1)
    ax2.xaxis.set_major_locator(xmajorLocator)
    xmajorFormatter = FormatStrFormatter('%d')
    ax2.xaxis.set_major_formatter(xmajorFormatter)
    ax2.set_xlabel('Wind Speed (Knots)', fontsize=18)
    # y axis
    ax2.yaxis.set_major_formatter(ScalarFormatter())
    ax2.set_yticks(np.linspace(100,1000,10))
    ax2.set_ylim(1050,100)
    plt.barbs(a,pl,u2,v2)
    plt.grid()    
    
    plt.show()