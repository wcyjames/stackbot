from ScopeFoundry import BaseMicroscopeApp

import logging
logging.basicConfig(level='DEBUG')
logging.getLogger('').setLevel(logging.WARNING)
logging.getLogger("ipykernel").setLevel(logging.WARNING)
logging.getLogger('PyQt4').setLevel(logging.WARNING)
logging.getLogger('PyQt5').setLevel(logging.WARNING)
logging.getLogger('traitlets').setLevel(logging.WARNING)

#logging.getLogger('ScopeFoundry.logged_quantity.LoggedQuantity').setLevel(logging.WARNING)

class PressureLogApp(BaseMicroscopeApp):
    '''
    stand alone app for pressure monitoring, will later use C-9215 for logging
    independent of x-series board
    '''
    name = 'PressureLogApp'
    
    def setup(self):
                 
        # SEM Hardware Components


        # Measurements
                
        from Auger.measurement.auger_pressure_history import AugerPressureHistory
        self.add_measurement_component(AugerPressureHistory(self))

        self.settings_load_ini('pressure_log_app_settings.ini')

        self.ui.show()
        
        
if __name__ == '__main__':
    app = PressureLogApp([])
    app.exec_()
