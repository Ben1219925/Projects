# Clock signal
set_property PACKAGE_PIN W5 [get_ports clk]							
	set_property IOSTANDARD LVCMOS33 [get_ports clk]
	create_clock -add -name sys_clk_pin -period 10.00 -waveform {0 5} [get_ports clk]

#Buttons
set_property PACKAGE_PIN U18 [get_ports rst]						
	set_property IOSTANDARD LVCMOS33 [get_ports rst]

#LEDs	
set_property PACKAGE_PIN W3 [get_ports {Led[0]}]					
	set_property IOSTANDARD LVCMOS33 [get_ports {Led[0]}]
set_property PACKAGE_PIN U3 [get_ports {Led[1]}]					
	set_property IOSTANDARD LVCMOS33 [get_ports {Led[1]}]
set_property PACKAGE_PIN P3 [get_ports {Led[2]}]					
	set_property IOSTANDARD LVCMOS33 [get_ports {Led[2]}]
set_property PACKAGE_PIN N3 [get_ports {Led[3]}]					
	set_property IOSTANDARD LVCMOS33 [get_ports {Led[3]}]
set_property PACKAGE_PIN P1 [get_ports {Led[4]}]					
	set_property IOSTANDARD LVCMOS33 [get_ports {Led[4]}]
set_property PACKAGE_PIN L1 [get_ports {Led[5]}]					
	set_property IOSTANDARD LVCMOS33 [get_ports {Led[5]}]	
	
#switches for spi
set_property PACKAGE_PIN T2 [get_ports {switches[0]}]					
	set_property IOSTANDARD LVCMOS33 [get_ports {switches[0]}]
set_property PACKAGE_PIN R3 [get_ports {switches[1]}]					
	set_property IOSTANDARD LVCMOS33 [get_ports {switches[1]}]
set_property PACKAGE_PIN W2 [get_ports {switches[2]}]					
	set_property IOSTANDARD LVCMOS33 [get_ports {switches[2]}]
set_property PACKAGE_PIN U1 [get_ports {switches[3]}]					
	set_property IOSTANDARD LVCMOS33 [get_ports {switches[3]}]
set_property PACKAGE_PIN T1 [get_ports {switches[4]}]					
	set_property IOSTANDARD LVCMOS33 [get_ports {switches[4]}]
set_property PACKAGE_PIN R2 [get_ports {switches[5]}]					
	set_property IOSTANDARD LVCMOS33 [get_ports {switches[5]}]

#uart transfer and receive	
set_property PACKAGE_PIN B18 [get_ports cmd]						
	set_property IOSTANDARD LVCMOS33 [get_ports cmd]
set_property PACKAGE_PIN A18 [get_ports results]						
	set_property IOSTANDARD LVCMOS33 [get_ports results]	
	
#spi to DAC
#Sch name = JC1
set_property PACKAGE_PIN K17 [get_ports {cs}]					
	set_property IOSTANDARD LVCMOS33 [get_ports {cs}]
#Sch name = JC2
set_property PACKAGE_PIN M18 [get_ports {data_0}]					
	set_property IOSTANDARD LVCMOS33 [get_ports {data_0}]
#Sch name = JC3
set_property PACKAGE_PIN N17 [get_ports {data_1}]					
	set_property IOSTANDARD LVCMOS33 [get_ports {data_1}]
#Sch name = JC4
set_property PACKAGE_PIN P18 [get_ports {spi_clk}]					
	set_property IOSTANDARD LVCMOS33 [get_ports {spi_clk}]	
	
#I2C to ADC
#Sch name = JB3                                                                        
set_property PACKAGE_PIN B15 [get_ports {i2c_clk}]					
    set_property IOSTANDARD LVCMOS33 [get_ports {i2c_clk}]
#Sch name = JB4
set_property PACKAGE_PIN B16 [get_ports {data}]					
    set_property IOSTANDARD LVCMOS33 [get_ports {data}]
    set_property PULLTYPE {PULLUP} [get_ports {data}]	
	