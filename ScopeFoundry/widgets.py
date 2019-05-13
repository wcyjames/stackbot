'''
Created on Jul 20, 2018

@author: lab
'''

from qtpy import  QtCore, QtWidgets, QtGui
import pyqtgraph as pg
import numpy as np

class MinMaxQSlider(QtWidgets.QWidget):
    """
    Costume QSlider widget designed to work with logged_quantities.
    Two spin boxes allow to dynamically update the min and max value of the slider.
    """
    
    #Signals
    updated_value = QtCore.Signal((float,),(int,))
    
    def __init__(self, name="", spinbox_decimals = 2, **QSlider_kwargs):

        self.name = name
        
        #Setup widget
        QtWidgets.QWidget.__init__(self)
        
        #slider
        self.slider = QtWidgets.QSlider(orientation = QtCore.Qt.Horizontal, **QSlider_kwargs)
        self.slider.valueChanged.connect(self.on_slider_value_changed)
        self.slider.setSingleStep(1)
        self.slider.sliderMoved[int].connect(self.set_title)
        
        #min and max spinbox
        self.min_double_spinbox = QtWidgets.QDoubleSpinBox()
        self.min_double_spinbox.setRange(-1e12, 1e12)
        self.max_double_spinbox = QtWidgets.QDoubleSpinBox()
        self.max_double_spinbox.setRange(-1e12, 1e12)
        
        self.min_double_spinbox.valueChanged[float].connect(self.update_slider_minimum)
        self.max_double_spinbox.valueChanged[float].connect(self.update_slider_maximum)
        
        self.setDecimals(spinbox_decimals)

        #title label
        self.title_label = QtWidgets.QLabel()
        
        #Setup layout
        self.layout_ = QtWidgets.QGridLayout()
        self.layout_.addWidget(self.min_double_spinbox, 0,0, alignment=QtCore.Qt.AlignLeft)
        self.layout_.addWidget(self.title_label, 0,1, alignment = QtCore.Qt.AlignHCenter)
        self.layout_.addWidget(self.max_double_spinbox, 0,2, alignment=QtCore.Qt.AlignRight)    
        self.layout_.addWidget(self.slider, 1,0, 1,3)
        
        self.setLayout(self.layout_)


    def set_name(self,name):
        self.name = name
        val = self.transform_from_slider(self.slider.value())
        self.set_title(val)
        
    @property
    def vmin(self):
        return self.min_double_spinbox.value()
    @property
    def vmax(self):
        return self.max_double_spinbox.value()
    @property
    def vrange(self):
        return self.vmax-self.vmin
        
    def transform_to_slider(self,x):
        pct = 100*(x-self.vmin)/self.vrange
        return int(pct)
    
    def transform_from_slider(self,x):
        val = self.vmin + (x*self.vrange/100)
        return val
        
    def update_min_double_spinbox(self, vmin):
        try:
            self.min_double_spinbox.blockSignals(True)
            self.min_double_spinbox.setValue(vmin)
        finally:
            self.min_double_spinbox.blockSignals(False)   
                     
    def update_max_double_spinbox(self, vmax):        
        try:
            self.max_double_spinbox.blockSignals(True)
            self.max_double_spinbox.setValue(vmax)
        finally:
            self.max_double_spinbox.blockSignals(False)
        
    def update_slider_minimum(self, vmin):
        val = self.slider.sliderPosition()
        self.slider.setMinimum(self.transform_to_slider(vmin))
        self.slider.setSliderPosition(val)
    def update_slider_maximum(self, vmax):
        self.slider.setMaximum(self.transform_to_slider(vmax))
        
    def update_value(self,x):
        try:
            self.slider.blockSignals(True)
            self.slider.setValue(self.transform_to_slider(x))
        finally:
            self.slider.blockSignals(False) 
        
    def on_slider_value_changed(self):
        val = self.transform_from_slider(self.slider.value())
        self.updated_value.emit(val)

    def setRange(self, vmin, vmax):
        # as it is currently used in LoggedQuantity.change_min_max()
        self.update_min_double_spinbox(vmin)
        self.update_max_double_spinbox(vmax)
        
    def setDecimals(self,decimals):
        self.min_double_spinbox.setDecimals(decimals)
        self.max_double_spinbox.setDecimals(decimals)
        
    def setSuffix(self,unit):
        self.min_double_spinbox.setSuffix(" "+unit)
        self.max_double_spinbox.setSuffix(" "+unit)

    def setSingleStep(self, spinbox_step):
        self.min_double_spinbox.setSingleStep(spinbox_step)
        self.max_double_spinbox.setSingleStep(spinbox_step)
        
    def set_title(self, val):
        val = self.transform_from_slider(val)
        text =self.name+" "+str(val)
        self.title_label.setText(text)

        
