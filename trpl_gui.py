import sys
from PySide import QtGui

from base_gui import BaseMicroscopeGUI
from hardware_components.picoharp import PicoHarpHardwareComponent
from hardware_components.apd_counter import APDCounterHardwareComponent
from hardware_components.andor_ccd import AndorCCDHardwareComponent
from hardware_components.acton_spec import ActonSpectrometerHardwareComponent
from hardware_components.flip_mirror import FlipMirrorHardwareComponent
from hardware_components.thorlabs_powermeter import ThorlabsPowerMeter 
from hardware_components.oceanoptics_spec import OceanOpticsSpectrometerHC
from hardware_components.mcl_xyz_stage import MclXYZStage
from hardware_components.keithley_sourcemeter import KeithleySourceMeterComponent
from hardware_components.srs_lockin import SRSLockinComponent
from hardware_components.thorlabs_optical_chopper import ThorlabsOpticalChopperComponent
from hardware_components.power_wheel_arduino import PowerWheelArduinoComponent
from hardware_components.crystaltech_aotf import CrystalTechAOTF
from hardware_components.shutter_servo_arduino import ShutterServoHardwareComponent

from measurement_components.ple import PLEPointMeasurement, PLE2DScanMeasurement
from measurement_components.trpl import \
    PicoHarpMeasurement, PicoHarpPowerWheelMeasurement, \
    TRPLScanMeasurement, TRPLScan3DMeasurement
from measurement_components.apd_confocal import APDOptimizerMeasurement, APDConfocalScanMeasurement, APDConfocalScan3DMeasurement
from measurement_components.andor_ccd_readout import AndorCCDReadout, AndorCCDReadBackground, AndorCCDReadSingle
from measurement_components.hyperspectral import SpectrumScan2DMeasurement
from measurement_components.power_scan import PowerScanContinuous
from measurement_components.photocurrent_scan import \
    Photocurrent2DMeasurement, Photocurrent3DMeasurement
from measurement_components.photocurrent_iv import PhotocurrentIVMeasurement
from measurement_components.power_scan import PowerScanMotorized
from measurement_components.oo_spec import OOSpecLive

class TRPLMicroscopeGUI(BaseMicroscopeGUI):
    
    ui_filename = "trpl_gui.ui"
    
    def setup(self):
        #Add hardware components
        print "Adding Hardware Components"
        
        self.picoharp_hc = self.add_hardware_component(PicoHarpHardwareComponent(self))
        self.apd_counter_hc = self.add_hardware_component(APDCounterHardwareComponent(self))
        self.andor_ccd_hc = self.add_hardware_component(AndorCCDHardwareComponent(self))
        self.acton_spec_hc = self.add_hardware_component(ActonSpectrometerHardwareComponent(self))
        self.flip_mirror_hc = self.add_hardware_component(FlipMirrorHardwareComponent(self))
        self.thorlabs_powermeter_hc = self.add_hardware_component(ThorlabsPowerMeter(self))
        self.mcl_xyz_stage_hc = self.add_hardware_component(MclXYZStage(self))
        self.keithley_sourcemeter_hc = self.add_hardware_component(KeithleySourceMeterComponent(self))
        self.srs_lockin_hc = self.add_hardware_component(SRSLockinComponent(self))  
        self.thorlabs_optical_chopper_hc = self.add_hardware_component(ThorlabsOpticalChopperComponent(self))        
        self.power_wheel_arduino_hc = self.add_hardware_component(PowerWheelArduinoComponent(self))    
        self.oceanoptics_spec_hc = self.add_hardware_component(OceanOpticsSpectrometerHC(self))
        self.crystaltech_aotf_hc = self.add_hardware_component(CrystalTechAOTF(self))
        self.shutter_servo_hc = self.add_hardware_component(ShutterServoHardwareComponent(self))
                      
        #Add measurement components
        print "Create Measurement objects"
        self.apd_optimizer_measure = self.add_measurement_component(APDOptimizerMeasurement(self))
        self.apd_scan_measure = self.add_measurement_component(APDConfocalScanMeasurement(self))
        self.apd_scan3d_measure = self.add_measurement_component(APDConfocalScan3DMeasurement(self))
        #self.ple_point_measure = self.add_measurement_component(PLEPointMeasurement(self))
        #self.ple2d_measure = self.add_measurement_component(PLE2DScanMeasurement(self))
        self.picoharp_measure = self.add_measurement_component(PicoHarpMeasurement(self))
        self.trpl_scan_measure = self.add_measurement_component(TRPLScanMeasurement(self))
        self.trpl_scan3d_measure = self.add_measurement_component(TRPLScan3DMeasurement(self))
        self.andor_ro_measure = self.add_measurement_component(AndorCCDReadout(self))
        self.andor_bg_measure = self.add_measurement_component(AndorCCDReadBackground(self))
        self.andor_single_measure = self.add_measurement_component(AndorCCDReadSingle(self))
        self.spec_map_measure = self.add_measurement_component(SpectrumScan2DMeasurement(self))
        self.power_scan_measure = self.add_measurement_component(PowerScanContinuous(self))
        self.photocurrent2D_measure = self.add_measurement_component(Photocurrent2DMeasurement(self))
        self.photocurrent3D_measure = self.add_measurement_component(Photocurrent3DMeasurement(self))
        self.photocurrent_iv_measure = self.add_measurement_component(PhotocurrentIVMeasurement(self))        
        self.picoharp_power_wheel_measure = self.add_measurement_component(PicoHarpPowerWheelMeasurement(self))
        self.motorized_power_wheel_measure = self.add_measurement_component(PowerScanMotorized(self))
        self.oo_spec_live_measure = self.add_measurement_component(OOSpecLive(self))
 
        #Add additional logged quantities

        # Connect to custom gui



if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    app.setApplicationName("TRPL Microscope Control Application")
    
    gui = TRPLMicroscopeGUI()
    gui.show()
    
    sys.exit(app.exec_())