library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity encoder is
  Port (clk, rst, i2done, done: in std_logic;
        data_in: in std_logic_vector(11 downto 0);
        start: out std_logic;
        data_out: out std_logic_vector(7 downto 0));
end encoder;

architecture Behavioral of encoder is


begin

data_out <= "11" & data_in(11 downto 6) when data_in(11 downto 6) = "111111" else --concat '11' at the end of numbers 111111
            "01" & data_in(11 downto 6) when data_in(11 downto 6) /= "111111"; -- concat '01' to the front of bits other than 111111
start <= i2done; 
  
end Behavioral;
