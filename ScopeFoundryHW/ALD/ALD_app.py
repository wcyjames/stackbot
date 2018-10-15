'''
Created on Nov 20, 2017

@author: Alan Buckley <alanbuckley@berkeley.edu>
                      <alanbuckley@lbl.gov>
'''

from ScopeFoundry.base_app import BaseMicroscopeApp

# logging.disable(50)



class ALD_App(BaseMicroscopeApp):
    
    """
    This ALD app was written to control a custom Atomic Layer Deposition system. 
    Individual modules were written completely independently of one another and 
    can be swapped out with other ScopeFoundry modules, depending on what the 
    user may need for their setup.
    
    *IMPORTANT:* :class:`ALD_Recipe` must be loaded before :class:`ALD_Display`
    because the classes are mutually independent and all resources must be loaded 
    in the correct order for successful application loading.
    
    
    +-------------------+----------------------------+------------------------------------+
    | Module Type       | Physical Device Name       |    Description                     |
    +===================+============================+====================================+
    | Hardware          | Seeed Relay Shield         | Relay controlling pulse valve      |
    |                   | + Arduino Uno              | actuation                          |
    |                   +----------------------------+------------------------------------+
    |                   | J.A. Woollam Ellipsometer  | Ellipsometer                       |
    |                   +----------------------------+------------------------------------+
    |                   | Love Controls 4B (Dwyer)   | Temperature controller             |
    |                   +----------------------------+------------------------------------+
    |                   | MKS 146                    | Multi-purpose Controller           |
    |                   |                            | (Used for Mass Flow Controller)    |
    |                   +----------------------------+------------------------------------+
    |                   | MKS 600                    | Throttle valve pressure            |
    |                   |                            | controller                         |
    |                   +----------------------------+------------------------------------+
    |                   | Pfeiffer MaxiGauge         | Compact Gauge measurement and      |
    |                   | TPG 256 A                  | control unit                       |
    +-------------------+----------------------------+------------------------------------+
    | Measurement       | Seeed Relay Shield         | Relay controlling pulse valve      |
    |                   | + Arduino Uno              | actuation                          |
    |                   +----------------------------+------------------------------------+
    |                   | J.A. Woollam Ellipsometer  | Ellipsometer                       |
    |                   +----------------------------+------------------------------------+
    |                   | Love Controls 4B (Dwyer)   | Temperature controller             |
    |                   +----------------------------+------------------------------------+
    |                   | MKS 146                    | Multi-purpose Controller           |
    |                   |                            | (Used for Mass Flow Controller)    |
    |                   +----------------------------+------------------------------------+
    |                   | MKS 600                    | Throttle valve pressure            |
    |                   |                            | controller                         |
    |                   +----------------------------+------------------------------------+
    |                   | Pfeiffer MaxiGauge         | Compact Gauge measurement and      |
    |                   | TPG 256 A                  | control unit                       |
    +-------------------+----------------------------+------------------------------------+
    
    +-------------------+----------------------------+------------------------------------+
    | Module Type       | Module Name                | Description                        |
    +===================+============================+====================================+
    | Measurement       | ALD Display                | Renders app UI. Plots sensor time  |
    |                   |                            | histories.                         |
    |                   +----------------------------+------------------------------------+
    |                   | ALD Recipe                 | Carries out Atomic Layer Deposition|
    |                   |                            | procedure.                         |
    +-------------------+----------------------------+------------------------------------+
    
    **Important:** Proper loading of :class:`ALD Recipe` and :class:`ALD Display` procedure at app level. Modules must be loaded in this order since modules 
    are co-dependent and were written separately for the sake of organization.
    
    .. highlight:: python
    .. code-block:: python

        from ScopeFoundry.base_app import BaseMicroscopeApp

        class ALD_App(BaseMicroscopeApp):
    
            from ScopeFoundryHW.ALD.ALD_recipes.ALD_recipe import ALD_Recipe
            self.recipe_measure = self.add_measurement(ALD_Recipe(self))
            
            from ScopeFoundryHW.ALD.ALD_recipes.ALD_display import ALD_Display
            self.display_measure = self.add_measurement(ALD_Display(self)).start()
            
            self.recipe_measure.load_display_module()

        if __name__ == '__main__':
        import sys
        app = ALD_App(sys.argv)
        sys.exit(app.exec_()) 
    
    """
    
    name="ald_app"
    
    def setup(self):
        
        from ScopeFoundryHW.ALD.ALD_relay.ald_relay_hardware import ALDRelayHW
        relay = self.add_hardware(ALDRelayHW(self))
        relay.settings['connected'] = True
        
        from ScopeFoundryHW.ALD.ALD_shutter.ALD_shutter import ALD_Shutter
        self.add_hardware(ALD_Shutter(self)).settings['connected'] = True
        
        from ScopeFoundryHW.ALD.ellipsometer.ellipsometer_hw import EllipsometerHW
        self.add_hardware(EllipsometerHW(self)).settings['connected'] = True
        
        from ScopeFoundryHW.ALD.Lovebox.lovebox_hw import LoveboxHW
        self.add_hardware(LoveboxHW(self)).settings['connected'] = True
        
        from ScopeFoundryHW.ALD.MKS_146.mks_146_hw import MKS_146_Hardware
        self.add_hardware(MKS_146_Hardware(self)).settings['connected'] = True
         
        from ScopeFoundryHW.ALD.MKS_600.mks_600_hw import MKS_600_Hardware
        self.add_hardware(MKS_600_Hardware(self)).settings['connected'] = True
        
        from ScopeFoundryHW.ALD.pfeiffer_vgc.pfeiffer_vgc_hw import Pfeiffer_VGC_Hardware
        self.add_hardware(Pfeiffer_VGC_Hardware(self)).settings['connected'] = True
          
        from ScopeFoundryHW.ALD.Seren.seren_hw import Seren_HW
        self.add_hardware(Seren_HW(self)).settings['connected'] = True
        
        from ScopeFoundryHW.ALD.ALD_relay.ald_relay_measure import ALDRelayMeasure
        self.add_measurement(ALDRelayMeasure(self)).start()
        
        from ScopeFoundryHW.ALD.ellipsometer.ellipsometer_measure import Ellipsometer_Measure
        self.add_measurement(Ellipsometer_Measure(self)).start()
          
        from ScopeFoundryHW.ALD.Lovebox.lovebox_measure import LoveboxMeasure
        self.add_measurement(LoveboxMeasure(self)).start()
        
        from ScopeFoundryHW.ALD.MKS_146.mks_146_measure import MKS_146_Measure
        self.add_measurement(MKS_146_Measure(self)).start()
        
        from ScopeFoundryHW.ALD.MKS_600.mks_600_measure import MKS_600_Measure
        self.add_measurement(MKS_600_Measure(self)).start()
         
        from ScopeFoundryHW.ALD.pfeiffer_vgc.pfeiffer_vgc_measure import Pfeiffer_VGC_Measure
        self.add_measurement(Pfeiffer_VGC_Measure(self)).start()
        
        from ScopeFoundryHW.ALD.Seren.seren_measure import Seren
        self.add_measurement(Seren(self)).start()

        from ScopeFoundryHW.ALD.ALD_recipes.ALD_recipe import ALD_Recipe
        self.recipe_measure = self.add_measurement(ALD_Recipe(self))
        
        from ScopeFoundryHW.ALD.ALD_recipes.ALD_display import ALD_Display
        self.display_measure = self.add_measurement(ALD_Display(self)).start()
        
        self.recipe_measure.load_display_module()




if __name__ == '__main__':
    import sys
    app = ALD_App(sys.argv)
    sys.exit(app.exec_()) 