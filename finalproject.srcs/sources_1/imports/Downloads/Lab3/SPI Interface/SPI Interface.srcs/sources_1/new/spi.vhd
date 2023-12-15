library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

-- Uncomment the following library declaration if instantiating
-- any Xilinx leaf cells in this code.
--library UNISIM;
--use UNISIM.VComponents.all;

entity spi is
  Port (clk, rst, load, switch: in std_logic;
        switch_in: in std_logic_vector(5 downto 0);
        data_0, data_1, spi_clk, cs, finished: out std_logic;
        leds: out std_logic_vector(5 downto 0);
        cs_leds: out std_logic_vector(1 downto 0));
end spi;

architecture Behavioral of spi is
component spi_master is
port (clk : in std_logic; -- clock input
      load : in std_logic; -- notification to send data
      rst : in std_logic;
      data_in : in std_logic_vector(15 downto 0); -- pdata in
      sdata_0 : out std_logic; -- serial data out 1
      sdata_1 : out std_logic; -- serial data out 2
      spi_clk : out std_logic; -- clk out to SPI devices
      CS0_n, finished : out std_logic;
      cs_leds: out std_logic_vector(1 downto 0)); -- chip select 1, active low
end component;

component blk_mem_gen_0 IS
  PORT (
    clka : IN STD_LOGIC;
    ena : IN STD_LOGIC;
    wea : IN STD_LOGIC_VECTOR(0 DOWNTO 0);
    addra : IN STD_LOGIC_VECTOR(16 DOWNTO 0);
    dina : IN STD_LOGIC_VECTOR(11 DOWNTO 0);
    douta : OUT STD_LOGIC_VECTOR(11 DOWNTO 0)
  );
END component;

signal data_out: std_logic_vector(15 downto 0);
signal addr : std_logic_vector(16 downto 0);
signal block_out: std_logic_vector(11 downto 0);
signal done: std_logic := '0';
signal count_s: integer range 0 to 160 := 0;
constant full_count: integer := 160;
constant addr_max: integer:= 100000;
signal address: integer range 0 to addr_max;

begin
master: spi_master port map(clk => clk,
                            load => load,
                            rst => rst,
                            data_in => data_out,
                            sdata_0 => data_0,
                            sdata_1 => data_1,
                            spi_clk => spi_clk,
                            cs0_n => cs,
                            finished => finished,
                            cs_leds => cs_leds);                          

RAM: blk_mem_gen_0 port map(clka => clk,
                            ena => '1',
                            wea => "0",
                            addra => addr,
                            dina => x"000",
                            douta => block_out);
addr <= std_logic_vector(to_unsigned(address, 17));                        
                                                               
process(clk,rst)
begin
    if rst = '1' then
        address <= 0;
    elsif rising_edge(clk) then
        if switch = '0' then
            address <= 0;
        else
            if address >= addr_max then
                address <= 0;
            else
                if done = '1' then
                    address <= address + 1;
                else
                    address <= address;
                end if;
            end if;
        end if;
    end if;
end process;    

process(clk,rst)
    begin
        if rst = '1' then
            count_s <= 0;
        elsif falling_edge(clk) then
            done <= '0';
            if load = '1' then
                if count_s = full_count then
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
                    
leds <= switch_in when switch = '0' else block_out(11 downto 6);
data_out(15 downto 12) <= x"0";
data_out(11 downto 6) <= switch_in when switch = '0' else block_out(11 downto 6);
data_out(5 downto 0) <= "000000" when switch = '0' else block_out(5 downto 0);

end behavioral;