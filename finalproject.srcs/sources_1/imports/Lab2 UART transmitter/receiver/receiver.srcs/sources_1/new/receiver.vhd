library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity receiver is
  Port (data,clk,rst : in std_logic;
        done : out std_logic;
        led_data : out std_logic_vector(7 downto 0));
end receiver;

architecture Behavioral of receiver is
component clock_div is
--full_l = 1 means look for full count, 0 means look for half count
  Port (clk,rst, full_l, count_en: in std_logic;
        clk_out, half_count_done : out std_logic);
end component;
component shifter is
  Port (shift, clk, data, rst : in std_logic;
        done : out std_logic;
        pdata : out std_logic_vector(7 downto 0));
end component;
component controller is
  Port (data : in std_logic := '1';
        clk, rst, done, half_count_done : in std_logic;
        full_l, count_en: out std_logic);
end component;

signal full_l_s, shift_s, done_s,half_count_done_s, count_en_s : std_logic;


begin
clk_div: clock_div port map(clk => clk,
                            rst => rst,
                            full_l => full_l_s,
                            clk_out => shift_s,
                            half_count_done => half_count_done_s,
                            count_en => count_en_s);
                            
data_shift: shifter port map(shift => shift_s,
                             clk => clk,
                             data => data,
                             rst => rst,
                             done => done_s,
                             pdata => led_data);
                             
control: controller port map(data => data,
                             clk => clk,
                             rst => rst,
                             done => done_s,
                             half_count_done => half_count_done_s,
                             full_l => full_l_s,
                             count_en => count_en_s);
done <= done_s;

end Behavioral;
