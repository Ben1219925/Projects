library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity UART is
    Port(clk,rst,data_in, load: in std_logic;
         data_out, busy, done: out std_logic;
         encoded: in std_logic_vector(7 downto 0);
         led_data: out std_logic_vector(7 downto 0));
end UART;

architecture Behavioral of UART is
component transmitter is
Port (data_in : in std_logic_vector(7 downto 0);
      load, clk, rst : in std_logic;
      data_out : out std_logic := '1';
      busy : out std_logic);
end component;
component receiver is
  Port (data,clk,rst : in std_logic;
        done : out std_logic;
        led_data : out std_logic_vector(7 downto 0));
end component;

begin                          
receive: receiver port map(data => data_in,
                           clk => clk,
                           rst => rst,
                           done => done,
                           led_data => led_data);
                                                     
transmit: transmitter port map(data_in => encoded,
                               load => load,
                               clk => clk,
                               rst => rst,
                               data_out => data_out,
                               busy => busy);


end Behavioral;
