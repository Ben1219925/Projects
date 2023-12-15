library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity transmitter is
Port (data_in : in std_logic_vector(7 downto 0);
      load, clk, rst : in std_logic;
      data_out : out std_logic := '1';
      busy : out std_logic);
end transmitter;

architecture Behavioral of transmitter is
type state_type is (idle, transmit);
signal cs: state_type:=idle;
signal count_s : integer range 0 to 868 :=0;
signal bit_num_s : integer range 0 to 9 := 0;
signal clk_out_s : std_logic := '0';
signal busy_s : std_logic := '0';
signal done_s : std_logic := '0';
constant full_count : integer := 868;


begin
    process(clk,rst)
    begin
        if rst = '1' then
            cs <= idle;
        elsif rising_edge(clk) then
            case cs is
-------------------------IDLE----------------------------------------
                when idle =>
                    busy_s <= '0';
                    if load = '1' then
                        cs <= transmit;
                    else
                        cs <= idle;
                    end if;
-------------------------Transmit----------------------------------------
                when transmit =>
                    busy_s <= '1';
                    if done_s = '1' then
                        cs <= idle;
                    else
                        cs <= transmit;
                    end if;
-------------------------OTHERS----------------------------------------
                when others =>
                    cs <= idle;
            end case;
        end if;
        
    end process;
    
    process(clk,rst)
    begin
        if rst = '1' then
            count_s <= 0;
        elsif falling_edge(clk) then
            if busy_s = '1' then
                count_s <= count_s +1;
                if count_s = full_count then
                    count_s <= 0;
                    clk_out_s <= '1';
                else
                    clk_out_s <= '0'; 
                end if;
            else
                count_s <= count_s;
                clk_out_s <= '0';
            end if;
            
        end if;
    end process;


--counter to maintain correct speed
    process(clk,rst)
    begin
        if rst = '1' then
            bit_num_s <= 0;
        elsif rising_edge(clk) then
            done_s <= '0';
            if clk_out_s = '1' then
                if bit_num_s = 0 then
                    data_out <= '0';
                    bit_num_s <= 1;
                elsif bit_num_s = 9 then
                    data_out <= '1';
                    bit_num_s <= 0;
                    done_s <= '1';                
                else
                    data_out <= data_in(bit_num_s - 1);
                    bit_num_s <= bit_num_s + 1;
                end if;
                
            else
                bit_num_s <= bit_num_s;
            end if;
        end if;
    end process;
    
    busy <= busy_s; --top level busy signal
end Behavioral;
