library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity controller is
  Port (data : in std_logic := '1';
        clk, rst, done, half_count_done : in std_logic;
        full_l, count_en: out std_logic:= '0');
end controller;

architecture Behavioral of controller is
type state_type is (idle, start_bit, save_data);
signal cs: state_type:=idle;
begin
    process(clk,rst)
    begin
        if rst = '1' then
            cs <= idle;
            full_l <= '0';
            count_en <= '0';
        elsif rising_edge(clk) then
            case cs is
-------------------------IDLE----------------------------------------
                when idle =>
                    count_en <= '0';
                    if data = '0' then
                        cs <= start_bit;
                        count_en <= '1';
                        full_l <= '0';
                    else
                        cs <= idle;
                    end if;
-------------------------START_BIT----------------------------------------
                when start_bit =>
                    if half_count_done = '1' then
                        cs <= save_data;
                        full_l <= '1';
                    else
                        cs <= start_bit;
                    end if;
-------------------------SAVE_DATA----------------------------------------
                when save_data =>
                    if done = '1' then
                        cs <= idle;
                    else
                        cs <= save_data;
                    end if;
-------------------------OTHERS----------------------------------------
                when others =>
                    cs <= idle;
            end case;
        end if;
    end process;
    
end Behavioral;