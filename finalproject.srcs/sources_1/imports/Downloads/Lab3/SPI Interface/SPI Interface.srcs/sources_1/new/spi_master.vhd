library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity spi_master is
-- spi_clk_f is limited to 30 MHz for DA2
--generic(m_clk_f : in integer := 100e6;
--        spi_clk_f : in integer := 10e6);

port (clk : in std_logic; -- clock input
      load : in std_logic; -- notification to send data
      rst : in std_logic;
      data_in : in std_logic_vector(15 downto 0); -- pdata in
      sdata_0 : out std_logic; -- serial data out 1
      sdata_1 : out std_logic; -- serial data out 2
      spi_clk : out std_logic; -- clk out to SPI devices
      CS0_n, finished : out std_logic;
      cs_leds: out std_logic_vector(1 downto 0)); -- chip select 1, active low
end spi_master;

architecture Behavioral of spi_master is
type state_type is (idle, transmit1, transmit2);
signal cs: state_type:=idle;
signal count_s: integer range 0 to 10 := 0;
signal bit_num_s : integer range 0 to 16 := 16;
signal done: std_logic := '0';
signal sdata_0_s, sdata_1_s, spi_clk_s, CS0_n_s, count_en, finished_s: std_logic;
constant count: integer := 10;
begin
process(clk,rst)
    begin
        if rst = '1' then
            cs <= idle;
            sdata_0_s <= '0';
            sdata_1_s <= '0';
            spi_clk_s <= '0';
            CS0_n_s <= '1';
            finished_s <= '0';
        elsif rising_edge(clk) then
            case cs is
-------------------------IDLE----------------------------------------            
                when idle =>
                    cs_leds <= "01";
                    CS0_n_s <= '1';
                    count_en <= '0';
                    spi_clk_s <= '0';
                    finished_s <= '0';
                    if load = '1' then
                        cs <= transmit1;
                    else
                        cs <= idle;                                            
                    end if;
-------------------------TRANSMIT1----------------------------------------
                when transmit1 =>    
                    cs_leds <= "10";                
                    cs0_n_s <= '0';
                    count_en <= '1';
                    if bit_num_s = 0 then
                        cs <= idle;
                        bit_num_s <= 16;
                        finished_s <= '1';
                    elsif done = '1' then
                        cs <= transmit2;
                        spi_clk_s <= '1';
                    else
                        cs <= transmit1;
                    end if;
-------------------------TRANSMIT2----------------------------------------
                when transmit2 =>
                    cs_leds <= "10";
                    sdata_0_s <= data_in(bit_num_s-1);
                    sdata_1_s <= data_in(bit_num_s-1); 
                    if done = '1' then
                        cs <= transmit1;
                        bit_num_s <= bit_num_s - 1;
                        spi_clk_s <= '0';
                    else
                        cs <= transmit2;                            
                    end if;                        
        end case;
    end if;
                    
end process;

--CLOCK DIVIDER FOR 10MHZ
process(clk,rst)
    begin
        if rst = '1' then
            count_s <= 0;
        elsif falling_edge(clk) then
            done <= '0';
            if count_en = '1' then
                if count_s = count then
                    done <= '1';
                    count_s <= 0;
                else
                    count_s <= count_s + 1;
                end if;
            else
                count_s <= 0;
            end if;            
        end if;
end process;

sdata_0 <= sdata_0_s;
sdata_1 <= sdata_1_s;
spi_clk <= spi_clk_s;
CS0_n <= CS0_n_s;
finished <= finished_s;

end Behavioral;
