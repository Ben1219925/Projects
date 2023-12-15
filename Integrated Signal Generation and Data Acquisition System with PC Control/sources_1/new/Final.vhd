library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity Final is
  Port (clk,rst,cmd: in std_logic;
        switches: in std_logic_vector(5 downto 0);
        results, data_0, data_1, spi_clk, cs, i2c_clk: out std_logic;
        data: inout std_logic;
        Led: out std_logic_vector(5 downto 0));
end Final;

architecture Behavioral of Final is
component main_control is
    Port(clk, rst, cmd_received, uart_busy, i2c_busy, spi_busy, spi_done: in std_logic;
         i2c_led_in: in std_logic_vector(5 downto 0);
         spi_led_in: in std_logic_vector(5 downto 0);
         i2c_cs_led: in std_logic_vector(3 downto 0);
         spi_cs_led: in std_logic_vector(1 downto 0);
         command: in std_logic_vector(7 downto 0);
         led_out: out std_logic_vector(5 downto 0);
         i2c_start, i2c_switch, spi_start, spi_switch: out std_logic);
end component;
component UART is
    Port(clk,rst,data_in, load: in std_logic;
         data_out, busy, done: out std_logic;
         encoded: in std_logic_vector(7 downto 0);
         led_data: out std_logic_vector(7 downto 0));
end component;
component encoder is
  Port (clk, rst, i2done, done: in std_logic;
        data_in: in std_logic_vector(11 downto 0);
        start: out std_logic;
        data_out: out std_logic_vector(7 downto 0));
end component;
component i2c is
  Port(clk, rst, start, switch: in std_logic;
       busy, i2c_clk: out std_logic;
       data: inout std_logic;
       LEDOut: out std_logic_vector(5 downto 0);
       cs_led: out std_logic_vector(3 downto 0);
       final_out: out std_logic_vector(11 downto 0);
       i2done : out std_logic);
end component;
component spi is
  Port (clk, rst, load, switch: in std_logic;
        switch_in: in std_logic_vector(5 downto 0);
        data_0, data_1, spi_clk, cs, finished: out std_logic;
        leds: out std_logic_vector(5 downto 0);
        cs_leds: out std_logic_vector(1 downto 0));
end component;

signal uart_busy_s, i2c_busy_s, spi_busy_s,i2c_start_s, i2c_switch_s, spi_start_s, spi_switch_s, store_s, done_s, received_s: std_logic;
signal command_s, encoded_s: std_logic_vector(7 downto 0);
signal spi_switches_s, i2c_led_s, spi_led_s: std_logic_vector(5 downto 0);
signal final_data_s : std_logic_vector(11 downto 0);
signal spi_cs_led_s: std_logic_vector(1 downto 0);
signal i2c_cs_led_s: std_logic_vector(3 downto 0);
signal i2done_s, start_s, spi_done_s : std_logic; 

begin

control: main_control port map(clk => clk,
                               rst => rst,
                               cmd_received => received_s,
                               uart_busy => uart_busy_s,
                               i2c_busy => i2c_busy_s,
                               spi_busy => spi_busy_s,
                               i2c_led_in => i2c_led_s,
                               spi_led_in => spi_led_s,
                               i2c_cs_led => i2c_cs_led_s,
                               spi_cs_led => spi_cs_led_s,
                               command => command_s,
                               i2c_start => i2c_start_s,
                               i2c_switch => i2c_switch_s,
                               spi_start => spi_start_s,
                               spi_done => spi_done_s,
                               spi_switch => spi_switch_s,
                               led_out => led);
                               
                               
computer: uart port map(clk => clk,
                        rst => rst,
                        data_in => cmd,
                        load => start_s,
                        data_out => results,
                        busy => uart_busy_s,
                        done => received_s,
                        encoded => encoded_s,
                        led_data => command_s);
                        
                        
encode: encoder port map(clk => clk,
                         rst => rst,
                         i2done => i2done_s,
                         done => uart_busy_s,
                         data_in => final_data_s,
                         start => start_s,
                         data_out => encoded_s);
                         
ad2: i2c port map(clk => clk,
                  rst => rst,
                  start => i2c_start_s,
                  switch => i2c_switch_s,
                  busy => i2c_busy_s,
                  i2c_clk => i2c_clk,
                  data => data,
                  LEDOut => i2c_led_s,
                  cs_led => i2c_cs_led_s,
                  final_out => final_data_s,
                  i2done => i2done_s);
                  
dac: spi port map(clk => clk,
                  rst => rst,
                  load => spi_start_s,
                  switch => spi_switch_s,
                  switch_in => spi_switches_s,
                  data_0 => data_0,
                  data_1 => data_1,
                  spi_clk => spi_clk,
                  cs => spi_busy_s,
                  finished => spi_done_s,
                  leds => spi_led_s,
                  cs_leds => spi_cs_led_s);
spi_switches_s <= switches;
cs <= spi_busy_s;
end Behavioral;