class RegionSlicer(QtWidgets.QWidget):
    '''
    **Bases:** :class: `QWidget <pyqt.QtWidgets.QWidget>`
    
    Adds a movable <pyqtgraph.LinearRegionItem> to a plot.
    Provides a numpy slice and mask that would slices the x_array within the region.
    
    ===============================  =============================================================================
    **Signals:**
    region_changed_signal()          Emitted when region is changed or activated by user
    ===============================  =============================================================================
    '''
    
    region_changed_signal = QtCore.Signal()
    
    def __init__(self, plot_item, x_array=None, name='array_slicer_name',
                 slicer_updated_func=lambda:None,  
                 initial=[0,100], 
                 brush=QtGui.QColor(0,255,0,70), ZValue=10, 
                 font=QtGui.QFont("Times", 12), label_line=1, activated=False):
        """Create a new LinearRegionItem on plot_item.
        
        ====================== ==============================================================
        **Arguments:**
        plot_item              <pyqtgraph.PlotDataItem> (recommended) 
                                or <pyqtgraph.PlotItem>  (does not grab x_array data from plot
                                item: initialize x_array manually
                                or use :func:`set_x_array <self.set_x_array>`)
        x_array                initializes x_array. 
        name                   <str> 
        slicer_updated_func    gets called when region is updated, alternatively use 
                               :sig:region_changed_signal().
        initial                [start_idx, stop_idx] of the slice
        brush,ZValue,          are passed to the LinearRegionItem
        font,                  passed to the label
        label_line             '0' or '1' for placement of label onto 'left' or 'right'
                               bounding line. 
        activated              <bool> state at initialization
        ====================== ==============================================================
        """
        QtWidgets.QWidget.__init__(self)        

        self.name = name
        
        from ScopeFoundry.logged_quantity import LQCollection
        self.settings = LQCollection()
        self.start = self.settings.New('start', int, initial=initial[0], vmin = 0)
        self.stop = self.settings.New('stop', int, initial=initial[1], vmin = 0)
        self.activated = self.settings.New('activated', bool, initial = activated)
        self.start.add_listener(self.on_change_start_stop)
        self.stop.add_listener(self.on_change_start_stop)
        self.activated.add_listener(self.on_change_activated)
        
        if  type(plot_item) == pg.PlotDataItem:
            self.plot_data_item = plot_item
            self.plot_data_item.sigPlotChanged.connect(self.set_x_array_from_data_data_item)
            self.parent_plot_item = plot_item.parentItem()
        elif type(plot_item) == pg.PlotItem:                
            self.plot_data_item = None
            self.parent_plot_item = plot_item

        self.linear_region_item = pg.LinearRegionItem(brush = brush)
        self.linear_region_item.setZValue(ZValue)                         
        self.parent_plot_item.addItem(self.linear_region_item)
        self.linear_region_item.sigRegionChangeFinished.connect(self.on_change_region)
        
        self.inf_line_label = pg.InfLineLabel(self.linear_region_item.lines[label_line],
                                              self.name, position=0.78, anchor=(0.5, 0.5))
        self.inf_line_label.setFont(font)
        self.set_label('')
        
        if x_array == None: #give it something to work with.
            x_array = np.arange(512)
        self.set_x_array(x_array)
        
        self.slicer_updated = slicer_updated_func
                
    
    @QtCore.Slot(object)
    def set_x_array_from_data_data_item(self):
        print('set_x_array_from_data_data_item')
        self.x_array,_ = self.plot_data_item.getData()
        self.apply_new_x_array()
    
    def set_x_array(self, x_array):
        '''
        use this function to update the x_array
        not required to use if type(plot_item) == pg.PlotDataItem
        '''
        self.x_array = x_array
        self.apply_new_x_array()
        
    def apply_new_x_array(self):
        self.linear_region_item.setBounds( [self.x_array.min(), self.x_array.max()] )
        kk_max = len(self.x_array)
        self.start.change_min_max(0, kk_max)
        self.stop.change_min_max(0, kk_max)
        if self.start.val > kk_max:
            self.start.update_value(kk_max)
        if self.stop.val > kk_max:
            self.stop.update_value(kk_max)
        self.on_change_start_stop()
        
    @property
    def slice(self):
        return np.s_[ self.settings['start'] : self.settings['stop'] ]
    
    @property
    def s(self):
        '''returns an activation sensitive slice'''
        if self.activated.val:
            return self.slice
        else:
            return np.s_[:]
        
    @property
    def mask(self):
        if self.activated.val:
            return (self.x_array >= self.region_min) * (self.x_array <= self.region_max)
        else:
            return np.ones_like(self.x_array, dtype=bool)       
    
    @QtCore.Slot(object)
    def on_change_region(self):
        '''
        updates settings based on region 
        '''
        print(self.name, 'on_change_region')
        self.region_min, self.region_max = mn,mx = self.linear_region_item.getRegion()
        self.settings['start'] = np.argmin( (self.x_array - mn)**2 )
        self.settings['stop'] = np.argmin( (self.x_array - mx)**2 )
        self.region_changed_signal.emit()
        self.slicer_updated()
        
    def on_change_start_stop(self):
        '''
        updates linear_region_item based on settings 
        '''
        rgn = [0,0]
        rgn[0] = self.x_array[ self.settings['start'] ]
        try:
            rgn[1] = self.x_array[ self.settings['stop'] ]
        except IndexError:
            rgn[1] = self.x_array[ self.settings['start'] ]
        self.linear_region_item.setRegion(rgn)    
        
    def on_change_activated(self):
        activated = self.activated.val
        self.linear_region_item.setEnabled(activated)
        self.linear_region_item.setAcceptHoverEvents(activated)
        self.linear_region_item.setAcceptTouchEvents(activated)
        if activated:
            opacity = 1
        else:
            opacity = 0
        self.linear_region_item.setOpacity(opacity)
        self.region_changed_signal.emit()
        self.slicer_updated()
        
    def New_UI(self):
        ui_widget = self.settings.New_UI()
        ui_widget.layout().insertRow(0, QtWidgets.QLabel("<b>{}</b>".format(self.name)) )        
        return ui_widget
        
    def set_label(self, text='', title=None, color=(200,200,200)):
        if title == None:
            title = self.name
        label = '<h3>{}</h3>{}'.format(title, text)
        self.inf_line_label.setHtml(label)
        self.inf_line_label.setColor(color)