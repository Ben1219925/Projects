library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity final_tb is
--  Port ( );
end final_tb;

architecture Behavioral of final_tb is
component Final is
  Port (clk,rst,cmd: in std_logic;
        switches: in std_logic_vector(5 downto 0);
        results, data_0, data_1, spi_clk, cs, i2c_clk: out std_logic;
        data: inout std_logic;
        Led: out std_logic_vector(5 downto 0));
end component;

signal clk_tb, rst_tb, cmd_tb, results_tb, data_0_tb, data_1_tb, spi_clk_tb, cs_tb, i2c_clk_tb, data_tb: std_logic := '0';
signal switches_tb, Led_tb: std_logic_vector(5 downto 0);
begin

uut: Final port map(clk => clk_tb,
                    rst => rst_tb,
                    cmd => cmd_tb,
                    results => results_tb,
                    data_0 => data_0_tb,
                    data_1 => data_1_tb,
                    spi_clk => spi_clk_tb,
                    cs => cs_tb,
                    i2c_clk => i2c_clk_tb,
                    data => data_tb,
                    switches => switches_tb,
                    Led => Led_tb);
                    
clk_tb <= not clk_tb after 5 ns;
                    
process
begin
    rst_tb <= '1';
    wait for 10 ns;
    rst_tb <= '0';
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '1';
    wait for 8680 ns;
    cmd_tb <= '1';
    wait for 8680 ns;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '1';
    wait for 8680 ns;
    data_tb <= 'Z';
    wait for 86 us;
    data_tb <= '0';
    wait for 10 us;
    data_tb <= 'Z';
    wait for 80 us;
    data_tb <= '0';
    wait for 10 us;
    data_tb <= 'Z';
    wait for 100 us;
    data_tb <= '0';
    wait for 50 us;
    data_tb <= '1';
    wait for 10 us;
    data_tb <= '0';
    wait for 10 us;
    data_tb <= '1';
    wait for 10 us;
    data_tb <= '0';
    wait for 10 us;
    data_tb <= '0';
    wait for 10 us;
    data_tb <= '1';
    wait for 10 us;
    data_tb <= '0';
    wait for 10 us;
    data_tb <= '1';
    wait for 10 us;
    data_tb <= '0';
    wait for 10 us;
    data_tb <= '1';
    wait for 10 us;
    data_tb <= '1';
    wait for 10 us;
    data_tb <= '0';
    wait for 10 us;
    data_tb <= '1';
    wait for 1 ms;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '1';
    wait for 1 ms;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '1';
    wait for 8680 ns;
    cmd_tb <= '1';
    wait for 8680 ns;
    cmd_tb <= '1';
    wait for 8680 ns;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '0';
    wait for 8680 ns;
    cmd_tb <= '1';
    wait for 8680 ns;
    data_tb <= 'Z';
    wait for 86 us;
    data_tb <= '0';
    wait for 10 us;
    data_tb <= 'Z';
    wait for 80 us;
    data_tb <= '0';
    wait for 10 us;
    data_tb <= 'Z';
    wait for 100 us;
    data_tb <= '0';
    wait for 50 us;
    data_tb <= '1';
    wait for 10 us;
    data_tb <= '0';
    wait for 10 us;
    data_tb <= '1';
    wait for 10 us;
    data_tb <= '0';
    wait for 10 us;
    data_tb <= '0';
    wait for 10 us;
    data_tb <= '1';
    wait for 10 us;
    data_tb <= '0';
    wait for 10 us;
    data_tb <= '1';
    wait for 10 us;
    data_tb <= '0';
    wait for 10 us;
    data_tb <= '1';
    wait for 10 us;
    data_tb <= '1';
    wait for 10 us;
    data_tb <= '0';
    wait for 10 us;
    data_tb <= '1';
    wait for 1 ms;
    
    

wait;
end process;

end Behavioral;
