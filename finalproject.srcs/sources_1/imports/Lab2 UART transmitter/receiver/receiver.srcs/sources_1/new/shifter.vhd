library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity shifter is
  Port (shift, clk, data, rst : in std_logic;
        done : out std_logic;
        pdata : out std_logic_vector(7 downto 0));
end shifter;

architecture Behavioral of shifter is
    signal bit_num_s : integer range 0 to 8 := 0;
begin
    process(clk,rst)
    begin
        if rst = '1' then
            pdata <= "00000000";
            bit_num_s <= 0;
            done <= '0';
        elsif rising_edge(clk) then
            if shift = '1' then
                if bit_num_s = 8 then
                    bit_num_s <= 0;
                    done <= '1';
                else
                    pdata(bit_num_s) <= data;
                    bit_num_s <= bit_num_s +1;
                    done <= '0';
                end if;
            else
                bit_num_s <= bit_num_s;
                done <= '0';
            end if;
        end if;
    end process;

end Behavioral;