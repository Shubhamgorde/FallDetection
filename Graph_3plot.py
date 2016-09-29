import matplotlib.pyplot as plt
plt.ion()
class DynamicUpdate():
    #Range of x axis
    min_x = 0
    max_x = 100

    def on_launch(self):
        #Set up plot
        self.figure, self.ax = plt.subplots()
        self.lines, = self.ax.plot([],[], 'r-',marker='o',label='x')
        self.lines1, = self.ax.plot([],[], 'g-',marker='*',label='y')
        self.lines2, = self.ax.plot([],[], 'b-',marker='+',label='z')
        self.ax.legend()
        #self.lines3, = self.ax.plot([],[],'y-')     ##remove if error
        #self.lines4, = self.ax.plot([],[],'v-')
        #self.lines5, = self.ax.plot([],[],'r-')

        #Autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on(True)

        #self.ax.set_xlim(self.min_x, self.max_x)
        #self.ax.set_autoscalex_on(True)
        #Other stuff
        self.ax.grid()


    def on_running_x(self, xdata, x,y,z): #add y_est and z_est for y and z
        self.ax.set_xlim(self.min_x, self.max_x)
        #Update data (with the new _and_ the old points)
        self.lines.set_xdata(xdata)
        self.lines.set_ydata(x)
        self.lines1.set_xdata(xdata)
        self.lines1.set_ydata(y)
        self.lines2.set_xdata(xdata)
        self.lines2.set_ydata(z)
        '''
        self.lines4.set_xdata(xdata)
        self.lines4.set_ydata(y_est)
        self.lines5.set_xdata(xdata)
        self.lines5.set_ydata(z_est)
        '''

        #Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view()

        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()


    #Example
    def __call__(self):
        import numpy as np
        import time
        self.on_launch()
        xdata = []
        ydata = []
        for x in np.arange(0,10,0.5):
            xdata.append(x)
            ydata.append(np.exp(-x**2)+10*np.exp(-(x-7)**2))
            self.on_running(xdata, ydata)
            time.sleep(1)
        return xdata, ydata

#d = DynamicUpdate()
#d()