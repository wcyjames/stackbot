import serial
import threading
import binascii
from collections import OrderedDict
import time

WAIT_TIME = 0.1

def replace_letters(inputstr):
    # output from Lakeshore is offset in hex by a value of ord('a') - 2 
    # this returns the corrected hex digit
    return str(ord(inputstr) - ord('a') + 2)
        
def decode_garbage(garbagein):
    # output from Lakeshore is off by a weird amount. Everything that isn't ASCII
    # is offset in one of its hex digits by ord('a') - 2. This function fixes this by
    # converting to hex and processing the hex representation of each character
    # before returning the corrected string representation
    hline = garbagein.hex()
    #print(hline)
    hline_arr = [hline[i:i+2] for i in range(0, len(hline), 2)]
    asdf = ''
    for kk in hline_arr:
        try: 
            if kk == '0d':
                continue
            this_char = binascii.unhexlify(kk)
            asdf = asdf + this_char.decode('ASCII')
        except Exception as ex:
            #print('not an ascii character')
            if kk == '8a':
                continue
            if kk[0] >= 'a': 
                #print(replace_letters(kk[0]))
                kk = replace_letters(kk[0]) + kk[1]
            else:
                #print(replace_letters(kk[1]))
                kk = kk[0] + replace_letters(kk[1])
            this_char = binascii.unhexlify(kk)
            asdf = asdf + this_char.decode('ASCII')
    return asdf

class Lakeshore331Interface(object):
    
    def __init__(self, port='COM6', debug=False):
        self.port = port
        self.debug = debug
        self.lock = threading.Lock()
        self.ser = serial.Serial(port = self.port,
                        baudrate = 9600,
                        timeout = 1,
                        bytesize = 7,
                        parity = serial.PARITY_ODD,
                        stopbits=1, xonxoff=0, rtscts=0)
        self.ask('*RST')
        self.ask('*CLS')
    
    def info(self):
        resp = self.ask("*IDN?")
        if self.debug: print("Lakeshore 331 Info",resp)
        return resp
    
    def close(self):
        self.ser.close()
    
    def send_cmd(self, cmd):
        self.ser.flush()
        cmd_bytes = (cmd + '\r\n').encode()
        if self.debug: print("Lakeshore 331 cmd: ", repr(cmd), repr(cmd_bytes))
        self.ser.write(cmd_bytes)
        time.sleep(WAIT_TIME)
        if self.debug: print("Lakeshore 331 done sending cmd")    
    
    def read_resp(self):
        self.ser.flush()
        resp = self.ser.readline()
        time.sleep(WAIT_TIME)
        if self.debug: print("Lakeshore 331 resp: ", repr(resp))
        return str(resp, 'ASCII')
    
    def read_T(self, chan='B'):
        resp = self.ask("KRDG? " + chan)
        if resp == '':
            return -1.0
        return float(resp)
        
    def set_output_enabled(self,enable):
        assert isinstance(enable,bool)
        out_dict = self.get_output()
        self.set_output(enable=int(enable==True),
                        chan=out_dict['channel'],
                        vmax=out_dict['max_10V'],
                        vmin=out_dict['min_0V'])
        
    def get_output_enabled(self):
        out_dict = self.get_output()
        return bool(out_dict['enable'])
    
    def set_output_channel(self,chan):
        assert chan == 'A' or chan == 'B'
        out_dict = self.get_output()
        self.set_output(enable=out_dict['enable'],
                        chan=chan,
                        vmax=out_dict['max_10V'],
                        vmin=out_dict['min_0V'])
    
    def get_output_channel(self):
        out_dict = self.get_output()
        return out_dict['channel']
    
    def set_output_vmax(self,vmax):
        out_dict = self.get_output()
        assert vmax > out_dict['min_0V'] and isinstance(vmax,float)
        self.set_output(enable=out_dict['enable'],
                        chan=out_dict['channel'],
                        vmin=out_dict['min_0V'],
                        vmax=vmax)
        
    def get_output_vmax(self):
        return self.get_output()['max_10V']
    
    def set_output_vmin(self,vmin):
        out_dict = self.get_output()
        assert vmin < out_dict['max_10V'] and vmin > 0 and isinstance(vmin,float)
        self.set_output(enable=out_dict['enable'],
                        chan=out_dict['channel'],
                        vmax=out_dict['max_10V'],
                        vmin=vmin)
        
    def get_output_vmin(self):
        return self.get_output()['min_0V']
        
    def set_output(self,enable=1,chan='A',vmax=100.0,vmin=0.0):
        self.ask('ANALOG 0,%d,%s,1,+%0.1f,+%0.1f,+0.0' % (enable, chan, vmax, vmin))
            
    
    def get_output(self):
        resp = self.ask('ANALOG?')
        if self.debug: print(resp)
        if resp == '':
            raise Exception('Error - no output in',resp)
            return None
        else:
            resp = resp.split(sep=',')
            resp_dict = OrderedDict(
                [('bipolar', int(resp[0])),
                ('enable', int(resp[1])),
                ('channel', resp[2]),
                ('max_10V', float(resp[4])),
                ('min_0V', float(resp[5])),
                ('manual', float(resp[6])),])
            if self.debug: 
                print("Lakeshore 331 analog output setup: ")
                for key, value in resp_dict.items():
                    print(key + ' ' + str(value))
            
            return resp_dict 
    
    def ask(self,cmd):
        with self.lock:
            self.send_cmd(cmd)
            return self.read_resp()
    
    def get_heater_range(self):
        return self.ask('RANGE?')
    
    def set_heater_range(self,ind):
        assert isinstance(ind, int) and ind >= 0 and ind <= 3
        self.ask('RANGE %d' % ind)
        if self.debug: print('Lakeshore 331 heater range set to %d sent' % ind)
        
    def get_remote_mode(self):
        return self.ask('MODE?')
    
    def set_remote_mode(self, ind):
        assert isinstance(ind,int) and ind >= 0 and ind <= 2
        self.ask('MODE %d' % ind)
        if self.debug: print('Lakeshore 331 remote mode set to %d sent' % ind)

    #def get_setpoint(self):
    
if __name__ == '__main__':
    tctrl = Lakeshore331Interface(debug=False)
    print(tctrl.info())
    print("T = " + str(tctrl.read_T()) + 'K')
    tctrl.set_output(enable=0,chan='B',vmax=0.0)
    tctrl.get_output()
    tctrl.close()
    