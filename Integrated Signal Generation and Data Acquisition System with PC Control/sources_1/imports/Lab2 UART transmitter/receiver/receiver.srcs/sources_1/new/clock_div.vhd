library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity clock_div is
--full_l = 1 means look for full count, 0 means look for half count
  Port (clk,rst, full_l, count_en: in std_logic;
        clk_out, half_count_done : out std_logic);
end clock_div;

architecture Behavioral of clock_div is

constant full_count : integer := 868; --count between data reads
constant half_count : integer := 434; --setting up the clock
signal count_s : integer range 0 to 868 :=0;

begin
    process(clk,rst)
    begin
        if rst = '1' then
            count_s <= 0;
        elsif falling_edge(clk) then
            if count_en = '1' then
                count_s <= count_s +1;
                if full_l = '0' then
                    if count_s = half_count then
                        half_count_done <= '1';
                        count_s <= 0;
                    else
                        half_count_done <= '0';
                    end if;
                elsif full_l = '1' then
                    if count_s = full_count then
                        clk_out <= '1';
                        count_s <= 0;
                    else
                        clk_out <= '0';
                    end if;
                end if;
            else
                count_s <= 0;
            end if;
        end if;
            
    end process;
    
end Behavioral;
