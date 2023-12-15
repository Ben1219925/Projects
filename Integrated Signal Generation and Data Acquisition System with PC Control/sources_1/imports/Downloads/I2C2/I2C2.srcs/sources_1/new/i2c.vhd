library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
library UNISIM;
use UNISIM.VComponents.all;

entity i2c is
  Port(clk, rst, start, switch: in std_logic;
       busy, i2c_clk: out std_logic;
       data: inout std_logic;
       LEDOut: out std_logic_vector(5 downto 0);
       cs_led: out std_logic_vector(3 downto 0);
       final_out: out std_logic_vector(11 downto 0);
       i2done : out std_logic);
end i2c;

architecture Behavioral of i2c is
component controller1 is
Port (clk, rst, start, dataIn, switch: in std_logic;
      read, busy, addr, i2c_clk: out std_logic;
      cs_led: out std_logic_vector(3 downto 0);
      dataOut: out std_logic_vector(17 downto 0);
      i2done : out std_logic);
end component;

component tristate is
  Port (read, dataIn : in std_logic;
        DataBUS : inout std_logic;  -- needs to be initialized in TB as High Impedence
        IntBus : out std_logic);
end component;

signal read_s, data_s, addr_s: std_logic;
signal dataOut_s: std_logic_vector(17 downto 0);


begin
control: controller1 port map(clk => clk,
                             rst => rst,
                             start => start,
                             dataIn => data_s,
                             switch => switch,
                             read => read_s,
                             busy => busy,
                             addr => addr_s,
                             i2c_clk => i2c_clk,
                             cs_led => cs_led,
                             dataOut => dataOut_s,
                             i2done => i2done);
                             
tri: tristate port map(read => read_s,
                       dataIn => addr_s,
                       DataBUS => data,
                       IntBus => data_s);
                       
LEDOut <= dataOut_s(12 downto 9) & dataOut_s(7 downto 6);
final_out <= dataOut_s(12 downto 9) & dataOut_s(7 downto 0);

end Behavioral;
