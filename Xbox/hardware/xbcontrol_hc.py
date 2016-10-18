from ScopeFoundry import HardwareComponent
from equipment.xbcontrol_ec import XboxControl_EC


class XboxControl_HC(HardwareComponent):

    name = "xbcontrol_hc"

    def setup(self):
        """Create logged quantities for each HID object including all hats, 
        sticks and buttons specific to the Xbox controller."""
        self.ls_lr = self.settings.New(name='Axis_0', initial=0,
                                            dtype=float, fmt="%.3f", 
                                            ro=True, vmin=-1.0, vmax=1.0)
        self.ls_ud = self.settings.New(name='Axis_1', initial=0,
                                            dtype=float, fmt="%.3f", 
                                            ro=True, vmin=-1.0, vmax=1.0)
        self.triggers = self.settings.New(name='Axis_2', initial=0,
                                            dtype=float, fmt="%.3f", 
                                            ro=True, vmin=-1.0, vmax=1.0)
        self.rs_ud = self.settings.New(name='Axis_3', initial=0,
                                            dtype=float, fmt="%.3f", 
                                            ro=True, vmin=-1.0, vmax=1.0)
        self.rs_lr = self.settings.New(name='Axis_4', initial=0,
                                            dtype=float, fmt="%.3f", 
                                            ro=True, vmin=-1.0, vmax=1.0)
        
        self.A = self.settings.New(name='A', initial=0,
                                            dtype=bool, ro=True)
        self.B = self.settings.New(name='B', initial=0,
                                            dtype=bool, ro=True)
        self.X = self.settings.New(name='X', initial=0,
                                            dtype=bool, ro=True)
        self.Y = self.settings.New(name='Y', initial=0,
                                            dtype=bool, ro=True)
        self.LB = self.settings.New(name='LB', initial=0,
                                            dtype=bool, ro=True)
        self.RB = self.settings.New(name='RB', initial=0,
                                    dtype=bool, ro=True)
        self.Back = self.settings.New(name='Back', initial=0,
                                    dtype=bool, ro=True)
        self.Start = self.settings.New(name="Start", initial=0,
                                    dtype=bool, ro=True)
        self.LP = self.settings.New(name="LP", initial=0,
                                    dtype=bool, ro=True)
        self.RP = self.settings.New(name="RP", initial=0,
                                    dtype=bool, ro=True)
        
        self.N = self.settings.New(name='N', initial=0,
                                    dtype=bool, ro=True)
        self.NW = self.settings.New(name='NW', initial=0,
                                    dtype=bool, ro=True)
        self.W = self.settings.New(name='W', initial=0,
                                    dtype=bool, ro=True)
        self.SW = self.settings.New(name='SW', initial=0,
                                    dtype=bool, ro=True)
        self.S = self.settings.New(name='S', initial=0,
                                    dtype=bool, ro=True)
        self.SE = self.settings.New(name='SE', initial=0,
                                    dtype=bool, ro=True)
        self.E = self.settings.New(name='E', initial=0,
                                    dtype=bool, ro=True)
        self.NE = self.settings.New(name='NE', initial=0, 
                                    dtype=bool, ro=True)
        self.origin = self.settings.New(name='Origin', initial=0,
                                    dtype=bool, ro=True)
        
        ## This logged quantity is meant to display the name of the connected controller.
        self.controller_name = self.settings.New(name="Controller_Name", initial="None",
                                    dtype=str, ro=True)
        
    def connect(self):
        """Creates joystick object and connects to controller upon clicking "connect" in ScopeFoundry app."""
        # Reference to equipment level joystick object
        self.joystick = XboxControl_EC().joystick
        XboxControl_EC().connect()
        
    def disconnect(self):
        """Disconnects and removes modules when no longer needed by the application."""
        self.dev.disconnect()
        # delete object
        del self.dev
        
    

        